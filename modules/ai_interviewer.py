import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-3.5-flash-lite"


def ask_ai(prompt):

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text

    except Exception:

        return "⚠️ Gemini rate limit reached. Please wait 30 seconds and try again."


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

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text

    except Exception:

        return "⚠️ Gemini rate limit reached. Please wait 30 seconds and try again."

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

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text

    except Exception:

        return "⚠️ Resume analysis failed because the Gemini API rate limit was reached. Please wait 30 seconds and upload the resume again."