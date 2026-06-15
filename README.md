![Market Trends Finder](https://placehold.co/1200x300/064e3b/d1fae5?text=Market+Trends+Finder)

# 🧠 Market Trends Finder

> 📈 **Playbook-driven market intelligence & trend discovery engine** — discovers high-performing startups, products, and trends, analyzes *why* they work, and auto-generates **playbooks** to replicate their success in other markets/regions (e.g., US → India). It learns from every run and improves over time.

---

## ✨ Features

- 🔍 **Trend Discovery** — finds trending startups, products, and market movements (TikTok skincare trends, finance news, startup discovery, etc.)
- 🧩 **Root-Cause Analysis** — analyzes *why* a trend/product is succeeding
- 📋 **Auto-Generated Playbooks** — actionable, step-by-step replication guides
- 🔁 **Continuous Learning** — stores skills/memory from past runs to improve future workflows
- 🏗️ **Sandboxed Execution** — each workflow run executes in an isolated Docker container
- 🌍 **Market Replication** — adapt a winning strategy from one market/region to another

---

## 🏗️ Architecture

### 🧭 System Philosophy

- Everything is a **workflow** (defined as Markdown playbooks)
- Intelligence is stored as **reusable skills**
- Learning is stored in **memory**
- Execution happens in **isolated Docker sandboxes**
- Improvement is automatic via a feedback loop

### 🔁 System Loop

1. 📥 Receive task / workflow
2. 🗺️ Plan execution
3. ♻️ Reuse or generate code
4. 🐳 Execute in a Docker sandbox
5. 💾 Store outputs + logs (`runs/`)
6. 🎓 Learn from results
7. 🧰 Convert useful code into reusable skills

### 🛠️ Tech Stack

- **Python 3.10**
- **Docker** (sandboxed agent execution — `system/agent_cli.py` is the container entrypoint)
- **Custom orchestration framework** — `system/orchestrator.py` (run lifecycle, Docker container management, sync-back) + `system/playbook_builder.py` (auto-generates replication playbooks)
- **OpenAI API** — powers the autonomous agent / code generation
- Libraries: `requests`, `beautifulsoup4`, `selenium`, `pandas`, `python-dotenv`, `docker`

### 📂 Project Structure

```
market_trends_finder/
├── run_workflow.py        # Main entrypoint - runs a workflow end-to-end
├── system/
│   ├── orchestrator.py    # Manages run lifecycle & Docker execution
│   ├── playbook_builder.py# Auto-generates replication playbooks
│   ├── agent_cli.py        # Docker container entrypoint (agent logic)
│   ├── db_manager.py       # Persistence layer
│   └── base_scraper.py
├── utils/                  # Scraping & analysis helpers (news, social, browser, competitors)
├── playbooks/              # Workflow definitions (Markdown playbooks)
├── projects/               # Defined workflow/project specs (e.g. tiktok_skincare_us.md)
├── runs/                    # Output of each run (timestamped, gitignored)
├── docs/                    # Architecture & design docs
├── Dockerfile
└── requirements.txt
```

---

## 🖼️ Demo / Screenshots

> 📌 *Placeholder images below — replace with real screenshots from your runs.*

![Report Demo](https://placehold.co/800x400?text=Report+Demo)

![Playbook Output](https://placehold.co/800x400?text=Playbook+Output)

![Run Logs](https://placehold.co/800x400?text=Run+Logs)

---

## ▶️ How to Run a Workflow

Run a workflow by name (corresponds to a project/playbook definition, e.g. `projects/tiktok_skincare_us.md`):

```bash
python run_workflow.py <workflow_name>
```

Example:

```bash
python run_workflow.py tiktok_skincare_us
```

This will:
1. Create a timestamped run directory under `runs/`
2. Execute the workflow inside a Docker sandbox
3. Sync results back to the local `runs/` folder
4. Auto-generate a replication playbook for the run

---

## 📝 Notes

- `runs/` and `data/` contain generated outputs and are excluded from version control.
- Never commit your `.env` file — it contains your OpenAI API key.

---

## 🛠️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/IbrahimPopatiya/market_trends_finder.git
cd market_trends_finder
```

### 2. Create a virtual environment & install dependencies

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate    # macOS/Linux

pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Docker setup (used for sandboxed workflow execution)

```bash
docker build -t mie-agent:latest .
```

> The orchestrator will use this image to execute each workflow run inside an isolated container.

---

## 🚀 Run

```bash
python run_workflow.py <workflow_name>
```
