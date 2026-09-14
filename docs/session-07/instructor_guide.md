---
session: 7
title: Malware Threats & Analysis — Instructor Guide
---

# Session 7 — Instructor Guide

## The one message
**Attack informs defence.** Students build a sample, take it apart two ways, then write the rules that catch it. If they leave with "analysis is detection engineering," the session worked.

## Pacing & the two chairs
- The session deliberately flips the student between attacker and analyst on **one** sample. Keep signposting which chair they are in.
- First half ends at the Break with a built + analysed sample. Second half is pure defence (ATT&CK → IOCs → YARA/Sigma → report).

## Where students struggle
- **Isolation discipline (P12/Lab C).** The single most important habit. Do not let anyone detonate without: snapshot, host-only network, tools armed. Make them run the `ping 8.8.8.8 should fail` check out loud.
- **Static vs dynamic order.** Reinforce: static is free and safe (always first); dynamic is powerful and dangerous (isolated, second).
- **"Packed" reading (P11).** A near-empty import table confuses beginners — frame it as *itself a finding* that pushes them to the sandbox.
- **YARA over-fitting (Lab D).** Watch for rules that match on one common string (false positives) or the exact hash (useless). Push for a *combining condition* on distinctive patterns.
- **Sigma vs YARA confusion.** YARA = file content; Sigma = log behaviour. Keep the pairing explicit.

## Board-worthy anchors
- WannaCry = worm (EternalBlue, the S5 flaw) + ransomware payload + killswitch domain — ties four session concepts to one real event.
- Pyramid of Pain — draw it; hashes cheap/brittle at the bottom, TTPs expensive/durable at the top.
- The lifecycle skeleton (delivery→execution→persistence→C2→actions) — draw once, refer back every page.

## Lab notes
- **Lab A:** if Kali AV/Defender-in-VM quarantines the payload, that is the SOC flip — narrate it, then exclude the lab folder.
- **Lab C:** provide `saved/lab_c_beacon.pcap` and a pre-recorded ProcMon log for anyone whose sandbox misbehaves — nobody should be blocked from the analysis for lack of a VM.
- **Lab D:** validate every YARA rule fires on the sample AND not on `/usr/bin` before moving on.
- **Lab E:** the report is the graded deliverable — hold time for it; do not let the capstone eat the final 20 minutes.

## Assessment
- Formative: 6 MCQs (P26) + 15 mini-labs (one per concept, self-checked).
- Summative: the incident triage report (Lab E) against `exercises/session-07/incident_triage_template.md` — see rubric in student_activity.md.
