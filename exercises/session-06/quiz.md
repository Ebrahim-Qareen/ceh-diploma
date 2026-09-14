---
session: 6
title: Quiz — Session 6
---

# Session 6 — Quiz

## Questions
1. What is the single most important activity in privilege escalation, and why?
2. Why is a root-owned SUID binary dangerous, and how does GTFOBins help?
3. A service account holds `SeImpersonatePrivilege`. Why is that almost SYSTEM?
4. Why is dumping LSASS with Mimikatz so valuable beyond the single host?
5. Which potato exploits are current on modern Windows, and why not JuicyPotato?
6. What is the highest-value SOC detection for this session's credential theft, and which Sysmon event is it?
7. Give the pattern that unifies SUID, sudo, and cron privesc in one sentence.
8. Why does the engagement report matter as much as getting root?

### Short answer
9. Name the four steps of the enumeration loop, in order.
10. You have a writable script that root runs via cron, but nothing happens after a minute. Give the two most likely causes.

## Answer key
1. **Thorough enumeration** — it finds the one misconfiguration; the exploit is a one-liner once found. Guessing wastes time and is noisy.
2. A SUID binary runs as its **owner (root)** regardless of who launches it; **GTFOBins** gives the exact one-liner to break it into a root shell.
3. A **potato** (PrintSpoofer/GodPotato) coerces a **SYSTEM token**, and SeImpersonate is exactly the right to impersonate a token handed to you → SYSTEM.
4. **LSASS caches logged-on users' credentials** — plaintext, hashes, tickets — often a domain admin's; one host's memory becomes network-wide access.
5. **PrintSpoofer / GodPotato**. JuicyPotato's DCOM/BITS trick was **patched on Server 2019 / Win10 1809+**.
6. **LSASS access = Sysmon Event ID 10** (a process opening lsass.exe with a dump access mask) — almost nothing legitimate does it.
7. **If a root process executes something you can change, you become root.**
8. The report — **severity, evidence, remediation** — is the client deliverable; a shell without it is worth far less, and it is the job.
9. Enumerate → identify → abuse → verify (then loop).
10. The script (or its directory) is **not actually writable** by you, or the cron job **does not run as root** (or the schedule/path differs) — confirm the writable bit and the crontab line.
