#!/usr/bin/env python3
"""Generate eval inputs for logo-coach: deliberately flawed SVG logos, one decent one, and 'sketch photo' PNGs.

Writes into evals/files/ next to this script:  python evals/make_fixtures.py Renders PNGs with the skill's render_png.py (Chrome backend).
"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
OUT = os.path.join(HERE, "files")
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import render_png  # noqa: E402

os.makedirs(OUT, exist_ok=True)


def write(name, svg):
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(svg)
    return p


# 1. Coffee roaster — clichés (cup + steam + bean), 5 colours + gradient, hairline steam, off-angle diagonal
#    (the "roast" diagonal runs at 43.5° instead of 45°), live <text>, tiny sparkle dots, not centred.
coffee = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8B5A2B"/><stop offset="1" stop-color="#3E2413"/></linearGradient></defs>
<path d="M58 118 L178 118 L168 206 Q166 218 154 218 L82 218 Q70 218 68 206 Z" fill="url(#g)"/>
<path d="M178 136 Q206 138 204 160 Q202 184 172 186" fill="none" stroke="#3E2413" stroke-width="7"/>
<path d="M86 104 Q76 88 88 74 Q100 60 90 44" fill="none" stroke="#C8B6A6" stroke-width="1.2"/>
<path d="M118 104 Q108 86 120 72 Q132 58 122 40" fill="none" stroke="#C8B6A6" stroke-width="1.2"/>
<path d="M150 104 Q140 88 152 74 Q164 60 154 44" fill="none" stroke="#C8B6A6" stroke-width="1.2"/>
<path d="M72 196 L172 101 L172 117 L88 196 Z" fill="#E4A33A"/>
<ellipse cx="208" cy="62" rx="20" ry="28" fill="#5B3A1E" transform="rotate(30 208 62)"/>
<path d="M200 40 Q214 62 214 84" fill="none" stroke="#E9DCC9" stroke-width="2"/>
<circle cx="40" cy="60" r="1.6" fill="#E4A33A"/><circle cx="46" cy="70" r="1.1" fill="#E4A33A"/><circle cx="34" cy="74" r="0.9" fill="#E4A33A"/>
<text x="118" y="246" text-anchor="middle" font-family="Georgia, serif" font-size="22" fill="#3E2413">EMBER &amp; OAK</text>
</svg>
"""
write("coffee-roaster-flawed.svg", coffee)

# 2. Fitness app — too many colours (6), swoosh cliché, fine detail that dies at 16 px, lopsided mass
fitness = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
<circle cx="128" cy="128" r="104" fill="#1E88E5"/>
<path d="M44 150 Q120 80 214 96 Q140 104 60 170 Z" fill="#FF7043"/>
<path d="M52 170 Q130 118 212 118 Q150 128 70 186 Z" fill="#FFCA28"/>
<path d="M150 58 L176 58 L160 92 L184 92 L136 150 L150 106 L128 106 Z" fill="#66BB6A"/>
<circle cx="96" cy="90" r="12" fill="#AB47BC"/>
<path d="M60 206 L200 206" stroke="#FFFFFF" stroke-width="1"/>
<path d="M70 214 L190 214" stroke="#FFFFFF" stroke-width="0.8"/>
<circle cx="200" cy="60" r="2" fill="#EC407A"/><circle cx="210" cy="70" r="1.5" fill="#EC407A"/>
</svg>
"""
write("fitness-app-flawed.svg", fitness)

# 3. A reasonably good one — "Harbor" savings app: an H whose crossbar is a calm water line, built on a grid,
#    one colour, real counters, clean 90° geometry, survives 16 px.
good = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><title>Harbor symbol</title>
<path fill-rule="evenodd" fill="#0F3D4C" d="M48 40 H96 V112 Q112 100 128 112 Q144 124 160 112 V40 H208 V216 H160 V156 Q144 168 128 156 Q112 144 96 156 V216 H48 Z"/>
</svg>
"""
write("harbor-good.svg", good)

# 4 + 5. 'Sketch photos' — pencil thumbnails on paper, slightly rotated, with a vignette, rendered to PNG.
PENCIL = ('<filter id="pencil" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" '
          'baseFrequency="0.9" numOctaves="2" seed="{seed}" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" '
          'scale="2.6" xChannelSelector="R" yChannelSelector="G"/></filter>')


def jitter_path(points, rnd, amp=1.2):
    return "M" + " L".join(f"{x + rnd.uniform(-amp, amp):.1f} {y + rnd.uniform(-amp, amp):.1f}" for x, y in points)


def circle_pts(cx, cy, r, n=40, a0=0.0, a1=360.0):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def stroke(d, w=3.2, c="#2e2e2e", op=0.85):
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" opacity="{op}"/>'


def sketch_page(cells, title, seed, cols=4, cell=220):
    rnd = random.Random(seed)
    rows = (len(cells) + cols - 1) // cols
    W, H = cols * cell + 80, rows * (cell + 40) + 120
    parts = [f'<rect width="{W}" height="{H}" fill="#efe9dc"/>']
    for y in range(0, H, 24):  # faint dot grid of a sketchbook
        for x in range(0, W, 24):
            parts.append(f'<circle cx="{x}" cy="{y}" r="0.9" fill="#cfc6b3"/>')
    parts.append(f'<text x="40" y="58" font-family="Segoe Print, Bradley Hand, Comic Sans MS, cursive" font-size="26" '
                 f'fill="#3a3a3a">{title}</text>')
    for i, draw in enumerate(cells):
        r, c = divmod(i, cols)
        ox, oy = 40 + c * cell, 90 + r * (cell + 40)
        parts.append(f'<rect x="{ox + 8}" y="{oy + 8}" width="{cell - 16}" height="{cell - 16}" fill="none" stroke="#9b958a" '
                     f'stroke-width="1.4" opacity="0.7" rx="3"/>')
        parts.append(f'<text x="{ox + 14}" y="{oy + cell + 20}" font-family="Segoe Print, Comic Sans MS, cursive" '
                     f'font-size="17" fill="#555">{i + 1}</text>')
        parts.append(f'<g transform="translate({ox + 20} {oy + 20}) scale({(cell - 40) / 200:.3f})">{draw(rnd)}</g>')
    body = "".join(parts)
    rot = rnd.uniform(-1.8, 1.8)
    return W, H, (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
                  f'<defs>{PENCIL.format(seed=seed)}<radialGradient id="vig" cx="0.5" cy="0.45" r="0.75">'
                  f'<stop offset="0.6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.28"/>'
                  f'</radialGradient></defs><rect width="{W}" height="{H}" fill="#d9d2c4"/>'
                  f'<g transform="rotate({rot:.2f} {W / 2} {H / 2})" filter="url(#pencil)">{body}</g>'
                  f'<rect width="{W}" height="{H}" fill="url(#vig)"/></svg>')


# Bakery "Rise" — a mix: clichés (wheat, chef hat, rolling pin), generic (R in circle), promising (R with rising
# dough bump, croissant-as-moon "baked before dawn", loaf-as-b), and one too close to a famous mark (a bitten
# apple-ish bun with a leaf — reads like Apple).
def wheat(rnd):
    s = stroke(jitter_path([(100, 190), (100, 40)], rnd))
    for k in range(6):
        y = 60 + k * 20
        s += stroke(jitter_path([(100, y + 14), (80, y)], rnd)) + stroke(jitter_path([(100, y + 14), (120, y)], rnd))
    return s


def chef_hat(rnd):
    return (stroke(jitter_path(circle_pts(70, 90, 30, 30, 90, 330), rnd)) + stroke(jitter_path(circle_pts(100, 70, 34, 30, 180, 360), rnd))
            + stroke(jitter_path(circle_pts(130, 90, 30, 30, 210, 450), rnd)) + stroke(jitter_path([(64, 118), (64, 160), (136, 160), (136, 118)], rnd)))


def rolling_pin(rnd):
    return (stroke(jitter_path([(50, 90), (150, 90), (150, 120), (50, 120), (50, 90)], rnd))
            + stroke(jitter_path([(20, 105), (50, 105)], rnd)) + stroke(jitter_path([(150, 105), (180, 105)], rnd)))


def r_circle(rnd):
    return (stroke(jitter_path(circle_pts(100, 100, 80, 50), rnd))
            + stroke(jitter_path([(76, 150), (76, 56), (112, 56), (126, 70), (112, 96), (76, 96)], rnd))
            + stroke(jitter_path([(104, 96), (130, 150)], rnd)))


def r_rising(rnd):
    return (stroke(jitter_path([(66, 170), (66, 70)], rnd), w=5)
            + stroke(jitter_path(circle_pts(98, 78, 34, 30, 180, 360), rnd), w=5)
            + stroke(jitter_path([(132, 78), (128, 108), (66, 112)], rnd), w=5)
            + stroke(jitter_path([(96, 112), (136, 170)], rnd), w=5))


def croissant_moon(rnd):
    return (stroke(jitter_path(circle_pts(100, 100, 70, 40, 60, 300), rnd), w=4)
            + stroke(jitter_path(circle_pts(128, 96, 52, 30, 80, 280), rnd), w=4)
            + stroke(jitter_path([(70, 60), (84, 88)], rnd)) + stroke(jitter_path([(52, 100), (82, 104)], rnd))
            + stroke(jitter_path([(66, 144), (88, 124)], rnd)) + '<circle cx="160" cy="46" r="3" fill="#2e2e2e"/>')


def loaf_b(rnd):
    return (stroke(jitter_path([(60, 40), (60, 170)], rnd), w=5)
            + stroke(jitter_path(circle_pts(100, 130, 40, 36, 180, 540), rnd), w=5)
            + stroke(jitter_path([(84, 116), (96, 102)], rnd)) + stroke(jitter_path([(100, 124), (112, 110)], rnd)))


def apple_bun(rnd):
    return (stroke(jitter_path(circle_pts(100, 118, 58, 44, -40, 290), rnd), w=4)
            + stroke(jitter_path(circle_pts(160, 90, 18, 20, 100, 260), rnd), w=4)
            + stroke(jitter_path([(100, 60), (112, 30), (124, 40), (104, 60)], rnd), w=4))


W, H, svg = sketch_page([wheat, chef_hat, r_circle, r_rising, croissant_moon, loaf_b, rolling_pin, apple_bun],
                        "Rise bakery - thumbnails p.1", seed=11)
p = write("_rise-sketches.svg", svg)
render_png.render(p, os.path.join(OUT, "rise-bakery-sketches.png"), W, H)
os.remove(p)


# Single sketch for Remix: "Tidewell" sea-swimming club — a T whose crossbar is a breaking wave.
def tide_t(rnd):
    return (stroke(jitter_path([(100, 80), (100, 180)], rnd), w=6)
            + stroke(jitter_path([(30, 80), (60, 70), (90, 78), (120, 70)], rnd), w=6)
            + stroke(jitter_path(circle_pts(140, 64, 22, 26, 200, 470), rnd), w=6)
            + stroke(jitter_path([(122, 80), (170, 80)], rnd), w=6))


W, H, svg = sketch_page([tide_t], "Tidewell - T + wave", seed=5, cols=1, cell=460)
p = write("_tidewell.svg", svg)
render_png.render(p, os.path.join(OUT, "tidewell-sketch.png"), W, H)
os.remove(p)
print("fixtures in", OUT)
for f in sorted(os.listdir(OUT)):
    print(" ", f, os.path.getsize(os.path.join(OUT, f)))
