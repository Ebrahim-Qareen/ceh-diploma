# Session 8 — Homework

## Core (everyone)
1. **Own DVWA end to end.** On your own DVWA, prove all five families (XSS reflected+stored, file upload→shell, command injection, IDOR, SQLi) at Low, and at least SQLi + upload at Medium (Burp needed). Capture a request+result screenshot for each.
2. **Manual then automated SQLi.** Dump the users table by hand (UNION), then reproduce with sqlmap and confirm they match. Crack the hashes with hashcat (rockyou).
3. **Write one detection.** A Sigma or grep rule for SQLi or XSS in the access log; validate it against your own attack traffic.

## Stretch
4. Complete the TryHackMe **SQL Injection** room (verified free) or three PortSwigger Web Security Academy SQLi labs.
5. Try **OWASP Juice Shop** — solve the SQLi login bypass and one XSS challenge; note how a modern JS app differs from DVWA.

## Submit
- The finding report (all vulns, evidence, OWASP+severity, remediation, prioritised)
- Your detection rule + proof it fired
- (stretch) room/lab completion notes

**Reminder:** self-hosted or explicitly-authorised targets only. Unauthorised web testing is a crime and every request is logged.
