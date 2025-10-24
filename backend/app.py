from flask import Flask, request, jsonify
from flask_cors import CORS
from db import SessionLocal, init_db
from models import Message, AnalysisResult
from prompts import summary_chain, sentiment_chain, keywords_chain
import json

app = Flask(__name__)
CORS(app)
init_db()

def run_chain(chain, text):
    return chain.run({"text": text})

@app.route("/api/messages", methods=["POST"])
def create_message():
    payload = request.get_json()
    text = payload.get("text", "").strip()
    if not text:
        return jsonify({"error": "text is required"}), 400

    db = SessionLocal()
    try:
        msg = Message(user_text=text)
        db.add(msg)
        db.commit()
        db.refresh(msg)
        return jsonify({"id": msg.id, "text": msg.user_text, "created_at": msg.created_at.isoformat()})
    finally:
        db.close()

@app.route("/api/messages/<int:msg_id>/analyze", methods=["POST"])
def analyze_message(msg_id):
    payload = request.get_json() or {}
    tasks = payload.get("tasks", ["summarization", "sentiment", "keywords"])
    db = SessionLocal()
    try:
        msg = db.query(Message).filter(Message.id == msg_id).first()
        if not msg:
            return jsonify({"error": "message not found"}), 404

        results = []
        text = msg.user_text

        if "summarization" in tasks:
            out = run_chain(summary_chain, text)
            res = AnalysisResult(message_id=msg.id, kind="summarization", result_text=out)
            db.add(res); db.commit(); db.refresh(res)
            results.append({"kind":"summarization","result": out})

        if "sentiment" in tasks:
            out = run_chain(sentiment_chain, text)
            try:
                parsed = json.loads(out)
            except Exception:
                parsed = {"raw": out}
            res = AnalysisResult(message_id=msg.id, kind="sentiment", result_text=json.dumps(parsed))
            db.add(res); db.commit(); db.refresh(res)
            results.append({"kind":"sentiment","result": parsed})

        if "keywords" in tasks:
            out = run_chain(keywords_chain, text)
            try:
                parsed = json.loads(out)
            except Exception:
                parsed = [k.strip() for k in out.split(",") if k.strip()]
            res = AnalysisResult(message_id=msg.id, kind="keywords", result_text=json.dumps(parsed))
            db.add(res); db.commit(); db.refresh(res)
            results.append({"kind":"keywords","result": parsed})

        return jsonify({"message_id": msg.id, "analyses": results})
    finally:
        db.close()

@app.route("/api/messages/<int:msg_id>", methods=["GET"])
def get_message(msg_id):
    db = SessionLocal()
    try:
        msg = db.query(Message).filter(Message.id == msg_id).first()
        if not msg:
            return jsonify({"error":"not found"}), 404
        analyses = []
        for a in msg.analyses:
            try:
                parsed = json.loads(a.result_text)
            except Exception:
                parsed = a.result_text
            analyses.append({"id": a.id, "kind": a.kind, "result": parsed, "created_at": a.created_at.isoformat()})
        return jsonify({"id": msg.id, "text": msg.user_text, "created_at": msg.created_at.isoformat(), "analyses": analyses})
    finally:
        db.close()

@app.route("/api/messages", methods=["GET"])
def list_messages():
    db = SessionLocal()
    try:
        msgs = db.query(Message).order_by(Message.created_at.desc()).limit(50).all()
        out = []
        for m in msgs:
            out.append({"id": m.id, "text": m.user_text, "created_at": m.created_at.isoformat()})
        return jsonify(out)
    finally:
        db.close()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
