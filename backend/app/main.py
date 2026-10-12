from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import health as health_routes
from app.api.routes import sessions as sessions_routes
from app.api.routes import models as models_routes
from app.api.routes import ingestion as ingestion_routes
from app.api.routes import chat as chat_routes
from app.api.routes import artifacts as artifacts_routes
from app.core.config import get_settings
from app.db.session import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("x-request-id", f"req-{int(datetime.now(timezone.utc).timestamp() * 1000)}")
    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    return response


@app.get("/api/v1/health")
async def health_route() -> dict:
    return await health_routes.health()


@app.get("/api/v1/health/ready")
async def ready_route() -> dict:
    return await health_routes.ready()


@app.get("/api/v1/config/public")
async def public_config() -> dict:
    return {
        "app_name": settings.app_name,
        "provider": settings.selected_provider,
        "model": settings.selected_model,
        "availability": {"ollama": True, "openai": bool(settings.openai_api_key), "anthropic": bool(settings.anthropic_api_key)},
    }


app.include_router(health_routes.router, prefix="/api/v1")
app.include_router(sessions_routes.router, prefix="/api/v1")
app.include_router(models_routes.router, prefix="/api/v1")
app.include_router(ingestion_routes.router, prefix="/api/v1")
app.include_router(chat_routes.router, prefix="/api/v1")
app.include_router(artifacts_routes.router, prefix="/api/v1")


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail, "status": "error"})


@app.get("/")
async def root() -> dict:
    return {"message": "Lenny Growth Assistant API"}
