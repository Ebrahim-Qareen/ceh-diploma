---
session: 6
title: Student Activity — Session 6
---

# Session 6 — Student Activity

## Activity 1 — Read the enumeration (pairs, 12 min)
Given a linPEAS output snippet, each pair circles the **three** most promising vectors and states, for each, the exact abuse command and why it works. Compare with another pair — did you pick the same three?

## Activity 2 — Linux or Windows? Which vector? (individual, 8 min)
For each finding, name the OS and the escalation:
1. `sudo -l` → `(ALL) NOPASSWD: /usr/bin/vim`
2. `whoami /priv` → `SeImpersonatePrivilege Enabled`
3. `find / -perm -4000` → `/usr/bin/php` (SUID)
4. `sc qc VulnSvc` → binary path is user-writable
5. `getcap -r /` → `/usr/bin/python3 = cap_setuid+ep`

## Activity 3 — Attack → detection (pairs, 12 min)
Match each escalation to the event a SOC would see, and name the one field a rule keys on: (a) PrintSpoofer → ? (b) `sc config` new service → ? (c) `sekurlsa::logonpasswords` → ? (d) a SUID `find` shell on Linux → ?

## Activity 4 — Plan the capstone (individual, 8 min)
You are handed one IP. In order, list the first five commands you run and what each would tell you — before you have any foothold. (Recon/enumeration muscle memory.)
