import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-3.6-flash"


def ask_ai(prompt):
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text


def evaluate_answer(question, answer):
    prompt = f"""
You are a senior technical interviewer.

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer honestly.

Return in this format:

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

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text