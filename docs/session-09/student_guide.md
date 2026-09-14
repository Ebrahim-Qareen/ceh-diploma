---
session: 9
title: Sniffing/MITM/Hijacking/Social Eng/DoS — Student Guide
---

# Session 9 — Student Guide

## What you will be able to do
Attack (and defend) the four things around an application: the network path, the session token, the human, and availability.

## The four surfaces
1. **Wire** — sniff traffic; become the MITM with ARP poisoning; strip HTTPS (defeated by HSTS).
2. **Session** — steal and replay a token (account takeover, no password); CSRF; TCP-level hijacking.
3. **Human** — social engineering (authority/urgency/trust/fear/reciprocity); phishing with SET.
4. **Availability** — DoS/DDoS: volumetric / protocol (SYN flood) / app-layer (Slowloris).

## Key insights
- **A session token is a bearer credential** — hold it, be the user. Login-time MFA is already behind a stolen active session.
- **Every token-theft method has a cookie-flag fix:** sniff→Secure+TLS, XSS→HttpOnly, fixation→regenerate on login, replay→expiry, CSRF→SameSite + anti-CSRF token.
- **The domain always betrays a phish** — the page can be perfect, the URL cannot.
- **DoS class picks the fix:** volumetric→upstream scrubbing, protocol→SYN cookies, app-layer→proxy timeouts.

## Detections (the SOC flip)
- MITM → ARP anomaly (gateway MAC changed).
- Hijack → one session token from two IPs / impossible-travel.
- Phishing → young look-alike domain + a user report.
- DoS → traffic/state spike (Gbps, SYN_RECV pile-up, all workers busy).

## Deliverable
A **four-surface assessment report** (template in `exercises/session-09/`): network, session, human, availability — findings, evidence, prioritised fixes, with your detection rules attached.

## The rules you never break
MITM, phishing, and DoS against anything you don't own are serious crimes. Isolated lab, consenting test accounts, or explicit written authorisation — always.
