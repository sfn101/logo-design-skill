# Inspiration Sources — where to study real work, and how

Real work by human designers is the best teacher. This file lists where to find it and how to study it so it
makes the designer better, rather than making their work derivative. When web search is available, use these to
find specific case studies; give **links plus your own one-line reason**, never copied text or images.

## Contents
1. Where to look
2. How to study a mark (the analysis routine)
3. How to study a case study
4. Study copies — for learning, never for sale
5. Using the local library alongside

---

## 1. Where to look

### Critique and case studies
- **Brand New** (UnderConsideration) — `underconsideration.com/brandnew` — reviews of new identities and redesigns,
  with before/after and reader votes. Best for: seeing how a professional critic reasons, and the rationale
  studios give. Assign one review, then ask the designer to write their own verdict *before* reading the review.
- **Behance case studies** — `behance.net` (search "brand identity" + category) — full process decks from
  studios and freelancers. Quality varies widely: teach the designer to tell a considered case study
  (research, rejected routes, system, applications) from a mockup dump.
- **BP&O** (Richard Baird) — `bpando.org` — thoughtful write-ups on identity and packaging projects.
- **Fonts In Use** — `fontsinuse.com` — real-world typography indexed by typeface, format and industry. Best for:
  type-pairing research and "what does this category set its type in?".

### Archives of marks
- **Logobook** — `logobook.com` — a curated archive of (mostly modernist) marks searchable by shape and theme.
  Great for range and for the familiarity check on a motif.
- **LogoLounge** — `logolounge.com` — a large logo database and the annual trend reports (paid tiers). Useful for
  seeing what's overused right now; the trend report is a list of things to be careful with, not to follow.
- **Letterform Archive** — `letterformarchive.org` — lettering and type history, with an online archive.

### Studio portfolios (study complete systems, not just marks)
- **Pentagram** — `pentagram.com` — partner-led identity work across every sector, with project write-ups.
- **Chermayeff & Geismar & Haviv** — `cghnyc.com` — decades of simple, durable marks; pair with the book *Identify*.
- **Sagmeister & Walsh** — the studio split in 2019 into Sagmeister Inc. and &Walsh; both portfolios show
  expressive, idea-first identity work that breaks conventions on purpose.
- **Koto** — `koto.studio` — contemporary identity systems, strong on motion and digital brands.
- Also worth following: Collins, DesignStudio, Base Design, Mucho, Studio Dumbar, Wolff Olins, Landor.

### Annuals and awards
- **Communication Arts** annuals, **Type Directors Club** (TDC) annual, **D&AD** annual, **Brand New Awards**,
  **The Dieline** (packaging — useful for bakery/coffee/food projects). Annuals show the ceiling of the craft.

When you recommend any of these, pick the one that fits the current task. "Look at Brand New" is not an
assignment; "Read Brand New's review of <a specific café or bakery rebrand you found>, and write down the one
idea in one sentence" is.

---

## 2. How to study a mark (the analysis routine)

Teach this routine and ask the designer to write the answers down:
1. **Brief backwards.** Who is it for, what should it feel like, what's the competition? (Guess, then check.)
2. **The one idea.** Say it in one sentence. If you can't, is that a weakness or is it an abstract mark that
   earns meaning through use (`principles.md` §5)?
3. **Construction.** What primitives? What grid or unit? Which angles repeat? Where are the optical corrections?
   (Render library files at large size to see this — `render_png.py`.)
4. **Small and one-colour.** How does it survive 16 px and black-only? What was sacrificed?
5. **Distinction.** What does the rest of its category look like? What did this mark refuse to do?
6. **The system.** How does the mark seed the rest of the identity (patterns, type, motion)?
7. **Steal the lesson, not the form.** Write one transferable principle ("use the counter of the letter as the
   second shape") — never "do a mark like this".

---

## 3. How to study a case study

- Read the problem statement first; stop; write what you would have done.
- Note the rejected routes (if shown) — what was wrong with them? That's where the judgement is visible.
- Note how the rationale is written: does it lead with the insight or the aesthetics? (Useful for Stage 6.)
- Look at the applications: which ones prove the system works, which are just decoration?

---

## 4. Study copies — for learning, never for sale

Copying a master's mark by hand (or redrawing it from memory) is one of the oldest ways to learn construction —
painters copy paintings in museums for the same reason. The rules are strict:
- **For learning only.** A study copy stays in the sketchbook or a private practice file. It is never shown as
  your work, never posted as original, never sold, never used for a client — not even "inspired by".
- **Label it.** Write the original designer/studio and the mark's name on every study copy.
- **Aim for understanding.** Redraw from memory first, then compare with the original: what did you get wrong
  about proportions, angles, weights? That gap is the lesson (see the memory drill in `practice-drills.md`).
- **Trademarks remain their owners'.** The bundled library logos are trademarks (see `TRADEMARKS.md` in the
  repository); the same goes for anything you find online.
- If a new client idea starts to look like a study copy, it's someone else's — change it or drop it
  (`principles.md` §6, the familiarity test).

---

## 5. Using the local library alongside

The bundled library (1,432 marks, mostly tech brands) is fast and offline:
```bash
python3 scripts/search_library.py --technique negative-space --exemplary --limit 8
python3 scripts/search_library.py --subject bird --format table
python3 scripts/search_library.py --type wordmark --type-style serif --exemplary
python3 scripts/search_library.py --industry developer-tools --summary
```
`references/library-guide.md` has curated lessons by technique with example files. For non-tech categories
(food, wellness, legal, craft), the library shows techniques and constructions well but not category
conventions — use the live sources above and your own knowledge for those.
