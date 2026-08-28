---
session: 4
title: System Hacking I — Vulnerability Analysis, Authentication & Password Attacks
---

# Session 4 — Student Guide

Your take-home reference. Everything here is yours to keep and re-read.

## 1. The one idea: attackers log in
You rarely "break" anything. A missing patch, a reused password, a weak service account, a workstation
that still trusts a broadcast — each hands you a **known exploit** or a **legitimate credential**. Session 4
turns your enumerated target profile into both, against a real domain. And because authentication is the
most-monitored surface anywhere, every attack you run has a log line — which you learn to read.

## 2. The vulnerability funnel
```
service + version → CVE → CVSS score → public exploit? → PoC → (Session 5 exploits it)
```
- **CVE** = the identifier for one specific flaw (CVE-2017-0144 = EternalBlue). Find it in NVD / cve.org / vendor advisories.
- **CVSS** = 0–10 severity. **Read the vector, not the number.** `AV:N/PR:N/UI:N` = network-reachable, no privileges, no user click — the actionable part. Currency: v4.0 exists (Nov 2023) but NVD/CEH still lead with v3.1; check which version a score is in before comparing.
- **Public exploit?** = the make-or-break question. `searchsploit <product> <version>`; a `(Metasploit)` hit is gold. No hit ≠ safe.
- **searchsploit is silent** (local DB, no target log). **`nmap --script vuln` is loud** (real probes → 5156, IDS).

## 3. Automated scanning
Nessus Essentials (free tier = **5 IPs** in 2026, not 16) or Greenbone/GVM (OpenVAS is the engine inside GVM).
A scanner finds *candidates*; **you** confirm findings. "Critical" is the tool's confidence, not proof — confirm the real version and reachability, and a version-match false positive dies.

## 4. What a credential is
| | Reversible? | Key? |
|---|---|---|
| Encoding (Base64) | yes | no — not security |
| Encryption (AES) | yes | yes |
| **Hashing (NTLM, SHA)** | **no** | **no** |

A hash is **guessed, not reversed** — hash every wordlist candidate and compare. Weak passwords fall because
they're in the list. **Salt** (random data before hashing) defeats rainbow tables; **NTLM has no salt**.

## 5. Where Windows credentials live
| Store | Holds | Attack (ATT&CK) |
|---|---|---|
| SAM (local) | local NT hashes | SAM dump — T1003.002 |
| LSASS (memory) | live hashes + tickets | mimikatz — T1003.001 (S6) |
| NTDS.dit (DC) | every domain hash | secretsdump — T1003.003 |
| The wire | NTLM challenge-response | poisoning/relay — T1557.001 |

## 6. NTLM and Kerberos
- **NTLM challenge-response:** the NT hash never crosses the wire — only the **NetNTLMv2** response does. Responder captures *that* (crack with **`-m 5600`**), not the NT hash (`-m 1000`).
- **Kerberos:** AS-REQ/AS-REP → TGT → TGS-REQ/TGS-REP → service ticket. Two bleed points:
  - **AS-REP roasting** (T1558.004): an account with no pre-auth → request its AS-REP → crack **`-m 18200`** (`GetNPUsers`).
  - **Kerberoasting** (T1558.003): any user requests a service ticket for any SPN → crack the service account's hash **`-m 13100`** (`GetUserSPNs`).

## 7. Password attacks — the map
- **Online** (attack the login): brute-force, **spraying**, credential stuffing. Slow, logged, lockout applies.
- **Offline** (attack a stolen hash): dictionary, rule-based, mask, hybrid. No lockout, no log — billions of guesses.
- **Spraying beats brute-force:** one password × many accounts = one attempt each, under the lockout threshold. It only takes one reused password.
- **Pass-the-hash (T1550.002):** the NT hash *is* the credential — feed it to `nxc -H` / `psexec`, no cracking.

Cracking pipeline: **hash → identify + mode → wordlist + rules/mask → plaintext.** The #1 mistake is the wrong `-m`.

| `-m` | Hash | From |
|---|---|---|
| 1000 | NTLM (NT hash) | SAM / NTDS |
| 5600 | NetNTLMv2 | Responder |
| 13100 | Kerberos TGS-REP | Kerberoast |
| 18200 | Kerberos AS-REP | AS-REP roast |

## 8. Tool currency (2026) — verify before you teach
| Old / wrong | Use / know |
|---|---|
| Nessus Home, 16 IPs | **Nessus Essentials, 5 IPs** |
| OpenVAS (as a product) | **Greenbone / GVM** (OpenVAS = its engine) |
| CrackMapExec / cme | **NetExec / nxc** |
| "LLMNR was removed" | **Still on by default in 2026** (Microsoft ramping to mDNS; Responder poisons mDNS too) |
| Impacket = SecureAuth | **Fortra**; commands are `impacket-*` |

## 9. MITRE ATT&CK
- **TA0006 Credential Access:** T1110.001/.003 (Guessing/Spraying) · T1003.001/.002/.003 (LSASS/SAM/NTDS) · T1558.003/.004 (Kerberoast/AS-REP) · T1557.001 (LLMNR/NBT-NS + relay) · T1550.002 (Pass-the-Hash).
- **TA0007 Discovery:** vulnerability scanning. **Hand-off:** T1210 Exploitation of Remote Services → Session 5.

## 10. The SOC flip — what the defender sees
| Attack | Event | Signature |
|---|---|---|
| Password spray | **4625** (+ 4771/4768) | many accounts, one source, short window; status 0xC000006A |
| Kerberoast | **4769** | one user, many SPNs, encryption type **0x17** (RC4) |
| AS-REP roast | **4768** | AS-REP request, no pre-auth |
| LLMNR poison | network/EDR | a host answering names it doesn't own; canary lookups |
| Account lockout (bad brute) | **4740** | too many failures on one account |

The honest truth: a modern EDR/identity product flags spraying and Kerberoasting in near-real-time. Teaching
the attack without the detection is half the job — and the detection half is the paid one.

## 11. The deliverable — the access plan
Per host: confirmed vulnerabilities (CVE + CVSS + **public exploit yes/no + reference**), credentials obtained
(and **how**), and the single **chosen way in**, with your Lab 7 detection rule attached. It is Session 5's input.

## Key terms
**one-way hash** · **salt** · **NetNTLMv2 vs NT hash** · **TGT / service ticket** · **SPN** · **Kerberoasting** ·
**AS-REP roasting** · **password spraying** · **pass-the-hash** · **CVSS vector** · **the SOC flip**.
