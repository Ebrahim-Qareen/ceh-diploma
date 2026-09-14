---
session: 8
title: Web Application Hacking & SQL Injection — Instructor Guide
---

# Session 8 — Instructor Guide

## The one message
**Every web vulnerability is data treated as code — so never trust input, and separate data from code.** If students can state that and place each attack at its tier boundary, the session worked.

## Structure
- First half: client + server tiers (Burp, enumeration, XSS, upload, cmd-injection, IDOR), ending in a shell via a web form.
- Second half: the database tier — SQLi from a one-line auth bypass through UNION and blind to sqlmap — then detection + report.
- The bridge/SOC-flip framing keeps students aware they are learning both sides.

## Where students struggle
- **Burp proxy setup.** The single biggest time-sink at the start. Pre-stage the browser proxy + Burp CA cert, or use Burp's built-in browser. Do not start attacks until everyone can intercept one request.
- **"Read the query" for SQLi (P15–P16).** Beginners memorise `' OR 1=1 --` without understanding it. Make them trace the query on paper (mini-lab) before typing the payload — comprehension here carries the whole second half.
- **Column count / UNION mechanics.** ORDER BY to find columns, matching column count in UNION — walk it slowly once; it feels like magic until they see it.
- **Blind SQLi patience.** Show the concept by hand (one SLEEP probe) then hand it to sqlmap. Do not make them extract a password bit-by-bit manually.
- **sqlmap before understanding.** Enforce the order: Lab C (manual) before Lab D (sqlmap). A student who runs sqlmap first learns nothing.

## Board-worthy anchors
- The three-tier diagram (client/server/DB) with each attack labelled at its boundary — draw it once, refer back every attack.
- "authn ≠ authz" for IDOR.
- The vulnerable-vs-parameterised query, side by side — the single most important slide for the fix.

## Lab notes
- **DVWA security levels** are the built-in difficulty ramp: Low (raw), Medium (weak filter — needs Burp), High (better filter). Use them to show why blocklists fail.
- **Lab B:** if a student's webshell won't execute, check the upload landed in a web-served path and PHP is enabled — most "failures" are the file stored outside webroot (which is, itself, the correct defence).
- **Lab E:** hold time for the report — it is the graded deliverable. The detection rule can be validated with `grep` over the access log if no SIEM is available.

## Assessment
- Formative: 6 MCQs (P27) + 16 mini-labs (one per concept, self-checked).
- Summative: the web-app finding report (Lab E) against `exercises/session-08/web_finding_report_template.md` — rubric in student_activity.md.
