from __future__ import annotations

from datetime import timedelta
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from sqlmodel import Session, select

from .auth import DEMO_PASSWORD, hash_password
from .config import settings
from .engine import run_review
from .kit_seed import KIT
from .models import Draft, Finding, Kit, Revision, User, utcnow
from .services import add_revision, apply_decision, new_id

USERS = [
    User(
        id="u-creator",
        name="Ananya Rao",
        role="creator",
        email="ananya@northwind.example",
        initials="AR",
        password_hash=hash_password(DEMO_PASSWORD),
    ),
    User(
        id="u-reviewer",
        name="Kabir Menon",
        role="reviewer",
        email="kabir@northwind.example",
        initials="KM",
        password_hash=hash_password(DEMO_PASSWORD),
    ),
    User(
        id="u-admin",
        name="Meera Shah",
        role="admin",
        email="meera@northwind.example",
        initials="MS",
        password_hash=hash_password(DEMO_PASSWORD),
    ),
]


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    path = settings.base_dir.parent / "project_docs" / "fonts" / "Ubuntu-Bold.ttf"
    try:
        return ImageFont.truetype(str(path), size)
    except Exception:
        return ImageFont.load_default()


def _banner(
    path: Path,
    background: str,
    headline: str,
    subhead: str,
    headline_colour: str,
    sub_colour: str,
    brand_colour: str,
    accent: str | None = None,
) -> None:
    image = Image.new("RGB", (1200, 630), background)
    draw = ImageDraw.Draw(image)
    if accent:
        draw.rectangle([80, 120, 96, 430], fill=accent)
    draw.text((130, 150), headline, font=_font(76), fill=headline_colour)
    draw.text((130, 255), subhead, font=_font(46), fill=sub_colour)
    draw.text((130, 360), "SIGNATURE CARD", font=_font(52), fill=sub_colour)
    draw.text((130, 545), "NORTHWIND BANK", font=_font(28), fill=brand_colour)
    image.save(path, format="PNG")


def _seed_images() -> tuple[Path, Path]:
    folder = settings.storage_dir
    folder.mkdir(parents=True, exist_ok=True)
    offbrand = folder / "seed-offbrand.png"
    clean = folder / "seed-clean.png"
    _banner(
        offbrand,
        "#8B1E3F",
        "5% CASHBACK",
        "ON EVERYTHING",
        "#B0838D",
        "#C79AA3",
        "#E7C9CF",
    )
    _banner(
        clean,
        "#1B2A6B",
        "2.5% CASHBACK",
        "ON EVERYDAY SPEND",
        "#EEF1FB",
        "#EEF1FB",
        "#FFFFFF",
        accent="#E4572E",
    )
    return offbrand, clean


def _store_findings(session: Session, draft: Draft, result: dict) -> list[Finding]:
    findings: list[Finding] = []
    for item in result["findings"]:
        finding = Finding(
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
        session.add(finding)
        findings.append(finding)
    draft.review_meta = result["meta"]
    session.add(draft)
    return findings


def _pick(findings: list[Finding], rule_id: str, needle: str | None = None) -> Finding | None:
    for finding in findings:
        if finding.rule_id != rule_id or finding.decision is not None:
            continue
        if needle and needle.lower() not in (finding.quote + " " + finding.title).lower():
            continue
        return finding
    return None


def seed_if_empty(session: Session) -> None:
    if session.exec(select(User)).first():
        return

    for user in USERS:
        session.add(user)

    kit = Kit(id=KIT["id"], name=KIT["name"], client=KIT["client"], data=KIT)
    session.add(kit)
    session.commit()

    offbrand, clean = _seed_images()
    now = utcnow()
    creator = USERS[0]
    reviewer = USERS[1]

    # 1 — the demo draft: every check fires.
    draft = Draft(
        id="d-1001",
        kit_id=kit.id,
        creator_id=creator.id,
        title="Signature card launch",
        caption=(
            "Earn 5% cashback on everything, with no annual fee for life. "
            "100% guaranteed approval. Act now and grab your card."
        ),
        alt_text="",
        image_file=offbrand.name,
        status="in_review",
        created_at=now - timedelta(hours=3),
        updated_at=now - timedelta(hours=2),
    )
    session.add(draft)
    session.commit()
    result = run_review(KIT, draft.caption, draft.alt_text, offbrand, use_model=False)
    findings = _store_findings(session, draft, result)
    add_revision(session, draft, creator, "draft.created", "Draft created with a banner image.")
    add_revision(
        session,
        draft,
        creator,
        "review.completed",
        f"{len(findings)} cited findings · {result['meta']['rules_checked']} kit items checked.",
    )
    visual = _pick(findings, "V-05")
    if visual:
        apply_decision(
            session,
            draft,
            visual,
            "keep",
            "Seasonal campaign variant approved by the brand lead.",
            creator,
        )
    session.commit()

    # 2 — approved, clean, no findings.
    draft = Draft(
        id="d-1002",
        kit_id=kit.id,
        creator_id=creator.id,
        title="Cashback that adds up",
        caption=(
            "Earn 2.5% cashback on everyday spend, capped at ₹12,000 a year. "
            "No annual fee in year one on the Signature card."
        ),
        alt_text="Northwind Signature card artwork with 2.5% cashback on everyday spend.",
        image_file=clean.name,
        status="approved",
        created_at=now - timedelta(days=2),
        updated_at=now - timedelta(days=1, hours=4),
        approved_by=reviewer.id,
        approved_at=now - timedelta(days=1, hours=4),
    )
    session.add(draft)
    session.commit()
    result = run_review(KIT, draft.caption, draft.alt_text, clean, use_model=False)
    _store_findings(session, draft, result)
    add_revision(session, draft, creator, "draft.created", "Draft created with a banner image.")
    add_revision(session, draft, creator, "review.completed", "0 findings. Silent pass.")
    add_revision(session, draft, creator, "draft.submitted", "Submitted for review.")
    add_revision(session, draft, reviewer, "draft.approved", "Approved — every claim resolves to a fact.")
    session.commit()

    # 3 — changes requested.
    draft = Draft(
        id="d-1003",
        kit_id=kit.id,
        creator_id=creator.id,
        title="Festive top-up offer",
        caption=(
            "Cheap top-ups with guaranteed rewards. Users can grab a festive bonus today. Act now."
        ),
        alt_text="",
        status="changes_requested",
        created_at=now - timedelta(days=1, hours=2),
        updated_at=now - timedelta(hours=20),
    )
    session.add(draft)
    session.commit()
    result = run_review(KIT, draft.caption, draft.alt_text, None, use_model=False)
    findings = _store_findings(session, draft, result)
    add_revision(session, draft, creator, "draft.created", "Text-only draft created.")
    add_revision(session, draft, creator, "review.completed", f"{len(findings)} cited findings.")
    add_revision(session, draft, creator, "draft.submitted", "Submitted for review.")
    preferred = _pick(findings, "T-03", "cheap")
    if preferred:
        apply_decision(
            session,
            draft,
            preferred,
            "keep",
            "The campaign uses the word deliberately; brand lead is reviewing it.",
            creator,
        )
    add_revision(
        session,
        draft,
        reviewer,
        "draft.changes_requested",
        "Please remove the guarantee and the urgency before this goes live.",
    )
    session.commit()

    # 4 — approved after an override: feeds Guideline Health.
    draft = Draft(
        id="d-1004",
        kit_id=kit.id,
        creator_id=creator.id,
        title="Weekend cashback push",
        caption="Earn 2.5% cashback on everyday spend. 100% guaranteed approval.",
        alt_text="",
        image_file=offbrand.name,
        status="in_review",
        created_at=now - timedelta(days=4),
        updated_at=now - timedelta(days=3),
    )
    session.add(draft)
    session.commit()
    result = run_review(KIT, draft.caption, draft.alt_text, offbrand, use_model=False)
    findings = _store_findings(session, draft, result)
    add_revision(session, draft, creator, "draft.created", "Draft created with a banner image.")
    banned = _pick(findings, "T-14")
    if banned:
        apply_decision(session, draft, banned, "accept", "", creator)
    alt = _pick(findings, "A-03", "alt text")
    if alt:
        apply_decision(session, draft, alt, "accept", "", creator)
    contrast = _pick(findings, "A-03", "contrast")
    if contrast:
        apply_decision(
            session,
            draft,
            contrast,
            "keep",
            "Legacy banner reused from the approved print campaign.",
            creator,
        )
    visual = _pick(findings, "V-05")
    if visual:
        apply_decision(
            session,
            draft,
            visual,
            "keep",
            "The maroon field is the approved festive variant.",
            creator,
        )
    add_revision(session, draft, creator, "draft.submitted", "Submitted for review.")
    add_revision(session, draft, reviewer, "draft.approved", "Approved with two recorded exceptions.")
    draft.status = "approved"
    draft.approved_by = reviewer.id
    draft.approved_at = now - timedelta(days=3)
    session.add(draft)
    session.commit()

    # 5 — approved, silent pass.
    draft = Draft(
        id="d-1005",
        kit_id=kit.id,
        creator_id=creator.id,
        title="Account safety notice",
        caption=(
            "Your account is protected. We will not ask for your PIN or password. "
            "If you notice something unusual, contact support."
        ),
        alt_text="",
        status="approved",
        created_at=now - timedelta(days=6),
        updated_at=now - timedelta(days=5),
        approved_by=reviewer.id,
        approved_at=now - timedelta(days=5),
    )
    session.add(draft)
    session.commit()
    result = run_review(KIT, draft.caption, draft.alt_text, None, use_model=False)
    _store_findings(session, draft, result)
    add_revision(session, draft, creator, "draft.created", "Text-only safety notice created.")
    add_revision(session, draft, creator, "review.completed", "0 findings. Silent pass.")
    add_revision(session, draft, reviewer, "draft.approved", "Approved.")
    session.commit()

    # 6 — a fresh draft, so the queue has work to do.
    draft = Draft(
        id="d-1006",
        kit_id=kit.id,
        creator_id=creator.id,
        title="Referral offer draft",
        caption="Invite a friend and you could both earn rewards. Terms apply.",
        alt_text="",
        status="draft",
        created_at=now - timedelta(minutes=40),
        updated_at=now - timedelta(minutes=40),
    )
    session.add(draft)
    session.commit()
    result = run_review(KIT, draft.caption, draft.alt_text, None, use_model=False)
    _store_findings(session, draft, result)
    add_revision(session, draft, creator, "draft.created", "Draft created.")
    add_revision(session, draft, creator, "review.completed", "0 findings. Silent pass.")
    session.commit()
