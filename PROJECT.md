# CEH Diploma — ITGate Academy

> **Read this first. Keep it short. Update the status table, not the rules.**
> One project, one entry doc. Everything else is reference material this file points to.

## 1. What this is

Convert the instructor's CEH training material (`Resources/CEH - Training Material/`,
10 modules, EC-Council 312-50v12 scope) into a complete, session-based, hands-on
ethical hacking course for ITGate Academy — built mainly on a **local VM lab**,
not cloud.

- Source of truth for exam scope: `Resources/EC-Council Materials/` (official CEHv13
  modules — reference only, never copied verbatim; instructor deck is the primary teaching source).
- Audience / prerequisites: to be confirmed with instructor deck assumptions (networking
  + OS basics) — record the decision in `design/scope_decisions.md`.

## 2. Folder map

```
CEH_Course/
├── PROJECT.md              ← this file — the only "read first" doc
├── DECISIONS.md            ← one line per decision, append-only, dated
├── Resources/               ← RAW SOURCE — untouched, reference only, never duplicated
│   ├── CEH - Training Material/
│   └── EC-Council Materials/
├── design/                  ← planning only, ONE folder (not five)
│   ├── topic_map.md          module → session map, dependencies (single sequencing doc)
│   └── scope_decisions.md    what's in/out and why (e.g. mobile/IoT gap)
│      (page/doc structure lives in the skills themselves — not duplicated here)
├── knowledge_base/          ← full official-detail reference, one file per module
│   └── Module_01_Introduction.md  (etc — never copied verbatim into sessions)
├── sessions/                 ← FINISHED teaching material only
│   └── session-01/ (index.html + assets/)
├── labs/                     ← local VM lab — ONE current design, no v2/v3 files
│   ├── lab_design.md         current topology + VM specs (edit in place)
│   ├── setup_guide.md        student build steps
│   └── vm_notes/              per-VM config notes — NO credentials
├── attacks/                  ← CTF-style challenges tied to sessions
├── scripts/                  ← code only, no prose (generators, helpers)
├── exercises/                ← quiz / homework / student activities per session
└── testing/                  ← QA: link check, credential scan, build validation
```

Secrets (lab passwords, keys) live **outside this folder tree** — never committed,
never in any `.md` file. Use placeholders + a local untracked credentials note.

## 3. Standing rules (apply to everything built here)

1. **No versioned files.** Never create `_v2`, `_v3`, `_proposal` copies of a design
   doc. Edit the current file in place; log the change as one line in `DECISIONS.md`.
2. **Delete, don't archive.** Superseded material is removed from the tree, not kept
   "for history" — history lives in the decisions log / git, not as dead files.
3. **Strict folder separation.** Planning (`design/`), finished material (`sessions/`),
   lab (`labs/`), code (`scripts/`), student work (`exercises/`) never mix in one folder.
4. **One canonical entry doc.** Nothing duplicates what `PROJECT.md` says — it links out.
5. **Reuse `Resources/` as-is.** Never copy the source PDFs elsewhere in the project.
6. **Build one session at a time**, approved before the next starts (see §6).
7. **Plain `git`/CLI for publishing** — no browser/computer-use automation for tasks a
   CLI command does directly.
8. **No secrets in the repo**, ever — not even in an "instructor only" folder.
9. **One skill = one responsibility.** Don't create a skill for a one-off task.

## 4. Skills (single responsibility each)

| Skill | Responsibility |
|---|---|
| `ceh-material-intake` | Turn one new source file (PDF or otherwise) into a compact topic-map entry — never a full-content copy |
| `ceh-topic-structure` | Maintain `design/topic_map.md` — the single topic-to-session map and dependency check |
| `ceh-session-html` | Visual/HTML template for one session's teaching page — look only |
| `ceh-session-package` | Fixed doc set for one session (plan, instructor guide, student guide, lab, activity, quiz, homework) — content structure only |
| `ceh-lab-build` | Maintain the ONE current local VM lab design + setup guide — edit in place, no version files |
| `ceh-attack-challenge` | Build one CTF-style attack/investigation challenge tied to a session |
| `ceh-web-research` | Research CEH topics via web search to fill gaps, verify official coverage, enrich knowledge_base files |
| `ceh-chrome-extract` | Extract content from web pages (THM, HTB, etc.) using Claude browser extension when WebFetch can't reach them |
| `ceh-github-publish` | Commit/push the course to GitHub via CLI — credential scan first, no GUI automation |

## 5. Build roadmap (do these phases in order)

| Phase | What | Avoids (from ECIR_Course) |
|---|---|---|
| 0 ✅ | Structure + skills scaffolded | No skill for lab/attack/publish work before |
| 1 ✅ | Scope locked: 10 sessions x 4h; `design/topic_map.md` built and condensed; gap topics identified | Doc sprawl — one topic map, not a topic-map + roadmap pair |
| 2 ✅ | All instructor-deck PDFs extracted to `knowledge_base/` (Modules 1-10); gap topics (Ch.11,12,17,18,19) built from web research; cross-referenced against official CEH v13 syllabus | Building ahead of source content, like the old S4 THM-wait rule |
| 3 ✅ | `labs/lab_design.md` — ONE lab design, baseline built | 4 lab rewrites from scratch |
| 4 | Sessions 1 -> 10, **one at a time, each fully built + approved before the next starts** (see §6 below) | Building multiple sessions/phases in parallel and losing track |
| 5 | `testing/` pass: credential scan, link check, review | No dedicated QA step before |
| 6 | `ceh-github-publish` — push once QA passes | Screenshot-driven GitHub Desktop pushes |

Current phase: **4 (Session 1 built, awaiting review; Session 2 not started)** — see §7 status table.

## 6. How a session gets built (repeat for each, phase 4)

0. New source material arrives → `ceh-material-intake` → `ceh-topic-structure`
   places it in `design/topic_map.md`. (One-time pass for existing Resources,
   then repeat only when new material is added.)
1. Confirm the session's scope against `design/topic_map.md` — don't expand it.
2. Build the session doc set with `ceh-session-package`.
3. Build the HTML page with `ceh-session-html`.
4. Build/attach the lab work: update `labs/` with `ceh-lab-build` only if the lab
   needs to change for this session (most sessions reuse the existing lab as-is).
5. Add one challenge in `attacks/` with `ceh-attack-challenge` if the session ends
   in hands-on exploitation (mirrors the source material's CTF-machine pattern).
6. Log the session as done in the status table below. Move to the next session only
   after review.
7. Publish with `ceh-github-publish` once the session is reviewed and approved.

## 7. Status

| # | Session | Status |
|---|---|---|
| — | Gap-topic content added via web research | done (Ch.11,12,17,18,19 in knowledge_base) |
| — | Lab design (baseline) | done |
| 1 | Foundations, Lab Build & First Contact | built — awaiting review |
| 2 | Footprinting/Recon & Scanning | not started |
| 3 | Enumeration & Vulnerability Analysis | not started |
| 4 | System Hacking I — Access | not started |
| 5 | System Hacking II — Exploitation | not started |
| 6 | System Hacking III — Privesc & Capstone | not started |
| 7 | Malware Threats | not started |
| 8 | Web Application Hacking & SQLi | not started |
| 9 | Sniffing, Social Eng, Wireless & Evasion | not started (gap topics now in knowledge_base) |
| 10 | Mobile, IoT/Cloud & Cryptography | not started (gap topics now in knowledge_base) |

## 8. What to avoid (token/quota discipline)

- Don't re-extract or re-summarize the source PDFs — the topic map already captures
  what's needed; refer to it instead of re-reading raw material.
- Don't regenerate a whole document to change one section — edit in place.
- Don't keep old architecture/design versions "just in case" — delete them.
- Don't use Chrome/computer-use for anything a CLI command (git, file ops) can do.
- Don't build ahead — one session, fully approved, before the next.
