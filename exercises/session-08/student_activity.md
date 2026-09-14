# Session 8 — Student Activity & Rubric

## Activity: full web-app assessment of DVWA
Assess DVWA end to end and produce the finding report — the same flow as a real web-app penetration test.

### Steps
1. **Recon** — proxy through Burp; enumerate directories/parameters (gobuster).
2. **Test each family** — XSS (reflected + stored), file upload → shell, command injection, IDOR, SQL injection. Prove each with a request + result.
3. **Extract** — dump the users table via manual SQLi (Lab C), verify with sqlmap (Lab D), take hashes to hashcat.
4. **Detect** — write one access-log/WAF rule (SQLi or XSS) and validate it against your own traffic.
5. **Report** — finding report: each vuln with evidence, OWASP category, severity, impact, remediation; prioritised.

## Rubric (100 pts)
| Criterion | Pts |
|---|---|
| Burp interception + enumeration demonstrated | 10 |
| XSS proven (reflected + stored) with filter bypass | 15 |
| File upload → shell (with a filter bypass) | 15 |
| SQL injection **by hand** (auth bypass + UNION dump) | 20 |
| sqlmap used and its output verified against the manual result | 10 |
| Detection rule written and validated against attack traffic | 10 |
| Finding report: all vulns, evidence, OWASP+severity, remediation, prioritised | 20 |

**Authorisation gate:** any testing shown against a target the student does not own/aren't authorised for scores 0 overall — scope discipline is non-negotiable.
