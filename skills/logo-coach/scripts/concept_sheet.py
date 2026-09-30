#!/usr/bin/env python3
"""Build a one-page concept overview (SVG + PNG) to show the user BEFORE any kit is produced.

Each concept gets a card: the artwork large, the same mark at 64 / 32 / 16 px (so scale is judged honestly),
a letter + name, and a one-line idea. Optionally a secondary file per concept (e.g. the lockup) under the symbol.
The PNG is rendered with render_png.py's backends (cairosvg, rsvg-convert, Inkscape, Chrome, Quick Look);
the SVG is always written.

Usage:
  python3 scripts/concept_sheet.py a.svg b.svg c.svg --names "Next Block" "Ranked F" "Forward f" \\
      --notes "One block steps forward: the next move." "An F of ranked priority bars." "The i-dot steps ahead." \\
      --title "Fabbit — logo concepts" --recommend 1 -o concepts.png
  python3 scripts/concept_sheet.py a.svg b.svg c.svg --lockups a-h.svg b-h.svg c-h.svg --greyscale -o round1.png

Rough mode (logo-coach Sketch Mode): 12–20 loose thumbnails on one sheet — flat grey, slightly wobbly edges,
no size ladder, no recommendation. --names = the idea, --notes = the word-map link, --tags = the angle.
  python3 scripts/concept_sheet.py t01.svg … t16.svg --rough --title "Stillroom — rough thumbnails" \\
      --names "S + held breath" … --notes "still → pause" … --tags lettermark negative-space … -o sheet.png
The script warns when a sheet has fewer than 12 / more than 20 thumbnails (6–10 with --remix) or when one
angle appears more than twice — range is the point of the exercise.

Show the resulting PNG to the user (view it yourself first), then stop and ask how to proceed.
"""
import argparse
import html
import os
import re
import sys

sys.dont_write_bytecode = True  # keep the skill folder clean (no __pycache__)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_png  # noqa: E402
import svglib  # noqa: E402


def embed(path, key, x, y, w, h):
    """Nested <svg> that fits the file into the box; ids are prefixed so several files can coexist."""
    raw = open(path, encoding="utf-8", errors="ignore").read()
    raw = re.sub(r"<\?xml[^>]*\?>|<!DOCTYPE[^>]*>", "", raw, flags=re.I)
    raw = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{key}-{m.group(1)}"', raw)
    raw = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{key}-{m.group(1)})", raw)
    raw = re.sub(r'(xlink:href|href)="#([^"]+)"', lambda m: f'{m.group(1)}="#{key}-{m.group(2)}"', raw)
    m = re.search(r"<svg\b[^>]*>", raw)
    tag = m.group(0)
    root_vb = svglib.view_box(svglib.load_svg(path)[1])
    vb = f' viewBox="{root_vb[0]:g} {root_vb[1]:g} {root_vb[2]:g} {root_vb[3]:g}"' if root_vb else ""
    new_tag = re.sub(r'\s(width|height|x|y|viewBox|preserveAspectRatio)\s*=\s*"[^"]*"', "", tag)
    new_tag = new_tag[:-1].rstrip("/") + f'{vb} x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" preserveAspectRatio="xMidYMid meet">'
    return raw.replace(tag, new_tag, 1)


def wrap(text, limit):
    words, lines, line = text.split(), [], ""
    for w in words:
        if len(line) + len(w) + 1 > limit and line:
            lines.append(line)
            line = ""
        line += (" " if line else "") + w
    if line:
        lines.append(line)
    return lines


ANGLES = ["wordmark", "letterform", "lettermark", "pictorial", "abstract", "emblem", "negative-space",
          "metaphor", "typographic-play", "mascot", "pattern"]


def rough_sheet(a):
    """A sketchbook-style grid of rough thumbnails: flat grey, wobbly edges, a label under each."""
    n = len(a.files)
    lo, hi = (6, 10) if a.remix else (12, 20)
    warnings = []
    if not lo <= n <= hi:
        warnings.append(f"{n} thumbnails — {'Remix' if a.remix else 'Sketch Mode'} asks for {lo}–{hi}")
    if a.tags:
        counts = {}
        for t in a.tags:
            counts[t] = counts.get(t, 0) + 1
        for t, c in sorted(counts.items()):
            if c > 2 and not a.remix:
                warnings.append(f"angle '{t}' used {c}× — keep it to two per angle for range")
        unknown = sorted({t for t in a.tags if t not in ANGLES})
        if unknown:
            warnings.append("non-standard angle tag(s): " + ", ".join(unknown) + f" (standard: {', '.join(ANGLES)})")
    cols = a.cols or (4 if n <= 12 else 5)
    rows = (n + cols - 1) // cols
    W, pad, gap = a.width, 50, 18
    cell_w = (W - 2 * pad - (cols - 1) * gap) / cols
    art = cell_w - 44
    cell_h = 30 + art + 104
    header = 140
    footer = 60
    H = header + rows * cell_h + (rows - 1) * gap + footer
    font = "font-family=\"'Segoe Print','Bradley Hand','Comic Sans MS',system-ui,sans-serif\""
    sans = "font-family=\"system-ui,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif\""
    # grey: desaturate, then lift black to dark graphite while white stays white (knockouts survive);
    # wobble: a little turbulence displacement so edges read as pencil-rough, not finished vector
    filt = ('<defs><filter id="rough" x="-5%" y="-5%" width="110%" height="110%">'
            '<feColorMatrix type="saturate" values="0" result="g"/>'
            '<feComponentTransfer in="g" result="lift"><feFuncR type="linear" slope="0.72" intercept="0.25"/>'
            '<feFuncG type="linear" slope="0.72" intercept="0.25"/><feFuncB type="linear" slope="0.72" intercept="0.25"/>'
            '</feComponentTransfer>')
    if a.wobble > 0:
        filt += (f'<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7" result="n"/>'
                 f'<feDisplacementMap in="lift" in2="n" scale="{a.wobble:g}" xChannelSelector="R" yChannelSelector="G"/>')
    filt += '</filter></defs>'
    parts = [f'<rect width="{W}" height="{H:g}" fill="#f4f1ea"/>',
             f'<text x="{pad}" y="72" {sans} font-size="36" font-weight="700" fill="#2b2b2b">{html.escape(a.title)}</text>',
             f'<text x="{pad}" y="108" {sans} font-size="18" fill="#6b6b6b">{html.escape(a.subtitle)}</text>']
    for i, f in enumerate(a.files):
        r, c = divmod(i, cols)
        x = pad + c * (cell_w + gap)
        y = header + r * (cell_h + gap)
        parts.append(f'<rect x="{x:g}" y="{y:g}" width="{cell_w:g}" height="{cell_h:g}" rx="6" fill="#fffdf8" '
                     f'stroke="#d9d4c7" stroke-width="1" stroke-dasharray="5 4"/>')
        parts.append(f'<text x="{x + 12:g}" y="{y + 22:g}" {sans} font-size="13" font-weight="700" fill="#8a8578">'
                     f'{i + 1:02d}</text>')
        if i < len(a.tags) and a.tags[i]:
            parts.append(f'<text x="{x + cell_w - 12:g}" y="{y + 22:g}" {sans} font-size="11" fill="#8a8578" '
                         f'text-anchor="end" letter-spacing="1">{html.escape(a.tags[i].upper())}</text>')
        parts.append('<g filter="url(#rough)">' + embed(f, f"t{i}", x + 22, y + 30, art, art) + "</g>")
        yy = y + 30 + art + 24
        name = a.names[i] if i < len(a.names) else os.path.splitext(os.path.basename(f))[0]
        for k, line in enumerate(wrap(name, int(cell_w / 9.2))[:2]):
            parts.append(f'<text x="{x + 12:g}" y="{yy + k * 20:g}" {font} font-size="16" fill="#2b2b2b">{html.escape(line)}</text>')
        note = a.notes[i] if i < len(a.notes) else ""
        for k, line in enumerate(wrap(note, int(cell_w / 7.4))[:2]):
            parts.append(f'<text x="{x + 12:g}" y="{yy + 44 + k * 17:g}" {sans} font-size="13" fill="#77736a">{html.escape(line)}</text>')
    parts.append(f'<text x="{pad}" y="{H - 24:g}" {sans} font-size="15" fill="#8a8578">Rough starting points, not designs. '
                 f'Pick 2–3 and develop them by hand.</text>')
    return W, H, filt + "".join(parts), warnings


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", help="one SVG per concept (usually the symbol)")
    ap.add_argument("--lockups", nargs="*", default=[], help="optional second file per concept (lockup/wordmark)")
    ap.add_argument("--names", nargs="*", default=[])
    ap.add_argument("--notes", nargs="*", default=[], help="one-sentence idea per concept")
    ap.add_argument("--title", default="Logo concepts")
    ap.add_argument("--subtitle", default="Concepts for review — pick a direction (or tell me what you like in each).")
    ap.add_argument("--recommend", type=int, help="1-based index of the recommended concept")
    ap.add_argument("--greyscale", action="store_true", help="show everything in greyscale (first-round rule)")
    ap.add_argument("--width", type=int, default=1600)
    ap.add_argument("-o", "--out", default="concepts.png", help="output .png (an .svg is written next to it)")
    ap.add_argument("--rough", action="store_true", help="Sketch Mode: rough thumbnail grid (grey, wobbly, labelled)")
    ap.add_argument("--remix", action="store_true", help="with --rough: variations of the user's sketch (expects 6–10)")
    ap.add_argument("--tags", nargs="*", default=[], help="with --rough: angle per thumbnail, e.g. lettermark negative-space")
    ap.add_argument("--cols", type=int, help="with --rough: columns (default 4 for ≤12 thumbnails, else 5)")
    ap.add_argument("--wobble", type=float, default=3.0, help="with --rough: edge roughness in px (0 = clean)")
    a = ap.parse_args()

    if a.rough:
        if a.title == "Logo concepts":
            a.title = "Rough variations" if a.remix else "Rough thumbnails"
        if a.subtitle.startswith("Concepts for review"):
            a.subtitle = "Loose starting points from the word map — not finished marks."
        W, H, body, warnings = rough_sheet(a)
        doc = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
               f'width="{W}" height="{H:g}" viewBox="0 0 {W} {H:g}">{body}</svg>\n')
        base = os.path.splitext(a.out)[0]
        with open(base + ".svg", "w", encoding="utf-8") as fh:
            fh.write(doc)
        print("wrote", base + ".svg", f"({len(a.files)} thumbnails)")
        for w in warnings:
            print("! WARN", w)
        used = render_png.render(base + ".svg", base + ".png", W, int(round(H)))
        if used:
            print(f"wrote {base}.png via {used} — view it, show it, then STOP and hand the choice back")
        else:
            print("PNG skipped (no renderer; see render_png.py --which) — show the SVG instead")
        return

    n = len(a.files)
    cols = min(n, 3)
    rows = (n + cols - 1) // cols
    W, pad, gap = a.width, 60, 28
    card_w = (W - 2 * pad - (cols - 1) * gap) / cols
    has_lock = bool(a.lockups)
    art_h = 300
    lock_h = 0
    if has_lock:
        ratios = []
        for lp in a.lockups:
            if lp:
                vb = svglib.view_box(svglib.load_svg(lp)[1])
                if vb and vb[3]:
                    ratios.append(vb[2] / vb[3])
        # wide lockups fit a short slot; squarish ones (emblems, stacked lockups) need more height
        lock_h = 120 if not ratios or min(ratios) >= 2.2 else (170 if min(ratios) >= 1.4 else 210)
    card_h = 40 + art_h + (lock_h + 24 if has_lock else 0) + 90 + 150 + (30 if a.recommend else 0) + 20
    header = 150
    H = header + rows * card_h + (rows - 1) * gap + pad
    parts = []
    filt = ('<defs><filter id="grey"><feColorMatrix type="saturate" values="0"/></filter></defs>' if a.greyscale else "")
    gattr = ' filter="url(#grey)"' if a.greyscale else ""
    font = "font-family=\"system-ui,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif\""
    parts.append(f'<rect width="{W}" height="{H}" fill="#f7f7f4"/>')
    parts.append(f'<text x="{pad}" y="78" {font} font-size="40" font-weight="700" fill="#161616">{html.escape(a.title)}</text>')
    parts.append(f'<text x="{pad}" y="116" {font} font-size="20" fill="#6b6b6b">{html.escape(a.subtitle)}</text>')
    for i, f in enumerate(a.files):
        r, c = divmod(i, cols)
        x = pad + c * (card_w + gap)
        y = header + r * (card_h + gap)
        rec = a.recommend == i + 1
        parts.append(f'<rect x="{x:g}" y="{y:g}" width="{card_w:g}" height="{card_h:g}" rx="18" fill="#fff" '
                     f'stroke="{"#161616" if rec else "#e4e4e0"}" stroke-width="{2 if rec else 1}"/>')
        inner_x, inner_w = x + 30, card_w - 60
        parts.append(f"<g{gattr}>" + embed(f, f"c{i}", inner_x, y + 40, inner_w, art_h) + "</g>")
        yy = y + 40 + art_h
        if has_lock and i < len(a.lockups) and a.lockups[i]:
            yy += 24
            parts.append(f"<g{gattr}>" + embed(a.lockups[i], f"l{i}", inner_x, yy, inner_w, lock_h) + "</g>")
            yy += lock_h
        # small sizes: 64 / 32 / 16 px, as they would appear
        sx = inner_x
        yy += 26
        for s in (64, 32, 16):
            parts.append(f"<g{gattr}>" + embed(f, f"s{i}{s}", sx, yy + (64 - s), s, s) + "</g>")
            parts.append(f'<text x="{sx + s / 2:g}" y="{yy + 84}" {font} font-size="12" fill="#8a8a8a" text-anchor="middle">{s}px</text>')
            sx += s + 26
        yy += 120
        label = f"{chr(65 + i)} · {a.names[i] if i < len(a.names) else os.path.splitext(os.path.basename(f))[0]}"
        parts.append(f'<text x="{inner_x}" y="{yy}" {font} font-size="26" font-weight="700" '
                     f'fill="{"#161616"}">{html.escape(label)}</text>')
        if rec:
            parts.append(f'<text x="{inner_x}" y="{yy + 28}" {font} font-size="15" font-weight="700" fill="#161616" '
                         f'letter-spacing="1.5">RECOMMENDED</text>')
            yy += 28
        note = a.notes[i] if i < len(a.notes) else ""
        for k, line in enumerate(wrap(note, int(inner_w / 9.6))[:3]):
            parts.append(f'<text x="{inner_x}" y="{yy + 34 + k * 26}" {font} font-size="19" fill="#555">{html.escape(line)}</text>')
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
           f'width="{W}" height="{H:g}" viewBox="0 0 {W} {H:g}">{filt}{"".join(parts)}</svg>\n')
    base = os.path.splitext(a.out)[0]
    svg_path = base + ".svg"
    with open(svg_path, "w", encoding="utf-8") as fh:
        fh.write(doc)
    print("wrote", svg_path)
    png_path = base + ".png"
    used = render_png.render(svg_path, png_path, W, int(round(H)))
    if used:
        print(f"wrote {png_path} via {used} — view it, show it to the user, then stop and ask")
    else:
        print("PNG skipped (no renderer; see render_png.py --which) — show the SVG instead")


if __name__ == "__main__":
    main()
