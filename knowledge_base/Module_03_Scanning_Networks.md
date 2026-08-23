---
source: Module 3 Scanning Networks.pdf (instructor deck, full)
session: 2
---

# Module 3 — Scanning Networks

## Official learning objectives (CEH Ch.3)

1. Explain Network Scanning Concepts
2. Explain Scanning Tools and Techniques
3. Explain Host Discovery Techniques
4. Explain Port and Service Discovery Techniques
5. Explain OS Discovery (Banner Grabbing/OS Fingerprinting)
6. Explain Scanning Beyond IDS and Firewall
7. Explain Source Code Review for Network Scanning

## 1. Network Scanning Concepts

Goal: identify live hosts, open ports, running services, OS, and
vulnerabilities on a target network. This is the second phase of the
hacking methodology — after recon, before enumeration.

Scanning discovers:
- Live hosts and their IP addresses
- Open ports on live hosts
- Operating systems and system architecture
- Services and their versions running on open ports
- Vulnerabilities in discovered services

## 2. Host Discovery

Two primary methods:

| Method | How it works | When to use |
|---|---|---|
| Ping sweep | Send ICMP echo requests to entire subnet, monitor for replies | Quick, but ICMP often blocked |
| ARP scan | Send broadcast ARP requests, wait for ARP replies | Local subnet only, very reliable (can't be blocked at host level) |

**Tools:** Angry IP Scanner (ping sweep GUI), `nmap -sn` (ping sweep),
`netdiscover` (ARP scan).

## 3. Port Scanning Techniques

### TCP Communication Flags

SYN, ACK, FIN, RST, PSH, URG — used in different scan types.

### TCP Scan Types

| Scan | Method | Stealth | Notes |
|---|---|---|---|
| TCP Connect (`-sT`) | Full 3-way handshake (SYN → SYN-ACK → ACK) | None — fully logged | Reliable but noisy |
| TCP SYN / Half-open (`-sS`) | SYN → SYN-ACK → RST (no ACK) | Moderate — some logs miss it | Default nmap scan; faster |
| TCP FIN (`-sF`) | Send FIN only | Higher — no SYN logged | Open port = no response; closed = RST |
| XMAS (`-sX`) | FIN+PSH+URG flags set | Higher | Same logic as FIN; **dangerous — can crash services** |

**Closed port behavior:** always replies with RST (but may be filtered by firewall).

### UDP Scanning (`-sU`)

Much slower and more intensive than TCP. Open ports may not respond at all;
closed ports send ICMP port-unreachable. Often skipped due to time cost,
but critical services run on UDP (DNS/53, SNMP/161, DHCP/67-68).

## 4. Nmap Usage Patterns (from instructor deck)

| Command Pattern | Purpose |
|---|---|
| `nmap -sn <subnet>` | Ping sweep — host discovery |
| `nmap <target>` | Basic port scan (top 1000) |
| `nmap -p <range> <target>` | Specific port range |
| `nmap -p- <target>` | All 65535 ports |
| `nmap -T<0-5> <target>` | Threading/timing (0=paranoid, 5=insane) |
| `nmap -sS <target>` | Stealth SYN scan |
| `nmap -sX <target>` | XMAS scan (use with permission only) |
| `nmap -O <target>` | OS detection |
| `nmap --script <script> <target>` | NSE script engine (`/usr/share/nmap/scripts/`) |
| `nmap -sV <target>` | Service version detection |
| `nmap -A <target>` | Aggressive — port + OS + version + scripts |
| `nmap -sU <target>` | UDP scan |

**Instructor's preferred scan:** `nmap -sS -sV -O -T4 <target>` (stealth
SYN + service version + OS detection, moderate speed).

**Warning:** nmap generates 100,000+ packets on a full scan — very noisy.
The "killing scan" (`-T5 -A -p-`) can crash weak targets.

## 5. OS Discovery

- **Passive:** monitor error messages, sniff traffic, check file extensions
  (`.aspx` = IIS/Windows)
- **Active:** send crafted packets, analyze TCP/IP stack behavior (TTL
  values, window sizes, DF bit) — `nmap -O`

## 6. Evasion Techniques (scanning past IDS/IPS/firewalls)

| Technique | How | Nmap flag |
|---|---|---|
| Source port manipulation | Forge traffic to look like it comes from a trusted port (e.g. 80) | `--source-port 80` |
| Packet fragmentation | Fragment packets below IDS reassembly threshold | `-f` or `--mtu 8` |
| IP address decoy | Scan from multiple spoofed IPs mixed with real | `-D RND:10` |
| MAC address spoofing | Forge MAC to bypass MAC-based ACLs | `--spoof-mac` |
| Source routing | Specify the route packets take | (manual crafting) |
| Packet encapsulation | Tunnel scan traffic inside another protocol | (manual) |

## 7. Other Scanning Tools

- **Netcat (`nc`)** — manual port scanning + banner grabbing
- **Metasploit Framework** — auxiliary scanner modules (`auxiliary/scanner/`)
- **Python** — instructor teaches building a custom port scanner

## 8. Scanning Countermeasures

- Don't be too noisy — start basic, then go advanced
- Be careful not to affect target operations
- Use multiple techniques (TCP + UDP + version scan)
- Perform scanning at different times to avoid pattern detection

### Defensive countermeasures

- Properly configure firewalls to block unauthorized scanning
- Deploy IDS/IPS to detect scan patterns
- Close unnecessary ports and disable unused services
- Regularly scan own networks to find what attackers would find
