---
session: 4
title: System Hacking I — Vulnerability Analysis, Authentication & Password Attacks
module_ref: Modules 5 (Vulnerability Analysis) & 6 pt1 (System Hacking — Access)
duration: 4 hours
---

# Session 4 — Session Plan

## Title
System Hacking I — Vulnerability Analysis, Authentication & Password Attacks

## Module reference
- Module 5 — Vulnerability Analysis (concepts, research sources, CVE/CVSS scoring, `searchsploit`, automated scanning).
- Module 6 pt1 — System Hacking / Access (authentication & hash algorithms, Windows auth NTLM/Kerberos, password cracking, LLMNR/NBT-NS poisoning, shell types + Metasploit intro as a concept bridge).
- Manual exploitation, msfvenom and buffer overflows are **Session 5** — only a short concept bridge lives here.

## Learning objectives
By the end of this session, students will be able to:
1. **Run** the vulnerability funnel — turn an enumerated service+version into a CVE, a CVSS score, and a yes/no on a public exploit (`searchsploit`, `nmap --script vuln`).
2. **Read** a CVSS vector (not just the number) and judge reachability; state the v3.1↔v4.0 currency difference.
3. **Triage** an automated scan (Nessus Essentials / Greenbone) and distinguish a real, reachable finding from a false positive.
4. **Explain** the mechanism before the tool — hashing vs encryption vs encoding, NTLM challenge-response (what crosses the wire), the Kerberos flow and its two bleed points.
5. **Crack** offline hashes (SAM NT hashes, `/etc/shadow`) with hashcat/John, choosing the correct mode.
6. **Attack** a real domain — password spray (netexec), LLMNR poison (Responder), Kerberoast + AS-REP roast (Impacket), and pass-the-hash.
7. **Generate and read** real auth-log evidence (4625 spray, 4769 Kerberoast, a Responder capture) and **write one working credential-attack detection rule** (Sigma/SPL/KQL).
8. **Assemble** an access plan — per host, confirmed vulns (CVE+CVSS+exploit?), credentials obtained and how, the single chosen way in — the Session 5 input.
9. **Map** every technique to MITRE ATT&CK (TA0006 Credential Access) and state the T1210 hand-off to Session 5.
10. **Verify** a tool is still current before teaching it (Nessus 5-IP limit, LLMNR 2026 status, Impacket source, CVSS v4).

## Time distribution (target 240 min; plan ~259 with documented absorb options)

| Block | Activity | Format | Min |
|---|---|---|---|
| Where we left off — the profile becomes ammunition + ATT&CK | Bridge | Theory | 8 |
| **Lab pre-flight** — domain up, profile in hand, rockyou unpacked | Hands-on | 5 |
| Vulnerability concepts + the vulnerability funnel | Theory (interactive) | 8 |
| Research sources + CVSS scoring (the vector) | Theory | 9 |
| `searchsploit` + `nmap --script vuln` | Theory (interactive) | 7 |
| **Lab 1** — version → CVE → "public exploit?" | Hands-on | 16 |
| Automated scanning — Nessus Essentials vs Greenbone | Theory (interactive) | 7 |
| **Lab 2** — scan demo + the false-positive "critical" | Hands-on demo | 8 |
| Authentication + hashing vs encryption vs encoding | Theory | 9 |
| Where creds live + NTLM challenge-response | Theory (animated) | 10 |
| Kerberos ticket flow + the two bleed points | Theory (animated) | 10 |
| Password-attack taxonomy + the cracking pipeline | Theory (interactive) | 9 |
| Break | — | 10 |
| Offline cracking — hashcat + John | Theory | 8 |
| **Lab 3** — crack SAM + /etc/shadow; the wordlist that fails | Hands-on | 15 |
| Online attacks — hydra/medusa/netexec; spray vs brute vs lockout | Theory | 8 |
| **Lab 4** — password spray the DC → the 4625 spike | Hands-on | 14 |
| LLMNR/NBT-NS poisoning + Responder | Theory | 8 |
| **Lab 5** — poison a broadcast, capture a NetNTLMv2, crack it | Hands-on | 14 |
| Kerberoast + AS-REP + Impacket + pass-the-hash | Theory | 9 |
| **Lab 6** — roast a service ticket → the 4769; the one that won't crack | Hands-on | 15 |
| The auth-log SOC flip (consolidated) | Defender | 6 |
| **Lab 7** — write the credential-attack detection rule | Hands-on (signature exercise) | 16 |
| **Lab 8** — assemble the access plan | Hands-on | 12 |
| Into Session 5 — shells + Metasploit (concept only) | Theory | 6 |
| Quiz + practice range + homework | Wrap-up | 12 |
| **Total** | | **~259** |

**Hands-on: pre-flight + 8 labs ≈ 117 min ≈ 45% (≈50% counting the guided scan demo and the two evidence-read blocks).**

### If you run over
The plan is ~259 min — about 19 over 240 (same shape as S1–S3, which the instructor kept). Absorb in this order:
1. **Move Lab 2 (scan demo) to homework / a recorded demo** (−8). The THM `openvas` room covers it free.
2. **Move the `/etc/shadow` half of Lab 3 to homework** (−4). MSF2 cracking is self-runnable.
3. **Trim the mechanism pages 1 min each** (−3–4) — the animated diagrams carry them.
4. Do **not** cut Labs 4, 5, 6 (the evidence), Lab 7 (the rule), or Lab 8 (the deliverable).

## Delivery notes
- **The spine is "attackers log in."** Authentication is the most-attacked and most-monitored surface; every credential attack is loud in the auth logs, so every attack gets its SOC flip (Event ID + signature).
- **Mechanism before tools.** Do not teach hashcat before hashing, or Responder before NTLM challenge-response. Build the diagrams first (P10–P13), then hang the tools on them.
- **The domain is the centrepiece.** This is the first session that attacks a domain (`ceh.lab`), not a standalone box — the AD lab from Session 3 is what this session was built for. Say that on the page.
- **Diagrams over words** (standing instructor preference): 16 hand-authored SVG (2 animated, 7 interactive) + 1 real captured-data figure + 3 placeholder capture slots.
- **Focus on methods, not syntax.** A student who runs `hashcat -m 1000` has learned nothing; one who can explain what an NTLM hash is, why it's crackable offline, why spraying beats brute-force, and what the SOC sees has learned authentication.
- **The honest EDR point, out loud:** a modern EDR/identity product (Defender for Identity) flags spraying and Kerberoasting in near-real-time. Teaching the attack without the detection is half the job — the detection half is the paid one.
- **Every tool gets the 7-part frame:** what it is / why it exists / the method / real syntax / how to read output / what it feeds / the SOC flip.

## Prerequisites (student background)
- MCSA + Linux + CCNA baseline. Kerberos, NTLM, hashing basics are used, not re-taught from zero — only as attacker leverage.

## Prerequisites (from earlier sessions)
- **Session 3:** the ranked **target profile** — version strings, users, shares, SNMP/LDAP findings. This session starts from it.
- **Session 3 lab:** the `ceh.lab` DC (WINSRV19), Win10 domain-joined, Win7 legacy target, Metasploitable2.

## Lab prep this session requires (before class)
- **`scripts/lab_s4_dc_setup.ps1 -Stage Kerberoast`** on the DC — SPN + weak password on `svc_backup` (cracks), plus `svc_sql` with an SPN + strong password (never cracks).
- **`-Stage SprayPolicy`** on the DC — one weak password on `a.fahmy`/`n.gamal`/`h.rashad`, a distinct strong one on `m.said`, and an account-lockout policy (5/15).
- **`-Stage LocalAccounts`** on Win7 and Win10 — 2–3 weak local accounts for the SAM/hashcat lab.
- **`-Stage CheckLLMNR`** on Win10 — confirm LLMNR/NBT-NS still enabled (they are, by default).
- **A vulnerability scanner** — Nessus Essentials (5-IP free tier; plugin download done before class) or Greenbone/GVM.
- **`rockyou.txt` unpacked** on Kali (`gunzip -k`). Take a third DC snapshot `baseline-s4`.
- See `labs/lab_design.md` §"Session 4 target preparation".

## Tools / VMs needed
- **VMs:** KALI-ATK01, METASPLOITABLE2, WIN7-TGT01, WIN10-TGT01 (domain member), WINSRV19-TGT01 (DC).
- **Kali tools:** `searchsploit` (exploitdb), `nmap`+NSE, Nessus Essentials / `gvm`, `hashcat`, `john` (jumbo), `hydra`, `medusa`, `netexec` (nxc), `responder`, the Impacket suite (`impacket-GetUserSPNs`, `-GetNPUsers`, `-secretsdump`, `-psexec`), `evil-winrm`; `mimikatz`/`msfconsole` introduced only. Verify each with `--version`/`-h` before class.

## Deliverable
An **access plan** — per host: confirmed vulnerabilities (CVE + CVSS base score + does a public exploit exist?), credentials obtained (and how: cracked hash / spray / LLMNR / Kerberoast / pass-the-hash), and the single chosen way in, plus the Lab 7 detection rule as an appendix. Template in `exercises/session-04/access_plan_template.md`. It is Session 5's input.

## Open items
- Windows auth-log capture slots (`event-4625-spray`, `responder-capture`, `getuserspns`) ship as labelled placeholders pending capture on the instructor's monitored domain — the SVG diagrams + the real hashcat capture carry the teaching meanwhile. This session is also the moment to capture the S3-deferred defender screenshots (5156/5157) on the same lab.
- Two Session 2 screenshot slots still placeholders (`crtsh-results`, `hunterio-domain-search`); Session 1 page 12 ATT&CK Navigator slot; official EC-Council PDFs for Ch.11/12/17/18/19.
