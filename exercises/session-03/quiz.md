---
session: 3
title: Scanning & Enumeration
---

# Session 3 — Quiz

Ten questions. The interactive version is on the teaching page (P25); this is the printable copy.

## Questions

1. On your host-only lab, which host-discovery method is most reliable and cannot be blocked at the host?
   a) ICMP echo  b) TCP SYN ping to 443  c) ARP  d) UDP ping

2. What makes a SYN scan "half-open"?
   a) It scans half the ports  b) It sends RST instead of the final ACK, never completing the handshake  c) It halves the timing  d) It only works on half-duplex links

3. Why does an Xmas scan report open ports as `open|filtered`?
   a) Xmas scans are inaccurate by design  b) The firewall rewrites the response  c) Open ports send RST  d) Open and filtered ports both stay silent, so they're indistinguishable

4. A live Windows host is missing from your `nmap -sn` sweep. Most likely cause?
   a) Windows Firewall blocks ICMP echo by default  b) The host is genuinely offline  c) nmap can't scan Windows  d) ARP is disabled on Windows

5. Why is a full connect scan noisier than a SYN scan?
   a) It always sends more packets per port  b) It uses UDP as well  c) It completes the handshake, so the application logs it  d) It scans more ports

6. Which pair names the current, maintained tools?
   a) enum4linux and crackmapexec  b) enum4linux-ng and NetExec (nxc)  c) enum4linux-ng and crackmapexec  d) smbmap and cme

7. `enum4linux-ng` returns nothing against a default Windows Server 2019. The correct conclusion is:
   a) The command was typed wrong  b) The host is offline  c) SMB isn't running  d) The host is hardened (null sessions off) — enumerate with credentials

8. What gates SNMP read access, and what's the common weakness?
   a) A community string, often left as the default 'public'  b) A Kerberos ticket, often expired  c) An SSH key, often shared  d) Nothing — SNMP is always open

9. Why can't you do LDAP enumeration against a standalone (non-domain) Windows box?
   a) LDAP is Linux-only  b) The firewall always blocks 389  c) There's no directory service running to query  d) LDAP needs SNMP first

10. Your port-scan detection rule should key on which pattern?
    a) A single SYN to port 445  b) One source hitting many distinct ports/hosts in a short time window  c) Any use of nmap's User-Agent  d) Encrypted traffic on port 443

### Short answer
11. In one sentence, why is "SYN scan = stealthy" a dated claim in 2026?
12. Give the breadth-then-depth workflow as two tool names and what each does.

## Answer key
1: c — ARP is layer-2, unblockable, local-only (your lab).
2: b — SYN/ACK received, then RST instead of ACK; handshake never completes.
3: d — open and filtered both go silent to FIN/NULL/Xmas probes.
4: a — Windows Firewall drops ICMP echo by default; use `-Pn`.
5: c — completing the handshake makes the application accept and log the connection.
6: b — enum4linux→enum4linux-ng; CrackMapExec (unmaintained 2023)→NetExec (nxc).
7: d — SMBv1/null sessions off by default on modern Windows; authenticated enum still works.
8: a — a community string, frequently the default 'public'.
9: c — no directory service runs on a standalone box; nothing to query.
10: b — the universal signature is one-to-many in a short window.
11: A modern IDS/flow monitor sees the SYN flood regardless of whether the handshake completed; SYN is faster/lighter, not invisible.
12: masscan/rustscan for breadth (find open ports fast) → nmap for depth (version/OS/scripts on only those ports).
