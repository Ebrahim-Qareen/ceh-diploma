---
session: 5
title: Homework — Session 5
---

# Session 5 — Homework

## Tasks
1. **Foothold record** — complete one block per host you landed on (Labs 1–8). The **"landed as"** column is mandatory; include your proof command output.
2. **Blue (TryHackMe)** — finish the free `Blue` room; paste your `getuid`/`whoami` proof and the module path you used.
3. **Detection rule** — write your Lab 9 reverse-shell rule (Sigma/SPL/KQL of your choice), and name **one false-positive source** it survives and how.
4. **Buffer overflow** — if Lab 8 ran as a demo, complete the chain yourself with the saved states; submit the offset, the bad-character list, and the JMP ESP address you used.
5. **Read ahead** — for ONE of your low-privilege footholds, name two privilege-escalation checks you would run first (Windows or Linux), one sentence each.

## Deliverables
- `foothold_record.md` (from the template) — or an export of your cumulative Team Report.
- One detection rule file + its false-positive note.
- BOF chain values (offset / bad chars / JMP ESP) or a short screenshot of the shell.

## Grading rubric (pass / needs-review)
**Pass:** a per-host foothold record with exploit/cred + payload + shell type + **user context** + proof; a rule that keys on the parent→child+egress behaviour (not exploit bytes) with a stated false-positive control; the Blue proof.
**Needs-review:** raw msfconsole/nc output with no conclusions; a rule that only matches EternalBlue bytes; missing "landed as" column.

## Looking ahead to Session 6
Bring at least one **low-privilege** shell you can reproduce. Session 6 (Privilege Escalation & Capstone) is the art of turning that into SYSTEM/root, then tying the whole engagement into a capstone.
