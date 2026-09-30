# Notes on the original `logo-design` skill (v1.4.4, kaankiziltug)

What each part does, and what `logo-coach` does with it. Verified in this environment (Windows 11, Python 3.14,
renderer = headless Chrome/Edge via `render_png.py`; `tools/smoke_test.py` → all checks passed).

## SKILL.md (223 lines)
Turns Claude into a senior identity designer that **does the design work**: brief → research → 8–12 one-line
concepts → builds 3 SVGs → audits/tests → concept checkpoint (stop) → full kit on approval. Modes: Design,
Critique, Redesign, System, Assets. Strong principles list, red-flags list, honesty/limits section.
→ **Adapt.** logo-coach inverts the role: the user designs, Claude directs. Keep the principles, red flags,
honesty section and tool table; drop the "Claude builds concepts" phases from Coach Mode; keep a narrow,
rough version of concept generation for Sketch Mode only; full workflow stays available as fallback via the
sibling `logo-design` skill.

## references/ (all reused as-is, copied into logo-coach)
| File | What it covers | In logo-coach |
|---|---|---|
| `principles.md` | 12 principles, mnemonic model, simplicity, relevance vs literal, distinction, longevity, tensions, 12 diagnostic questions | **Reuse** — main citation source for critique |
| `discovery-brief.md` | fast 5 questions, full question bank, brief template, word mapping, brief warning signs | **Reuse** — Stage 1 & 2 (user does the word map) |
| `mark-types.md` | 9 mark types with pros/cons + decision guide | **Reuse** — sketch-range angles, critique of type choice |
| `visual-techniques.md` | grids, balance, optical corrections (overshoot, bone, irradiation, optical centre), negative space, paradoxes | **Reuse** — citations for construction/optical-balance scores |
| `typography.md` | type study, classification voices, custom letters, lockups, licensing, mistakes | **Reuse** — typography-pairing score, wordmark reading |
| `color.md` | order of operations, harmony, how many colours, reproduction, accessibility | **Reuse** — one-colour / palette critique |
| `testing-checklist.md` | scale, colour/value, form, distinctiveness, meaning, media, context | **Reuse** — what the test sheet proves |
| `process.md` | stage map, exploration stages A/B/C, vector development, final checklist, habits | **Reuse** — sketch-quota & "quantity before quality" teaching |
| `critique.md` | method, 10-dimension scorecard, diagnoses→fixes, output format | **Adapt** into `critique-rubric.md` (new dimensions, 1/3/5 anchors, no "demonstrate the fix as SVG") |
| `svg-construction.md` | clean-SVG craft | **Reuse** — for Sketch Mode drawing + teaching SVG hygiene when the user exports |
| `presentation-delivery.md` | presentation structure, feedback, committees | **Reuse** — Stage 6 presentation practice |
| `identity-system.md` | kit of parts, systems, motion | **Reuse** — longevity/system questions |
| `redesign.md` | refresh vs rebrand | **Reuse** — when the user brings an old mark |
| `library-guide.md` | what's in the 1,432-logo library, insights, curated examples by technique | **Reuse** — research assignments, look-alike checks |

## scripts/ (all reused; dependency-free Python)
| Script | Does | Coach use |
|---|---|---|
| `svg_audit.py` | structure, colour count, near-miss angles, tiny details, centring, complexity vs library, 0–100 score | Stage 5 critique evidence |
| `preview_sheet.py` | HTML test sheet: size ladder, 16/32 px, backgrounds, one-colour, squint, mirror/rotate, contexts, shelf test | Stage 5 critique evidence (screenshot with `render_png.py`) |
| `search_library.py` | filter library by type/technique/geometry/subject/industry/colour/mood; `--summary`; `--exemplary` | Stage 3 research assignments; look-alike checks for sketches |
| `concept_sheet.py` | one-image overview of ~3 polished concepts with 64/32/16 px ladder | **Extended with `--rough`**: 12–20 thumbnail grid, flat grey, label under each |
| `render_png.py` | SVG→PNG, HTML screenshot via Chrome, favicon.ico; backend fallback chain | Viewing user files and sheets |
| `presentation_board.py` | client board with industry mockups | Optional in Stage 6 (user's own marks only) |
| `export_variants.py` | black/white/mono/favicon/app-icon/web icons | Not part of coaching; kept for completeness/fallback |
| `svglib.py` | shared parsing helpers | Required by all |
| `build_catalog.py` | maintainer: rebuild library catalog | Kept (maintainers) |

Gotchas found: (1) paths with spaces must be quoted (the working dir here has one); (2) **the library has no
food/beverage/wellness/legal industry** — it skews to tech. Coffee/bakery/yoga searches must use `--subject` /
`--query` (e.g. `--subject coffee` → java, coffeescript, caffe2, mocha — all steaming cups: itself a lesson in
the cliché); (3) `svg_audit.py` only reads SVG, so PNG/photo uploads need a wrapper to go through the test sheet.

## templates/
`brand-guidelines-template.md`, `presentation-spec.example.json` → **Reuse** unchanged.

## assets/library/
1,432 SVGs + `catalog.json`, `classifications.json`, `stats.json`, `gallery.html` (14 MB). → **Reuse** unchanged
(study + look-alike checks only; TRADEMARKS.md applies).

## evals/evals.json (repo root)
3 design-output prompts (Kiln coffee, Tidepool dev tool, critique+refresh), no assertions. → Not reused; logo-coach
gets its own `skills/logo-coach/evals/evals.json` with 9+ coaching prompts and assertions.

## tools/
`smoke_test.py` (CI, logo-design only) and `package_skill.py` (dist zips for logo-design). → Kept; logo-coach gets
parallel packaging (`dist/logo-coach.zip`, `dist/logo-coach-lite.zip`).
