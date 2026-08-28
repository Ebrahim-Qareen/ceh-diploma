---
session: 4
status: built — awaiting review
---

# Session 4 — Build Log

What was built, what changed, and what is still open. Rationale is in `DECISIONS.md`; this is the working
detail. Same shape as the Session 1–3 build logs.

## Current state
- **29 pages**, ~184 KB single HTML file at `docs/session-04/index.html`
- **16 hand-authored inline SVG diagrams** — **7 click-to-reveal** (vuln funnel · research-vs-scan · triage funnel · taxonomy · hash-cracking pipeline · credential-across-OS · bind-vs-reverse) and **2 animated with replay** (NTLM challenge-response · Kerberos ticket flow)
- **1 real captured-data figure** (`hashcat-crack.jpg` — a genuine `hashcat -m 1000` run against fake lab NT hashes, cracked 4/4, rendered ~50 KB) + **3 Windows/domain capture slots deferred as labelled placeholders** (`event-4625-spray`, `responder-capture`, `getuserspns`)
- **6 practice blocks / rooms** linking verified-free rooms; a consolidated free practice-plan page
- **The signature exercise (Lab 7):** students write one working credential-attack detection rule (Sigma worked + SPL/KQL skeletons) from the 4625/4769/Responder evidence they generated in Labs 4–6
- **8 hands-on blocks + a lab pre-flight ≈ 117 min ≈ 45%** (≈50% counting the guided scan demo); plan is ~259 min (+19 over 240) with documented absorb options
- Break timer, 10-question self-scoring quiz + 2 short-answer, sidebar nav, progress bar, keyboard nav
- Full 7-doc package + an access-plan template
- One new PowerShell lab-prep script (`scripts/lab_s4_dc_setup.ps1`), credential-scanned clean
- Not yet published to GitHub (awaiting review)

## What makes this session different
Sessions 2–3 found the doors. **Session 4 gets the keys.** The spine is "attackers don't break in — they log
in," and it's the first session that attacks a **real domain** (`ceh.lab`) rather than a standalone box — the
AD lab built in Session 3 is what this session was built for. Every credential attack carries its auth-log SOC
flip, and the session ends with students writing the detection rule for the very events they generated. The
offensive and defensive tracks meet on the authentication surface — built for a SOC-analyst instructor.

## Build history

### Outline first, then build (approved)
Presented the page-by-page outline with timings, hands-on %, tool grouping, the lab-prep decisions (the
`lab_s4_dc_setup.ps1` extension), the API-verified THM rooms, the capture-vs-author visual plan, the detection-
rule language, and the Session 5 bridge recommendation. Instructor approved all four decisions as recommended
(build the outline · approve the seeding · Nessus Essentials primary · S5 bridge concept-only). Same gate as S1–S3.

### The page (29 pages)
Built in 12 HTML fragments and concatenated. Structure: cover/agenda (P1) → bridge (P2) → pre-flight (P3) →
**Half A** vuln concepts + funnel (P4) → research + CVSS (P5) → searchsploit/nmap-vuln (P6) → Lab 1 (P7) →
scanner tools (P8) → Lab 2 demo (P9) → **Half B** auth + hashing (P10) → NTLM animated (P11) → Kerberos
animated (P12) → taxonomy + pipeline (P13) → break (P14) → hashcat/john (P15) → Lab 3 (P16) → hydra/nxc (P17)
→ Lab 4 spray (P18) → LLMNR/Responder (P19) → Lab 5 capture (P20) → Kerberoast/Impacket/PtH (P21) → Lab 6 (P22)
→ the auth-log SOC flip (P23) → **Lab 7 the detection rule** (P24) → **Lab 8 the access plan** (P25) → into
Session 5 concept (P26) → quiz (P27) → practice range (P28) → takeaways/homework (P29). Every page opens with a
`.box.intro`; every attack page carries its SOC flip; techniques map to TA0006 + TA0007 with the T1210 hand-off.

### Mechanism before tools
P10–P13 build the mechanism as diagrams first (hashing vs encryption vs encoding; NTLM challenge-response
animated; Kerberos flow with its two bleed points; the online/offline taxonomy), then the tool pages hang the
commands on them. This is the deliberate anti-"run `hashcat -m 1000` and learn nothing" structure.

### Visuals (diagrams over words — standing instructor preference)
16 hand-authored SVG (beats S3's mix on animated + captures): the 10 must-have visuals (vuln funnel · CVSS
vector · NTLM animated · Kerberos animated · LLMNR poisoning · taxonomy · cracking pipeline · pass-the-hash ·
auth-log SOC flip · credential-across-OS matrix) plus hashing-vs-encryption, searchsploit silent-vs-loud, the
triage funnel, brute-vs-spray, and the bind-vs-reverse bridge. Reuses the shared `.dgm.interactive` /
`.dgm.animate-run` mechanics — no new CSS/JS. Shared arrow markers are carried in a hidden top-of-article
`<defs>` SVG (more robust than S3's "defs live in one diagram" — removing any diagram can't break the arrows).
The one real capture is a genuine in-container hashcat run; the Windows/domain captures need the instructor's
monitored domain and ship as labelled placeholders (same pattern as S3's deferred defender screenshots).

### The 7-document package
- `docs/session-04/`: `session_plan.md`, `instructor_guide.md`, `student_guide.md`, `guided_lab.md`, `build_log.md`
- `exercises/session-04/`: `student_activity.md`, `quiz.md`, `homework.md`, `access_plan_template.md`
All follow the exact section shapes of the Session 1–3 packages.

### Lab prep (new script + docs edited in place — no version files)
`scripts/lab_s4_dc_setup.ps1` (sibling to the S3 scripts) handles four stages: `Kerberoast` (SPN + weak
password on `svc_backup`; a second SPN account `svc_sql` with a strong password = the never-cracks case),
`SprayPolicy` (one weak password on a 3-of-5 subset, `m.said` distinct + strong, account-lockout policy),
`LocalAccounts` (2–3 weak local accounts on Win7/Win10 for the SAM lab), and `CheckLLMNR` (read-only status
report on Win10). No credentials in the file; every secret prompted at runtime; credential-scanned clean.
`labs/lab_design.md` gained a "Session 4 target preparation" section and a `baseline-s4` snapshot note;
`labs/setup_guide.md` gained the S4 prep steps. Nessus Essentials chosen as the classroom scanner (5-IP free
tier, guided demo).

## Research performed (TryHackMe + tool/standard currency)
Verified every candidate room via the reliable API method (`/api/v2/rooms/details?roomCode=<slug>`,
`freeToUse` + `displaySubscriptionTier`). **Free path:** `vulnerabilities101`, `openvas`, `crackthehash`,
`hydra`, `attacktivedirectory` (the gem — free AD credential chain), `networkservices2`. **Premium/private:**
`hashingcrypto101`, `johntheripperbasics` (`johntheripper0` is a dead slug/404), `passwordattacks` (Max),
`attackingkerberos`, `nessus` (private), `responder` (private), `rpvulnerabilityscanning` (404), `holo`
(inconsistent API data / premium network). Recorded in `design/practice_platforms.md` under a new S4 section.
Currency corrections confirmed against primary sources: **Nessus Essentials is now 5 IPs (was 16)**; LLMNR/NBT-NS
still default-on in 2026 (Microsoft ramping to mDNS; Responder poisons mDNS too); Impacket is Fortra's; CVSS
v4.0 exists (Nov 2023) but NVD/CEH lead with v3.1; hashcat modes 1000/5600/13100/18200; rockyou ships gzipped.

## Verification performed
Playwright (design_system §8 recipe, `viewport:` not `viewportSize:`) across 1400/1100/900/700/480px, all 29 pages:
- Document-level horizontal overflow: **none at any width**
- Elements wider than viewport outside a scroll container: **none**
- SVG text escaping its viewBox: **none**
- Interactive diagrams: **28 `data-node`s, 28 `data-detail` panels, 0 orphans, 0 duplicate keys**; each opens exactly one
- Console/page errors: only the expected image-404s for the 3 placeholder capture slots (they degrade to labelled placeholders); the real `hashcat-crack.jpg` loads
- 29 pages, snum P02–P29 contiguous; 16/16 tables wrapped in `.tbl-scroll`; all `<figure>/<svg>/<section>/<g>/<pre>/<table>` tags balanced; arrow markers defined once before first use
- Local http-server check: `/session-04/index.html` + asset paths return 200
- **No instructor-only text in the student HTML**; the `.box.intro`-per-page rule holds; ATT&CK IDs (T1110.001/.003, T1003.001/.002/.003, T1558.003/.004, T1557.001, T1550.002, T1210) confirmed

## Open items
1. **Windows/domain capture slots deferred.** `event-4625-spray`, `responder-capture`, `getuserspns` need
   capture on the instructor's monitored domain (this container has no Windows/AD), so they ship as labelled
   placeholders. The 16 SVG diagrams + the real hashcat capture carry the teaching meanwhile. **This session is
   the moment to also capture the S3-deferred defender screenshots (5156/5157, Zeek, Suricata) on the same lab.**
2. **Timing is ~259 min (+19 over 240)** — same shape as S1–S3, kept with documented absorb options (Lab 2 demo
   → homework; the shadow half of Lab 3 → homework; trim mechanism pages). Protected: Labs 4/5/6, Lab 7, Lab 8.
3. **DC-declined fallback** written into the instructor guide (spray MSF3 Star Wars accounts; Kerberoast has no
   non-domain equivalent → THM `attacktivedirectory` + `saved/` evidence). Confirm the DC is built before teaching.
4. Carried over: S2's two screenshot placeholders (`crtsh-results`, `hunterio-domain-search`); S1 page 12 ATT&CK
   Navigator slot; official EC-Council PDFs for Ch.11/12/17/18/19.

## Files owned by this session
```
docs/session-04/index.html                     the teaching page (29 pages)
docs/session-04/assets/img/hashcat-crack.jpg   1 real captured-data JPG
docs/session-04/session_plan.md
docs/session-04/instructor_guide.md
docs/session-04/student_guide.md
docs/session-04/guided_lab.md
docs/session-04/build_log.md
exercises/session-04/student_activity.md
exercises/session-04/quiz.md
exercises/session-04/homework.md
exercises/session-04/access_plan_template.md
scripts/lab_s4_dc_setup.ps1
```
Shared (not forked): `docs/assets/css/ceh.css`, `docs/assets/js/session.js`, `docs/index.html` (dashboard — S4
card flipped to Delivered), `labs/lab_design.md`, `labs/setup_guide.md`, `design/practice_platforms.md`,
`design/topic_map.md`.

## Still to do before/at publish
- Instructor review of the page and package.
- Run `lab_s4_dc_setup.ps1` on the real lab and confirm the labs return data; capture the three deferred shots.
- `git push` via GitHub Desktop (Cowork has no push credentials) — commit is staged locally per logical change.
- Note: **Session 3 is also still uncommitted** in the working tree — review both S3 and S4 in GitHub Desktop before pushing.
