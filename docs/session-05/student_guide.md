---
session: 5
title: Student Guide — Session 5
---

# Session 5 — Student Guide

## 1. The one idea: turn access into a shell
Session 4 gave you a vulnerability and a credential. Session 5 turns either one into **your code running on the target**. Two paths, same destination: an exploit, or a credential.

## 2. The exploitation pipeline
Matched CVE → find the PoC → **read it** → configure → fire → shell. Metasploit automates 4–6; it never does step 3 for you. Always know what an exploit does before you run it.

## 3. Manual vs Metasploit
Lab 1 exploits vsftpd 2.3.4 with raw `nc`; Lab 2 does the identical thing in three lines of `msfconsole`. The framework is fast, but manual proves you understand it — and the exam tests the manual one.

## 4. The Metasploit model
**exploit + payload + options → session.** Auxiliary modules scan (no payload); post modules run after you have a session. `search / use / show options / set / exploit`.

## 5. EternalBlue (MS17-010)
The SMBv1 kernel flaw leaked in 2017. Because SMB runs as SYSTEM, the exploit lands you as **SYSTEM** directly — no escalation. Patched everywhere since 2017; WIN7-TGT01 is a deliberately unpatched lab box.

## 6. Bind vs reverse shells
Bind = the target opens a port and you connect **in** (firewalls block it). Reverse = the target connects **out** to you (firewalls allow it). **Default to reverse**, usually on 443/53 to blend in.

## 7. Payloads: staged vs stageless
`/` = staged (a small stager fetches the rest — needs the handler up). `_` = stageless (whole payload, bigger, more reliable). `msfvenom` builds them; `multi/handler` catches them. **Encoding is not AV evasion.**

## 8. Shell upgrade
Your first shell is "dumb" (no tab, no sudo, dies on Ctrl-C). Upgrade with `python3 -c 'import pty;pty.spawn("/bin/bash")'` + `stty raw -echo; fg`, or all the way to meterpreter (`sessions -u`).

## 9. A credential is an exploit
On Windows a valid credential (or its hash) is remote code execution — `psexec`, `wmiexec`, `evil-winrm`, `nxc`. No CVE, no crash, and the quietest foothold. This is the bridge from S4 and into S6.

## 10. Buffer overflow — why exploits exist
Too much input overwrites the saved return address (EIP). Fuzz → crash → find the offset → control EIP → remove bad characters → point EIP at a JMP ESP → your shellcode runs. Modern mitigations: DEP/NX, ASLR, stack canaries.

## 11. The SOC flip
A shell is a **process with a parent and a connection**. The durable detection: a server/service process spawning a shell interpreter (4688 / Sysmon 1) that then makes an outbound connection (Sysmon 3). EternalBlue and meterpreter are also caught by IDS signatures in near-real-time.

## 12. The deliverable — the foothold record
Per host: how you got in, the payload, the shell type, **what user you landed as**, and proof. The "landed as" column is what Session 6 starts from.

## Key terms
PoC · payload · staged/stageless · handler · meterpreter · bind/reverse · pass-the-hash · EIP/offset/JMP ESP/shellcode/NOP sled · bad characters · DEP/ASLR/canary · foothold.
