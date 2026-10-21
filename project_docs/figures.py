"""Vector illustrations for the PrismCheck Round 1 PDF.

Self-contained drawing helpers so the main builder only has to call two functions.
Everything is drawn with primitives: crisp at any zoom, no external assets.
"""
import math


def _arrow(pdf, x1, y1, x2, y2, color, w=0.45):
    pdf.set_draw_color(*color)
    pdf.set_line_width(w)
    pdf.line(x1, y1, x2, y2)
    ang = math.atan2(y2 - y1, x2 - x1)
    s = 1.6
    p1 = (x2, y2)
    p2 = (x2 - s * math.cos(ang - 0.45), y2 - s * math.sin(ang - 0.45))
    p3 = (x2 - s * math.cos(ang + 0.45), y2 - s * math.sin(ang + 0.45))
    pdf.set_fill_color(*color)
    pdf.polygon([p1, p2, p3], style="F")


def _pill(pdf, x, y, w, h, text, fill, accent, size=6.6, bold=True):
    pdf.set_fill_color(*fill)
    pdf.rect(x, y, w, h, style="F")
    pdf.set_fill_color(*accent)
    pdf.rect(x, y, 0.9, h, style="F")
    pdf.set_font("UB", "B" if bold else "", size)
    pdf.set_text_color(*accent)
    pdf.set_xy(x + 2.2, y + (h - 3.2) / 2)
    pdf.cell(w - 3.0, 3.2, text)


def _label(pdf, x, y, text, color, size=7.4):
    pdf.set_font("UB", "B", size)
    pdf.set_text_color(*color)
    pdf.set_xy(x, y)
    pdf.cell(0, 4, text)


def draw_drift(pdf, M, CW, P):
    """Figure: the same three content sources, with and without a review gate."""
    ink, muted = P["ink"], P["muted"]
    teal, teald, tealf = P["teal"], P["teald"], P["tealf"]
    rose, rosef = P["rose"], P["rosef"]
    green, greenf = P["green"], P["greenf"]
    line, white = P["line"], P["white"]

    top = pdf.get_y() + 1
    colw = CW / 2 - 3

    # ---- left: no gate ----
    x = M
    _label(pdf, x, top, "WITHOUT A GATE", rose)

    src = [("Employee", x, top + 7), ("Agency", x, top + 14.6), ("AI tool", x, top + 22.2)]
    for name, sx, sy in src:
        _pill(pdf, sx, sy, 24, 5.6, name, white, muted, 7.2)
        _arrow(pdf, sx + 24.4, sy + 2.8, sx + 29.4, sy + 2.8, muted)

    # result block
    rx = x + 30
    ry = top + 6.5
    pdf.set_fill_color(*rosef)
    pdf.rect(rx, ry, colw - 30, 22, style="F")
    pdf.set_font("UB", "B", 8.3)
    pdf.set_text_color(*rose)
    pdf.set_xy(rx + 2.5, ry + 2.4)
    pdf.cell(colw - 35, 4, "PUBLISHED, UNCHECKED")
    pdf.set_font("UB", "", 7.7)
    pdf.set_text_color(*ink)
    pdf.set_xy(rx + 2.5, ry + 7.4)
    pdf.multi_cell(colw - 35, 3.4, "Nothing compares the draft with the brand book at the moment it goes out.")

    issues = ["unsupported claim", "outdated price", "off-brand colour", "missing alt text"]
    for i, t in enumerate(issues):
        ix = x + (i % 2) * 42.5
        iy = top + 32.5 + (i // 2) * 7.0
        _pill(pdf, ix, iy, 40, 5.6, t, rosef, rose, 7.4)

    # ---- divider ----
    pdf.set_draw_color(*line)
    pdf.set_line_width(0.5)
    pdf.line(M + CW / 2, top, M + CW / 2, top + 46)

    # ---- right: with gate ----
    x2 = M + CW / 2 + 3
    _label(pdf, x2, top, "WITH PRISMCHECK", green)

    for name, sx, sy in [("Employee", x2, top + 7), ("Agency", x2, top + 14.6), ("AI tool", x2, top + 22.2)]:
        _pill(pdf, sx, sy, 24, 5.6, name, white, muted, 7.2)
        _arrow(pdf, sx + 24.4, sy + 2.8, sx + 29.4, sy + 2.8, muted)

    gx = x2 + 30
    gy = top + 6.5
    pdf.set_fill_color(*tealf)
    pdf.rect(gx, gy, colw - 30, 22, style="F")
    pdf.set_fill_color(*teal)
    pdf.rect(gx, gy, 1.1, 22, style="F")
    pdf.set_font("UB", "B", 8.3)
    pdf.set_text_color(*teald)
    pdf.set_xy(gx + 2.5, gy + 2.4)
    pdf.cell(colw - 35, 4, "BRAND KIT GATE")
    pdf.set_font("UB", "I", 7.7)
    pdf.set_text_color(*ink)
    pdf.set_xy(gx + 2.5, gy + 7.4)
    pdf.multi_cell(colw - 35, 3.4, "Every check cites an approved rule, fact or asset. No source, no flag.")

    _pill(pdf, x2, top + 32.5, 40, 5.6, "2 cited findings", greenf, green, 7.4)
    _pill(pdf, x2 + 42.5, top + 32.5, 40, 5.6, "1 clean pass", white, muted, 7.4)
    pdf.set_font("UB", "B", 7.9)
    pdf.set_text_color(*green)
    pdf.set_xy(x2, top + 40.5)
    pdf.cell(colw - 4, 4, "Creator decides  \u00bb  manager approves  \u00bb  publish")

    pdf.set_y(top + 50)


def draw_kit_and_checks(pdf, M, CW, P):
    """Figure: what the Brand Kit holds, and the four cited checks."""
    ink, muted = P["ink"], P["muted"]
    teal, teald, tealf = P["teal"], P["teald"], P["tealf"]
    amber, amberf = P["amber"], P["amberf"]
    green, greenf = P["green"], P["greenf"]
    rose, rosef = P["rose"], P["rosef"]
    line, white = P["line"], P["white"]

    top = pdf.get_y() + 1
    colw = CW / 2 - 3

    # ---------- left: brand kit ----------
    x = M
    h = 62
    pdf.set_fill_color(*white)
    pdf.set_draw_color(*line)
    pdf.set_line_width(0.4)
    pdf.rect(x, top, colw, h, style="DF")
    pdf.set_fill_color(*tealf)
    pdf.rect(x, top, colw, 6.4, style="F")
    pdf.set_font("UB", "B", 8.5)
    pdf.set_text_color(*teald)
    pdf.set_xy(x + 2.6, top + 1.8)
    pdf.cell(colw - 5, 4, "WHAT THE BRAND KIT HOLDS")

    # colours
    cy = top + 9
    pdf.set_font("UB", "B", 7.7)
    pdf.set_text_color(*muted)
    pdf.set_xy(x + 2.6, cy)
    pdf.cell(18, 3.4, "COLOURS")
    swatches = [((46, 138, 153), "#2E8A99"), ((206, 145, 72), "#CE9148"),
                ((74, 150, 122), "#4A967A"), ((188, 104, 120), "#BC6878")]
    for i, (rgb, hx) in enumerate(swatches):
        swx = x + 21 + i * 15
        pdf.set_fill_color(*rgb)
        pdf.rect(swx, cy - 0.4, 5.4, 5.4, style="F")
        pdf.set_font("UB", "", 6.7)
        pdf.set_text_color(*muted)
        pdf.set_xy(swx - 1.2, cy + 5.2)
        pdf.cell(12, 3, hx)

    # facts
    fy = top + 18
    pdf.set_font("UB", "B", 7.7)
    pdf.set_text_color(*muted)
    pdf.set_xy(x + 2.6, fy)
    pdf.cell(18, 3.4, "FACTS")
    pdf.set_font("UB", "", 7.5)
    pdf.set_text_color(*ink)
    pdf.set_xy(x + 21, fy)
    pdf.multi_cell(colw - 24, 3.4, "F-01 delivery 2 days  \u00b7  F-02 no annual fee year one  \u00b7  F-03 rate sheet v4")

    # terminology
    ty = top + 28
    pdf.set_font("UB", "B", 7.7)
    pdf.set_text_color(*muted)
    pdf.set_xy(x + 2.6, ty)
    pdf.cell(18, 3.4, "TERMS")
    _pill(pdf, x + 21, ty - 0.6, 30, 4.8, "prefer: members", greenf, green, 7.0)
    _pill(pdf, x + 53, ty - 0.6, 28, 4.8, "ban: guaranteed", rosef, rose, 7.0)

    # tone
    ty2 = top + 37
    pdf.set_font("UB", "B", 7.7)
    pdf.set_text_color(*muted)
    pdf.set_xy(x + 2.6, ty2)
    pdf.cell(18, 3.4, "TONE")
    for i, (nm, frac) in enumerate([("warm", 0.68), ("direct", 0.42), ("formal", 0.22)]):
        sy = ty2 + i * 6.4
        pdf.set_font("UB", "", 7.1)
        pdf.set_text_color(*muted)
        pdf.set_xy(x + 21, sy)
        pdf.cell(12, 3, nm)
        track_x = x + 34
        track_w = colw - 38
        pdf.set_draw_color(*line)
        pdf.set_line_width(0.8)
        pdf.line(track_x, sy + 1.6, track_x + track_w, sy + 1.6)
        pdf.set_fill_color(*teal)
        pdf.rect(track_x + track_w * frac - 1.1, sy + 0.3, 2.2, 2.6, style="F")

    # ---------- right: four checks ----------
    x2 = M + CW / 2 + 3
    checks = [
        ("Claims and facts", "deterministic + model", rose, rosef,
         "Is the claim in the fact bank?"),
        ("Tone and intent", "model, cited rewrite", amber, amberf,
         "Does this match the tone rule?"),
        ("Visual vs kit", "deterministic", teal, tealf,
         "Colour distance and clear space"),
        ("Accessibility", "deterministic", green, greenf,
         "4.5:1 contrast, alt text present"),
    ]
    bw = (colw - 4) / 2
    bh = 27
    for i, (title, tag, accent, fill, line1) in enumerate(checks):
        cx = x2 + (i % 2) * (bw + 4)
        cy2 = top + (i // 2) * (bh + 4)
        pdf.set_fill_color(*fill)
        pdf.rect(cx, cy2, bw, bh, style="F")
        pdf.set_fill_color(*accent)
        pdf.rect(cx, cy2, bw, 0.9, style="F")
        pdf.set_font("UB", "B", 8.1)
        pdf.set_text_color(*accent)
        pdf.set_xy(cx + 2.4, cy2 + 2.6)
        pdf.cell(bw - 4.8, 3.4, title)
        pdf.set_font("UB", "B", 6.7)
        pdf.set_text_color(*muted)
        pdf.set_xy(cx + 2.4, cy2 + 6.6)
        pdf.cell(bw - 4.8, 3.0, tag.upper())
        pdf.set_font("UB", "", 7.5)
        pdf.set_text_color(*ink)
        body_h2 = pdf.multi_cell(bw - 4.8, 3.4, line1, dry_run=True, output="HEIGHT")
        pdf.set_xy(cx + 2.4, cy2 + 11.2)
        pdf.multi_cell(bw - 4.8, 3.4, line1)
        pdf.set_font("UB", "I", 6.9)
        pdf.set_text_color(*muted)
        pdf.set_xy(cx + 2.4, cy2 + 11.2 + body_h2 + 1.2)
        pdf.cell(bw - 4.8, 3.0, "cites a kit item")

    label_y = top + 2 * bh + 4 + 2.4
    pdf.set_font("UB", "I", 7.0)
    pdf.set_text_color(*muted)
    pdf.set_xy(x2, label_y)
    pdf.multi_cell(colw - 2, 3.2, "Checks that must never guess run deterministically; the model only cites.")

    pdf.set_y(top + h + 3)
