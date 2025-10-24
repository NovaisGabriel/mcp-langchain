from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from chains import run_chain

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app)

    @app.route("/api/analyze", methods=["POST"])
    def analyze():
        data = request.get_json()
        text = data.get("text", "")
        if not text:
            return jsonify({"error": "Missing text"}), 400

        try:
            result = run_chain(text)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
