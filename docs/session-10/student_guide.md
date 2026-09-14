---
session: 10
title: Evasion, Wireless & Emerging Tech — Student Guide (FINAL)
---

# Session 10 — Student Guide (FINAL SESSION)

## What you will be able to do
Sweep the last of the attack surface — evade the defences that watch you, break Wi-Fi, assess mobile/IoT/cloud, and audit the crypto under everything — then tie all ten sessions into a defence-in-depth capstone.

## The four blocks
1. **Evasion** — IDS/IPS detection methods; evade by fragmentation/encoding (signature) or low-and-slow/blend-in (anomaly); firewall tunnelling; honeypots.
2. **Wireless** — WEP (dead) / WPA2 (weak-passphrase → offline crack) / WPA3 (fixed); deauth → handshake capture → aircrack.
3. **Emerging surface** — mobile (app storage, pinning, MDM), IoT/OT (default creds, old firmware, no-auth protocols, physical stakes), cloud (shared responsibility, public buckets, IAM).
4. **Cryptography** — symmetric (confidentiality) / asymmetric (key-exchange + signatures) / hashing (integrity); TLS hybrid handshake; crypto fails in *deployment*.

## Key insights
- **Evasion targets the detection method** — know whether the sensor matches signatures or learns baselines.
- **Wireless = protocol + passphrase** — WPA2's whole risk is a weak passphrase cracked offline.
- **Cloud/IoT fail on configuration** — check, don't exploit; public bucket, default creds.
- **Match the crypto tool to the job**; crypto fails at the edges (old algorithms, weak keys, unverified signatures).
- **Security is layers** — attackers chain weaknesses; defenders chain controls; detection sits under all of it.

## Deliverable — your graduation piece
A **defence-in-depth capstone report** (template in `exercises/session-10/`) spanning all ten sessions: attack narrative, findings by layer, defence-in-depth analysis, prioritised remediation, detections. Keep it for your portfolio.

## The rules you never break
Evasion, wireless, cloud, and device attacks target only lab hosts, your own AP/adapter, and your own cloud/devices. Everything else is a crime.

## And then — you graduate
From your first ping sweep to a full-stack, both-chairs security professional. Pick your depth, keep the reps, and go do the work.
