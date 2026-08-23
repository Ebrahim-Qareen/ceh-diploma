# CEH Diploma — ITGate Academy

Course build for the CEH Diploma track at ITGate Academy: session pages, lab
design, instructor and student materials.

**Live site:** https://ebrahim-qareen.github.io/ceh-diploma/

## Structure

- `docs/` — the published site (GitHub Pages source). `index.html` is the
  course dashboard; each `docs/session-XX/` folder is one session's page
  plus its own assets.
- `design/topic_map.md` — the single source of truth for which topic goes
  in which session.
- `design/design_system.md` — the shared visual/interaction component
  reference every session page is built from: colour tokens, callout boxes,
  diagram rules, interactive/animated mechanics, and the pre-publish
  verification checklist. **Read before building any session page.**
- `design/practice_platforms.md` — verified external lab rooms
  (TryHackMe / OverTheWire / HTB / picoCTF) with confirmed access tiers,
  used by the "Practice this topic" blocks.
- `docs/session-XX/build_log.md` — per-session build history, verification
  results, and open items.
- `labs/` — lab topology and the student VM setup guide.
- `exercises/` — per-session homework, quizzes, and activities.
- `knowledge_base/` — condensed study notes per CEH module.
- `DECISIONS.md` — running log of build decisions and why they were made.
- `PROJECT.md` — project overview and conventions.

Raw vendor/source PDFs are kept local only (not published here) — see
`.gitignore`.
