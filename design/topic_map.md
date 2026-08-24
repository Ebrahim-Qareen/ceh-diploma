# Topic Map — CEH Diploma

Single sequencing document (see `ceh-topic-structure`). **Locked scope: 10
sessions × 4 hours = 40 hours.** One row per topic. Re-split 2026-08-22 after
instructor re-review (see DECISIONS.md) — the previous session-level draft
overloaded Sessions 9 and 10 and gave Session 1 no attacker hands-on.
Rebalanced 2026-08-23 — Session 3 was overloaded (13 topics, 11 hands-on, in
4h); Vulnerability Analysis moved to Session 4 and Session 10's weakest-depth
topics trimmed (see DECISIONS.md).

**Still open, not yet actioned in this map** (flagged for instructor
decision):
- No AD (Active Directory) lab exists yet, but Session 4 (NTLM/Kerberos,
  LLMNR poisoning) and Session 6 (Windows privesc — Mimikatz, token abuse)
  teach AD-style attacks against standalone Windows targets only. Recommend
  adding one domain controller + domain-joined workstation to
  `labs/lab_design.md` before Session 4 is built, or explicitly scoping those
  topics to local (non-domain) Windows auth. See `scope_decisions.md` §Open.
- Official EC-Council module PDFs for Ch.11, 12, 17, 18, 19 are still not in
  `Resources/EC-Council Materials/` — those sessions' content (Session
  Hijacking, Evasion, Mobile, IoT/OT, Cloud) was built from verified public
  syllabus/web research, not the source deck. Recommend sourcing the official
  PDFs before finalizing Session 9-10 depth.
- No continuity target across Sessions 1-6 — each session currently uses a
  fresh, unrelated lab target. Running one persistent target through Recon
  (S2) → Scan/Enumerate (S3) → Vuln Analysis/Creds (S4) → Exploit (S5) →
  Privesc (S6) would reinforce the kill-chain framing taught in Session 1.
  **Partly actioned (2026-08-24):** Session 2 adopts `tryhackme.com` as a
  single carry-through target for all *passive* recon (legal against any
  public domain), producing a ranked recon report that is explicitly framed
  as Session 3's scan-list input. Active recon in S2 still uses authorised
  stand-ins (`zonetransfer.me`, `scanme.nmap.org`, the local `ceh-lab.local`
  zone) because you cannot lawfully send packets at `tryhackme.com`. A single
  continuity target that can be *attacked* end to end (S3→S6) still needs an
  instructor-owned domain or a dedicated lab company — unchanged open item.

- Currency corrections surfaced while building Session 2 (do not change
  sequencing, but the instructor deck / older courseware is wrong on them):
  WHOIS→RDAP for gTLDs (ICANN, 28 Jan 2025); Google `cache:` operator retired
  (Sep 2024); recon tool rot (Sublist3r, Photon dormant; knockpy/ffuf/wfuzz
  current). Captured on the Session 2 page and in its student guide.

Audience baseline: students arrive with **MCSA + Linux + CCNA**. No topic here
re-teaches networking, TCP/IP, Windows admin, or Linux basics — those are
assumed and only referenced as attacker leverage.

## Session titles

| # | Session | CEH chapters |
|---|---|---|
| 1 | Foundations, Lab Build & First Contact | 1, 2 (partial) |
| 2 | Footprinting & Reconnaissance | 2 |
| 3 | Scanning & Enumeration | 3, 4 |
| 4 | System Hacking I — Vulnerability Analysis, Authentication & Password Attacks | 5, 6 (pt1) |
| 5 | System Hacking II — Exploitation, Shells & Payloads | 6 (pt2) |
| 6 | System Hacking III — Privilege Escalation & CTF Capstone | 6 (pt3+pt4) |
| 7 | Malware Threats & Analysis | 7 |
| 8 | Web Application Hacking & SQL Injection | 13, 14, 15 |
| 9 | Sniffing, MITM, Session Hijacking, Social Engineering & DoS | 8, 9, 10, 11 |
| 10 | Evasion, Wireless & Emerging-Tech Sweep | 12, 16, 17, 18, 19, 20 |

## Topic rows

| Topic | Source | Prerequisite topics | Session # | Hands-on? |
|---|---|---|---|---|
| Information security concepts (CIA+AA) | Module 1 | — | 1 | No (discussion) |
| Attack = motive + method + vulnerability | Module 1 | InfoSec concepts | 1 | No (discussion) |
| Attack classification (passive/active/close-in/insider/distribution) | Module 1 | InfoSec concepts | 1 | No (discussion) |
| Hacker classes & ethical hacking scope | Module 1 | — | 1 | No (discussion) |
| Authorization, rules of engagement, legal boundaries | Module 1 | Ethical hacking scope | 1 | Yes (scope-doc exercise) |
| 5-phase hacking methodology | Module 1 | Hacker classes | 1 | Yes (mapping exercise) |
| Cyber Kill Chain / MITRE ATT&CK / Diamond Model | Module 1 | 5-phase methodology | 1 | Yes (mapping exercise) |
| Lab topology & host-only networking | Module 2 pt1, labs/lab_design.md | — | 1 | Yes (build) |
| Kali attacker box build & verification | Module 2 pt1 | Lab topology | 1 | Yes (build) |
| Metasploitable2 target build & verification | Module 2 pt1 | Lab topology | 1 | Yes (build) |
| Windows targets (Win10 / WinSrv2019) build | Module 2 pt1 | Lab topology | 1 | Yes (homework build) |
| Snapshot discipline (baseline/revert) | labs/lab_design.md | VM builds | 1 | Yes |
| Passive vs active footprinting (concept) | Module 2 pt2 | 5-phase methodology | 1 | No (theory chunk) |
| First contact: host discovery + banner grabbing | Module 2 pt2, Module 3 | Lab build, passive/active concept | 1 | Yes |
| Lab report format & evidence standards | design/scope_decisions.md §8 | — | 1 | Yes (write one) |
| Search-engine recon & Google dorks / GHDB | Module 2 pt2 | Passive footprinting concept | 2 | Yes |
| Shodan / Netcraft / crt.sh / hunter.io | Module 2 pt2 | Passive footprinting concept | 2 | Yes |
| WHOIS & domain registration recon | Module 2 pt2 | Passive footprinting concept | 2 | Yes |
| theHarvester / Sublist3r / Wappalyzer | Module 2 pt2 | Passive footprinting concept | 2 | Yes |
| Social-media & people recon (LinkedIn) | Module 2 pt2 | Passive footprinting concept | 2 | Yes |
| DNS recon & zone transfers (dnsrecon) | Module 2 pt2 | Active footprinting concept | 2 | Yes |
| Route tracing & web crawling (Photon) | Module 2 pt2 | Active footprinting concept | 2 | Yes |
| Subdomain vs subdirectory brute-force (Knockpy, dirb, wfuzz) | Module 2 pt2 | DNS recon | 2 | Yes |
| Footprinting countermeasures | Module 2 pt2 | All recon techniques | 2 | No |
| Host discovery techniques | Module 3 | First contact (S1) | 3 | Yes |
| TCP flags & scan types (SYN, connect, FIN, XMAS, NULL, ACK) | Module 3 | Host discovery | 3 | Yes |
| UDP scanning | Module 3 | TCP scan types | 3 | Yes |
| Nmap usage patterns & timing | Module 3 | TCP/UDP scanning | 3 | Yes |
| OS & service/version discovery | Module 3 | Nmap usage | 3 | Yes |
| Scanning countermeasures | Module 3 | Scan types | 3 | No |
| Enumeration concepts | Module 4 | Service discovery | 3 | No |
| Service-specific enumeration (SMB, SNMP, SMTP, LDAP, NFS, FTP) | Module 4 | Enumeration concepts | 3 | Yes |
| NSE scripts & directory enumeration | Module 4 | Nmap usage | 3 | Yes |
| Manual enumeration (netcat, banner analysis) | Module 4 | Enumeration concepts | 3 | Yes |
| Vulnerability concepts & research sources | Module 5 | Enumeration (S3) | 4 | Yes |
| CVE / CVSS scoring & exploit searching (searchsploit) | Module 5 | Vulnerability concepts | 4 | Yes |
| Automated vulnerability scanning (Nessus/OpenVAS) | Module 5 | Vulnerability concepts | 4 | Yes |
| Authentication concepts & hash algorithms | Module 6 pt1 | — | 4 | No |
| Windows authentication (NTLM, Kerberos) | Module 6 pt1 | Auth concepts | 4 | Yes |
| Password cracking (hashcat, John, hydra) | Module 6 pt1 | Hash algorithms | 4 | Yes |
| LLMNR/NBT-NS poisoning (Responder) | Module 6 pt1 | Windows authentication | 4 | Yes |
| Shell types (bind vs reverse) | Module 6 pt1 | — | 4 | Yes |
| Introduction to exploitation & Metasploit | Module 6 pt1 | Vulnerability research | 4 | Yes |
| Manual exploitation workflow | Module 6 pt2 | Metasploit intro | 5 | Yes |
| Payload generation with msfvenom | Module 6 pt2 | Shell types | 5 | Yes |
| Buffer overflow & RCE | Module 6 pt2 | Manual exploitation | 5 | Yes |
| Linux privilege escalation (linpeas, SUID, GTFOBins, cron) | Module 6 pt3 | Gaining access (S5) | 6 | Yes |
| Windows privilege escalation (winPEAS, Mimikatz, token abuse) | Module 6 pt3 | Gaining access (S5) | 6 | Yes |
| Steganography | Module 6 pt3 | — | 6 | Yes |
| CTF capstone machines (Blue, Academy, DoubleTrouble, Blackpearl) | Module 6 pt4 | Full S3-S6 chain | 6 | Yes |
| Malware types & classification | Module 7 | — | 7 | No |
| Static malware analysis (strings, VirusTotal, hybrid-analysis) | Module 7 | Malware types | 7 | Yes |
| Dynamic malware analysis (procmon, tcpview, sandbox) | Module 7 | Static analysis | 7 | Yes |
| Trojan/backdoor creation & detection | Module 7 | msfvenom (S5) | 7 | Yes |
| Malware countermeasures & SOC detection angle | Module 7 | Static + dynamic analysis | 7 | No |
| Web technology fundamentals & HTTP/Burp | Module 8 pt1 | Enumeration (S3) | 8 | Yes |
| Web enumeration (dirb/gobuster, robots.txt) | Module 8 pt2 | HTTP/Burp | 8 | Yes |
| XSS (reflected, stored, DOM) | Module 8 pt1 | Web fundamentals | 8 | Yes |
| File upload vulnerabilities | Module 8 pt2 | Web enumeration | 8 | Yes |
| Command injection | Module 8 pt2 | Web fundamentals | 8 | Yes |
| IDOR | Module 8 pt2 | HTTP/Burp | 8 | Yes |
| SQL fundamentals & SQL injection types (error/union/blind) | Module 8 pt2 | Web fundamentals | 8 | Yes |
| SQLi exploitation flow (DVWA) & automated SQLi (sqlmap) | Module 8 pt2 | SQL injection types | 8 | Yes |
| Web attack countermeasures & SOC detection angle | Module 8 pt1+pt2 | All web attacks | 8 | No |
| Sniffing concepts & techniques (ARP/MAC/DHCP/DNS) | Module 9 (Ch.8) | Scanning (S3) | 9 | Yes |
| Man-in-the-middle & interception (Wireshark, ettercap) | Module 9 (Ch.8) | Sniffing concepts | 9 | Yes |
| Session hijacking — application-level (token/cookie theft) | Module 11 (Ch.11) | Sniffing, HTTP/Burp (S8) | 9 | Yes |
| Session hijacking — network-level (TCP/IP) | Module 11 (Ch.11) | MITM | 9 | Yes |
| Social engineering (phishing, setoolkit, pretexting) | Module 9 (Ch.9) | — | 9 | Yes |
| DoS / DDoS attacks & botnets | Module 9 (Ch.10) | Sniffing concepts | 9 | Partial (concept + limited demo) |
| IDS / IPS concepts & evasion techniques | Module 12 (Ch.12) | Scanning evasion (S3) | 10 | Yes |
| Firewall & honeypot evasion / detection | Module 12 (Ch.12) | IDS evasion | 10 | Yes |
| Wireless security & attacks (WEP/WPA, aircrack-ng suite) | Module 9 (Ch.16) | Sniffing concepts (S9) | 10 | Yes |
| Mobile platform attacks (Android/iOS, OWASP Mobile Top 10) | Module 17 (Ch.17) | — | 10 | No (overview only) |
| IoT & OT hacking | Module 18 (Ch.18) | — | 10 | No (overview only) |
| Cloud computing attacks & shared-responsibility model | Module 19 (Ch.19) | — | 10 | Partial |
| Cryptography (symmetric/asymmetric/hashing, PKI, cryptanalysis) | Module 10 (Ch.20) | — | 10 | No (pre-reading/homework, not live lecture time) |

## Notes

- **Session count locked at 10 × 4h.** Session titles table above is the
  session-level view; topic rows are the authoritative sequencing.
- Session 1 gives every student real attacker hands-on the same day the lab is
  built: authorization/scope-doc exercise, ATT&CK/kill-chain mapping, VM
  builds + snapshot discipline, and a **first-contact host discovery + banner
  grab against the freshly-built Metasploitable2** — no target-less OSINT and
  **no AD domain** required for Session 1.
- OSINT/passive+active footprinting techniques stay in Session 2 (Session 1
  teaches only the passive-vs-active *concept* so first-contact makes sense).
- Cryptography stays concept-only (no lab in the source material either) and
  is assigned as pre-reading/homework, not live Session 10 lecture time — it
  was the lowest-value use of live minutes in an already 6-chapter session.
- Session 9 topic order (Sniffing → MITM → Session Hijacking → Social
  Engineering → DoS) already runs hijacking immediately after MITM, ahead of
  social engineering — verified correct, no change needed.
- Mobile and IoT/OT (Session 10) scoped down to overview-only (no hands-on)
  to protect time for Evasion and Wireless, the two Session 10 topics with
  real hands-on labs.
- Prerequisite check passed: no topic depends on a topic assigned to a later
  session.
