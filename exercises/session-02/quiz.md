---
session: 2
title: Footprinting & Reconnaissance
doc: Quiz (10 questions)
---

# Session 2 — Quiz

Each question maps to a Session 2 learning objective (LO1–LO10 from the Session Plan).
These test the **methods**, not command memorisation.

## Questions

**Q1 (LO1, MCQ).** Which action is **passive** reconnaissance?
- A. Running `nmap -sV` against the target's web server
- B. Requesting `/robots.txt` directly from the target
- C. Querying `crt.sh` for the target's certificates
- D. Sending an AXFR request to the target's name server

**Q2 (LO5, MCQ).** As of 2025, what officially replaced WHOIS for generic TLDs?
- A. DNSSEC
- B. RDAP — the Registration Data Access Protocol
- C. A new WHOIS v2 protocol
- D. Certificate Transparency logs

**Q3 (LO4, MCQ).** Why does searching `crt.sh` reveal subdomains a normal DNS lookup never would?
- A. crt.sh brute-forces the target's DNS server
- B. It reads the target's zone file directly
- C. Every issued TLS certificate is logged publicly, and its SAN field names the hosts it covers
- D. It intercepts the target's HTTPS traffic

**Q4 (LO7, MCQ).** `dig axfr @1.1.1.1 zonetransfer.me` fails. The most likely reason:
- A. Zone transfers are always blocked everywhere now
- B. `1.1.1.1` is a recursive resolver, not authoritative for the zone
- C. You need to run it as root
- D. The domain does not exist

**Q5 (LO4, short).** Reading a host on Shodan is passive. Explain *why*, and name the one field you should read **first** and why.

**Q6 (LO6, MCQ).** Why is a single confirmed email address such a valuable recon finding?
- A. It gives you that person's password
- B. It reveals the naming convention, which generates every employee's username
- C. It lets you read that person's email
- D. It confirms the mail server is vulnerable

**Q7 (LO8, MCQ).** The difference between subdomain and subdirectory brute-force is that…
- A. One is passive, the other is active
- B. One is legal, the other is not
- C. They use the same wordlists interchangeably
- D. One interrogates a DNS server, the other interrogates a web server

**Q8 (LO2, MCQ).** Which recon tool is effectively **dormant** and should be known for the exam but replaced in practice?
- A. knockpy
- B. theHarvester
- C. Sublist3r
- D. ffuf

**Q9 (LO8, MCQ).** During directory brute-force, why is a `403` often more interesting than a `200`?
- A. 403 means the server has crashed
- B. 403 means the path exists but is deliberately protected — they're hiding something there
- C. 403 means the file was deleted
- D. 403 pages always contain credentials

**Q10 (LO10, short + scenario).** You find an **open zone transfer** during an authorised test. (a) Name the MITRE ATT&CK sub-technique. (b) Name one thing the dump might contain that a subdomain *scan* never would. (c) Name one log source that would have caught your AXFR request.

## Answer key

1. **C** — crt.sh queries a third-party certificate log; nothing reaches the target. (A, B, D all send packets to the target.) (LO1)
2. **B** — ICANN sunsetted WHOIS for gTLDs on 28 Jan 2025 in favour of RDAP (JSON over HTTPS). `whois` still works via failover but RDAP is authoritative. (LO5)
3. **C** — Certificate Transparency is a public, append-only log of issued certs; the SAN field names every host the cert covers, so internal-sounding names become public — often before the host is live. (LO4)
4. **B** — A recursive resolver never serves a zone transfer. You must send AXFR to a server authoritative for the zone; get it from the NS records first. (LO7)
5. **Passive because** Shodan's own scanners contacted the target and stored the banner — you are only querying Shodan's database, so no packet of yours reaches the target. **Read "Last Seen" first**, because the data is a point-in-time snapshot; a host may have been patched, firewalled or reassigned since the crawl, so an old date makes any "finding" a hypothesis, not a fact. (LO4)
6. **B** — One address reveals the convention (e.g. `first.last`); combined with a public staff list it generates every employee's username — the input to password spraying in Session 4 — with no packets sent. (LO6)
7. **D** — Subdomain brute-force queries a **DNS server** (names left of the domain; misses = NXDOMAIN); subdirectory brute-force queries a **web server** (paths right of the slash; misses = 404). Different namespace, tool, protocol and log. Both are active. (LO8)
8. **C** — Sublist3r's last release was v1.1 in 2020 (Python-2 era, several dead sources). knockpy (v8, 2025), subfinder, ffuf and wfuzz (v3.1.1, 2026) are current. Standing lesson: check the release date. (LO2)
9. **B** — `403 Forbidden` means the path exists but access is denied — they know it's sensitive. `404` means nothing is there. The 403/401 paths are the ones to carry into Session 8. (LO8)
10. (a) **T1590.002** (Gather Victim Network Information: DNS). (b) e.g. **TXT records with pasted secrets, HINFO records naming the OS, or internal hostnames with no certificate/web presence** — none of which a certificate-log or brute-force approach surfaces. (c) **BIND query log**, **Windows DNS Analytical log**, or **Zeek `dns.log`** showing an `AXFR` from a source that is not a listed secondary. (LO10)
