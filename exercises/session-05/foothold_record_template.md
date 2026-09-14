---
session: 5
title: Foothold Record — Session 5 deliverable
---

# Foothold Record — <your name / pair> — <date>

The Session 5 deliverable and Session 6's input. One block per host you landed on. Conclusions, not raw dumps.
Built from your Session 4 access plan plus today's Labs 1–8.

## Scope statement
- Targets: my own host-only lab VMs only (list IPs). No exploit left the host-only network.
- The `ceh.lab` domain and its accounts are lab-only, throwaway, and never reused anywhere real.

## Per-host foothold (repeat this block per host)
- **Host / IP:**
- **Got in via:** (exploit + CVE, or credential + how it was obtained in S4)
- **Payload / delivery:** (e.g. staged x64 meterpreter reverse_tcp / bind shell / psexec)
- **Shell type:** (meterpreter / TTY / raw / PowerShell)
- **Landed as (USER CONTEXT):**  <-- the field Session 6 starts from
- **Proof of execution:** (`getuid` / `id` / `whoami` output)
- **Reliability note:** (worked first try? crashed the service? needed a revert?)
- **SOC flip:** (what event this generated — 4688 / Sysmon 1 / Sysmon 3 / IDS)

## Chosen next step per host (reading into Session 6)
- If landed as SYSTEM/root: already maximal on this host — pivot / loot next.
- If landed low-priv: name the first two privilege-escalation checks you will run.

## Detection rule (attach)
Paste your Lab 9 reverse-shell rule and the one false-positive source it survives.
