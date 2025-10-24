# MCP LangChain (separate frontend + backend)

Structure:
- backend/: Flask API that stores messages and calls LangChain chains
- frontend/: Vite + React frontend consuming the API

Run backend:
- cd backend
- python -m venv .venv
- source .venv/bin/activate
- pip install -r requirements.txt
- copy .env.example to .env and set OPENAI_API_KEY
- python app.py

Run frontend:
- cd frontend
- npm install
- npm run dev

Note: For production, add authentication and move LLM calls to background workers.
