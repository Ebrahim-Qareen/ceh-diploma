---
session: 4
title: Access Plan — Session 4 deliverable
---

# Access Plan — <your name / pair> — <date>

The Session 4 deliverable and Session 5's input. One block per host. Conclusions, not raw dumps — exact CVEs,
the public-exploit answer, credentials with their method, and a single chosen way in. Built from your Session 3
target profile plus today's Labs 1–6.

## Scope statement
- Targets: my own host-only lab VMs only (list IPs). No attack left the host-only network.
- The `ceh.lab` domain and its accounts are lab-only, throwaway, and never reused anywhere real.

---

## Host 1 — <IP> · <role, e.g. METASPLOITABLE2>
| Field | Finding |
|---|---|
| Confirmed vulnerabilities | e.g. vsftpd 2.3.4 backdoor — CVE-2011-2523 — CVSS 10.0 — **public exploit: yes** (MSF `vsftpd_234_backdoor`) |
| | e.g. Samba usermap_script — CVE-2007-2447 — CVSS 6.0 — **public exploit: yes** |
| Credentials obtained (and how) | e.g. msfadmin:msfadmin (`/etc/shadow` + John) |
| Other findings / anomalies | e.g. a scanner "critical" that was a false positive on confirming the real version |
| **Chosen way in (for Session 5)** | e.g. vsftpd 2.3.4 backdoor → root (unauth, reliable, network-reachable) |

## Host 2 — <IP> · WIN7-TGT01 (legacy Windows)
| Field | Finding |
|---|---|
| Confirmed vulnerabilities | e.g. MS17-010 — CVE-2017-0144 — CVSS 8.1 — **public exploit: yes** (MSF `ms17_010_eternalblue`) |
| Credentials obtained (and how) | e.g. labuser:Summer2024 (SAM dump + hashcat -m 1000) |
| Other findings | e.g. SMBv1 enabled; local admin NT hash dumped |
| **Chosen way in (for Session 5)** | e.g. EternalBlue → SYSTEM |

## Host 3 — <IP> · WIN10-TGT01 (modern Windows, domain member)
| Field | Finding |
|---|---|
| Confirmed vulnerabilities | e.g. patched — no confirmed public exploit for this build (a finding in itself) |
| Credentials obtained (and how) | e.g. NetNTLMv2 for j.doe captured via LLMNR poison + hashcat -m 5600 |
| Other findings | e.g. LLMNR/NBT-NS enabled (poisonable); SAM hashes dumped |
| **Chosen way in (for Session 5)** | e.g. authenticated access with the captured credential / pass-the-hash |

## Host 4 — <IP> · WINSRV19-TGT01 / DC (ceh.lab)
| Field | Finding |
|---|---|
| Confirmed vulnerabilities | e.g. weak service-account password (Kerberoastable) |
| Credentials obtained (and how) | e.g. svc_backup:<pw> (Kerberoast + hashcat -m 13100); a.fahmy:Autumn2025! (spray) |
| | e.g. svc_sql — roastable but **not cracked** (strong password — the countermeasure worked) |
| Other findings | e.g. account-lockout policy present; NTDS dumpable with a privileged credential |
| **Chosen way in (for Session 5)** | e.g. authenticated foothold with svc_backup → lateral movement |

---

## Vulnerability summary table
| Host | CVE | CVSS | Public exploit? | Reference |
|---|---|---|---|---|
| | | | yes / no | MSF module / EDB id |

## Credential summary table
| Account | Credential type | How obtained | ATT&CK |
|---|---|---|---|
| | plaintext / NT hash | crack / spray / LLMNR / Kerberoast / PtH | T1110.003 / T1003.* / T1558.* / T1557.001 / T1550.002 |

## Appendix A — Detection rule (from Lab 7)
Paste your complete Sigma / SPL / KQL rule, with:
- the threshold and time window, and one sentence on what would false-positive it;
- the ATT&CK mapping (T1110.003 / T1558.003 / T1557.001);
- one sentence on how a *slow* spray could evade it and what you'd change.

```yaml
# your rule here
```

## Appendix B — Evidence index
List the files this plan is built from (sam.txt, unshadowed.txt, netntlm.txt, spn.txt, lab4_spray.evtx,
lab6_kerberoast.evtx …) so a reviewer can check any claim.
