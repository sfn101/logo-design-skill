# DECISIONS — logo-coach build

One line per judgment call, with reasoning.

- **Renderer:** cairosvg pip-installed but its Cairo DLL is missing on this Windows box; `render_png.py` already falls back to headless Chrome/Edge, which works — so no GTK/Cairo system install. Documented as optional dependency.
- **Fork:** `gh` is not installed/authenticated, so the repo was plain-`git clone`d; the fork + push must be done by hand (see final report).
- **Claude CLI:** not on PATH; used the desktop-bundled `%APPDATA%\Claude\claude-code\2.1.284\claude.exe` for skill-creator's `run_loop.py`.
- **critique.md → critique-rubric.md:** the original critique's step 6 ("demonstrate the fix as an SVG revision") contradicts the no-redraw guardrail, so logo-coach replaces it with the rubric (diagnoses table folded in); `redesign.md`'s pointer updated.
- **Rough sheets:** extended logo-coach's copy of `concept_sheet.py` with `--rough/--remix/--tags/--cols/--wobble` rather than a wrapper — the polished 3-card layout can't hold 12–20 thumbnails. `logo-design`'s copy is untouched.
- **Rough look:** desaturate + lift black to graphite (knockouts survive) + light turbulence wobble, off-white paper cells, handwriting-ish label font; angle tags let the script enforce "≤2 per angle" and 12–20 count.
- **raster_wrap.py (new):** PNG/JPEG exports and sketch photos can't enter `preview_sheet.py`; wrapping them as SVG gives the visual tests without pretending to vectorise.
- **rubric_report.py validates:** it refuses to call vague notes/missing principles/>3 top changes clean (exit 1), enforcing the "every point cites a principle" guardrail mechanically.
- **Reading list:** titles/authors/editions verified by web search (Wheeler+Meyerson 6th ed 2024, Lupton 3rd ed 2024, Identify 2011, Evamy Logotype 2012, Cheng 2nd ed 2020, Mollerup 2013); topics named instead of chapter numbers because chapter numbering differs across editions and couldn't be verified.
- **Sagmeister & Walsh:** listed with a note that the studio split (2019) into Sagmeister Inc. and &Walsh, to avoid a stale link.
- **TRADEMARKS.md + LICENSE copied into skills/logo-coach/** so the notice travels inside the zip; repo-root copies kept.
- **Description:** first draft was 1,259 chars (limit 1,024) and contained a YAML-breaking colon; trimmed to 980.
- **No TodoWrite tool in this session:** progress tracked in chat/chapters instead of a TodoList.
