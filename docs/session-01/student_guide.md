---
session: 1
title: Foundations, Lab Build & First Contact
doc: Student Guide
---

# Session 1 — Student Guide

Simplified notes for self-review after class. This matches the session page.

## 1. The attacker mindset
You are learning offense to get better at defense (SOC). To catch an attacker you have to know what they do and in what order.

**Every attack = Motive + Method + Vulnerability.** Take away any one and the attack fails — that's where defenders win.

**Hacker classes:** white (authorized/ethical — this is us), black (malicious), gray (no malice, no permission), suicide, script kiddie, state-sponsored, hacktivist. The line between white and black is one word: **authorization**.

**The 5 phases (memorize the order):**
1. **Reconnaissance** — gather info (passive = quiet, active = you touch the target)
2. **Scanning** — find live hosts, open ports, services
3. **Gaining Access** — exploit a weakness to get in
4. **Maintaining Access** — persistence (backdoors, escalated privileges)
5. **Clearing Tracks** — remove evidence

**SOC angle (why you care):** each phase leaves a different trace — recon shows in external logs, scanning in IDS/firewall logs, access in auth logs/EDR, persistence in new services/scheduled tasks, clearing tracks as suspicious log gaps.

## 2. Frameworks
- **Cyber Kill Chain** (Lockheed Martin): Recon → Weaponize → Deliver → Exploit → Install → C2 → Actions on Objectives.
- **MITRE ATT&CK**: a matrix of attacker *tactics* (the "why") and *techniques* (the "how"). You'll use this all course to describe what an attacker did.
- **Diamond Model**: adversary ↔ infrastructure ↔ capability ↔ victim.

## 3. Authorization & scope (the legal line)
The only legal difference between a pentester and a criminal is a **signed scope + rules of engagement (RoE)**.
- **Scope** = exactly which IPs/domains you may test.
- **RoE** = allowed times, allowed techniques, and hard no-gos (e.g. no DoS).
- **Your scope for this whole course = your own host-only lab only.** Nothing else. Scanning the academy network or the internet is out of scope and can be a crime.

## 4. The lab (what you're building)
Host-only network, everything isolated from the real network:
- **KALI-ATK01** — your attacker box (used every session).
- **METASPLOITABLE2** — deliberately vulnerable Linux target.
- **WIN10-TGT01 / WINSRV19-TGT01** — Windows targets (build as homework, used from Session 3).

**Why host-only:** the vulnerable targets must never reach the internet. Safety control.

**Snapshots:** take a "baseline" snapshot right after building each VM. Revert to baseline before each session so old labs don't break new ones.

## 5. Passive vs active footprinting
- **Passive** — you gather info without touching the target (OSINT — that's Session 2).
- **Active** — you send packets at the target; it can log you.
- **First contact** = the first active packets you send at a target you're *allowed* to test.

## 6. First contact — step by step (for self-review)
Replace `<MSF2_IP>` with your Metasploitable2 IP, `<CIDR>` with your host-only subnet.

```
# 1. Check your own address / subnet
ip a

# 2. Who is alive on the network? (host discovery)
sudo nmap -sn <CIDR>

# 3. Can I reach the target?
ping -c 3 <MSF2_IP>

# 4. Light service/version sweep (full scanning is Session 3)
nmap -sV --top-ports 20 <MSF2_IP>

# 5. Grab service banners by hand (this is "first contact")
nc -nv <MSF2_IP> 21     # expect: 220 (vsFTPd 2.3.4)
nc -nv <MSF2_IP> 22     # expect: SSH-2.0-OpenSSH_4.7p1
nc -nv <MSF2_IP> 25     # expect: 220 ... ESMTP Postfix
```
Copy at least 3 banners word-for-word into your lab report.

## Key terms
- **Footprinting/Reconnaissance** — gathering information about a target before attacking.
- **Passive recon** — info gathering with no direct contact with the target.
- **Active recon** — info gathering that touches the target (may be logged).
- **Host discovery** — finding which hosts are alive on a network.
- **Banner grabbing** — reading the identifying text a service returns on connect (often reveals software + version).
- **Scope** — the exact systems you are authorized to test.
- **Rules of engagement (RoE)** — the agreed rules for how/when you may test.
- **Host-only network** — a virtual network isolated from the physical LAN and internet.
- **Baseline snapshot** — a clean saved VM state you revert to before each session.
- **MITRE ATT&CK** — framework of attacker tactics and techniques.
- **Cyber Kill Chain** — 7-stage model of an intrusion.
