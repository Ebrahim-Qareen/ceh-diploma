---
session: 3
title: Scanning & Enumeration
---

# Session 3 — Student Guide

Your take-home reference. Everything here is yours to keep and re-read.

## 1. The one idea: scanning is loud
Recon (Session 2) was invisible — you read public data and the target never knew. **Scanning is
the opposite.** The moment you send a packet *at* a target, your IP lands in its logs. Scanning is
the single most commonly detected stage of a real intrusion. So for every scan you learn to run,
you also learn what it leaves behind.

## 2. Host discovery — ask the right question
| You are… | Use | Why |
|---|---|---|
| On the same segment (your lab) | **ARP** (`nmap -sn`, `arp-scan`, `netdiscover`) | Can't be blocked; local only |
| Across a router (the internet) | **ICMP** (`-PE`) or **TCP ping** (`-PS443`, `-PA80`) | ICMP is often dropped; TCP ping usually gets through |
| Getting no reply but sure it's up | **`-Pn`** | Skips discovery, scans anyway |

**The rule:** ICMP silence means "no answer," never "no host." Windows Firewall blocks ICMP by
default — a live Windows box looks dead to a ping sweep. `-Pn` is the fix, and the #1 beginner miss.

## 3. Scan types — learn the reflex, not the flags
| Port state | to a SYN | to FIN/NULL/Xmas | to an ACK |
|---|---|---|---|
| **Open** | SYN/ACK | *silence* | RST |
| **Closed** | RST | RST | RST |
| **Filtered** | *silence* / ICMP unreachable | *silence* | *silence* |

- **SYN (`-sS`)** — half-open: SYN → SYN/ACK → **RST** (never completes). Fast and light. *Not* invisible any more — a modern IDS sees the SYN flood regardless.
- **Connect (`-sT`)** — completes the handshake, so the application logs it. Use when you lack root.
- **FIN/NULL/Xmas (`-sF`/`-sN`/`-sX`)** — can only say "not closed" (open+filtered both silent). Slip past SYN-only devices. Useless against Windows (it RSTs everything).
- **ACK (`-sA`)** — maps the firewall, not open ports. RST = unfiltered, silence = filtered.
- **UDP (`-sU`)** — slow (ICMP rate-limiting). Always scope it: `-p 53,161,123,137`. Where SNMP/DNS/DHCP live.

## 4. The workflow: breadth, then depth
```
masscan / rustscan   → find open ports fast (all 65,535 in seconds)
        ↓ open ports
nmap -sS -sV -O -T4 -p <those>   → interrogate only them (service, version, OS)
```
Read version/OS output **critically** — it guesses. It called a real service `tcpwrapped` and
returned "no exact OS match" in our own captures. Confirm by hand with netcat when unsure.

`-T` timing: `-T4` on a fast LAN (your lab), `-T0/-T1` to creep under an IDS (very slow). `-T5` can miss ports and crash weak targets.

## 5. Enumeration — the funnel
```
open port → service → version → users / shares / config / policy → way in (S4/S5)
```
Enumeration is a *conversation* with the service — you connect and query it, sometimes anonymously,
sometimes with a credential. That's why it's louder and more logged than scanning.

| Service | Port | Tool | Leaks |
|---|---|---|---|
| SMB | 139/445 | `enum4linux-ng`, `smbclient`, `smbmap`, `nxc` | shares, users, groups, policy, version |
| SNMP | 161/udp | `onesixtyone`, `snmpwalk` | processes, software, interfaces, accounts |
| LDAP | 389/636 | `ldapsearch`, `windapsearch`, `nxc` | every user/group/computer in the domain |
| NFS | 2049/111 | `showmount -e` | exported directories |
| FTP | 21 | `ftp`, `--script ftp-anon` | anonymous login, version |
| SMTP | 25 | `smtp-user-enum` | valid usernames |
| RPC/NetBIOS | 135/137-139 | `rpcclient -U "" -N`, `nbtscan` | users, domain, endpoints |

**The SMB lesson:** on a modern Windows box, `enum4linux-ng` returns almost nothing — SMBv1 and null
sessions are off by default since Win10 FCU / Server 2019. That's a *hardening finding*, not a
failure. Authenticated enumeration (`nxc ... -u -p`) still works.

## 6. Tool currency (2026) — verify before you teach the command
| Dead / old | Use instead |
|---|---|
| `enum4linux` | **`enum4linux-ng`** |
| `crackmapexec` / `cme` | **NetExec / `nxc`** (CME unmaintained since 2023) |
| one giant `nmap -A -p-` | **masscan/rustscan breadth → nmap depth** |
Always run `<tool> --version` and check the last release before you rely on it.

## 7. MITRE ATT&CK
- **Reconnaissance (TA0043):** T1595 Active Scanning · T1595.001 Scanning IP Blocks · T1590 Gather Victim Network Info.
- **Discovery (TA0007):** T1046 Network Service Discovery · T1018 Remote System Discovery · T1135 Network Share Discovery · T1087 Account Discovery · T1069 Permission Groups Discovery · T1201 Password Policy Discovery.

## 8. The SOC flip — what the defender sees
The universal signature under every scan and enumeration is **one source → many ports/hosts → short
window**. Individual packets can be forged; the *pattern* of touching everything can't be hidden.
- SYN scan → many SYNs, no completed handshakes (IDS portscan; Win Firewall 5156).
- Connect scan → the above **plus** application logs on every open port.
- NULL/FIN/Xmas → illegal flag combos, high-signal.
- UDP → burst of outbound ICMP port-unreachable.
- Enumeration → service logs (4624/4625 logon, 5140/5145 share access, LDAP binds, SMTP VRFY).
The honest truth: a modern EDR/IDS catches a default `nmap -A` in seconds. Evasion buys time and
muddies attribution; it does not grant invisibility.

## 9. The deliverable
A **ranked target profile** — per host: live/dead + how confirmed, open TCP/UDP ports, service +
version, OS guess + confidence, shares, users, SNMP/LDAP findings, and a ranked "most likely way
in," with your Lab 7 detection rule attached. It is Session 4's input.

## Key terms
**Half-open scan** · **filtered vs closed** · **null session** · **community string** · **naming
context (LDAP base DN)** · **NSE category** · **breadth-then-depth** · **`-Pn`** · **the SOC flip**.
