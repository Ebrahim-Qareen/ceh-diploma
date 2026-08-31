---
session: 3
status: built — awaiting review
---

# Session 3 — Build Log

What was built, what changed, and what is still open. Rationale is in `DECISIONS.md`; this is the
working detail. Same shape as the Session 1 and 2 build logs.

## Current state
- **29 pages**, ~190 KB single HTML file at `docs/session-03/index.html`
- **16 hand-authored inline SVG diagrams** — **7 click-to-reveal** (four-OS target zoo + the practice-range machines), **1 animated with replay**
- **2 real captured-data screenshots** (generated from live scans, ~96 KB total) + **3–4 defender-side slots deferred as placeholders**
- **5 practice blocks** linking verified free rooms; a consolidated fully-free practice-plan page
- **The signature exercise (Lab 7):** students write one working port-scan detection rule (Sigma worked + SPL/KQL skeletons) from evidence they captured in Lab 2
- **8 hands-on blocks + a lab pre-flight ≈ 124 min ≈ 50%** of live time; plan is ~256 min (+16 over 240) with documented absorb options
- Break timer, 10-question self-scoring quiz + 2 short-answer, sidebar nav, progress bar, keyboard nav
- Full 7-doc package + a target-profile template
- Two PowerShell lab-prep scripts (DC promotion + SNMP), credential-scanned clean
- Not yet published to GitHub (awaiting review)

## What makes this session different
Sessions 1–2 were recon: invisible to the target. **Session 3 is where the attacker becomes visible**,
so the spine is **noise and detection**. Every scan type carries its SOC flip (what the target logs,
in which log, with which Event ID/signature), and the session ends by having students write the
detection rule for the very packets they generated. This is the session where the offensive and
defensive tracks meet — built for a SOC-analyst instructor.

## Build history

### Outline first, then build (approved)
Presented the page-by-page outline with timings, hands-on %, tool grouping, the lab-prep decisions
(SNMP / DC promotion / SMB policy), the verified THM rooms with the free-path correction, the
capture-vs-author visual plan, and the detection-rule language choice. Instructor approved with "i
approve" → taken as DC-promotion yes + keep ~250 min with documented absorb options. Same gate as S1/S2.

### Real packet capture (the evidence base)
Before writing a line, ran real scans in the container against a veth/network-namespace lab target
(22/80/445 open, 443 closed, 8080 filtered), captured with tcpdump/tshark: SYN, connect, FIN, NULL,
Xmas, ACK, UDP, version and aggressive scans, plus the evasion techniques (fragment, decoy,
source-port). The scan-type page's interactive panels and the two rendered JPGs use this **real**
data — including two genuine failure cases (`-sV` mislabelling a service `tcpwrapped`, `-O` returning
"no exact OS match") that the labs teach students to distrust.

### The page (27 pages)
Built in 24 HTML fragments and concatenated. Structure: bridge/spine (P2) → pre-flight (P3) → host
discovery + Lab 1 (P4–5) → scan types + UDP + Lab 2/Wireshark (P6–8) → timing/version + Lab 3 (P9–10)
→ scanning countermeasures/SOC flip (P11) → break (P12) → evasion preview (P13) → enumeration concepts
(P14) → SMB + Lab 4 (P15–16) → SNMP/LDAP + Lab 5 (P17–18) → other services + Lab 6 (P19–20) →
enumeration countermeasures (P21) → the detection-rule Lab 7 (P22) → target profile Lab 8 (P23) →
bridge/quiz/practice/wrap (P24–27). Every page opens with a `.box.intro`; every attack page carries
its SOC flip; techniques map to ATT&CK TA0043 + TA0007 (all IDs verified live).

### Visuals (mix, Wireshark-forward)
10 hand-authored SVG diagrams (5 click-to-reveal incl. the scan-type response matrix built from real
captured packets; 1 animated handshake→half-open-SYN diverge; host-discovery ARP-vs-router;
enumeration funnel; SNMP MIB tree; evasion matrix; S2→S6 continuity) reusing the shared
`.dgm.interactive` / `.dgm.animate-run` mechanics — no new CSS/JS. Plus 2 real captured-data JPGs
generated with matplotlib from the live captures: `syn-vs-connect-capture.jpg` (the three-scan
side-by-side) and `packet-noise-comparison.jpg` (real packet counts 13/103/708 — the noise argument),
each wrapped in `<figure class="shot">` so a missing file degrades to a labelled placeholder.

### The 7-document package
- `docs/session-03/`: `session_plan.md`, `instructor_guide.md`, `student_guide.md`, `guided_lab.md`
- `exercises/session-03/`: `student_activity.md`, `quiz.md`, `homework.md`, `target_profile_template.md`
All follow the exact section shapes of the Session 1 and 2 packages.

### Lab prep (edited in place — no version files)
`labs/lab_design.md` gained a "Session 3 target preparation" section (DC promotion of WINSRV19 for
`ceh.lab` + Win10 join; SNMP install with a weak community string; the deliberate SMB non-change with
its rationale; the second `baseline-dc` snapshot). `scripts/lab_s3_dc_setup.ps1` and
`scripts/lab_s3_snmp_setup.ps1` automate the two builds — no credentials in either file, every secret
prompted at runtime, both scanned clean. The topic_map "no AD lab" open item is closed.

## Research performed (TryHackMe + tool/ATT&CK currency)
Re-verified every candidate room live (logged-out + the `/api/v2/rooms/details` `freeToUse` field —
the reliable check, since the room HTML returns a false "Unauthorized" for some free rooms).
**Correction to the Session 1 record:** the flagship **Nmap** room (`furthernmap`) and `nmap02`,
`networkservices`, `networkservices2`, `rustscan`, `vulnversity`, `basicpentestingjt`, `blue` are all
**FREE** — a fully-free S3 path. `nmap` (The Basics), `nmap03/04` and the Wireshark rooms are Premium;
`enumeration`/`rpnmap` are private; `nmap01` is conflicting (flagged verify-on-day); `nmapthebasics`
is dead. Recorded under `design/practice_platforms.md`. Also verified: NetExec (nxc) is the maintained
CrackMapExec successor; enum4linux-ng wraps nmblookup/net/rpcclient/smbclient; rustscan/masscan
current; SMBv1 off by default (Microsoft); all 9 ATT&CK IDs live.

## Verification performed
Playwright (design_system §8 recipe, `viewport:` not `viewportSize:`) across 1400/1100/900/700/480px:
- Document-level horizontal overflow: **none at any width**
- Elements wider than viewport outside a scroll container: **none**
- SVG text escaping its viewBox: **none**
- Interactive diagrams: **20 `data-node`s, 20 `data-detail` panels, 0 orphans**; each opens exactly one
- Console/page errors: **0**; both real JPGs load
- Page count 27, snum P02–P27 contiguous, all four SVG arrow markers defined before first use

Also confirmed: **no instructor-only text in the student HTML**; every external room fetched and its
tier confirmed; the `.box.intro`-per-page rule holds; local http-server check returns 200 for the page
and every asset path.

## Update — four-OS target zoo (2026-08-28, instructor request)
Added **WIN7-TGT01** (unpatched Windows 7) as the legacy-Windows target so students scan across every OS
type: Metasploitable2 (Linux/2012) · Windows 7 (legacy, SMBv1/EternalBlue) · Windows 10 (modern/hardened)
· Server 2019 DC. New diagram-led page **P04 "One scan, every OS"** — lab-topology diagram, an interactive
same-command-four-OS result matrix, and an SMBv1/null-session per-OS matrix. Win7 woven into the pre-flight
target list, Lab 4 (the box where classic `enum4linux` output still appears + `smb-vuln-ms17-010`), and the
Blue practice note (Blue's target IS a Win7). Lab docs updated in place: `lab_design.md` gained the
target-zoo table, Metasploitable2 acquisition/import steps + the "never expose to a hostile network"
warning, and a recommended-additional-machines table (Metasploitable3, Kioptrix, Stapler, VulnOS/SickOs,
THM Blue; GOAD noted, out of scope). `setup_guide.md` gained a Win7 build section. Re-verified: §8 clean at
all 5 widths, 28 pages, 24/24 interactive nodes, 0 errors.

## Update — practice range: Metasploitable 3 · Kioptrix 1 · Stapler 1 (2026-08-28, instructor request)
Instructor downloaded three more vulnerable machines; added them as a **practice range** for extra
scan/enum reps. New diagram-led page **P27 "The practice range"** with real per-machine output (interactive):
Metasploitable 3 (Windows Server 2008 R2 — web-service stack + SNMP `public` + SMB "Star Wars" accounts,
scan `-Pn`), Kioptrix 1 (mod_ssl 2.8.4 OpenFuck + Samba 2.2.1a trans2open — version→exploit), Stapler 1
(`enum4linux` user-list dump + a service hidden on 12380). Wired into the practice-plan page and homework
(task 4). Lab docs edited in place: `lab_design.md` practice-range table with real port signatures + import
steps; `setup_guide.md` VulnHub-OVA + Metasploitable3 import steps. Output verified against public
walkthroughs. Re-verified: §8 clean at all 5 widths, 29 pages, 27/27 interactive nodes, 0 errors.

## Open items
1. **Defender-side screenshots deferred.** Windows Event Viewer (5156/5157), Zeek `conn.log` and a
   Suricata alert line ship as labelled placeholders — they need capture on the instructor's monitored
   Windows/IDS lab, which this container can't produce. The SVG real-capture panels + the two rendered
   captured-data JPGs carry the teaching meanwhile.
2. **Lighter total diagram count than Session 2** (10 vs ~24). Deliberate — the scan-type real-capture
   panels do more teaching per figure than S2's many small diagrams — but flagged rather than padded
   with weak diagrams. Can add more on request.
3. **`nmap01` tier is conflicting** (API free, logged-out page blocked) — verify on the day before
   assigning; not linked as required.
4. **DC-declined fallback** is written into Lab 5 and the instructor guide (LDAP → THM `networkservices2`
   + concept-only) but assumes the instructor ran `lab_s3_dc_setup.ps1`. Confirm the DC is built before
   teaching.
5. Carried over: S2's two screenshot placeholders (`crtsh-results`, `hunterio-domain-search`); S1 page
   12 ATT&CK Navigator slot; official EC-Council PDFs for Ch.11/12/17/18/19.

## Files owned by this session
```
docs/session-03/index.html                     the teaching page (27 pages)
docs/session-03/assets/img/                     2 real captured-data JPGs
docs/session-03/session_plan.md
docs/session-03/instructor_guide.md
docs/session-03/student_guide.md
docs/session-03/guided_lab.md
docs/session-03/build_log.md
exercises/session-03/student_activity.md
exercises/session-03/quiz.md
exercises/session-03/homework.md
exercises/session-03/target_profile_template.md
scripts/lab_s3_dc_setup.ps1
scripts/lab_s3_snmp_setup.ps1
```
Shared (not forked): `docs/assets/css/ceh.css`, `docs/assets/js/session.js`, `docs/index.html`
(dashboard — S3 card flipped to Delivered), `labs/lab_design.md`, `design/practice_platforms.md`,
`design/topic_map.md`.

## Still to do before/at publish
- Instructor review of the page and package.
- Run `lab_s3_dc_setup.ps1` + `lab_s3_snmp_setup.ps1` on the real lab and confirm the labs return data.
- `git push` via GitHub Desktop (Cowork has no push credentials) — commit is staged locally per logical change.
