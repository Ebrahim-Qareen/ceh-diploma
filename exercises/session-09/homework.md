# Session 9 — Homework

## Core (everyone)
1. **MITM + sniff on your lab.** Two host-only VMs: ARP-poison one, capture a cleartext HTTP login in Wireshark, then repeat against an HTTPS service and confirm you get only ciphertext. Write up what TLS + DAI would change. Stop the spoof cleanly.
2. **Session hijack.** Steal a session cookie (from your MITM capture or an S8 XSS) and replay it for account takeover on a lab app. Then set `Secure; HttpOnly; SameSite` and re-test — document which attacks now fail.
3. **Phishing analysis (defender side).** Take a real phishing email (from your spam or a public sample), and produce a one-page analysis: the psychological levers, the header/domain indicators, and the controls that would have stopped it.

## Stretch
4. Complete a free TryHackMe room: **Phishing Analysis Fundamentals** (analyst side) or a network-attacks intro room.
5. Run a SYN flood + Slowloris against a throwaway lab web VM, apply SYN cookies and a proxy timeout, and record the before/after.

## Submit
- The MITM write-up (with the HTTP-vs-HTTPS capture comparison)
- The session-hijack + cookie-flags before/after
- The phishing analysis one-pager
- (stretch) room completion / DoS before-after

**Reminder:** MITM, phishing, and DoS against anything you don't own are crimes. Isolated lab, consenting accounts, or written authorisation — always.
