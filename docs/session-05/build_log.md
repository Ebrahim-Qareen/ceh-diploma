---
session: 5
title: Build Log — Session 5
---

# Session 5 — Build Log

**Title:** System Hacking II — Exploitation, Shells & Payloads (CEH Module 6 pt2)
**Spine:** "You found the way in and got the key (S4). This is where you turn it into a shell."
**Built:** 2026-09-11. Reuses the shared design system (`ceh.css` / `session.js`) unchanged — no per-session CSS/JS.

## What was built
- **27-page `index.html`** assembled by `s5build/` (build.py + pages.py + pages2.py + docs.py). Each theory concept is paired with a **simple "Prove it" mini-lab** (instructor request), plus 10 milestone labs.
- **Full package:** session_plan, instructor_guide, student_guide, guided_lab, build_log (this file) in `docs/session-05/`; student_activity, quiz, homework, foothold_record_template in `exercises/session-05/`.
- **Cumulative team report** extended to S2+S3+S4+S5 (`docs/session-05/report.html`) — new `s5-foothold` key added to `scripts/gen_session_report.py`; shared storage key + namespaced ids, so it carries a team's earlier answers forward and exports the whole engagement.

## Visuals (stepped, "watch it" per instructor preference)
- **6 stepped `.dgm.pktflow`** flows (Back/Play/Next): the kill-chain bridge, the **EternalBlue worked chain**, **bind vs reverse**, and the **buffer-overflow stack** (fuzz → crash → offset → EIP → JMP ESP → shellcode), plus two more.
- **5 `.dgm.interactive`** click-to-reveal diagrams: the exploitation pipeline, the Metasploit module model, staged vs stageless, shell-upgrade path, and the reverse-shell SOC-flip attack→log map.
- **SIM-SCREENs** for msfconsole (vsftpd, EternalBlue), impacket-psexec, the reverse handler and the BOF `nc` catch. **6 self-scoring MCQs.**
- Real msfconsole/meterpreter captures deferred (no Windows/AD in the build environment) — the sims stand in and cannot 404.

## Labs (10 + 8 mini-labs, ~54% hands-on)
Manual vsftpd (root) · same via MSF · EternalBlue → SYSTEM · bind-blocked vs reverse-out · msfvenom+handler · shell upgrade · credential access (S4 cred) · guided buffer overflow (vulnserver+Immunity+mona primary, Kali gdb fallback, saved state at each step) · **reverse-shell detection rule** (Sigma worked + SPL/KQL skeletons) · **foothold record** (deliverable, S6 input). Deliberate failures kept: handler-down (no stage), bind blocked by firewall, bad-chars mangle the shellcode.

## Currency verified before teaching
EternalBlue module path `exploit/windows/smb/ms17_010_eternalblue` (current; check = `auxiliary/scanner/smb/smb_ms17_010`) · msfvenom staged `/` vs stageless `_` · encoding ≠ AV evasion · Metasploitable2 is 2012-era · naive stack overflow is a teaching model (DEP/ASLR/canary are the countermeasure).

## Practice rooms (TryHackMe API-verified free)
`blue` (MS17-010 — Lab 3 on the platform), `metasploitintro`, `ice`, `blaster` = all free. BOF rooms `bufferoverflowprep`/`gatekeeper` were API rate-limited at build time — flagged **verify tier on the day** before linking; the guided Lab 8 + saved states are the fallback.

## Verification (container Playwright, chromium-1194)
- `scripts/audit_layout.js` **24/24** at 1920/1400/1100/900/700/480 (edges, padding, colgroup, overflow, **SVG-breakout check 5**) — S5 + S3/S4 + dashboard clean.
- 6 pktflows wired (steps-in-SVG == caps); **0** SVG text outside viewBox; **20 interactive nodes, 0 orphans**; **0 duplicate ids**; **0 console/page errors**; sims + MCQs present. `gen_table_colgroups.py` folded into the build (5 tables / 5 colgroups).
- Build order (locked): `build.py` (assemble) → `gen_table_colgroups.py` (auto) → `audit_layout.js`.

## Files owned by this session
```
docs/session-05/index.html            the teaching page (27 pages)
docs/session-05/report.html           cumulative team report (S2..S5)
docs/session-05/session_plan.md
docs/session-05/instructor_guide.md
docs/session-05/student_guide.md
docs/session-05/guided_lab.md
docs/session-05/build_log.md
exercises/session-05/student_activity.md
exercises/session-05/quiz.md
exercises/session-05/homework.md
exercises/session-05/foothold_record_template.md
scripts/lab_s5_setup.ps1              (BOF target prep — placeholders, secrets prompted)
```
Shared (not forked): `docs/assets/css/ceh.css`, `docs/assets/js/session.js`, `docs/index.html` (dashboard — S5 card Delivered), `labs/lab_design.md`, `labs/setup_guide.md`, `design/practice_platforms.md`, `scripts/gen_session_report.py`.

## Still to do before/at publish
- Instructor review of the page and package.
- Confirm the two BOF room tiers on the day; capture the deferred msfconsole/meterpreter shots on the monitored lab.
- `git push` via GitHub Desktop (Cowork has no push credentials) — commit staged locally per logical change. S3/S4 rebuilds may also be uncommitted; review together in GitHub Desktop before pushing.
