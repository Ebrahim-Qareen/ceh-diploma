---
session: 4
title: System Hacking I — Vulnerability Analysis, Authentication & Password Attacks
---

# Session 4 — Homework

Due before Session 5. This homework produces Session 5's starting input — arrive without it and you'll build
it while everyone else exploits.

## Tasks

1. **Finish the access plan** (`access_plan_template.md`) for all four hosts — Metasploitable2, Windows 7,
   Windows 10, the DC. Per host: confirmed vulnerabilities (CVE + CVSS base score + **public exploit yes/no +
   reference**), credentials obtained (and **how**: cracked hash / spray / LLMNR / Kerberoast / pass-the-hash),
   and the single **chosen way in** for Session 5. Attach your Lab 7 detection rule as an appendix.

2. **One-page credential report.** From your own Labs 4–6, show one cracked hash, one spray hit, and one roasted
   ticket, and for each write the **Event ID a SOC would see** and its ATT&CK technique. If a capture didn't
   save, re-generate it against your lab.

3. **Practice (free rooms).** Complete TryHackMe **Vulnerabilities 101** (`vulnerabilities101`) and **Attacktive
   Directory** (`attacktivedirectory`). Write one thing each taught you that this session didn't. Both are free.

4. **Practice range (local machines).** Spray **Metasploitable 3**'s weak "Star Wars" accounts and crack at
   least **two** of their hashes, using **Stapler 1**'s `enum4linux` user-list dump as your spray list. Host-only only.

5. **Stretch (optional).** Extend your Lab 7 detection rule so it also fires on a *slow* spray (a long wait
   between rounds), and write one sentence on the false-positive cost of doing so.

## Deliverables
- `access_plan.md` (all four hosts, ranked, with the detection rule appendix).
- `credential_report.pdf` or `.md` (one cracked hash + one spray hit + one roasted ticket, each with its Event ID).
- A short note listing what the two free rooms added.

## Grading rubric (pass / needs-review)
**Pass:**
- Every host has confirmed vulns with **exact CVEs** and the public-exploit answer; credentials list the method.
- A defensible single **chosen way in** per host that weighs reliability + reach + privilege.
- A complete, working detection rule with a threshold and time window, mapped to ATT&CK.
- The credential report built from *your own* Lab 4–6 evidence, each item tied to its Event ID.

**Needs-review:**
- Raw tool output pasted in with no CVE, method, or choice.
- "Cracked some hashes" with no mode, source, or credential recorded.
- A detection rule with no threshold/window, or one copied without understanding the one-to-many pattern.
- A "critical" from a scanner reported without confirming the real version.

## Looking ahead to Session 5
Session 5 — System Hacking II: Exploitation, Shells & Payloads — takes your access plan straight in: the
"chosen way in" per host is the exact exploit it executes (EternalBlue on Win7, vsftpd/usermap on
Metasploitable2, a cracked or pass-the-hash credential on the domain). You'll do it by hand first, then with
msfvenom and Metasploit. Your access plan is the ammunition — bring it complete.
