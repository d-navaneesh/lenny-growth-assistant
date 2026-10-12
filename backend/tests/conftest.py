from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings
from app.db.base import Base
from app.db.models import *  # noqa: F401,F403
from app.main import app

os.environ["DATABASE_URL"] = "sqlite+pysqlite:///./test.db"
settings = get_settings()

engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
