#!/usr/bin/env python3
"""Draw the AI Ghee mark.

    python3 make_logo.py

The mark is the churn signal used as the surface of the ghee. The load sits
flat while nothing is happening, swells as the fat gathers, peaks, then drops
away when the butter lets go. That shape is the one thing here that no other
ghee brand could have drawn, because it only exists because a machine was
watching, so it is the mark.

Writes the favicon, the small header mark, and the square logo files in both
colourways. PNGs are made with rsvg-convert if it is on the path, and skipped
without complaint if it is not. Nothing here needs anything installed.
"""

import math
import os
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

GOLD, DEEP = "#c08a2e", "#a8681a"
CREAM, DARK = "#f4ead7", "#221a11"
LIT, LIT2 = "#e9b657", "#f2cd85"


def surface(t, base=64.0, peak=22.0, r0=0.30, r1=0.615, f1=0.715, rec=0.88,
            under=5.0, pw=2.0, rt=0.070):
    """Height of the ghee at fraction t across the mark.

    Flat, then the swell, then the break, then it settles back. The numbers
    are shaped after the run in data/churn_20260816.csv rather than measured
    off it, because a logo has to read at sixteen pixels.
    """
    if t < r0:
        return base
    if t < r1 - rt:
        return base - ((t - r0) / (r1 - r0)) ** pw * (base - peak)
    if t < r1 + rt:
        f = (t - (r1 - rt)) / (2 * rt)
        a = base - ((r1 - rt - r0) / (r1 - r0)) ** pw * (base - peak)
        b = peak + (0.5 - 0.5 * math.cos(rt / (f1 - r1) * math.pi)) * (base + under - peak)
        return a + (0.5 - 0.5 * math.cos(f * math.pi)) * (b - a)
    if t < f1:
        f = (t - r1) / (f1 - r1)
        return peak + (0.5 - 0.5 * math.cos(f * math.pi)) * (base + under - peak)
    if t < rec:
        f = (t - f1) / (rec - f1)
        return base + under - (0.5 - 0.5 * math.cos(f * math.pi)) * under
    return base


def mark(body, ring, ring_w=4.8, clip_r=40.6, uid="m", n=260):
    pts = [(-6 + i / n * 112.0, surface(i / n)) for i in range(n + 1)]
    d = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " L106,112 L-6,112 Z"
    return (f'<clipPath id="{uid}"><circle cx="50" cy="50" r="{clip_r}"/></clipPath>'
            f'<g clip-path="url(#{uid})"><path d="{d}" fill="{body}"/></g>'
            f'<circle cx="50" cy="50" r="44" fill="none" stroke="{ring}" stroke-width="{ring_w}"/>')


def page(size, inner, body, ring, bg=None, pad=0.0, **kw):
    scale = (size * (1 - 2 * pad)) / 100.0
    off = size * pad
    ground = f'<rect width="{size}" height="{size}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" '
            f'width="{size}" height="{size}">{ground}'
            f'<g transform="translate({off:g},{off:g}) scale({scale:g})">'
            f'{mark(body, ring, uid=inner, **kw)}</g></svg>')


FILES = {
    # A favicon is judged at sixteen pixels, so the ring is drawn heavier and
    # the ghee pulled in to keep the gap between them open. No background, so
    # the empty part of the vessel takes the colour of whatever tab it sits in.
    "favicon.svg": page(100, "f", GOLD, DEEP, ring_w=7.0, clip_r=39.2),
    "logo.svg": page(100, "l", GOLD, DEEP),
    "logo/ai-ghee-mark-cream.svg": page(800, "c", GOLD, DEEP, bg=CREAM, pad=0.085),
    "logo/ai-ghee-mark-dark.svg": page(800, "d", LIT, LIT2, bg=DARK, pad=0.085),
    "logo/apple-touch-icon-src.svg": page(180, "a", GOLD, DEEP, bg=CREAM, pad=0.12),
}

PNGS = {
    "logo/ai-ghee-mark-cream.svg": ("logo/ai-ghee-mark-cream-800.png", 800),
    "logo/ai-ghee-mark-dark.svg": ("logo/ai-ghee-mark-dark-800.png", 800),
    "logo/apple-touch-icon-src.svg": ("apple-touch-icon.png", 180),
}

for name, svg in FILES.items():
    path = os.path.join(HERE, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        fh.write(svg)
    print("wrote", name)

rsvg = shutil.which("rsvg-convert")
if not rsvg:
    print("rsvg-convert not found, leaving the PNGs alone")
else:
    for src, (out, w) in PNGS.items():
        subprocess.run([rsvg, "-w", str(w), os.path.join(HERE, src),
                        "-o", os.path.join(HERE, out)], check=True)
        print("wrote", out)
