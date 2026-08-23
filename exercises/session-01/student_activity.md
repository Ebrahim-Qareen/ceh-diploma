---
session: 1
title: Foundations, Lab Build & First Contact
doc: Student Activity
---

# Session 1 — Student Activity

Two short independent tasks that build on the guided lab, with less hand-holding.

## Activity 1 — Kill Chain / ATT&CK mapping (pairs, 20 min)

Read the breach story below. As a pair, map **each sentence** to a Cyber Kill Chain stage, and name **at least one MITRE ATT&CK tactic** for each.

> An attacker scraped employee names from the company's LinkedIn page and guessed email addresses. They sent a finance clerk a fake invoice with a macro-laden attachment. The clerk opened it; the macro downloaded a payload that called back to the attacker's server. The attacker used stored browser credentials to log into the VPN, created a new local admin account, and disabled Windows Event Logging before copying the customer database out.

**Deliverable:** a 7-row table — sentence/phase → Kill Chain stage → ATT&CK tactic → one line on how a SOC could detect it.

**Success criteria:** every stage of the story is placed; at least 5 distinct ATT&CK tactics named; each has a plausible detection idea.

## Activity 2 — Write your Rules of Engagement (individual, 15 min)

Write a one-page **scope + RoE** for this course's lab. Must include:
- In-scope systems (list them precisely by role/IP range).
- Explicitly out-of-scope systems (name the categories you must never touch).
- Allowed techniques and at least two hard no-gos.
- One sentence on what you'd do if you discovered a real vulnerability *outside* the lab by accident.

**Success criteria:** scope is limited to the host-only lab only; out-of-scope explicitly names the academy/real network and the internet; no-gos are concrete.

**Time box:** 35 min total for both. Turn in with your lab report.
