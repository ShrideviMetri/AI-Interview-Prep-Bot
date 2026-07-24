
import streamlit as st
from modules.ai_interviewer import (
    ask_ai, 
    evaluate_answer,
    analyze_resume
)
from modules.pdf_reader import extract_text_from_pdf
# ---------------- Page Config ---------------- #

st.set_page_config(
    page_title="AI Interview Prep Bot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Interview Prep Bot")
st.write("Practice technical interviews with AI.")

# ---------------- Session State ---------------- #

if "started" not in st.session_state:
    st.session_state.started = False

if "question_no" not in st.session_state:
    st.session_state.question_no = 1

if "current_question" not in st.session_state:
    st.session_state.current_question = ""
    
if "resume_summary" not in st.session_state:
    st.session_state.resume_summary = ""

# ---------------- Inputs ---------------- #

role = st.selectbox(
    "Select Job Role",
    [
        "Python Developer",
        "Java Developer",
        "Frontend Developer",
        "Backend Developer",
        "AI/ML Engineer",
        "Data Analyst",
        "HR Interview"
    ]
)

difficulty = st.selectbox(
    "Select Difficulty",
    ["Easy", "Medium", "Hard"]
)

total_questions = st.selectbox(
    "Number of Questions",
    [5, 10, 15]
)

st.divider()

uploaded_resume = st.file_uploader(
    "📄 Upload Your Resume (PDF)",
    type=["pdf"]
)

resume_text = ""

if uploaded_resume is not None:

    

    if st.session_state.resume_summary == "":

        resume_text = extract_text_from_pdf(uploaded_resume)

        with st.spinner("Analyzing resume..."):
            st.session_state.resume_summary = analyze_resume(resume_text)

    st.subheader("📋 Resume Analysis")
    st.write(st.session_state.resume_summary)
    st.subheader("📋 Resume Analysis")

    st.write(st.session_state.resume_summary)
    st.success("✅ Resume uploaded successfully!")

    with st.expander("View Extracted Resume Text"):

        st.text(resume_text)
        
# ---------------- Generate Question ---------------- #

def generate_question():
  prompt = f"""
You are a senior technical interviewer.

Interview Role:
{role}

Difficulty:
{difficulty}

Question Number:
{st.session_state.question_no}

Resume Analysis:
{st.session_state.resume_summary}

Rules:

If the resume is provided:
- Generate ONE interview question based ONLY on the resume.
- Focus on the candidate's skills, projects, technologies, and experience.

If no resume is provided:
- Generate a normal interview question for the selected role.

Do NOT provide hints.
Do NOT provide answers.
Return ONLY the question.
"""
  return ask_ai(prompt)

# ---------------- Start Interview ---------------- #

if not st.session_state.started:

    if st.button("🚀 Start Interview"):

        with st.spinner("Generating Question..."):

            st.session_state.current_question = generate_question()

        st.session_state.started = True

        st.rerun()

# ---------------- Interview ---------------- #

if st.session_state.started:

    st.subheader(
        f"Question {st.session_state.question_no} / {total_questions}"
    )

    st.info(st.session_state.current_question)

    answer = st.text_area(
        "💬 Your Answer",
        height=200,
        key=f"answer_{st.session_state.question_no}"
    )

    # -------- Evaluate -------- #

    if st.button("Evaluate Answer"):

        if answer.strip() == "":

            st.warning("Please enter your answer.")

        else:

            with st.spinner("Evaluating..."):

                feedback = evaluate_answer(
                    st.session_state.current_question,
                    answer
                )

            st.subheader("📊 AI Feedback")

            st.write(feedback)

    # -------- Next Question -------- #

    if st.session_state.question_no < total_questions:

        if st.button("➡️ Next Question"):

            st.session_state.question_no += 1

            with st.spinner("Generating Next Question..."):

                st.session_state.current_question = generate_question()

            st.rerun()

    else:

        st.success("🎉 Interview Completed!")

        if st.button("Start New Interview"):

            st.session_state.started = False
            st.session_state.question_no = 1
            st.session_state.current_question = ""

            st.rerun()