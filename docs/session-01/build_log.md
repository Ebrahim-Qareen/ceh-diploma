---
session: 1
status: delivered — enhanced 2026-08-23
---

# Session 1 — Build Log

What was built, what changed, and what is still open. Chronological within each phase.
Rationale for each decision lives in `DECISIONS.md`; this file is the working detail.

## Current state

- **24 pages**, ~203 KB single HTML file at `sessions/session-01/index.html`
- **18 inline SVG diagrams** — 2 click-to-reveal, 1 animated with replay
- **8 screenshot slots** — 7 filled, 1 missing (see Open items)
- **6 practice blocks** linking **20 verified external rooms**
- Break timer, 10-question self-scoring quiz, sidebar nav, progress bar, keyboard nav
- Published: `github.com/Ebrahim-Qareen/ceh-diploma` → `docs/session-01/`

## Build history

### Phase 1 — initial build
Original 217-line single-scroll page. Rejected by the instructor as "not related to
what I want". Rebuilt against the eCIR diploma site as the design reference (paged
navigation, sidebar, progress bar, callout boxes), then recoloured to a CEH-specific
palette so it has its own identity rather than reusing eCIR's tokens.

### Phase 2 — narrative restructure
Rebuilt again from 17 topic-per-page slides into a **22-page integrated narrative**.
Every page now opens with a `.box.intro` explaining why it follows the previous one.
Added the ice-breaker, the 4-page prior-knowledge recall block, and the virtualization
block sourced from the instructor's own "Virtual Machines" deck.

VM build moved out of class time into homework — class covers virtualization and lab
design as theory, and the reclaimed time went to the recall block and a longer
first-contact lab.

### Phase 3 — student-facing cleanup
- Removed all instructor-only meta boxes (`Instructor: what to listen for`) — students
  receive these files.
- Renamed the ice-breaker heading `Ask the room first` → `Discuss first` (13 places).
  The old wording was a stage direction being read aloud to the room.
- Swapped the NAT/BRIDGED labels on the network-modes diagram at instructor request
  (my technical objection is recorded in `DECISIONS.md`).
- Full-cast table: added icons per hacker type (6 cropped from a supplied infographic
  with connected-component background removal, 3 hand-drawn SVG badges for
  APT / Suicide hacker / Insider), added an APT row.
- Fixed persistent name-wrapping — root cause was the CSS Grid `min-width:auto` bug,
  not text wrapping. See `design/design_system.md` §7.

### Phase 4 — enhancement (2026-08-23)
Two new pages:
- **P08 "What We're Actually Protecting"** — CIA + Authenticity + Non-repudiation as a
  click-to-reveal diagram, each pillar opening a real breach that broke *that* property.
  This closed the one official Module 1 objective the page never covered.
- **P22 "Your Practice Plan"** — ordered self-study roadmap plus the platform
  free-vs-premium comparison.

Diagrams made dynamic:
- 5-phase methodology → click-to-reveal per phase (attacker tooling, SOC detection with
  real event IDs, ATT&CK tactic ID, session cross-reference).
- TCP handshake → animated packet flow with a replay button.
- Both mechanics were added to the **shared** CSS/JS so Sessions 2–10 reuse them.

Lab extended with a Step 5 stretch goal (`nmap -O`, `nmap --script=default`) for pairs
who finish early.

## Verification performed

Playwright across 1400 / 1100 / 900 / 700 / 480 px:
- Document-level horizontal overflow: **none at any width**
- 24 pages, 24 sidebar entries
- 2 interactive diagrams, 10 nodes, 10 detail panels, **no orphans**
- All 10 nodes click-tested: each opens exactly one panel
- No console or page errors
- All 20 external link hosts valid

## Open items

1. **MITRE ATT&CK Navigator screenshot missing.** The original low-res file
   (480×320) no longer exists on the instructor's device. Page 12 renders the
   labelled placeholder. Awaiting a replacement screenshot.
2. **Session runs 246 min against a 240-min slot** (+6 from the new CIA page).
   Two absorb options documented in `session_plan.md`; instructor to choose.
3. **GitHub Pages not yet enabled.** Repo and `/docs` structure are ready; needs
   Settings → Pages → `main` / `/docs` in the GitHub web UI.
4. **AD domain** still not in the lab — flagged for revisit before Session 4.

## Files owned by this session

```
sessions/session-01/index.html          the teaching page
sessions/session-01/assets/img/         8 screenshots + 6 cast icons
sessions/session-01/session_plan.md     timing, objectives, delivery notes
sessions/session-01/instructor_guide.md
sessions/session-01/student_guide.md
sessions/session-01/guided_lab.md
exercises/session-01/                   quiz, homework, activity, lab report template
```

Shared (do not fork per session): `sessions/assets/css/ceh.css`,
`sessions/assets/js/session.js`, `sessions/index.html` (dashboard).
