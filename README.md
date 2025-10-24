# MCP LangChain (separate frontend + backend)

(Windows)

Project Layout:
mcp-langchain/
├─ backend/
│  ├─ app.py                 # Flask app + endpoints
│  ├─ models.py              # SQLAlchemy models
│  ├─ db.py                  # DB init helper
│  ├─ requirements.txt
│  └─ prompts.py             # Prompt templates & LangChain chains
├─ frontend/
│  ├─ package.json
│  ├─ src/
│  │  ├─ App.jsx
│  │  ├─ components/
│  │  │  ├─ ChatBox.jsx
│  │  │  └─ ResultsList.jsx
│  │  └─ api.js
│  └─ tailwind.config.js (optional)
└─ README.md


Structure:
- backend/: Flask API that stores messages and calls LangChain chains
- frontend/: Vite + React frontend consuming the API

Run backend:
- cd backend
- python -m venv .venv
- .venv\Scripts\activate.ps1
- pip install -r requirements.txt
- copy .env.example to .env and set OPENAI_API_KEY
- python app.py

Run frontend:
- cd frontend
- npm install
- npm run dev

Note: For production, add authentication and move LLM calls to background workers.

Prompts tips:
1. Summarization: ask for word or sentence limits; instruct style (bullet points vs one paragraph).
2. Sentiment: prefer JSON outputs or fixed enumerations (positive/neutral/negative) to ease parsing.
3. Keywords: ask for exactly N keywords, or key phrases; if you want multi-word phrases, instruct the model: “prefer 1–3 word phrases”.
4. Temperature: use low temperature (0 — 0.3) for deterministic outputs.
5. Token limits: for very long texts, chunk before summarizing or use a chain-of-thought summarization pattern (chunk → intermediate summaries → final summary).