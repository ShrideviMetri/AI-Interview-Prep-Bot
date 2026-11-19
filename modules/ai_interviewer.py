
import os
import time
import requests

from dotenv import load_dotenv
from google import genai

load_dotenv()

# =====================================================
# GEMINI CONFIGURATION
# =====================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = (
    genai.Client(api_key=GEMINI_API_KEY)
    if GEMINI_API_KEY
    else None
)

GEMINI_MODEL = "gemini-3.5-flash-lite"


# =====================================================
# OLLAMA CONFIGURATION
# =====================================================

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2:latest"
)


# Tracks the provider used for the latest request
LAST_PROVIDER = "Not used"


def get_last_provider():
    return LAST_PROVIDER


# =====================================================
# ERROR DETECTION
# =====================================================

def get_error_status(error):
    """Extract HTTP status from Gemini exceptions."""

    for value in (
        getattr(error, "code", None),
        getattr(error, "status_code", None),
        getattr(getattr(error, "response", None), "status_code", None)
    ):
        try:
            if value is not None:
                return int(value)
        except (TypeError, ValueError):
            continue

    return None


def is_authentication_error(error):
    status = get_error_status(error)
    message = str(error).lower()

    return (
        status in (401, 403)
        or "api_key_invalid" in message
        or "invalid api key" in message
        or "unauthorized" in message
        or "permission denied" in message
    )



def is_rate_limit_error(error):
    status = get_error_status(error)
    message = str(error).lower()

    return (
        status == 429
        or "429" in message
        or "resource_exhausted" in message
        or "resource exhausted" in message
        or "quota exceeded" in message
        or "rate limit" in message
        or "too many requests" in message
    )



def is_temporary_server_error(error):
    status = get_error_status(error)
    message = str(error).lower()

    return (
        status in (500, 502, 503, 504)
        or "service unavailable" in message
        or "internal server error" in message
        or "bad gateway" in message
        or "gateway timeout" in message
        or "server error" in message
    )


def is_network_error(error):
    """Identify temporary network errors from the Gemini SDK."""

    error_type = type(error).__name__

    network_error_types = {
        "TimeoutException",
        "ConnectError",
        "ConnectTimeout",
        "ReadTimeout",
        "WriteTimeout",
        "NetworkError",
        "RemoteProtocolError"
    }

    message = str(error).lower()

    return (
        isinstance(error, (TimeoutError, ConnectionError))
        or error_type in network_error_types
        or "timed out" in message
        or "connection reset" in message
        or "temporary failure in name resolution" in message
        or "network is unreachable" in message
    )


# =====================================================
# OLLAMA GENERATION
# =====================================================

 
def ask_ollama(prompt):
    """Generate a response using local Ollama."""

    print("Switching to Ollama...")

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=(10, 180)
        )

        if response.status_code == 404:
            raise RuntimeError(
                f"Model '{OLLAMA_MODEL}' not found. "
                f"Run: ollama pull {OLLAMA_MODEL}"
            )

        response.raise_for_status()

        result = response.json()

        if result.get("error"):
            raise RuntimeError(result["error"])

        answer = result.get("response", "").strip()

        if not answer:
            raise RuntimeError("Ollama returned an empty response.")

        return answer

    except requests.exceptions.HTTPError as error:
        details = response.text
        raise RuntimeError(
            f"Ollama HTTP error: {response.status_code}. "
            f"Details: {details}"
        ) from error

    except requests.exceptions.ConnectionError as error:
        raise RuntimeError(
            "Cannot connect to Ollama. Check whether Ollama is running."
        ) from error

    except requests.exceptions.Timeout as error:
        raise RuntimeError("Ollama request timed out.") from error

    except requests.exceptions.RequestException as error:
        raise RuntimeError(f"Ollama connection error: {error}") from error


# =====================================================
# GEMINI + OLLAMA PROVIDER MANAGER
# =====================================================

def generate_ai_response(prompt):
    """
    Try Gemini first.
    Retry temporary failures once.
    Switch to Ollama for rate limits and temporary failures.
    """

    global LAST_PROVIDER

    LAST_PROVIDER = "Not used"

    if not GEMINI_API_KEY or client is None:
        LAST_PROVIDER = "Configuration error"

        return (
            "⚠️ Gemini API key is missing. "
            "Please check GEMINI_API_KEY in your .env file."
        )

    for attempt in range(2):

        try:
            print("Using Gemini...")

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

            if not response.text:
                LAST_PROVIDER = "Gemini"
                return "⚠️ Gemini returned an empty response."

            LAST_PROVIDER = "Gemini"

            print("Gemini response generated successfully.")

            return response.text

        except Exception as error:

            print(f"Gemini error: {error}")

            # Invalid API key or permission error
            if is_authentication_error(error):
                LAST_PROVIDER = "Configuration error"

                return (
                    "⚠️ Gemini authentication failed. "
                    "Please check your API key and permissions."
                )

            # Rate limit: switch immediately
            if is_rate_limit_error(error):
                print("Gemini rate limit reached.")
                break

            # Temporary server/network errors: retry once
            if (
                is_temporary_server_error(error)
                or is_network_error(error)
            ):

                if attempt == 0:
                    print("Temporary Gemini error. Retrying once...")
                    time.sleep(2)
                    continue

                print("Gemini retry failed. Switching to Ollama...")
                break

            # Other errors: do not silently switch
            LAST_PROVIDER = "Gemini error"

            return f"⚠️ Gemini API error: {error}"

    # =================================================
    # FALLBACK TO OLLAMA
    # =================================================

    try:
        result = ask_ollama(prompt)

        LAST_PROVIDER = "Ollama"

        print("Ollama response generated successfully.")

        return result

    except Exception as ollama_error:

        LAST_PROVIDER = "Unavailable"

        print(f"Ollama fallback failed: {ollama_error}")

        return (
            "⚠️ Gemini is temporarily unavailable, "
            "and Ollama could not generate a response.\n\n"
            f"Reason: {ollama_error}"
        )


# =====================================================
# INTERVIEW QUESTION GENERATION
# =====================================================

def ask_ai(prompt):
    return generate_ai_response(prompt)


# =====================================================
# ANSWER EVALUATION
# =====================================================

def evaluate_answer(question, answer):

    prompt = f"""
You are a senior technical interviewer.

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer.

Return ONLY in this format:

Score: X/10

Strengths:
- ...

Weaknesses:
- ...

Ideal Answer:
...

Improvement Tips:
- ...
"""

    return generate_ai_response(prompt)


# =====================================================
# RESUME ANALYSIS
# =====================================================

def analyze_resume(resume_text):

    prompt = f"""
You are an expert technical recruiter.

Analyze the following resume.

Resume:
{resume_text}

Extract ONLY these sections.

Skills:
Projects:
Programming Languages:
Frameworks:
Databases:
Tools:
Experience:
"""

    return generate_ai_response(prompt)


