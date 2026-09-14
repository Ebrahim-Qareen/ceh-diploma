---
session: 5
title: Instructor Guide — Session 5
---

# Session 5 — Instructor Guide

## Pre-class checklist
- [ ] `pre-s5` snapshot on every target (EternalBlue and the BOF **crash** boxes — you will revert).
- [ ] WIN7 MS17-010 confirmed: `auxiliary/scanner/smb/smb_ms17_010` → *likely VULNERABLE*.
- [ ] Metasploitable2 reachable; vsftpd 2.3.4 banner on 21.
- [ ] `vulnserver` running on WIN10 with Immunity attached + `mona` configured; Linux `gdb` fallback compiled.
- [ ] `msfdb init` done; `db_status` = Connected.
- [ ] Each student has their S4 access plan and at least one working credential.

## The currency corrections — know these cold
- **EternalBlue module path** is `exploit/windows/smb/ms17_010_eternalblue` (current). The *check* is `auxiliary/scanner/smb/smb_ms17_010`.
- **msfvenom staged vs stageless** is the `/` vs `_`: `windows/x64/meterpreter/reverse_tcp` (staged) vs `..._reverse_tcp` (stageless). Staged needs the handler up.
- **Encoding is NOT AV evasion.** `-e shikata_ga_nai` removes bad characters; it has not evaded modern AV for years. Real evasion is S6/S7.
- **Metasploitable2 is 2012-era** — perfect for teaching CVE→exploit, not a picture of a modern vuln landscape. Say so.
- **The naive stack overflow is a teaching model** — DEP/ASLR/stack canaries stop it on modern targets; that is the countermeasure and the exam answer.

## The one thing to get right: manual before framework, and read step 3
Students want to jump to `msfconsole`. Hold the line: Lab 1 (manual vsftpd) **before** Lab 2 (the same via MSF). The pipeline's step 3 — *read the exploit before you run it* — is the ethical-hacker point and the thing the framework never does.

## Teaching flow
### P2 — Where we left off (7 min)
Open with "take out your access plan." Make the kill-chain diagram concrete: today's to-do list IS the plan.
### P3 — Lab pre-flight (5 min)
Everyone confirms targets + `db_status` + one S4 credential. Snapshot now.
### P4 + Lab 1 (8 + 15) — pipeline, then manual vsftpd
Step through the pipeline diagram; run the searchsploit mini-lab; then Lab 1 by hand (nc → root). This is the anchor of Half A.
### P5 + Lab 2 (9 + 12) — the framework, then the same exploit
Teach exploit+payload+options→session on the interactive diagram. Lab 2 fires the same vuln in three lines — then ask the room "what did it NOT do?" (step 3).
### P7 + Lab 3 (7 + 15) — EternalBlue, the flagship
Walk the worked-chain diagram; run the auxiliary-check mini-lab; then Lab 3 to SYSTEM. Emphasise `getuid` = SYSTEM and *why* (SMB runs as SYSTEM).
### P9 + Lab 4 (8 + 12) — bind vs reverse
The single most useful diagram of the day. Let the bind shell **fail** against the firewall before the reverse succeeds.
### P11 + Lab 5 (9 + 14) — payloads
Staged vs stageless on the interactive; msfvenom 7-part. Lab 5 generates the reverse-shell evidence for Lab 9. Demo the **handler-down failure**.
### Break (10)
### P13 + Lab 6 (7 + 10) — shell upgrade
The pty/stty ritual. Quick — this is muscle memory.
### P15 + Lab 7 (6 + 10) — credential access
"A credential is an exploit." psexec/evil-winrm with an S4 cred. This is the S6 bridge.
### P17 + Lab 8 (12 + 20) — buffer overflow (the compress candidate)
Step through the stack diagram slowly — it is the hardest concept. Run Lab 8 as a **guided demo with saved states**; students repeat as homework if time is tight.
### P19 + Lab 9 (6 + 16) — SOC flip + the rule, PROTECT this time
The interactive attack→log map, then students write ONE reverse-shell rule. Do not let this get squeezed.
### Lab 10 (12) — the foothold record
The deliverable. Insist on the "landed as" column.
### P22 — Into Session 6 (6)
User context = where S6 starts per host.
### P24–P26 — Quiz, practice, wrap (19)

## Bridge to next session
Session 6 (Privilege Escalation & Capstone) starts from the foothold record — specifically the **low-privilege** shells. Tell students to bring at least one they can reproduce.

## If the BOF lab breaks or Immunity misbehaves
Fall back to the Linux `gdb`/`pwndbg` binary — identical fuzz→offset→control→shellcode logic, no VM. Or run Lab 8 fully as a projected demo and set it as homework with the saved states. Never let a stuck debugger eat Lab 9.
