#!/usr/bin/env python3
"""Build PrismCheck AI — Round 3 Submission PDF.

Run from the repository root:
    python project_docs/build_pdf_round3.py

Output:
    project_docs/PrismCheck_Round3_Submission.pdf
"""

from __future__ import annotations

from pathlib import Path

from fpdf import FPDF

HERE = Path(__file__).resolve().parent
FONT_BOLD = HERE / "fonts" / "Ubuntu-Bold.ttf"
FONT_REGULAR = HERE / "fonts" / "Ubuntu-Regular.ttf"

INK = (20, 22, 34)
MUTED = (100, 104, 116)
TEAL = (0, 120, 120)
GREEN = (24, 140, 84)
AMBER = (176, 110, 12)
RED = (190, 40, 40)
LIGHT = (243, 245, 247)

LIVE_URL = "https://tech-coders.onrender.com/"
REPO_URL = "https://github.com/venkatanarayana15/tech-coders"
PDF_URL = REPO_URL + "/blob/main/project_docs/PrismCheck_Round3_Submission.pdf"


class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("UB", "", 7.5)
        self.set_text_color(*MUTED)
        self.cell(0, 6, "PrismCheck AI | Round 3 Submission | Team A2Z Creators", align="R")
        self.ln(7)

    def footer(self):
        self.set_y(-12)
        self.set_font("U", "", 7.5)
        self.set_text_color(*MUTED)
        self.cell(0, 6, f"Page {self.page_no()}", align="C")


def section(pdf, number, title):
    pdf.add_page()
    pdf.ln(2)
    pdf.set_font("UB", "", 13.5)
    pdf.set_text_color(*INK)
    pdf.cell(0, 7, f"{number}. {title}")
    pdf.ln(8)


def subhead(pdf, text, color=INK):
    pdf.ln(1.5)
    pdf.set_font("UB", "", 10.6)
    pdf.set_text_color(*color)
    pdf.cell(0, 6, text)
    pdf.ln(6)


def bullets(pdf, items, size=8.6, lh=4.6):
    pdf.set_font("U", "", size)
    pdf.set_text_color(*INK)
    for item in items:
        pdf.multi_cell(0, lh, f"- {item}")
        pdf.ln(1)


def kv(pdf, rows, label_w=38, size=8.8, lh=4.8):
    pdf.set_font("U", "", size)
    for label, value in rows:
        pdf.set_font("UB", "", size)
        pdf.cell(label_w, lh, label)
        pdf.set_font("U", "", size)
        pdf.set_text_color(*INK)
        pdf.multi_cell(0, lh, value)
        pdf.ln(0.8)


def para(pdf, text, size=8.8, lh=4.8, color=INK):
    pdf.set_font("U", "", size)
    pdf.set_text_color(*color)
    pdf.multi_cell(0, lh, text)
    pdf.ln(1.2)


def build():
    pdf = PDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.add_font("UB", "", str(FONT_BOLD))
    pdf.add_font("U", "", str(FONT_REGULAR))
    pdf.set_margins(16, 16, 16)

    # ---------------------------------------------------------------- cover
    pdf.add_page()
    pdf.ln(30)
    pdf.set_font("UB", "", 26)
    pdf.set_text_color(*INK)
    pdf.cell(0, 10, "PrismCheck AI")
    pdf.ln(2)
    pdf.set_font("U", "", 14)
    pdf.set_text_color(*TEAL)
    pdf.cell(0, 8, "Round 3 Submission - the finished product")
    pdf.ln(12)
    pdf.set_font("U", "", 10.5)
    pdf.set_text_color(*MUTED)
    pdf.cell(0, 6, "Team A2Z Creators | Tech Circuit 2026")
    pdf.ln(5)
    pdf.cell(0, 6, f"Live: {LIVE_URL}")
    pdf.ln(5)
    pdf.cell(0, 6, f"Source: {REPO_URL}")
    pdf.ln(5)
    pdf.cell(0, 6, f"PDF: {PDF_URL}")
    pdf.ln(14)
    pdf.set_font("U", "", 9.5)
    pdf.set_text_color(*INK)
    pdf.multi_cell(
        0,
        6,
        "A pre-publication brand-governance review workspace. It reviews captions, artwork, PDFs, and DOCX files "
        "against a structured brand kit, cites every finding to the exact rule or approved fact, and keeps a human "
        "in the approval loop.",
    )

    # ---------------------------------------------------------------- 1 summary
    section(pdf, 1, "Executive summary")
    kv(pdf, [
        ("Product", "Deployed web app. Judges only need the live link and the printed demo credentials."),
        ("Journey", "Sign in -> create a review -> see cited findings -> fix or keep with note -> submit -> review -> approve -> insights."),
        ("Three improvements", "All three committed improvements are implemented and observable; one is delivered with an honest scope note (see section 5)."),
        ("Testing", "47/47 live end-to-end checks pass on a fresh database; 7 unit tests pass; clean-clone verified."),
        ("Verification", f"Live health check: {LIVE_URL}api/health returns 200 with engine status ready."),
    ])

    # ---------------------------------------------------------------- 2 features
    section(pdf, 2, "Complete list of features")
    subhead(pdf, "Access and identity")
    bullets(pdf, [
        "Role-based demo sign-in with email and password; all demo credentials are printed on the login page.",
        "Signed HttpOnly cookie sessions that survive refresh.",
        "Server-side role enforcement for creator, reviewer, and admin.",
        "Per-user workspace independence: creators see only their own drafts; reviewers and admins see the shared workspace.",
    ])
    subhead(pdf, "Review workspace")
    bullets(pdf, [
        "Creator dashboard with live counts, search, status filters, and priority queues.",
        "New review from a caption, artwork upload, PDF upload, or DOCX upload.",
        "Artwork validation for PNG, JPG, and WebP; clear rejection for unreadable files.",
        "PDF text extraction and review; DOCX text extraction and review.",
        "PII masking on ingest for emails, phone numbers, and Aadhaar-style IDs.",
    ])
    subhead(pdf, "Review engine checks")
    bullets(pdf, [
        "Claims against the approved fact bank (C-01).",
        "Banned absolute-guarantee review (T-14).",
        "Urgency and absolute-language review (T-02).",
        "Preferred-vocabulary review (T-03).",
        "CIELAB palette-distance review (V-05).",
        "WCAG contrast and alt-text requirement (A-03).",
        "Citation Lock: every displayed finding resolves to a real kit item; uncited findings are dropped and counted.",
    ])
    subhead(pdf, "Workflow and decisions")
    bullets(pdf, [
        "One-click fixes grounded in approved facts, with capitalization preserved.",
        "Keep-as-is decision with a required reason.",
        "Draft lifecycle: draft -> submitted -> approved / changes requested, with backend guards.",
        "Submit guard blocks drafts with unresolved findings.",
        "Reviewer approve and request-changes actions with notes.",
        "Approved drafts are locked against further edits.",
        "Re-run review against the current kit.",
        "Revision timeline and audit trail on every draft.",
    ])
    subhead(pdf, "Kit and insights")
    bullets(pdf, [
        "Brand Kit reference: 7 rules, 5 approved facts, 5 palette colours, 10 language entries, each addressable by ID.",
        "Admin Brand Kit editor with automatic version bump and a history trail.",
        "Insights page: citation coverage, most-flagged rules, most-overridden rules, ambiguous-guideline signal, decision rate, and average review time.",
        "Clean compliant drafts pass with zero findings.",
        "Health endpoint and SPA served by the same FastAPI process.",
        "Seeded demo workspace plus a clean second creator workspace.",
    ])

    # ---------------------------------------------------------------- 3 architecture
    section(pdf, 3, "Technical architecture and implementation")
    subhead(pdf, "Components")
    bullets(pdf, [
        "Frontend: React 18 + Vite 5, handcrafted CSS; production build in frontend/dist is served by FastAPI from the same origin.",
        "Backend: FastAPI 0.141 on Python 3.14+; SQLModel + SQLite; signed HttpOnly cookie sessions.",
        "Images: Pillow 12 + numpy 2.5 for CIELAB DeltaE palette checks and WCAG contrast.",
        "Documents: pypdf 6 for PDFs; zip/XML extraction for DOCX.",
        "Review engine: deterministic in-process engine by default; optional Gemini 2.5 Flash / Ollama adapters, with Citation Lock enforced on every finding.",
        "Infrastructure: Render Python web service defined in render.yaml; health check at /api/health.",
    ])
    subhead(pdf, "How components talk")
    para(pdf, "The browser talks only to the FastAPI JSON/multipart API. Sessions are signed HttpOnly cookies. Every route re-checks the user's role on the server, so UI hiding is never the security boundary.")
    subhead(pdf, "Data flow")
    para(pdf, "A draft is created from caption/alt text/uploads. Text and images are PII-masked, then stored. The deterministic engine runs checks and attaches a source_id to every candidate finding. The Citation Lock resolves each source_id against the kit; findings without a valid source are dropped and counted. Findings and a revision record are persisted, and payloads are returned to the UI.")
    subhead(pdf, "Models and APIs")
    para(pdf, "Core tables: User, Kit (JSON data), Draft, Finding (JSON fixes and measured values), Revision. Key endpoints: /api/session, /api/users, /api/bootstrap, /api/kit (GET/PATCH), /api/drafts, /api/drafts/{id}/decisions, /submit, /approve, /request-changes, /rerun, /api/insights, /api/files/{name}.")
    subhead(pdf, "Hardest problem solved")
    para(pdf, "Guaranteeing that every displayed finding is defensible. The Citation Lock is a single server-side choke point: an uncited or unmatched finding can never reach the screen. A close second was keeping fixes correct when edits shift text: decisions now record an explicit note when the exact quote is no longer present, instead of silently doing nothing.")

    # ---------------------------------------------------------------- 4 testing
    section(pdf, 4, "Testing details")
    subhead(pdf, "What we tested and how")
    bullets(pdf, [
        "Unit tests (pytest): 7 tests cover overlapping-claim deduplication, approved-fact silence, banned-promise hard stop, urgent-tone soft note, PII masking, and stale-quote replacement behavior.",
        "Evaluation harness (backend/evaluate.py): 30 synthetic-labelled cases; precision 0.900, recall 0.900, F1 0.900, false-positive rate 0.100.",
        "Live end-to-end suite (backend/tests/e2e_live.py): 47 checks against a running server on a fresh database - auth, user independence, full caption journey, request-changes loop, image-only and off-brand uploads, real PDF/DOCX extraction, bad inputs, submit/approve guards, role 403s, kit editing, insights, and health/SPA. Result: 47/47 passed.",
        "Manual browser testing on the deployed link: credentials visible on the login page; admin signs in with email + password; edit-save bumps kit version 4.3 to 4.4; new frontend bundle serves after deploy.",
        "Clean-clone verification: fresh clone, pip install -r backend/requirements.txt, uvicorn start, / serves the SPA and /api/health returns 200; npm ci and npm run build also succeed.",
    ])
    subhead(pdf, "What we found and fixed")
    bullets(pdf, [
        "Image-only uploads were rejected -> fixed in backend and frontend.",
        "Missing title returned 422 -> now a clean 400.",
        "Overlapping claim text produced duplicate C-01 findings -> deduplicated.",
        "A stale quote could silently no-op a fix -> decisions now record a clear note when no text changed.",
        "Double submit/approve/decide could slip through -> now blocked with 400.",
    ])
    subhead(pdf, "Still known to be imperfect")
    bullets(pdf, [
        "Evaluation labels are synthetic, not a real 30-draft dataset.",
        "No OCR: scanned/image-only PDFs are rejected with a clear message.",
        "Logo clear-space (L-01) is documented but not pixel-enforced.",
        "PII masking covers emails, phones, and Aadhaar-style IDs; not a full redaction engine.",
        "SQLite resets on deploy unless a persistent disk is attached.",
        "Mobile layout is implemented but not device-tested.",
    ])

    # ---------------------------------------------------------------- 5 improvements
    section(pdf, 5, "The three improvements: committed vs delivered")
    subhead(pdf, "Improvement 1 - measured evaluation and false-positive reduction", AMBER)
    para(pdf, "Committed: build a 30-draft labelled set, publish precision/recall, cut false positives toward 10%, and collapse overlapping claim matches into one finding.", color=INK)
    para(pdf, "Delivered: we delivered the measurement rig and a concrete quality fix. Overlapping claim spans are deduplicated, so '5% cashback for life' now produces one C-01 finding. The harness runs 30 labelled cases and reports precision 0.900, recall 0.900, F1 0.900, and a false-positive rate of 0.100. Honest scope note: the 30 cases are synthetic-labelled, not a collected dataset of 30 real drafts, so these are engineering estimates, not real-world accuracy. The real-world labelled set is our first post-event milestone.", color=MUTED)
    subhead(pdf, "Improvement 2 - editable, versioned Brand Kit and Guideline Health", AMBER)
    para(pdf, "Committed: turn the read-only kit into an editor for rules, facts, banned terms, preferred vocabulary, and palette; version every change; show which rules are frequently overridden; let an admin promote an override into a kit revision.", color=INK)
    para(pdf, "Delivered: fully. Admins edit audience, colour tolerance, minimum contrast, rule labels/severity/rule text, approved facts, palette name/hex/role, banned terms, and preferred swaps in-app. Every save bumps the version (verified 4.3 to 4.4) and appends a 10-entry history snapshot. Insights already surfaces most-overridden rules with an ambiguous-guideline signal. Non-admins receive 403 on edit attempts.", color=MUTED)
    subhead(pdf, "Improvement 3 - failure recovery and reliability hardening", AMBER)
    para(pdf, "Committed: typed, actionable recovery states for empty kits, malformed/oversized uploads, documents with no selectable text, missing citation sources, and model-provider outages; retries/fallbacks; pytest coverage for engine, Citation Lock, role gates, and approval transitions.", color=INK)
    para(pdf, "Delivered: mostly, with scope honesty. We ship clear 4xx/413 responses for missing title/caption, unreadable or oversized files, plain-text uploads, empty scanned PDFs, duplicate actions, unauthorized access, and approved-draft edits. The model layer falls back to the deterministic local engine when a provider is unavailable. Stale-quote decisions record an explicit note. Double submit/approve/decide are blocked. Engine/decision unit tests plus the 47-check live E2E suite pass. What we did not build: a user-visible retry UI for third-party model outages, because the demo runs the local engine by default and we will not claim a recovery UI we did not ship.", color=MUTED)

    # ---------------------------------------------------------------- 6 extras
    section(pdf, 6, "Anything else improved after Round 2")
    bullets(pdf, [
        "Email + password demo login with credentials printed on the same login page (was one-click-only).",
        "Added a second demo creator (Rohan) and verified per-user workspace isolation end to end.",
        "PII masking at ingest for emails, phone numbers, and Aadhaar-style IDs.",
        "Image-only reviews enabled (previously required a caption).",
        "Clean 400 for missing title; consistent error messages across upload types.",
        "render.yaml blueprint and README with clone-and-run instructions.",
        "Built frontend dist committed so the repo runs without a build step.",
    ])

    # ---------------------------------------------------------------- 7 roadmap
    section(pdf, 7, "Product roadmap and future development plan")
    subhead(pdf, "0-3 months: make the numbers real")
    para(pdf, "Recruit 1-2 mid-size brand teams (fintech or D2C) as pilots. Collect 30 real drafts across captions, banners, and documents; label them with two independent raters; publish precision/recall and inter-rater agreement alongside the synthetic harness results. Success measure: a published, real 30-draft evaluation card.")
    subhead(pdf, "3-6 months: close the declared gaps")
    para(pdf, "Add OCR for scanned PDFs (Tesseract or a hosted vision model behind the existing Citation Lock). Implement pixel-level logo clear-space enforcement for L-01. Add exportable audit reports (PDF/CSV) so approval records can be handed to compliance.")
    subhead(pdf, "6-12 months: distribution and integrations")
    para(pdf, "Build Figma and Canva panels so designers are reviewed where they work; add a verified publishing hand-off that carries the approval record to social schedulers/CMS. Add sector compliance packs for regulated industries, starting with financial services.")
    subhead(pdf, "Who it is for, and what it would take")
    para(pdf, "Brand and content teams at mid-to-large organizations, and the agencies submitting drafts on their behalf. One engineer for OCR and clear-space work, one for integrations, plus pilot customers for labelled data. The roadmap is sequenced so a small team can ship the highest-visibility gaps first, and every item has a measurable exit condition.")

    # ---------------------------------------------------------------- 8 limitations
    section(pdf, 8, "Honest limitations and disclosures")
    bullets(pdf, [
        "The evaluation set is synthetic-labelled, not a real 30-draft dataset.",
        "No OCR: scanned/image-only PDFs are rejected with a clear message.",
        "Logo clear-space (L-01) is documented but not pixel-enforced.",
        "PII masking is not a full redaction engine.",
        "SQLite is ephemeral on Render unless a persistent disk is attached; the demo workspace reseeds on a fresh disk.",
        "Mobile layouts are implemented in CSS but not device-tested.",
    ])

    # ---------------------------------------------------------------- 9 team
    section(pdf, 9, "Team and declarations")
    kv(pdf, [
        ("Team", "A2Z Creators - Venkata Narayana G V (Team Leader, Developer), Mahesh Babu Ch (Research & Analysis)."),
        ("Build window", "All product code was written during the Tech Circuit 2026 event window."),
        ("AI disclosure", "This document and the code were prepared with AI assistance. The product uses a deterministic local review engine by default; optional external model adapters are disclosed in the UI when enabled."),
        ("Privacy", "PII is masked on ingest; demo facts are synthetic; no customer content is used for training."),
    ])
    para(pdf, "PrismCheck AI - Round 3 Submission - Team A2Z Creators. Thank you for reviewing.", color=MUTED)

    out = HERE / "PrismCheck_Round3_Submission.pdf"
    pdf.output(str(out))
    print("WROTE", out)
    print("PAGES", pdf.page_no())


if __name__ == "__main__":
    build()
