---
session: 8
title: Web Application Hacking & SQL Injection
duration_min: 240
---

# Session 8 — Session Plan

## Title
Web Application Hacking & SQL Injection (CEH Chapters 13–15)

## Module reference
- Web technology fundamentals (client/server/DB tiers), HTTP, Burp Suite
- Web enumeration (gobuster/ffuf/ParamSpider)
- The OWASP Top 10 attack surface
- XSS (reflected, stored, DOM), file upload to shell, command injection, IDOR
- SQL injection: fundamentals, auth bypass, in-band/UNION, blind (boolean + time), sqlmap
- Access-log/WAF detection, countermeasures, the web-app finding report

## Learning objectives
By the end a student can:
1. Explain the three-tier web stack and locate each attack at its boundary (data-vs-code).
2. Intercept, modify, and replay any request with **Burp Suite**; explain why client-side validation is not security.
3. Enumerate hidden web content and parameters.
4. Find and prove **XSS** (reflected + stored), **file upload → shell**, **command injection**, and **IDOR**.
5. Perform **SQL injection** manually: auth bypass, UNION extraction, and blind (boolean + time-based).
6. Automate with **sqlmap** and critically verify its output.
7. Write **access-log/WAF detection rules** for the attacks and a prioritised **web-app finding report**.

## Time distribution (target 240 min)
| Block | Min | Format |
|---|---|---|
| Bridge from S7 (payload → front door) | 4 | theory |
| Why web security | 5 | theory |
| The web stack (+ mini-lab) | 7 | theory |
| HTTP & Burp (+ mini-lab) | 7 | tool |
| Web enumeration (+ mini-lab) | 7 | tool |
| The web attack surface / OWASP (+ mini-lab) | 6 | theory |
| XSS types (+ mini-lab) | 7 | theory |
| Stored XSS & bypass (+ mini-lab) | 7 | attack |
| File upload → shell (+ mini-lab) | 7 | attack |
| Command injection (+ mini-lab) | 7 | attack |
| IDOR (+ mini-lab) | 6 | attack |
| Lab A — XSS on DVWA | 16 | hands-on |
| Lab B — upload webshell → shell | 16 | hands-on |
| **Break** | 10 | — |
| SQL fundamentals (+ mini-lab) | 7 | theory |
| SQLi auth bypass (+ mini-lab) | 7 | attack |
| SQLi types (+ mini-lab) | 6 | theory |
| UNION extraction (+ mini-lab) | 7 | attack |
| Blind SQLi (+ mini-lab) | 7 | attack |
| sqlmap (+ mini-lab) | 7 | tool |
| Lab C — manual SQLi on DVWA | 18 | hands-on |
| Lab D — sqlmap + verify | 14 | hands-on |
| The web-attack SOC flip | 6 | defender |
| Lab E — detect + finding report | 20 | hands-on |
| Countermeasures (+ mini-lab) | 6 | defender |
| Where next / practice range | 5 | resources |
| Knowledge check (6 MCQs) | 10 | assess |
| Takeaways | 4 | summary |

## Materials
- Kali (Burp, gobuster/ffuf, sqlmap, webshells) + **DVWA** (all four security levels) as the primary target
- Optional: OWASP Juice Shop, bWAPP (IDOR), PortSwigger Web Security Academy (free, online)
- `scripts/lab_s8_setup.sh` stands up DVWA (Docker) + optional Juice Shop on the lab network
- Fallbacks under `saved/`: a sample access.log with attack traffic (for the Lab E detection), and screenshots of each attack succeeding

## Safety note
Every payload here is illegal against a site you do not own. DVWA/Juice Shop are self-hosted; delete any uploaded webshell at session end; unauthorised web testing is a crime and is logged.
