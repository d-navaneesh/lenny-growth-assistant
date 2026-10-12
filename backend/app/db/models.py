from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import relationship, mapped_column

from app.db.base import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = mapped_column(Integer, primary_key=True, index=True)
    title = mapped_column(String(255), nullable=False)
    owner = mapped_column(String(255), nullable=True)
    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    artifacts = relationship("Artifact", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"

    id = mapped_column(Integer, primary_key=True, index=True)
    conversation_id = mapped_column(ForeignKey("conversations.id", ondelete="CASCADE"), index=True)
    role = mapped_column(String(32), nullable=False)
    content = mapped_column(Text, nullable=False)
    timestamp = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    message_metadata = mapped_column(JSON, nullable=True)
    provider = mapped_column(String(64), nullable=True)
    model = mapped_column(String(128), nullable=True)

    conversation = relationship("Conversation", back_populates="messages")


class TranscriptSource(Base):
    __tablename__ = "transcript_sources"

    id = mapped_column(Integer, primary_key=True, index=True)
    title = mapped_column(String(255), nullable=False)
    source_url = mapped_column(String(500), nullable=True)
    author = mapped_column(String(255), nullable=True)
    episode = mapped_column(String(255), nullable=True)
    ingested_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    content_hash = mapped_column(String(128), nullable=False, index=True)
    status = mapped_column(String(32), default="indexed")
    source_metadata = mapped_column(JSON, nullable=True)

    chunks = relationship("TranscriptChunk", back_populates="source", cascade="all, delete-orphan")


class TranscriptChunk(Base):
    __tablename__ = "transcript_chunks"

    id = mapped_column(Integer, primary_key=True, index=True)
    source_id = mapped_column(ForeignKey("transcript_sources.id", ondelete="CASCADE"), index=True)
    chunk_index = mapped_column(Integer, nullable=False)
    chunk_text = mapped_column(Text, nullable=False)
    char_count = mapped_column(Integer, nullable=False)
    token_count = mapped_column(Integer, nullable=True)
    embedding = mapped_column(JSON, nullable=True)
    chunk_metadata = mapped_column(JSON, nullable=True)

    source = relationship("TranscriptSource", back_populates="chunks")


class Artifact(Base):
    __tablename__ = "artifacts"

    id = mapped_column(Integer, primary_key=True, index=True)
    conversation_id = mapped_column(ForeignKey("conversations.id", ondelete="SET NULL"), index=True, nullable=True)
    title = mapped_column(String(255), nullable=False)
    artifact_type = mapped_column(String(32), nullable=False)
    content = mapped_column(Text, nullable=False)
    created_at = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    validation_status = mapped_column(String(32), default="pending")
    rendering_metadata = mapped_column(JSON, nullable=True)

    conversation = relationship("Conversation", back_populates="artifacts")
