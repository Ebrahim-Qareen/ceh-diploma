---
session: 4
title: System Hacking I — Vulnerability Analysis, Authentication & Password Attacks
---

# Session 4 — Quiz

Ten questions. The interactive version is on the teaching page (P27); this is the printable copy.

## Questions

1. Why can't you simply "decrypt" an NTLM hash back to the password?
   a) The key is stored on the DC  b) It's Base64-encoded  c) Hashing is one-way with no key — you guess inputs instead  d) You can, with the right AES key

2. Responder poisons a broadcast and captures a credential off the wire. What did it actually get?
   a) The plaintext password  b) The NetNTLMv2 challenge-response (crack with -m 5600)  c) The NT hash from the SAM (-m 1000)  d) A Kerberos TGT

3. Why does password spraying succeed where brute-force fails against a lockout policy?
   a) It's faster  b) It uses stolen hashes  c) It encrypts its traffic  d) One password across many accounts = one attempt each, never reaching the lockout threshold

4. What makes Kerberoasting possible for any low-privilege domain user?
   a) Any user can request a service ticket for any SPN, encrypted with the service account's hash  b) The DC emails the password  c) Service accounts have no password  d) It requires Domain Admin

5. Two vulns both score CVSS 8.1. Which vector means you can reach and trigger it from Kali with no help from the victim?
   a) AV:L/PR:H/UI:R  b) AV:P/AC:H  c) AV:N/PR:N/UI:N  d) S:C alone

6. You dumped an NT hash but it won't crack. How can it still get you in?
   a) It can't  b) Pass-the-hash — feed the hash straight to nxc/psexec  c) Decode it from Base64  d) Email it to the DC

7. Which auth-log signature best identifies Kerberoasting on the DC?
   a) 4625 from many sources  b) 4740 lockout  c) A single 4624 success  d) A burst of 4769 with encryption type 0x17 (RC4), one user, many SPNs

8. Which of these leaves NO trace on the target?
   a) searchsploit (local Exploit-DB query)  b) nmap --script vuln  c) A Nessus scan  d) GetUserSPNs -request

9. How many IPs does the free Nessus Essentials tier scan in 2026?
   a) Unlimited  b) 16  c) 5  d) 32

10. What's the correct countermeasure to LLMNR/NBT-NS poisoning, and its 2026 status?
    a) Nothing — it was removed years ago  b) Disable LLMNR + NBT-NS via GPO; still on by default in 2026, so the attack still works  c) Enable SMBv1  d) Turn off Kerberos

### Short answer
11. In one sentence, why is a captured NetNTLMv2 cracked with a different hashcat mode than an NT hash dumped from the SAM?
12. Give the one-line reason a modern EDR/identity product makes teaching credential attacks without their detection "half the job."

## Answer key
1: c — hashing is one-way with no key; you guess candidates and compare.
2: b — Responder captures the NetNTLMv2 response (-m 5600); the NT hash never crosses the wire.
3: d — one password, many accounts, one attempt each — under the lockout threshold.
4: a — any authenticated user can request a service ticket for any SPN, encrypted with the service account's hash (-m 13100).
5: c — AV:N/PR:N/UI:N = network-reachable, no privileges, no user interaction; the actionable part of the vector.
6: b — pass-the-hash (T1550.002); NTLM authenticates with the hash, so no cracking is needed.
7: d — 4769 with encryption type 0x17 (RC4), one user requesting many SPNs in a short window.
8: a — searchsploit queries a local offline database; it never touches the target, so no log.
9: c — 5 IPs (the old "Nessus Home" was 16); verify a tool's current limits before quoting them.
10: b — disable LLMNR (EnableMulticast=0) + NBT-NS via GPO; both still default-on in 2026, and Responder poisons mDNS too.
11: They're different artefacts of the same account — the NT hash (1000) is the stored secret; NetNTLMv2 (5600) is a keyed challenge-response computed from it, so each has its own format and mode.
12: Products like Defender for Identity flag spraying and Kerberoasting in near-real-time, so the paid work is writing and tuning the detections, not just running the attack.
