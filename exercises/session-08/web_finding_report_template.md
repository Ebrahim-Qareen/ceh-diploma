# Web Application Penetration Test — Finding Report

**Tester:** ____________________  **Target (scope):** ____________  **Date:** ____________

---
## Executive summary
- Scope tested: `<app / URL, authorised>`
- Findings: `<n>` total — `<c>` critical/high, `<m>` medium, `<l>` low
- Headline risk (one line): `<the worst thing an attacker could do>`

## Findings (one block per vulnerability, highest risk first)

### F-1 · <Title>
- **OWASP category:** `<e.g. A03:2021 Injection>`
- **Severity:** Critical / High / Medium / Low  (CVSS: `<score>` if used)
- **Affected:** `<endpoint + parameter>`
- **Evidence:** `<the request sent + the result — dumped row / popup / shell output; attach screenshot>`
- **Impact:** `<what an attacker gains — full DB read, RCE, account takeover, data exposure>`
- **Remediation:** `<the ONE primary fix — e.g. parameterised queries; output encoding + CSP; server-side upload allow-list; per-object authorization>`

### F-2 · <Title>
*(repeat)*

## Risk prioritisation
| # | Finding | OWASP | Severity | Fix effort |
|---|---|---|---|---|
| 1 | SQL injection | A03 | Critical | Low (parameterise) |
| 2 | File upload → RCE | A05/A03 | High | Medium |
| 3 | Stored XSS | A03 | High | Low (encode+CSP) |
| 4 | IDOR | A01 | High | Medium (authz) |
| 5 | Reflected XSS | A03 | Medium | Low |

## Blue-team follow-up (detection)
- Attached rule(s): `<Sigma/WAF/grep signature for the attacks found>`
- Validated against: `<the test traffic these attacks generated>`

---
*Only authorised scope tested. Every payload was logged; findings are reproducible from the evidence above.*
