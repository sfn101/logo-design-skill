# Sketch Mode and Remix

Sketch Mode exists for when the designer is stuck and explicitly asks for starting points. It produces **raw
material to react to**, not designs. The designer's hand does the real work afterwards. Read this in full before
producing any sheet.

## Contents
1. When it's on (and when it isn't)
2. The sheet: rules
3. The angle list (for range)
4. Drawing thumbnails in SVG — keep them rough
5. Labels
6. Building the sheet
7. The stopping rule and the hand-back
8. Remix: variations of the designer's own sketch
9. Fallback: "just make me a finished logo"

---

## 1. When it's on

Only on an explicit request: "sketch mode", "give me starting points", "rough ideas", "I'm stuck, spark some
ideas", "quick thumbnails", "variations of my sketch". Anything else — including "what do you think of my logo?",
"help me with a brief", "which sketch should I push?" — is Coach Mode, and Coach Mode never draws marks.

If the request is ambiguous ("any ideas for Stillroom?"), offer both in one line: prompts to spark their own map
(Coach Mode) or a rough thumbnail sheet (Sketch Mode) — their call.

---

## 2. The sheet: rules

- **12–20 thumbnails**, on **one** concept sheet image. Not 3 polished concepts; not 40.
- **Greyscale, single colour.** Draw everything in black; the rough sheet renders it as graphite grey. No colour
  versions, no gradients, no second tone.
- **Deliberately loose.** Simple primitives and a few paths. No type refinement (a letter can be a plain path
  or a stock-looking skeleton), no optical corrections, no audit passes, no cleanup iterations. Speed over
  finish — the looseness tells the designer "this is a prompt, not a proposal".
- **Range.** Spread across the angles in §3, **no more than two thumbnails per angle**. Aim for at least six
  different angles on a 12–20 sheet. Range means different *forms*, not different tags: two thumbnails that are the
  same shape (an S lying flat, tagged once as letterform and once as typographic play) count as one — replace one.
- **Letter test.** Any thumbnail built on a letter must still read as that letter at a glance. If it reads as
  another letter or a symbol (a T that becomes a Y, an f or the Aries sign), fix it or say so in its label.
- **Respect the brief.** If a brief or clichés list exists (or the category has obvious clichés — lotus and
  zen circle for yoga; wheat for bakeries; cups and beans for coffee), don't use them unless the thumbnail is a
  deliberate fresh form, and label it as such.
- **Look-alike check.** Before finalising, glance at your strongest motifs against the library
  (`search_library.py --subject <motif>`) and famous marks. Drop or change anything that reads as an existing logo.
- **One label per thumbnail** (§5).

---

## 3. The angle list

Use these tags (they're what `concept_sheet.py --tags` expects and counts):

| Tag | What it means |
|---|---|
| `wordmark` | The whole name as the mark, with one typographic move (a cut, a joined pair, a changed letter) |
| `letterform` | A single initial carrying the idea |
| `lettermark` | Two or more initials combined (monogram) |
| `pictorial` | A recognisable thing — but not the product itself |
| `abstract` | Pure form expressing an attribute (stillness, rise, flow) |
| `emblem` | Name and symbol inside a container (badge, seal, stamp) |
| `negative-space` | The idea lives in the gap or figure/ground |
| `metaphor` | A borrowed image standing for the brand's promise or process |
| `typographic-play` | Letters doing something unexpected: stacking, rotation, a letter as an object |
| `mascot` | A character (use sparingly; rarely right for small businesses that want calm) |
| `pattern` | A repeatable unit that could also be the mark |

`mark-types.md` explains each in depth.

---

## 4. Drawing thumbnails in SVG — keep them rough

- One SVG per thumbnail, `viewBox="0 0 200 200"`, black fills/strokes only, no `<text>` for the mark itself
  (a label is on the sheet, not in the art). Strokes are fine here (they're thumbnails, not masters).
- Aim for 1–6 elements each. If a thumbnail takes more than ~10 lines of SVG, it's too finished — cut it back.
- Don't iterate on a thumbnail. Draw it once, render the sheet once, look, fix only genuine breakage (a shape off
  the canvas, an unreadable label), done.
- Write the thumbnails into a working folder (e.g. `sketch-mode/<brand>/t01.svg … t16.svg`), not into the
  skill folder.

---

## 5. Labels

Each thumbnail gets a short label: **the idea + the word-map link it came from**.
- `--names`: the idea in ≤ 5 words — "S + held breath", "K + kiln arch", "Pause mark in a circle".
- `--notes`: the link — "still → breath held", "room → doorway", "stillness → the gap between".
- `--tags`: the angle from §3.

A label that could describe a competitor's logo ("lotus flower") is a sign the thumbnail is a cliché.

---

## 6. Building the sheet

```bash
python3 scripts/concept_sheet.py sketch-mode/stillroom/t*.svg --rough \
    --title "Stillroom — rough thumbnails" \
    --names "S + held breath" "Doorway pause" … \
    --notes "still → breath held" "room → threshold" … \
    --tags letterform negative-space … \
    -o sketch-mode/stillroom/sheet.png
```
The script warns if the count is outside 12–20 (6–10 with `--remix`) or an angle appears more than twice — fix
the set if it warns. View the PNG yourself before showing it.

---

## 7. The stopping rule and the hand-back

**Stop at the sheet.** In Sketch Mode, never:
- develop a thumbnail further on your own initiative,
- produce colour versions, lockups, mockups, a test sheet of your thumbnails, or a kit,
- pick a winner for the designer (you may say which 2–3 *you'd* find most promising and why, as one opinion).

End every Sketch Mode reply by handing back, in this shape:
```markdown
<sheet image>
These are rough prompts, not designs — steal a gesture, not a logo.
**Your move:** pick 2–3 that spark something and develop them by hand (8+ variations each, on paper).
When you have versions, send them over and I'll switch back to Coach Mode and critique them.
```

---

## 8. Remix: variations of the designer's own sketch

Trigger: the designer uploads their sketch and asks for variations ("give me variations of my sketch",
"remix this", "other ways to build this idea").

- Look at the sketch; describe the core idea back in one sentence to confirm you've understood it.
- Produce **6–10 rough variations of *their* idea** — same idea, different **construction** (geometric vs.
  organic), **weight** (mono-line vs. solid), **angle** (how the elements meet), **geometry** (circle, square,
  grid), **proportion**, or **figure/ground**. Don't swap in a different idea.
- Same rough style and sheet: `concept_sheet.py … --rough --remix` with labels describing the change
  ("heavier stroke, wave closes into a circle"). Tags can repeat in Remix.
- Apply the letter test to every variation; in the reply, name any variation where the letter stops reading (it
  may still be interesting, but the designer should know the cost).
- Same stopping rule. End with: "Which of these changes interests you? Take it back to paper and push it — then
  bring me your version for a critique."

---

## 9. Fallback: "just make me a finished logo"

If the designer explicitly asks for a full finished design (not starting points), say **one sentence** first —
e.g. "Quick reminder: Coach Mode can walk you through designing this yourself — but if you want me to design it,
I'll do that." Then respect their choice: follow the sibling `logo-design` skill's Design workflow (brief →
concepts → build → test → concept checkpoint). If `logo-design` isn't installed, follow its principles from this
skill's references (`process.md`, `svg-construction.md`, `testing-checklist.md`). Don't lecture or repeat the
reminder later in the conversation.
