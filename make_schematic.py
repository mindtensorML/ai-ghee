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

import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_WIDE = os.path.join(HERE, "images", "schematic.svg")
OUT_NARROW = os.path.join(HERE, "images", "schematic-narrow.svg")

INK, GOLD, DEEP = "#2a2118", "#c08a2e", "#a8681a"
CREAM, PAPER, LINE = "#f4ead7", "#fff8ec", "#e3d2b4"
FAINT, RED = "#9a836a", "#b0402c"
SANS = '"Avenir Next","Segoe UI",sans-serif'

SIG, PWR = 1.9, 6.2          # the two line weights


def css(s=1.0):
    return f"""
 .grid{{stroke:{LINE};stroke-width:{0.7*s:.2f};opacity:.45}}
 .box{{fill:{PAPER};stroke:{INK};stroke-width:{2.0*s:.2f}}}
 .chip{{fill:{PAPER};stroke:{DEEP};stroke-width:{1.7*s:.2f}}}
 .sig{{fill:none;stroke:{INK};stroke-width:{SIG*s:.2f};stroke-linecap:round;stroke-linejoin:round}}
 .pwr{{fill:none;stroke:{GOLD};stroke-width:{PWR*s:.2f};stroke-linecap:round;stroke-linejoin:round}}
 .pwrk{{fill:none;stroke:{DEEP};stroke-width:{PWR*s:.2f};stroke-linecap:round;stroke-linejoin:round}}
 .ttl{{font:700 {13*s:.1f}px {SANS};fill:{INK};letter-spacing:{0.16*s:.2f}em}}
 .nm{{font:700 {12*s:.1f}px {SANS};fill:{INK};letter-spacing:{0.10*s:.2f}em}}
 .sub{{font:400 {10*s:.1f}px {SANS};fill:{FAINT};letter-spacing:{0.05*s:.2f}em}}
 .pin{{font:600 {10.5*s:.1f}px {SANS};fill:{DEEP};letter-spacing:{0.04*s:.2f}em}}
 .val{{font:600 {10.5*s:.1f}px {SANS};fill:{INK}}}
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
         f'<text class="nm" x="{x+12}" y="{y+24}">12 V SUPPLY</text>',
         f'<text class="sub" x="{x+12}" y="{y+41}">switch mode, off the wall</text>']
    for i in range(4):
        vx = x + w - 16 - i * 9
        o.append(f'<line x1="{vx}" y1="{y+10}" x2="{vx}" y2="{y+h-10}" stroke="{LINE}" '
                 f'stroke-width="{1.4*s:.2f}"/>')
    if mains_left:
        o.append(f'<line class="sig" x1="{x-36*s}" y1="{y+h/2}" x2="{x}" y2="{y+h/2}"/>')
        o.append(f'<text class="sub" x="{x-18*s}" y="{y+h/2-8}" text-anchor="middle">MAINS</text>')
    return "".join(o)


def wide():
    W, H = 1060, 812
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Wiring of the ghee rig. A Raspberry Pi drives a BTS7960 H-bridge over four '
         f'signal wires and reads an INA260 current sensor over I2C. A 12 volt supply, a 15 amp fuse, '
         f'the emergency stop button and the sensor sit in series in the motor loop, which the Pi '
         f'never touches.">',
         f'<rect width="{W}" height="{H}" fill="{CREAM}"/>',
         f'<style>{css()}</style>', f'<g>{grid(W, H)}</g>']

    PI = (62, 92, 208, 206)
    HB = (596, 92, 226, 206)
    o.append(block(*PI, "RASPBERRY PI 3", "gpiozero, 50 Hz control loop"))
    o.append(block(*HB, "BTS7960 H-BRIDGE", "two half bridges, 12 V motor side"))

    px, hx = PI[0] + PI[2], HB[0]
    for i, (gpio, fn, extra) in enumerate((
            ("GPIO 18", "RPWM", "1 kHz"), ("GPIO 19", "LPWM", "1 kHz"),
            ("GPIO 23", "R_EN", "held high"), ("GPIO 24", "L_EN", "held high"))):
        y = 132 + i * 40
        o.append(f'<line class="sig" x1="{px}" y1="{y}" x2="{hx}" y2="{y}"/>')
        o.append(dot(px, y) + dot(hx, y))
        o.append(f'<text class="pin" x="{px+12}" y="{y-8}">{gpio}</text>')
        o.append(f'<text class="pin" x="{hx-12}" y="{y-8}" text-anchor="end">{fn}</text>')
        o.append(f'<text class="sub" x="{(px+hx)/2}" y="{y+16}" text-anchor="middle">{extra}</text>')

    o.append(motor(930, 195, 52))
    for y in (175, 215):
        o.append(f'<line class="pwr" x1="{HB[0]+HB[2]}" y1="{y}" x2="882" y2="{y}"/>')
    o.append(f'<text class="pin" x="{HB[0]+HB[2]+10}" y="168">M+</text>')
    o.append(f'<text class="pin" x="{HB[0]+HB[2]+10}" y="236">M&#8722;</text>')
    o.append('<text class="sub" x="930" y="272" text-anchor="middle">CORDLESS DRILL</text>')

    RAIL, RET = 520, 706
    INA = (476, 482, 200, 78)
    PSU = (62, 560, 152, 74)
    BPX, BMX = 716, 800
    ES, FU = 400, 310
    SDA_X, SCL_X = 520, 556

    o.append(f'<path class="sig" d="M200,{PI[1]+PI[3]} L200,392 L{SDA_X},392 L{SDA_X},{INA[1]}"/>')
    o.append(f'<path class="sig" d="M232,{PI[1]+PI[3]} L232,368 L{SCL_X},368 L{SCL_X},{INA[1]}"/>')
    o.append(dot(200, PI[1] + PI[3]) + dot(232, PI[1] + PI[3]))
    o.append('<text class="pin" x="192" y="322" text-anchor="end">GPIO 2 &#183; 3</text>')
    o.append('<text class="sub" x="192" y="340" text-anchor="end">I2C BUS 1</text>')
    o.append(f'<text class="pin" x="{SDA_X+8}" y="440">SDA</text>')
    o.append(f'<text class="pin" x="{SCL_X+8}" y="418">SCL</text>')

    o.append(block(*INA, "INA260", "0x40 &#183; 1.25 mA a bit", cls="chip"))
    o.append(f'<text class="pin" x="{INA[0]-10}" y="{RAIL-11}" text-anchor="end">IN+</text>')
    o.append(f'<text class="pin" x="{INA[0]+INA[2]+10}" y="{RAIL-11}">IN&#8722;</text>')

    o.append(supply(*PSU))
    PR = PSU[0] + PSU[2]
    o.append(f'<text class="val" x="{PR+10}" y="{PSU[1]+12}">+</text>')
    o.append(f'<text class="val" x="{PR+10}" y="{PSU[1]+74}">&#8722;</text>')
    o.append(f'<path class="pwr" d="M{PR},{PSU[1]+20} L246,{PSU[1]+20} L246,{RAIL} L{ES-24},{RAIL}"/>')
    o.append(f'<path class="pwr" d="M{ES+24},{RAIL} L{INA[0]},{RAIL}"/>')
    o.append(f'<path class="pwr" d="M{INA[0]+INA[2]},{RAIL} L{BPX},{RAIL} L{BPX},{HB[1]+HB[3]}"/>')
    o.append(f'<path class="pwr" d="M{BMX},{HB[1]+HB[3]} L{BMX},{RET} L246,{RET} '
             f'L246,{PSU[1]+56} L{PR},{PSU[1]+56}"/>')
    o.append(f'<text class="pin" x="{BPX-10}" y="{HB[1]+HB[3]+22}" text-anchor="end">B+</text>')
    o.append(f'<text class="pin" x="{BMX+10}" y="{HB[1]+HB[3]+22}">B&#8722;</text>')

    o.append(fuse(FU, RAIL))
    o.append(f'<text class="val" x="{FU}" y="{RAIL-20}" text-anchor="middle">15 A</text>')
    o.append(estop(ES, RAIL))
    o.append(f'<text class="pin" x="{ES}" y="{RAIL-58}" text-anchor="middle">EMERGENCY STOP</text>')

    o.append(note(272, 326, [
        "Four wires, and not one of them carries the motor.",
        "The Pi says how hard and which way. It never",
        "touches the current it is asking for."]))
    o.append(note(834, 336, [
        "Only one PWM is ever above",
        "zero, and every reversal passes",
        "through zero on the way, so the",
        "two halves can never both be on."]))
    o.append(note(834, 500, [
        "Read once a second. Its logic",
        "side runs off the Pi, so it still",
        "answers with the supply off."]))
    o.append(note(452, 574, [
        "Nothing runs from this button to the Pi. It breaks the loop",
        "itself. The rig works out that it is open by asking for 30 per",
        "cent and getting less than 200 mA back."], cls="notek", anchor="middle"))
    o.append(f'<path class="lead" d="M{ES},{RAIL+16} L{ES},554 L452,554"/>')
    o.append(note(596, 58, ["8 A held for three seconds and the software lets go.",
                            "The fuse is for everything software cannot catch."]))

    o.append('<line class="sig" x1="66" y1="52" x2="106" y2="52"/>')
    o.append('<text class="sub" x="114" y="56">SIGNAL, MILLIAMPS</text>')
    o.append('<line class="pwr" x1="66" y1="74" x2="106" y2="74"/>')
    o.append('<text class="sub" x="114" y="78">MOTOR LOOP, AMPS</text>')

    tb = (798, 724, 200, 62)
    o.append(f'<rect x="{tb[0]}" y="{tb[1]}" width="{tb[2]}" height="{tb[3]}" rx="4" '
             f'fill="none" stroke="{FAINT}" stroke-width="1"/>')
    o.append(f'<line x1="{tb[0]}" y1="{tb[1]+26}" x2="{tb[0]+tb[2]}" y2="{tb[1]+26}" '
             f'stroke="{FAINT}" stroke-width="1"/>')
    o.append(f'<text class="ttl" x="{tb[0]+11}" y="{tb[1]+18}">THE BEAST</text>')
    o.append(f'<text class="sub" x="{tb[0]+11}" y="{tb[1]+42}">POWER AND SENSE</text>')
    o.append(f'<text class="sub" x="{tb[0]+11}" y="{tb[1]+56}">READ FROM THE RIG</text>')

    o.append("</svg>")
    return "".join(o)


def narrow():
    """The same circuit as one vertical chain, which is how a phone reads it."""
    W, H = 460, 906
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Wiring of the ghee rig. A Raspberry Pi drives a BTS7960 H-bridge over four '
         f'signal wires and reads an INA260 current sensor over I2C. A 12 volt supply, a 15 amp fuse, '
         f'the emergency stop button and the sensor sit in series in the motor loop, which the Pi '
         f'never touches.">',
         f'<rect width="{W}" height="{H}" fill="{CREAM}"/>',
         f'<style>{css(1.18)}</style>', f'<g>{grid(W, H, 22)}</g>']

    o.append('<line class="sig" x1="26" y1="30" x2="58" y2="30"/>')
    o.append('<text class="sub" x="66" y="34">SIGNAL</text>')
    o.append('<line class="pwr" x1="182" y1="30" x2="214" y2="30"/>')
    o.append('<text class="sub" x="222" y="34">MOTOR LOOP</text>')

    PI = (26, 64, 408, 78)
    HB = (62, 292, 298, 78)
    PB = PI[1] + PI[3]
    o.append(block(*PI, "RASPBERRY PI 3", "gpiozero, 50 Hz loop"))
    o.append(block(*HB, "BTS7960 H-BRIDGE", "two half bridges"))

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

    o.append(motor(412, 331, 31, 1.18))
    for y in (318, 344):
        o.append(f'<line class="pwr" x1="{HB[0]+HB[2]}" y1="{y}" x2="381" y2="{y}"/>')
    o.append('<text class="sub" x="412" y="382" text-anchor="middle">DRILL</text>')

    CH, RTX, RET = 112, 332, 800
    INA = (62, 410, 232, 74)

    # I2C runs down the far left, outside everything, so it crosses nothing
    o.append(f'<path class="sig" d="M42,{PB} L42,432 L{INA[0]},432"/>')
    o.append(f'<path class="sig" d="M56,{PB} L56,456 L{INA[0]},456"/>')
    o.append(dot(42, PB, 4) + dot(56, PB, 4))
    o.append('<text class="pin" x="26" y="292" text-anchor="middle" '
             'transform="rotate(-90 26 292)">I2C &#183; SDA &#183; SCL</text>')

    o.append(f'<line class="pwr" x1="{CH}" y1="{HB[1]+HB[3]}" x2="{CH}" y2="{INA[1]}"/>')
    o.append(f'<text class="pin" x="{CH+11}" y="{HB[1]+HB[3]+24}">B+</text>')
    o.append(block(*INA, "INA260", "0x40 &#183; read once a second", cls="chip"))
    o.append(f'<text class="pin" x="{CH+11}" y="{INA[1]+INA[3]+22}">IN+</text>')

    o.append(f'<line class="pwr" x1="{CH}" y1="{INA[1]+INA[3]}" x2="{CH}" y2="528"/>')
    o.append(estop_v(CH, 560, 1.18))
    o.append(f'<text class="pin" x="{CH+46}" y="556">EMERGENCY</text>')
    o.append(f'<text class="pin" x="{CH+46}" y="574">STOP</text>')
    o.append(f'<line class="pwr" x1="{CH}" y1="592" x2="{CH}" y2="638"/>')
    o.append(f'<g transform="rotate(90 {CH} 656)">{fuse(CH, 656, 1.18)}</g>')
    o.append(f'<text class="val" x="{CH+32}" y="660">15 A</text>')
    o.append(f'<line class="pwr" x1="{CH}" y1="674" x2="{CH}" y2="700"/>')

    PSU = (58, 700, 176, 70)
    o.append(supply(*PSU, s=1.18, mains_left=False))
    o.append(f'<line class="sig" x1="{PSU[0]+PSU[2]}" y1="{PSU[1]+42}" x2="{PSU[0]+PSU[2]+34}" y2="{PSU[1]+42}"/>')
    o.append(f'<text class="sub" x="{PSU[0]+PSU[2]+38}" y="{PSU[1]+46}">MAINS</text>')
    o.append(f'<text class="val" x="{CH+13}" y="{PSU[1]-8}">+</text>')
    o.append(f'<text class="val" x="{CH+13}" y="{PSU[1]+PSU[3]+22}">&#8722;</text>')
    o.append(f'<path class="pwr" d="M{CH},{PSU[1]+PSU[3]} L{CH},{RET} L{RTX},{RET} L{RTX},{HB[1]+HB[3]}"/>')
    o.append(f'<text class="pin" x="{RTX+11}" y="{HB[1]+HB[3]+24}">B&#8722;</text>')

    o.append(note(230, 842, [
        "Nothing runs from that button to the Pi. It breaks the",
        "loop itself. The rig works out it is open by asking for",
        "30 per cent and getting less than 200 mA back."],
        cls="notek", anchor="middle", lh=18))
    o.append("</svg>")
    return "".join(o)


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "images"), exist_ok=True)
    for path, svg in ((OUT_WIDE, wide()), (OUT_NARROW, narrow())):
        with open(path, "w") as fh:
            fh.write(svg)
        print("wrote", os.path.relpath(path, HERE))
