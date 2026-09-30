#!/usr/bin/env python3
"""Package the skills as zip files for upload (e.g. claude.ai → Settings → Capabilities → Skills).

  python tools/package_skill.py                 # both skills
  python tools/package_skill.py logo-coach      # one skill

Writes dist/<skill>.zip (full) + dist/<skill>-lite.zip for each skill. The lite package leaves out the 1,400+ SVG
files and gallery.html (catalog metadata, scripts and all references are kept) for platforms with upload size
limits. Eval fixtures (evals/) are development-only and never packaged.
"""
import os
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
SKIP_DIRS = {"__pycache__", ".DS_Store", "evals"}
SKILLS = ["logo-design", "logo-coach"]


def build(skill, name, lite):
    src = os.path.join(ROOT, "skills", skill)
    os.makedirs(DIST, exist_ok=True)
    out = os.path.join(DIST, name)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for dirpath, dirnames, filenames in os.walk(src):
            rel_dir = os.path.relpath(dirpath, src).replace(os.sep, "/")
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS or rel_dir != "."]
            dirnames[:] = [d for d in dirnames if d not in {"__pycache__", ".DS_Store"}]
            if lite and rel_dir.startswith("assets/library/svg"):
                continue
            for fn in filenames:
                if fn in SKIP_DIRS or fn.endswith(".pyc"):
                    continue
                if lite and fn == "gallery.html":
                    continue
                full = os.path.join(dirpath, fn)
                z.write(full, os.path.join(skill, os.path.relpath(full, src)))
    print(f"{out}  {os.path.getsize(out) / 1e6:.1f} MB")


if __name__ == "__main__":
    for skill in sys.argv[1:] or SKILLS:
        build(skill, f"{skill}.zip", lite=False)
        build(skill, f"{skill}-lite.zip", lite=True)
