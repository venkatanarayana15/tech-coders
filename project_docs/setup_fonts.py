#!/usr/bin/env python3
"""Regenerate the static Ubuntu instances used by build_pdf.py.

The distro ships Ubuntu-R.ttf / Ubuntu-B.ttf / Ubuntu-M.ttf as symlinks to a
single variable font file, so fpdf2 loads weight 400 for every style and bold
text silently renders as regular. This script pins the variable axes and writes
real static faces next to the builder.
"""
import os

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "fonts")
SRC = "/usr/share/fonts/truetype/ubuntu/Ubuntu[wdth,wght].ttf"
SRC_IT = "/usr/share/fonts/truetype/ubuntu/Ubuntu-Italic[wdth,wght].ttf"

JOBS = [
    (SRC, "Ubuntu-Regular.ttf", 400),
    (SRC, "Ubuntu-Medium.ttf", 500),
    (SRC, "Ubuntu-Bold.ttf", 700),
    (SRC_IT, "Ubuntu-Italic.ttf", 400),
    (SRC_IT, "Ubuntu-BoldItalic.ttf", 700),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    for src, name, wght in JOBS:
        font = TTFont(src)
        axes = {a.axisTag for a in font["fvar"].axes}
        loc = {"wght": wght}
        if "wdth" in axes:
            loc["wdth"] = 100
        inst = instantiateVariableFont(font, loc, inplace=False, updateFontNames=True)
        inst.save(os.path.join(OUT, name))
        print(name, "weight", inst["OS/2"].usWeightClass)


if __name__ == "__main__":
    main()
