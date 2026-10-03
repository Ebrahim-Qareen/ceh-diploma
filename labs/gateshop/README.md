# GateShop — intentionally vulnerable web application (CEH Diploma, ITGate Academy)

A realistic online-shop lab for teaching Session 8 ("Web Application Hacking & SQL Injection").
Every vulnerability lives in a believable feature, each has an **insecure ↔ secure** toggle, and the
exact vulnerable code can be shown on screen in class (or opened in your editor).

> In the spirit of DVWA / OWASP Juice Shop / WebGoat. **It is deliberately insecure — see Safety.**

## ⚠️ Safety / isolation — read first

- Run it **only** on an isolated VM (host-only or NAT network). **Never** expose it to the internet.
- **Snapshot the VM** before class so you can roll back.
- Command-injection, file-upload and SSRF labs are real code execution **inside the container** — keep the
  Docker network isolated and don't run it on a machine you care about.
- The instructor console at `/instructor` is **not password-protected** (by design, for class). That's
  another reason to keep this off any shared network.

## Run it (Docker — recommended)

```bash
cp .env.example .env          # then edit REMEMBER_KEY and the passwords
docker compose up -d --build  # builds the app + MySQL and starts everything
# open   http://<vm-ip>:8080
```

- The database is **created and seeded automatically** on first load (no manual SQL).
- **Instructor console:** `http://<vm-ip>:8080/instructor` — every lab, its goal, the vulnerable
  `file · function`, a **Show code** link, and a per-lab **security-level toggle** (insecure/secure),
  plus a **Reset** button.
- **Reset between classes:** click Reset in `/instructor`, or run `bash scripts/reset.sh`.
- To lock the app to the VM only (instructor demo, no student machines), change the port mapping in
  `docker-compose.yml` to `"127.0.0.1:8080:80"`.

## Run it without Docker (quick local dev)

Needs PHP 8 with `pdo_sqlite`:

```bash
DB_DRIVER=sqlite DB_SQLITE="$PWD/data/gateshop.sqlite" \
  php -S 0.0.0.0:8080 -t app/public devrouter.php
```

## Seeded accounts

| user | password | role |
|---|---|---|
| admin | admin123 | admin |
| instructor | teach123 | admin |
| carlos | carlos123 | user (the "victim") |
| wiener | peter | user |

## How a class runs

1. Open `/instructor`, pick a lab (it starts **insecure**).
2. Give students the **goal** shown on the lab page; they exploit it in the browser / Burp.
3. Click **Show vulnerable code** → the exact function appears, the bug highlighted, with its
   `file · function · line` so you can also open it in your editor and point at it.
4. Flip the lab to **secure** and show the same attack now fails — point at the `FIX:` code.

## What's inside

- `app/public/` — web root (front controller `index.php`, assets, uploads).
- `app/src/core/` — tiny framework: DB, helpers, views, the **code viewer**, the **lab registry**, the seeder.
- `app/src/handlers/` — one small file per feature; **every vulnerable line is tagged `// VULN:` and
  paired with a `// FIX:`** used at the secure level.
- `MANIFEST.md` — every lab → Session-8 page, URL, goal, `file:function:lines`, exploit, fix.
- `scripts/` — `reset.sh`, `gen_manifest.php`.

## Vulnerability coverage

23 labs, all live: SQLi (search + login bypass), OS command injection, XXE, SSTI, insecure
deserialization, IDOR, mass assignment, business logic, auth/username-enumeration, path traversal,
file upload, SSRF, information disclosure, reflected/stored/DOM XSS, CSRF, CORS, clickjacking,
host-header, open redirect, and a mock web-LLM prompt-injection lab.

Not yet included (need extra services — a **phase 2**): NoSQL injection (MongoDB), LDAP injection
(OpenLDAP), WebSocket CSWSH, web cache poisoning & HTTP request smuggling (caching/proxy tier),
JWT & OAuth, server-side prototype pollution, race conditions. Ask and I'll add them.
