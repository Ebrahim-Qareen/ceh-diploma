# Session 9 — Student Activity & Rubric

## Activity: four-surface assessment of the lab environment
Assess the wire, the session, the human, and availability — then produce the consolidated report.

### Steps
1. **Wire** — ARP-poison MITM (Lab A); capture a cleartext credential; note whether TLS/DAI would stop it.
2. **Session** — steal & replay a token (Lab B); build a CSRF PoC; check the cookie flags (Secure/HttpOnly/SameSite).
3. **Human** — run the SET harvester on a lab account (Lab C, ethics-gated); list the phishing indicators and controls.
4. **Availability** — SYN flood + Slowloris (Lab D); apply the class-specific mitigation; confirm recovery.
5. **Detect + report** — write detections for each surface; validate against your own traffic; write the assessment report.

## Rubric (100 pts)
| Criterion | Pts |
|---|---|
| ARP-poison MITM performed + cleartext credential captured | 15 |
| Session token stolen & replayed (account takeover shown) + why MFA-on-login fails explained | 15 |
| CSRF PoC + correct cookie-flag mapping (Secure/HttpOnly/SameSite) | 10 |
| SET phishing lab run **within the ethics gate** (consenting/lab only) + indicators listed | 15 |
| DoS: SYN flood + Slowloris with the **class-matched** mitigation and recovery | 15 |
| Detections written and validated against own traffic (≥2 surfaces) | 10 |
| Assessment report: four surfaces, evidence, prioritised fixes | 20 |

**Ethics gate:** any attack shown against a non-lab / non-consenting target scores 0 overall — authorisation is non-negotiable.
