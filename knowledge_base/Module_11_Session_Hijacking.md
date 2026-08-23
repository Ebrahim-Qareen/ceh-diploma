---
source: web research (official CEH v13 syllabus + InfoSecTrain CEH Module 11 reference)
session: 9
gap_topic: true
---

# Module 11 — Session Hijacking

> **Gap topic:** no instructor-deck PDF exists for this module. Content
> built from official CEH syllabus topics and verified web sources.

## Official learning objectives (CEH Ch.11)

1. Explain Session Hijacking Concepts
2. Describe Application-Level Session Hijacking
3. Describe Network-Level Session Hijacking
4. Explain Session Hijacking Tools and Countermeasures

## 1. Session Hijacking Concepts

Session hijacking = taking over an active session between a client and
server by stealing or predicting a valid session token. The attacker
impersonates the legitimate user without needing credentials.

**Session management:** web applications use session tokens (cookies, URL
parameters, hidden form fields) to maintain state after authentication.
If an attacker obtains this token, they own the session.

### Why attacks succeed

- No account lockout for invalid session tokens
- Sessions with no expiration / infinite timeouts
- Weak or predictable session ID generation
- Session IDs transmitted in cleartext (no TLS)
- Insecure session token storage (client-side)
- Small session ID length (brute-forceable)

### Session hijacking vs. spoofing

| | Spoofing | Hijacking |
|---|---|---|
| Target | Initiates a new session with stolen credentials | Takes over an existing active session |
| Timing | Before authentication | After authentication |
| Session state | New | Existing |

## 2. Application-Level Session Hijacking

### Techniques

| Technique | Description |
|---|---|
| Session token sniffing | Intercept tokens in transit (unencrypted HTTP, Wi-Fi) |
| Session token prediction | Predict next token from pattern in generated tokens |
| Man-in-the-Browser (MitB) | Trojan in browser intercepts/modifies transactions in real-time |
| Cross-Site Scripting (XSS) | Inject JS to steal `document.cookie` and send to attacker |
| Cross-Site Request Forgery (CSRF) | Force authenticated user's browser to perform unwanted actions |
| Session fixation | Attacker sets a known session ID before victim authenticates |
| Session replay | Capture and replay a valid session token |
| Cookie theft | Steal cookies via XSS, network sniffing, or physical access |

### CSRF (Cross-Site Request Forgery)

Attacker crafts a request that performs an action on a site where the victim
is authenticated. The victim's browser sends the request with their session
cookie automatically. Example: `<img src="http://bank.com/transfer?to=attacker&amount=1000">`.

**Countermeasure:** anti-CSRF tokens (unique per form), SameSite cookie
attribute, re-authentication for sensitive actions.

## 3. Network-Level Session Hijacking

| Technique | Description |
|---|---|
| TCP session hijacking | Predict TCP sequence numbers to inject packets into an active TCP session |
| Man-in-the-Middle (MITM) | ARP spoofing / DNS spoofing to intercept traffic between client and server |
| IP spoofing | Forge source IP to impersonate one side of the session |
| Blind hijacking | Inject commands without seeing responses (relies on predicted sequence numbers) |
| UDP hijacking | Easier than TCP (no sequence numbers) — spoof UDP packets |

## 4. Tools

- **Burp Suite** — intercept and manipulate session tokens
- **OWASP ZAP** — automated session management testing
- **Ettercap** — MITM / ARP spoofing for network-level hijacking
- **Bettercap** — modern MITM framework
- **Wireshark** — capture session tokens in transit
- **Hamster / Ferret** — session sidejacking (cookie theft on shared Wi-Fi)

## 5. Countermeasures

- Use HTTPS/TLS everywhere (encrypt session tokens in transit)
- Generate strong, random, long session IDs
- Regenerate session ID after login (prevent session fixation)
- Set session timeouts (idle + absolute)
- Use Secure, HttpOnly, SameSite cookie attributes
- Implement anti-CSRF tokens
- Use HTTP Public Key Pinning (HPKP) where supported
- Monitor for ARP cache poisoning
- Deploy IDS/IPS to detect session hijacking patterns
- Implement multi-factor authentication
- Log and audit session activity
- Implement proper logout functionality (invalidate server-side session)
- Never pass session IDs in URLs
