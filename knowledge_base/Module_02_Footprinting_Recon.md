---
source: Module 2 footprinting and recon.pdf (instructor deck, full)
session: 1 (lab build), 2 (recon techniques)
---

# Module 2 — Footprinting and Reconnaissance

> This module is split across two sessions: **Session 1** covers the lab
> build (Part 1 of the instructor deck), **Session 2** covers the
> footprinting/recon techniques (Part 2).

## Official learning objectives (CEH Ch.2)

1. Explain Footprinting Concepts
2. Perform Footprinting through Search Engines and OSINT
3. Perform Footprinting through Web Services
4. Perform Footprinting through Social Networking Sites
5. Perform Website/Email/DNS/Network Footprinting
6. Explain Footprinting Tools and Countermeasures

## Part 1 — Lab Build (mapped to Session 1)

Lab requirements and VM setup — see `labs/lab_design.md` for full specs.
The instructor deck specifies: VMware Workstation, Kali Linux, Windows 10,
Windows Server 2019, Metasploitable 2 — all on a host-only network.

## Part 2 — Footprinting and Reconnaissance (mapped to Session 2)

### What is footprinting?

Process of gathering as much information as possible about the target
before attacking. More information = easier exploitation. Two types:
passive (no direct interaction with target) and active (direct interaction,
activity may be logged).

### Passive Footprinting Techniques

| # | Technique | Tool/Resource |
|---|---|---|
| 1 | Search engine recon | Google Dorks: `site:`, `filetype:`, `ext:`, `inurl:`, `intitle:` |
| 2 | Google Hacking Database | Predefined dork queries for finding exposed data |
| 3 | IoT/device search | Shodan |
| 4 | Domain/subdomain/OS info | Netcraft |
| 5 | Certificate transparency | crt.sh (subdomain discovery via SSL cert logs) |
| 6 | Email harvesting | hunter.io |
| 7 | OSINT aggregation | theHarvester (emails, subdomains, IPs from multiple sources) |
| 8 | Subdomain enumeration | Sublist3r |
| 9 | Technology detection | Netcraft extension, Wappalyzer extension |
| 10 | Domain registration | WHOIS lookup |
| 11 | Social media recon | LinkedIn (employee roles, org structure, tech stack clues) |

### Active Footprinting Techniques

**Warning:** all activity is logged; may affect target operations.

| # | Technique | Tool |
|---|---|---|
| 1 | Host discovery | `ping` (ICMP echo) |
| 2 | Route tracing | `traceroute` / `tracert` |
| 3 | DNS recon | `dnsrecon` (zone transfers, record enumeration) |
| 4 | Web crawling / URL extraction | Photon |
| 5 | Subdomain brute-force | Knockpy |
| 6 | Subdirectory brute-force | dirb, DirBuster, wfuzz |

**Subdomain vs subdirectory:** `sub.example.com` (subdomain) vs
`example.com/dir` (subdirectory) — different enumeration approaches.

### Countermeasures

- Restrict WHOIS data (privacy protection)
- Disable DNS zone transfers
- Limit information exposure on social media / job postings
- Use robots.txt and proper access controls to prevent crawling sensitive paths
- Monitor for data leaks (Google Dorks against own org)

### Tools summary

Passive: Google Dorks, Shodan, Netcraft, crt.sh, hunter.io, theHarvester,
Sublist3r, Wappalyzer, WHOIS. Active: ping, traceroute, dnsrecon, Photon,
Knockpy, dirb, DirBuster, wfuzz.
