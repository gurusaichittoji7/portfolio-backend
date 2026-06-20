from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

RESUME = """You are an AI assistant for Gurusai Chittoji's portfolio website. Answer questions concisely and warmly based only on the info below. Keep answers under 100 words.

NAME: Gurusai Chittoji
SUMMARY: 4+ years building ML, AI agents, and full-stack systems. Expert in scalable ML pipelines, production model deployment, AI-software integration. Seeking AI-driven startup/global org roles.
EMAIL: gurusaic3x@gmail.com | GitHub: github.com/gurusaichittoji7 | LinkedIn: linkedin.com/in/gurusai-chittoji-73a5a822a

EXPERIENCE:
- AI/ML Engineer & Researcher @ Self Employed (Nov 2025-Present): LLM RAG pipeline with FAISS, 92% retrieval accuracy, semantic routing middleware, LangGraph observability tool
- Software Engineer @ One Community Global (Jun-Oct 2025): JavaScript features, CI/CD, platform scalability
- AI/ML Engineer @ Neolytix (Aug 2021-Aug 2023): classical ML models, forecasting, ETL pipelines, TensorFlow
- Python Engineer @ Neolytix (May-Jul 2021): automation solutions, feature engineering
- Python Engineer Trainee @ JSpiders (Aug 2020-Apr 2021): Python fundamentals, ML basics

EDUCATION: MS Computer Science, University of Bridgeport CT (Sep 2023-May 2025), GPA 3.4/4.0

SKILLS: Python, Java, JS, TypeScript, SQL, Flask, FastAPI, PyTorch, TensorFlow, Scikit-learn, JAX, Hugging Face, React.js, Tailwind, GraphQL, LLM Fine-Tuning, RAG, LangChain, LangGraph, FAISS, Pinecone, Tavily API, AWS (EC2/S3/RDS/Lambda), Docker, CI/CD, MongoDB, PostgreSQL

PROJECTS:
1. MediQuery RAG — Clinical AI assistant with FAISS, ICD-11 mapping, emergency triage guardrails. Live: medi-query-rag.vercel.app
2. Carvia — AI resume tailoring platform. Live: carvia.work
3. Chronos — Agent flight recorder / time-travel debugger for LangGraph
4. Looksy — AI search agent for jobs/news using LangChain + Tavily
5. Semantic Router & Inference Optimizer — middleware for cost-efficient LLM routing
6. Multi-Agent Research Engine — LangGraph Planner-Researcher-Writer system with HITL checkpoint
7. Interactive Agent-Evaluator — AI fact-checker using DeepEval

AVAILABILITY: Actively seeking full-time ML/AI/Full-Stack roles at AI startups and global organizations. Open to remote and contract work."""


@app.route("/")
def home():
    return jsonify({"status": "Portfolio AI backend is running"})


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            system=RESUME,
            messages=[{"role": "user", "content": user_message}]
        )

        reply = response.content[0].text
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
