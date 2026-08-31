---
session: 3
title: Target Profile — Session 3 deliverable
---

# Target Profile — <your name / pair> — <date>

The Session 3 deliverable and Session 4's input. One block per **live** host. Conclusions, not raw
dumps — exact versions, stated confidence, ranked way-in. Note dead/absent hosts and *how* you
confirmed the state.

## Scope statement
- Targets: my own host-only lab VMs only (list IPs). No scan left the host-only network.
- Public host `scanme.nmap.org` used only for the LAN-vs-internet contrast, rate-limited.

---

## Host 1 — <IP> · <role, e.g. METASPLOITABLE2>
| Field | Finding |
|---|---|
| Live? How confirmed | e.g. Up — ARP reply (not ICMP) |
| Open TCP ports | |
| Open UDP ports | |
| Service + version (per port) | e.g. 21 → vsftpd 2.3.4 · 445 → Samba 3.0.20 |
| OS guess + confidence | e.g. Linux 2.6.x — high (stack + banners agree) |
| Shares | |
| Users | |
| SNMP findings | community string? processes? software? |
| LDAP findings | base DN, users, groups (DC only) |
| Anomalies / tool lied? | e.g. -sV said tcpwrapped; netcat confirmed Samba 3.0.20 |
| **Ranked "most likely way in"** | 1) … 2) … 3) … (name the service+version + one-line reason each) |

## Host 2 — <IP> · <role, e.g. WIN7-TGT01 (legacy Windows)>
_(repeat the table — note SMBv1 status + MS17-010 result)_

## Host 3 — <IP> · <role, e.g. WIN10-TGT01 (modern Windows)>
_(repeat the table — expect "null session denied": a hardening finding)_

## Host 4 — <IP> · <role, e.g. WINSRV19 / DC>
_(repeat the table — LDAP naming context, users, groups)_

---

## Dead / absent hosts
| IP | State | How confirmed |
|---|---|---|
| | e.g. no host | ARP + `-Pn` both silent |

## Appendix A — Detection rule (from Lab 7)
Paste your complete Sigma / SPL / KQL rule here, with:
- the threshold and time window, and one sentence on what would false-positive it;
- the ATT&CK mapping (T1046 Network Service Discovery / T1595 Active Scanning);
- one sentence on how a `-T0/-T1` scan could evade it and what you'd change.

```yaml
# your rule here
```

## Appendix B — Evidence index
List the output files this profile is built from (hosts_arp.txt, depth.txt, lab2_syn.pcap,
smb_msf.txt, ldap_users.txt, service_sweep.txt …) so a reviewer can check any claim.
