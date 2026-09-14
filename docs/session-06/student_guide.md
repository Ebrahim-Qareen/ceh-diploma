---
session: 6
title: Student Guide — Session 6
---

# Session 6 — Student Guide

## 1. The one idea: access is not control
Session 5 got you a shell. Most were low-privilege. Privilege escalation turns that shell into **root** (Linux) or **SYSTEM** (Windows) — full control of the host.

## 2. The enumeration loop
Enumerate → identify → abuse → verify. Then loop. Enumeration is 90% of privesc; the exploit is a one-liner once you have found the target. linPEAS/winPEAS automate the looking.

## 3. Linux surface
SUID binaries (GTFOBins), sudo rights (`sudo -l`), cron jobs (writable root scripts), writable PATH, capabilities (`getcap -r /`), kernel exploits (last resort). Look these up on **GTFOBins**.

## 4. The Linux pattern
**If root runs something you can change, you are root** — a SUID shell-capable binary, a NOPASSWD sudo break-out, a writable cron script. Find the crossing point of "root runs it" and "I can write it."

## 5. Windows surface
Service misconfigs (weak perms / unquoted path / writable binary), token privileges (`whoami /priv` → SeImpersonate), AlwaysInstallElevated, stored credentials (unattend.xml, registry, LSASS). Lookup table: **LOLBAS**.

## 6. Token abuse (potato)
A service account with **SeImpersonatePrivilege** is SYSTEM with an extra step: a potato (PrintSpoofer/GodPotato) coerces a SYSTEM token, and the privilege lets you impersonate it → SYSTEM.

## 7. Mimikatz
As SYSTEM, `privilege::debug` then `sekurlsa::logonpasswords` dumps plaintext passwords, NT hashes and Kerberos tickets from **LSASS memory**. One box's memory becomes the network's credentials.

## 8. Steganography
Hiding data inside data. Image stego (steghide/stegseek — crack the passphrase), NTFS ADS (`file:hidden`, `dir /r`). The capstone hides a credential in an image.

## 9. The capstone
An IP and nothing else → recon → enumerate → way in → shell → escalate → **document**. Two machines (DoubleTrouble, Blackpearl), two routes, the same methodology.

## 10. The SOC flip
Elevation is rare, so it is detectable: 4672 (new SYSTEM rights), 7045 (service installed), **Sysmon 10** (LSASS access — the best signal), auditd/EDR (uid 1000→0 from a SUID binary).

## 11. The deliverable — the engagement report
Exec summary, scope, methodology, findings (severity + evidence + remediation), proof. Anyone can get root; a professional writes the report. This closes the offensive half.

## Key terms
vertical/horizontal privesc · SUID/GTFOBins · sudo/cron abuse · capabilities · SeImpersonate/potato · unquoted service path · Mimikatz/LSASS · pass-the-hash · steghide/stegseek/ADS · Sysmon 10 · engagement report.
