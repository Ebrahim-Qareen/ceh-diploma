---
session: 3
title: Scanning & Enumeration
---

# Session 3 — Instructor Guide

Everything you need to run the session. Pair this with `session_plan.md` (timings) and
`guided_lab.md` (the exact commands students run). Rationale for design choices is in
`DECISIONS.md`; this is the teaching-flow detail.

## Pre-class checklist
- [ ] All four VMs boot; baseline snapshots exist. **Second baseline on WINSRV19 after the DC promotion + SNMP install** (`baseline-dc`) — reverting past it breaks every AD lab.
- [ ] `scripts/lab_s3_dc_setup.ps1` run: WINSRV19 is a DC for `ceh.lab`, Win10 domain-joined, directory seeded (a.fahmy, m.said, n.gamal, svc_backup + lab groups + LabDocs share).
- [ ] `scripts/lab_s3_snmp_setup.ps1` run: SNMP up on WINSRV19 with a weak, guessable community string.
- [ ] From Kali: `nmap -sn <subnet>` returns Metasploitable2 + both Windows boxes; `snmpwalk` and `ldapsearch` both return data against WINSRV19.
- [ ] Wireshark works on Kali against the host-only interface.
- [ ] Verify tool currency live: `nxc --version`, `enum4linux-ng`, `rustscan --version`, `masscan --version`. Install any that are missing (lines in the guided lab).
- [ ] `saved/` fallback output files are on each student image (hosts_arp.txt, depth.txt, lab2_syn.pcap, smb_msf.txt, ldap_users.txt, service_sweep.txt) for anyone whose VM dies.
- [ ] One lab credential per student for Lab 4 Step 3 (authenticated SMB) — hand out, never write in any repo file.

## The currency corrections — know these cold
Say each out loud as "verify the tool is still alive before you teach the command," not as trivia.
1. **`crackmapexec` → NetExec (`nxc`).** CME unmaintained since 2023; the active fork is NetExec. Use `nxc`.
2. **`enum4linux` → `enum4linux-ng`.** The rewrite outputs JSON/YAML and does LDAP + password policy natively (wraps nmblookup/net/rpcclient/smbclient).
3. **SMBv1 + null sessions are OFF by default** on Win10 (FCU+) and Server 2019+. Microsoft: "SMBv1 isn't installed by default in any edition of Windows 11 or Windows Server 2019 and later versions." So the classic enum4linux dump doesn't appear on a modern host — that's a hardening finding, not a failed command.
4. **Windows Firewall blocks ICMP echo** by default — a live Windows host looks dead to `nmap -sn`. Teach `-Pn` as the #1 beginner fix.
5. **masscan/rustscan for breadth, nmap for depth** is the current real workflow — not one giant `nmap -A -p-`.
6. **Metasploitable2 is 2012-era.** Perfect for teaching, useless as a picture of a modern host. Say so, so students don't generalise.

## The one thing to get right all session: the noise/detection spine
This is the session where offense meets defense. Every time a student runs a scan, ask "what did the target just log?" before moving on. The universal signature under every scan and enumeration is **one source → many ports/hosts → short window**. Drive toward Lab 7, where they encode exactly that into a rule.

## Teaching flow

### P2 — Where we left off (8 min)
Open by connecting to S2's recon report: it becomes today's scan list. Land the spine hard — recon left no target-side log, scanning fills a firewall log with the student's IP. Show the ATT&CK table (TA0043 → TA0007). Don't re-teach what a port is.

### P3 — Lab pre-flight (6 min, hands-on)
Everyone runs `nmap -sn` on the subnet. Expect a Windows box to be "missing" — that is the teed-up lesson for Lab 1, not a fault. Work the troubleshooting table for anyone genuinely stuck. Do not let anyone turn off Windows Firewall.

### P4 — Host discovery (9 min)
The ARP-vs-router distinction is the method here. ARP can't be blocked but is local-only (their whole lab); ICMP/TCP cross routers but get filtered. `-Pn` is the resolution. Click through the interactive diagram.

### Lab 1 (12 min, hands-on)
The set-piece: ARP sweep (ground truth) vs ICMP sweep (misses a Windows host) vs `-Pn` (proves it was alive). The teaching moment is the diff between hosts_arp.txt and hosts_icmp.txt. Make them say the rule aloud: *ICMP silence means "no answer," never "no host."*

### P6 — Scan types (12 min)
The heart of the session. Teach the reflex table (open answers SYN, ignores stealth flags; closed RSTs everything; filtered is silent) so every scan type is derivable. Play the animated handshake→SYN-scan diverge. Then the interactive real-capture panels — these are actual packets, walk one column. Kill the "SYN is stealthy" myth: it's *faster/lighter*, not invisible.

### P7 — UDP (5 min)
Why it's slow (ICMP rate-limiting), why you still do it (SNMP/DNS/DHCP), and always scope it. Sets up SNMP in Lab 5.

### Lab 2 (20 min, hands-on + Wireshark) — the signature lab
The must-do. Three scans against Metasploitable2 with Wireshark capturing. The deliverable is the three-column comparison (real capture image on the page as a model). **Make them save `lab2_syn.pcap`** — Lab 7 depends on it. Two minutes on the defender filter `tcp.flags.syn==1 and tcp.flags.ack==0` seeds Lab 7.

### P9 + Lab 3 (10 + 15 min)
Breadth-then-depth (rustscan/masscan → nmap). The two failures are the lesson: `tcpwrapped`/`?` version guesses (confirm by hand later) and a full UDP scan that never ends (scope it). Note the packet-noise chart — depth costs noise (13 → 103 → 708 packets, real numbers).

### P11 — Scanning countermeasures (7 min)
Pivot to the SOC desk. Walk the consolidated flip table. The universal pattern (one-to-many, short window) is the thesis they'll encode in Lab 7. This is the tier-1 SOC ticket they'll actually triage.

### Break (10 min)

### P13 — Evasion preview (12 min) — keep it SHORT
This is a 10–15 min preview, not the chapter. Four tricks + the honest EDR truth. Every technique's detail says why it fades against a modern sensor. If you're short on time, this compresses to 8. Full evasion is Session 10 — do not expand it, and do not remove it from S10.

### P14 — Enumeration concepts (7 min)
Scanning = one-way reflex reading; enumeration = a conversation you log into. The funnel (port→service→version→users/shares→way in) applies to every service. This is where "recon" becomes "intrusion attempt" for a defender.

### P15 + Lab 4 (10 + 16 min) — the SMB contrast
The key enumeration lesson. enum4linux-ng rich on Metasploitable2, near-silent on modern Windows, then authenticated with a credential. Drill the line: "enum4linux returned nothing" is never the finding — "the host refuses null sessions → hardened → enumerate with creds" is.

### P17 + Lab 5 (8 + 15 min) — SNMP + LDAP
SNMP: find the community string (onesixtyone), walk the tree. LDAP: bind to the DC, dump users/groups. Both feed S4's password attacks. Be honest that SNMP was deliberately enabled weak — a hardened box doesn't run it. **If the DC build was declined:** Part B runs against THM `networkservices2` and LDAP is concept-only here — do not fake a directory.

### P19 + Lab 6 (8 + 12 min) — the service sweep
NFS/FTP/SMTP/RPC on Metasploitable2, then a manual netcat banner grab to confirm a version. This is the absorb-to-homework lab if you're behind.

### P21 — Enumeration countermeasures (5 min)
Every win came from a default. The GRC angle: finding + fix is what an assessment report is.

### Lab 7 (16 min, hands-on) — the signature exercise, protect this time
The session's reason to exist. They read their own `lab2_syn.pcap`, identify the scan from evidence alone, and write one working rule. Worked Sigma on the page; they complete SPL or KQL. Push them on the threshold and the false-positive cost, and on how a `-T0` scan slips under it. Do not let this get squeezed.

### Lab 8 (12 min) — the target profile
Assemble everything per host, ranked. Same pass/needs-review standard as S2's recon report: conclusions, not dumps. This is literally S4's input — make them finish it as homework if class runs out.

### P24–P27 — Bridge, quiz, practice, wrap (21 min)
Bridge to S4 (profile → vuln + passwords, now against a real domain). Run the 10-question quiz. Point at the fully-free practice path. Assign homework.

## Bridge to next session
Session 4 — Vulnerability Analysis, Authentication & Password Attacks. The target profile's version strings go into CVE/CVSS + searchsploit; the user list goes into password spraying; and because WINSRV19 is now a DC, NTLM/Kerberos/LLMNR poisoning run against a real domain. The AD lab built for this session is what unlocks S4 and S6.
