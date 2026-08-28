---
session: 4
title: System Hacking I — Vulnerability Analysis, Authentication & Password Attacks
---

# Session 4 — Instructor Guide

Everything to run the session. Pair with `session_plan.md` (timings) and `guided_lab.md` (exact commands).
Rationale is in `DECISIONS.md`; this is the teaching-flow detail. Same shape as the S1–S3 guides.

## Pre-class checklist
- [ ] All five VMs boot; DC (`ceh.lab`) is up. **Third baseline snapshot `baseline-s4`** exists on the DC (reverting past it removes the Kerberoast SPN and spray passwords).
- [ ] `lab_s4_dc_setup.ps1 -Stage Kerberoast` run: `svc_backup` has an SPN + a **weak** (wordlist-crackable) password; `svc_sql` has an SPN + a **strong** password.
- [ ] `-Stage SprayPolicy` run: `a.fahmy`/`n.gamal`/`h.rashad` share one weak password, `m.said` has a distinct strong one, lockout policy = 5 tries / 15 min.
- [ ] `-Stage LocalAccounts` run on **Win7 and Win10**: 2–3 weak local accounts.
- [ ] `-Stage CheckLLMNR` on Win10 reports LLMNR + NBT-NS **enabled**.
- [ ] Vulnerability scanner ready: Nessus Essentials (plugins downloaded) **or** Greenbone (feed synced). Confirm it scans the four targets.
- [ ] `rockyou.txt` unpacked on Kali; `best64.rule` present (`/usr/share/hashcat/rules/`).
- [ ] Verify tool currency live: `hashcat --version`, `nxc --version`, `responder -h`, `impacket-GetUserSPNs -h`, `evil-winrm --version`, `searchsploit -h`.
- [ ] `saved/` fallback evidence on each student image: `sam.txt`, `unshadowed.txt`, `lab4_4625.evtx`, `lab5_netntlmv2.txt`, `lab6_4769.evtx`, `lab6_krb5tgs.txt`.
- [ ] One local-admin credential per student for the SAM dump (Lab 3) — hand out, never write in the repo.

## The currency corrections — know these cold
Say each as "verify the tool is still alive before you teach the command," not trivia.
1. **Nessus Home → Nessus Essentials, and it's 5 IPs now (not 16).** Confirmed on Tenable's product page, 2026. Fits our four targets. "Essentials Plus" (paid) is 20.
2. **OpenVAS → Greenbone / GVM.** "OpenVAS" is the scanner engine *inside* GVM now; the product is Greenbone.
3. **CrackMapExec → NetExec (`nxc`).** CME unmaintained since 2023 (established in S3).
4. **CVSS v3.1 vs v4.0.** v4.0 shipped Nov 2023 but NVD still leads with v3.1 and CEH v12 is v3.x. v4 reworked the vector (VC/VI/VA + SC/SI/SA + AT, dropped Scope). Teach the vector, and "check which version a score is in."
5. **LLMNR/NBT-NS are still on by default on Windows 10/11 in 2026.** Microsoft is "ramping down" toward mDNS but hasn't disabled them — the attack is alive (fresh public LLMNR→DC write-ups monthly). Responder poisons mDNS too.
6. **Impacket is maintained by Fortra** (github.com/fortra/impacket); Kali ships it as `impacket-scripts` (commands prefixed `impacket-`).
7. **hashcat modes:** NTLM 1000, NetNTLMv2 5600, Kerberoast TGS 13100, AS-REP 18200. `rockyou` ships gzipped on current Kali.
8. **Metasploitable2 is 2012-era** — perfect for CVE→exploit practice, useless as a modern vuln picture. Say so, as in S3.

## The one thing to get right: mechanism before tools
The failure mode is jumping to `hashcat -m 1000` before students know what an NT hash is. Build P10–P13 (hashing, NTLM, Kerberos, taxonomy) as diagrams **first**. If a student can explain what crosses the wire in NTLM (NetNTLMv2, not the NT hash) and why spraying beats brute-force, the tools are trivial. Drive every attack toward its auth-log signature and Lab 7.

## Teaching flow

### P2 — Where we left off (8 min)
Land the spine: recon invisible (S2), scanning loud (S3), **now credentials against a real domain**. The target profile is today's ammunition. Walk the ATT&CK table (TA0006). Don't re-teach ports.

### P3 — Lab pre-flight (5 min, hands-on)
Confirm the DC answers on 88/389/445 and LDAP returns `DC=ceh,DC=lab`. Everyone unpacks rockyou. If a student reverted to `baseline-dc` not `baseline-s4`, the Kerberoast/spray targets are gone — re-run the S4 script or use `saved/`.

### P4–P6 — Vuln analysis theory (8+9+7)
The funnel (interactive) is the through-line. On CVSS, drive "read the vector, not the number" with the EternalBlue example. On P6, the key idea is **searchsploit is silent, `--script vuln` is loud** — the interactive diagram makes it stick.

### Lab 1 (16 min, hands-on)
Disciplined lookup, no firing. The MS17-010 line ("CVE-2017-0144, CVSS 8.1, public exploit: yes") is the Session 5 target — make them write it. The failure case: a searchsploit hit is a *lead*, confirmed by exact version.

### P8 + Lab 2 (7 + 8 min) — guided demo
One scan on the projector; everyone reads it. The teaching moment is Step 2 — pick a "critical," confirm the real version, judge false positive. Don't let every student launch their own scan.

### P10 — Auth + hashing (9 min)
The hashing-vs-encryption-vs-encoding diagram is load-bearing. Drive "a hash is guessed, not reversed." Salting → why NTLM (unsalted) is so attractive.

### P11 — NTLM animated (10 min)
Play the animation. The one line to land: **Responder captures NetNTLMv2 (mode 5600), not the NT hash (mode 1000)** — same account, different artefact. This prevents the #1 mode mistake in Lab 5.

### P12 — Kerberos animated (10 min)
Play it. Two bleed points: AS-REP roast (no pre-auth, 18200) and Kerberoast (any user, 13100). Preview the 4768/4769 signatures — they return in the SOC flip and Lab 7.

### P13 — Taxonomy + pipeline (9 min)
The interactive map puts every tool in its place. The online↔offline split is the key idea (offline = no lockout, no log). Pass-the-hash node: you don't always crack.

### Break (10 min)

### P15 + Lab 3 (8 + 15 min) — offline cracking
secretsdump the SAM, `-m 1000`; unshadow + John for MSF2. The failure case (Step 3): "Exhausted" ≠ "uncrackable" — add rules. **No target log** — the detectable event was the *theft*, not the crack. Say it.

### P17 + Lab 4 (8 + 14 min) — spray, generates 4625
The brute-vs-spray diagram is the point. Lab 4 hits 3/5 and misses `m.said` (realistic). **Make them save the DC Security log** — Lab 7 needs it. Step 3: brute one account, trip lockout (4740), feel why spraying exists.

### P19 + Lab 5 (8 + 14 min) — LLMNR, generates a capture
The single poisoning diagram teaches the whole attack. Responder on Kali, trigger a typo'd share from Win10, capture NetNTLMv2, crack `-m 5600` (not 1000). Countermeasure + 2026 currency. **Save the capture.**

### P21 + Lab 6 (9 + 15 min) — Kerberoast, generates 4769
Impacket 7-part; the pass-the-hash diagram (cracking is optional). Lab 6: roast both SPNs, crack `svc_backup` (13100), fail on `svc_sql` (strong pw — the honest limit), then pass-the-hash + evil-winrm. **Save the 4769 log.**

### P23 — The auth-log SOC flip (6 min)
Pivot to the SOC desk. The side-by-side diagram (orange did it, green saw it) + the interactive credential-across-OS map. Land the honest EDR point — this sets up Lab 7 as the paid skill.

### Lab 7 (16 min) — the signature exercise, PROTECT this time
The session's reason to exist. They read their own 4625/4769 evidence, identify the attack from evidence alone, and write one working rule. Worked Sigma (password spray) on the page; they complete SPL or KQL. Push on threshold, false positives, and how a *slow* spray evades the window. Do not let this get squeezed.

### Lab 8 (12 min) — the access plan
Assemble per host: confirmed vulns (CVE+CVSS+exploit?), creds + how, one chosen way in. Same pass/needs-review standard as S3's target profile — conclusions, not dumps. This is literally S5's input; finish as homework if class runs out.

### P26 — Into Session 5 (6 min, concept only)
Bind vs reverse (interactive), msfconsole in one line, "you have the key — next session you turn it." **Do not lab exploitation here** — that's S5, and expanding it blows the timing.

### P27–P29 — Quiz, practice, wrap (12 min)
10-question quiz. Point at the fully-free THM path (Attacktive Directory is the gem — free). Assign homework.

## Bridge to next session
Session 5 — System Hacking II: Exploitation, Shells & Payloads. The access plan's "chosen way in" per host is exactly what S5 executes — EternalBlue on Win7, vsftpd/usermap on MSF2, a cracked/pass-the-hash credential on the domain. Manual exploitation first, then msfvenom and buffer overflows. Same local lab, same carry-through target.

## If the DC build was declined or broke
Labs 4/5/6 need the domain. Fallbacks: Lab 4 sprays the local Metasploitable3 "Star Wars" accounts instead; Lab 5 poisons any Windows member (even non-domain); Lab 6 (Kerberoast) has **no** non-domain equivalent — run it against THM `attacktivedirectory` (free) as a group, and use the `saved/lab6_*` evidence for Lab 7. Never fake a ticket.
