# Session 10 — Final Quiz (answers at the bottom)

1. How do you evade a signature-based IDS vs an anomaly-based IDS?
2. How does a DNS tunnel get a shell through a restrictive firewall, and how is it detected?
3. Why is an implausibly easy, exposed target a reason for caution?
4. Rank WEP, WPA2, WPA3 by security and state how each falls (or resists).
5. Why is capturing a WPA2 handshake dangerous despite WPA2 using AES?
6. What single frame enables handshake capture, wireless DoS, and the evil twin — and what fixes it?
7. What causes most real-world cloud data exposures, and on whose side of shared responsibility?
8. Match each crypto tool to its job: symmetric, asymmetric, hashing.
9. Walk through how TLS combines the three tools.
10. Where does cryptography most commonly fail, and give two examples.

---
## Answers
1. Signature: change the bytes (fragmentation, encoding, polymorphism) so the pattern doesn't match. Anomaly: look normal (blend into allowed ports/protocols) or go low-and-slow under the rate threshold.
2. The implant encodes shell data into DNS queries (subdomains) to an attacker-controlled domain; the firewall allows DNS so it passes. Detected by DNS analytics — high query volume + long, high-entropy subdomains to one domain.
3. It may be a honeypot logging your every move; any interaction with a decoy is a high-signal detection. A real system is rarely that open/helpful.
4. WEP (broken, crack in minutes) < WPA2 (strong AES but the 4-way handshake is captured and cracked offline against a wordlist — weak passphrase falls) < WPA3 (SAE removes the offline-crackable handshake).
5. Cracking happens offline: seconds near the AP captures the handshake, then the passphrase is brute-forced on your own hardware with no rate limit or lockout. A weak passphrase is the whole vulnerability.
6. The (unauthenticated) deauthentication frame. Fixed by 802.11w Protected Management Frames / WPA3.
7. Customer misconfiguration — a public storage bucket, over-permissioned IAM — on the customer's side of shared responsibility ("security in the cloud"), not provider exploits.
8. Symmetric (AES) = confidentiality (fast, bulk); asymmetric (RSA/ECC) = key exchange + digital signatures; hashing (SHA-256) = integrity (one-way).
9. Asymmetric crypto (plus a CA-signed certificate for identity) securely agrees a symmetric session key, then fast symmetric AES encrypts the bulk data — combining asymmetric security with symmetric speed.
10. In deployment, not the math: e.g. old algorithms (MD5/SHA-1/WEP/DES), weak keys/passphrases, unsalted password hashes, or unverified/expired signatures.
