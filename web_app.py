import os
import sqlite3
import threading
from flask import Flask, render_template, request, jsonify, redirect, url_for
from system.orchestrator import Orchestrator
from system.playbook_builder import PlaybookBuilder

app = Flask(__name__, template_folder="templates", static_folder="static")

WORKSPACE_ROOT = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(WORKSPACE_ROOT, "data", "mie_vault.db")
PROJECTS_DIR = os.path.join(WORKSPACE_ROOT, "projects")

running_workflows = {}


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_available_workflows():
    workflows = []
    if os.path.exists(PROJECTS_DIR):
        for f in os.listdir(PROJECTS_DIR):
            if f.endswith(".md"):
                workflows.append(f.replace(".md", ""))
    return workflows


@app.route("/")
def index():
    workflows = get_available_workflows()
    return render_template("index.html", workflows=workflows)


@app.route("/api/run", methods=["POST"])
def run_workflow():
    data = request.get_json()
    workflow_name = data.get("workflow", "").strip()
    if not workflow_name:
        return jsonify({"error": "No workflow specified"}), 400

    workflow_file = os.path.join(PROJECTS_DIR, f"{workflow_name}.md")
    if not os.path.exists(workflow_file):
        return jsonify({"error": f"Workflow '{workflow_name}' not found"}), 404

    if workflow_name in running_workflows and running_workflows[workflow_name] == "running":
        return jsonify({"error": "Workflow already running"}), 409

    def execute(name):
        running_workflows[name] = "running"
        try:
            orchestrator = Orchestrator(WORKSPACE_ROOT)
            run_path, timestamp = orchestrator.initialize_run(name)
            exit_code = orchestrator.run_docker_container(run_path, name)
            orchestrator.sync_back(run_path)
            builder = PlaybookBuilder(WORKSPACE_ROOT)
            builder.generate_playbook(name)
            running_workflows[name] = "done"
        except Exception as e:
            running_workflows[name] = f"error: {e}"

    thread = threading.Thread(target=execute, args=(workflow_name,))
    thread.start()
    return jsonify({"status": "started", "workflow": workflow_name})


@app.route("/api/status/<workflow_name>")
def workflow_status(workflow_name):
    status = running_workflows.get(workflow_name, "idle")
    return jsonify({"workflow": workflow_name, "status": status})


@app.route("/api/history")
def history():
    conn = get_db()
    rows = conn.execute("""
        SELECT c.id, c.name, c.origin_country, c.description, c.growth_signal, c.timestamp,
               mg.viability_score
        FROM companies c
        LEFT JOIN market_gaps mg ON c.id = mg.company_id
        ORDER BY c.timestamp DESC
    """).fetchall()
    conn.close()
    results = []
    for r in rows:
        results.append({
            "id": r["id"],
            "name": r["name"],
            "origin_country": r["origin_country"],
            "description": r["description"],
            "growth_signal": r["growth_signal"],
            "timestamp": r["timestamp"],
            "viability_score": r["viability_score"],
        })
    return jsonify(results)


@app.route("/api/research/<int:company_id>")
def research_detail(company_id):
    conn = get_db()
    row = conn.execute("""
        SELECT c.name, c.origin_country, c.description, c.growth_signal, c.timestamp,
               mg.viability_score, mg.adaptation_strategy, mg.execution_plan,
               mg.risks, mg.final_verdict, mg.full_report, mg.target_market
        FROM companies c
        LEFT JOIN market_gaps mg ON c.id = mg.company_id
        WHERE c.id = ?
        ORDER BY mg.id DESC LIMIT 1
    """, (company_id,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Not found"}), 404
    return jsonify({
        "name": row["name"],
        "origin_country": row["origin_country"],
        "description": row["description"],
        "growth_signal": row["growth_signal"],
        "timestamp": row["timestamp"],
        "viability_score": row["viability_score"],
        "adaptation_strategy": row["adaptation_strategy"],
        "execution_plan": row["execution_plan"],
        "risks": row["risks"],
        "final_verdict": row["final_verdict"],
        "full_report": row["full_report"],
        "target_market": row["target_market"],
    })


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    app.run(debug=True, port=5000)
