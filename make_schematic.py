#!/usr/bin/env python3
"""Draw the wiring of The Beast, wide and narrow.

    python3 make_schematic.py

Everything here was read off the rig rather than remembered. The pin numbers,
the PWM frequency, the sample rate and the trip currents come from
bilona_ramped.py on the Pi, and the sensor address and scaling from
current_test.py. The one thing software cannot tell you is the physical order
of the fuse, the button and the sensor around the loop, and the caption on
the page says so.

The drawing has two line weights and they mean something. Thin is signal,
where nothing carries more than a few milliamps. Thick is the motor loop,
where fifteen amps is a normal afternoon. The Pi only ever touches the thin
lines.
"""

import base64
import os
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_WIDE = os.path.join(HERE, "images", "schematic.svg")
OUT_NARROW = os.path.join(HERE, "images", "schematic-narrow.svg")

INK, GOLD, DEEP = "#2a2118", "#c08a2e", "#a8681a"
CREAM, PAPER, LINE = "#f4ead7", "#fff8ec", "#e3d2b4"
FAINT, RED = "#9a836a", "#b0402c"
SANS = '"Avenir Next","Segoe UI",sans-serif'

SIG, PWR = 1.9, 6.2          # the two line weights



PARTS = os.path.join(HERE, "images", "parts")


def jpeg_size(path):
    """Width and height from the JPEG start of frame, no dependencies."""
    with open(path, "rb") as fh:
        fh.read(2)
        while True:
            b = fh.read(1)
            while b == b"\xff":
                b = fh.read(1)
            if not b:
                raise ValueError(f"no frame header in {path}")
            marker, = struct.unpack("B", b)
            length, = struct.unpack(">H", fh.read(2))
            if marker in set(range(0xC0, 0xD0)) - {0xC4, 0xC8, 0xCC}:
                h, w = struct.unpack(">HH", fh.read(5)[1:])
                return w, h
            fh.seek(length - 2, 1)


def photo(name, x, y, w):
    """Place a part photograph, sized from the file so it never distorts.

    The bytes travel inside the drawing. An SVG loaded in an img tag is not
    allowed to fetch anything, so a linked file would simply not appear.
    """
    path = os.path.join(PARTS, name)
    pw, ph = jpeg_size(path)
    with open(path, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode()
    return (f'<image x="{x}" y="{y}" width="{w}" height="{w*ph/pw:.1f}" '
            f'preserveAspectRatio="xMidYMid meet" '
            f'href="data:image/jpeg;base64,{b64}"/>')


def css(s=1.0):
    return f"""
 .grid{{stroke:{LINE};stroke-width:{0.7*s:.2f};opacity:.45}}
 .box{{fill:{PAPER};stroke:{INK};stroke-width:{2.0*s:.2f}}}
 .chip{{fill:{PAPER};stroke:{DEEP};stroke-width:{1.7*s:.2f}}}
 .sig{{fill:none;stroke:{INK};stroke-width:{SIG*s:.2f};stroke-linecap:round;stroke-linejoin:round}}
 .pwr{{fill:none;stroke:{GOLD};stroke-width:{PWR*s:.2f};stroke-linecap:round;stroke-linejoin:round}}
 .pwrk{{fill:none;stroke:{DEEP};stroke-width:{PWR*s:.2f};stroke-linecap:round;stroke-linejoin:round}}
 .ttl{{font:700 {14*s:.1f}px {SANS};fill:{INK};letter-spacing:{0.16*s:.2f}em}}
 .nm{{font:700 {15*s:.1f}px {SANS};fill:{INK};letter-spacing:{0.10*s:.2f}em}}
 .sub{{font:500 {11*s:.1f}px {SANS};fill:{FAINT};letter-spacing:{0.05*s:.2f}em}}
 .pin{{font:600 {12*s:.1f}px {SANS};fill:{DEEP};letter-spacing:{0.04*s:.2f}em}}
 .val{{font:700 {12.5*s:.1f}px {SANS};fill:{INK}}}
 .note{{font:italic 400 {11*s:.1f}px Georgia,serif;fill:{FAINT}}}
 .notek{{font:italic 400 {11*s:.1f}px Georgia,serif;fill:{DEEP}}}
 .lead{{fill:none;stroke:{FAINT};stroke-width:{0.9*s:.2f};stroke-dasharray:{2.5*s:.1f} {2.5*s:.1f}}}
 .red{{fill:none;stroke:{RED};stroke-width:{PWR*s:.2f};stroke-linecap:round}}
"""


def grid(w, h, step=26):
    out = []
    x = step
    while x < w:
        out.append(f'<line class="grid" x1="{x}" y1="0" x2="{x}" y2="{h}"/>')
        x += step
    y = step
    while y < h:
        out.append(f'<line class="grid" x1="0" y1="{y}" x2="{w}" y2="{y}"/>')
        y += step
    return "".join(out)


def block(x, y, w, h, name, sub="", cls="box", r=6):
    return (f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/>'
            f'<text class="nm" x="{x+13}" y="{y+24}">{name}</text>'
            + (f'<text class="sub" x="{x+13}" y="{y+41}">{sub}</text>' if sub else ""))


def dot(x, y, r=3.4, fill=None):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill or INK}"/>'


def estop(cx, cy, s=1.0):
    """A break in the loop with a mushroom head over it.

    Drawn as an open lever, which is the usual convention even for a switch
    that is closed in normal use, because a closed one drawn flat is
    indistinguishable from plain wire.
    """
    L, R = cx - 24 * s, cx + 24 * s
    return (f'<line class="red" x1="{L-16*s}" y1="{cy}" x2="{L}" y2="{cy}"/>'
            f'<line class="red" x1="{R}" y1="{cy}" x2="{R+16*s}" y2="{cy}"/>'
            f'<line x1="{L}" y1="{cy}" x2="{cx+13*s}" y2="{cy-19*s}" stroke="{RED}" '
            f'stroke-width="{3.0*s:.2f}" stroke-linecap="round"/>'
            f'<line x1="{cx-5*s}" y1="{cy-11*s}" x2="{cx-5*s}" y2="{cy-33*s}" stroke="{RED}" '
            f'stroke-width="{2.6*s:.2f}"/>'
            f'<rect x="{cx-24*s}" y="{cy-46*s}" width="{38*s}" height="{13*s}" rx="{6.5*s}" '
            f'fill="{RED}"/>'
            + dot(L, cy, 3.6 * s, RED) + dot(R, cy, 3.6 * s, RED))


def estop_v(cx, cy, s=1.0):
    """The same break, drawn for a vertical run. The head is left off here
    because at phone size it turns into a blob and the label does the work."""
    T, B = cy - 22 * s, cy + 22 * s
    return (f'<line class="red" x1="{cx}" y1="{T-18*s}" x2="{cx}" y2="{T}"/>'
            f'<line class="red" x1="{cx}" y1="{B}" x2="{cx}" y2="{B+18*s}"/>'
            f'<line x1="{cx}" y1="{B}" x2="{cx+21*s}" y2="{T+6*s}" stroke="{RED}" '
            f'stroke-width="{3.2*s:.2f}" stroke-linecap="round"/>'
            + dot(cx, T, 4.0 * s, RED) + dot(cx, B, 4.0 * s, RED))


def fuse(cx, cy, s=1.0):
    return (f'<rect x="{cx-17*s}" y="{cy-8*s}" width="{34*s}" height="{16*s}" rx="{3*s}" '
            f'fill="{PAPER}" stroke="{DEEP}" stroke-width="{1.8*s:.2f}"/>'
            f'<line x1="{cx-17*s}" y1="{cy}" x2="{cx+17*s}" y2="{cy}" stroke="{DEEP}" '
            f'stroke-width="{1.6*s:.2f}"/>')


def battery(x, y, s=1.0):
    """Cells drawn long-short, long plate is the positive terminal."""
    o = []
    for i, (dx, hh) in enumerate(((0, 20), (9, 10), (18, 20), (27, 10))):
        o.append(f'<line x1="{x+dx*s}" y1="{y-hh*s}" x2="{x+dx*s}" y2="{y+hh*s}" '
                 f'stroke="{GOLD}" stroke-width="{(3.4 if hh > 15 else 2.4)*s:.2f}" stroke-linecap="round"/>')
    return "".join(o)


def motor(cx, cy, r, s=1.0):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{PAPER}" stroke="{GOLD}" '
            f'stroke-width="{PWR*s:.2f}"/>'
            f'<text class="nm" x="{cx}" y="{cy+5*s}" text-anchor="middle">M</text>')


def note(x, y, lines, cls="note", anchor="start", lh=15):
    return "".join(f'<text class="{cls}" x="{x}" y="{y+i*lh}" text-anchor="{anchor}">{t}</text>'
                   for i, t in enumerate(lines))


def supply(x, y, w, h, s=1.0, mains_left=True):
    """The 12 V open frame switch mode supply, and its lead to the wall."""
    o = [f'<rect class="box" x="{x}" y="{y}" width="{w}" height="{h}" rx="5"/>',
         f'<text class="nm" x="{x+12}" y="{y+27}">12 V SUPPLY</text>']
    for i in range(7):
        vx = x + 14 + i * 9
        o.append(f'<line x1="{vx}" y1="{y+h-30}" x2="{vx}" y2="{y+h-9}" stroke="{LINE}" '
                 f'stroke-width="{1.4*s:.2f}"/>')
    if mains_left:
        o.append(f'<line class="sig" x1="{x-54*s}" y1="{y+h/2}" x2="{x}" y2="{y+h/2}"/>')
        o.append(f'<text class="sub" x="{x-27*s}" y="{y+h/2-9}" text-anchor="middle">MAINS</text>')
    return "".join(o)


def wide():
    """Symbols, names and values, and a photograph of each board."""
    W, H = 1120, 740
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Circuit diagram of the ghee rig. A Raspberry Pi drives a BTS7960 H-bridge '
         f'over four signal wires and reads an INA260 current sensor over I2C. A 12 volt supply, a '
         f'15 amp fuse, the emergency stop button and the sensor sit in series in the motor loop, '
         f'which the Pi never touches.">',
         f'<rect width="{W}" height="{H}" fill="{CREAM}"/>',
         f'<style>{css()}</style>', f'<g>{grid(W, H, 24)}</g>']

    PI = (60, 88, 210, 204)
    HB = (600, 88, 240, 204)
    o.append(block(*PI, "RASPBERRY PI 3"))
    o.append(photo("pi.jpg", 78, 128, 174))
    o.append(block(*HB, "BTS7960 H-BRIDGE"))
    o.append(photo("bts.jpg", 645, 128, 150))

    px, hx = PI[0] + PI[2], HB[0]
    for i, (gpio, fn, val) in enumerate((("GPIO 18", "RPWM", "1 kHz"), ("GPIO 19", "LPWM", "1 kHz"),
                                         ("GPIO 23", "R_EN", ""), ("GPIO 24", "L_EN", ""))):
        y = 138 + i * 35
        o.append(f'<line class="sig" x1="{px}" y1="{y}" x2="{hx}" y2="{y}"/>')
        o.append(dot(px, y) + dot(hx, y))
        o.append(f'<text class="pin" x="{px+12}" y="{y-9}">{gpio}</text>')
        o.append(f'<text class="pin" x="{hx-12}" y="{y-9}" text-anchor="end">{fn}</text>')
        if val:
            o.append(f'<text class="sub" x="{(px+hx)/2}" y="{y-9}" text-anchor="middle">{val}</text>')

    o.append(motor(960, 190, 52))
    for y in (172, 208):
        o.append(f'<line class="pwr" x1="{HB[0]+HB[2]}" y1="{y}" x2="911" y2="{y}"/>')
    o.append(f'<text class="pin" x="{HB[0]+HB[2]+10}" y="164">M+</text>')
    o.append(f'<text class="pin" x="{HB[0]+HB[2]+10}" y="228">M&#8722;</text>')
    o.append('<text class="sub" x="960" y="266" text-anchor="middle">DRILL</text>')

    RAIL, RET = 480, 620
    INA = (430, 406, 250, 148)
    PSU = (76, 445, 132, 70)
    BPX, BMX = 706, 776
    ES, FU = 350, 262
    SDA_X, SCL_X = 470, 506
    PB = PI[1] + PI[3]

    o.append(f'<path class="sig" d="M186,{PB} L186,356 L{SDA_X},356 L{SDA_X},{INA[1]}"/>')
    o.append(f'<path class="sig" d="M214,{PB} L214,336 L{SCL_X},336 L{SCL_X},{INA[1]}"/>')
    o.append(dot(186, PB) + dot(214, PB))
    o.append(f'<text class="pin" x="178" y="{PB+24}" text-anchor="end">I2C</text>')
    o.append(f'<text class="pin" x="{SDA_X+9}" y="392">SDA</text>')
    o.append(f'<text class="pin" x="{SCL_X+9}" y="372">SCL</text>')

    o.append(f'<rect class="chip" x="{INA[0]}" y="{INA[1]}" width="{INA[2]}" '
             f'height="{INA[3]}" rx="6"/>')
    o.append(f'<text class="nm" x="{INA[0]+14}" y="{INA[1]+27}">INA260</text>')
    o.append(f'<text class="sub" x="{INA[0]+14}" y="{INA[1]+45}">0x40</text>')
    o.append(photo("ina.jpg", 566, 432, 96))
    o.append(f'<text class="pin" x="{INA[0]-10}" y="{RAIL-12}" text-anchor="end">IN+</text>')
    o.append(f'<text class="pin" x="{INA[0]+INA[2]+10}" y="{RAIL-12}">IN&#8722;</text>')

    o.append(supply(*PSU))
    PR = PSU[0] + PSU[2]
    o.append(f'<text class="val" x="{PR+11}" y="{PSU[1]+14}">+</text>')
    o.append(f'<text class="val" x="{PR+11}" y="{PSU[1]+68}">&#8722;</text>')
    o.append(f'<path class="pwr" d="M{PR},{PSU[1]+18} L240,{PSU[1]+18} L240,{RAIL} L{ES-24},{RAIL}"/>')
    o.append(f'<path class="pwr" d="M{ES+24},{RAIL} L{INA[0]},{RAIL}"/>')
    o.append(f'<path class="pwr" d="M{INA[0]+INA[2]},{RAIL} L{BPX},{RAIL} L{BPX},{HB[1]+HB[3]}"/>')
    o.append(f'<path class="pwr" d="M{BMX},{HB[1]+HB[3]} L{BMX},{RET} L240,{RET} '
             f'L240,{PSU[1]+52} L{PR},{PSU[1]+52}"/>')
    o.append(f'<text class="pin" x="{BPX-10}" y="{HB[1]+HB[3]+24}" text-anchor="end">B+</text>')
    o.append(f'<text class="pin" x="{BMX+10}" y="{HB[1]+HB[3]+24}">B&#8722;</text>')

    o.append(fuse(FU, RAIL))
    o.append(f'<text class="val" x="{FU}" y="{RAIL-21}" text-anchor="middle">15 A</text>')
    o.append(estop(ES, RAIL))
    o.append(f'<text class="pin" x="{ES}" y="{RAIL-60}" text-anchor="middle">EMERGENCY STOP</text>')

    o.append('<line class="sig" x1="62" y1="48" x2="98" y2="48"/>')
    o.append('<text class="sub" x="106" y="52">SIGNAL</text>')
    o.append('<line class="pwr" x1="200" y1="48" x2="236" y2="48"/>')
    o.append('<text class="sub" x="244" y="52">MOTOR LOOP</text>')

    tb = (900, 640, 190, 58)
    o.append(f'<rect x="{tb[0]}" y="{tb[1]}" width="{tb[2]}" height="{tb[3]}" rx="4" '
             f'fill="none" stroke="{FAINT}" stroke-width="1"/>')
    o.append(f'<line x1="{tb[0]}" y1="{tb[1]+26}" x2="{tb[0]+tb[2]}" y2="{tb[1]+26}" '
             f'stroke="{FAINT}" stroke-width="1"/>')
    o.append(f'<text class="ttl" x="{tb[0]+11}" y="{tb[1]+18}">THE BEAST</text>')
    o.append(f'<text class="sub" x="{tb[0]+11}" y="{tb[1]+44}">POWER AND SENSE</text>')
    o.append("</svg>")
    return "".join(o)


def narrow():
    """The same circuit as one vertical chain, which is how a phone reads it."""
    W, H = 460, 900
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Circuit diagram of the ghee rig. A Raspberry Pi drives a BTS7960 H-bridge '
         f'over four signal wires and reads an INA260 current sensor over I2C. A 12 volt supply, a '
         f'15 amp fuse, the emergency stop button and the sensor sit in series in the motor loop, '
         f'which the Pi never touches.">',
         f'<rect width="{W}" height="{H}" fill="{CREAM}"/>',
         f'<style>{css(1.18)}</style>', f'<g>{grid(W, H, 22)}</g>']

    o.append('<line class="sig" x1="26" y1="28" x2="58" y2="28"/>')
    o.append('<text class="sub" x="66" y="32">SIGNAL</text>')
    o.append('<line class="pwr" x1="182" y1="28" x2="214" y2="28"/>')
    o.append('<text class="sub" x="222" y="32">MOTOR LOOP</text>')

    PI = (26, 56, 408, 118)
    HB = (62, 300, 298, 122)
    PB = PI[1] + PI[3]
    o.append(f'<rect class="box" x="{PI[0]}" y="{PI[1]}" width="{PI[2]}" height="{PI[3]}" rx="6"/>')
    o.append(photo("pi.jpg", 42, 74, 104))
    o.append(f'<text class="nm" x="166" y="{PI[1]+66}">RASPBERRY PI 3</text>')

    for i, (gpio, fn) in enumerate((("GPIO 18", "RPWM &#183; 1 kHz"), ("GPIO 19", "LPWM &#183; 1 kHz"),
                                    ("GPIO 23", "R_EN"), ("GPIO 24", "L_EN"))):
        x = 112 + i * 68
        mid = (PB + HB[1]) / 2
        o.append(f'<line class="sig" x1="{x}" y1="{PB}" x2="{x}" y2="{HB[1]}"/>')
        o.append(dot(x, PB, 4) + dot(x, HB[1], 4))
        o.append(f'<text class="pin" x="{x-8}" y="{mid}" text-anchor="middle" '
                 f'transform="rotate(-90 {x-8} {mid})">{gpio}</text>')
        o.append(f'<text class="sub" x="{x+11}" y="{mid}" text-anchor="middle" '
                 f'transform="rotate(-90 {x+11} {mid})">{fn}</text>')

    o.append(f'<rect class="box" x="{HB[0]}" y="{HB[1]}" width="{HB[2]}" height="{HB[3]}" rx="6"/>')
    o.append(f'<text class="nm" x="{HB[0]+14}" y="{HB[1]+28}">BTS7960</text>')
    o.append(f'<text class="sub" x="{HB[0]+14}" y="{HB[1]+46}">H-BRIDGE</text>')
    o.append(photo("bts.jpg", 262, 316, 84))

    o.append(motor(412, 345, 31, 1.18))
    for y in (332, 358):
        o.append(f'<line class="pwr" x1="{HB[0]+HB[2]}" y1="{y}" x2="382" y2="{y}"/>')
    o.append('<text class="sub" x="412" y="396" text-anchor="middle">DRILL</text>')

    CH, RTX, RET = 112, 332, 866
    INA = (62, 470, 232, 124)
    o.append(f'<line class="pwr" x1="{CH}" y1="{HB[1]+HB[3]}" x2="{CH}" y2="{INA[1]}"/>')
    o.append(f'<text class="pin" x="{CH+11}" y="{HB[1]+HB[3]+24}">B+</text>')

    o.append(f'<path class="sig" d="M42,{PB} L42,492 L{INA[0]},492"/>')
    o.append(f'<path class="sig" d="M56,{PB} L56,516 L{INA[0]},516"/>')
    o.append(dot(42, PB, 4) + dot(56, PB, 4))
    o.append('<text class="pin" x="26" y="300" text-anchor="middle" '
             'transform="rotate(-90 26 300)">I2C &#183; SDA &#183; SCL</text>')

    o.append(f'<rect class="chip" x="{INA[0]}" y="{INA[1]}" width="{INA[2]}" '
             f'height="{INA[3]}" rx="6"/>')
    o.append(f'<text class="nm" x="{INA[0]+14}" y="{INA[1]+28}">INA260</text>')
    o.append(f'<text class="sub" x="{INA[0]+14}" y="{INA[1]+46}">0x40</text>')
    o.append(photo("ina.jpg", 202, 500, 78))
    o.append(f'<text class="pin" x="{CH+11}" y="{INA[1]+INA[3]+22}">IN+</text>')

    o.append(f'<line class="pwr" x1="{CH}" y1="{INA[1]+INA[3]}" x2="{CH}" y2="616"/>')
    o.append(estop_v(CH, 640, 1.18))
    o.append(f'<text class="pin" x="{CH+46}" y="636">EMERGENCY</text>')
    o.append(f'<text class="pin" x="{CH+46}" y="654">STOP</text>')
    o.append(f'<line class="pwr" x1="{CH}" y1="672" x2="{CH}" y2="704"/>')
    o.append(f'<g transform="rotate(90 {CH} 722)">{fuse(CH, 722, 1.18)}</g>')
    o.append(f'<text class="val" x="{CH+32}" y="726">15 A</text>')
    o.append(f'<line class="pwr" x1="{CH}" y1="740" x2="{CH}" y2="760"/>')

    PSU = (58, 760, 176, 70)
    o.append(supply(*PSU, s=1.18, mains_left=False))
    o.append(f'<line class="sig" x1="{PSU[0]+PSU[2]}" y1="{PSU[1]+42}" '
             f'x2="{PSU[0]+PSU[2]+34}" y2="{PSU[1]+42}"/>')
    o.append(f'<text class="sub" x="{PSU[0]+PSU[2]+38}" y="{PSU[1]+46}">MAINS</text>')
    o.append(f'<text class="val" x="{CH+13}" y="{PSU[1]-8}">+</text>')
    o.append(f'<text class="val" x="{CH+13}" y="{PSU[1]+PSU[3]+22}">&#8722;</text>')
    o.append(f'<path class="pwr" d="M{CH},{PSU[1]+PSU[3]} L{CH},{RET} L{RTX},{RET} '
             f'L{RTX},{HB[1]+HB[3]}"/>')
    o.append(f'<text class="pin" x="{RTX+11}" y="{HB[1]+HB[3]+24}">B&#8722;</text>')
    o.append("</svg>")
    return "".join(o)


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "images"), exist_ok=True)
    for path, svg in ((OUT_WIDE, wide()), (OUT_NARROW, narrow())):
        with open(path, "w") as fh:
            fh.write(svg)
        print("wrote", os.path.relpath(path, HERE))
