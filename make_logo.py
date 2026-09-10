#!/usr/bin/env python3
"""Draw the AI Ghee mark and everything made from it.

    python3 make_logo.py

The mark is the Nepali word for ghee, घ्यू, with its shirorekha carried on
past the word. Somewhere in that run the line takes one reading, flat then a
swell then the break, which is the shape the rig watches for while it churns.
A dot marks the apex.

The letterform is stored below as outline paths rather than as text, so
nothing here needs Noto Serif Devanagari installed and no renderer can
re-shape the conjunct wrongly. The half form of घ, where it drops its stem
and joins य, is baked into the artwork.

Every file is built from one set of numbers, so the whole family stays in
step. Changing MASTER changes all of it at once. PNGs are written with
rsvg-convert when it is on the path and skipped quietly when it is not.
"""

import math
import os
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- the palette
INK, GOLD, DEEP = "#1b1712", "#c08a2e", "#a8681a"
CREAM, PAPER, LIT = "#f4ead7", "#fff8ec", "#e9b657"
BLACK, WHITE = "#000000", "#ffffff"

# ------------------------------------------------------------ the letterform
# Outlines of घ्यू at font-size 100 with the baseline at y=0, taken from Noto
# Serif Devanagari. BBOX is x, y, width, height of the ink at that size.
GLYPH = {
    500: [
        "m 26.6,-11 q -3.7,0 -7.1,-1.2 -3.3,-1.3 -6.3,-4.3 -2.5,-2.3 -4.5,-5.2 -1.9,-3 -1.9,-6.3 0,-3.6 2,-6.2 2,-2.7 5.4,-4.4 -4.5,-2.1 -7.3,-5.1 -2.7,-3.1 -2.7,-7.6 0,-1.7 0.6,-3.4 h -5 l -4.4,-6.6 v -1.1 h 45.5 l 4.3,6.7 v 1 H 14.7 q -1.3,2.1 -1.3,4.5 0,2.6 1.4,5.1 1.4,2.4 4.3,4.5 3.2,-0.9 7,-1.3 l 5.5,7.9 q -7.3,0.6 -12,3.2 -4.7,2.5 -4.7,6.7 0,2.5 1.8,4.1 1.9,1.6 5.7,1.6 4.9,0 9.9,-3.2 5,-3.2 8.6,-8.1 l 5.5,7.3 q -3.5,4.8 -8.7,8.1 -5.2,3.3 -11.1,3.3 z",
        "m 63.599902,-13.9 q -9.1,0 -15.5,-5.7 -6.3,-5.7 -10,-14.7 6.6,-2.7 10.1,-5.8 3.6,-3.2 3.6,-7.1 0,-2.4 -0.9,-4.2 -0.8,-1.8 -1.9,-3.3 h -14.3 l -4.4,-6.5 v -1.2 h 61.8 l 4.3,6.7 v 1 h -12.6 V 0.7 h -1.1 l -7.8,-5.5 v -12.5 q -2.3,1.6 -5.3,2.5 -2.9,0.9 -6,0.9 z m -12.2,-9.7 q 1.4,0.9 3.3,1.5 2,0.6 4.3,0.6 4.5,0 8.6,-2.1 4.2,-2.1 7.3,-5.8 v -25.3 h -19.9 q 2.1,2.6 3.6,5.6 1.5,2.9 1.5,5.9 0,4.3 -2.5,7.3 -2.4,2.9 -7.4,6.3 -1.5,1.1 -1.5,2.2 0,2.1 2.7,3.8 z",
        "m 82.499924,27.799974 q -3.4,0 -6.4,-1.7 -3.1,-1.7 -5.6,-4.1 -2.3,-2.3 -3.7,-4.9 -1.4,-2.5 -1.4,-5.8 0,-3.0999999 1.6,-5.8999999 1.6,-2.8 4.6,-4.60000004 2.9,-1.7 7.1,-1.7 5.6,0 10.3,3.20000004 4.6,3.2 9.5,8.8999999 4.899996,5.8 11.299996,13.2 l -5,3.5 q -4.899996,-6.5 -8.699996,-11.2 -3.7,-4.6 -7.1,-7.0999999 -3.4,-2.5 -7.2,-2.5 -4,0 -6.5,2.2 -2.5,2.1999999 -2.5,5.6999999 0,2.9 1.5,4.4 1.4,1.5 4,1.5 2.2,0 4.7,-0.8 2.5,-0.7 5.8,-3 l 2.8,8.4 q -2.4,1.1 -4.4,1.7 -2.1,0.6 -4.7,0.6 z",
    ],
    600: [
        "m 26.9,-10.9 q -7.5,0 -13.3,-5.2 -2.8,-2.4 -5,-5.3 -2.2,-3 -2.2,-6.5 0,-3.5 1.9,-6.1 2,-2.7 5.4,-4.5 -4.5,-2.2 -7.3,-5.2 -2.7,-3 -2.7,-7.3 0,-1.4 0.4,-2.7 h -4.6 l -4.8,-7.5 v -1.3 h 45.9 l 4.8,7.6 v 1.2 H 14.7 q -0.9,2 -0.9,4.1 0,5.1 5.2,9 3.3,-1 7.2,-1.5 l 5.8,8.7 q -7.4,0.7 -12,3.1 -4.6,2.4 -4.6,6.3 0,2.4 1.7,3.8 1.8,1.4 5.2,1.4 3.2,0 6.7,-1.6 3.5,-1.6 6.7,-4.3 3.2,-2.8 5.6,-6 l 6,7.9 q -4,5.4 -9.3,8.7 -5.3,3.2 -11.1,3.2 z",
        "m 65.799954,-13.1 q -9,0 -15.9,-5.6 -6.8,-5.6 -11,-15.5 6.9,-2.9 10.3,-5.9 3.5,-3.1 3.5,-7.1 0,-1.9 -0.6,-3.5 -0.5,-1.6 -1.4,-3 h -15.7 l -4.8,-7.5 v -1.3 h 64.2 l 4.8,7.6 v 1.2 h -12.9 V 0.7 h -1.2 l -9.4,-6.2 v -10.2 q -2.1,1.2 -4.6,1.9 -2.5,0.7 -5.3,0.7 z m -12.7,-10.6 q 1.3,0.9 3.1,1.5 1.8,0.5 3.8,0.5 4.3,0 8.4,-2 4.1,-2.1 7.3,-5.8 v -24.2 h -18.3 q 2.2,2.7 3.5,5.6 1.4,2.8 1.4,5.5 0,4.2 -2.4,7.2 -2.4,2.9 -7.3,6.2 -1.7,1.2 -1.7,2.3 0,1.7 2.2,3.2 z",
        "m 84.499992,28.099948 q -3.7,0 -6.8,-1.6 -3.2,-1.6 -5.8,-4 -2.5,-2.4 -4.1,-5.3 -1.6,-2.8 -1.6,-6.4 0,-3.1999999 1.7,-5.9999999 1.6,-2.8 4.6,-4.49999998 3,-1.70000002 7.1,-1.70000002 5.6,0 10.2,2.9 4.6,2.9 9.7,8.5999999 5.099998,5.7 12.199998,13.9 l -5.6,4 q -4.9,-6.6 -8.599998,-11.2 -3.6,-4.5 -6.9,-6.7999999 -3.3,-2.3 -7.2,-2.3 -4,0 -6.5,2.1 -2.5,2.0999999 -2.5,5.2999999 0,2.5 1.5,3.9 1.4,1.4 3.9,1.4 2.2,0 4.8,-0.9 2.5,-0.9 5.7,-3.1 l 3.3,9.4 q -2.3,1.2 -4.4,1.7 -2.1,0.6 -4.7,0.6 z",
    ],
}
# Horizontal centre of the ink, in glyph units. Solved by rendering against
# the master and minimising the pixel difference, which landed at 45 pixels in
# 640,000, so this reproduces route-7-ghyu-cream exactly rather than nearly.
INK_CX = {500: 52.41, 600: 53.41}

# --------------------------------------------------------------- the geometry
# Measured off a render of the type, in em. The drawn rule sits at SH_MID with
# SH_TH weight so it merges into the glyph's own shirorekha with no seam.
SH_MID, SH_TH = 0.5854, 0.0792
INK_TOP, INK_BOT = 0.6250, -0.2750
RISE = 0.118

# route-7-ghyu-cream is the master. These are its numbers and nothing here
# re-tunes them, so every other file in the family is the same drawing.
MASTER = dict(fs=50.0, rw=42.0, peak_at=(6.0, 23.5), weight=500)


def place(weight, fs, cx, baseline):
    """Transform putting the glyph's ink centre at cx, on the given baseline."""
    s = fs / 100.0
    return f"translate({cx - INK_CX[weight] * s:.4f},{baseline:.4f}) scale({s:.6f})"


def glyph_svg(weight, fs, cx, baseline, fill):
    g = "".join(f'<path d="{d}"/>' for d in GLYPH[weight])
    return f'<g transform="{place(weight, fs, cx, baseline)}" fill="{fill}">{g}</g>'


def baseline_for(fs, peak):
    """Baseline that centres the whole lockup, the peak's rise included."""
    return (100 + (INK_TOP + INK_BOT) * fs + (RISE * fs if peak else 0.0)) / 2


def signal(x0, x1, y, rise, n=90):
    """Flat, swell, break, flat. Drawn from the shape of a churn."""
    pts = []
    for i in range(n + 1):
        t = i / n
        if t < 0.30:
            v = 0.0
        elif t < 0.68:
            v = -((t - 0.30) / 0.38) ** 1.8
        elif t < 0.85:
            v = -1.0 + (0.5 - 0.5 * math.cos((t - 0.68) / 0.17 * math.pi))
        else:
            v = 0.0
        pts.append((x0 + t * (x1 - x0), y + v * rise))
    return pts


def mark(ink, accent=None, peak=True, dot=True, weight=None, scale=1.0):
    """The full mark. accent is the apex dot, left off for one colour work."""
    fs = MASTER["fs"]
    rw = MASTER["rw"]
    wt = weight or MASTER["weight"]
    base = baseline_for(fs, peak)
    y = base - SH_MID * fs
    w = SH_TH * fs
    o = []
    if peak:
        pts = signal(MASTER["peak_at"][0], MASTER["peak_at"][1], y, RISE * fs)
        apex = min(pts, key=lambda q: q[1])
        d = (f"M{50-rw:.2f},{y:.2f} L"
             + " L".join(f"{a:.2f},{b:.2f}" for a, b in pts)
             + f" L{50+rw:.2f},{y:.2f}")
        o.append(f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="{w:.2f}" '
                 f'stroke-linecap="butt" stroke-linejoin="round"/>')
    else:
        o.append(f'<line x1="{50-rw:.2f}" y1="{y:.2f}" x2="{50+rw:.2f}" y2="{y:.2f}" '
                 f'stroke="{ink}" stroke-width="{w:.2f}" stroke-linecap="butt"/>')
    o.append(glyph_svg(wt, fs, 50.0, base, ink))
    if peak and dot and accent:
        o.append(f'<circle cx="{apex[0]:.2f}" cy="{apex[1]:.2f}" r="{w*0.92:.2f}" fill="{accent}"/>')
    inner = "".join(o)
    if scale != 1.0:
        inner = f'<g transform="translate(50,50) scale({scale}) translate(-50,-50)">{inner}</g>'
    return inner


def glyph(ink, fs=62.0, weight=600):
    """Just the word, set heavier. For favicons, where a hairline rule dies."""
    return glyph_svg(weight, fs, 50.0, baseline_for(fs, False), ink)


def page(inner, bg=None, size=800, pad=0.0, circle=False):
    s = 1.0 - 2 * pad
    off = size * pad
    ground = ""
    if bg and circle:
        ground = f'<circle cx="{size/2}" cy="{size/2}" r="{size/2}" fill="{bg}"/>'
    elif bg:
        ground = f'<rect width="{size}" height="{size}" fill="{bg}"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" '
            f'width="{size}" height="{size}">{ground}'
            f'<g transform="translate({off:g},{off:g}) scale({size*s/100:.6f})">{inner}</g></svg>')


# ------------------------------------------------------------------ the files
# name -> (svg, png width or None). Everything is built from mark() and glyph()
# so the whole family is one drawing in different clothes.
SQ, CIRC = dict(pad=0.10), dict(pad=0.10, circle=True)
GCIRC = dict(pad=0.14, circle=True)

FILES = {
    # the site itself
    # the icons are set larger than the brand glyph, because at 16px every
    # unit of the box matters and there is nothing else in there to balance
    "favicon.svg":        (page(glyph(GOLD, fs=80), None, 100, pad=0.02), None),
    "logo.svg":           (page(glyph(INK, fs=80), None, 100, pad=0.02), None),
    "logo-mark.svg":      (page(mark(INK, GOLD), None, 100, **SQ), None),

    # the brand files, primary
    "logo/ai-ghee-mark-cream.svg":        (page(mark(INK, GOLD), CREAM, **SQ), 800),
    "logo/ai-ghee-mark-ink.svg":          (page(mark(PAPER, GOLD), INK, **SQ), 800),
    "logo/ai-ghee-mark-gold.svg":         (page(mark(INK, PAPER), GOLD, **SQ), 800),
    "logo/ai-ghee-mark-clear.svg":        (page(mark(INK, GOLD), None, **SQ), None),

    # in a circle, for avatars and anything that gets cropped round
    "logo/ai-ghee-mark-circle-cream.svg": (page(mark(INK, GOLD), CREAM, **CIRC), 800),
    "logo/ai-ghee-mark-circle-ink.svg":   (page(mark(PAPER, GOLD), INK, **CIRC), 800),
    "logo/ai-ghee-mark-circle-gold.svg":  (page(mark(INK, PAPER), GOLD, **CIRC), 800),

    # the quiet cut, for places where the reading is too much
    "logo/ai-ghee-quiet-cream.svg":       (page(mark(INK, None, peak=False, dot=False), CREAM, **SQ), 800),
    "logo/ai-ghee-quiet-ink.svg":         (page(mark(PAPER, None, peak=False, dot=False), INK, **SQ), 800),

    # the word alone, for small sizes where a hairline rule cannot survive
    "logo/ai-ghee-glyph-cream.svg":       (page(glyph(INK), CREAM, **SQ), 800),
    "logo/ai-ghee-glyph-ink.svg":         (page(glyph(LIT), INK, **SQ), 800),
    "logo/ai-ghee-glyph-circle-ink.svg":  (page(glyph(LIT), INK, **GCIRC), 800),
    "logo/ai-ghee-glyph-clear.svg":       (page(glyph(INK), None, **SQ), None),

    # one colour, for print, stamps, embossing and faxes
    "logo/print/mark-black.svg":          (page(mark(BLACK, None, dot=False), WHITE, **SQ), 800),
    "logo/print/mark-white.svg":          (page(mark(WHITE, None, dot=False), BLACK, **SQ), 800),
    "logo/print/mark-black-clear.svg":    (page(mark(BLACK, None, dot=False), None, **SQ), None),
    "logo/print/mark-white-clear.svg":    (page(mark(WHITE, None, dot=False), None, **SQ), None),
    "logo/print/mark-circle-black.svg":   (page(mark(WHITE, None, dot=False), BLACK, **CIRC), 800),
    "logo/print/glyph-black-clear.svg":   (page(glyph(BLACK), None, **SQ), None),
    "logo/print/glyph-white-clear.svg":   (page(glyph(WHITE), None, **SQ), None),
}

EXTRA_PNG = {"apple-touch-icon.png": (page(glyph(LIT, fs=72), INK, 180, pad=0.14), 180)}


def main():
    rsvg = shutil.which("rsvg-convert")
    for name, (svg, png_w) in FILES.items():
        path = os.path.join(HERE, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fh:
            fh.write(svg)
        print("wrote", name)
        if png_w and rsvg:
            out = path[:-4] + ".png"
            subprocess.run([rsvg, "-w", str(png_w), path, "-o", out], check=True)
            print("wrote", name[:-4] + ".png")
    for name, (svg, png_w) in EXTRA_PNG.items():
        tmp = os.path.join(HERE, "logo", "_tmp.svg")
        os.makedirs(os.path.dirname(tmp), exist_ok=True)
        with open(tmp, "w") as fh:
            fh.write(svg)
        if rsvg:
            subprocess.run([rsvg, "-w", str(png_w), tmp,
                            "-o", os.path.join(HERE, name)], check=True)
            print("wrote", name)
        os.remove(tmp)
    if not rsvg:
        print("rsvg-convert not found, the PNGs were left alone")


if __name__ == "__main__":
    main()
