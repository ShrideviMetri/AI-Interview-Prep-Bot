# 🤖 AI Interview Prep Bot

An AI-powered Interview Preparation Bot built using **Python**, **Streamlit**, and the **Google Gemini API**. The application generates role-specific interview questions, evaluates user answers with detailed AI feedback, and creates personalized interview questions based on an uploaded resume.

---

## 🚀 Features

- 🤖 AI-generated interview questions
- 📄 Resume upload (PDF)
- 🧠 AI-powered resume analysis
- 🎯 Resume-based interview questions
- 💼 Multiple job roles
- 📊 Difficulty selection (Easy, Medium, Hard)
- 🔢 Configurable number of interview questions
- ✅ AI-powered answer evaluation
- 💡 Detailed feedback with strengths, weaknesses, ideal answers, and improvement tips
- 🌐 Interactive Streamlit web interface

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Google Gemini API
- Google GenAI SDK
- PyMuPDF
- Gemini 3.6 Flash

---

## 📂 Project Structure

```text
INTERVIEW_PREP_BOT/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── modules/
│   ├── ai_interviewer.py
│   └── pdf_reader.py
└── assets/
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/ShrideviMetri/AI-Interview-Prep-Bot.git
cd AI-Interview-Prep-Bot
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment (Windows)

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create a `.env` file

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### Get a Gemini API Key

Generate a free API key from Google AI Studio:

https://aistudio.google.com/apikey

### Run the application

```bash
streamlit run app.py
```

---

## 🤖 AI Model

- **Provider:** Google Gemini API
- **Model:** Gemini 3.5 Flash-lite

---

## 🌐 Live Demo

Add your deployed Streamlit application URL here.

---

## 📸 Screenshots

_Add screenshots of the application here._

---

## 📌 Future Improvements

- 📈 Overall Interview Performance Report
- 🎙️ Voice-based Interview
- 📄 Download Interview Report as PDF
- 📚 Interview History
- 📊 Performance Dashboard
- 🔐 User Authentication & Profiles

---

## 👩‍💻 Author

**Shridevi Metri**