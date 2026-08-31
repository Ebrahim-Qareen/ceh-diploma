---
session: 3
title: Scanning & Enumeration
module_ref: Modules 3 (Scanning Networks) & 4 (Enumeration)
duration: 4 hours
---

# Session 3 — Session Plan

## Title
Scanning & Enumeration

## Module reference
- Module 3 — Scanning Networks (host discovery, scan types, timing, OS/version discovery, a scoped evasion preview).
- Module 4 — Enumeration (concepts, SMB/SNMP/LDAP/NFS/FTP/SMTP/RPC, NSE, manual banner grabbing, countermeasures).
- Full IDS/firewall/honeypot evasion is deliberately deferred to Session 10 — only a 10–15 min preview lives here.

## Learning objectives
By the end of this session, students will be able to:
1. **Run** a lab pre-flight and triage a "dead" target (wrong adapter, ICMP-blocking firewall, DHCP re-lease).
2. **Choose** the correct host-discovery method by context — ARP on the local segment, TCP probes across a router — and explain why `-Pn` exists.
3. **Explain** every TCP scan type (SYN, connect, FIN, NULL, Xmas, ACK) from the open/closed/filtered reflex, not memorised flags, and read the packets each produces.
4. **Perform** UDP scanning correctly (scoped, not blind) and explain why it is slow.
5. **Apply** the breadth-then-depth workflow (masscan/rustscan → nmap) and read version/OS output critically, including when it lies.
6. **State**, scan type by scan type, exactly what the target logs — the SOC flip — and map each to MITRE ATT&CK.
7. **Enumerate** SMB, SNMP, LDAP, NFS, FTP, SMTP and RPC, and explain why the textbook SMB output is empty on a modern Windows host.
8. **Write one working port-scan detection rule** (Sigma/SPL/KQL) from packet/log evidence they generated themselves.
9. **Assemble** a ranked target profile — the session deliverable and Session 4's input.
10. **Verify** that a tool is still maintained before teaching its command (enum4linux-ng, NetExec).

## Time distribution (240 min)

| Block | Activity | Format | Min |
|---|---|---|---|
| Where we left off + the noise spine + ATT&CK | Bridge (interactive) | Theory | 8 |
| **Lab pre-flight** — 4 VMs, 1 subnet, 3 targets | Hands-on | 6 |
| Host discovery — ARP vs ICMP/TCP, LAN vs internet | Theory (interactive) | 9 |
| **Lab 1** — live hosts + the host that plays dead | Hands-on | 12 |
| TCP flags & scan types (SYN/connect/FIN/NULL/Xmas/ACK) | Theory (interactive + animated) | 12 |
| UDP scanning | Theory | 5 |
| **Lab 2** — one target, three scans, Wireshark | Hands-on + Wireshark | 20 |
| Timing, breadth-then-depth, OS/version | Theory | 10 |
| **Lab 3** — full scan + the version guess that lies | Hands-on | 15 |
| Scanning countermeasures — the consolidated SOC flip | Defender | 7 |
| Break | — | 10 |
| Evasion preview (frag/decoy/timing/source-port/-Pn) | Theory (interactive) | 12 |
| Enumeration concepts + the funnel | Theory (interactive) | 7 |
| SMB enumeration + the modern-Windows-empty lesson | Theory | 10 |
| **Lab 4** — SMB against 2012 vs today | Hands-on | 16 |
| SNMP + LDAP | Theory | 8 |
| **Lab 5** — walk the MIB, query the directory | Hands-on | 15 |
| NFS/FTP/SMTP/RPC + NSE + manual netcat | Theory | 8 |
| **Lab 6** — the service sweep | Hands-on | 12 |
| Enumeration countermeasures | Defender | 5 |
| **Lab 7** — read your noise, write the detection rule | Hands-on (signature exercise) | 16 |
| **Lab 8** — assemble the target profile | Hands-on | 12 |
| Into Session 4 + quiz + practice + homework | Wrap-up | 21 |
| **Total** | | **~256** |

**Hands-on: pre-flight + 8 labs ≈ 124 min ≈ 50% of live time.**

### If you run over
The plan is ~256 min — about 16 over 240, the same shape as Sessions 1 and 2. Absorb in this order:
1. **Move Lab 6 (service sweep) to homework** (−12). The services are self-runnable on Metasploitable2, already met in Session 1, and the guided-lab script runs clean unattended. This is the cleanest cut.
2. **Trim Lab 2 to 16 min** (−4) by dropping the optional Windows-Xmas failure case (keep it as a "try at home" note).
3. Do **not** cut Lab 7 (the detection rule) or Lab 2's core — they are the session's signature and its evidence source.

## Delivery notes
- **The spine is noise and detection.** Recon (S2) was invisible; scanning is the loudest, most-detected attacker stage. Every scan gets its SOC flip: what the target logs, in which log, with which Event ID/signature.
- **Both tracks at once.** Attacker terminal on one side, defender's capture/log on the other. Orange = attacker, green = defender/SOC.
- **Focus on methods, not flags.** A student who memorises `nmap -sS -p- -T4` has learned nothing; one who can explain the open/closed/filtered reflex, when `-Pn` is mandatory, and what the SOC sees, has learned scanning.
- **The honest EDR point, said out loud:** a modern EDR/IDS catches a default `nmap -A` in seconds. Teaching flags without teaching that is teaching a myth.
- **Every tool gets the 7-part frame:** what it is / why it exists / the method / real syntax / how to read the output / what it feeds / the SOC flip.

## Prerequisites (student background)
- MCSA + Linux + CCNA baseline (per scope decisions). TCP/IP, ports and the handshake are assumed, not re-taught — only used as attacker leverage.

## Prerequisites (from earlier sessions)
- **Session 1:** lab built (Kali + Metasploitable2 + Win10 + WinSrv2019), snapshot discipline, first-contact `nmap -sn`/`-sV`/netcat.
- **Session 2:** the ranked recon report — this session starts from it as the scan list.

## Lab prep this session requires (before class)
- **WINSRV19-TGT01 promoted to a domain controller** for `ceh.lab`, with Win10 domain-joined — makes LDAP real and unblocks S4/S6. (`scripts/lab_s3_dc_setup.ps1`.)
- **SNMP installed on WINSRV19-TGT01** with a weak read community string (`scripts/lab_s3_snmp_setup.ps1`) — deliberately findable.
- **SMB policy left at modern defaults** — teach why enum4linux is empty, don't re-enable SMBv1.
- NFS/FTP/SMTP/RPC/Samba are live on Metasploitable2 — anchor Lab 6 there.
- See `labs/lab_design.md` §"Session 3 target preparation".

## Tools / VMs needed
- **VMs:** KALI-ATK01, METASPLOITABLE2, WIN10-TGT01, WINSRV19-TGT01 (DC).
- **Kali tools:** nmap + NSE, masscan, rustscan, netdiscover/arp-scan, hping3, netcat, Wireshark/tshark, enum4linux-ng, smbclient, smbmap, nbtscan, rpcclient, netexec (nxc), snmpwalk, onesixtyone, ldapsearch/windapsearch, showmount, smtp-user-enum, gobuster/ffuf. Verify each with `--version` before class; install lines are in the guided lab.

## Deliverable
A **ranked target profile** — per host: live/dead + how confirmed, open TCP/UDP ports, service + version, OS guess + confidence, shares, users, SNMP/LDAP findings, ranked "most likely way in", plus the Lab 7 detection rule as an appendix. Template in `exercises/session-03/`. It is Session 4's input.

## Open items
- Two Session 2 screenshot slots still placeholders (`crtsh-results`, `hunterio-domain-search`).
- Session 1 page 12 ATT&CK Navigator slot still empty (S2's `attack-navigator-ta0043.jpg` could fill it — offered, not applied).
- Defender-side screenshots (Windows Event Viewer 5156/5157, Zeek `conn.log`, Suricata alert) ship as labelled placeholders pending capture on the instructor's Windows/monitored lab — the SVG-rendered real captures carry the teaching in the meantime.
- Official EC-Council PDFs for Ch.11/12/17/18/19 still missing from `Resources/`.
