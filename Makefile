PYTHON = backend/.venv/Scripts/python.exe
FRONTEND = frontend

.PHONY: backend frontend test docs

backend:
	cd backend && $(PYTHON) -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

frontend:
	cd frontend && npm run dev -- --host 0.0.0.0

test:
	cd backend && $(PYTHON) -m pytest -q

build-frontend:
	cd frontend && npm run build
