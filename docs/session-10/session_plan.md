---
session: 10
title: Evasion, Wireless & Emerging Tech (FINAL)
duration_min: 240
---

# Session 10 — Session Plan (FINAL SESSION)

## Title
Evasion, Wireless & Emerging Tech — the diploma capstone (CEH Chapters 12, 16, 17, 18, 19, 20)

## Module reference
- Evading IDS, firewalls & honeypots (Ch.12)
- Wireless attacks: WEP/WPA2/WPA3, deauth, handshake capture, evil twin (Ch.16)
- Emerging-tech sweep: mobile (Ch.17), IoT/OT (Ch.18), cloud (Ch.19)
- Cryptography: symmetric/asymmetric/hashing, TLS hybrid, signatures, weak-crypto findings (Ch.20)
- The everywhere SOC flip, defence in depth, and the ten-session capstone

## Learning objectives
By the end a student can:
1. Explain IDS/IPS detection methods and **evade** them (fragmentation, decoys, timing, tunnelling); explain firewall/honeypot evasion.
2. Assess **wireless**: identify WEP/WPA2/WPA3, capture a WPA2 handshake via deauth, and crack it offline.
3. Sweep the **emerging surface** — mobile (OWASP Mobile, app static analysis), IoT/OT (default creds, weak protocols), cloud (shared responsibility, public buckets, IAM).
4. Use and **audit cryptography** — the three tools, the TLS hybrid handshake, digital signatures, and weak-deployment findings.
5. Map every attack to its **detection** and articulate **defence in depth** across the whole stack.
6. Produce a **defence-in-depth capstone report** tying all ten sessions together.

## Time distribution (target 240 min)
| Block | Min | Format |
|---|---|---|
| Bridge / the whole arc | 4 | theory |
| Why the sweep | 5 | theory |
| IDS/IPS & detection methods (+ mini-lab) | 7 | theory |
| IDS evasion (+ mini-lab) | 7 | attack |
| Firewalls & evasion (+ mini-lab) | 7 | attack |
| Honeypots (+ mini-lab) | 6 | theory |
| Lab A — nmap evasion vs a lab IDS | 16 | hands-on |
| Wireless protocols (+ mini-lab) | 7 | theory |
| Wireless attacks (+ mini-lab) | 7 | attack |
| WPA2 handshake flow (+ mini-lab) | 6 | attack |
| Lab B — capture & crack a WPA2 handshake | 16 | hands-on |
| **Break** | 10 | — |
| Mobile (+ mini-lab) | 6 | theory |
| IoT & OT (+ mini-lab) | 6 | theory |
| Cloud (+ mini-lab) | 6 | theory |
| Lab C — open bucket + default device | 14 | hands-on |
| Cryptography fundamentals (+ mini-lab) | 7 | theory |
| Hybrid crypto & TLS (+ mini-lab) | 6 | theory |
| Hashing, signatures & weakness (+ mini-lab) | 6 | theory |
| Lab D — crypto hands-on + audit | 14 | hands-on |
| The everywhere SOC flip | 6 | defender |
| Lab E — defence-in-depth capstone | 20 | hands-on |
| Defence in depth | 6 | defender |
| What you can now do (the whole map) | 5 | summary |
| Where next / careers | 5 | resources |
| Final knowledge check (6 MCQs) | 10 | assess |
| Takeaways / graduation | 4 | summary |

## Materials
- Kali (nmap evasion flags, aircrack-ng suite, openssl, awscli/curl) + a **monitor-mode Wi-Fi adapter** + a **test AP** (weak passphrase for Lab B) + a lab host running **Snort/Suricata** (Lab A) + a test cloud bucket / lab IoT device (Lab C)
- `scripts/lab_s10_setup.sh` (IDS target reminder, wireless-adapter check, a public-then-fixed test bucket helper)
- Fallbacks under `saved/`: `wpa2_handshake.cap` (a capture to crack without an adapter), `suricata_scan_alerts.log`, `open_bucket_listing.txt`, and a weak-cipher `ssl-enum` sample

## Safety note
Evasion, wireless, cloud, and device attacks must target only lab hosts, your own AP/adapter, and your own cloud/devices. Attacking others' networks, Wi-Fi, cloud, or IoT is illegal. The instructor states the line before Labs A/B/C.
