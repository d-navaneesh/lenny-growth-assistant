# Lenny Growth Assistant

A local-first AI product research assistant that turns transcript evidence into grounded answers and reusable artifacts for product and growth work.

## What it does
- Chat with transcript-backed context from demo sources.
- Show evidence snippets for every answer.
- Persist conversations and messages locally.
- Generate a structured artifact for follow-up work.
- Support local Ollama usage and optional cloud provider adapters.

## Stack
- Backend: FastAPI, SQLAlchemy, Pydantic, Uvicorn
- Frontend: Vite, React, TypeScript
- Local model path: Ollama
- Database: SQLite by default, PostgreSQL supported via config and Docker Compose

## Quick start

### 1) Install Python dependencies

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

If a requirements file is not present in the environment, use the project metadata in `backend/pyproject.toml` and install with:

```bash
pip install -e .
```

### 2) Run backend

```bash
cd backend
.venv\Scripts\activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3) Run frontend

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

### 4) Optional Docker local stack

```bash
docker compose up -d postgres ollama
```

## Environment variables
Copy `.env.example` to `.env` and adjust values. The repo is intentionally configured to avoid storing credentials in version control.

## Verification
This workspace has been validated with:

```bash
cd backend
.venv\Scripts\python.exe -m pytest -q
```

and

```bash
cd frontend
npm run build
```

## Project structure
- `backend/app` — API, models, provider config, retrieval, and skills
- `frontend/src` — UI shell and interaction logic
- `data/transcripts` — transcript corpus used by the demo
- `docs` — product, design, architecture, and demo materials

## Notes
- The default local configuration uses SQLite for a frictionless demo.
- PostgreSQL is included as a production-oriented option but not required for the current local validation path.
- The transcript corpus is synthetic demo content rather than licensed production media.
