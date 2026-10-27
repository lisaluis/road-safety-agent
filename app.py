"""Road Safety policy agent: web page + API.
Run:  pip install -r requirements.txt
      PowerShell: $env:GROQ_API_KEY="your_key"      Mac/Linux: export GROQ_API_KEY=your_key
      python app.py      ->  http://localhost:5000
Routes: /  (page)   POST /api/policies {"question": "..."}   GET /api/facts   GET /api/health
"""
import os
from flask import Flask, jsonify, request, send_from_directory
import agent as policy_agent          # agent.py sits next to this file

BASE = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=None)   # no static route: source files are never served

@app.get("/")
def page():
    return send_from_directory(BASE, "agent.html")

@app.get("/api/health")
def health():
    return jsonify(status="ok", model=policy_agent.MODEL, key_set=bool(os.environ.get("GROQ_API_KEY")))

@app.get("/api/facts")
def facts():
    return jsonify(policy_agent.load_facts())

@app.post("/api/policies")
def policies():
    question = (request.get_json(silent=True) or {}).get("question", "").strip()
    if not question:
        return jsonify(error="Please type a question."), 400
    if len(question) > 500:
        return jsonify(error="Question too long (max 500 characters)."), 400
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        return jsonify(error="Server has no GROQ_API_KEY set. Set it and restart."), 500
    try:
        from groq import Groq
        return jsonify(policy_agent.run(question, Groq(api_key=key)))
    except Exception as e:
        return jsonify(error=f"Agent failed: {type(e).__name__}: {e}"), 502

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)), debug=False)
