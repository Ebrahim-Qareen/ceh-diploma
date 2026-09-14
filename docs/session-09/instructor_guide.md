---
session: 9
title: Sniffing/MITM/Hijacking/Social Eng/DoS — Instructor Guide
---

# Session 9 — Instructor Guide

## The one message
**The app doesn't live alone — the wire, the session, the human, and uptime are each an attack surface with a signature and a fix.** If students leave able to name all four and their defences, the session worked.

## Structure & the ethics gate
- First half: machine layers (sniffing, ARP MITM, SSL strip, session hijacking, CSRF, TCP hijack).
- Second half: the human (social engineering, phishing) and availability (DoS).
- **The phishing lab (C) and DoS lab (D) are ethics-gated.** State the legal line out loud before each: isolated lab, consenting test accounts, never a real person/brand/network. Model the authorisation conversation.

## Where students struggle
- **ARP/MITM setup.** Two VMs + IP forwarding is fiddly. Pre-stage the topology; have `saved/session9_mitm.pcap` ready so nobody is blocked from the credential-reading exercise.
- **"Why doesn't MFA stop a stolen session?"** (P6/Lab B). The key insight of the session-hijacking block: authentication already happened; the token inherits it. Hammer this — it's the most common misconception.
- **Cookie flags mapping.** Keep the Secure/HttpOnly/SameSite → attack mapping explicit; students conflate them. HttpOnly stops XSS theft; Secure stops sniffing; SameSite stops CSRF.
- **Social engineering as "just common sense."** Push past that — make them name the psychological lever (authority/urgency/etc.). The lever is why smart people click; naming it is the training.
- **DoS class → fix.** Students want one fix for all DoS. Force the mapping: volumetric→upstream, protocol→SYN cookies, app-layer→proxy timeouts.

## Board-worthy anchors
- The four-surface diagram (wire/session/human/uptime) — draw once, return every block.
- "A session token is a bearer credential" — the sentence that explains hijacking + why MFA-on-login fails.
- The Secure/HttpOnly/SameSite → sniff/XSS/CSRF mapping.

## Lab notes
- **Lab A:** always stop the ARP spoof cleanly (`arp.spoof off`) or the lab network stays broken for the next exercise.
- **Lab C (phishing):** clone a *lab* login page, never a real brand; the credential captured is one the student types. The lesson is how trivial the tech is → how much rides on MFA + awareness.
- **Lab D (DoS):** short bursts only, throwaway lab web VM; the point is watching the resource deplete and the mitigation restore it, not the takedown.
- **Lab E:** hold time for the report — it's the graded deliverable spanning all four surfaces.

## Assessment
- Formative: 6 MCQs (P25) + 14 mini-labs.
- Summative: the four-surface assessment report (Lab E) against `exercises/session-09/assessment_report_template.md` — rubric in student_activity.md.
