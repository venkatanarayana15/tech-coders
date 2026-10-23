from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Column
from sqlalchemy.types import JSON
from sqlmodel import Field, SQLModel


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    role: str  # creator | reviewer | admin
    email: str
    initials: str


class Kit(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    client: str
    data: dict = Field(default_factory=dict, sa_column=Column(JSON))


class Draft(SQLModel, table=True):
    id: str = Field(primary_key=True)
    kit_id: str = Field(index=True)
    creator_id: str = Field(index=True)
    title: str
    caption: str
    alt_text: str = ""
    image_file: str | None = None
    doc_name: str | None = None
    doc_text: str | None = None
    status: str = "draft"  # draft | in_review | changes_requested | approved
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
    approved_by: str | None = None
    approved_at: datetime | None = None
    review_meta: dict = Field(default_factory=dict, sa_column=Column(JSON))


class Finding(SQLModel, table=True):
    id: str = Field(primary_key=True)
    draft_id: str = Field(index=True)
    check: str  # claims | tone | visual | accessibility
    rule_id: str = Field(index=True)
    severity: str = "soft"  # hard | soft
    title: str
    detail: str
    quote: str
    field: str = "caption"  # caption | alt_text | image
    source: dict = Field(default_factory=dict, sa_column=Column(JSON))
    fixes: list = Field(default_factory=list, sa_column=Column(JSON))
    measured: dict | None = Field(default=None, sa_column=Column(JSON))
    decision: str | None = None  # accepted | kept
    note: str | None = None
    decided_by: str | None = None
    decided_at: datetime | None = None
    created_at: datetime = Field(default_factory=utcnow)


class Revision(SQLModel, table=True):
    id: str = Field(primary_key=True)
    draft_id: str = Field(index=True)
    actor_id: str
    action: str
    summary: str
    created_at: datetime = Field(default_factory=utcnow)
