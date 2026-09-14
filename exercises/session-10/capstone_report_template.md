# CEH Diploma — Defence-in-Depth Capstone Report

**Assessor:** ____________________  **Scope (authorised lab):** ____________  **Date:** ____________

*The culminating deliverable of the diploma. Assess across every layer; frame findings as a defence-in-depth chain; make it portfolio-grade.*

---
## 1. Executive summary
- Environment assessed: `<the lab, in one line>`
- Overall posture: `<one paragraph a manager can read — biggest risks, headline recommendation>`
- Top 3 recommendations (highest leverage): `<e.g. MFA; patching; least privilege>`

## 2. Attack narrative (the chain)
Tell the story of how an attacker moves through the environment, chaining ≥3 sessions' techniques:
- Recon/scan (S2-3) → `<what was exposed>`
- Access/exploit (S4-5) → `<foothold>`
- Privesc (S6) → `<escalation>`
- Lateral / web / network (S7-9) → `<spread / data>`
- Evasion / wireless / cloud (S10) → `<perimeter & modern-surface angle>`

## 3. Findings by layer
| # | Layer | Finding | Evidence | Severity |
|---|---|---|---|---|
| 1 | Application | `<e.g. SQLi on /x>` | `<request+result>` | Critical |
| 2 | Identity | `<e.g. no MFA; over-priv account>` | | High |
| 3 | Endpoint | `<e.g. unpatched MS17-010>` | | High |
| 4 | Network | `<e.g. ARP MITM possible; weak cookie flags>` | | High |
| 5 | Perimeter/Cloud | `<e.g. public bucket; evadable IDS>` | | High/Med |
| 6 | Crypto | `<e.g. TLS 1.0/RC4; weak WPA2 passphrase>` | | Medium |

## 4. Defence-in-depth analysis
For each key attack path, show **what failed and what held**:
- `<Attack path>` — failed: `<control that was missing>`; held: `<control that caught/limited it>`; would have stopped it: `<the layer that closes it>`.
- The point: no single control is enough; a control at any layer breaks the chain.

## 5. Prioritised remediation (leverage-ranked)
| # | Fix | Closes | Effort | Leverage |
|---|---|---|---|---|
| 1 | MFA | phishing, stolen tokens, some cred reuse | Low | very high |
| 2 | Patch management | S5 exploits, EternalBlue | Med | high |
| 3 | Least privilege | S6 escalation, lateral movement | Med | high |
| 4 | Parameterised queries + output encoding | S8 injection | Low | high |
| 5 | TLS + Secure/HttpOnly/SameSite | S9 sniffing/hijack/CSRF | Low | high |
| 6 | Config scanning (CSPM) + block-public-default | S10 cloud misconfig | Low | high |

## 6. Detections deployed (the SOC flip)
- `<rule/monitor per layer — e.g. Sysmon 10 LSASS; access-log SQLi; ARP anomaly; CSPM public-bucket; IDS full reassembly>`
- Each validated against the assessment's own attack traffic.

---
*Security is layers, and every attack is detectable if you know where to look. Only authorised scope assessed; all findings reproducible.*

**🎓 CEH Diploma — completed.**
