from __future__ import annotations

import html
import io
import re
import uuid
import zipfile
from collections import defaultdict
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, File, Form, HTTPException, Request, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image as PILImage
from pydantic import BaseModel
from pypdf import PdfReader
from sqlmodel import Session, select

from .auth import DEMO_PASSWORD, clear_session, current_user, session_user, set_session, verify_password
from .config import settings
from .db import engine, get_session, init_db
from .engine import mask_pii, run_review
from .kit_seed import KIT
from .llm import model_identity
from .models import Draft, Finding, Kit, Revision, User, utcnow
from .seed import seed_if_empty
from .services import (
    add_revision,
    apply_decision,
    draft_payload,
    finding_payload,
    new_id,
    revision_payload,
)

ALLOWED_IMAGES = {".png", ".jpg", ".jpeg", ".webp"}
ALLOWED_DOCS = {".pdf", ".docx"}


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    with Session(engine) as session:
        seed_if_empty(session)
    yield


app = FastAPI(title="PrismCheck AI", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SessionIn(BaseModel):
    user_id: str | None = None
    email: str | None = None
    password: str | None = None


class KitUpdateIn(BaseModel):
    audience: str | None = None
    tone: dict | None = None
    tolerance: dict | None = None
    palette: list | None = None
    rules: list | None = None
    facts: list | None = None
    banned: list | None = None
    preferred: list | None = None


class DecisionIn(BaseModel):
    finding_id: str
    action: str
    note: str = ""
    fix_index: int = 0


class NoteIn(BaseModel):
    note: str = ""


def _users(db: Session) -> dict[str, User]:
    return {user.id: user for user in db.exec(select(User)).all()}


def _get_kit_data(db: Session) -> dict[str, Any]:
    kit_row = db.get(Kit, KIT["id"])
    return kit_row.data if kit_row and kit_row.data else dict(KIT)


def _draft_or_404(db: Session, draft_id: str) -> Draft:
    draft = db.get(Draft, draft_id)
    if draft is None:
        raise HTTPException(status_code=404, detail="Draft not found.")
    return draft


def _can_view(draft: Draft, user: User) -> bool:
    return draft.creator_id == user.id or user.role in {"reviewer", "admin"}


def _detail(db: Session, draft: Draft, user: User) -> dict[str, Any]:
    findings = db.exec(
        select(Finding).where(Finding.draft_id == draft.id).order_by(Finding.created_at)
    ).all()
    revisions = db.exec(
        select(Revision).where(Revision.draft_id == draft.id).order_by(Revision.created_at)
    ).all()
    people = _users(db)
    is_owner = draft.creator_id == user.id
    can_edit = (is_owner or user.role == "admin") and draft.status != "approved"
    return {
        "draft": draft_payload(draft, people.get(draft.creator_id), list(findings)),
        "findings": [finding_payload(finding) for finding in findings],
        "revisions": [
            revision_payload(revision, people.get(revision.actor_id)) for revision in revisions
        ],
        "permissions": {
            "can_decide": can_edit,
            "can_submit": can_edit and draft.status in {"draft", "changes_requested"},
            "can_review": user.role in {"reviewer", "admin"} and draft.status == "in_review",
            "can_rerun": can_edit,
        },
    }


def _extract_docx(content: bytes) -> str:
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        xml = archive.read("word/document.xml").decode("utf-8", errors="ignore")
    xml = xml.replace("</w:p>", "\n")
    text = re.sub(r"<[^>]+>", " ", xml)
    return re.sub(r"\n{3,}", "\n\n", html.unescape(text)).strip()


def _extract_pdf(content: bytes) -> str:
    reader = PdfReader(io.BytesIO(content))
    return "\n\n".join((page.extract_text() or "") for page in reader.pages).strip()


async def _store_upload(upload: UploadFile) -> tuple[str, str] | None:
    if not upload or not upload.filename:
        return None
    suffix = Path(upload.filename).suffix.lower()
    content = await upload.read()
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail=f"Uploads are limited to {settings.max_upload_mb} MB.",
        )

    if suffix in ALLOWED_IMAGES:
        try:
            PILImage.open(io.BytesIO(content)).verify()
        except Exception as exc:  # noqa: BLE001
            raise HTTPException(status_code=400, detail="That image could not be read.") from exc
        name = f"{uuid.uuid4().hex}{suffix}"
        (settings.storage_dir / name).write_bytes(content)
        return ("image", name)

    if suffix in ALLOWED_DOCS:
        try:
            text = _extract_pdf(content) if suffix == ".pdf" else _extract_docx(content)
        except Exception as exc:  # noqa: BLE001
            raise HTTPException(status_code=400, detail="That document could not be read.") from exc
        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="No selectable text was found in that document.",
            )
        return ("document", text)

    raise HTTPException(
        status_code=400,
        detail="Upload a PNG, JPG, WEBP, PDF or DOCX file.",
    )


@app.get("/api/health")
def health() -> dict[str, Any]:
    identity = model_identity()
    return {
        "status": "ok",
        "product": "PrismCheck AI",
        "engine": identity,
        "demo_mode": settings.demo_mode,
    }


@app.get("/api/users")
def users(db: Session = Depends(get_session)) -> dict[str, Any]:
    people = db.exec(select(User)).all()
    return {
        "users": [
            {
                "id": u.id,
                "name": u.name,
                "role": u.role,
                "initials": u.initials,
                "email": u.email,
                "password": DEMO_PASSWORD if settings.demo_mode else None,
            }
            for u in people
        ]
    }


@app.get("/api/session")
def get_session_state(
    request: Request, db: Session = Depends(get_session)
) -> dict[str, Any]:
    user = session_user(request, db)
    return {
        "user": {"id": user.id, "name": user.name, "role": user.role, "initials": user.initials}
        if user
        else None
    }


@app.post("/api/session")
def sign_in(payload: SessionIn, response: Response, db: Session = Depends(get_session)) -> dict:
    if payload.user_id:
        user = db.get(User, payload.user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="That demo account does not exist.")
    elif payload.email:
        user = db.exec(select(User).where(User.email == payload.email.strip().lower())).first()
        if user is None or not verify_password(payload.password or "", user.password_hash):
            raise HTTPException(status_code=401, detail="Email or password is incorrect.")
    else:
        raise HTTPException(status_code=400, detail="Pick a demo account or enter credentials.")
    set_session(response, user.id)
    return {"user": {"id": user.id, "name": user.name, "role": user.role, "initials": user.initials}}


@app.delete("/api/session")
def sign_out(response: Response) -> dict:
    clear_session(response)
    return {"ok": True}


@app.get("/api/bootstrap")
def bootstrap(user: User = Depends(current_user), db: Session = Depends(get_session)) -> dict:
    drafts = db.exec(select(Draft)).all()
    findings = db.exec(select(Finding)).all()
    pending = sum(1 for draft in drafts if draft.status == "in_review")
    kit_data = _get_kit_data(db)
    return {
        "user": {"id": user.id, "name": user.name, "role": user.role, "initials": user.initials},
        "demo_users": [
            {"id": u.id, "name": u.name, "role": u.role, "initials": u.initials}
            for u in db.exec(select(User)).all()
        ],
        "stats": {
            "drafts": len(drafts),
            "pending_review": pending,
            "findings": len(findings),
            "open_findings": sum(1 for f in findings if f.decision is None),
        },
        "model": model_identity(),
        "kit": {
            "id": kit_data["id"],
            "name": kit_data["name"],
            "client": kit_data["client"],
            "version": kit_data.get("version", KIT["version"]),
        },
    }


@app.get("/api/kit")
def get_kit(
    user: User = Depends(current_user), db: Session = Depends(get_session)
) -> dict:
    return {"kit": _get_kit_data(db)}


@app.patch("/api/kit")
def update_kit(
    payload: KitUpdateIn,
    user: User = Depends(current_user),
    db: Session = Depends(get_session),
) -> dict:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Only an admin can edit the brand kit.")
    kit_row = db.get(Kit, KIT["id"])
    if kit_row is None:
        kit_row = Kit(
            id=KIT["id"],
            name=KIT["name"],
            client=KIT["client"],
            data=dict(KIT),
        )
    data = dict(kit_row.data or KIT)

    snapshot = {
        "version": data.get("version"),
        "updated": data.get("updated"),
        "owner": data.get("owner"),
        "audience": data.get("audience"),
        "tone": data.get("tone"),
        "tolerance": data.get("tolerance"),
        "palette": data.get("palette"),
        "rules": data.get("rules"),
        "facts": data.get("facts"),
        "banned": data.get("banned"),
        "preferred": data.get("preferred"),
    }
    history = list(data.get("history") or [])
    history.append(snapshot)
    data["history"] = history[-10:]

    fields = (
        ("audience", payload.audience),
        ("tone", payload.tone),
        ("tolerance", payload.tolerance),
        ("palette", payload.palette),
        ("rules", payload.rules),
        ("facts", payload.facts),
        ("banned", payload.banned),
        ("preferred", payload.preferred),
    )
    for key, value in fields:
        if value is not None:
            data[key] = value

    version = str(data.get("version") or KIT["version"])
    match = re.match(r"^(\d+)\.(\d+)$", version)
    data["version"] = f"{int(match.group(1))}.{int(match.group(2)) + 1}" if match else f"{version}+edit"
    data["updated"] = utcnow().isoformat()
    data["owner"] = user.name

    kit_row.data = data
    db.add(kit_row)
    db.commit()
    return {"kit": data}


@app.get("/api/drafts")
def list_drafts(
    user: User = Depends(current_user), db: Session = Depends(get_session)
) -> dict[str, Any]:
    statement = select(Draft).order_by(Draft.updated_at.desc())
    drafts = db.exec(statement).all()
    if user.role == "creator":
        drafts = [draft for draft in drafts if draft.creator_id == user.id]
    people = _users(db)
    out = []
    for draft in drafts:
        findings = db.exec(select(Finding).where(Finding.draft_id == draft.id)).all()
        out.append(draft_payload(draft, people.get(draft.creator_id), list(findings)))
    return {"drafts": out}


@app.get("/api/drafts/{draft_id}")
def get_draft(
    draft_id: str, user: User = Depends(current_user), db: Session = Depends(get_session)
) -> dict:
    draft = _draft_or_404(db, draft_id)
    if not _can_view(draft, user):
        raise HTTPException(status_code=403, detail="This draft belongs to another creator.")
    return _detail(db, draft, user)


@app.post("/api/drafts")
async def create_draft(
    title: str = Form(...),
    caption: str = Form(""),
    alt_text: str = Form(""),
    kit_id: str = Form("kit-northwind"),
    image: UploadFile | None = File(None),
    document: UploadFile | None = File(None),
    user: User = Depends(current_user),
    db: Session = Depends(get_session),
) -> dict:
    if user.role == "reviewer":
        raise HTTPException(status_code=403, detail="Switch to a creator or admin account to submit.")
    if not title.strip():
        raise HTTPException(status_code=400, detail="Give the draft a title.")

    stored_image: str | None = None
    doc_text = ""
    doc_name: str | None = None

    image_result = await _store_upload(image) if image else None
    if image_result and image_result[0] == "image":
        stored_image = image_result[1]

    if document:
        doc_result = await _store_upload(document)
        if doc_result and doc_result[0] == "document":
            doc_text = doc_result[1]
            doc_name = Path(document.filename or "document").name

    caption = mask_pii(caption.strip())
    doc_text = mask_pii(doc_text)

    if not caption.strip() and not doc_text.strip() and stored_image is None:
        raise HTTPException(
            status_code=400,
            detail="Add a caption, artwork, or a document to review.",
        )

    kit_row = db.get(Kit, kit_id)
    kit = kit_row.data if kit_row else _get_kit_data(db)

    draft = Draft(
        id=new_id("d"),
        kit_id=kit_id,
        creator_id=user.id,
        title=title.strip(),
        caption=caption.strip(),
        alt_text=alt_text.strip(),
        image_file=stored_image,
        doc_name=doc_name,
        doc_text=doc_text,
    )
    db.add(draft)
    db.commit()

    result = run_review(
        kit,
        draft.caption,
        draft.alt_text,
        settings.storage_dir / stored_image if stored_image else None,
        doc_text=doc_text,
    )
    for item in result["findings"]:
        db.add(
            Finding(
                id=item["id"],
                draft_id=draft.id,
                check=item["check"],
                rule_id=item["rule_id"],
                severity=item["severity"],
                title=item["title"],
                detail=item["detail"],
                quote=item["quote"],
                field=item["field"],
                source=item["source"],
                fixes=item["fixes"],
                measured=item["measured"],
            )
        )
    draft.review_meta = result["meta"]
    db.add(draft)
    add_revision(
        db,
        draft,
        user,
        "draft.created",
        f"Draft created with {len(result['findings'])} cited findings.",
    )
    db.commit()
    return _detail(db, draft, user)


@app.post("/api/drafts/{draft_id}/decisions")
def decide(
    draft_id: str,
    payload: DecisionIn,
    user: User = Depends(current_user),
    db: Session = Depends(get_session),
) -> dict:
    draft = _draft_or_404(db, draft_id)
    if draft.creator_id != user.id and user.role != "admin":
        raise HTTPException(status_code=403, detail="Only the creator can decide on this draft.")
    finding = db.get(Finding, payload.finding_id)
    if finding is None or finding.draft_id != draft.id:
        raise HTTPException(status_code=404, detail="Finding not found on this draft.")
    try:
        apply_decision(db, draft, finding, payload.action, payload.note, user, payload.fix_index)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    db.commit()
    return _detail(db, draft, user)


@app.post("/api/drafts/{draft_id}/submit")
def submit(
    draft_id: str, user: User = Depends(current_user), db: Session = Depends(get_session)
) -> dict:
    draft = _draft_or_404(db, draft_id)
    if draft.creator_id != user.id and user.role != "admin":
        raise HTTPException(status_code=403, detail="Only the creator can submit this draft.")
    if draft.status not in {"draft", "changes_requested"}:
        raise HTTPException(status_code=400, detail="This draft is not waiting to be submitted.")
    findings = db.exec(select(Finding).where(Finding.draft_id == draft.id)).all()
    unresolved = [finding for finding in findings if finding.decision is None]
    if unresolved:
        raise HTTPException(
            status_code=400,
            detail=f"Resolve all {len(unresolved)} open findings before submitting.",
        )
    draft.status = "in_review"
    draft.updated_at = utcnow()
    db.add(draft)
    add_revision(db, draft, user, "draft.submitted", "Submitted for review.")
    db.commit()
    return _detail(db, draft, user)


@app.post("/api/drafts/{draft_id}/approve")
def approve(
    draft_id: str,
    payload: NoteIn,
    user: User = Depends(current_user),
    db: Session = Depends(get_session),
) -> dict:
    draft = _draft_or_404(db, draft_id)
    if user.role not in {"reviewer", "admin"}:
        raise HTTPException(status_code=403, detail="Only a reviewer or admin can approve.")
    if draft.status != "in_review":
        raise HTTPException(status_code=400, detail="Only a draft in review can be approved.")
    findings = db.exec(select(Finding).where(Finding.draft_id == draft.id)).all()
    unresolved = [finding for finding in findings if finding.decision is None]
    if unresolved:
        raise HTTPException(
            status_code=400,
            detail=f"Resolve all {len(unresolved)} open findings before approving.",
        )
    draft.status = "approved"
    draft.approved_by = user.id
    draft.approved_at = utcnow()
    draft.updated_at = utcnow()
    db.add(draft)
    add_revision(
        db,
        draft,
        user,
        "draft.approved",
        payload.note.strip() or "Approved — every displayed finding resolves to the kit.",
    )
    db.commit()
    return _detail(db, draft, user)


@app.post("/api/drafts/{draft_id}/request-changes")
def request_changes(
    draft_id: str,
    payload: NoteIn,
    user: User = Depends(current_user),
    db: Session = Depends(get_session),
) -> dict:
    draft = _draft_or_404(db, draft_id)
    if user.role not in {"reviewer", "admin"}:
        raise HTTPException(status_code=403, detail="Only a reviewer or admin can request changes.")
    if draft.status != "in_review":
        raise HTTPException(status_code=400, detail="Only a draft in review can be sent back.")
    if not payload.note.strip():
        raise HTTPException(status_code=400, detail="Tell the creator what needs changing.")
    draft.status = "changes_requested"
    draft.updated_at = utcnow()
    db.add(draft)
    add_revision(db, draft, user, "draft.changes_requested", payload.note.strip())
    db.commit()
    return _detail(db, draft, user)


@app.post("/api/drafts/{draft_id}/rerun")
def rerun(
    draft_id: str, user: User = Depends(current_user), db: Session = Depends(get_session)
) -> dict:
    draft = _draft_or_404(db, draft_id)
    if draft.creator_id != user.id and user.role != "admin":
        raise HTTPException(status_code=403, detail="Only the creator can re-run the review.")
    if draft.status == "approved":
        raise HTTPException(status_code=400, detail="Approved drafts are locked.")
    for finding in db.exec(select(Finding).where(Finding.draft_id == draft.id)).all():
        db.delete(finding)
    db.commit()
    result = run_review(
        _get_kit_data(db),
        draft.caption,
        draft.alt_text,
        settings.storage_dir / draft.image_file if draft.image_file else None,
        doc_text=draft.doc_text or "",
    )
    for item in result["findings"]:
        db.add(
            Finding(
                id=item["id"],
                draft_id=draft.id,
                check=item["check"],
                rule_id=item["rule_id"],
                severity=item["severity"],
                title=item["title"],
                detail=item["detail"],
                quote=item["quote"],
                field=item["field"],
                source=item["source"],
                fixes=item["fixes"],
                measured=item["measured"],
            )
        )
    draft.review_meta = result["meta"]
    draft.updated_at = utcnow()
    db.add(draft)
    add_revision(
        db,
        draft,
        user,
        "review.rerun",
        f"Review re-run: {len(result['findings'])} cited findings.",
    )
    db.commit()
    return _detail(db, draft, user)


@app.get("/api/insights")
def insights(user: User = Depends(current_user), db: Session = Depends(get_session)) -> dict:
    drafts = db.exec(select(Draft)).all()
    findings = db.exec(select(Finding)).all()
    rules = {rule["id"]: rule for rule in _get_kit_data(db).get("rules", [])}

    flagged: dict[str, int] = defaultdict(int)
    overridden: dict[str, int] = defaultdict(int)
    decided: dict[str, int] = defaultdict(int)
    by_check: dict[str, int] = defaultdict(int)
    received = kept = dropped = 0
    durations = []

    for finding in findings:
        flagged[finding.rule_id] += 1
        by_check[finding.check] += 1
        if finding.decision:
            decided[finding.rule_id] += 1
        if finding.decision == "kept":
            overridden[finding.rule_id] += 1

    for draft in drafts:
        meta = draft.review_meta or {}
        lock = meta.get("citation_lock") or {}
        received += int(lock.get("received") or 0)
        kept += int(lock.get("kept") or 0)
        dropped += int(lock.get("dropped") or 0)
        if meta.get("duration_ms"):
            durations.append(int(meta["duration_ms"]))

    def rule_row(rule_id: str, count: int) -> dict:
        rule = rules.get(rule_id, {"label": rule_id, "check": "other", "severity": "soft"})
        return {
            "rule_id": rule_id,
            "label": rule["label"],
            "check": rule["check"],
            "severity": rule["severity"],
            "count": count,
        }

    most_flagged = sorted(
        (rule_row(rule_id, count) for rule_id, count in flagged.items()),
        key=lambda row: row["count"],
        reverse=True,
    )[:5]

    overridden_rows = []
    for rule_id, count in overridden.items():
        total = decided.get(rule_id, count)
        rate = count / total if total else 0
        row = rule_row(rule_id, count)
        row.update(
            {
                "decided": total,
                "rate": round(rate * 100),
                "ambiguous": count >= 2 and rate >= 0.4,
            }
        )
        overridden_rows.append(row)
    overridden_rows.sort(key=lambda row: (row["count"], row["rate"]), reverse=True)

    coverage = round((kept / received) * 100, 1) if received else 100.0
    return {
        "most_flagged": most_flagged,
        "most_overridden": overridden_rows[:5],
        "by_check": [{"check": key, "count": value} for key, value in sorted(by_check.items())],
        "totals": {
            "drafts": len(drafts),
            "approved": sum(1 for draft in drafts if draft.status == "approved"),
            "pending": sum(1 for draft in drafts if draft.status == "in_review"),
            "findings": len(findings),
            "decided": sum(1 for finding in findings if finding.decision),
            "accepted": sum(1 for finding in findings if finding.decision == "accepted"),
            "kept": sum(1 for finding in findings if finding.decision == "kept"),
            "citation_received": received,
            "citation_kept": kept,
            "citation_dropped": dropped,
            "citation_coverage": coverage,
            "avg_review_ms": round(sum(durations) / len(durations)) if durations else 0,
        },
        "model": model_identity(),
    }


@app.get("/api/files/{name}")
def get_file(
    name: str, user: User = Depends(current_user)
) -> FileResponse:
    if "/" in name or "\\" in name or ".." in name:
        raise HTTPException(status_code=400, detail="Invalid file name.")
    path = settings.storage_dir / name
    if not path.is_file():
        raise HTTPException(status_code=404, detail="File not found.")
    return FileResponse(path)


FRONTEND_DIST = settings.base_dir.parent / "frontend" / "dist"
if (FRONTEND_DIST / "assets").is_dir():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")


@app.get("/{full_path:path}")
def spa(full_path: str) -> FileResponse:
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Not found.")
    index = FRONTEND_DIST / "index.html"
    if not index.is_file():
        raise HTTPException(
            status_code=503,
            detail="Frontend is not built yet. Run `npm install && npm run build` in frontend/.",
        )
    candidate = FRONTEND_DIST / full_path
    if full_path and candidate.is_file():
        return FileResponse(candidate)
    return FileResponse(index)
