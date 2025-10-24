# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()

app = Flask(__name__)
CORS(app)

# --- Database config ---
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///messages.db"
db = SQLAlchemy(app)

# --- Model ---
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    summarization = db.Column(db.Text)
    sentiment = db.Column(db.Text)
    keywords = db.Column(db.Text)

# --- Create tables safely ---
with app.app_context():
    db.create_all()

# --- LLM setup ---
llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))
parser = StrOutputParser()

summary_prompt = ChatPromptTemplate.from_template("Summarize this text:\n{text}")
sentiment_prompt = ChatPromptTemplate.from_template("Analyse the sentiment (Positive, Negative, or Neutral):\n{text}")
keywords_prompt = ChatPromptTemplate.from_template("Extract the main keywords from this text:\n{text}")

def run_chain(prompt, text):
    chain = prompt | llm | parser
    return chain.invoke({"text": text})

# --- Routes ---
@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    summary = run_chain(summary_prompt, text)
    sentiment = run_chain(sentiment_prompt, text)
    keywords = run_chain(keywords_prompt, text)

    message = Message(
        text=text,
        summarization=summary,
        sentiment=sentiment,
        keywords=keywords,
    )
    db.session.add(message)
    db.session.commit()

    return jsonify(
        {"summary": summary, "sentiment": sentiment, "keywords": keywords}
    )

if __name__ == "__main__":
    app.run(port=5000, debug=True)
