#!/usr/bin/env python3
"""Draw the churn signal chart from the real sensor log.

    python3 make_signal.py

Reads data/churn_20260816.csv, the log from the run in the photographs, and
writes images/signal.svg and images/signal-narrow.svg.

The raw readings are noisy. A cordless drill under load spikes hard every
time the churn catches, so single samples run from under a hundred to over
seventeen thousand milliamps and a plot of every point is a solid block of
ink. So the chart shows two things instead. The shaded band is the middle
half of the readings in a moving window, and the line through it is the
median of that window. Nothing is invented, but the noise is summarised
rather than drawn.

The run ends where the motor stopped, about twenty six and a half minutes in.
"""

import csv
import math
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "data", "churn_20260816.csv")
OUT_WIDE = os.path.join(HERE, "images", "signal.svg")
OUT_NARROW = os.path.join(HERE, "images", "signal-narrow.svg")

MOTOR_ON_MA = 800     # below this the drill is not turning
END_S = 1600          # the motor stops for good just before this
WINDOW_S = 50         # width of the moving window
STEP_S = 15

XMIN, XMAX = 0.0, 30.0        # minutes
YMIN, YMAX = 1500.0, 6500.0   # milliamps


def percentile(values, p):
    v = sorted(values)
    return v[min(len(v) - 1, int(len(v) * p / 100))]


def ideal(m):
    """The textbook shape of a churn, in milliamps at minute m.

    Drawn as a dashed second line so the chart can show what the signal is
    supposed to look like next to what this run actually recorded. It is
    hand drawn, not measured, and the legend says so.
    """
    if m < 20.0:
        return 2750.0
    if m < 25.2:
        return 2750.0 + ((m - 20.0) / 5.2) ** 1.45 * 1950.0
    if m < 26.4:
        f = (m - 25.2) / 1.2
        return 4700.0 - (0.5 - 0.5 * math.cos(f * math.pi)) * 2200.0
    return 2500.0 - (m - 26.4) * 14.0


def ideal_path(X, Y):
    pts = []
    m = XMIN
    while m <= XMAX + 1e-9:
        pts.append(f"{X(m):.1f},{Y(ideal(m)):.1f}")
        m += 0.15
    return "M" + " L".join(pts)


def series():
    """Moving median and middle-half band, in minutes and milliamps."""
    with open(LOG, newline="") as fh:
        rows = [r for r in csv.DictReader(fh) if r.get("current_mA")]
    on = [(float(r["elapsed_s"]), float(r["current_mA"])) for r in rows
          if float(r["current_mA"]) > MOTOR_ON_MA and float(r["elapsed_s"]) <= END_S]
    if not on:
        sys.exit(f"no motor-on samples in {LOG}")

    out = []
    t = 0.0
    while t <= END_S:
        w = [c for s, c in on if t - WINDOW_S / 2 <= s < t + WINDOW_S / 2]
        if len(w) >= 8:
            out.append((t / 60.0, percentile(w, 25), statistics.median(w),
                        percentile(w, 75)))
        t += STEP_S

    # The band edges are smoothed a little so the shaded area reads as an
    # envelope rather than a field of spikes. The median line is left alone.
    def smooth(idx):
        vals = [r[idx] for r in out]
        return [statistics.mean(vals[max(0, i - 1):i + 2]) for i in range(len(vals))]

    lo, hi = smooth(1), smooth(3)
    return [(m, lo[i], med, hi[i]) for i, (m, _, med, _) in enumerate(out)]


def build(w, h, pad, ysteps, xsteps, fonts, labels, path, yoff=42, key=None):
    L, R, T, B = pad
    pw, ph = w - L - R, h - T - B
    X = lambda m: L + (m - XMIN) / (XMAX - XMIN) * pw
    Y = lambda v: T + (1 - (min(max(v, YMIN), YMAX) - YMIN) / (YMAX - YMIN)) * ph

    pts = series()
    peak = max(pts, key=lambda r: r[2])

    med = " ".join(("M" if i == 0 else "L") + f"{X(m):.1f},{Y(v):.1f}"
                   for i, (m, _, v, _) in enumerate(pts))
    top = " ".join(("M" if i == 0 else "L") + f"{X(m):.1f},{Y(v):.1f}"
                   for i, (m, _, _, v) in enumerate(pts))
    bot = " ".join(f"L{X(m):.1f},{Y(v):.1f}" for m, v, _, _ in reversed(pts))
    band = top + " " + bot + " Z"

    g = []
    for v in ysteps:
        g.append(f'<line x1="{L}" y1="{Y(v):.1f}" x2="{w-R}" y2="{Y(v):.1f}" class="grid"/>')
        g.append(f'<text x="{L-10}" y="{Y(v)+4:.1f}" class="ax" text-anchor="end">{v}</text>')
    for mm in xsteps:
        g.append(f'<text x="{X(mm):.1f}" y="{h-B+22:.1f}" class="ax" text-anchor="middle">{mm}</text>')

    kx, ky, gap = key
    legend = (
        f'<line x1="{kx}" y1="{ky}" x2="{kx+34}" y2="{ky}" class="trace"/>'
        f'<text x="{kx+44}" y="{ky+5}" class="key">This run</text>'
        f'<line x1="{kx}" y1="{ky+gap}" x2="{kx+34}" y2="{ky+gap}" class="ideal"/>'
        f'<text x="{kx+44}" y="{ky+gap+5}" class="key">The shape it looks for</text>'
    )

    tx = "".join(
        f'<text x="{X(m):.1f}" y="{Y(v)+dy:.1f}" class="{cls}" text-anchor="{a}">{s}</text>'
        for s, m, v, dy, a, cls in labels)

    fa, fl, fs, fu, fk = fonts
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="Motor current across one churn, from the sensor log. The load sits near 2700 milliamps for the first twenty minutes, climbs as the fat gathers, peaks near 4700, then falls away.">
<style>
 .grid{{stroke:#e3d2b4;stroke-width:1}}
 .ax{{font:{fa}px "Avenir Next","Segoe UI",sans-serif;fill:#9a836a;letter-spacing:.04em}}
 .lbl{{font:600 {fl}px "Avenir Next","Segoe UI",sans-serif;fill:#6b5846}}
 .lbl-s{{font:600 {fs}px "Avenir Next","Segoe UI",sans-serif;fill:#a8681a;letter-spacing:.09em}}
 .unit{{font:600 {fu}px "Avenir Next","Segoe UI",sans-serif;fill:#9a836a;letter-spacing:.16em;text-transform:uppercase}}
 .band{{fill:#c08a2e;opacity:.17}}
 .trace{{fill:none;stroke:#c08a2e;stroke-width:2.6;stroke-linejoin:round;stroke-linecap:round}}
 .ideal{{fill:none;stroke:#9a836a;stroke-width:2;stroke-dasharray:7 6;opacity:.85}}
 .key{{font:600 {fk}px "Avenir Next","Segoe UI",sans-serif;fill:#6b5846}}
</style>
<g>{''.join(g)}</g>
<path d="{band}" class="band"/>
<path d="{ideal_path(X, Y)}" class="ideal"/>
<path d="{med}" class="trace"/>
{legend}
<circle cx="{X(peak[0]):.1f}" cy="{Y(peak[2]):.1f}" r="5.5" fill="#a8681a"/>
{tx}
<text x="{L-yoff}" y="{T+ph/2:.1f}" class="unit" text-anchor="middle" transform="rotate(-90 {L-yoff} {T+ph/2:.1f})">Motor current, mA</text>
<text x="{L+pw/2:.1f}" y="{h-9}" class="unit" text-anchor="middle">Minutes into the churn</text>
</svg>'''
    with open(path, "w") as fh:
        fh.write(svg)
    return peak


peak = build(
    900, 470, (74, 26, 44, 62),
    range(2000, 6001, 1000), range(0, 31, 5),
    (13, 14, 13, 11, 13),
    [("Nothing much for twenty minutes", 2.6, 2750, -46, "start", "lbl"),
     ("Fat gathering", 19.6, 2050, 0, "end", "lbl"),
     ("THE BREAK", 24.6, 4704, -24, "end", "lbl-s")],
    OUT_WIDE, key=(102, 66, 26))

build(
    430, 460, (74, 14, 46, 50),
    range(2000, 6001, 2000), range(0, 31, 10),
    (14, 15, 14, 11, 14),
    [("THE BREAK", 23.0, 4704, -20, "end", "lbl-s"),
     ("Nothing yet", 1.2, 2750, -58, "start", "lbl")],
    OUT_NARROW, yoff=58, key=(100, 66, 28))

print(f"peak median {peak[2]:.0f} mA at {peak[0]:.1f} min")
print("wrote", os.path.relpath(OUT_WIDE, HERE), "and", os.path.relpath(OUT_NARROW, HERE))
