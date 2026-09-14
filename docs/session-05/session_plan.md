---
session: 5
title: System Hacking II — Exploitation, Shells & Payloads
duration_min: 240
---

# Session 5 — Session Plan

## Title
System Hacking II — Exploitation, Shells & Payloads (CEH Module 6 pt2)

## Module reference
- Manual exploitation workflow · Metasploit framework · payload generation (msfvenom)
- Shell types (bind vs reverse, full treatment) · staged vs stageless · shell upgrade / meterpreter (intro)
- Buffer overflow & RCE (guided) · credential-based access (bridge from S4, bridge to S6)

## Learning objectives
By the end of the session a student can:
1. Walk the six-step exploitation pipeline and **read a PoC before running it**.
2. Exploit a service **manually** and then **via Metasploit**, and state what the framework automates (and does not).
3. Fire **EternalBlue (MS17-010)** end to end and land a **SYSTEM** shell.
4. Explain and demonstrate **bind vs reverse** shells and why reverse wins through a firewall.
5. Generate payloads with **msfvenom** (staged vs stageless), catch them with `multi/handler`, and **upgrade a dumb shell**.
6. Use an **S4 credential** to get a shell with no exploit (`psexec`/`evil-winrm`).
7. Walk a **stack buffer overflow** end to end (fuzz → offset → EIP → bad chars → JMP ESP → shellcode) and name the modern mitigations.
8. Write **one working reverse-shell detection rule** and assemble a per-host **foothold record**.

## Time distribution (target 240 min; plan ~253 with documented absorb options)
| Block | Min | Format |
|---|---|---|
| Where we left off (bridge) | 7 | theory |
| Lab pre-flight | 5 | hands-on |
| Exploitation pipeline (+ mini-lab) | 8 | theory |
| Lab 1 — manual vsftpd | 15 | hands-on |
| Metasploit model + msfconsole (+ mini-lab) | 9 | theory |
| Lab 2 — same via MSF | 12 | hands-on |
| EternalBlue chain (+ mini-lab) | 7 | theory |
| Lab 3 — EternalBlue → SYSTEM | 15 | hands-on |
| Bind vs reverse (+ mini-lab) | 8 | theory |
| Lab 4 — bind blocked / reverse out | 12 | hands-on |
| Staged vs stageless + msfvenom (+ mini-lab) | 9 | theory |
| **Break** | 10 | — |
| Lab 5 — msfvenom + handler | 14 | hands-on |
| Shell upgrade (+ mini-lab) | 7 | theory |
| Lab 6 — upgrade a shell | 10 | hands-on |
| Credential access (+ mini-lab) | 6 | theory |
| Lab 7 — psexec/evil-winrm | 10 | hands-on |
| Buffer overflow theory (+ mini-lab) | 12 | theory |
| Lab 8 — guided BOF | 20 | hands-on |
| The SOC flip | 6 | defender |
| Lab 9 — detection rule | 16 | hands-on |
| Lab 10 — foothold record | 12 | hands-on |
| Into Session 6 | 6 | theory |
| Knowledge check · practice · wrap | 19 | wrap |
| **Total** | **~253** | ~54% hands-on (10 labs + 8 mini-labs) |

### If you run over
Absorb order (never cut Lab 3, Lab 9, Lab 10):
1. Run **Lab 8 as a demo only** (project the guided BOF; students repeat it as homework with the saved states).
2. Move **Lab 6** (shell upgrade) to homework — the mini-lab already shows the pty/stty trick.
3. Trim **Lab 2** to a 4-minute side-by-side against Lab 1.

## Delivery notes
- Every theory page has a **simple mini-lab** ("Prove it") — run them live; they are 2–3 minutes each and make the concept concrete before the milestone lab.
- Diagrams are stepped: use Back/Play/Next live so students **watch** the mechanism (pipeline, EternalBlue chain, bind vs reverse, the BOF stack).
- Manual before framework is deliberate (Lab 1 before Lab 2). Do not skip Lab 1.

## Prerequisites (student background)
MCSA + Linux + CCNA. Comfortable in a shell; understands TCP ports and Windows/Linux basics.

## Prerequisites (from earlier sessions)
The **S4 access plan** (per host: CVE + public-exploit? + a credential and how). At least one working S4 credential for Lab 7.

## Lab prep this session requires (before class)
- WIN7-TGT01 unpatched, SMBv1 on (from S3) — confirm MS17-010 with the auxiliary check.
- Metasploitable2 up (vsftpd 2.3.4).
- `vulnserver` + Immunity Debugger + `mona.py` on WIN10-TGT01 for Lab 8 (primary); a Kali `gdb`/`pwndbg` fallback binary.
- Metasploit DB initialised (`msfdb init`). Snapshots `pre-s5` on every target (EternalBlue/BOF can crash them).

## Tools / VMs needed
Kali (msfconsole, msfvenom, impacket, evil-winrm, nc, gdb/pwndbg), Metasploitable2, WIN7-TGT01, WIN10-TGT01, `ceh.lab` DC.

## Deliverable
The **foothold record** (per host: exploit/cred, payload, shell type, user context landed as, proof) + one **reverse-shell detection rule**. The foothold record is Session 6's input.

## Open items
- Confirm the two BOF practice rooms' tier on the day (`bufferoverflowprep`, `gatekeeper`) — API rate-limited at build time.
- Real msfconsole/meterpreter captures deferred (no Windows/AD in the build environment) — self-contained SIM-SCREENs stand in; capture on the monitored lab when available.
