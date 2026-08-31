---
session: 3
title: Scanning & Enumeration
---

# Session 3 — Homework

Due before Session 4. This homework produces Session 4's starting input — arrive without it and
you'll build it while everyone else attacks.

## Tasks

1. **Finish the target profile** (`target_profile_template.md`) for all four live hosts —
   Metasploitable2, Windows 7, Windows 10, WinSrv/DC. Exact service versions, OS guess + confidence, shares, users,
   SNMP/LDAP findings, and a ranked "most likely way in" per host. Attach your Lab 7 detection rule as
   an appendix.

2. **One-page scan-type report.** From your own Lab 2 captures, produce the SYN-vs-connect-vs-Xmas
   three-column comparison (screenshot or table) and write two sentences on what each scan left in a
   log. If your capture didn't save, re-run the three scans against Metasploitable2 and capture again.

3. **Practice (free rooms).** Complete TryHackMe **Nmap** (`furthernmap`) and **Network Services**
   (`networkservices`). Write one thing each taught you that this session didn't. Both are free.

4. **Practice range (local machines).** Scan and enumerate at least **two** of the range machines —
   **Metasploitable 3** (Windows web-service + SMB "Star Wars" accounts, scan `-Pn`), **Kioptrix 1**
   (read the old versions as exploit leads), **Stapler 1** (`enum4linux` dumps a big user list; a service
   hides on `12380`, so run `-p-`). Add a short target-profile block for each. Host-only only.

5. **Stretch (optional).** Improve your Lab 7 detection rule so it also fires on a slow `-T1` scan,
   and write one sentence on the false-positive cost of doing so.

## Deliverables
- `target_profile.md` (all three hosts, ranked, with the detection rule appendix).
- `scan_types_report.pdf` or `.md` (the three-column comparison + log note).
- A short note listing what the two free rooms added.

## Grading rubric (pass / needs-review)
**Pass:**
- Every live host has a block; exact versions; confidence stated where you guessed.
- A defensible ranked "way in" naming specific service+version, not "SMB looks old."
- A complete, working detection rule with a threshold and time window.
- The three-scan comparison built from *your own* captures, with the log note.

**Needs-review:**
- Raw nmap output pasted in with no ranking or analysis.
- "No SMB findings" written where the real finding is "hardened — enumerate with creds."
- A detection rule with no threshold/window, or copied without understanding the pattern.

## Looking ahead to Session 4
Session 4 — Vulnerability Analysis, Authentication & Password Attacks — takes your target profile
straight in: version strings → CVE/CVSS + searchsploit; user list → password spraying + hash
cracking; and, because WINSRV19 is now a domain controller, real NTLM/Kerberos and LLMNR poisoning
against the `ceh.lab` domain. Your profile is the ammunition.
