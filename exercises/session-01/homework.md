---
session: 1
title: Foundations, Lab Build & First Contact
doc: Homework
---

# Session 1 — Homework

> **Note on scope (changed 2026-08-23):** the VM build is now homework, not class
> work. Session 1 class time covers virtualization, lab design and snapshot
> discipline as theory, then spends its hands-on block on first contact. Students
> who did not have VMs ready in class watched that block and repeat it themselves
> here — nobody is exempt from personally running the commands.

## Tasks

1. **Check virtualization support — do this first.**
   Task Manager → Performance → CPU → confirm `Virtualization: Enabled`. If it
   says Disabled, enable Intel VT-x / AMD-V in BIOS/UEFI and re-check. If Hyper-V,
   WSL2 or Docker Desktop is installed, be aware they can hold the virtualization
   extensions and block VMware.
   **Report immediately if your BIOS is locked by an employer policy** — that needs
   an alternative arrangement and cannot wait until Session 3.

2. **Build KALI-ATK01 and METASPLOITABLE2** on the VMnet1 host-only network per
   `labs/setup_guide.md`. Set the network adapter to host-only **before the first
   power-on** of Metasploitable2.

3. **Take `baseline-clean` snapshots** of both machines while they are powered
   off. Prove the revert works: boot Kali, `touch /tmp/snapshot-test`, revert, and
   confirm the file is gone.

4. **Run first contact yourself** against your own Metasploitable2 — the full
   sequence from class:
   - `ip a` — confirm you are on `192.168.56.x`
   - `sudo nmap -sn 192.168.56.0/24` — find the target
   - `ping -c 3 <MSF2_IP>` — confirm reachability, note the TTL
   - `nmap -sV --top-ports 20 <MSF2_IP>` — open ports with versions
   - `nc -nv <MSF2_IP> 21`, `22`, `25` — at least three raw banners

5. **Build WIN10-TGT01 and WINSRV19-TGT01** on the same host-only network with
   `baseline-clean` snapshots. These are targets from Session 3 — start now, the
   Windows installs take real time.

6. **Write the Session 1 lab report** using `lab_report_template.md`.

## Deliverables

- Completed `lab_report.md` (from the template), covering tasks 1–5.
- Screenshot showing `Virtualization: Enabled`.
- Screenshot of Snapshot Manager on Kali and Metasploitable2 showing `baseline-clean`.
- Your Rules-of-Engagement page written in the class activity.

## Grading rubric (pass / needs-review)

| Criterion | Pass |
|---|---|
| Lab works | Kali + Metasploitable2 + both Windows targets on host-only, all four with `baseline-clean` snapshots |
| Snapshot discipline | Revert was tested and the result recorded, not just "snapshot taken" |
| Evidence | ≥3 verbatim banners + host discovery and `-sV` output, matching the student's own IPs |
| Honesty / depth | "What went wrong" is filled with a real issue and its fix — not left blank |
| Understanding | "What I learned" and the SOC-angle line are specific to what they actually did |

Needs-review = any criterion missing; the student revises and resubmits. No numeric
grade — the quiz is the graded assessment.
