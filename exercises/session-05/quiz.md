---
session: 5
title: Quiz — Session 5
---

# Session 5 — Quiz

## Questions
1. Why do reverse shells succeed where bind shells fail on most networks?
2. What does the `/` in `windows/x64/meterpreter/reverse_tcp` tell you, and what must you remember because of it?
3. Which step of the exploitation pipeline does Metasploit NOT do for you?
4. Why does EternalBlue give you SYSTEM directly with no privilege escalation?
5. In a stack overflow, why is "controlling EIP" the milestone, and what is a JMP ESP used for?
6. What is the most durable way to detect a reverse shell regardless of the exploit used?
7. Give one reason a credential-based foothold (psexec) is harder for a SOC to detect than EternalBlue.
8. Why is `msfvenom -e shikata_ga_nai` NOT antivirus evasion?

### Short answer
9. Name the six steps of a classic stack buffer overflow in order.
10. Your `msfvenom` staged payload runs on the target but no session opens. Give the two most likely causes.

## Answer key
1. The **target** connects OUT in a reverse shell and firewalls allow outbound far more than inbound; a bind shell needs a blocked inbound connection.
2. It is **staged** — a small stager fetches the full payload — so the **handler must be listening** at the moment of the callback.
3. **Reading and understanding** the exploit before running it (step 3). It automates find/configure/fire (4–6).
4. EternalBlue corrupts kernel memory in the **SMB service, which runs as SYSTEM**, so code execution lands as SYSTEM.
5. EIP is the **return address** — control it and you decide what code runs next. A **JMP ESP** is a trampoline: set EIP to its address and execution jumps to your shellcode at ESP (defeats address uncertainty).
6. Alert when a **server/service process spawns a shell interpreter** that then makes an **outbound connection** — behaviour, not exploit bytes.
7. A valid login looks like a valid login: no crash, no exploit signature, no unusual child process in many cases — just an authentication event.
8. Encoders were designed to remove **bad characters**, not evade AV; signatures caught them years ago. Real evasion is S6/S7.
9. Fuzz → crash → find offset → control EIP → remove bad chars → JMP ESP → shellcode. (Six milestones.)
10. The **handler was not up** when the staged payload connected (no stage delivered), or the **wrong `-f`/architecture** so it did not run / connect back (also: bad LHOST/LPORT, or AV killed it).
