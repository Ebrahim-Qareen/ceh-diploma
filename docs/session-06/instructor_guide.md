---
session: 6
title: Instructor Guide — Session 6
---

# Session 6 — Instructor Guide

## Pre-class checklist
- [ ] Every student can reproduce a **low-priv shell** (from their S5 foothold record).
- [ ] linPEAS on the Linux targets; winPEAS + PrintSpoofer/GodPotato on Windows; Mimikatz staged (with a Defender exclusion for the demo copy).
- [ ] **DoubleTrouble** and **Blackpearl** imported, host-only, snapshotted `pre-s6`.
- [ ] Seeded misconfigs present: a GTFOBins SUID, a writable cron / NOPASSWD sudo, a SeImpersonate service account, a SUID PHP on Blackpearl.

## The currency corrections — know these cold
- **Potatoes:** JuicyPotato is patched on Server 2019 / Win10 1809+. Use **PrintSpoofer** or **GodPotato** now.
- **GTFOBins / LOLBAS** are the lookup tables — Linux (gtfobins) and Windows (lolbas). Teach the lookup, not memorisation.
- **Mimikatz vs EDR:** on a modern monitored host, Mimikatz is flagged instantly (Sysmon 10). It still teaches the concept; real ops use LSASS-dump alternatives + evasion (S7).
- **Kernel exploits are the last resort** — they can panic the box. Misconfigs first.

## The one thing to get right: enumerate before you exploit
Students want to jump to a technique. Hold the loop: **enumerate → identify → abuse → verify.** linPEAS/winPEAS automate the looking; the judgement is the skill. Every lab starts with enumeration.

## Teaching flow
### P2 — Where we left off (6) — open the foothold record; low-priv rows are today's targets.
### P3–P5 — the loop, the Linux surface, linPEAS (8+8+7) — map before tools.
### Lab 1 (15) — SUID + GTFOBins → root. The highest-frequency Linux privesc.
### P7 + Lab 2 (8+14) — sudo/cron; do at least one path. Note the deliberate "not writable" failure.
### P9–P10 + Lab 3 (8+8+15) — Windows surface + token abuse, then potato → SYSTEM.
### P12 + Lab 4 (9+12) — winPEAS + Mimikatz; dump LSASS, reuse a credential. Generates the Sysmon 10 evidence.
### Break (10)
### P14 + Lab 5 (7+10) — steganography; drill stegseek — the capstone needs it.
### P16 + Lab 6 + Lab 7 (6+25+25) — the capstone methodology, then the two machines. This is the heart of the session; protect the time.
### P19 + Lab 8 (6+16) — the privesc SOC flip, then the detection rule (LSASS is the best one). PROTECT this.
### Lab 9 (14) — the engagement report. Insist on severity + remediation per finding.
### P22–P25 — where next, quiz, practice, wrap.

## Bridge to next session
Session 7 (Malware Threats) builds and analyses the payloads that establish and hide footholds like the ones created today — and the AV/EDR evasion that Mimikatz just ran into.

## If a capstone breaks or time runs short
Run **one capstone in class** and set the other as homework with the hint sheet. Never let a stuck capstone eat Lab 8/9 — the detection rule and the report are the graded deliverables.
