---
session: 8
title: Web Application Hacking & SQL Injection — Student Guide
---

# Session 8 — Student Guide

## What you will be able to do
Test a web application methodically: intercept every request, map the surface, find and prove XSS / upload / command injection / IDOR / SQL injection, then detect and report them.

## The one idea
**Every web vulnerability is data treated as code.** XSS at the browser, command injection at the OS, SQLi at the database, IDOR at access control. Wherever the app trusts input, there is an attack — and the fix is always "separate data from code."

## The method (any web target)
1. **Intercept** — proxy the browser through Burp; you can now edit any request.
2. **Enumerate** — find hidden directories, files, and parameters.
3. **Test each family** — XSS (`<script>`/`onerror`), IDOR (change the id), command injection (`; id`), SQLi (`' OR 1=1 --`), upload (`.php`).
4. **Extract / exploit** — UNION or blind for SQLi; webshell for upload.
5. **Detect + report** — every attack is an HTTP request; write the log rule and the finding.

## SQL injection cheat-path
- Auth bypass: `' OR '1'='1' -- `
- Column count: `' ORDER BY N -- ` (increase until error)
- Map DB: `' UNION SELECT table_name,NULL FROM information_schema.tables -- `
- Dump: `' UNION SELECT user,password FROM users -- `
- Blind: `' AND SLEEP(5) -- ` (delay = injectable) → then sqlmap

## Key distinctions
- **Client-side validation is not security** — the server only sees the HTTP you send.
- **Stored XSS > reflected** — fires for everyone, no click.
- **authn ≠ authz** — IDOR is a missing per-object ownership check.
- **In-band vs blind** — see the data (UNION) vs infer it (boolean/time).
- **Understand before you automate** — do SQLi by hand (Lab C) before sqlmap (Lab D).

## Deliverable
A **web-app finding report** (template in `exercises/session-08/`): each vulnerability with evidence, OWASP category, severity, impact, and the one fix — prioritised by risk — plus a detection rule for the blue team.

## The rule you never break
Only attack apps you own or are authorised to test. DVWA/Juice Shop/PortSwigger are legal because you host them; a live third-party site is a crime and is logged.
