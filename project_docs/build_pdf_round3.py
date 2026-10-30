#!/usr/bin/env python3
"""
Build PrismCheck AI — Round 3 Submission PDF.

Takes the Round 3 content from the paste and emits a 10-page product PDF.
Figures (architecture diagram, metrics legend, roadmap bars) are drawn
by draw_round3.py, which matches the existing figure style used by the
Round 1 and Round 2 submission PDFs.

Usage:
    python build_pdf_round3.py
Output:
    project_docs/PrismCheck_Round3_Submission.pdf
"""
from __future__ import annotations

import os
from pathlib import Path

from fpdf import FPDF

HERE = Path(__file__).resolve().parent
os.chdir(HERE)

try:
    from draw_round3 import (
        draw_image_metrics,
        draw_roadmap_footer,
        draw_arch_overview,
    )
except Exception as exc:  # noqa: BLE001 - graceful degradation to text-only
    draw_image_metrics = draw_roadmap_footer = draw_arch_overview = None
    _DRAW_WARN = str(exc)
else:
    _DRAW_WARN = None


# ---------------------------------------------------------------- fonts / palette
FONT_DIR = HERE / "fonts"
INK      = (62, 74, 80)
MUTED    = (112, 126, 134)
TEAL     = (46, 138, 153)
TEALD    = (34, 112, 126)
TEALF    = (233, 246, 248)
AMBER    = (206, 145, 72)
AMBERF   = (253, 244, 230)
GREEN    = (74, 150, 122)
GREENF   = (232, 246, 240)
ROSE     = (188, 104, 120)
ROSEF    = (252, 238, 241)
LINE     = (222, 232, 236)
WHITE    = (255, 255, 255)
VOID     = (238, 243, 245)
COVER    = (246, 251, 252)
CREAM    = (253, 252, 249)
GREY     = (130, 138, 144)
ROAD_T   = (46, 138, 153)
ROAD_M   = (206, 145, 72)
ROAD_X   = (188, 104, 120)
RED      = (188, 104, 120)
REDF     = (252, 238, 241)

BLOCK = r"""
.----------------.  .----------------.  .----------------.  .----------------.
|  Sign in (demo)|->|  New review    |  | Kit & checks   |  ->|  Decision     |
|  email+word|  |  caption/      |  | every finding  |     |  accept/      |
|  credentials on|  |  image/PDF/    |  | resolves to a  |     |  keep with    |
|  the login page|  |  DOCX           |  | real kit item  |     |  reason       |
'----------------'  '----------------'  '----------------'  '----------------'
        |                  |                 |                  |
        v                  v                 v                  v
  .----------------.  .----------------.  .----------------.  .----------------.
  | Dashboard      |  | Artwork/PDF/   |  | Approve or     |  | Revision     |
  | live counts,   |  | DOCX extraction|  | request changes|  | history +    |
  | search, queues |  | + checks run   |  | with notes     |  | audit trail  |
  '----------------'  '----------------'  '----------------'  '----------------'
"""
# Box width/height
_BOX_W = 29.6
_BOX_H = 10.2


M = 16.0
W = 210.0
CW = W - 2 * M
H = 297.0
BOT = H - 20


def pill(pdf, x, y, text, fill, accent, size=7.2, h=5.0):
    est = pdf.get_string_width(text) + 5.0
    pdf.set_font("U", "", size)
    if x + est > W - M:
        return M
    return x + est


def card(pdf, x, y, w, h, fill, border):
    pdf.set_fill_color(*fill)
    pdf.rect(x, y, w, h, style="F")
    if border is not None:
        pdf.set_draw_color(*border)
        pdf.set_line_width(0.4)
        pdf.rect(x, y, w, h, style="D")
        pdf.set_line_width(0.2)


def stat_row(pdf, stats, fill=TEALF, accent=TEALD, big_size=14.0):
    n = len(stats)
    colw = CW / n
    y = pdf.get_y()
    for (num, label, desc) in stats:    idx = stats.index((num, label, desc))
    pdf.set_fill_color(*fill)
    pdf.rect(pdf.l_margin + idx * colw, y, colw - 4, 30, style="F")
    pdf.set_xy(pdf.l_margin + idx * colw + 2, y + 2)
    pdf.set_font("U", "B", big_size)
    pdf.set_text_color(*accent)
    pdf.cell(colw - 4, 6.5, num)
    pdf.set_font("U", "", 7.8)
    pdf.set_text_color(*accent)
    pdf.set_xy(pdf.l_margin + idx * colw + 2, y + 10)
    pdf.multi_cell(colw - 4, 3.3, label)
    pdf.set_font("U", "", 7.2)
    pdf.set_text_color(*MUTED)
    pdf.set_xy(pdf.l_margin + idx * colw + 2, y + 22)
    pdf.multi_cell(colw - 4, 3.0, desc)
    pdf.set_y(y + 34)


class Doc(FPDF):
    """Page template shared by the Round 1 and Round 2 submissions."""

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-12)
        self.set_x(16)
        self.set_font("U", "", 7)
        self.set_text_color(*MUTED)
        self.cell(0, 5, "PrismCheck AI - Round 3 submission - Team A2Z Creators", align="L")
        self.set_x(self.w - 16)
        self.cell(0, 5, str(self.page_no()) + " / " + str(self.pages_count), align="R")

    def __init__(self) -> None:
        super().__init__()
        self.set_auto_page_break(True, 16)
        self.set_margin(16)

        regular = FONT_DIR / "Ubuntu-Regular.ttf"
        bold    = FONT_DIR / "Ubuntu-Bold.ttf"
        italic  = FONT_DIR / "Ubuntu-Italic.ttf"
        boldit  = FONT_DIR / "Ubuntu-BoldItalic.ttf"
        # Monospace is optional; the template degrades to a serif-less
        # typewriter feel using the regular weight when no mono font ships.
        mono_dir = FONT_DIR / "monospace"
        mono     = mono_dir / "UbuntuMono-Regular.ttf"
        monob    = mono_dir / "UbuntuMono-Bold.ttf"
        if mono.exists() and monob.exists():
            self.add_font("UM", "", str(mono))
            self.add_font("UM", "B", str(monob))
        else:
            # Best-effort: alias mono to the regular family so code blocks
            # still render, even without a dedicated mono TTF.
            self.add_font("UM", "", str(regular))
            self.add_font("UM", "B", str(bold))

        self.add_font("U", "", str(regular))
        self.add_font("U", "B", str(bold))
        self.add_font("U", "I", str(italic))
        self.add_font("U", "BI", str(boldit))

    def cover_title(self) -> None:
        self.set_font("U", "B", 27)
        self.cell(0, 7.2, "PrismCheck AI")
        self.ln(3.4)
        self.set_font("U", "I", 13.5)
        self.cell(0, 4.9, "Round 3 submission")
        self.ln(6.6)

    def section_head(self, text: str) -> None:
        self.set_font("U", "B", 14.6)
        self.set_text_color(*INK)
        self.cell(0, 5.6, text)
        self.ln(2.0)


def new_doc() -> Doc:
    return Doc()


# ---------------------------------------------------------------- content
def cover(pdf: Doc) -> None:
    pdf.add_page()
    pdf.set_fill_color(*COVER)
    pdf.rect(0, 0, W, 122, style="F")
    pdf.set_fill_color(*TEAL)
    pdf.rect(0, 0, W, 4.2, style="F")
    pdf.set_fill_color(*AMBER)
    pdf.rect(W * 0.34, 4.2, W * 0.3, 1.4, style="F")
    pdf.set_fill_color(*GREEN)
    pdf.rect(W * 0.64, 4.2, W * 0.3, 1.4, style="F")

    pdf.set_font("U", "B", 8.2)
    pdf.set_text_color(*TEALD)
    pdf.set_xy(M, 18)
    pdf.cell(0, 5, "TECHCIRCUIT 2026   \u00b7   ROUND 3 SUBMISSION   \u00b7   THE FINISH")

    pdf.set_font("U", "B", 34)
    pdf.set_text_color(*INK)
    pdf.set_xy(M, 26)
    pdf.cell(0, 14, "PrismCheck AI")

    pdf.set_font("U", "", 14.2)
    pdf.set_text_color(*TEALD)
    pdf.set_xy(M, 42)
    pdf.cell(0, 8, "Intelligent pre-publication brand governance")

    pdf.set_font("U", "B", 10.6)
    pdf.set_text_color(*MUTED)
    pdf.set_xy(M, 53)
    pdf.cell(0, 6, "\u201cFinish the build. Publish the numbers.\u201d")

    x, y = M, 66
    for txt, f, a in [
        ("Three improvements delivered", GREENF, GREEN),
        ("47/47 live checks passing", AMBERF, AMBER),
        ("0.900 precision / 0.100 FP", ROSEF, ROSE),
    ]:
        pdf.set_font("U", "B", 7.9)
        est = pdf.get_string_width(txt) + 5.0
        if x + est > W - M:
            x = M
            y += 7.0
        x = pill(pdf, x, y, txt, f, a, 7.9) + 3.6

    pdf.set_xy(M, 82)
    pdf.set_font("U", "", 9.3)
    pdf.set_text_color(*INK)
    pdf.multi_cell(CW * 0.72, 4.9,
        "A review gate between \u201csomeone made this\u201d and \u201cthis goes live\u201d. "
        "PrismCheck checks text, images and documents against one approved Brand Kit, "
        "explains every flag with a citation, and suggests fixes that keep the creator's purpose.")

    # team block
    y0 = 118
    card(pdf, M, y0, CW, 36, WHITE, LINE)
    pdf.set_font("U", "B", 8.0)
    pdf.set_text_color(*TEALD)
    pdf.set_xy(M + 5, y0 + 3.6)
    pdf.cell(0, 4, "TEAM A2Z CREATORS  \u00b7  TWO MEMBERS")
    pdf.set_font("U", "", 8.8)
    pdf.set_text_color(*INK)
    pdf.set_xy(M + 5, y0 + 10.0)
    pdf.multi_cell(CW - 10, 4.9,
        "Venkata Narayana G V  \u2014  Team Leader, Developer  \u2014  venkatnarayana727@gmail.com")
    pdf.set_x(M + 5)
    pdf.multi_cell(CW - 10, 4.9,
        "Mahesh Babu Ch  \u2014  Research and Analysis  \u2014  maheshmamtha242@gmail.com")
    pdf.set_x(M + 5)
    pdf.set_font("U", "", 8.2)
    pdf.set_text_color(*TEALD)
    pdf.multi_cell(CW - 10, 4.6,
        "Live build:  https://tech-coders.onrender.com/")
    pdf.set_x(M + 5)
    pdf.multi_cell(CW - 10, 4.6,
        "Repository:  https://github.com/venkatanarayana15/tech-coders")
    pdf.set_x(M + 5)
    pdf.set_font("U", "I", 8.0)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(CW - 10, 4.5, "Round 3  \u00b7  submitted 30 Oct 2026  \u00b7  the finish of the Round 1 plan to a shipped product.")

    # at-a-glance strip
    pdf.set_y(169)
    stat_row(pdf, [
        ("3", "content formats\nreviewed", "text \u00b7 image \u00b7 document"),
        ("47/47", "live\nintegration checks", "auth \u00b7 review \u00b7 approval \u00b7 kit"),
        ("0.900", "measured\nevaluation F1", "30 labelled cases, synthetic"),
    ])

    pdf.set_y(209)
    pdf.set_font("U", "I", 8.2)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(CW, 4.0,
        "Round 3 reuses the Round 1 template, palette and figure style; only the edition copy, the named Round 2 "
        "improvements, the live numbers and the roadmap changed.")


def sec1(pdf: Doc) -> None:
    pdf.add_page()
    pdf.section_head("1. Complete list of features")
    pdf.set_font("U", "", 8.9)
    pdf.set_text_color(*MUTED)

    # Demo access quick reference card
    y0 = pdf.get_y()
    demo_rows = [
        ("Creator", "ananya@northwind.example"),
        ("Creator", "rohan@northwind.example"),
        ("Reviewer", "kabir@northwind.example"),
        ("Admin", "meera@northwind.example"),
    ]
    demo_h = 7.0 + len(demo_rows) * 5.2 + 4.0
    card(pdf, M, y0, CW, demo_h, TEALF, LINE)
    pdf.set_xy(M + 4, y0 + 2.2)
    pdf.set_font("U", "B", 8.8)
    pdf.set_text_color(*TEALD)
    pdf.cell(0, 4.6, "Demo access - every account uses the password demo123")
    for role, email in demo_rows:
        pdf.set_x(M + 4)
        pdf.set_font("U", "B", 8.3)
        pdf.set_text_color(*INK)
        pdf.cell(27, 5.2, role)
        pdf.set_font("U", "", 8.3)
        pdf.set_text_color(*MUTED)
        pdf.set_x(M + 32)
        pdf.multi_cell(CW - 36, 5.2, email)
    pdf.set_y(y0 + demo_h + 2.0)
    pdf.set_font("U", "I", 8.0)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        CW, 3.9,
        "Judge fast path: sign in as meera@northwind.example (admin) to open the Brand Kit editor, "
        "ananya@northwind.example to create a review, and kabir@northwind.example to approve.",
    )
    pdf.ln(1.4)

    blocks: list[tuple[str, list[str], tuple[int, int, int]] | None] = [
        (
            "Sign-in and sessions",
            [
                "Role-based demo sign-in with email and password; all demo credentials are printed on the login page.",
                "Signed HttpOnly cookie sessions that survive refresh.",
                "Server-side role enforcement: creator, reviewer, admin.",
            ],
            TEAL,
        ),
        (
            "Creator dashboard",
            [
                "Creator dashboard with live counts, search, status filters, and priority queues.",
                "Seeded demo workspace (Ananya's 6 drafts) plus a clean second creator workspace (Rohan).",
            ],
            AMBER,
        ),
        (
            "New review intake",
            [
                "New review from a caption, artwork upload, PDF upload, or DOCX upload.",
                "Artwork validation for PNG, JPG, and WebP.",
                "PDF text extraction and review.",
                "DOCX text extraction and review.",
                "PII masking on ingest for emails, phone numbers, and Aadhaar-style IDs.",
            ],
            GREEN,
        ),
        (
            "The checks",
            [
                "Claim review against the approved fact bank (C-01).",
                "Banned absolute-guarantee review (T-14).",
                "Urgency and absolute-language review (T-02).",
                "Preferred-vocabulary review (T-03).",
                "CIELAB palette-distance review (V-05).",
                "WCAG contrast review and alt-text requirement (A-03).",
            ],
            RED,
        ),
        (
            "Citation Lock",
            [
                "Citation Lock: every displayed finding resolves to a real kit item; uncited findings are dropped and counted.",
                "One-click fixes grounded in approved facts, with capitalization preserved.",
                "Keep-as-is decision with a required reason.",
                "Draft lifecycle: draft -> submitted -> approved / changes requested, with backend guards.",
                "Submit guard blocks drafts with unresolved findings.",
                "Reviewer approve and request-changes actions with notes.",
                "Approved drafts are locked against further edits.",
                "Re-run review against the current kit.",
                "Revision timeline and audit trail on every draft.",
            ],
            TEAL,
        ),
        (
            "Brand Kit and insights",
            [
                "Brand Kit reference: 7 rules, 5 approved facts, 5 palette colors, 10 language entries, each addressable by ID.",
                "Admin Brand Kit editor with automatic version bump and a history trail.",
                "Insights page: citation coverage, most-flagged rules, most-overridden rules, ambiguous-guideline signal, decision rate, and average review time.",
                "Clean compliant drafts  with zero findings.",
                "Health endpoint and SPA served by the same FastAPI process.",
            ],
            AMBER,
        ),
    ]

    for name, lines, color in blocks:
        pdf.ln(1.1 if pdf.get_y() < 32 else 1.6)
        # color chip
        pdf.set_fill_color(*color)
        pdf.set_draw_color(*color)
        x0 = pdf.get_x()
        y0 = pdf.get_y()
        r = min(2.2, min(10, 9))  # safe chip size
        pdf.rect(x0 + 1.0, y0 + 0.4, r, r, style="DF")
        pdf.set_xy(x0 + 1.0 + r + 1.6, y0)
        pdf.set_font("U", "B", 9.4)
        pdf.set_text_color(*MUTED)
        pdf.cell(0, 4.6, name)
        pdf.set_xy(x0 + 1.0, y0 + r + 2.0)
        pdf.set_x(pdf.l_margin + 2.6)
        pdf.set_font("U", "", 8.7)
        pdf.set_text_color(*MUTED)
        for i, line in enumerate(lines):
            nudge = 0.2 if i == 0 else 0.0
            pdf.set_y(pdf.get_y() + nudge)  # type: ignore[union-attr]
            pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin - 2.6, 4.2, "- " + line)

        pdf.set_y(pdf.get_y() + 0.4)

    pdf.ln(1.6)
    pdf.set_font("U", "I", 8.2)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0, 4.0,
        "Numbered IDs above (C-01, T-14, T-02, T-03, V-05, A-03) are the same ids used in the kit and in the "
        "findings returned by the API, so a judge can trace any flag back to a line in the Brand Kit.",
    )


def sec2(pdf: Doc) -> None:
    pdf.add_page()
    pdf.section_head("2. Technical architecture and implementation summary")
    pdf.set_font("U", "", 8.9)
    pdf.set_text_color(*MUTED)

    def sub(label: str, lines: list[str]) -> None:
        pdf.ln(1.2)
        pdf.set_font("U", "B", 9.3)
        pdf.set_text_color(*MUTED)
        pdf.cell(0, 4.6, label)
        pdf.ln(1.2)
        pdf.set_font("U", "", 8.7)
        pdf.set_text_color(*MUTED)
        pdf.set_x(pdf.l_margin + 2.4)
        for line in lines:
            pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin - 2.4, 4.2, line)
            pdf.set_x(pdf.l_margin + 2.4)
        pdf.set_x(pdf.l_margin)

    sub("Components.", [
        "The product is a single-origin web app. The frontend is React 18 + Vite 5 with handcrafted CSS; the "
        "production build lives in frontend/dist and is served by FastAPI. The backend is FastAPI 0.141 on "
        "Python 3.14+ with SQLModel + SQLite.",
    ])

    pdf.ln(0.6)
    pdf.set_font("U", "I", 7.6)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0, 3.6,
        "Read as text: this round is measured against the three improvements committed at Round 2, plus finishing "
        "the features left open. Nothing new and nothing changed in direction.",
    )

    sub("How they talk.", [
        "The browser talks only to the FastAPI JSON/multipart API. Sessions are signed HttpOnly cookies "
        "(itsdangerous); demo passwords are PBKDF2-hashed. Every route re-checks the user's role on the server.",
    ])

    sub("Data flow.", [
        "A draft is created from caption/alt text/uploads -> text and images are PII-masked and stored -> "
        "the deterministic engine runs checks -> every finding has a source_id -> the Citation Lock resolves it "
        "against the kit; a finding with no valid source is dropped and counted -> findings and a revision record "
        "are persisted -> payloads are returned to the UI.",
    ])

    sub("Models and APIs.", [
        "Core tables: User, Kit (JSON data), Draft, Finding (JSON fixes/measured values), Revision.",
        "Key endpoints: /api/session, /api/users, /api/bootstrap, /api/kit (GET/PATCH), /api/drafts, "
        "/api/drafts/{id}/decisions, /submit, /approve, /request-changes, /rerun, /api/insights, /api/files/{name}.",
    ])

    sub("Infrastructure.", [
        "Render web service via render.yaml (Python runtime, pip install -r backend/requirements.txt, "
        "uvicorn --app-dir backend app.main:app). Uploads are stored on the local filesystem; SQLite is on "
        "the service disk (ephemeral unless a persistent disk is attached).",
    ])

    sub("Hardest problem solved.", [
        "Guaranteeing that every displayed finding is defensible. We built the Citation Lock as a single "
        "server-side choke point, so an uncited or unmatched finding can never reach the screen - this is what "
        "makes the `reliable, explainable results` claim enforceable rather than aspirational. A close second was "
        "keeping fixes correct when edits shift text; decisions now report when the exact quote is no longer present "
        "instead of silently doing nothing.",
    ])

    if _DRAW_WARN:
        pdf.ln(2)
        pdf.set_font("U", "I", 7.6)
        pdf.set_text_color(*MUTED)
        pdf.multi_cell(0, 3.6, "Diagram note: figure layer unavailable (" + _DRAW_WARN + ").")
    elif draw_arch_overview is not None:
        pdf.ln(2.4)
        y_before = pdf.get_y()
        draw_arch_overview(pdf, pdf.l_margin, pdf.w - pdf.l_margin - pdf.r_margin, pdf)
        pdf.set_y(max(y_before + 4.0, pdf.get_y()))


def sec3(pdf: Doc) -> None:
    pdf.add_page()
    pdf.section_head("3. Testing details")
    pdf.set_font("U", "", 8.9)
    pdf.set_text_color(*MUTED)

    def sub(label: str, lines: list[str], lead: bool = True) -> None:
        pdf.ln(1.3 if lead else 1.0)
        pdf.set_font("U", "B", 9.3)
        pdf.set_text_color(*MUTED)
        pdf.cell(0, 4.7, label)
        pdf.ln(1.2)
        pdf.set_font("U", "", 8.7)
        pdf.set_text_color(*MUTED)
        pdf.set_x(pdf.l_margin + 2.4)
        for line in lines:
            pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin - 2.4, 4.2, line)
            pdf.set_x(pdf.l_margin + 2.4)
        pdf.set_x(pdf.l_margin)

    sub("Unit tests (pytest).", [
        "7 tests cover: overlapping-claim deduplication, approved-fact silence, banned-promise hard stop, "
        "urgent-tone soft note, PII masking, and stale-quote replacement behavior.",
    ])

    sub("Evaluation harness.", [
        "backend/evaluate.py runs 30 synthetic-labelled cases: precision 0.900, recall 0.900, F1 0.900, "
        "false-positive rate 0.100.",
    ])

    sub("Live integration / E2E.", [
        "backend/tests/e2e_live.py runs 47 checks against a running server: auth, per-user independence, "
        "full caption journey, request-changes loop, image-only and off-brand uploads, real PDF/DOCX extraction, "
        "bad inputs (corrupt image, .txt, oversized), submit/approve guards, role 403s, kit editing, insights, "
        "and health/SPA. Result: 47/47 passed on a fresh database.",
    ])

    sub("Manual / browser testing.", [
        "Verified on the deployed link: credentials visible on the login page; admin signs in with email + "
        "password; edit-save bumps kit version 4.3 -> 4.4; new frontend bundle serves after deploy.",
    ])

    sub("Clean-clone verification.", [
        "Cloned the repo fresh, ran pip install -r backend/requirements.txt, started uvicorn, and confirmed "
        "/ serves the SPA and /api/health returns 200. `npm ci && npm run build` also succeeds.",
    ])

    sub("What we found and fixed.", [
        "- Image-only uploads were rejected -> fixed in backend and frontend.",
        "- Missing title returned 422 -> now a clean 400.",
        "- Overlapping claim text produced duplicate C-01 findings -> deduplicated.",
        "- A stale quote could silently no-op a fix -> decisions now record a clear note when no text changed.",
        "- Double submit/approve/decide could slip through -> now blocked with 400.",
    ])

    sub("Still known to be imperfect.", [
        "- Evaluation labels are synthetic, not a real 30-draft dataset.",
        "- No OCR: scanned/image-only PDFs are rejected with a clear message.",
        "- Logo clear-space (L-01) is documented but not pixel-enforced.",
        "- PII masking covers emails, phones, and Aadhaar-style IDs - not a full redaction engine.",
        "- SQLite resets on deploy unless a persistent disk is attached.",
        "- Mobile layout is implemented but not device-tested.",
    ])


def _metric_bar(pdf: Doc, label: str, value: float, maxv: float = 1.0, color: tuple[int, int, int] = TEAL) -> None:
    """A single horizontal metric with a readable percentage bar."""
    pdf.set_font("U", "B", 9.0)
    pdf.set_text_color(*MUTED)
    pdf.cell(43, 4.8, label)
    pct = max(0.0, min(1.0, value / maxv))
    bar_w = pdf.w - pdf.l_margin - pdf.r_margin - 43 - 22
    y0 = pdf.get_y() + 0.6
    pdf.set_draw_color(*LINE)
    pdf.set_fill_color(*VOID)
    pdf.rect(pdf.l_margin + 43 + 1.0, y0, bar_w, 4.6, style="DF")
    if pct > 0.001:
        pdf.set_fill_color(*color)
        pdf.set_draw_color(*color)
        pdf.rect(pdf.l_margin + 43 + 1.0, y0, max(0.4, bar_w * pct), 4.6, style="F")
    pdf.set_xy(pdf.l_margin + 43 + 1.0 + bar_w + 1.2, y0 - 0.2)
    pdf.set_font("U", "B", 8.4)
    pdf.set_text_color(*MUTED)
    pdf.cell(20, 4.8, f"{pect(pct)}")


def pect(pct: float) -> str:
    return f"{pct:.1%}"


def sec4(pdf: Doc) -> None:
    pdf.add_page()
    pdf.section_head("4. Improvement 1 - measured evaluation and false-positive reduction")
    pdf.set_font("U", "", 8.9)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0, 4.3,
        "Committed: build a 30-draft labelled set, publish precision/recall, cut false positives toward 10%, "
        "and collapse overlapping claim matches into one finding.",
    )
    pdf.ln(0.8)
    pdf.multi_cell(
        0, 4.3,
        "Delivered, and the honest part: we delivered the measurement rig and one concrete quality fix - overlapping "
        "claim spans are deduplicated, which is why `5% cashback for life` now produces one C-01 finding instead of two. "
        "The harness (backend/evaluate.py) runs 30 labelled cases and reports precision 0.900, recall 0.900, F1 0.900, "
        "and a false-positive rate of 0.100. However, the 30 cases are synthetic-labelled, not a real collected dataset "
        "of 30 real drafts. We did not run real creator interviews or collect real drafts within the window, so the "
        "numbers are engineering estimates, not real-world accuracy. We say this plainly: the improvement delivered is a "
        "repeatable evaluation core plus real deduplication, and the real-world labelled set is the first post-event milestone.",
    )

    if draw_image_metrics is not None:
        pdf.ln(2.4)
        y0 = pdf.get_y()
        draw_image_metrics(pdf, pdf.l_margin, pdf.w - pdf.l_margin - pdf.r_margin, pdf)
        pdf.set_y(max(y0 + 4.0, pdf.get_y()))
    else:
        pdf.ln(1.6)
        pdf.set_font("U", "I", 7.6)
        pdf.set_text_color(*MUTED)
        pdf.multi_cell(
            0, 3.6,
            "Metrics diagram note: figure layer unavailable; the numbers above are the source of truth.",
        )


def sec5(pdf: Doc) -> None:
    pdf.add_page()
    pdf.section_head("5. Improvement 2 - editable, versioned Brand Kit and Guideline Health loop")
    pdf.set_font("U", "", 8.9)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0, 4.3,
        "Committed: turn the read-only kit into an editor for rules, facts, banned terms, preferred vocabulary, "
        "and palette; version every change; show which rules are frequently overridden; let an admin promote an "
        "override into a kit revision.",
    )
    pdf.ln(0.8)
    pdf.multi_cell(
        0, 4.3,
        "Delivered: fully. The admin role now has an in-app Brand Kit editor covering audience, color tolerance, "
        "minimum contrast, rule labels/severity/rule text, approved facts, palette name/hex/role, banned terms, "
        "and preferred swaps. Every save bumps the version (verified 4.3 -> 4.4) and appends a 10-entry history "
        "snapshot. The Insights page already surfaces most-overridden rules with an ambiguous-guideline signal, "
        "closing the loop from review evidence to kit maintenance. Non-admins receive 403 on edit attempts.",
    )


def sec6(pdf: Doc) -> None:
    pdf.add_page()
    pdf.section_head("6. Improvement 3 - failure recovery and reliability hardening")
    pdf.set_font("U", "", 8.9)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        0, 4.3,
        "Committed: typed, actionable recovery states for empty kits, malformed/oversized uploads, documents with "
        "no selectable text, missing citation sources, and model-provider outages; retries/fallbacks; pytest coverage "
        "for engine, Citation Lock, role gates, and approval transitions.",
    )
    pdf.ln(0.8)
    pdf.multi_cell(
        0, 4.3,
        "Delivered: mostly, with scope honesty. What is real: clear 4xx/413 responses for missing title/caption, "
        "unreadable or oversized files, plain-text uploads, empty scanned PDFs, duplicate actions, unauthorized access, "
        "and approved-draft edits; the model layer falls back to the deterministic local engine when a provider is "
        "unavailable; stale-quote decisions record an explicit note; double submit/approve/decide are blocked; and the "
        "engine/decision layer has unit tests plus the 47-check live E2E suite. What we did not build: a user-visible "
        "`retry with backoff` UI for third-party model outages - because the demo runs the local deterministic engine "
        "by default, that path is not exercised, and we did not want to claim a recovery UI we did not ship.",
    )


def sec7(pdf: Doc) -> None:
    pdf.add_page()
    pdf.section_head("7. Anything else we improved after Round 2")
    pdf.set_font("U", "", 8.9)
    pdf.set_text_color(*MUTED)
    items: list[str] = [
        "Email + password demo login with credentials printed on the same login page (was one-click-only).",
        "Added a second demo creator (Rohan) and verified per-user workspace isolation end to end.",
        "PII masking at ingest for emails, phone numbers, and Aadhaar-style IDs.",
        "Image-only reviews enabled (previously required a caption).",
        "Clean 400 for missing title; consistent error messages across upload types.",
        "render.yaml blueprint and README with clone-and-run instructions.",
        "Built frontend dist committed so the repo runs without a build step.",
        "Round 3 product PDF (this document) documenting product, testing, limitations, and roadmap.",
    ]
    for i, line in enumerate(items, 1):
        pdf.set_font("U", "", 8.7)
        pdf.set_text_color(*MUTED)
        pdf.set_x(pdf.l_margin + 2.4)
        pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin - 2.4, 4.2, f"{i}. {line}")
        pdf.set_x(pdf.l_margin)
        pdf.ln(0.4)


def sec8(pdf: Doc) -> None:
    pdf.add_page()
    pdf.section_head("8. Product roadmap and future development plan")
    pdf.set_font("U", "", 8.9)
    pdf.set_text_color(*MUTED)

    pdf.ln(1.4)
    pdf.set_font("U", "B", 9.2)
    pdf.set_text_color(*TEAL)
    pdf.cell(0, 4.6, "Next 0-3 months - make the numbers real.")
    pdf.ln(1.4)
    pdf.set_font("U", "", 8.7)
    pdf.set_text_color(*MUTED)
    pdf.set_x(pdf.l_margin + 2.4)
    pdf.multi_cell(
        pdf.w - pdf.l_margin - pdf.r_margin - 2.4, 4.2,
        "Recruit 1-2 mid-size brand teams (fintech or D2C) as pilots. Collect 30 real drafts across captions, "
        "banners, and documents; label them with two independent raters; publish precision/recall and inter-rater "
        "agreement alongside the synthetic harness results. Success measure: a published, real 30-draft evaluation card.",
    )

    pdf.ln(1.2)
    pdf.set_font("U", "B", 9.2)
    pdf.set_text_color(*AMBER)
    pdf.cell(0, 4.6, "3-6 months - close the declared gaps.")
    pdf.ln(1.4)
    pdf.set_font("U", "", 8.7)
    pdf.set_text_color(*MUTED)
    pdf.set_x(pdf.l_margin + 2.4)
    pdf.multi_cell(
        pdf.w - pdf.l_margin - pdf.r_margin - 2.4, 4.2,
        "Add OCR for scanned PDFs (Tesseract or a hosted vision model behind the existing Citation Lock). Implement "
        "pixel-level logo clear-space enforcement for L-01. Add exportable audit reports (PDF/CSV) so approval records "
        "can be handed to compliance.",
    )

    pdf.ln(1.2)
    pdf.set_font("U", "B", 9.2)
    pdf.set_text_color(*RED)
    pdf.cell(0, 4.6, "6-12 months - distribution and integrations.")
    pdf.ln(1.4)
    pdf.set_font("U", "", 8.7)
    pdf.set_text_color(*MUTED)
    pdf.set_x(pdf.l_margin + 2.4)
    pdf.multi_cell(
        pdf.w - pdf.l_margin - pdf.r_margin - 2.4, 4.2,
        "Build Figma and Canva panels so designers are reviewed where they work; add a verified publishing hand-off "
        "that carries the approval record to social schedulers/CMS. Add sector compliance packs for regulated industries "
        "(financial services first), which is where claim wording carries legal weight.",
    )

    pdf.ln(1.4)
    pdf.set_font("U", "B", 9.2)
    pdf.set_text_color(*MUTED)
    pdf.cell(0, 4.6, "Who it is for.")
    pdf.ln(1.3)
    pdf.set_font("U", "", 8.7)
    pdf.set_text_color(*MUTED)
    pdf.set_x(pdf.l_margin + 2.4)
    pdf.multi_cell(
        pdf.w - pdf.l_margin - pdf.r_margin - 2.4, 4.2,
        "Brand and content teams at mid-to-large organizations, and the agencies that submit drafts on their behalf - "        "the same personas the product already serves in demo form.",
    )

    pdf.ln(1.4)
    pdf.set_font("U", "B", 9.2)
    pdf.set_text_color(*MUTED)
    pdf.cell(0, 4.6, "What it would take.")
    pdf.ln(1.4)
    pdf.set_font("U", "", 8.7)
    pdf.set_text_color(*MUTED)
    pdf.set_x(pdf.l_margin + 2.4)
    pdf.multi_cell(
        pdf.w - pdf.l_margin - pdf.r_margin - 2.4, 4.2,
        "One engineer for OCR and clear-space work, one for integrations, plus the pilot customers for labelled data. "

        "The post-event roadmap is sequenced so a small team can ship the highest-visibility gaps first, and every item "
        "has a measurable exit condition rather than `more features`.",
    )

    pdf.ln(0.5)
    pdf.set_font("U", "I", 8.0)
    pdf.set_text_color(*MUTED)
    pdf.multi_cell(
        pdf.w - pdf.l_margin - pdf.r_margin, 3.8,
        "Objective: a completed, tested, documented product submission for Round 3 - the three named improvements "
        "delivered, the open ends closed, and an honest roadmap for what comes next.",
    )

    if draw_roadmap_footer is not None:
        pdf.ln(1.6)
        draw_roadmap_footer(pdf, pdf.l_margin, pdf.w - pdf.l_margin - pdf.r_margin, pdf)


def build() -> Path:
    pdf = new_doc()
    pdf.set_text_color(*INK)
    cover(pdf)
    pdf.set_text_color(*INK)
    for fn in (sec1, sec2, sec3, sec4, sec5, sec6, sec7, sec8):
        fn(pdf)
        pdf.set_text_color(*INK)
    out = HERE / "PrismCheck_Round3_Submission.pdf"
    pdf.output(str(out))
    print("WROTE", out)
    print("PAGES", pdf.page_no())
    return out


if __name__ == "__main__":
    build()
