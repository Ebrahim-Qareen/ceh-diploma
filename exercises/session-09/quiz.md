# Session 9 — Quiz (answers at the bottom)

1. Why does sniffing on a switched network require ARP poisoning, but a hub/open Wi-Fi does not?
2. How does ARP poisoning make you the man in the middle, and what detects it?
3. What does SSL strip actually attack, and which header defeats it?
4. Why doesn't login-time MFA stop an attacker who replays a stolen session token?
5. Map each cookie flag (Secure, HttpOnly, SameSite) to the attack it stops.
6. Why does CSRF succeed without the attacker ever stealing the cookie?
7. Name the five psychological levers of social engineering.
8. What is the single most reliable tell of a phishing page, and the top technical control?
9. Classify DoS into three types and give the matching mitigation for each.
10. Give one detection signature for MITM, session hijacking, and DoS.

---
## Answers
1. A switch delivers frames only to the destination port, so you must actively redirect the victim's traffic to yourself (ARP poisoning). A hub/open Wi-Fi is a shared medium — passive listening works.
2. Send forged ARP replies so the victim caches your MAC as the gateway (and the gateway caches your MAC as the victim); traffic routes through you. Detected by an ARP anomaly — the gateway IP mapping to a new MAC (arpwatch/DAI).
3. The HTTP-before-HTTPS moment — it keeps the victim on HTTP while proxying HTTPS to the server; it never breaks TLS. HSTS (the browser refuses HTTP for the domain) defeats it.
4. Authentication already happened; the token inherits it, so replaying it needs no login and never triggers MFA. MFA on login only protects the login step.
5. Secure = not sent over HTTP (stops sniffing); HttpOnly = unreadable by document.cookie (stops XSS theft); SameSite = not sent on cross-site requests (stops CSRF).
6. The browser automatically attaches the target site's cookie to any request to that site, including one triggered from the attacker's page, so the forged request runs with the victim's session.
7. Authority, urgency, trust/familiarity, fear, reciprocity.
8. The domain/URL — the page can be cloned perfectly but the domain is never the real one. Top technical control: MFA (a phished password alone fails), plus awareness + reporting.
9. Volumetric (bandwidth) → upstream scrubbing/CDN; protocol/SYN flood (connection state) → SYN cookies/rate limit; application-layer/Slowloris (workers) → reverse-proxy timeouts.
10. MITM = ARP anomaly (gateway MAC changed); hijack = one session ID from two IPs / impossible-travel; DoS = traffic/state spike (Gbps, SYN_RECV pile-up, all workers busy).
