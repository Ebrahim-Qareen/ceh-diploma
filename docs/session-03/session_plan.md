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
7. **Describe** each of the seven enumeration protocols — SMB, LDAP, SNMP, RPC, NFS, FTP, SMTP — before touching a tool: what it is, how one normal transaction works, and what an attacker gains from finding it.
8. **Enumerate** all seven, and explain why the textbook SMB output is empty on a modern Windows host.
9. **Read a packet capture of every scan and every protocol taught** — state, from the packets alone, which scan was run and what a SOC would have alerted on.
10. **Write one working port-scan detection rule** (Sigma/SPL/KQL) from packet/log evidence they generated themselves.
11. **Assemble** a ranked target profile — the session deliverable and Session 4's input.
12. **Run a full team engagement** end to end: authorisation gate → an authorised internet host → the four-OS lab zoo → the practice range → reading another team's capture.
13. **Verify** that a tool is still maintained before teaching its command (enum4linux-ng, NetExec).

## Time distribution (240 min)

> **Read with the absorb list below.** The 2026-09-07 rebuild added ~40 min of *reference* material
> (7 protocol pages, per-scan capture boxes, the capture library). Most of it is designed to be read,
> not lectured — see "How the new material is delivered".

| Block | Activity | Format | Min |
|---|---|---|---|
| Where we left off + the noise spine + ATT&CK | Bridge (interactive) | Theory | 8 |
| **Wireshark first** — 5 things + the display-filter table + capture library | Theory | 8 |
| **Lab pre-flight** — 4 VMs, 1 subnet, 3 targets | Hands-on | 6 |
| Host discovery — ARP vs ICMP/TCP + 2 packet flows | Theory (stepped) | 10 |
| **Lab 1** — live hosts + the host that plays dead | Hands-on | 12 |
| The scan-type reflex — handshake + open/closed/filtered | Theory (stepped) | 9 |
| SYN & Connect — 2 packet flows, 2 captures | Theory (stepped) | 11 |
| Stealth family & ACK — 2 packet flows, 2 captures | Theory (stepped) | 9 |
| UDP scanning + its packet flow | Theory (stepped) | 7 |
| **Lab 2** — one target, three scans, Wireshark | Hands-on + Wireshark | 20 |
| Timing, breadth-then-depth, version & OS + the noise ladder | Theory (stepped) | 12 |
| **Lab 3** — full scan + the version guess that lies | Hands-on | 15 |
| Scanning countermeasures — the consolidated SOC flip | Defender | 7 |
| Break | — | 10 |
| Evasion preview + its packet flow | Theory (stepped) | 12 |
| Enumeration concepts + the funnel | Theory (interactive) | 7 |
| **Protocol: SMB** — what it is, 9-step flow, what it buys | Theory (stepped) | 10 |
| SMB enumeration + the modern-Windows-empty lesson | Theory | 8 |
| **Lab 4** — SMB against 2012 vs today | Hands-on | 16 |
| **Protocol: LDAP** + **Protocol: SNMP** | Theory (stepped) | 14 |
| SNMP + LDAP enumeration | Theory | 6 |
| **Lab 5** — walk the MIB, query the directory | Hands-on | 15 |
| **Protocol: RPC · NFS · FTP · SMTP** (4 short pages) | Theory (stepped) | 16 |
| NFS/FTP/SMTP/RPC enumeration + NSE + manual netcat | Theory | 6 |
| **Lab 6** — the service sweep | Hands-on | 12 |
| Enumeration countermeasures | Defender | 5 |
| **Lab 7** — read your noise, write the detection rule | Hands-on (signature exercise) | 16 |
| **Lab 8** — assemble the target profile | Hands-on | 12 |
| **Lab 9** — the team engagement (see note) | Hands-on (teams) | 45 |
| Into Session 4 + quiz + practice + homework | Wrap-up | 21 |
| **Total as written** | | **~385** |

**Hands-on as written: pre-flight + 9 labs ≈ 169 min. Delivered at 240 min (see below): ≈ 124 min ≈ 50%.**

### How the new material is delivered — the 240-minute plan

The page now carries ~385 min of material. That is deliberate: it is a **teaching page and a reference
page at the same time**. The instructor decision for a 4-hour delivery is fixed as follows.

| Block | In class | Why |
|---|---|---|
| The 7 protocol pages (66 min as written) | **Teach SMB + LDAP live (24 min). Set SNMP, RPC, NFS, FTP, SMTP as pre-reading** with 8 min of Q&A in class instead of 42 min of lecture. | SMB and LDAP carry the mechanisms the rest reuse (session/auth, and query/oracle). Once a student has those two, the other five are the same shapes with different names — and the pages are written to be read alone. |
| The per-scan Wireshark boxes | **Project them, do not read them.** 30–45 s each: point at the filter, point at the one line that matters, move on. | They exist so the student can re-derive the lesson at home with the capture open. In class they are a caption, not a section. |
| The capture library (19 pcaps) | **Announce once, at the Wireshark page.** Set "open three of them tonight" as homework. | Self-study asset. |
| **Lab 9 — team engagement (45 min)** | **Runs at the start of Session 4**, or as a separate 1-hour workshop slot. | It is a full engagement, not a lab. Squeezing it into the tail of a 4-hour session is how it gets done badly. If you have a 5-hour slot, run it here instead — it is the best thing in the session. |

That leaves **~256 min** in class, exactly the shape Sessions 1–3 already had. Absorb the remaining 16 in this order:

1. **Move Lab 6 (service sweep) to homework** (−12). Self-runnable on Metasploitable2, already met in Session 1, and the guided-lab script runs clean unattended. Cleanest cut.
2. **Trim Lab 2 to 16 min** (−4) by dropping the optional Windows-Xmas failure case (keep it as a "try at home" note).
3. Do **not** cut Lab 7 (the detection rule), Lab 2's core, or the SMB/LDAP protocol pages — they are the session's signature, its evidence source, and the two mechanisms everything else reuses.

## Delivery notes
- **The spine is noise and detection.** Recon (S2) was invisible; scanning is the loudest, most-detected attacker stage. Every scan gets its SOC flip: what the target logs, in which log, with which Event ID/signature.
- **Both tracks at once.** Attacker terminal on one side, defender's capture/log on the other. Orange = attacker, green = defender/SOC.
- **Focus on methods, not flags.** A student who memorises `nmap -sS -p- -T4` has learned nothing; one who can explain the open/closed/filtered reflex, when `-Pn` is mandatory, and what the SOC sees, has learned scanning.
- **The honest EDR point, said out loud:** a modern EDR/IDS catches a default `nmap -A` in seconds. Teaching flags without teaching that is teaching a myth.
- **Every tool gets the 7-part frame:** what it is / why it exists / the method / real syntax / how to read the output / what it feeds / the SOC flip.
- **Protocol before scan (added 2026-09-07).** Every enumeration protocol now gets its own page *before* the tool that enumerates it: what it is, a stepped packet flow of one normal transaction, a facts grid, and an "what finding this port buys the attacker" ladder. Teach the protocol page first, every time — the tool page assumes it.
- **Every scan carries three fixed blocks (added 2026-09-07):** a stepped packet-flow diagram (what happens on the wire), a *What this scan gets you* box (learn / reach for it when / it feeds / remember it as), and an *In Wireshark* box (display filter + real packet lines + what the SOC sees + a link to the capture). The blocks are deliberately identical every time so students learn the shape and can predict what comes next.
- **Wireshark is open all session.** The session now opens with a dedicated Wireshark page and ships **19 real packet captures** in `docs/session-03/assets/pcap/` — one per scan type and per protocol. Every capture was taken from a live lab; nothing is illustrated from memory. Students can follow along with the capture even if their own VM is broken.

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
Two: (1) the **team engagement report** (`docs/session-03/report.html`, cumulative from Session 2) and (2) a **ranked target profile** — per host: live/dead + how confirmed, open TCP/UDP ports, service + version, OS guess + confidence, shares, users, SNMP/LDAP findings, ranked "most likely way in", plus the Lab 7 detection rule as an appendix. Template in `exercises/session-03/`. It is Session 4's input.

## Open items
- Two Session 2 screenshot slots still placeholders (`crtsh-results`, `hunterio-domain-search`).
- Session 1 page 12 ATT&CK Navigator slot still empty (S2's `attack-navigator-ta0043.jpg` could fill it — offered, not applied).
- Defender-side screenshots (Windows Event Viewer 5156/5157, Zeek `conn.log`, Suricata alert) ship as labelled placeholders pending capture on the instructor's Windows/monitored lab — the SVG-rendered real captures carry the teaching in the meantime.
- Official EC-Council PDFs for Ch.11/12/17/18/19 still missing from `Resources/`.
