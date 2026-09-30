# Design Journal — keeping a progress log

Growth shows up across sessions, not within one. The journal lets you (and the designer) see recurring mistakes,
what was assigned, and what improved. Read this at the start and end of a coaching session.

## Where it lives

**Writable workspace (Claude Code, a desktop agent with file access):**
- The journal is `design-journal.md` in the current working directory.
- **At session start:** if it exists, read it before responding. Use it to (a) greet the work in context
  ("last time you were working on the Rise R — did you try the 8 variations?"), (b) check whether the last
  assignment was done, and (c) watch for the recurring mistakes it lists.
- **At session end (wrap-up):** append the entry below. Create the file with a one-line header if it doesn't
  exist. Never rewrite or delete earlier entries — the history is the point. Tell the designer it's been saved.
- Ask once before creating the file in a new folder ("Want me to keep a design journal here?"); after that, just
  append at wrap-up.

**No writable workspace (Claude.ai, mobile):**
- At wrap-up, output the entry as a copy-ready block (a fenced markdown block) and say: "Paste this into your
  journal. Next session, paste your last few entries at the start so I can pick up where we left off."
- If the designer pastes previous entries at the start, treat them exactly like the file.

## Entry format

```markdown
## <YYYY-MM-DD> · <project> · <stage reached>
- **Worked on:** <what was reviewed/made>
- **Improved:** <specific, with evidence — "16 px now reads; gap opened from 4 to 10 units">
- **Recurring:** <patterns seen again — "tiny details (3rd time)", "stock sans unmodified">
- **Scores (if critiqued):** concept 3 · relevance 4 · distinct 2 · simple 3 · construction 3 · optical 3 · 16px 2 · one-colour 4 · type 2 · longevity 3
- **Assigned:** <drill + reading>
- **Open decisions:** <what the designer must decide>
```

## Spotting patterns

When reading the journal, look for:
- The same criterion scoring ≤ 2 across projects → that's the "practise next" skill; pick a drill from
  `practice-drills.md` that targets it.
- Assignments not done → ask about it kindly; adjust size (a 15-minute drill beats an ignored 2-hour one).
- Scores rising → name it. Progress the designer can see is what keeps them practising.
- Stage skipping (always jumping to digital, never hitting the sketch quota) → name the habit and its cost.
