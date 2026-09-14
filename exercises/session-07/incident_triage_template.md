# Malware Incident Triage Report

**Analyst:** ____________________  **Date:** ____________  **Ticket #:** ____________

---
## 1. Summary & Verdict
- **Sample:** `<filename>`  **SHA-256:** `<hash>`
- **Verdict:** MALICIOUS / SUSPICIOUS / BENIGN — `<family / class>`
- **Impact (one line):** `<what it would do to the org>`
- **Confidence:** high / medium / low — `<basis: static + dynamic + reputation>`

## 2. Behaviour along the lifecycle (with ATT&CK)
| Stage | What it did | ATT&CK | Evidence source |
|---|---|---|---|
| Delivery | | | |
| Execution | | T1204 / T1059 | Sysmon 1 / 4688 |
| Persistence | | T1547 / T1053 / T1543 | Sysmon 13 / 7045 |
| C2 | | T1071.001 | Sysmon 3 / proxy |
| Actions/Impact | | T1486 / T1003 | file volume / Sysmon 10 |

## 3. Indicators of Compromise (by durability)
- **Host:** `<hash, filename, registry path, mutex>`
- **Network:** `<C2 IP/domain/URL, port>`
- **Behaviour/TTP:** `<the durable rule, e.g. unsigned exe in %TEMP% → outbound 443 + Run key>`

## 4. Detections (attached)
- **YARA (file):** `<rule name>` — matches sample, verified not to match benign files
- **Sigma (behaviour):** `<title>` — keys on `<field/condition>`, tag `<attack.tXXXX>`

## 5. Containment
- Isolate host `<id>`; block C2 `<indicator>` at the proxy/firewall; reset exposed credentials `<scope>`.

## 6. Hardening recommendations
- `<e.g. block internet macros; egress filtering; app allow-listing; patch <CVE>; offline backups>`

---
*Static-first, dynamic-in-isolation. Analysis → action.*
