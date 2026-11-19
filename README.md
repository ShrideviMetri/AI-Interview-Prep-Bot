# 🤖 AI Interview Prep Bot

An AI-powered interview preparation application that helps candidates practice technical interviews, receive feedback on their answers, and prepare using their own resumes.

## ✨ Features

- **AI Interview Questions:** Generates interview questions based on the selected job role and difficulty.
- **Resume-Based Interviews:** Upload your resume in PDF format to generate questions based on your skills, projects, technologies, and experience.
- **Answer Evaluation:** Evaluates your answers and provides scores, strengths, weaknesses, ideal answers, and improvement tips.
- **Multiple Difficulty Levels:** Practice Easy, Medium, and Hard questions.
- **Customizable Interviews:** Choose the number of interview questions.
- **Duplicate Question Prevention:** Tracks previously asked questions to reduce repetition.
- **AI Provider Fallback:** Uses Google Gemini as the primary AI provider and automatically switches to local Ollama when Gemini reaches its rate limit or encounters temporary server/network errors.
- **Local AI Support:** Uses the Llama 3.2 model through Ollama.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Streamlit | User interface |
| Google Gemini API | Primary AI model |
| Ollama (Llama 3.2) | Local AI fallback |
| PyMuPDF | PDF text extraction |
| Requests | HTTP communication |
| Python-dotenv | Environment variable management |

## 📁 Project Structure

```text
AI-Interview-Prep-Bot/
│
├── modules/
│   ├── __init__.py
│   ├── ai_interviewer.py
│   └── pdf_reader.py
│
├── uploads/
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI-Interview-Prep-Bot
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=llama3.2:latest
```

Replace the Gemini API key placeholder with your own key.

### 6. Set up Ollama

- Install Ollama from https://ollama.com/
- Pull the Llama 3.2 model:

```bash
ollama pull llama3.2:latest
```

- Make sure Ollama is running locally.

### 7. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🔄 AI Fallback Mechanism

The application follows a primary and fallback AI architecture:

1. Sends the request to Google Gemini.
2. Retries once for temporary server or network errors.
3. If Gemini reaches its rate limit or encounters supported temporary errors, the application switches to Ollama.
4. Ollama generates the response locally.

**Note:** Ollama must be installed and running on the same machine as the application for local fallback to work.

## 🔐 Security

- Store API keys in the `.env` file.
- Never upload `.env` to GitHub.
- Add `.env` and `venv/` to `.gitignore`.

## 🚀 Future Enhancements

- Interview performance tracking.
- Interview history and progress dashboard.
- More AI model integrations.
- Additional interview categories.

## 👩‍💻 Author

**Shridevi Metri**

- GitHub: https://github.com/ShrideviMetri
- LinkedIn: https://www.linkedin.com/in/shridevi-metri-922a46334
