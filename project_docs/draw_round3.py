"""
Round 3 figure layer for project_docs.

Provides the three diagram/card helpers called from build_pdf_round3.py:
    draw_arch_overview(pdf, M, CW, pdf)
    draw_image_metrics(pdf, M, CW, pdf)
    draw_roadmap_footer(pdf, M, CW, pdf)

All coordinates are in millimetres. The inputs M (margin) and CW
(content width) are the same convention used by build_pdf.py.

This module is optional: build_pdf_round3.py degrades to text-only if
it cannot import these helpers.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fpdf import FPDF

# palette mirrors build_pdf_round3.py colours (mm-tolerant values)
INK   = (62, 74, 80)
MUTED = (112, 126, 134)
GREY  = (130, 138, 144)
LINE  = (222, 232, 236)

TEAL  = (46, 138, 153)
TEALF = (233, 246, 248)
TEALD = (34, 112, 126)
AMBER = (206, 145, 72)
AMBERF = (253, 244, 230)
GREEN = (74, 150, 122)
GREENF = (232, 246, 240)
ROSE  = (188, 104, 120)
ROSEF = (252, 238, 241)
RED   = (188, 104, 120)
REDF  = (252, 238, 241)
WHITE = (255, 255, 255)
CREAM = (253, 252, 249)
VOID  = (236, 238, 240)
VOIDD = (222, 226, 230)


def _rect(pdf: "FPDF", x: float, y: float, w: float, h: float,
          fill: tuple[int, int, int] | None, draw: tuple[int, int, int],
          lw: float = 0.3) -> None:
    if fill is not None:
        pdf.set_fill_color(*fill)
    pdf.set_draw_color(*draw)
    pdf.set_line_width(lw)
    pdf.rect(x, y, w, h, style=("DF" if fill is not None else "D"))
    pdf.set_line_width(0.2)


def _arrow(pdf: "FPDF", x1: float, y1: float, x2: float, y2: float,
           color: tuple[int, int, int], w: float = 0.35) -> None:
    pdf.set_draw_color(*color)
    pdf.set_line_width(w)
    pdf.line(x1, y1, x2, y2)
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    hl = 1.7
    pdf.line(x2, y2,
             x2 - hl * math.cos(ang - 0.45), y2 - hl * math.sin(ang - 0.45))
    pdf.line(x2, y2,
             x2 - hl * math.cos(ang + 0.45), y2 - hl * math.sin(ang + 0.45))
    pdf.set_line_width(0.2)


def draw_arch_overview(pdf: "FPDF", M: float, CW: float, pdf_add: "FPDF") -> None:
    """Single-origin architecture strip: browser -> FastAPI/SPA -> engine -> kit.

    Placed in section 2 with `pdf.set_y` left to the caller.
    """
    top = pdf_add.get_y() + 0.8

    cols: list[tuple[str, tuple[int, int, int], tuple[int, int, int],
                      float, list[tuple[str, str, tuple[int, int, int]]]]] = [
        (
            "Frontend (React + Vite)", TEAL, TEALF,
            CW * 0.24,
            [
                ("Browser", "React 18 SPA, handcrafted CSS", MUTED),
                ("Sessions", "Signed HttpOnly cookie (itsdangerous)", MUTED),
                ("Assets", "frontend/dist served by FastAPI", MUTED),
            ],
        ),
        (
            "API + auth (FastAPI)", AMBER, AMBERF,
            CW * 0.22,
            [
                ("Roles", "creator / reviewer / admin", MUTED),
                ("Auth", "PBKDF2 demo passwords", MUTED),
                ("Routes", "every route re-checks role", MUTED),
            ],
        ),
        (
            "Engine", GREEN, GREENF,
            CW * 0.26,
            [
                ("Checks", "T-02, T-03, T-14, C-01, V-05, A-03", MUTED),
                ("Match", "in-process token overlap over 5 facts", MUTED),
                ("Citations", "every finding has a source_id", MUTED),
            ],
        ),
        (
            "Storage", ROSE, ROSEF,
            CW * 0.28,
            [
                ("Data", "SQLModel + SQLite", MUTED),
                ("Kit", "JSON rules/facts/palette/lang", MUTED),
                ("Audit", "Revision + Finding + Draft", MUTED),
            ],
        ),
    ]

    gap = (CW - sum(c[3] for c in cols)) / (len(cols) - 1)
    xcur = M
    boxes: list[float] = []
    for title, fill, accent, width, rows in cols:
        y = top
        h = 4.8 + 3.4 * len(rows) + 0.6
        pdf_add.set_fill_color(*fill)
        _rect(pdf_add, xcur, y, width, h, fill, accent, lw=0.3)
        pdf_add.set_xy(xcur + 1.0, y + 0.7)
        pdf_add.set_font("U", "B", 7.6)
        pdf_add.set_text_color(*accent)
        pdf_add.cell(width - 2.0, 3.6, title, align="L")
        pdf_add.set_text_color(*INK)
        for j, (name, desc, txtcol) in enumerate(rows, 1):
            ry = y + 4.4 + (j - 1) * 3.5
            pdf_add.set_xy(xcur + 1.1, ry)
            pdf_add.set_font("U", "B", 7.0)
            pdf_add.set_text_color(*INK)
            wname = pdf_add.get_string_width(name) + 1.0
            pdf_add.cell(wname, 3.4, name)
            pdf_add.set_font("U", "", 6.8)
            pdf_add.set_text_color(*txtcol)
            pdf_add.cell(width - 2.2 - wname, 3.4, desc, align="L")
        boxes.append(xcur + width)
        xcur += width + gap

    xarr = [M + boxes[0] - 0.2]
    for i in range(len(boxes) - 1):
        xarr.append(boxes[i] + gap / 2.0)
    yarr = top + 11.0
    for i, xx in enumerate(xarr[:-1]):
        _arrow(pdf_add, xx, yarr, xarr[i + 1] - 0.4, yarr, GREY, w=0.3)

    pdf_add.set_y(max(pdf_add.get_y(), yarr + 1.2))


def draw_image_metrics(pdf: "FPDF", M: float, CW: float, pdf_add: "FPDF") -> None:
    """Improvement-1 metrics card: precision/recall/F1/false-positive bars."""
    top = pdf_add.get_y() + 1.0
    card_h = 30.0
    y0 = top

    pdf_add.set_fill_color(*CREAM)
    _rect(pdf_add, M, y0, CW, card_h, CREAM, LINE, lw=0.4)
    pdf_add.set_xy(M + 3, y0 + 2.2)
    pdf_add.set_font("U", "B", 8.6)
    pdf_add.set_text_color(*INK)
    pdf_add.cell(0, 4.0, "Measured evaluation - 30 labelled cases (synthetic)")

    pdf_add.set_xy(M + 3, y0 + 6.4)
    pdf_add.set_font("U", "", 7.6)
    pdf_add.set_text_color(*MUTED)
    pdf_add.cell(
        0, 3.4,
        "precision 0.900  ·  recall 0.900  ·  F1 0.900  ·  false-positive rate 0.100",
    )

    bars: list[tuple[str, float, tuple[int, int, int], tuple[int, int, int]]] = [
        ("Precision", 0.900, TEAL, TEALF),
        ("Recall", 0.900, AMBER, AMBERF),
        ("F1", 0.900, GREEN, GREENF),
        ("False-positive rate", 0.100, ROSE, ROSEF),
    ]
    by = y0 + 11.2
    bar_h = 4.4
    max_bar = CW - 9.0
    for name, val, bar, bg in bars:
        pdf_add.set_xy(M + 3, by)
        pdf_add.set_font("U", "", 7.4)
        pdf_add.set_text_color(*INK)
        pdf_add.cell(26, 4.0, name)
        pdf_add.set_fill_color(*bg)
        _rect(pdf_add, M + 29, by + 0.2, max_bar, bar_h, bg, LINE, lw=0.2)
        pdf_add.set_fill_color(*bar)
        pdf_add.rect(M + 29, by + 0.2, max_bar * val, bar_h, style="F")
        pdf_add.set_font("U", "B", 7.2)
        pdf_add.set_text_color(*bar)
        pdf_add.set_xy(M + 29 + max_bar * val - 8.0, by + 0.6)
        pdf_add.cell(8.0, 3.2, f"{val:.3f}", align="R")
        by += bar_h + 0.8

    pdf_add.set_y(y0 + card_h + 1.2)


def draw_roadmap_footer(pdf: "FPDF", M: float, CW: float, pdf_add: "FPDF") -> None:
    """Three-phase roadmap strip for the last content page."""
    top = pdf_add.get_y() + 0.8

    phases: list[tuple[str, str, tuple[int, int, int], tuple[int, int, int]]] = [
        (
            "0-3 months",
            "Make the numbers real:\n30 real drafts, 2 raters, precision/recall.",
            TEAL, TEALF,
        ),
        (
            "3-6 months",
            "Close declared gaps:\nOCR, logo clear-space, audit reports.",
            AMBER, AMBERF,
        ),
        (
            "6-12 months",
            "Distribution & integrations:\nFigma/Canva panels, verified handoff, sector packs.",
            GREEN, GREENF,
        ),
    ]

    colw = (CW - 6) / len(phases)
    for i, (tag, body, bar, bg) in enumerate(phases):
        x = M + i * (colw + 3)
        pdf_add.set_fill_color(*bg)
        _rect(pdf_add, x, top, colw, 26, bg, bar, lw=0.3)
        pdf_add.set_fill_color(*bar)
        pdf_add.rect(x, top, colw, 2.0, style="F")
        pdf_add.set_xy(x + 1.4, top + 2.4)
        pdf_add.set_font("U", "B", 7.6)
        pdf_add.set_text_color(*INK)
        pdf_add.cell(colw - 2.8, 3.2, tag)
        pdf_add.set_font("U", "", 7.0)
        pdf_add.set_text_color(*INK)
        pdf_add.set_xy(x + 1.4, top + 5.6)
        pdf_add.multi_cell(colw - 2.8, 3.2, body)

    pdf_add.set_y(max(pdf_add.get_y(), top + 30))
