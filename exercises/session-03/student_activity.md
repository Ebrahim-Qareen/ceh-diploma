---
session: 3
title: Scanning & Enumeration
---

# Session 3 — Student Activity

Two in-class activities. The first is done in pairs; the second is individual. Neither needs a
working VM — both run on evidence, so they double as the fallback for anyone whose lab is down.

## Activity 1 — Name that scan (pairs, 15 min)
Your instructor hands each pair three short packet captures (or the printed packet lists below),
labelled A, B, C. For each, decide the scan type **from the packets alone** and justify it.

**Capture A**
```
101 → 102  80  [SYN]
102 → 101  80  [SYN, ACK]
101 → 102  80  [RST]
101 → 102  443 [SYN]
102 → 101  443 [RST, ACK]
101 → 102  8080 [SYN]        (no reply, retried)
```

**Capture B**
```
101 → 102  445 [FIN, PSH, URG]
101 → 102  443 [FIN, PSH, URG]
102 → 101  443 [RST, ACK]
101 → 102  22  [FIN, PSH, URG]     (no reply)
101 → 102  80  [FIN, PSH, URG]     (no reply)
```

**Capture C**
```
101 → 102  443 [ACK] ;  102 → 101  443 [RST]
101 → 102  445 [ACK] ;  102 → 101  445 [RST]
101 → 102  8080 [ACK]              (no reply)
```

For each, write: (1) the scan type and flag, (2) which ports are open / closed / filtered and how you
can tell, (3) one sentence on what a defender would see. Then answer: **which of the three tells you
the least about open ports, and why?**

> Answer key (instructor): A = SYN scan (`-sS`) — 80 open (SYN/ACK then RST), 443 closed (RST,ACK),
> 8080 filtered (no reply). B = Xmas (`-sX`) — 443 closed (RST), 22/80/445 open|filtered (silence);
> tells you least about open ports because open and filtered are indistinguishable. C = ACK scan
> (`-sA`) — 443/445 unfiltered (RST), 8080 filtered (silence); finds the firewall, not open ports.

## Activity 2 — Hardened or not reachable? (individual, 12 min)
For each result below, decide whether it means the service is **hardened**, **not running**, or
**leaking**, and state the next move.

1. `enum4linux-ng -A <win2019>` returns "null session denied," empty users/shares.
2. `enum4linux-ng -A <metasploitable2>` returns full users, shares, groups, workgroup.
3. `nmap -sn <subnet>` shows a Windows host as down, but `nmap -Pn -p445` shows 445 open.
4. `snmpwalk -v2c -c public <host>` times out; `onesixtyone` finds no community string.
5. `showmount -e <host>` returns `/  *` (exported to everyone).

> Answer key (instructor): 1 = hardened → enumerate with a credential (`nxc -u -p`). 2 = leaking →
> take the users into S4 password attacks. 3 = the host was never down; ICMP was filtered — `-Pn` is
> the right tool. 4 = SNMP not running / no default string → not a finding here, move on. 5 = leaking
> badly → mount it (`root_squash` missing is the countermeasure).

**Close:** in one sentence each, why is "the command returned nothing" never, by itself, a finding —
and what turns it into one?
