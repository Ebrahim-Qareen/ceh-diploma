---
session: 6
title: System Hacking III — Privilege Escalation & CTF Capstone
duration_min: 240
---

# Session 6 — Session Plan

## Title
System Hacking III — Privilege Escalation & CTF Capstone (CEH Module 6 pt3+pt4)

## Module reference
- Privilege escalation concept + the enumeration loop (vertical / horizontal)
- Linux privesc: linPEAS, SUID + GTFOBins, sudo, cron, capabilities, kernel
- Windows privesc: winPEAS, service misconfig, token abuse (SeImpersonate/potato), Mimikatz/LSASS
- Steganography (image stego, NTFS ADS) · two capstone CTFs (DoubleTrouble, Blackpearl) · the engagement report

## Learning objectives
By the end a student can:
1. Run the privesc **enumeration loop** (enumerate → identify → abuse → verify) on Linux and Windows.
2. Escalate on Linux via a **SUID/GTFOBins** binary and a **sudo/cron** misconfiguration.
3. Escalate on Windows via a **service misconfig** and **token abuse** (SeImpersonate → potato → SYSTEM).
4. Dump credentials from **LSASS with Mimikatz** and reuse them to move laterally.
5. Hide and recover data with **steganography** (steghide/stegseek, NTFS ADS).
6. Complete **two full-chain capstones** (recon → shell → root) unaided.
7. Write a **privilege-escalation detection rule** (LSASS access / 4672 / 7045).
8. Write a complete **engagement report** — the deliverable that closes the offensive half.

## Time distribution (target 240 min; plan ~257 with documented absorb options)
| Block | Min | Format |
|---|---|---|
| Where we left off (bridge) | 6 | theory |
| Lab pre-flight | 5 | hands-on |
| Privesc concept + loop (+ mini-lab) | 8 | theory |
| Linux surface (+ mini-lab) | 8 | theory |
| linPEAS (+ mini-lab) | 7 | theory |
| Lab 1 — SUID + GTFOBins → root | 15 | hands-on |
| sudo & cron (+ mini-lab) | 8 | theory |
| Lab 2 — sudo/cron → root | 14 | hands-on |
| Windows surface (+ mini-lab) | 8 | theory |
| Token abuse (+ mini-lab) | 8 | theory |
| Lab 3 — service/token → SYSTEM | 15 | hands-on |
| winPEAS + Mimikatz (+ mini-lab) | 9 | theory |
| **Break** | 10 | — |
| Lab 4 — Mimikatz LSASS dump | 12 | hands-on |
| Steganography (+ mini-lab) | 7 | theory |
| Lab 5 — steghide/stegseek + ADS | 10 | hands-on |
| The capstone (methodology) | 6 | theory |
| Lab 6 — Capstone A: DoubleTrouble | 25 | hands-on |
| Lab 7 — Capstone B: Blackpearl | 25 | hands-on |
| The privesc SOC flip | 6 | defender |
| Lab 8 — detection rule | 16 | hands-on |
| Lab 9 — engagement report | 14 | hands-on |
| Where next · knowledge check · practice · wrap | 23 | wrap |
| **Total** | **~257** | ~56% hands-on (9 labs + 8 mini-labs) |

### If you run over
Absorb order (never cut the capstones or Lab 8/9):
1. Run **one capstone in class** (DoubleTrouble), set the other (Blackpearl) as homework with a hint sheet.
2. Move **Lab 2** (second Linux path) to homework — the mini-lab shows the sudo/cron checks.
3. Trim **Lab 5** (stego) to the stegseek demo; the ADS half becomes homework.

## Delivery notes
- Every theory page has a **mini-lab** ("Prove it") — run them live; they make each concept concrete before the milestone lab.
- Diagrams are stepped (Back/Play/Next): the privesc loop, cron abuse, token/potato, Mimikatz/LSASS, and the capstone methodology.
- Enumerate-before-exploit is the spine — do not let students guess techniques before running linPEAS/winPEAS.

## Prerequisites
- From S5: at least one **low-privilege shell** per student they can reproduce (the foothold record).
- linPEAS/winPEAS and Mimikatz staged; both capstone VMs (DoubleTrouble, Blackpearl) imported + snapshotted.

## Tools / VMs needed
Kali, the low-priv foothold targets (WIN10, Metasploitable2-family), the `ceh.lab` DC (for Mimikatz), and **DoubleTrouble + Blackpearl** capstone VMs. Tools: linPEAS/winPEAS, GTFOBins, PrintSpoofer/GodPotato, Mimikatz, steghide/stegseek, gobuster, msfconsole.

## Deliverable
A complete **engagement report** for at least one capstone (exec summary, scope, methodology, findings with severity + remediation, proof) + one **privilege-escalation detection rule**.

## Open items
- Confirm capstone VM sources on the day (VulnHub); snapshot before class.
- Real Mimikatz/Sysmon captures deferred (no Windows/AD in the build environment) — SIM-SCREENs stand in.
