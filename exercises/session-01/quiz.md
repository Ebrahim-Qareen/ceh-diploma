---
session: 1
title: Foundations, Lab Build & First Contact
doc: Quiz (10 questions)
---

# Session 1 — Quiz

Each question maps to a Session 1 learning objective (LO1-LO5 from the Session Plan).

## Questions

**Q1 (LO1, MCQ).** An attack is best described as the combination of which three elements?
- A. Tool + target + time
- B. Motive + method + vulnerability
- C. Exploit + payload + shell
- D. Recon + scanning + access

**Q2 (LO1, MCQ).** Put the 5 hacking phases in the correct order.
- A. Scanning → Recon → Access → Clearing Tracks → Maintaining Access
- B. Recon → Scanning → Gaining Access → Maintaining Access → Clearing Tracks
- C. Recon → Gaining Access → Scanning → Clearing Tracks → Maintaining Access
- D. Scanning → Gaining Access → Recon → Maintaining Access → Clearing Tracks

**Q3 (LO1, MCQ).** The single factor that separates a white-hat from a black-hat performing the identical nmap scan is:
- A. The tool version
- B. The time of day
- C. Written authorization / scope
- D. Whether the scan succeeds

**Q4 (LO2, MCQ).** In the Cyber Kill Chain, delivering a malicious attachment to a victim maps to which stage?
- A. Reconnaissance
- B. Weaponization
- C. Delivery
- D. Actions on Objectives

**Q5 (LO2, short).** An attacker creates a new local admin account for persistence after break-in. Name the MITRE ATT&CK tactic this falls under, and one log source a SOC analyst would check to detect it.

**Q6 (LO3, MCQ).** Which of the following is *out of scope* for this course's engagement?
- A. Scanning your own Metasploitable2 VM
- B. Grabbing banners from your Kali-built lab
- C. Scanning the academy's production Wi-Fi
- D. Reverting your target to a baseline snapshot

**Q7 (LO4, MCQ).** Why must the lab VMs sit on a host-only network?
- A. It's faster than NAT
- B. To isolate deliberately-vulnerable targets from the real network and internet
- C. Because Kali requires it
- D. To get internet access on the targets

**Q8 (LO4, short).** You are about to start an attack lab on Metasploitable2. What should you do *first* with respect to snapshots, and why?

**Q9 (LO5, MCQ).** Which command performs host discovery (a "who is alive" sweep) without a full port scan?
- A. `nmap -sV <ip>`
- B. `nmap -sn <cidr>`
- C. `nc -nv <ip> 21`
- D. `ping -c 3 <ip>`

**Q10 (LO5, scenario).** You run `nc -nv <MSF2_IP> 21` and see `220 (vsFTPd 2.3.4)`. What is this called, what two pieces of information did you just learn, and why does it matter for the next session?

## Answer key

1. **B** — Attack = Motive + Method + Vulnerability. (LO1)
2. **B** — Recon → Scanning → Gaining Access → Maintaining Access → Clearing Tracks. (LO1)
3. **C** — Authorization/scope is the only legal difference. (LO1)
4. **C** — Delivery (getting the weaponized payload to the victim). (LO2)
5. **Persistence** (ATT&CK tactic); detect via **Windows Security event logs** (e.g. account-creation event 4720) / EDR. (LO2)
6. **C** — The academy's production Wi-Fi is the real network — out of scope. (LO3)
7. **B** — Host-only isolates vulnerable targets from the real network/internet (safety control). (LO4)
8. **Take a `baseline-clean` snapshot (or revert to it) first**, so the lab starts from a known clean state and doesn't carry over changes from a previous lab. (LO4)
9. **B** — `nmap -sn <cidr>` is a ping/host-discovery sweep with no port scan. (`ping` only tests one host; not a sweep.) (LO5)
10. It's **banner grabbing**. You learned the **service (FTP / vsftpd)** and its **exact version (2.3.4)**. It matters because that version can be matched to known CVEs/exploits in the vulnerability-analysis and scanning work next session. (LO5)
