---
session: 6
title: Homework — Session 6
---

# Session 6 — Homework

## Tasks
1. **Capstones** — finish both DoubleTrouble and Blackpearl. Submit a full **engagement report** for at least one: exec summary, scope, methodology, findings (severity + evidence + remediation), proof of root.
2. **Linux PrivEsc (TryHackMe)** — complete the free room; list every vector you used (SUID, sudo, cron, capabilities, PATH, kernel) and the command for each.
3. **Detection rule** — write your Lab 8 rule (the LSASS/Sysmon 10 one is best) in Sigma/SPL/KQL, and name one false-positive source it survives.
4. **Read ahead** — for a host where you got SYSTEM, one paragraph: what you would do next to reach the domain, and how a SOC would catch it.

## Deliverables
- `engagement_report.md` (from the template) — or an export of the cumulative Team Report.
- One detection rule file + its false-positive note.
- The Linux PrivEsc vector list.

## Grading rubric (pass / needs-review)
**Pass:** a report with every section and a remediation per finding; two capstones rooted; a rule that keys on behaviour (LSASS access / service install / 4672) with a stated false-positive control.
**Needs-review:** screenshots with no narrative or fixes; a rule that only matches a tool name; a capstone with no privesc.

## Looking ahead to Session 7
Session 7 (Malware Threats) builds and analyses the payloads — trojans, backdoors — that create and hide footholds like the ones you established, and the AV/EDR evasion that flagged your Mimikatz today.
