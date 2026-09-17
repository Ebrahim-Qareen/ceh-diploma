# CEH Diploma — ITGate Academy

![Status](https://img.shields.io/badge/status-in%20build-F59E0B?style=flat-square)
![Site](https://img.shields.io/badge/site-GitHub%20Pages-2563EB?style=flat-square)
![Stack](https://img.shields.io/badge/stack-HTML%20%C2%B7%20Python-1F2937?style=flat-square)
![License](https://img.shields.io/badge/material-%C2%A9%20ITGate%20Academy-6B7280?style=flat-square)

Instructor-led Certified Ethical Hacker (EC-Council 312-50) diploma track: session pages, lab design, instructor and student materials, and a verified index of practice platforms. Third course in the ITGate path: **SOC Analyst → CEH → eCIR → eCDFP**.

**Live site →** https://ebrahim-qareen.github.io/ceh-diploma/

## How the course is built

- **One topic map, one order.** `design/topic_map.md` is the single source of truth for which topic lands in which session and what it depends on.
- **One design system.** Every session page is built from `design/design_system.md` — colour tokens, callout boxes, diagram rules, interactive mechanics and the pre-publish checklist — so all sessions look and behave identically.
- **Practice you can actually reach.** `design/practice_platforms.md` lists TryHackMe / OverTheWire / HTB / picoCTF rooms with their access tier confirmed before they are linked from a "Practice this topic" block.
- **Attacks are taught with their detections.** Each offensive technique is paired with what a defender sees — logs, alerts, ATT&CK technique ID — because the students continue into the SOC and IR tracks.
- **Per-session build logs.** `docs/session-XX/build_log.md` records what was built, what was verified and what is still open.

## Repository layout

| Path | Purpose |
|---|---|
| `docs/` | Published site (GitHub Pages source). `index.html` is the course dashboard; `docs/session-XX/` is one session page plus its assets |
| `design/topic_map.md` | Topic → session mapping and dependencies |
| `design/design_system.md` | Shared visual/interaction component reference — read before building any page |
| `design/practice_platforms.md` | Verified external lab rooms and access tiers |
| `labs/` | Lab topology and student VM setup guide |
| `exercises/` | Per-session homework, quizzes and activities |
| `knowledge_base/` | Condensed study notes per CEH module |
| `DECISIONS.md` | Running log of build decisions and why |
| `PROJECT.md` | Project overview and conventions |

Raw vendor/source PDFs are kept local only and are excluded by `.gitignore`.

## Running locally

```bash
python3 -m http.server --directory docs 8000
```

No build step and no external dependencies — the site renders on a classroom machine with no internet.

## Credits and licence

Course material © ITGate Academy. Built against the EC-Council CEH v13 syllabus; vendor material is referenced, never republished. Practice platforms are linked, not rehosted.

Maintainer: Ebrahim Mohamed — [LinkedIn](https://linkedin.com/in/EbrahimMohamed)
