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
import re
import statistics
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "data", "churn_20260816.csv")

# Every word on the chart, once per language. The data is read once and both
# versions are drawn from it, so the two can never disagree about the run.
#
# Devanagari hangs from one bar along the top of a word, so the tracking that
# opens up the Latin labels would break that bar, and it is set to nothing on
# the Nepali chart. The font stack keeps the Latin faces in front, so a
# Devanagari face is only reached for the characters they do not carry.
SANS = '"Avenir Next","Segoe UI",sans-serif'
SANS_NE = ('"Avenir Next","Segoe UI","Kohinoor Devanagari",'
           '"Devanagari Sangam MN","Nirmala UI","Noto Sans Devanagari",sans-serif')
SANS_ZH = ('"Avenir Next","Segoe UI","PingFang SC","Hiragino Sans GB",'
           '"Microsoft YaHei","Noto Sans CJK SC","Noto Sans SC",sans-serif')
SANS_KA = ('"Avenir Next","Segoe UI","Noto Sans Georgian",Sylfaen,sans-serif')
SANS_BN = ('"Avenir Next","Segoe UI","Kohinoor Bangla","Bangla Sangam MN",'
           '"Nirmala UI","Noto Sans Bengali",Vrinda,sans-serif')
SANS_JA = ('"Avenir Next","Segoe UI","Hiragino Sans","Hiragino Kaku Gothic ProN",'
           '"Yu Gothic",Meiryo,"Noto Sans CJK JP","Noto Sans JP",sans-serif')
SANS_YUE = ('"Avenir Next","Segoe UI","PingFang HK","Hiragino Sans CNS",'
            '"Microsoft JhengHei","Noto Sans CJK HK","Noto Sans CJK TC",'
            '"Noto Sans HK",sans-serif')
SANS_AR = ('"Avenir Next","Segoe UI","Geeza Pro","Segoe UI Arabic",'
           '"Noto Sans Arabic","Noto Naskh Arabic",Tahoma,sans-serif')

# A chart in a right to left language sets `iso`, and every piece of text that
# language supplies is then wrapped in a pair of Unicode isolates.
#
# The obvious alternative was direction:rtl in the stylesheet inside the SVG,
# and it is the wrong tool. A renderer does honour it, but it also flips what
# text-anchor start and end mean, so every label on the chart would move and
# the geometry below would have to be written twice and kept in step. The
# isolates do only the thing actually wanted. They set the base direction of
# the run, so the words and the units come out in the order an Arabic reader
# expects, and they leave the anchors and every coordinate exactly as they are
# for the other eighteen languages. Checked in rsvg and in a browser.
#
# The tick numbers are not wrapped. They are bare Latin digits with nothing
# around them, so there is no reordering for an isolate to do.
RLI, LRI, PDI = "\u2067", "\u2066", "\u2069"

# A Latin technical run inside a right to left label.
#
# `12 V SUPPLY` becomes `تغذية 12 V` in Arabic, and written as it stands that
# draws as `تغذية V 12`. The digits are read as an Arabic number, because the
# word before them is Arabic, the unit is read as Latin, the space between
# belongs to the Arabic, and the two end up as separate pieces laid out right
# to left. The Unicode algorithm is doing the right thing with a string that
# did not say what it meant. A value and its unit are one object and have to
# be marked as one, which is what the left to right isolate does.
#
# Only a run holding a Latin letter is wrapped. A bare number is already laid
# out correctly and wrapping one would change nothing.
TECH_RUN = re.compile(
    r"[A-Za-z0-9][A-Za-z0-9.+\-/_]*(?:[ \u00a0][A-Za-z0-9][A-Za-z0-9.+\-/_]*)*")


def protect(text):
    """Hold each Latin technical run together inside a right to left label."""
    return TECH_RUN.sub(
        lambda m: (LRI + m.group(0) + PDI
                   if re.search("[A-Za-z]", m.group(0)) else m.group(0)),
        text)



# `caps` is left at none on every chart now and the axis titles are written in
# the case they are meant to print in. CSS uppercasing cannot tell a word from
# a unit, and it was turning the milliamps on the current axis into MA, which
# is megaamps. The field stays because a script may still want the transform.
EN = dict(
    stack=SANS, track=(".04em", ".09em", ".16em"), caps="none", lift=1.0,
    out=("signal.svg", "signal-narrow.svg"),
    aria="Motor current across one churn, from the sensor log. The load sits "
         "near 2700 milliamps for the first twenty minutes, climbs as the fat "
         "gathers, peaks near 4700, then falls away.",
    y="MOTOR CURRENT, mA", x="MINUTES INTO THE CHURN",
    run="This run", ideal="The shape it looks for",
    wide=[("Nothing much for twenty minutes", 2.6, 2750, -46, "start", "lbl"),
          ("Fat gathering", 19.6, 2050, 0, "end", "lbl"),
          ("THE BREAK", 24.6, 4704, -24, "end", "lbl-s")],
    narrow=[("THE BREAK", 23.0, 4704, -20, "end", "lbl-s"),
            ("Nothing yet", 1.2, 2750, -58, "start", "lbl")],
)

NE = dict(
    stack=SANS_NE, track=("0", "0", ".02em"), caps="none", lift=1.16,
    out=("signal-ne.svg", "signal-ne-narrow.svg"),
    lean=9, lean_narrow=0,
    aria="एउटै मोही पार्दाको मोटर करेन्टको चार्ट, सेन्सर लगबाट। लोड सुरुको बीस "
         "मिनेट करिब 2700 मिलिएम्पियरमा बस्छ, बोसो जम्मा हुँदै जाँदा चढ्छ, करिब "
         "4700 मा पुग्छ, अनि झर्छ।",
    y="मोटर करेन्ट, mA", x="मोही पार्न थालेको, मिनेट",
    run="यो रन", ideal="खोजिएको आकार",
    wide=[("बीस मिनेट केही हुँदैन", 2.6, 2750, -46, "start", "lbl"),
          ("बोसो जम्मा हुँदै", 19.6, 2050, 0, "end", "lbl"),
          ("नौनी छुट्टियो", 24.6, 4704, -24, "end", "lbl-s")],
    narrow=[("नौनी छुट्टियो", 23.0, 4704, -20, "end", "lbl-s"),
            ("अझै केही छैन", 1.2, 2750, -58, "start", "lbl")],
)

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


def iso(S, text):
    """A language supplied string, given its own base direction if it needs one."""
    return f"{RLI}{protect(text)}{PDI}" if S.get("iso") else text


def scaled(size, lift):
    """A type size after the language's lift, kept whole where it lands whole."""
    v = round(size * lift, 1)
    return int(v) if v == int(v) else v


def build(w, h, pad, ysteps, xsteps, fonts, labels, path, yoff=42, key=None,
          S=EN):
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
        f'<text x="{kx+44}" y="{ky+5}" class="key">{iso(S, S["run"])}</text>'
        f'<line x1="{kx}" y1="{ky+gap}" x2="{kx+34}" y2="{ky+gap}" class="ideal"/>'
        f'<text x="{kx+44}" y="{ky+gap+5}" class="key">{iso(S, S["ideal"])}</text>'
    )

    tx = "".join(
        f'<text x="{X(m):.1f}" y="{Y(v)+dy:.1f}" class="{cls}" '
        f'text-anchor="{a}">{iso(S, s)}</text>'
        for s, m, v, dy, a, cls in labels)

    fa, fl, fs, fu, fk = (scaled(f, S["lift"]) for f in fonts)
    ta, ts, tu = S["track"]
    st = S["stack"]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{S["aria"]}">
<style>
 .grid{{stroke:#e3d2b4;stroke-width:1}}
 .ax{{font:{fa}px {st};fill:#9a836a;letter-spacing:{ta}}}
 .lbl{{font:600 {fl}px {st};fill:#6b5846}}
 .lbl-s{{font:600 {fs}px {st};fill:#a8681a;letter-spacing:{ts}}}
 .unit{{font:600 {fu}px {st};fill:#9a836a;letter-spacing:{tu};text-transform:{S["caps"]}}}
 .band{{fill:#c08a2e;opacity:.17}}
 .trace{{fill:none;stroke:#c08a2e;stroke-width:2.6;stroke-linejoin:round;stroke-linecap:round}}
 .ideal{{fill:none;stroke:#9a836a;stroke-width:2;stroke-dasharray:7 6;opacity:.85}}
 .key{{font:600 {fk}px {st};fill:#6b5846}}
</style>
<g>{''.join(g)}</g>
<path d="{band}" class="band"/>
<path d="{ideal_path(X, Y)}" class="ideal"/>
<path d="{med}" class="trace"/>
{legend}
<circle cx="{X(peak[0]):.1f}" cy="{Y(peak[2]):.1f}" r="5.5" fill="#a8681a"/>
{tx}
<text x="{L-yoff}" y="{T+ph/2:.1f}" class="unit" text-anchor="middle" transform="rotate(-90 {L-yoff} {T+ph/2:.1f})">{iso(S, S["y"])}</text>
<text x="{L+pw/2:.1f}" y="{h-9}" class="unit" text-anchor="middle">{iso(S, S["x"])}</text>
</svg>'''
    with open(path, "w") as fh:
        fh.write(svg)
    return peak



# French is Latin script, so it keeps the stack and the tracking the English
# chart was drawn with. Both wide annotations run longer than their English
# originals, which is why they were checked at render rather than assumed.
FR = dict(
    stack=SANS, track=(".04em", ".09em", ".16em"), caps="none", lift=1.0,
    out=("signal-fr.svg", "signal-fr-narrow.svg"),
    aria="Graphique du courant du moteur sur un barattage, d'apr\u00e8s le log du "
         "capteur. La charge reste pr\u00e8s de 2700 milliamp\u00e8res pendant les vingt "
         "premi\u00e8res minutes, monte \u00e0 mesure que la mati\u00e8re grasse se rassemble, "
         "culmine pr\u00e8s de 4700, puis retombe.",
    y="COURANT MOTEUR, mA", x="MINUTES DE BARATTAGE",
    run="Cette fourn\u00e9e", ideal="La forme recherch\u00e9e",
    wide=[("Presque rien pendant vingt minutes", 2.6, 2750, -46, "start", "lbl"),
          ("Le gras se rassemble", 19.6, 2050, 0, "end", "lbl"),
          ("LA CASSURE", 24.6, 4704, -24, "end", "lbl-s")],
    narrow=[("LA CASSURE", 23.0, 4704, -20, "end", "lbl-s"),
            ("Toujours rien", 1.2, 2750, -58, "start", "lbl")],
)


# Kinyarwanda is Latin script, so it takes the English stack and tracking.
RW = dict(
    stack=SANS, track=(".04em", ".09em", ".16em"), caps="none", lift=1.0,
    out=("signal-rw.svg", "signal-rw-narrow.svg"),
    aria="Igishushanyo cya courant ya moteur mu gucunda rimwe, kivuye mu log ya "
         "capteur. Charge iguma hafi ya 2700 milliamp\u00e8res mu minota "
         "makumyabiri ya mbere, izamuka uko ibinure biteranira, igera ku ntera "
         "ya hejuru hafi ya 4700, hanyuma iragwa.",
    y="COURANT YA MOTEUR, mA", x="IMINOTA MU GUCUNDA",
    run="Iki gikorwa", ideal="Ishusho ishakwa",
    wide=[("Nta kintu mu minota makumyabiri", 2.6, 2750, -46, "start", "lbl"),
          ("Ibinure biteranira", 19.6, 2050, 0, "end", "lbl"),
          ("AMAVUTA YACITSE", 24.6, 4704, -24, "end", "lbl-s")],
    narrow=[("AMAVUTA YACITSE", 23.0, 4704, -20, "end", "lbl-s"),
            ("Nta kintu kirabaho", 1.2, 2750, -58, "start", "lbl")],
)


# Luganda is Latin script and takes the English stack and tracking. The eng,
# U+014B, appears in gakuŋŋaana and is carried by the faces already in front
# of the stack, which was checked in the rendered drawing rather than assumed.
LG = dict(
    stack=SANS, track=(".04em", ".09em", ".16em"), caps="none", lift=1.0,
    out=("signal-lg.svg", "signal-lg-narrow.svg"),
    aria="Chart ya current ya motor mu kusunda omulundi gumu, nga eva mu log ya "
         "sensor. Omugugu gubeera okumpi ne 2700 mA mu ddakiika 20 ezisooka, "
         "gulinnya ng'amasavu gaku\u014b\u014baana, gutuuka okumpi ne 4700, "
         "oluvannyuma gugwa.",
    y="CURRENT YA MOTOR, mA", x="EDDAKIIKA Z'OKUSUNDA",
    run="Okusunda kuno", ideal="Enkula gye kinoonya",
    wide=[("Eddakiika 20 tewali kibaawo", 2.6, 2750, -46, "start", "lbl"),
          ("Amasavu gaku\u014b\u014baana", 19.6, 2050, 0, "end", "lbl"),
          ("OMUZIGO GWAVAAYO", 24.6, 4704, -24, "end", "lbl-s")],
    narrow=[("GWAVAAYO", 23.0, 4704, -20, "end", "lbl-s"),
            ("Tewali kintu", 1.2, 2750, -58, "start", "lbl")],
)


# German is Latin script and keeps the English stack and tracking. DER BRUCH is
# the real dairy word for the moment the emulsion inverts, not a translation of
# the English, and it happens to be exactly as long as THE BREAK, so the orange
# mark sits where it was drawn. NOCH NICHTS matches NOTHING YET to the
# character as well, which is luck rather than design.
DE = dict(
    stack=SANS, track=(".04em", ".09em", ".16em"), caps="none", lift=1.0,
    out=("signal-de.svg", "signal-de-narrow.svg"),
    aria="Diagramm des Motorstroms \u00fcber eine Butterung, aus dem Sensorlog. "
         "Die Last liegt in den ersten zwanzig Minuten nahe 2700 Milliampere, "
         "steigt, w\u00e4hrend sich das Fett sammelt, erreicht ihren H\u00f6chstwert "
         "nahe 4700 und f\u00e4llt dann ab.",
    y="MOTORSTROM, mA", x="MINUTEN DER BUTTERUNG",
    run="Dieser Durchlauf", ideal="Die gesuchte Form",
    wide=[("Zwanzig Minuten lang fast nichts", 2.6, 2750, -46, "start", "lbl"),
          ("Das Fett sammelt sich", 19.6, 2050, 0, "end", "lbl"),
          ("DER BRUCH", 24.6, 4704, -24, "end", "lbl-s")],
    narrow=[("DER BRUCH", 23.0, 4704, -20, "end", "lbl-s"),
            ("Noch nichts", 1.2, 2750, -58, "start", "lbl")],
)


# Chinese is the second script on the site after Devanagari, and it wants the
# opposite corrections. A Han character fills its em where a Latin capital
# fills about seven tenths of it, so at a matched size it reads as the larger
# of the two and the lift comes down rather than up. The tracking that opens
# up Latin capitals is left on the axis numbers, which are still Latin digits,
# and taken off everything set in Han.
#
# caps is none, and that matters here rather than being tidy. The axis titles
# are drawn with text-transform, and the current axis ends in mA, which
# uppercase would turn into MA.
ZH = dict(
    stack=SANS_ZH, track=(".04em", ".06em", ".08em"), caps="none", lift=0.94,
    out=("signal-zh.svg", "signal-zh-narrow.svg"),
    aria="\u4e00\u6b21\u6405\u62cc\u8fc7\u7a0b\u4e2d\u7684\u7535\u673a\u7535\u6d41\u66f2\u7ebf\uff0c"
         "\u6570\u636e\u6765\u81ea\u4f20\u611f\u5668\u65e5\u5fd7\u3002"
         "\u524d\u4e8c\u5341\u5206\u949f\u8d1f\u8f7d\u4fdd\u6301\u5728 2700 \u6beb\u5b89\u5de6\u53f3\uff0c"
         "\u968f\u7740\u8102\u80aa\u805a\u96c6\u800c\u4e0a\u5347\uff0c"
         "\u5728 4700 \u6beb\u5b89\u9644\u8fd1\u8fbe\u5230\u5cf0\u503c\uff0c\u7136\u540e\u56de\u843d\u3002",
    y="\u7535\u673a\u7535\u6d41\uff0cmA", x="\u6405\u62cc\u5206\u949f\u6570",
    run="\u8fd9\u4e00\u6b21", ideal="\u5b83\u8981\u627e\u7684\u5f62\u72b6",
    wide=[("\u524d\u4e8c\u5341\u5206\u949f\u51e0\u4e4e\u6ca1\u6709\u52a8\u9759", 2.6, 2750, -46, "start", "lbl"),
          ("\u8102\u80aa\u5f00\u59cb\u805a\u96c6", 19.6, 2050, 0, "end", "lbl"),
          ("\u7834\u4e73", 24.6, 4704, -24, "end", "lbl-s")],
    narrow=[("\u7834\u4e73", 23.0, 4704, -20, "end", "lbl-s"),
            ("\u8fd8\u6ca1\u6709\u52a8\u9759", 1.2, 2750, -58, "start", "lbl")],
)


# Russian is Cyrillic, which sets to the same rhythm as Latin and takes the
# stack and the tracking the English chart was drawn with. Both named faces in
# front of the stack carry Cyrillic, so nothing falls through to a different
# shape mid word. ПЕРЕЛОМ is a break and also a turning point, which is what
# the curve does, and it is shorter than THE BREAK rather than longer.
RU = dict(
    stack=SANS, track=(".04em", ".09em", ".16em"), caps="none", lift=1.0,
    out=("signal-ru.svg", "signal-ru-narrow.svg"),
    aria="График тока двигателя за одно сбивание, по данным датчика. "
         "Первые двадцать минут нагрузка держится около 2700 миллиампер, "
         "растёт по мере того как собирается жир, доходит до пика около 4700, "
         "затем падает.",
    y="ТОК ДВИГАТЕЛЯ, mA", x="МИНУТЫ СБИВАНИЯ",
    run="Этот прогон", ideal="Форма, которую оно ищет",
    wide=[("Двадцать минут почти ничего", 2.6, 2750, -46, "start", "lbl"),
          ("Жир собирается", 19.6, 2050, 0, "end", "lbl"),
          ("ПЕРЕЛОМ", 24.6, 4704, -24, "end", "lbl-s")],
    narrow=[("ПЕРЕЛОМ", 23.0, 4704, -20, "end", "lbl-s"),
            ("Пока ничего", 1.2, 2750, -58, "start", "lbl")],
)


# Spanish is Latin script and keeps the stack and tracking of the English
# chart. EL CORTE is what happens to the emulsion, se corta, and it is the
# phrase a Spanish cook already uses for a sauce that splits.
ES = dict(
    stack=SANS, track=(".04em", ".09em", ".16em"), caps="none", lift=1.0,
    out=("signal-es.svg", "signal-es-narrow.svg"),
    aria="Gráfico de la corriente del motor durante un batido, a partir del "
         "registro del sensor. La carga se mantiene cerca de 2700 "
         "miliamperios durante los primeros veinte minutos, sube a medida que "
         "la grasa se junta, llega a su pico cerca de 4700 y después cae.",
    y="CORRIENTE DEL MOTOR, mA", x="MINUTOS DE BATIDO",
    run="Esta tanda", ideal="La forma que busca",
    wide=[("Veinte minutos sin casi nada", 2.6, 2750, -46, "start", "lbl"),
          ("La grasa se junta", 19.6, 2050, 0, "end", "lbl"),
          ("EL CORTE", 24.6, 4704, -24, "end", "lbl-s")],
    narrow=[("EL CORTE", 23.0, 4704, -20, "end", "lbl-s"),
            ("Todavía nada", 1.2, 2750, -58, "start", "lbl")],
)


# Hindi is the same script as Nepali and takes the same settings. The tracking
# that opens up Latin capitals cuts the headline bar that Devanagari hangs
# from, and the script fills less of its em than a Latin capital, so it is set
# larger. मक्खन छूटा, the butter let go, is shorter on the page than THE BREAK
# was, because the matras ride above and below rather than taking width.
HI = dict(
    stack=SANS_NE, track=("0", "0", ".02em"), caps="none", lift=1.16,
    out=("signal-hi.svg", "signal-hi-narrow.svg"),
    lean=9, lean_narrow=0,
    aria="एक मथने भर मोटर करेंट का चार्ट, सेंसर लॉग से। शुरू के बीस मिनट लोड "
         "करीब 2700 मिलीएम्पियर पर रहता है, चिकनाई जमा होते जाने पर चढ़ता है, "
         "करीब 4700 पर चोटी पर पहुँचता है, और फिर गिर जाता है।",
    y="मोटर करेंट, mA", x="मथने के मिनट",
    run="यह रन", ideal="जो आकार यह ढूँढता है",
    wide=[("बीस मिनट तक कुछ खास नहीं", 2.6, 2750, -46, "start", "lbl"),
          ("चिकनाई जमा हो रही है", 19.6, 2050, 0, "end", "lbl"),
          ("मक्खन छूटा", 24.6, 4704, -24, "end", "lbl-s")],
    narrow=[("मक्खन छूटा", 23.0, 4704, -20, "end", "lbl-s"),
            ("अभी कुछ नहीं", 1.2, 2750, -58, "start", "lbl")],
)


# Turkish is Latin script and keeps the stack and tracking the English chart
# was drawn with, but it cannot let CSS do the uppercasing. Turkish has a
# dotless i whose capital is I and a dotted i whose capital is İ, and a
# renderer that does not know the text is Turkish gets the second one wrong.
# DAKİKALARI would come out DAKIKALARI. So the axis titles are written in the
# case they are meant to print in, which the whole file now does anyway.
TR = dict(
    stack=SANS, track=(".04em", ".09em", ".16em"), caps="none", lift=1.0,
    out=("signal-tr.svg", "signal-tr-narrow.svg"),
    aria="Bir yayıklama boyunca motor akımının grafiği, sensör kaydından. "
         "Yük ilk yirmi dakika boyunca 2700 miliamper civarında duruyor, "
         "yağ toplandıkça yükseliyor, 4700 yakınında zirve yapıyor, sonra "
         "düşüyor.",
    y="MOTOR AKIMI, mA", x="YAYIKLAMA DAKİKALARI",
    run="Bu çalışma", ideal="Aradığı biçim",
    wide=[("Yirmi dakika pek bir şey yok", 2.6, 2750, -46, "start", "lbl"),
          ("Yağ toplanıyor", 19.6, 2050, 0, "end", "lbl"),
          ("KOPMA", 24.6, 4704, -24, "end", "lbl-s")],
    narrow=[("KOPMA", 23.0, 4704, -20, "end", "lbl-s"),
            ("Henüz yok", 1.2, 2750, -58, "start", "lbl")],
)


# Basque is Latin script and keeps the stack and tracking of the English
# chart. HAUSTURA is the noun from hautsi, the verb Basque already uses for an
# emulsion breaking, so the chart and the prose name the same thing.
EU = dict(
    stack=SANS, track=(".04em", ".09em", ".16em"), caps="none", lift=1.0,
    out=("signal-eu.svg", "signal-eu-narrow.svg"),
    aria="Motorraren korrontearen grafikoa irabiatze batean, sentsorearen "
         "erregistrotik. Karga 2700 miliampere inguruan egoten da lehen hogei "
         "minutuetan, gantza biltzen den heinean igotzen da, 4700 inguruan "
         "jotzen du gailurra, eta gero behera egiten du.",
    y="MOTORRAREN KORRONTEA, mA", x="IRABIATZE-MINUTUAK",
    run="Saio hau", ideal="Bilatzen duen forma",
    wide=[("Hogei minutuz ezer gutxi", 2.6, 2750, -46, "start", "lbl"),
          ("Gantza biltzen", 19.6, 2050, 0, "end", "lbl"),
          ("HAUSTURA", 24.6, 4704, -24, "end", "lbl-s")],
    narrow=[("HAUSTURA", 23.0, 4704, -20, "end", "lbl-s"),
            ("Oraindik ez", 1.2, 2750, -58, "start", "lbl")],
)


# Georgian is the first script here with no capital letters at all, so there
# is nothing for the tracking that opens up Latin capitals to open and it
# comes almost off. It needs no size lift either. Measured at a matched size
# its body is 8.8px against a Latin capital's 8.5px, and its ascenders and
# descenders carry it to 11.2px, so it already reads as the larger of the two.
KA = dict(
    stack=SANS_KA, track=(".04em", ".04em", ".06em"), caps="none", lift=1.0,
    out=("signal-ka.svg", "signal-ka-narrow.svg"),
    aria="მოტორის დენის გრაფიკი ერთი დღვების განმავლობაში, სენსორის "
         "ჩანაწერიდან. დატვირთვა პირველი ოცი წუთი 2700 მილიამპერის "
         "მახლობლად რჩება, ცხიმის შეგროვებასთან ერთად ადის, პიკს 4700-თან "
         "აღწევს და მერე ეცემა.",
    y="მოტორის დენი, mA", x="დღვების წუთები",
    run="ეს პროცესი", ideal="საძიებელი ფორმა",
    wide=[("ოცი წუთი თითქმის არაფერი", 2.6, 2750, -46, "start", "lbl"),
          ("ცხიმი გროვდება", 19.6, 2050, 0, "end", "lbl"),
          ("გარდატეხა", 24.6, 4704, -24, "end", "lbl-s")],
    narrow=[("გარდატეხა", 23.0, 4704, -20, "end", "lbl-s"),
            ("ჯერ არაფერი", 1.2, 2750, -58, "start", "lbl")],
)

# Every language the chart is drawn in, in the order the site lists them.
# Bangla hangs from a headline bar the way Devanagari does, so it takes the
# Devanagari settings outright. The lift is not a guess. Measured at a matched
# size the body of a Bengali letter is 7.0px and of a Devanagari letter 7.0px,
# against a Latin capital's 8.25px, and 1.16 is what brings both up to it.
# The same `lean` applies, because the rotated axis title carries marks above
# and below the line and was touching the 4000 tick on the Nepali chart.
BN = dict(
    stack=SANS_BN, track=("0", "0", ".02em"), caps="none", lift=1.16,
    out=("signal-bn.svg", "signal-bn-narrow.svg"),
    lean=9, lean_narrow=0,
    aria="একটি মন্থন জুড়ে মোটর কারেন্টের চার্ট, সেন্সর লগ থেকে। লোড প্রথম বিশ মিনিট "
         "2700 মিলিঅ্যাম্পিয়ারের কাছে থাকে, ননী জমতে জমতে ওঠে, 4700-র কাছে চূড়ায় "
         "পৌঁছায়, তারপর পড়ে যায়।",
    y="মোটর কারেন্ট, mA", x="মন্থনের মিনিট",
    run="এই রান", ideal="যে আকার এটা খোঁজে",
    wide=[("বিশ মিনিট কিছুই হয় না", 2.6, 2750, -46, "start", "lbl"),
          ("ননী জমছে", 19.6, 2050, 0, "end", "lbl"),
          ("মাখন ছাড়ল", 24.6, 4704, -24, "end", "lbl-s")],
    narrow=[("মাখন ছাড়ল", 23.0, 4704, -20, "end", "lbl-s"),
            ("এখনও কিছু নয়", 1.2, 2750, -58, "start", "lbl")],
)

# Filipino is Latin script and keeps the stack and the tracking of the English
# chart. The first annotation writes the twenty as digits, because
# `dalawampung minuto` spelled out runs the line well past the room it has and
# a number on a chart is ordinary.
FIL = dict(
    stack=SANS, track=(".04em", ".09em", ".16em"), caps="none", lift=1.0,
    out=("signal-fil.svg", "signal-fil-narrow.svg"),
    aria="Chart ng kuryente ng motor sa isang buong pagbati, mula sa log ng "
         "sensor. Ang load ay nananatili malapit sa 2700 milliamp sa unang "
         "dalawampung minuto, umaakyat habang namumuo ang taba, umaabot sa "
         "pinakamataas na malapit sa 4700, at pagkatapos ay bumababa.",
    y="KURYENTE NG MOTOR, mA", x="MINUTO SA PAGBATI",
    run="Ang takbong ito", ideal="Ang hugis na hinahanap",
    wide=[("Walang nangyayari, 20 minuto", 2.6, 2750, -46, "start", "lbl"),
          ("Namumuo ang taba", 19.6, 2050, 0, "end", "lbl"),
          ("PAGHIWALAY", 24.6, 4704, -24, "end", "lbl-s")],
    narrow=[("PAGHIWALAY", 23.0, 4704, -20, "end", "lbl-s"),
            ("Wala pa", 1.2, 2750, -58, "start", "lbl")],
)

# Japanese takes the Chinese numbers, because kanji fill their em the way Han
# does and read as the larger of the two against a Latin capital at a matched
# size. It does not take the Chinese font stack. The two scripts share most of
# their characters and draw a number of them differently, and the ones where
# that shows are on these pages already.
JA = dict(
    stack=SANS_JA, track=(".04em", ".06em", ".08em"), caps="none", lift=0.94,
    out=("signal-ja.svg", "signal-ja-narrow.svg"),
    aria="一回の撹拌を通したモーター電流のグラフ。センサーのログから描いている。"
         "負荷は最初の二十分は 2700 ミリアンペア前後にとどまり、脂肪が集まるに"
         "つれて上がり、4700 近くで頂点に達し、そのあと落ちていく。",
    y="モーター電流、mA", x="撹拌の経過時間、分",
    run="今回の撹拌", ideal="探している形",
    wide=[("二十分はほとんど動かない", 2.6, 2750, -46, "start", "lbl"),
          ("脂肪が集まる", 19.6, 2050, 0, "end", "lbl"),
          ("バター分離", 24.6, 4704, -24, "end", "lbl-s")],
    narrow=[("バター分離", 23.0, 4704, -20, "end", "lbl-s"),
            ("まだ何も", 1.2, 2750, -58, "start", "lbl")],
)

# Cantonese takes the Han settings, and its own faces. Written Cantonese uses
# characters that a Simplified font does not reliably carry, 嘅 and 冇 and 喐
# among them, so the stack asks for Hong Kong traditional faces by name rather
# than leaning on the Chinese one.
YUE = dict(
    stack=SANS_YUE, track=(".04em", ".06em", ".08em"), caps="none", lift=0.94,
    out=("signal-yue.svg", "signal-yue-narrow.svg"),
    aria="一次攪拌入面馬達電流嘅圖，由感應器嘅紀錄嚟。頭二十分鐘負載喺 2700 "
         "毫安左右，脂肪聚埋之後就升，去到 4700 附近見頂，跟住跌返落嚟。",
    y="馬達電流，mA", x="攪咗幾分鐘",
    run="呢一次", ideal="佢要搵嘅形狀",
    wide=[("頭二十分鐘冇咩動靜", 2.6, 2750, -46, "start", "lbl"),
          ("脂肪聚埋", 19.6, 2050, 0, "end", "lbl"),
          ("散開", 24.6, 4704, -24, "end", "lbl-s")],
    narrow=[("散開", 23.0, 4704, -20, "end", "lbl-s"),
            ("仲未有動靜", 1.2, 2750, -58, "start", "lbl")],
)

# Arabic is the first chart here that reads right to left, so it is the first
# to set `iso`. Everything it supplies gets a pair of Unicode isolates and the
# anchors and coordinates below are untouched.
#
# The tracking is zero on all three, which is firmer than any other language
# on this chart. Arabic joins along the baseline, so a word is one connected
# stroke and letter spacing pulls it apart at the joints. It is the objection
# Devanagari has to tracking and a shade worse, because a broken join reads as
# a different letter rather than as loose spacing.
#
# The lift is measured rather than guessed, and it goes up where Georgian's
# went down. The body of an Arabic letter that neither rises nor descends is
# 7.5px at this size and a Latin capital is 8.0px, so 1.08 is what brings the
# two to the same reading size. The ascenders then sit above the Latin, which
# is how Arabic is supposed to look.
#
# `lean` is larger than the Devanagari 9, for the same reason it exists at
# all. The y axis title is set on its side, so what runs into the 4000 tick
# is the part of the script that hangs below the line, and Arabic hangs a
# long way below it. At 0 the title sat across the tick. 14 is where it
# comes clear. The narrow chart needs none of that, because its title starts
# 16px further out to begin with, and at 14 it was pushed clean off the canvas.
AR = dict(
    stack=SANS_AR, track=("0", "0", "0"), caps="none", lift=1.08, iso=True,
    out=("signal-ar.svg", "signal-ar-narrow.svg"),
    lean=14, lean_narrow=0,
    aria="رسم بياني لتيار المحرك خلال عملية خض واحدة، من سجل المستشعر. يستقر "
         "الحمل قرب 2700 ميلي أمبير في العشرين دقيقة الأولى، ثم يصعد مع تجمع "
         "الدهن، ويبلغ قمته قرب 4700، ثم يهبط.",
    y="تيار المحرك، mA", x="دقائق من بدء الخض",
    run="هذا التشغيل", ideal="الشكل الذي تبحث عنه",
    wide=[("لا شيء يذكر عشرين دقيقة", 2.6, 2750, -46, "start", "lbl"),
          ("الدهن يتجمع", 19.6, 2050, 0, "end", "lbl"),
          ("الانفصال", 24.6, 4704, -24, "end", "lbl-s")],
    narrow=[("الانفصال", 23.0, 4704, -20, "end", "lbl-s"),
            ("لا شيء بعد", 1.2, 2750, -58, "start", "lbl")],
)

# Newari, that is Nepal Bhasa, is a different language from a different family
# written in the same script as Nepali, so it takes the Devanagari settings
# whole. Ghee is घ्यः here and not the Nepali घिउ, which is the single thing
# about this language most worth getting right.
NEW = dict(
    stack=SANS_NE, track=("0", "0", ".02em"), caps="none", lift=1.16,
    out=("signal-new.svg", "signal-new-narrow.svg"),
    lean=9, lean_narrow=0,
    aria="छगू हे थायेज्याया मोटर करेन्टया चार्ट, सेन्सर लगपाखें। लोड न्हापांगु नी "
         "मिनेट करिब 2700 मिलिएम्पियरय् दनाच्वनी, दाः मुने ज्वीवं च्वय् वनी, करिब "
         "4700 य् थ्यनी, अले कुतुं वनी।",
    y="मोटर करेन्ट, mA", x="थायेगु ई, मिनेट",
    run="थ्व रन", ideal="मालाच्वंगु आकार",
    wide=[("नी मिनेट तक छुं मजू", 2.6, 2750, -46, "start", "lbl"),
          ("दाः मुनावन", 19.6, 2050, 0, "end", "lbl"),
          ("मख्खन पिहां वल", 24.6, 4704, -24, "end", "lbl-s")],
    narrow=[("मख्खन पिहां वल", 23.0, 4704, -20, "end", "lbl-s"),
            ("छुं मजूनि", 1.2, 2750, -58, "start", "lbl")],
)

CHARTS = [EN, NE, FR, RW, LG, DE, ZH, RU, ES, HI, TR, EU, KA,
          BN, FIL, JA, YUE, AR, NEW]

written = []
for S in CHARTS:
    wide, narrow = (os.path.join(HERE, "images", n) for n in S["out"])

    # The current axis title is set on its side, so a script with parts above
    # and below the line is wider there than Latin is, and Devanagari at its
    # lift was touching the 4000 tick. `lean` is how far that title sits from
    # the plot, and a script that needs more simply asks for more.
    lean = S.get("lean", 0)
    # The narrow chart starts its axis title 16px further out than the wide one
    # does, so a script that needs the title moved on the wide chart may need
    # it left alone here, and the narrow canvas has no room to give. Arabic is
    # the case that showed it up. It needs 14 on the wide chart to clear the
    # 4000 tick and 0 here, where 14 pushed the title off the edge entirely.
    #
    # Looking at that turned up the same fault already shipped. Every narrow
    # chart has its leftmost ink about 8px in, except the four written in a
    # script that hangs from a headline bar, where it was sitting on 0 and the
    # bar was being cut by the edge of the canvas. Those four had inherited a
    # lean that only the wide chart ever needed. They are all on 0 here now,
    # which moves the Nepali and the Hindi phone charts and is meant to.
    # Defaulting to `lean` leaves every language written before this untouched.
    lean_narrow = S.get("lean_narrow", lean)
    peak = build(
        900, 470, (74, 26, 44, 62),
        range(2000, 6001, 1000), range(0, 31, 5),
        (13, 14, 13, 11, 13), S["wide"], wide, yoff=42 + lean,
        key=(102, 66, 26), S=S)

    build(
        430, 460, (74, 14, 46, 50),
        range(2000, 6001, 2000), range(0, 31, 10),
        (14, 15, 14, 11, 14), S["narrow"], narrow, yoff=58 + lean_narrow,
        key=(100, 66, 28), S=S)

    written += [os.path.relpath(wide, HERE), os.path.relpath(narrow, HERE)]

print(f"peak median {peak[2]:.0f} mA at {peak[0]:.1f} min")
print("wrote " + ", ".join(written))
