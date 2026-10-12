from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.ingestion_service import ingest_transcripts

router = APIRouter(prefix="/ingestion", tags=["ingestion"])


class IngestionRequest(BaseModel):
    source: str = "fixtures"


@router.post("/jobs")
async def create_ingestion_job(payload: IngestionRequest) -> dict:
    result = ingest_transcripts()
    return {"job_id": "job-ingest-1", "status": result["status"], "details": result}


@router.get("/jobs/{job_id}")
async def get_ingestion_job(job_id: str) -> dict:
    if job_id != "job-ingest-1":
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, "status": "completed", "details": {"status": "ok"}}
