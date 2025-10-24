# Backend (Flask) - MCP LangChain

Steps:
1. Create a python venv and activate it.
   python -m venv .venv
   source .venv/bin/activate

2. Install dependencies:
   pip install -r requirements.txt

3. Copy .env.example to .env and set OPENAI_API_KEY

4. Run:
   python app.py

API endpoints:
- POST /api/messages { text }
- POST /api/messages/<id>/analyze { tasks?: [summarization,sentiment,keywords] }
- GET /api/messages
- GET /api/messages/<id>
