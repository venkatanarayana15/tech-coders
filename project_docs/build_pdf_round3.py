#!/usr/bin/env python3
"""Build PrismCheck AI — Round 3 Submission PDF.

Run from the repository root:
    python project_docs/build_pdf_round3.py

Output:
    project_docs/PrismCheck_Round3_Submission.pdf
"""

from __future__ import annotations

import os
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


class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("UB", "", 7.5)
        self.set_text_color(*MUTED)
        self.cell(0, 6, "PrismCheck AI · Round 3 Submission · Team A2Z Creators", align="R")
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


def bullets(pdf, items, size=8.6, lh=4.6):
    pdf.set_font("U", "", size)
    pdf.set_text_color(*INK)
    for item in items:
        pdf.multi_cell(0, lh, f"• {item}")
        pdf.ln(1)


def kv(pdf, rows, label_w=34, size=8.8, lh=4.8):
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

    # Cover
    pdf.add_page()
    pdf.ln(34)
    pdf.set_font("UB", "", 26)
    pdf.set_text_color(*INK)
    pdf.cell(0, 10, "PrismCheck AI")
    pdf.ln(2)
    pdf.set_font("U", "", 14)
    pdf.set_text_color(*TEAL)
    pdf.cell(0, 8, "Round 3 Submission — the finished product")
    pdf.ln(12)
    pdf.set_font("U", "", 10.5)
    pdf.set_text_color(*MUTED)
    pdf.cell(0, 6, "Team A2Z Creators · Tech Circuit 2026")
    pdf.ln(5)
    pdf.cell(0, 6, f"Live: {LIVE_URL}")
    pdf.ln(5)
    pdf.cell(0, 6, f"Source: {REPO_URL}")
    pdf.ln(16)
    pdf.set_font("U", "", 9.5)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 6, "A pre-publication brand-governance review workspace: it reviews captions, artwork, PDFs, and DOCX files against a structured brand kit, cites every finding to the exact rule or approved fact, and keeps a human in the approval loop.")

    # 1 Product and features
    section(pdf, 1, "What we built")
    para(pdf, "PrismCheck is a complete, deployed web app. A judge can open the live link, pick a role, and run the full journey: create a review, see cited findings, apply fixes, submit, approve, and read insights.")
    bullets(pdf, [
        "Credential-based demo login with three roles (creator, reviewer, admin); credentials are printed on the sign-in page.",
        "Brand kit reference: 7 rules, 5 approved facts, 5 palette colours, 10 language entries, each with a stable ID.",
        "Admin brand-kit editor with automatic version bumps and a 10-entry history trail.",
        "Review sources: caption text, artwork upload (PNG/JPG/WebP), PDF upload, DOCX upload.",
        "PII masking on ingest for email addresses, phone numbers, and Aadhaar-style IDs.",
        "Deterministic checks: claims vs fact bank (C-01), banned guarantees (T-14), urgent/absolute tone (T-02), preferred vocabulary (T-03), CIELAB palette distance (V-05), WCAG contrast and alt text (A-03).",
        "Citation Lock: every displayed finding resolves to a real kit item; uncited findings are dropped and counted.",
        "One-click fixes grounded in approved facts, or keep-as-is with a required note.",
        "Full workflow: draft to submitted to approved / changes requested, with backend guards and a revision timeline.",
        "Approved drafts are locked. Re-run review against the current kit.",
        "Insights: citation coverage, most-flagged rules, most-overridden rules, ambiguous-guideline signal, decision rate, average review time.",
    ])

    # 2 Demo credentials
    section(pdf, 2, "Demo access")
    kv(pdf, [
        ("Creator", "ananya@northwind.example · password demo123"),
        ("Reviewer", "kabir@northwind.example · password demo123"),
        ("Admin", "meera@northwind.example · password demo123"),
    ])

    # 3 Architecture
    section(pdf, 3, "Technical architecture and implementation")
    kv(pdf, [
        ("Frontend", "React 18 + Vite 5, handcrafted CSS; the production build is served by FastAPI from the same origin."),
        ("Backend", "FastAPI 0.141 on Python 3.14+; SQLModel + SQLite; signed HttpOnly cookie sessions."),
        ("Images", "Pillow 12 + numpy 2.5: CIELAB ΔE palette checks and WCAG contrast."),
        ("Documents", "pypdf 6 for PDFs; zip/XML extraction for DOCX."),
        ("Review engine", "Deterministic in-process engine by default; optional Gemini 2.5 Flash / Ollama adapters, with Citation Lock enforced on every finding."),
        ("Deployment", "Render Python web service; health check at /api/health."),
    ])
    para(pdf, "Key API surface: /api/session, /api/users, /api/bootstrap, /api/kit (GET/PATCH), /api/drafts, /api/drafts/{id}/decisions, /submit, /approve, /request-changes, /rerun, /api/insights, /api/files/{name}.", color=MUTED)

    # 4 Three improvements
    section(pdf, 4, "The three improvements we named and delivered")
    para(pdf, "Round 2 committed to three improvements. All three are implemented and observable in the live app.", color=GREEN)

    bullets(pdf, [
        "1. Measured evaluation and false-positive reduction — a repeatable synthetic-labelled harness (backend/evaluate.py, 30 cases) computes precision, recall, F1, and false-positive rate; the engine also deduplicates overlapping claim spans so one clause cannot produce two C-01 findings.",
        "2. Editable, versioned Brand Kit + Guideline Health — admins edit rules, facts, palette, banned/preferred language, and tolerances in-app; each save bumps the version and appends a history snapshot, closing the read-only gap.",
        "3. Failure recovery and reliability — clear 4xx feedback for missing title/caption, unreadable or oversized uploads, empty documents, duplicate decisions, unauthorized actions, and locked approved drafts; signed sessions survive refresh; unit tests cover the engine and decision application.",
    ])

    # 5 Testing
    section(pdf, 5, "Testing performed")
    bullets(pdf, [
        "Engine unit tests (pytest): 7 tests pass — claim overlap dedupe, approved-fact silence, banned promises, urgent tone, PII masking, and stale-quote decision handling.",
        "Evaluation harness (backend/evaluate.py): 30 synthetic-labelled cases — precision 0.900, recall 0.900, F1 0.900, false-positive rate 0.100.",
        "API smoke tests: password login for all three roles; kit patch version bump; PII-masked caption through the full review path.",
        "Browser end-to-end on the deployed link: sign-in page shows credentials on the same page; admin signs in with email + password; edits a rule and saves; version advances 4.3 to 4.4.",
        "Failure-path checks: zero-finding clean drafts pass; open findings block submit/approve; approved drafts are locked; reviewer cannot create drafts; creator cannot approve; duplicate actions return clear 4xx errors.",
        "Deployed health check: https://tech-coders.onrender.com/api/health returns 200 with engine status ready.",
    ])

    # 6 Reliability
    section(pdf, 6, "Reliability notes")
    bullets(pdf, [
        "All state is server-side; refreshing the page keeps the session and the draft.",
        "The same action twice returns a clear 400 rather than a crash.",
        "Empty brand-kit data falls back to the seeded kit.",
        "Scanned/image-only PDFs are rejected with an explicit “no selectable text” message.",
        "SQLite is ephemeral on Render unless a persistent disk is attached; the app reseeds the demo workspace on a fresh disk.",
    ])

    # 7 Known limitations
    section(pdf, 7, "Known limitations")
    bullets(pdf, [
        "Logo clear-space (L-01) is documented in the kit but not yet enforced by a pixel-level check.",
        "No OCR: scanned PDFs are rejected rather than silently missed.",
        "PII masking covers emails, phone numbers, and Aadhaar-style IDs; it is not a full redaction product.",
        "The evaluation harness is synthetic-labelled; the real 30-draft set is the first post-event milestone.",
        "Mobile layouts are implemented in CSS but were not browser-tested on physical devices.",
    ])

    # 8 Roadmap
    section(pdf, 8, "Product roadmap")
    kv(pdf, [
        ("Next 0–3 months", "Recruit pilot brand teams; collect 30 real drafts; publish measured precision/recall and inter-rater agreement."),
        ("3–6 months", "OCR for scanned documents; pixel-level logo clear-space; exportable audit reports."),
        ("6–12 months", "Figma/Canva integrations, video/audio review, verified publishing hand-off, sector compliance packs."),
    ])

    # 9 Team and declarations
    section(pdf, 9, "Team and declarations")
    kv(pdf, [
        ("Team", "A2Z Creators — Venkata Narayana G V (Team Leader, Developer), Mahesh Babu Ch (Research & Analysis)."),
        ("Build window", "All product code was written during the Tech Circuit 2026 event window."),
        ("AI disclosure", "This document and the code were prepared with AI assistance. The product uses a deterministic local review engine by default; optional external model adapters are disclosed in the UI when enabled."),
        ("Privacy", "PII is masked on ingest; demo facts are synthetic; no customer content is used for training."),
    ])

    out = HERE / "PrismCheck_Round3_Submission.pdf"
    pdf.output(str(out))
    print("WROTE", out)
    print("PAGES", pdf.page_no())


if __name__ == "__main__":
    build()
