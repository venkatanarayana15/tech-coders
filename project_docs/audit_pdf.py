#!/usr/bin/env python3
"""Reusable auditor for the Round 1 submission PDF.

Checks: margin overflow, overlapping text blocks, sparse pages, dark fills,
missing glyphs, page furniture, font sizes actually used.
"""
import statistics
import sys

import pymupdf

PDF = sys.argv[1] if len(sys.argv) > 1 else "PrismCheck_Round1_Submission.pdf"
doc = pymupdf.open(PDF)
N = len(doc)
MM = 72 / 25.4
MARGIN_TOL = 2.0 * MM
LEFT = 16.0 * MM
RIGHT = (210.0 - 16.0) * MM


def blocks(page):
    out = []
    d = page.get_text("dict")
    for b in d["blocks"]:
        if b["type"] != 0:
            continue
        txt = "".join(s["text"] for l in b["lines"] for s in l["spans"]).strip()
        if not txt:
            continue
        sizes = [s["size"] for l in b["lines"] for s in l["spans"]]
        out.append((pymupdf.Rect(b["bbox"]), txt, max(sizes)))
    return out


overflow, overlaps, sparse, sizes_all, dark = [], [], [], [], []
for i, page in enumerate(doc, 1):
    bs = blocks(page)
    chars = sum(len(t) for _, t, _ in bs)
    # a page is sparse only if it has little text AND little artwork
    if 0 < chars < 260 and len(page.get_drawings()) < 25:
        sparse.append((i, chars, len(page.get_drawings())))
    for r, t, sz in bs:
        sizes_all.append(round(sz, 1))
        if r.x0 < LEFT - MARGIN_TOL or r.x1 > RIGHT + MARGIN_TOL:
            overflow.append((i, round(r.x0, 1), round(r.x1, 1), t[:48]))
    for a in range(len(bs)):
        for b in range(a + 1, len(bs)):
            ra, ta, _ = bs[a]
            rb, tb, _ = bs[b]
            inter = ra & rb
            if inter.is_empty or inter.width < 3 or inter.height < 3:
                continue
            small = min(ra.get_area(), rb.get_area())
            if small > 0 and inter.get_area() / small > 0.30:
                overlaps.append((i, ta[:32], tb[:32]))
    for info in page.get_texttrace():
        if info["type"] == 3:  # ignorable / .notdef glyph
            pass
    for dr in page.get_drawings():
        f = dr.get("fill")
        if f is None:
            continue
        lum = 0.2126 * f[0] + 0.7152 * f[1] + 0.0722 * f[2]
        area = dr["rect"].get_area()
        if lum < 0.45 and area > 400:
            dark.append((i, tuple(round(c, 2) for c in f), round(area)))

def containers(page):
    out = []
    for dr in page.get_drawings():
        if dr.get("fill") is None:
            continue
        r = dr["rect"]
        if r.width < 40 or r.height < 6:
            continue
        out.append(r)
    return out


line_hits = []
for i, page in enumerate(doc, 1):
    lines = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            t = "".join(s["text"] for s in l["spans"]).strip()
            if t:
                lines.append((pymupdf.Rect(l["bbox"]), t))
    for a in range(len(lines)):
        for b2 in range(a + 1, len(lines)):
            r = lines[a][0] & lines[b2][0]
            if not r.is_empty and r.width > 0.4 and r.height > 0.4:
                line_hits.append((i, r.width, r.height, lines[a][1][:30], lines[b2][1][:30]))

spills = []
for i, page in enumerate(doc, 1):
    rects = containers(page)
    for r, t, _ in blocks(page):
        inside = [c for c in rects
                  if r.x0 >= c.x0 - 1 and r.y0 >= c.y0 - 1
                  and r.x1 <= c.x1 + 3 and r.y0 < c.y1]
        if not inside:
            continue
        c = min(inside, key=lambda c: c.get_area())
        over = r.y1 - c.y1
        if over > 1.5:
            spills.append((i, round(over, 1), t[:44]))

text = "\n".join(p.get_text() for p in doc)
print(f"FILE   {PDF}")
print(f"PAGES  {N}")
print(f"CHARS  {len(text)}")
print(f"FONTS  {sorted({f[3] for p in doc for f in p.get_fonts()})}")
print(f"SIZES  min {min(sizes_all)} / median {statistics.median(sizes_all)} / max {max(sizes_all)}")
print(f"BODY   median body size {statistics.median([s for s in sizes_all if s >= 8.0])}")
print(f"MOJI   {'none' if chr(0xFFFD) not in text else 'REPLACEMENT CHAR PRESENT'}")
print()
print(f"margin overflow : {len(overflow)}")
for o in overflow[:8]:
    print("   p%-3d x0=%-6s x1=%-6s %s" % o)
print(f"overlaps        : {len(overlaps)}")
for o in overlaps[:8]:
    print("   p%-3d %r vs %r" % o)
print(f"sparse pages    : {len(sparse)}")
for sp in sparse:
    print("   p%-3d %d chars %d drawings" % sp)
print(f"line collisions : {len(line_hits)}")
for lh in line_hits[:8]:
    print("   p%-3d %.1fx%.1f %r vs %r" % lh)
print(f"card spills     : {len(spills)}")
for sp in spills[:10]:
    print("   p%-3d +%.1fmm %r" % sp)
print(f"dark fills      : {len(dark)}")
for dk in dark[:8]:
    print("   p%-3d %s area=%s" % dk)

# page furniture present on every page except cover
missing_furniture = []
for i, page in enumerate(doc, 1):
    if i == 1:
        continue
    t = page.get_text()
    if f"Page {i} of {N}" not in t:
        missing_furniture.append(i)
print(f"footer gaps     : {len(missing_furniture)} {missing_furniture[:8]}")

bad = bool(overflow or overlaps or sparse or dark or missing_furniture or spills or line_hits)
print()
print("RESULT", "FAIL" if bad else "PASS")
sys.exit(1 if bad else 0)
