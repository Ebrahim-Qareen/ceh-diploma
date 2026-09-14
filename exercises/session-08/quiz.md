# Session 8 — Quiz (answers at the bottom)

1. Why is client-side input validation never a security control?
2. Name the three tiers of a web app and the signature attack at each boundary.
3. Why is stored XSS more dangerous than reflected XSS?
4. What is the difference between authentication and authorization, and which does IDOR exploit?
5. Trace what `' OR '1'='1' -- ` does to `SELECT * FROM users WHERE user='INPUT' AND pass='INPUT'`.
6. Give the four-step UNION extraction recipe.
7. An injectable parameter shows no output but `' AND SLEEP(5)--` delays the reply. What type is it and how do you extract data?
8. Why must you learn manual SQLi before using sqlmap?
9. What is the primary, definitive fix for SQL injection, and why does it work?
10. Give one access-log signature each for enumeration, XSS, and SQLi.

---
## Answers
1. It only runs in the browser; an attacker edits the request in a proxy after the browser, so the server receives unvalidated input. The server only sees the HTTP you send.
2. Client (browser/JS → XSS), Server (PHP/OS → file upload, command injection, IDOR), Database (SQL → SQL injection).
3. It is stored and served to every visitor automatically, with no link/click, including admins — highest severity. Reflected needs the victim to click a crafted link.
4. Authentication = who you are; authorization = what you may access. IDOR exploits missing authorization (per-object ownership check) despite valid authentication.
5. The quote closes the username string; `OR '1'='1'` makes the condition always true; `-- ` comments out the AND pass check → returns the first user row → login without a password.
6. `' ORDER BY N --` to find column count → `' UNION SELECT 1,2,.. --` to find displayed columns → `UNION SELECT ... FROM information_schema` to map tables/columns → `UNION SELECT user,password FROM users` to dump.
7. Blind (time-based). Inject a conditional `SLEEP()` and infer each bit of the data from whether the response is delayed; automate with sqlmap.
8. So you understand and can verify what sqlmap does; the tool provides speed, the manual method provides the judgement to trust and tune it.
9. Parameterised queries / prepared statements — input is bound as data, never parsed as query logic, so an injected quote is treated as a literal value.
10. Enumeration = a 404 spike per source IP; XSS = `<script>`/`onerror`/`%3Cscript%3E` in a parameter; SQLi = `UNION SELECT`/`information_schema`/`SLEEP(`/quote-heavy input in a parameter.
