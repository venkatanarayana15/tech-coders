from __future__ import annotations

import re
import uuid
from datetime import datetime
from typing import Any

from sqlmodel import Session

from .models import Draft, Finding, Revision, User, utcnow

STATUS_LABELS = {
    "draft": "Draft",
    "in_review": "In review",
    "changes_requested": "Changes requested",
    "approved": "Approved",
}


def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:10]}"


def iso(value: datetime | None) -> str | None:
    return value.isoformat() if value else None


def add_revision(
    session: Session, draft: Draft, actor: User, action: str, summary: str
) -> Revision:
    revision = Revision(
        id=new_id("rev"),
        draft_id=draft.id,
        actor_id=actor.id,
        action=action,
        summary=summary,
    )
    session.add(revision)
    draft.updated_at = utcnow()
    return revision


def apply_decision(
    session: Session,
    draft: Draft,
    finding: Finding,
    action: str,
    note: str,
    actor: User,
    fix_index: int = 0,
) -> None:
    if finding.decision is not None:
        raise ValueError("This finding has already been decided.")
    if draft.approved_at is not None:
        raise ValueError("Approved drafts are locked.")
    if action not in {"accept", "keep"}:
        raise ValueError("Decision must be 'accept' or 'keep'.")
    if action == "keep" and not note.strip():
        raise ValueError("Add a short note when you keep your own wording.")

    if action == "accept":
        if finding.fixes:
            index = fix_index if 0 <= fix_index < len(finding.fixes) else 0
            fix = finding.fixes[index]
            text = fix.get("text", "")
            if finding.field == "caption" and text is not None and finding.quote:
                pattern = re.compile(re.escape(finding.quote), re.IGNORECASE)
                if pattern.search(draft.caption):
                    def replace(match: re.Match) -> str:
                        replacement = text
                        if match.group(0)[:1].isupper() and replacement:
                            replacement = replacement[:1].upper() + replacement[1:]
                        return replacement

                    updated = pattern.sub(replace, draft.caption, count=1)
                    updated = re.sub(r"([.!?])\1+", r"\1", updated)
                    updated = re.sub(r"\s+([,.;:])", r"\1", updated)
                    draft.caption = re.sub(r"\s{2,}", " ", updated).strip()
            elif finding.field == "alt_text" and text:
                draft.alt_text = text
        finding.decision = "accepted"
        summary = f"Accepted a fix for {finding.rule_id}: {finding.title}"
    else:
        finding.decision = "kept"
        summary = f"Kept their wording on {finding.rule_id}: {finding.title}"

    finding.note = note.strip() or None
    finding.decided_by = actor.id
    finding.decided_at = utcnow()
    draft.updated_at = utcnow()
    session.add(finding)
    session.add(draft)
    add_revision(session, draft, actor, f"finding.{action}", summary)


def finding_payload(finding: Finding) -> dict[str, Any]:
    return {
        "id": finding.id,
        "check": finding.check,
        "rule_id": finding.rule_id,
        "severity": finding.severity,
        "title": finding.title,
        "detail": finding.detail,
        "quote": finding.quote,
        "field": finding.field,
        "source": finding.source,
        "fixes": finding.fixes,
        "measured": finding.measured,
        "decision": finding.decision,
        "note": finding.note,
        "decided_by": finding.decided_by,
        "decided_at": iso(finding.decided_at),
        "created_at": iso(finding.created_at),
    }


def draft_payload(
    draft: Draft,
    creator: User | None = None,
    findings: list[Finding] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "id": draft.id,
        "kit_id": draft.kit_id,
        "creator_id": draft.creator_id,
        "creator": creator.name if creator else draft.creator_id,
        "creator_initials": creator.initials if creator else "?",
        "title": draft.title,
        "caption": draft.caption,
        "alt_text": draft.alt_text,
        "image_url": f"/api/files/{draft.image_file}" if draft.image_file else None,
        "doc_name": draft.doc_name,
        "doc_text": draft.doc_text,
        "status": draft.status,
        "status_label": STATUS_LABELS.get(draft.status, draft.status),
        "created_at": iso(draft.created_at),
        "updated_at": iso(draft.updated_at),
        "approved_by": draft.approved_by,
        "approved_at": iso(draft.approved_at),
        "review_meta": draft.review_meta,
    }
    if findings is not None:
        open_count = sum(1 for finding in findings if finding.decision is None)
        payload["finding_count"] = len(findings)
        payload["open_count"] = open_count
        payload["hard_count"] = sum(1 for finding in findings if finding.severity == "hard")
        payload["checks"] = sorted({finding.check for finding in findings}) or ["claims", "tone"]
    return payload


def revision_payload(revision: Revision, actor: User | None = None) -> dict[str, Any]:
    return {
        "id": revision.id,
        "actor_id": revision.actor_id,
        "actor": actor.name if actor else revision.actor_id,
        "action": revision.action,
        "summary": revision.summary,
        "created_at": iso(revision.created_at),
    }
