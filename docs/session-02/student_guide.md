---
session: 2
title: Footprinting & Reconnaissance
doc: Student Guide
---

# Session 2 — Student Guide

Simplified notes for self-review after class. This matches the session page.

## 1. The one rule: passive vs active
- **Passive** = you never touch the target. You read what third parties already published (Google, Shodan, certificate logs, registries). The target **cannot detect it** and cannot log it. Legal against anyone.
- **Active** = a packet reaches the target. It ends up in someone's log with your source IP. **Legal only against a target that authorised you in writing.**
- Do passive recon *first and thoroughly*, so that when you finally go active you already know exactly where to aim.

## 2. The reconnaissance funnel
Each stage narrows the last:
1. **Everything public** (passive) — Google, GHDB, Shodan, Netcraft.
2. **Only what mentions them** (passive) — WHOIS/RDAP, crt.sh, hunter.io, theHarvester.
3. **Names that resolve** (passive) — `dig` at a public resolver, subfinder.
4. **Assets that answer** (active) — dnsrecon, zone transfer, traceroute, knockpy, gobuster.
5. **Output** — a **ranked target list** = Session 3's scan list.

## 3. Passive tools (never touch the target)
- **Google dorks:** `site:` `filetype:`/`ext:` `inurl:` `intitle:` `intext:` `"exact"` `-exclude` `OR`. You're searching for the *shape of a mistake* (a stray file, a self-naming login page, an open directory listing). `cache:` was **retired by Google in Sept 2024** — use the Wayback Machine.
- **GHDB** (`exploit-db.com/google-hacking-database`): a library of proven dorks by category. Always add `site:yourtarget` — never run an unscoped GHDB dork against strangers.
- **Shodan:** a search engine for *services/banners*, not pages. Its scanners hit the target; you read the database. **Read "Last Seen" first** — the data is a snapshot and may be stale. Free tier ≈ 50 queries/mo, limited filters.
- **Netcraft** (`sitereport.netcraft.com`): hosting history — can reveal the **origin IP behind a CDN/WAF**.
- **crt.sh** (certificate transparency): search `%.target.com`. Every TLS cert names its hosts in the SAN field, so this leaks subdomains — often before a host is even live. Usually the biggest chunk of your subdomain list, free.
- **WHOIS → RDAP:** who owns the domain. **ICANN replaced WHOIS with RDAP (JSON over HTTPS) on 28 Jan 2025** — learn both. After GDPR, read what survives redaction: creation/expiry dates, **name servers** (the pivot to DNS recon), status codes (registrar lock).
- **hunter.io / LinkedIn:** find the **email convention** (e.g. `first.last@`). One address + a public staff list = every employee's username. Read-only — never message anyone. Free tier = 50 credits/mo.
- **theHarvester:** automates all of the above — `theHarvester -d target -b crtsh,duckduckgo,rapiddns,hackertarget -l 200 -f out`. Name your sources; don't use `-b all`. Many sources need API keys.

## 4. Active tools (packets reach the target — authorised targets only)
- **DNS records:** `dig +short <TYPE> domain @1.1.1.1` (A, AAAA, MX, NS, SOA, TXT). Asking a **public resolver** is passive; asking the target's **authoritative server** is active. **TXT = supply-chain map** (SPF `include:` lines) and **phishing forecast** (DMARC `p=none` = unenforced).
- **Zone transfer (AXFR):** if a name server isn't restricted, it hands you the whole zone in one reply.
  - Find the authoritative server first: `dig +short NS domain`
  - `dig axfr @<authoritative-ns> domain`
  - **Fails if** you ask a recursive resolver (`@1.1.1.1` never serves AXFR), the server is correctly restricted (that's a finding), or your network blocks TCP/53.
- **traceroute / tcptraceroute / mtr:** map the path; read the **last few hops** (their provider, border device, where it goes dark).
- **Web crawling (Photon / katana):** maps a whole site — loud, hundreds of requests. Photon is unmaintained (2019); `katana` is the modern one.
- **Brute-force — two different things:**
  - **Subdomain** (`knockpy`, `ffuf` DNS mode) — guesses *names* left of the domain, asks a **DNS server** → misses = **NXDOMAIN**.
  - **Subdirectory** (`gobuster`, `ffuf`, `dirb`) — guesses *paths* right of the slash, asks a **web server** → misses = **404**. Read the codes: `200` readable, `301/302` redirect, **`403`/`401` exist-but-protected (often the most interesting)**, `404` nothing.

## 5. Tool state (2026) — always check the release date
| Tool | Job | State |
|---|---|---|
| knockpy | subdomain | v8, 2025 — current |
| subfinder / amass | subdomain | current |
| Sublist3r | subdomain | **dormant (2020)** — know for exam, don't rely on |
| gobuster / ffuf | directory | current |
| dirb | directory | unmaintained (~2014), still in Kali; the exam tool |
| DirBuster | directory | effectively dead |
| wfuzz | fuzzing | v3.1.1, 2026 — **alive** (rumour says dead; it isn't) |
| theHarvester | OSINT | v4.11, 2026 — current |
| Photon | crawler | 2019 — dormant; use katana |
| Wappalyzer | fingerprint | went closed-source/paywalled 2023; use `whatweb` (CLI) |

## 6. MITRE ATT&CK — Reconnaissance (TA0043)
- **T1593** Search Open Websites/Domains — dorks, LinkedIn
- **T1594** Search Victim-Owned Websites — robots.txt, crawling
- **T1596** Search Open Technical Databases — WHOIS/RDAP, crt.sh, Shodan, Netcraft
- **T1589** Gather Victim Identity Info — hunter.io, theHarvester
- **T1590** Gather Victim Network Info — dig, DNS, traceroute (`.002` = DNS/zone transfer)
- **T1595** Active Scanning — brute-force (`.003` = Wordlist Scanning)

## 7. SOC angle — what a defender can and can't see
- **Can't detect (most of it):** dorking, Shodan, crt.sh, WHOIS, hunter.io, theHarvester — they touch third parties. Defence = **publish less** + **monitor the same sources** (CT-log alerts, Shodan Monitor, dork yourself, alert on your own WHOIS changing).
- **Can detect (≈3 techniques):** **zone transfer** (AXFR in DNS logs from a non-secondary), **subdomain brute-force** (NXDOMAIN spike), **directory brute-force** (404 burst + tool User-Agent).

## 8. The deliverable
`recon_report.md` — nine sections built across the eight labs, ending in a **ranked target list** and an **executive summary**. Mark every claim **fact or hypothesis** (a Shodan banner is "reported, last seen <date>", not "confirmed"). This report is what you scan in Session 3.

## Key terms
- **Footprinting / reconnaissance** — gathering information about a target before attacking.
- **Passive / active recon** — without / with contact that the target could log.
- **Dork** — a search query using operators to find unintentionally-exposed data.
- **GHDB** — Google Hacking Database, a categorised catalogue of dorks.
- **Certificate transparency** — public append-only log of issued TLS certs; leaks subdomains via crt.sh.
- **RDAP** — Registration Data Access Protocol; the 2025 JSON-over-HTTPS successor to WHOIS.
- **Zone transfer (AXFR)** — copying an entire DNS zone; a finding when unrestricted.
- **SPF / DMARC** — mail-authentication TXT records; read as a supply-chain map and a phishing forecast.
- **Subdomain vs subdirectory** — left of the domain (DNS) vs right of the slash (web server).
- **Email convention** — the rule (e.g. `first.last@`) that generates every employee's username.
