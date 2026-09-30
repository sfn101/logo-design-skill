#!/usr/bin/env python3
"""Render a one-page critique report (HTML, optional PNG) from rubric scores + notes in a JSON file.

The report is the written record of a Coach Mode critique round: the designer's mark (never a redraw), the
first impression, what works, the 10-criterion rubric from references/critique-rubric.md with a principle
cited for every score, the top changes in priority order, the embedded test sheet, and the next assignment.
It validates the critique as it renders: a score without a principle, a note that says nothing, or more than
three "top" changes are reported as problems, because vague critique doesn't teach.

Usage:
  python3 scripts/rubric_report.py critique.json -o report.html
  python3 scripts/rubric_report.py critique.json -o report.html --png report.png     # + screenshot (Chrome)
  python3 scripts/rubric_report.py --template > critique.json                        # starter JSON

JSON (paths relative to the JSON file):
{
  "project": "Kiln Roasters", "designer": "Soufiane", "round": 1, "date": "2026-09-30",
  "mark": "kiln-v3.svg",                         # the designer's file (SVG, PNG or JPEG)
  "test_sheet": "kiln-v3-tests.png",             # screenshot of preview_sheet.py (optional)
  "first_impression": "…",
  "what_works": ["…", "…"],
  "scores": [ {"criterion": "concept", "score": 3, "note": "…", "principle": "principles.md §2.7 Focus on one thing"}, … ],
  "fatal_flaw": "",                              # optional: one flaw that outweighs the total
  "top_changes": [ {"change": "…", "why": "…", "principle": "visual-techniques.md §3 Overshoot"} ],
  "assignment": "…", "reading": "…"
}
Criteria keys: concept, relevance, distinctiveness, simplicity, construction, optical-balance, scalability,
one-colour, typography, longevity. "principle" defaults to the rubric's mapping when omitted (a warning is
still printed so you cite the specific section). Use "n/a" as the score for typography on a symbol-only mark.
Standard library only; PNG export uses render_png.py (headless Chrome/Chromium/Edge).
"""
import argparse
import base64
import html
import json
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_png  # noqa: E402
import svglib  # noqa: E402,F401  (UTF-8 console)

CRITERIA = [
    ("concept", "Concept strength", "principles.md §2.7 Focus on one thing"),
    ("relevance", "Relevance to brief", "principles.md §2.4 / §5 Relevance vs. literalness"),
    ("distinctiveness", "Distinctiveness vs. category", "principles.md §2.5 / §6; testing-checklist.md §4"),
    ("simplicity", "Simplicity", "principles.md §2.3 / §4 Simplicity, properly understood"),
    ("construction", "Construction & geometry", "visual-techniques.md §1; svg-construction.md §2–3"),
    ("optical-balance", "Optical balance", "visual-techniques.md §2 Balance, §3 Optical corrections"),
    ("scalability", "Legibility & scalability (16 px)", "principles.md §2.8; testing-checklist.md §1"),
    ("one-colour", "One-colour performance", "testing-checklist.md §2; color.md §1 Order of operations"),
    ("typography", "Typography pairing", "typography.md §1 / §5 Lockups"),
    ("longevity", "Longevity", "principles.md §2.9 / §7 Longevity vs. trend"),
]
VAGUE = {"looks good", "feels off", "nice", "good", "bad", "ok", "fine", "great", "not great", "meh"}

TEMPLATE = {
    "project": "Brand name", "designer": "Your name", "round": 1, "date": "YYYY-MM-DD",
    "mark": "my-logo.svg", "test_sheet": "my-logo-tests.png",
    "first_impression": "What a stranger sees and remembers in two seconds.",
    "what_works": ["Something that earned praise, and why."],
    "scores": [{"criterion": k, "score": 3, "note": "Evidence you can point at.", "principle": p} for k, _, p in CRITERIA],
    "fatal_flaw": "",
    "top_changes": [{"change": "What to change (not how it should look).", "why": "The effect it has now.",
                     "principle": "principles.md §2.3"}],
    "assignment": "The next thing to make or practise.", "reading": "Book + chapter/topic, and why.",
}


def data_uri(path):
    ext = os.path.splitext(path)[1].lower()
    mime = {".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".gif": "image/gif", ".webp": "image/webp"}.get(ext, "application/octet-stream")
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode("ascii")


def validate(spec):
    problems, warnings = [], []
    by_key = {s.get("criterion"): s for s in spec.get("scores", [])}
    known = {k for k, _, _ in CRITERIA}
    for k in by_key:
        if k not in known:
            problems.append(f"unknown criterion '{k}' (use: {', '.join(sorted(known))})")
    for k, label, default in CRITERIA:
        s = by_key.get(k)
        if not s:
            problems.append(f"missing score for '{k}' ({label})")
            continue
        sc = s.get("score")
        if sc != "n/a" and not (isinstance(sc, (int, float)) and 1 <= sc <= 5):
            problems.append(f"'{k}': score must be 1–5 or \"n/a\", got {sc!r}")
        note = (s.get("note") or "").strip()
        if len(note) < 20 or note.lower().strip(".! ") in VAGUE:
            problems.append(f"'{k}': note is too vague to teach anything — name what you see and where")
        if not (s.get("principle") or "").strip():
            s["principle"] = default
            warnings.append(f"'{k}': no principle cited — defaulted to {default}; cite the specific section")
    changes = spec.get("top_changes", [])
    if not changes:
        problems.append("no top_changes — a critique must end in something the designer can act on")
    if len(changes) > 3:
        problems.append(f"{len(changes)} top changes — keep it to the 3 with the biggest impact")
    for i, c in enumerate(changes, 1):
        if not (c.get("principle") or "").strip():
            problems.append(f"top change {i}: cite the principle behind it")
    if not spec.get("mark"):
        problems.append("no 'mark' file — the report shows the designer's own work")
    return problems, warnings


def bar(score):
    if score == "n/a":
        return '<span class="na">n/a</span>'
    cells = "".join(f'<i class="{"on" if j < round(score) else ""}"></i>' for j in range(5))
    return f'<span class="bar">{cells}</span><b>{score:g}</b>'


def build(spec, base):
    esc = html.escape
    by_key = {s["criterion"]: s for s in spec.get("scores", []) if s.get("criterion")}
    nums = [s["score"] for s in by_key.values() if isinstance(s.get("score"), (int, float))]
    total = sum(nums)
    maxi = 5 * len(nums)
    mark = os.path.join(base, spec["mark"])
    mark_uri = data_uri(mark) if os.path.exists(mark) else ""
    rows = []
    for k, label, _ in CRITERIA:
        s = by_key.get(k)
        if not s:
            continue
        rows.append(f"<tr><td class='crit'>{esc(label)}</td><td class='sc'>{bar(s.get('score'))}</td>"
                    f"<td>{esc(s.get('note', ''))}<div class='pr'>↳ {esc(s.get('principle', ''))}</div></td></tr>")
    changes = "".join(f"<li><b>{esc(c.get('change', ''))}</b> {esc(c.get('why', ''))}"
                      f"<div class='pr'>↳ {esc(c.get('principle', ''))}</div></li>" for c in spec.get("top_changes", []))
    works = "".join(f"<li>{esc(w)}</li>" for w in spec.get("what_works", []))
    sheet = ""
    ts = spec.get("test_sheet")
    if ts and os.path.exists(os.path.join(base, ts)):
        sheet = (f"<h2>Test sheet</h2><p class='muted'>preview_sheet.py — 16 px, one-colour, reversed, squint, "
                 f"mirror, contexts, shelf.</p><img class='sheet' src='{data_uri(os.path.join(base, ts))}'>")
    fatal = spec.get("fatal_flaw", "").strip()
    fatal_html = f"<div class='fatal'><b>Fatal flaw:</b> {esc(fatal)} — this outweighs the total.</div>" if fatal else ""
    sizes = "".join(f"<div><img src='{mark_uri}' style='width:{s}px;height:{s}px'><span>{s}px</span></div>"
                    for s in (64, 32, 16)) if mark_uri else ""
    meta = " · ".join(esc(str(x)) for x in (spec.get("designer"), f"Round {spec.get('round')}" if spec.get("round") else None,
                                              spec.get("date")) if x)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Critique — {esc(spec.get('project', ''))}</title>
<style>
:root{{--ink:#1d1d1b;--muted:#6f6c66;--line:#e3dfd6;--paper:#faf8f3;--acc:#1d1d1b;--bad:#9b2c1f}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:15px/1.5 system-ui,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif}}
.page{{max-width:1100px;margin:0 auto;padding:40px 44px 56px}}
h1{{font-size:30px;margin:0 0 4px}}h2{{font-size:17px;margin:30px 0 8px;letter-spacing:.3px}}
.muted{{color:var(--muted);margin:0 0 10px}}
.top{{display:grid;grid-template-columns:300px 1fr;gap:32px;align-items:start;margin-top:24px}}
.mark{{background:#fff;border:1px solid var(--line);border-radius:12px;padding:24px}}
.mark>img{{width:100%;height:220px;object-fit:contain;display:block}}
.sizes{{display:flex;gap:18px;align-items:flex-end;margin-top:16px}}.sizes div{{display:flex;flex-direction:column;align-items:center;gap:4px}}
.sizes img{{object-fit:contain}}.sizes span{{font-size:11px;color:var(--muted)}}
.total{{font-size:40px;font-weight:700;line-height:1}}.total small{{font-size:16px;color:var(--muted);font-weight:400}}
table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden}}
td{{padding:10px 14px;border-top:1px solid var(--line);vertical-align:top}}tr:first-child td{{border-top:0}}
.crit{{width:230px;font-weight:600}}.sc{{width:150px;white-space:nowrap}}
.bar{{display:inline-flex;gap:3px;margin-right:8px;vertical-align:middle}}.bar i{{width:14px;height:10px;border-radius:2px;background:var(--line)}}
.bar i.on{{background:var(--acc)}}.na{{color:var(--muted)}}
.pr{{color:var(--muted);font-size:12.5px;margin-top:3px}}
ol,ul{{margin:0;padding-left:20px}}li{{margin:6px 0}}
.fatal{{border-left:4px solid var(--bad);background:#fff;padding:10px 14px;margin-top:14px}}
.next{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}.card{{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px 18px}}
.sheet{{width:100%;border:1px solid var(--line);border-radius:12px;background:#fff}}
footer{{margin-top:34px;color:var(--muted);font-size:13px}}
@media (max-width:760px){{.top,.next{{grid-template-columns:1fr}}.crit{{width:auto}}}}
</style></head><body><div class="page">
<h1>Critique — {esc(spec.get('project', ''))}</h1><p class="muted">{meta}</p>
<div class="top"><div class="mark">{f"<img src='{mark_uri}' alt='the designer&#39;s mark'>" if mark_uri else "<p>(mark file not found)</p>"}
<div class="sizes">{sizes}</div></div>
<div><div class="total">{total:g}<small> / {maxi}</small></div><p class="muted">Rough guide only — one fatal flaw outweighs a high total.</p>
<h2>First impression</h2><p>{esc(spec.get('first_impression', ''))}</p>
{f"<h2>What works</h2><ul>{works}</ul>" if works else ""}{fatal_html}</div></div>
<h2>Rubric</h2><table>{''.join(rows)}</table>
<h2>Top changes, in priority order</h2><ol>{changes}</ol>
{sheet}
<h2>Next</h2><div class="next"><div class="card"><b>Assignment</b><p>{esc(spec.get('assignment', ''))}</p></div>
<div class="card"><b>Reading</b><p>{esc(spec.get('reading', ''))}</p></div></div>
<footer>Critique only — nothing here was redrawn. The changes are yours to make.</footer>
</div></body></html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", nargs="?")
    ap.add_argument("-o", "--out", default="critique-report.html")
    ap.add_argument("--png", help="also screenshot the report to this PNG (needs Chrome/Chromium/Edge)")
    ap.add_argument("--width", type=int, default=1100)
    ap.add_argument("--template", action="store_true", help="print a starter JSON and exit")
    a = ap.parse_args()
    if a.template:
        print(json.dumps(TEMPLATE, indent=2, ensure_ascii=False))
        return
    if not a.spec:
        ap.error("give a critique JSON (or --template)")
    with open(a.spec, encoding="utf-8") as fh:
        spec = json.load(fh)
    problems, warnings = validate(spec)
    for w in warnings:
        print("! WARN", w)
    for p in problems:
        print("✖ PROBLEM", p)
    base = os.path.dirname(os.path.abspath(a.spec))
    doc = build(spec, base)
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write(doc)
    print("wrote", a.out, "— fix the problems above before sharing it" if problems else "")
    if a.png:
        h = 1500 + 20 * len(spec.get("top_changes", []))
        ts = spec.get("test_sheet")
        if ts and os.path.exists(os.path.join(base, ts)):
            size = render_png.png_size(os.path.join(base, ts))
            if size:
                h += int((a.width - 88) * size[1] / size[0]) + 80
        try:
            render_png.screenshot_html(a.out, a.png, a.width, h)
            print("wrote", a.png)
        except Exception as e:  # no Chrome available
            print(f"PNG skipped ({e}); open the HTML instead")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
