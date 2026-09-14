---
session: 6
title: Engagement Report — Session 6 deliverable
---

# Engagement Report — <machine / capstone> — <your name / team> — <date>

The Session 6 deliverable and the capstone of the diploma's offensive half. Write it for a paying client:
what you did, how, what it means, and how to fix it. One findings block per issue.

## 1. Executive summary
One short paragraph a manager can read: was the host compromised, how serious, and the single most important fix. No jargon.

## 2. Scope & authorisation
- Target(s): <IPs / hostnames> — my own host-only lab / capstone VMs only.
- Dates: <...>. Everything stayed on the authorised host-only network; nothing external was touched.

## 3. Methodology
The phases run, in order: Recon → Scan → Enumerate → Way in → Shell → Privilege escalation → Loot → Document.

## 4. Findings (repeat per issue)
- **Title:**
- **Severity:** Critical / High / Medium / Low
- **Evidence:** command + output (or screenshot reference)
- **Impact:** what an attacker gains
- **Remediation:** the specific fix

## 5. Proof of compromise
- Initial foothold (user context): <www-data / low-priv>
- Escalation route: <SUID find / sudo / potato / service>
- Final privilege: `id` = root  /  `whoami` = nt authority\system
- Loot: flags, credentials dumped (redacted), lateral movement proven

## 6. Remediation summary (priority order)
1. <highest-priority fix>
2. <next>
3. <next>

## 7. Detection note (attach)
The privilege-escalation detection rule (Lab 8) and the one false-positive source it survives.
