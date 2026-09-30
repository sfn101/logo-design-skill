#!/usr/bin/env python3
"""Package the skills as zip files for upload (e.g. claude.ai → Settings → Capabilities → Skills).

  python tools/package_skill.py                 # both skills
  python tools/package_skill.py logo-coach      # one skill

Writes dist/<skill>.zip (full) + dist/<skill>-lite.zip for each skill. claude.ai accepts at most 200 files per
upload and no nested archives, so the full package stores the 1,400+ library SVGs as ONE text file,
assets/library/svg-bundle.json ({"file.svg": "<svg…>"}); the scripts unpack it to a temp cache on first use
(see svglib._library_svg_dir). The lite package leaves the SVGs
and gallery.html out entirely (catalog metadata, scripts and all references are kept). Eval fixtures (evals/) are
development-only and never packaged.
"""
import json
import os
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
SKILLS = ["logo-design", "logo-coach"]
MAX_FILES = 200


def svg_bundle(svg_dir):
    files = {}
    for fn in sorted(os.listdir(svg_dir)):
        if fn.lower().endswith(".svg"):
            with open(os.path.join(svg_dir, fn), encoding="utf-8", errors="replace") as fh:
                files[fn] = fh.read()
    return json.dumps(files, ensure_ascii=False, separators=(",", ":"))


def build(skill, name, lite):
    src = os.path.join(ROOT, "skills", skill)
    os.makedirs(DIST, exist_ok=True)
    out = os.path.join(DIST, name)
    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for dirpath, dirnames, filenames in os.walk(src):
            rel_dir = os.path.relpath(dirpath, src).replace(os.sep, "/")
            if rel_dir == ".":
                dirnames[:] = [d for d in dirnames if d != "evals"]
            dirnames[:] = [d for d in dirnames if d not in {"__pycache__", ".DS_Store"}]
            if rel_dir == "assets/library/svg" or rel_dir.startswith("assets/library/svg/"):
                continue  # handled below: nested archive (full) or omitted (lite)
            for fn in filenames:
                if fn == ".DS_Store" or fn.endswith(".pyc") or (lite and fn == "gallery.html"):
                    continue
                full = os.path.join(dirpath, fn)
                z.write(full, os.path.join(skill, os.path.relpath(full, src)))
                count += 1
        svg_dir = os.path.join(src, "assets", "library", "svg")
        if not lite and os.path.isdir(svg_dir):
            z.writestr(f"{skill}/assets/library/svg-bundle.json", svg_bundle(svg_dir))
            count += 1
        nested = [n for n in z.namelist() if n.lower().endswith((".zip", ".tar", ".gz", ".tgz", ".7z", ".rar"))]
    print(f"{out}  {os.path.getsize(out) / 1e6:.1f} MB  {count} files")
    if nested:
        sys.exit(f"✖ {name} contains nested archives (not allowed on upload): {nested}")
    if count > MAX_FILES:
        sys.exit(f"✖ {name} has {count} files — over the {MAX_FILES}-file upload limit")


if __name__ == "__main__":
    for skill in sys.argv[1:] or SKILLS:
        build(skill, f"{skill}.zip", lite=False)
        build(skill, f"{skill}-lite.zip", lite=True)
