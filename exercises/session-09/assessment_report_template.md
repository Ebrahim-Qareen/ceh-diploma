# Network & Human Assessment Report

**Assessor:** ____________________  **Scope (authorised):** ____________  **Date:** ____________

---
## Executive summary
- Surfaces assessed: network, session, human, availability
- Headline risk (one line): `<the worst realistic outcome>`
- Top recommendation: `<the single highest-leverage control — usually MFA + TLS/cookie flags>`

## 1. Network (sniffing / MITM)
- **Finding:** `<e.g. ARP poisoning possible (no DAI); HTTP credentials sniffable>`
- **Evidence:** `<the capture / ARP-table change>`
- **Fix:** `<TLS everywhere + HSTS; Dynamic ARP Inspection; port security; VPN on untrusted nets>`

## 2. Session (hijacking / CSRF)
- **Finding:** `<e.g. cookie lacks HttpOnly/Secure; no expiry; no anti-CSRF token>`
- **Evidence:** `<replayed token → takeover; CSRF PoC fired>`
- **Fix:** `<Secure+HttpOnly+SameSite; strong random IDs; regenerate on login; short expiry; anti-CSRF tokens>`

## 3. Human (social engineering / phishing)
- **Finding:** `<e.g. staff clicked the lab phish; no MFA; no reporting path>`
- **Evidence:** `<harvested test credential; lever(s) used>`
- **Fix:** `<MFA; awareness training on the levers; DMARC/SPF/DKIM; reporting button; verify via 2nd channel>`

## 4. Availability (DoS / DDoS)
- **Finding:** `<e.g. SYN flood succeeded (no syncookies); Slowloris tied up workers>`
- **Evidence:** `<SYN_RECV count; workers busy at low rate>`
- **Fix:** `<SYN cookies + rate limit; reverse-proxy timeouts; upstream scrubbing/CDN; redundancy>`

## Prioritised remediation
| # | Surface | Finding | Fix | Leverage |
|---|---|---|---|---|
| 1 | Session/Human | no MFA | enforce MFA | very high (kills phished pw + limits token value) |
| 2 | Network/Session | no TLS / weak cookie flags | TLS + Secure/HttpOnly/SameSite | high |
| 3 | Network | no DAI | Dynamic ARP Inspection / port security | medium |
| 4 | Availability | no SYN cookies | enable + rate-limit / scrubbing | medium |

## Detections (attached)
- ARP-anomaly monitor · session-token-from-two-IPs correlation · SYN-flood threshold — validated against the test traffic.

---
*Only authorised scope assessed. All attacks were contained to the lab; evidence is reproducible.*
