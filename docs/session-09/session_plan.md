---
session: 9
title: Sniffing, MITM, Session Hijacking, Social Engineering & DoS
duration_min: 240
---

# Session 9 — Session Plan

## Title
Sniffing, MITM, Session Hijacking, Social Engineering & DoS (CEH Chapters 8, 9, 10, 11)

## Module reference
- Sniffing (passive vs active), ARP poisoning MITM, SSL strip / HTTPS downgrade
- Session hijacking: concepts, application-level (sniff/XSS/prediction/fixation/replay/MitB), CSRF, network-level TCP hijacking
- Social engineering: psychology (authority/urgency/trust/fear/reciprocity), vectors, phishing with SET
- DoS/DDoS: volumetric / protocol (SYN flood) / application-layer (Slowloris)
- Detection across all four surfaces + countermeasures + assessment report

## Learning objectives
By the end a student can:
1. Explain passive vs active sniffing and perform an **ARP-poisoning MITM**; capture a cleartext credential.
2. Explain **SSL strip** and why **HSTS** defeats it.
3. Steal and **replay a session token** for account takeover; explain why login MFA doesn't stop it; build a **CSRF** PoC.
4. Explain **network-level TCP hijacking** and why encryption/random ISNs defeat it.
5. Name the **psychological levers** of social engineering and the phishing **vectors**; build a SET credential harvester (lab only, ethics-gated).
6. Classify **DoS** (volumetric/protocol/app-layer) and run a **SYN flood + Slowloris** with the matching mitigation.
7. Write **detections** for each surface (ARP anomaly, session-token-from-two-IPs, SYN-flood threshold) and a four-surface **assessment report**.

## Time distribution (target 240 min)
| Block | Min | Format |
|---|---|---|
| Bridge from S8 | 4 | theory |
| Why these attacks | 5 | theory |
| Sniffing (+ mini-lab) | 7 | theory |
| ARP poisoning & MITM (+ mini-lab) | 7 | attack |
| HTTPS downgrade / SSL strip (+ mini-lab) | 6 | attack |
| Session hijacking concepts (+ mini-lab) | 6 | theory |
| App-level hijacking (+ mini-lab) | 7 | attack |
| Steal & replay (+ mini-lab) | 6 | attack |
| CSRF (+ mini-lab) | 6 | attack |
| TCP hijacking (+ mini-lab) | 6 | attack |
| Lab A — ARP poison + sniff | 18 | hands-on |
| Lab B — steal & replay a cookie | 14 | hands-on |
| **Break** | 10 | — |
| Social engineering psychology (+ mini-lab) | 7 | theory |
| SE vectors (+ mini-lab) | 6 | theory |
| Phishing with SET (+ mini-lab) | 7 | tool |
| Lab C — SET credential harvester | 16 | hands-on |
| DoS/DDoS concepts (+ mini-lab) | 6 | theory |
| SYN flood & Slowloris (+ mini-lab) | 6 | attack |
| Lab D — controlled DoS | 14 | hands-on |
| The consolidated SOC flip | 6 | defender |
| Lab E — detect + assessment report | 20 | hands-on |
| Countermeasures (+ mini-lab) | 6 | defender |
| Where next / practice | 5 | resources |
| Knowledge check (6 MCQs) | 10 | assess |
| Takeaways | 4 | summary |

## Materials
- Kali (bettercap/ettercap, Wireshark, SET/setoolkit, hping3, slowhttptest) + two lab VMs (victim + a gateway/target) on the host-only network + a lab web service (HTTP for sniffing, and a small server for DoS)
- DVWA (CSRF + session labs)
- `scripts/lab_s9_setup.sh` (arpwatch install + isolation reminders); DoS uses hping3/slowhttptest against a throwaway lab web VM
- Fallbacks under `saved/`: `session9_mitm.pcap` (a capture with a cleartext credential), `arpwatch_alert.txt`, and a sample phishing email for the analysis exercise

## Safety note
MITM, phishing, and DoS against systems you do not own are serious crimes. Everything here is isolated-lab-only; the phishing lab is ethics-gated (consenting test accounts, never a real person or brand). The instructor states the legal line before Labs A, C, and D.
