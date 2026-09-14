---
session: 7
title: Malware Threats & Analysis
duration_min: 240
---

# Session 7 — Session Plan

## Title
Malware Threats & Analysis (CEH Chapter 7)

## Module reference
- Malware concepts, propagation & the 5-stage lifecycle
- Classes: trojan/RAT, virus, worm, ransomware, fileless/LOLbins, rootkit
- Static analysis: hashing + VirusTotal, strings, PE imports
- Dynamic analysis: the isolated sandbox, ProcMon/TCPView/CurrPorts
- MITRE ATT&CK mapping, IOCs & the Pyramid of Pain
- Detection engineering: YARA (file) + Sigma (behaviour); countermeasures; incident triage report

## Learning objectives
By the end a student can:
1. Classify any sample by **behaviour** (propagation x purpose) and walk its **5-stage lifecycle**.
2. Explain trojans/RATs, viruses vs worms, ransomware, and fileless malware — and the tell that betrays each.
3. Perform **static analysis** safely: hash + VirusTotal, strings, PE imports.
4. Build and run an **isolated sandbox** and perform **dynamic analysis** (ProcMon/TCPView).
5. Map observed behaviour to **MITRE ATT&CK** and rank IOCs on the **Pyramid of Pain**.
6. Write a working **YARA** rule (file) and **Sigma** rule (behaviour) from their own analysis.
7. Produce a complete **incident triage report** — the session deliverable.

## Time distribution (target 240 min)
| Block | Min | Format |
|---|---|---|
| Bridge from S6 (foothold to artifact) | 4 | theory |
| Why malware matters | 5 | theory |
| Malware taxonomy (+ mini-lab) | 8 | theory |
| The malware lifecycle (+ mini-lab) | 7 | theory |
| Trojans & RATs (+ mini-lab) | 7 | theory |
| Viruses & worms (+ mini-lab) | 7 | theory |
| Ransomware (+ mini-lab) | 7 | theory |
| Fileless malware (+ mini-lab) | 7 | theory |
| Static vs dynamic (+ mini-lab) | 6 | theory |
| Static I: hash + VirusTotal (+ mini-lab) | 7 | tool |
| Static II: strings + imports (+ mini-lab) | 8 | tool |
| Dynamic 0: the sandbox (+ mini-lab) | 7 | tool |
| Dynamic: ProcMon/TCPView (+ mini-lab) | 8 | tool |
| Lab A — craft the sample (msfvenom) | 14 | hands-on |
| Lab B — static analysis | 16 | hands-on |
| Lab C — dynamic analysis (detonate) | 18 | hands-on |
| **Break** | 10 | — |
| ATT&CK mapping (+ mini-lab) | 7 | theory |
| IOCs & the Pyramid of Pain (+ mini-lab) | 7 | theory |
| YARA (+ mini-lab) | 8 | tool |
| The malware SOC flip | 6 | defender |
| Lab D — write YARA + Sigma | 18 | hands-on |
| Countermeasures (+ mini-lab) | 6 | defender |
| Lab E — incident triage report | 20 | hands-on |
| Where next / practice range | 5 | resources |
| Knowledge check (6 MCQs) | 10 | assess |
| Takeaways | 4 | summary |

## Materials
- Kali (build the sample) + an **isolated** Windows/Linux analysis VM with a clean snapshot
- Sysinternals (ProcMon, TCPView), `strings`, `pefile`/PE-bear, `yara`, `steghide`/`stegseek` (from S6 stego kit optional)
- Fallbacks under `saved/`: sample IOC sheet, `lab_c_beacon.pcap`, and event logs for students without a working sandbox

## Safety note
Lab A produces a **working trojan**. It stays on the host-only lab network, is never emailed or uploaded, and is deleted at session end. Live third-party samples are analysed **only** inside the isolated chamber.
