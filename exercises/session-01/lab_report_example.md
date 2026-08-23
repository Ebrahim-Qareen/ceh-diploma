---
doc: Lab Report — FILLED EXAMPLE (Session 1)
note: Show this beside the blank template so students see the expected depth.
---

# Lab Report — Session 1: Foundations, Lab Build & First Contact

**Student:** A. Sample  **Pair partner:** B. Sample  **Date:** 2026-08-22

## 1. Objective
Build an isolated Kali + Metasploitable2 host-only lab, snapshot it, then make first contact — discover the target and grab service banners.

## 2. Environment
| Item | Value |
|---|---|
| Attacker box | KALI-ATK01 (192.168.56.101) |
| Target(s) | METASPLOITABLE2 (192.168.56.120) |
| Network | host-only 192.168.56.0/24 |
| Snapshot used | baseline-clean (Y) |

## 3. What I did — steps, commands, results
| # | Command / action | Expected | Actual result | Right / Wrong |
|---|---|---|---|---|
| 1 | `ip a` on Kali | host-only 192.168.56.x | eth0 = 192.168.56.101 | Right |
| 2 | Set both VM adapters to Host-only | both isolated | Kali was on NAT at first — no target found | Wrong → fixed |
| 3 | `sudo nmap -sn 192.168.56.0/24` | target listed up | 192.168.56.120 Host is up (VMware MAC) | Right |
| 4 | `ping -c 3 192.168.56.120` | 3 replies TTL~64 | 3 replies, ttl=64 | Right |
| 5 | `nmap -sV --top-ports 20 192.168.56.120` | services + versions | 21 vsftpd 2.3.4, 22 OpenSSH 4.7p1, 25 Postfix, 80 Apache 2.2.8 | Right |
| 6 | `nc -nv 192.168.56.120 21/22/25` | raw banners | got all 3 banners (below) | Right |

## 4. Evidence
```
$ sudo nmap -sn 192.168.56.0/24
Nmap scan report for 192.168.56.120
Host is up (0.00042s latency).
MAC Address: 00:0C:29:xx:xx:xx (VMware)

$ nc -nv 192.168.56.120 21
220 (vsFTPd 2.3.4)
$ nc -nv 192.168.56.120 22
SSH-2.0-OpenSSH_4.7p1 Debian-8ubuntu1
$ nc -nv 192.168.56.120 25
220 metasploitable.localdomain ESMTP Postfix (Ubuntu)
```

## 5. What went wrong & how I fixed it
My first `nmap -sn` found nothing. Cause: Kali's adapter was still on NAT from a previous class, so it wasn't on the host-only net. Fixed by switching Kali's network adapter to Host-only in VMware and re-checking `ip a` (address changed to 192.168.56.101). Discovery then worked.

## 6. What I learned
- Host discovery (`-sn`) and a full port scan are different steps — sweep first, then dig.
- A banner hands you the exact software version for free (vsftpd 2.3.4) — that version is the lead for finding a known exploit later.
- Network adapter mode is the #1 reason a target "disappears."

## 7. SOC angle
All of this created inbound connection attempts and FTP/SSH/SMTP session logs on the target — a defender would see a burst of connections from one internal IP hitting many ports/services in seconds, the classic scan signature.
