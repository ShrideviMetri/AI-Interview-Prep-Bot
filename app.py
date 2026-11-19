
import streamlit as st
import hashlib
import re
from difflib import SequenceMatcher

from modules.ai_interviewer import (
    ask_ai,
    evaluate_answer,
    analyze_resume,
    get_last_provider
)

from modules.pdf_reader import extract_text_from_pdf


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AI Interview Prep Bot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Interview Prep Bot")

st.write(
    "Practice technical interviews with AI. "
    "Upload your resume or select your preferred interview settings."
)


# =====================================================
# SESSION STATE INITIALIZATION
# =====================================================

defaults = {
    "started": False,
    "question_no": 1,
    "current_question": "",
    "resume_summary": "",
    "resume_text": "",
    "feedback": "",
    "total_questions": 5,
    "resume_provider": "",
    "question_provider": "",
    "feedback_provider": "",
    "resume_file_signature": None,
    "asked_questions": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================================
# INTERVIEW SETTINGS
# =====================================================

st.subheader("Interview Settings")

role = st.selectbox(
    "Select Job Role",
    [
        "Select Job Role",
        "Python Developer",
        "Java Developer",
        "Frontend Developer",
        "Backend Developer",
        "AI/ML Engineer",
        "Data Analyst",
        "HR Interview"
    ],
    index=0
)

difficulty = st.selectbox(
    "Select Difficulty",
    [
        "Select Difficulty",
        "Easy",
        "Medium",
        "Hard"
    ],
    index=0
)

total_questions = st.selectbox(
    "Number of Questions",
    [
        "Select Number of Questions",
        5,
        10,
        15
    ],
    index=0
)

st.divider()


# =====================================================
# RESUME UPLOAD
# =====================================================

st.subheader("📄 Upload Your Resume")

uploaded_resume = st.file_uploader(
    "Upload your resume in PDF format",
    type=["pdf"],
    key="resume_uploader"
)


# =====================================================
# PROCESS RESUME
# =====================================================

if uploaded_resume is not None:

    pdf_bytes = uploaded_resume.getvalue()

    file_signature = hashlib.sha256(pdf_bytes).hexdigest()

    if file_signature != st.session_state.resume_file_signature:

        # Reset previous interview and resume information
        st.session_state.resume_text = ""
        st.session_state.resume_summary = ""
        st.session_state.resume_provider = ""

        st.session_state.started = False
        st.session_state.question_no = 1
        st.session_state.current_question = ""
        st.session_state.feedback = ""
        st.session_state.asked_questions = []

        st.session_state.resume_file_signature = file_signature

        try:

            with st.spinner("Reading your resume..."):

                st.session_state.resume_text = (
                    extract_text_from_pdf(uploaded_resume)
                )

            if not st.session_state.resume_text.strip():

                st.error("No readable text found in the PDF.")

                st.session_state.resume_file_signature = None

            else:

                with st.spinner("Analyzing your resume..."):

                    summary = analyze_resume(
                        st.session_state.resume_text
                    )

                    st.session_state.resume_provider = (
                        get_last_provider()
                    )

                if not summary or summary.startswith("⚠️"):

                    st.error(
                        summary or "Resume analysis failed."
                    )

                    st.session_state.resume_summary = ""

                else:

                    st.session_state.resume_summary = summary

                    st.success(
                        "✅ Resume uploaded and analyzed successfully!"
                    )

        except Exception as e:

            st.error(f"Could not read the uploaded PDF: {e}")

            st.session_state.resume_text = ""
            st.session_state.resume_summary = ""


    # Display resume analysis

    if st.session_state.resume_summary:

        st.subheader("📋 Resume Analysis")

        st.write(st.session_state.resume_summary)

        st.caption(
            f"Resume analysis provider: "
            f"{st.session_state.resume_provider}"
        )

        with st.expander("View Extracted Resume Text"):

            st.text(st.session_state.resume_text)


# Handle resume removal

elif st.session_state.resume_file_signature is not None:

    st.session_state.resume_file_signature = None

    st.session_state.resume_text = ""
    st.session_state.resume_summary = ""
    st.session_state.resume_provider = ""

    st.session_state.started = False
    st.session_state.question_no = 1
    st.session_state.current_question = ""
    st.session_state.feedback = ""
    st.session_state.asked_questions = []


st.divider()


# =====================================================
# QUESTION DUPLICATE CHECK
# =====================================================

def normalize_question(question):

    question = question.lower().strip()

    question = re.sub(r"[^a-z0-9\s]", "", question)

    question = re.sub(r"\s+", " ", question)

    return question


def is_duplicate_question(new_question):

    new_normalized = normalize_question(new_question)

    for previous_question in st.session_state.asked_questions:

        previous_normalized = normalize_question(previous_question)

        similarity = SequenceMatcher(
            None,
            new_normalized,
            previous_normalized
        ).ratio()

        if similarity >= 0.80:
            return True

    return False


# =====================================================
# GENERATE INTERVIEW QUESTION
# =====================================================

def generate_question():

    previous_questions = "\n".join(
        f"- {question}"
        for question in st.session_state.asked_questions
    )

    # CASE 1: RESUME-BASED INTERVIEW

    if st.session_state.resume_text.strip():

        prompt = f"""
You are a senior technical interviewer.

Generate ONE NEW interview question based ONLY on the
candidate's uploaded resume.

Resume Analysis:
{st.session_state.resume_summary}

Question Number:
{st.session_state.question_no}

PREVIOUSLY ASKED QUESTIONS:
{previous_questions if previous_questions else "None"}

STRICT RULES:

1. Generate a completely new question.
2. Never repeat a previously asked question.
3. Do not ask the same question using different wording.
4. Explore different skills, projects, technologies
   and experiences from the resume.
5. Do not assume a job role.
6. Do not provide hints or answers.
7. Return ONLY the interview question.
"""

    # CASE 2: ROLE-BASED INTERVIEW

    else:

        prompt = f"""
You are a senior technical interviewer.

Interview Role:
{role}

Difficulty:
{difficulty}

Question Number:
{st.session_state.question_no}

PREVIOUSLY ASKED QUESTIONS:
{previous_questions if previous_questions else "None"}

STRICT RULES:

1. Generate a completely new interview question.
2. Never repeat a previously asked question.
3. Do not ask the same question using different wording.
4. Explore different topics related to the selected role.
5. Follow the selected difficulty.
6. Do not provide hints or answers.
7. Return ONLY the interview question.
"""

    # Try up to 3 times to get a unique question

    for attempt in range(3):

        question = ask_ai(prompt)

        provider = get_last_provider()

        if not question or question.startswith("⚠️"):
            return question or "⚠️ Could not generate a question."

        if not is_duplicate_question(question):

            st.session_state.asked_questions.append(question)

            st.session_state.question_provider = provider

            return question

        print(
            f"Duplicate question detected. "
            f"Regeneration attempt: {attempt + 1}"
        )

        prompt += f"""

IMPORTANT:
Your previous generated question was too similar to an
earlier question.

Generate a DIFFERENT question covering another topic.
Do not repeat or rephrase previous questions.
"""

    return (
        "⚠️ Could not generate a sufficiently different question "
        "after 3 attempts. Please try generating again."
    )


# =====================================================
# START INTERVIEW
# =====================================================

if not st.session_state.started:

    if st.button("🚀 Start Interview", type="primary"):

        resume_available = bool(
            st.session_state.resume_text.strip()
            and st.session_state.resume_summary.strip()
        )

        # Resume-based interview
        if resume_available:

            st.session_state.total_questions = (
                total_questions
                if isinstance(total_questions, int)
                else 5
            )

        # Role-based interview
        else:

            if role == "Select Job Role":

                st.warning("Please select a job role.")

            elif difficulty == "Select Difficulty":

                st.warning("Please select a difficulty level.")

            elif not isinstance(total_questions, int):

                st.warning("Please select the number of questions.")

            else:

                st.session_state.total_questions = total_questions

        # Start only when valid settings are available

        if resume_available or (
            role != "Select Job Role"
            and difficulty != "Select Difficulty"
            and isinstance(total_questions, int)
        ):

            # Reset history only for a new interview

            st.session_state.asked_questions = []

            st.session_state.question_no = 1

            st.session_state.feedback = ""

            st.session_state.current_question = ""

            with st.spinner("Generating Interview Question..."):

                question = generate_question()

            if question and not question.startswith("⚠️"):

                st.session_state.current_question = question

                st.session_state.started = True

                st.rerun()

            else:

                st.error(
                    question or "Could not generate an interview question."
                )


# =====================================================
# INTERVIEW SCREEN
# =====================================================

if st.session_state.started:

    st.divider()

    st.subheader(
        f"Question {st.session_state.question_no} / "
        f"{st.session_state.total_questions}"
    )

    st.info(st.session_state.current_question)

    st.caption(
        f"Question generated by: "
        f"{st.session_state.question_provider}"
    )

    answer = st.text_area(
        "💬 Your Answer",
        height=200,
        key=f"answer_{st.session_state.question_no}"
    )


    # =================================================
    # EVALUATE ANSWER
    # =================================================

    if st.button("Evaluate Answer"):

        if not answer.strip():

            st.warning("Please enter your answer.")

        else:

            with st.spinner("Evaluating your answer..."):

                feedback = evaluate_answer(
                    st.session_state.current_question,
                    answer
                )

                st.session_state.feedback = feedback

                st.session_state.feedback_provider = (
                    get_last_provider()
                )

            if feedback.startswith("⚠️"):

                st.error(feedback)

            else:

                st.success("Answer evaluated successfully!")


    # =================================================
    # DISPLAY FEEDBACK
    # =================================================

    if st.session_state.feedback:

        st.subheader("📊 AI Feedback")

        st.write(st.session_state.feedback)

        st.caption(
            f"Evaluation provider: "
            f"{st.session_state.feedback_provider}"
        )


    st.divider()


    # =================================================
    # NEXT QUESTION
    # =================================================

    if (
        st.session_state.question_no
        < st.session_state.total_questions
    ):

        if st.button("➡️ Next Question"):

            previous_question_no = st.session_state.question_no

            st.session_state.question_no += 1

            st.session_state.feedback = ""

            st.session_state.feedback_provider = ""

            with st.spinner("Generating Next Question..."):

                question = generate_question()

            if question and not question.startswith("⚠️"):

                st.session_state.current_question = question

                st.rerun()

            else:

                st.session_state.question_no = previous_question_no

                st.error(
                    question or "Could not generate the next question."
                )


    # =================================================
    # INTERVIEW COMPLETED
    # =================================================

    else:

        if (
            st.session_state.feedback
            and not st.session_state.feedback.startswith("⚠️")
        ):

            st.success("🎉 Interview Completed!")

        if st.button("🔄 Start New Interview"):

            st.session_state.started = False

            st.session_state.question_no = 1

            st.session_state.current_question = ""

            st.session_state.feedback = ""

            st.session_state.question_provider = ""

            st.session_state.feedback_provider = ""

            st.session_state.asked_questions = []

            st.rerun()
