# Implementation plan

## Assignment requirement
Build a production-minded Lenny Growth Assistant with a FastAPI backend, PostgreSQL-backed persistence, a React + Vite frontend, an Ollama-local-first provider model, a cloud fallback, transcript ingestion and retrieval, a Ship 30 for 30 writing workflow, and artifact generation with a safe preview model. The project should be runnable locally, testable, and documented for demo and handoff.

## Planned implementation
- Create a lightweight monorepo structure with backend, frontend, docs, scripts, and data fixtures.
- Implement a FastAPI app with typed schemas, config, health endpoints, SQLAlchemy models, and session/message persistence.
- Add a provider abstraction for local Ollama and cloud OpenAI fallback with explicit provider selection and graceful errors.
- Add a simple transcript ingestion and retrieval pipeline using synthetic fixture data so the project works without networked copyrighted sources.
- Implement a grounded agent execution path with retrieval and a dedicated Ship 30 for 30 skill.
- Add artifact generation for Markdown and HTML/CSS under a sandboxed preview strategy.
- Create a Vite React + TypeScript frontend with a chat UI, sidebar, evidence explorer, model control center, and artifact viewer.
- Run backend and frontend tests, fix issues, and document blockers. 

## Relevant file paths
- backend/app/main.py
- backend/app/core/config.py
- backend/app/db/session.py
- backend/app/db/models.py
- backend/app/api/routes/*.py
- backend/app/providers/*.py
- backend/app/retrieval/*.py
- backend/app/skills/ship_30_for_30/*.py
- backend/tests/*.py
- frontend/src/*
- docs/*.md
- docker-compose.yml
- .env.example
- README.md

## Verification method
- Run backend pytest checks against API, persistence, rag, and model behavior.
- Run a frontend build and targeted UI tests.
- Start PostgreSQL via Docker Compose and verify database readiness.
- Exercise the local Ollama path when the model is available; otherwise document the blocked state and keep the app usable without it.

## Current status
- Workspace initialized with the repo skeleton.
- Environment audit is complete.
- The project is now being implemented in a working vertical slice: backend app, config, database model layer, retrieval, and frontend shell.
