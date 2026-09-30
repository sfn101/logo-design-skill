# Critique Rubric (Coach Mode, Stage 5)

The scored rubric for reviewing the designer's own marks. Built on the original skill's critique scorecard, with
anchors for what a 1, 3 and 5 actually look like, and a principle file behind every criterion. Read this before
every critique round.

## Contents
1. How to run a critique round
2. The ten criteria (with 1 / 3 / 5 anchors)
3. Writing a critique point that teaches
4. Common diagnoses (symptom → cause → what to try)
5. Output format (chat + report JSON)
6. Special cases: raster files, sketches, "tell me it's perfect"

---

## 1. How to run a critique round

1. **Context first.** A logo can only be judged against its brief. If you don't know the business, audience and
   adjectives, ask one question or state your assumptions in one line.
2. **Two-second read.** Look at the mark once, small, and write what a stranger would see, feel and remember.
   This is the most honest data you'll get — record it before analysing.
3. **Run the tools** (never skip for SVG; for PNG/JPEG wrap first — see §6):
   ```bash
   python3 scripts/svg_audit.py their-mark.svg
   python3 scripts/preview_sheet.py their-mark.svg --refs <3–5 category marks> -o tests.html
   python3 scripts/render_png.py tests.html -o tests.png --width 1400 --height 2400
   ```
   Look at `tests.png` yourself. The 16 px row, one-colour row, squint blur and the shelf are where most marks
   fail. For the shelf, choose references with `search_library.py --subject … --format paths` or
   `--industry … --format paths` (the library skews to tech; use `--subject`/`--query` for food, wellness, legal…).
4. **Look-alike check.** `search_library.py --subject <main motif>` — and your own knowledge of famous marks. If it
   resembles something known, say so plainly and name it; this is the most valuable thing a mentor can catch.
5. **Score all ten criteria** (§2) with one line of evidence each and the principle behind it.
6. **Prioritise** the three changes with the biggest impact. Describe *what* to change and *why*, never draw it.
7. **Hand it back**: the designer decides what to try; you set the next exercise and, when useful, a reading.
8. Optionally render the written record: `scripts/rubric_report.py critique.json -o report.html --png report.png`.

The tool output is evidence, not the critique. Translate each finding into what it means for the viewer
("the steam lines are 1.2 units wide — they disappear below 32 px, so the cup reads as a plain mug on a tab").

---

## 2. The ten criteria

Score 1–5. Use "n/a" only where a criterion truly doesn't apply (typography on a symbol with no lockup yet). The
total is a rough guide; **one fatal flaw** (illegible small, looks like a known mark, unfortunate reading)
outweighs any total — call it out separately.

### 1. Concept strength → `principles.md` §2.7 (Focus on one thing), §2 "Pose a question (lightly)"
- **1** No idea beyond depicting the product; or three ideas fighting. Can't be said in one sentence.
- **3** One idea is present and sayable, but it's the first idea anyone would have, or it needs explaining.
- **5** One clear idea with an ownable twist; the viewer "gets it" in a glance and enjoys the small click.
*Ask:* "Say the idea in one sentence without mentioning shapes."

### 2. Relevance to brief → `principles.md` §2.4, §5 (Relevance vs. literalness); `discovery-brief.md` §5
- **1** Tone contradicts the adjectives (sharp and cold for a warm bakery), or it fits any business.
- **3** Tone roughly fits; relevance comes from literal depiction rather than attitude.
- **5** Shape, weight, rhythm and type all carry the adjectives; it evokes rather than illustrates.

### 3. Distinctiveness vs. category → `principles.md` §2.5, §6 (Familiarity test); `testing-checklist.md` §4
- **1** Blends into the shelf; uses the category's top clichés as-is; or resembles a known mark.
- **3** Uses a familiar sign with a partial twist; stands out a little on the shelf.
- **5** Instantly separable on the shelf, still reads as the right world; no look-alikes found.

### 4. Simplicity → `principles.md` §2.3, §4 (Simple is not plain)
- **1** Elements that exist because they were fun to draw; details compete; or so plain it's generic.
- **3** Mostly reduced, one or two non-essential parts remain.
- **5** Nothing to remove, and one detail makes it ownable.

### 5. Construction & geometry → `visual-techniques.md` §1; `svg-construction.md` §2–3; `svg_audit.py`
- **1** Near-miss angles, lumpy curves, inconsistent stroke weights and radii, accidental notches at junctions.
- **3** Clean overall; a few inconsistent radii or angles; one or two messy junctions.
- **5** A visible system: consistent unit, radii, angles (0/15/30/45/60/90°), clean junctions, few anchors.

### 6. Optical balance → `visual-techniques.md` §2 (Balance), §3 (Overshoot, bone effect, optical centre)
- **1** Accidental tilt, top-heavy mass, round forms looking smaller than straight ones.
- **3** Stable, but uncorrected: geometric centring, no overshoot, pinched rounded rectangles.
- **5** Feels effortlessly settled; corrections are invisible but present.

### 7. Legibility & scalability (16 px) → `principles.md` §2.8; `testing-checklist.md` §1
- **1** Mush at 32 px; letters unreadable; gaps close.
- **3** Survives 32 px; at 16 px only a blob remains, but the blob is at least recognisable.
- **5** The idea survives 16 px (or a deliberate small-size cut exists); also holds up very large.

### 8. One-colour performance → `testing-checklist.md` §2; `color.md` §1 (Order of operations), §5
- **1** Depends on colour or gradient to exist; turns into a blob in black; reversed version breaks.
- **3** Works in black; reversed looks heavier (irradiation) or loses a detail.
- **5** Equally strong in black, white-on-dark and greyscale; colour adds, never rescues.

### 9. Typography pairing → `typography.md` §1 (Type study), §4 (Letterform craft), §5 (Lockups)
- **1** Default stock font, unmodified; clashing geometry with the symbol; poor spacing; live text in a "final".
- **3** Appropriate voice, but off-the-shelf and loosely spaced; symbol and type share little.
- **5** Custom or customised letters, optical spacing, and symbol and type share a logic (radii, weights, angles).

### 10. Longevity → `principles.md` §2.9, §7 (Longevity vs. trend)
- **1** Built on an effect (gradient, glow, trendy font); will date within a few years.
- **3** Mostly conceptual, one trendy element.
- **5** Built on an idea and a durable form; could run unchanged for a decade.

---

## 3. Writing a critique point that teaches

Every point has four parts: **what you see → why it matters → the principle → what to try (in words)**.

> The three steam lines are 1.2 units wide and vanish below 32 px (see the 16 px row), so on a browser tab the
> mark reads as a generic mug. *Principle: think small — `principles.md` §2.8.* Try: either drop the steam
> entirely and see if the idea survives without it, or make it one bold shape instead of three hairlines.
> Compare how the Chermayeff & Geismar marks in *Identify* hold together at stamp size.

Rules of thumb:
- **Point at evidence.** "The diagonal is 43.5°, not 45° (audit: near-miss-angle)" — not "the angle feels off".
- **Name the principle and the file.** The designer should be able to go read it.
- **Describe, don't draw.** Offer options in words ("try thickening", "try removing", "try a 45° cut"), plus a
  real-world example to study. Never produce a corrected SVG or a "here's what I mean" redraw in Coach Mode.
- **Praise only what earned it**, with the same specificity as criticism ("the counter of the R echoes the
  outer circle — that's real consistency, keep it").
- **Critique the work, not the person.** Direct is kind; vague is not.
- **Ask one question back** when the designer's intent is unclear ("Is the bean meant to read as a flame?").

---

## 4. Common diagnoses

| Symptom | Likely cause | What to try (in words) |
|---|---|---|
| Mush at small sizes | Too many elements, hairlines, small gaps | Remove details; thicken strokes; open gaps; plan a small-size cut |
| Generic / template-like | Stock font; cliché symbol (globe, swoosh, bean, leaf) | Customise a letter; find the twist in the name or process, not the product |
| Dated | Effects (gradients, bevels, glows), trend fonts | Flatten; rebuild the idea without the effect; choose a more durable type voice |
| Busy | Two or three ideas competing | Pick one; move the others into the wider identity system |
| Symbol and type unrelated | Different geometry and weight logic | Share radii, weights, angles; rebalance relative size |
| Unstable | Accidental tilt, top-heavy mass | Widen the base; correct axes; check optical centre |
| Circle looks small next to letters | No overshoot | Let round forms overshoot 1–3 % |
| Rounded rectangle looks pinched | Bone effect | Smooth the curvature transitions |
| Reversed version looks bold | Irradiation | Plan a slightly thinned reversed file |
| Hidden meaning nobody sees | Too subtle or too complex | Make it the bonus, not the point — or simplify until it reads |
| Feels familiar | Memory of an existing mark | Search it down; if it's someone else's, change it significantly |

---

## 5. Output format

### In chat
```markdown
## Critique — <project>, round <n>
**Two-second read:** <what a stranger sees and remembers>
**What works:** <1–3 bullets, only if earned, each with the reason>

| Criterion | Score | Evidence | Principle |
|---|---|---|---|
| Concept strength | 2 | … | principles.md §2.7 |
| … (all ten) | | | |
**Total:** <n>/50 (rough guide) · **Fatal flaw:** <if any>

**Top 3 changes, in priority order** (what and why — you decide how):
1. …
2. …
3. …

**Your next move:** <the exercise for the next round, e.g. "3 versions without the steam, one-colour only">
**Study:** <one real example or reading, with the reason>
```
Attach the test-sheet PNG (and the report PNG if you made one). End by handing the decision back: which change
they want to tackle first, or whether they disagree with any score (disagreement is useful — ask why).

### Report JSON (for `scripts/rubric_report.py`)
`python3 scripts/rubric_report.py --template` prints a starter. Fill every criterion with a note and a
principle; the script flags vague notes, missing principles and more than three top changes.

---

## 6. Special cases

- **PNG / JPEG exports.** `python3 scripts/raster_wrap.py export.png` wraps the image as SVG so
  `preview_sheet.py` can run the size ladder, squint, mirror and context tests. `svg_audit.py` will flag the
  raster (correctly) and can't measure anchors or angles — ask for the SVG if construction is the question.
  One-colour tests on a photo with a paper background become solid squares; say that those tests need a cut-out
  or vector version rather than reporting them as failures.
- **Sketch photos.** Don't score construction or one-colour on pencil thumbnails — judge idea, relevance,
  distinctiveness, simplicity and small-size potential. Use `coaching-workflow.md` Stage 4 instead of this rubric.
- **"Tell me it's perfect."** The designer wants confidence. Real confidence comes from knowing what's strong and
  what to fix. Acknowledge the ask warmly in one line, then give the honest critique — lead with what genuinely
  works, keep the tone kind and direct, and frame the top changes as the path to the confidence they want. Do not
  inflate scores or call it perfect when it isn't.
- **Someone else's logo** (a famous mark, a competitor): same rubric, as a study exercise. Ask the designer to
  score it first, then compare with your scores — the gap is the lesson.
