#!/usr/bin/env python3
"""Live end-to-end API suite for PrismCheck AI.

Requires a running server (the app or a deployed instance):

    uvicorn app.main:app --host 127.0.0.1 --port 8000
    python backend/tests/e2e_live.py          # default http://127.0.0.1:8000
    PRISMCHECK_E2E_BASE=https://tech-coders.onrender.com python backend/tests/e2e_live.py
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import httpx
from fpdf import FPDF

BASE = os.getenv("PRISMCHECK_E2E_BASE", "http://127.0.0.1:8000").rstrip("/")
PASS: list[str] = []
FAILURES: list[str] = []


def check(name: str, cond: bool, extra: object = "") -> None:
    if cond:
        PASS.append(name)
        print(f"PASS  {name}")
    else:
        FAILURES.append(name)
        print(f"FAIL  {name}  {extra}")


def login(email: str, password: str = "demo123") -> httpx.Client:
    client = httpx.Client(base_url=BASE, timeout=30)
    response = client.post("/api/session", json={"email": email, "password": password})
    if response.status_code != 200:
        raise RuntimeError(f"login failed for {email}: {response.status_code} {response.text}")
    return client


def create_draft(client, title, caption="", alt="", files=None):
    data = {"title": title, "caption": caption, "alt_text": alt, "kit_id": "kit-northwind"}
    return client.post("/api/drafts", data=data, files=files)


def build_sample_files(tmp: Path) -> dict:
    pdf_path = tmp / "sample.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, "Earn 5% cashback guaranteed for life. Act now.\nContact support@example.com or +91 98765 43210.")
    pdf.output(str(pdf_path))

    docx_path = tmp / "sample.docx"
    docxml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:body><w:p><w:r><w:t>Approval is guaranteed within 24 hours. Act now.</w:t></w:r></w:p>'
        "</w:body></w:document>"
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        "</Types>"
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        "</Relationships>"
    )
    with ZipFile(docx_path, "w", ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", docxml)

    return {
        "pdf": pdf_path,
        "docx": docx_path,
        "oversized": tmp / "oversized.pdf",
        "corrupt": tmp / "corrupt.png",
        "txt": tmp / "notes.txt",
    }


def main() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="prism-e2e-"))
    files = build_sample_files(tmp)
    files["oversized"].write_bytes(b"x" * (9 * 1024 * 1024))
    files["corrupt"].write_bytes(b"not a real png")
    files["txt"].write_text("plain text")
    clean = Path("backend/storage/seed-clean.png")
    offbrand = Path("backend/storage/seed-offbrand.png")

    # A. Auth
    bad = httpx.Client(base_url=BASE, timeout=30)
    r = bad.post("/api/session", json={"email": "ananya@northwind.example", "password": "wrongpass"})
    check("A1 wrong password rejected 401", r.status_code == 401, r.status_code)

    ananya = login("ananya@northwind.example")
    rohan = login("rohan@northwind.example")
    reviewer = login("kabir@northwind.example")
    admin = login("meera@northwind.example")
    check("A2 all four demo roles sign in", True)
    session = ananya.get("/api/session")
    check("A3 session persists via cookie", session.json()["user"]["id"] == "u-creator")

    # B. Independence
    a_drafts = ananya.get("/api/drafts").json()["drafts"]
    r_drafts = rohan.get("/api/drafts").json()["drafts"]
    k_drafts = reviewer.get("/api/drafts").json()["drafts"]
    m_drafts = admin.get("/api/drafts").json()["drafts"]
    check("B1 Ananya sees only her 6 seeded drafts", len(a_drafts) == 6 and all(d["creator_id"] == "u-creator" for d in a_drafts), len(a_drafts))
    check("B2 Rohan starts with an empty workspace", r_drafts == [])
    check("B3 reviewer sees all drafts", len(k_drafts) >= 6, len(k_drafts))
    check("B4 admin sees all drafts", len(m_drafts) >= 6, len(m_drafts))

    # C. Caption journey
    r = create_draft(rohan, "Bad caption journey", "Earn 5% cashback guaranteed for life. Act now.")
    body = r.json()
    rules = {f["rule_id"] for f in body["findings"]}
    check("C1 caption draft created with cited findings", r.status_code == 200 and {"T-14", "C-01", "T-02"} <= rules, rules)
    check("C2 citation coverage 100%", body["draft"]["review_meta"]["citation_lock"]["kept"] == len(body["findings"]))
    draft_id = body["draft"]["id"]
    findings = body["findings"]
    t14 = next(f for f in findings if f["rule_id"] == "T-14")

    r = rohan.post(f"/api/drafts/{draft_id}/decisions", json={"finding_id": t14["id"], "action": "accept", "fix_index": 0, "note": "fix guarantee"})
    check("C3 T-14 fix accepted", r.status_code == 200, f"{r.status_code} {r.text[:80]}")
    check("C4 caption rewritten after fix", "guaranteed" not in r.json()["draft"]["caption"], r.json()["draft"]["caption"])

    for f in findings:
        if f["id"] == t14["id"]:
            continue
        rr = rohan.post(f"/api/drafts/{draft_id}/decisions", json={"finding_id": f["id"], "action": "accept", "fix_index": 0, "note": "fix"})
        check(f"C5 decide {f['rule_id']}", rr.status_code == 200, f"{rr.status_code}")

    rr = rohan.post(f"/api/drafts/{draft_id}/decisions", json={"finding_id": t14["id"], "action": "keep", "note": "again"})
    check("C6 duplicate decision blocked 400", rr.status_code == 400, f"{rr.status_code}")

    r = rohan.post(f"/api/drafts/{draft_id}/submit")
    check("C7 submit for review", r.status_code == 200 and r.json()["draft"]["status"] == "in_review", r.text[:80])
    r = rohan.post(f"/api/drafts/{draft_id}/submit")
    check("C8 double submit blocked 400", r.status_code == 400, f"{r.status_code}")
    r = reviewer.post(f"/api/drafts/{draft_id}/approve", json={"note": "ok"})
    check("C9 reviewer approves", r.status_code == 200 and r.json()["draft"]["status"] == "approved", r.text[:80])
    r = reviewer.post(f"/api/drafts/{draft_id}/approve", json={"note": "again"})
    check("C10 double approve blocked 400", r.status_code == 400, f"{r.status_code}")
    r = rohan.post(f"/api/drafts/{draft_id}/rerun")
    check("C11 rerun on approved blocked 400", r.status_code == 400, f"{r.status_code}")

    # D. Request-changes loop
    r = create_draft(rohan, "Clean draft flow", "No annual fee in year one on the Northwind Signature card.")
    clean_id = r.json()["draft"]["id"]
    check("D1 clean draft has zero findings", r.json()["draft"]["finding_count"] == 0)
    r = rohan.post(f"/api/drafts/{clean_id}/submit")
    check("D2 clean draft submits immediately", r.status_code == 200, r.text[:80])
    r = reviewer.post(f"/api/drafts/{clean_id}/request-changes", json={"note": "tone it down"})
    check("D3 reviewer requests changes", r.status_code == 200 and r.json()["draft"]["status"] == "changes_requested", r.text[:80])
    r = rohan.post(f"/api/drafts/{clean_id}/submit")
    check("D4 creator resubmits", r.status_code == 200 and r.json()["draft"]["status"] == "in_review", r.text[:80])
    r = reviewer.post(f"/api/drafts/{clean_id}/approve", json={"note": "approved"})
    check("D5 approved after loop", r.json()["draft"]["status"] == "approved")

    # E. Images and bad inputs
    with open(clean, "rb") as fh:
        r = create_draft(rohan, "clean no alt", files={"image": ("clean.png", fh, "image/png")})
    check("E1 clean image-only accepted", r.status_code == 200, f"{r.status_code} {r.text[:80]}")
    check("E2 missing alt flagged A-03 only", {f["rule_id"] for f in r.json()["findings"]} == {"A-03"})

    with open(offbrand, "rb") as fh:
        r = create_draft(rohan, "offbrand no alt", files={"image": ("offbrand.png", fh, "image/png")})
    rules = {f["rule_id"] for f in r.json()["findings"]}
    check("E3 offbrand flags V-05 and A-03", "V-05" in rules and "A-03" in rules, rules)

    with open(files["corrupt"], "rb") as fh:
        r = create_draft(rohan, "corrupt image", files={"image": ("corrupt.png", fh, "image/png")})
    check("E4 corrupt image rejected 400", r.status_code == 400 and "could not be read" in r.text, f"{r.status_code} {r.text[:80]}")

    with open(files["txt"], "rb") as fh:
        r = create_draft(rohan, "txt doc", files={"document": ("notes.txt", fh, "text/plain")})
    check("E5 txt rejected 400 with allowed list", r.status_code == 400 and "Upload a PNG" in r.text, f"{r.status_code}")

    with open(files["oversized"], "rb") as fh:
        r = create_draft(rohan, "oversized", files={"document": ("oversized.pdf", fh, "application/pdf")})
    check("E6 oversized rejected 413", r.status_code == 413 and "limited to 8 MB" in r.text, f"{r.status_code}")

    r = create_draft(rohan, "")
    check("E7 missing title rejected 4xx", 400 <= r.status_code < 500, f"{r.status_code}")
    r = create_draft(rohan, "nothing")
    check("E8 no content rejected 400", r.status_code == 400, f"{r.status_code}")

    # F. Documents
    with open(files["pdf"], "rb") as fh:
        r = create_draft(rohan, "pdf sample", files={"document": ("sample.pdf", fh, "application/pdf")})
    body = r.json()
    rules = {f["rule_id"] for f in body["findings"]}
    check("F1 PDF extracted and flagged", "T-14" in rules and "C-01" in rules and "T-02" in rules, rules)
    doc_text = body["draft"].get("doc_text") or ""
    check("F2 PDF text PII-masked", "[email]" in doc_text and "[phone]" in doc_text, doc_text[:100])

    with open(files["docx"], "rb") as fh:
        r = create_draft(rohan, "docx sample", files={"document": ("sample.docx", fh, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")})
    rules = {f["rule_id"] for f in r.json()["findings"]}
    check("F3 DOCX extracted and flagged", "T-14" in rules and "T-02" in rules, rules)

    # G. Submit guard
    r = create_draft(rohan, "unresolved", "Earn 5% cashback for life.")
    unresolved_id = r.json()["draft"]["id"]
    r = rohan.post(f"/api/drafts/{unresolved_id}/submit")
    check("G1 submit with open findings blocked 400", r.status_code == 400, f"{r.status_code}")

    # H. Role guards
    r = create_draft(reviewer, "reviewer tries", "Earn 2.5% cashback on everyday spend, capped at ₹12,000 a year.")
    check("H1 reviewer cannot create 403", r.status_code == 403, f"{r.status_code}")
    r = create_draft(rohan, "approve attempt", "Earn 5% cashback for life.")
    guard_id = r.json()["draft"]["id"]
    for f in r.json()["findings"]:
        rohan.post(f"/api/drafts/{guard_id}/decisions", json={"finding_id": f["id"], "action": "accept", "fix_index": 0, "note": "x"})
    rohan.post(f"/api/drafts/{guard_id}/submit")
    r = rohan.post(f"/api/drafts/{guard_id}/approve", json={"note": "x"})
    check("H2 creator cannot approve 403", r.status_code == 403, f"{r.status_code}")
    r = ananya.get(f"/api/drafts/{guard_id}")
    check("H3 another creator cannot view 403", r.status_code == 403, f"{r.status_code}")

    # I. Kit editing
    r = rohan.patch("/api/kit", json={"audience": "hack"})
    check("I1 creator cannot edit kit 403", r.status_code == 403, f"{r.status_code}")
    r = admin.patch("/api/kit", json={"audience": "Retail banking customers in India, aged 21 and over."})
    check("I2 admin edits kit", r.status_code == 200, f"{r.status_code} {r.text[:80]}")
    kit = r.json()["kit"]
    check("I3 version bumped to 4.3+", kit["version"] == "4.3", kit["version"])
    check("I4 history recorded", len(kit.get("history") or []) >= 1, len(kit.get("history") or []))

    # J. Insights
    insights = reviewer.get("/api/insights").json()
    check("J1 insights totals returned", insights["totals"]["drafts"] >= 6, insights["totals"])
    check("J2 most-flagged rules returned", len(insights["most_flagged"]) > 0)

    # K. Health and SPA
    health = httpx.get(f"{BASE}/api/health")
    check("K1 health 200", health.status_code == 200 and health.json()["status"] == "ok")
    root = httpx.get(f"{BASE}/")
    check("K2 root SPA served 200", root.status_code == 200 and "PrismCheck" in root.text)

    print()
    print(f"TOTAL CHECKED {len(PASS) + len(FAILURES)}  PASSED {len(PASS)}  FAILED {len(FAILURES)}")
    if FAILURES:
        print("FAILURES:", FAILURES)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
