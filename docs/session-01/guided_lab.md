---
session: 1
title: Foundations, Lab Build & First Contact
doc: Guided Lab
---

# Session 1 — Guided Lab: Build the Lab & Make First Contact

## Objective
By the end of this lab you can prove you can:
1. Bring up an isolated host-only attack lab (Kali + Metasploitable2).
2. Take and revert a baseline snapshot.
3. Discover a live target and grab at least 3 service banners from it — and record the evidence.

## Environment / VMs required
See `labs/setup_guide.md` for full build steps and `labs/lab_design.md` for specs.
- **KALI-ATK01** (attacker) — required in class.
- **METASPLOITABLE2** (target) — required in class.
- **VMware host-only network** (e.g. `192.168.56.0/24`).
- WIN10-TGT01 / WINSRV19-TGT01 — built as homework, **not** needed for this lab.

> You should arrive with the VMs already built from the setup guide. This class block is to **verify and fix**, then do first contact — not to sit through installs.

## Part A — Verify the lab (host-only + connectivity)

**Step 1.** On the VMware host, confirm both VMs' network adapter = **Host-only**.
*Expected:* both VMs on the same host-only adapter, none set to NAT/Bridged.

**Step 2.** Boot KALI-ATK01. Open a terminal:
```
ip a
```
*Expected:* an interface with a `192.168.56.x` address (your host-only subnet).

**Step 3.** Boot METASPLOITABLE2. Log in and get its IP:
```
ifconfig
```
*Expected:* a `192.168.56.x` address. Note it as `<MSF2_IP>`.

**Step 4.** From Kali, confirm the two can talk:
```
ping -c 3 <MSF2_IP>
```
*Expected:* 3 replies, TTL ~64.

## Part B — Snapshot discipline

**Step 5.** In VMware, take a snapshot of **each** VM named `baseline-clean` (VM ▸ Snapshot ▸ Take Snapshot).
*Expected:* snapshot appears in the snapshot manager, dated today.

**Step 6.** (Instructor-led demo, students follow) On Metasploitable2 create a throwaway file, then revert:
```
touch /tmp/iwillbegone
```
Revert the VM to `baseline-clean` in VMware, reboot, and check:
```
ls /tmp/iwillbegone
```
*Expected:* `No such file or directory` — the revert wiped it. This is why we snapshot.

## Part C — First contact (host discovery + banner grabbing)

**Step 7.** Host discovery — who is alive on the network?
```
sudo nmap -sn <CIDR>       # e.g. 192.168.56.0/24
```
*Expected:* Metasploitable2 listed as "Host is up" with IP + MAC (VMware OUI).

**Step 8.** Light service/version sweep (this is a preview — full scanning is Session 3):
```
nmap -sV --top-ports 20 <MSF2_IP>
```
*Expected:* open ports with versions, e.g. `21/tcp vsftpd 2.3.4`, `22/tcp OpenSSH 4.7p1`, `23/tcp telnet`, `25/tcp Postfix smtpd`, `80/tcp Apache`, `445/tcp Samba`.

**Step 9.** Manual banner grabbing — connect by hand and read what the service says:
```
nc -nv <MSF2_IP> 21
nc -nv <MSF2_IP> 22
nc -nv <MSF2_IP> 25
```
*Expected banners:*
- `220 (vsFTPd 2.3.4)`
- `SSH-2.0-OpenSSH_4.7p1 Debian-8ubuntu1`
- `220 metasploitable.localdomain ESMTP Postfix (Ubuntu)`

Press `Ctrl+C` to exit each.

**Step 10.** Record evidence: copy at least **3 banners verbatim** and the `nmap -sV` output into your lab report. Note the software + version for each — those versions are what you'll research for vulnerabilities in Session 3.

## Success check (show your instructor)
- [ ] Kali and Metasploitable2 both on host-only, can ping each other.
- [ ] `baseline-clean` snapshot exists on both VMs; you demonstrated a revert.
- [ ] `nmap -sn` found the target; `nmap -sV` listed services with versions.
- [ ] At least 3 service banners captured verbatim in your lab report.

## Common mistakes
- **Adapter set to NAT/Bridged** — target becomes reachable from the real network (unsafe) or Kali can't see it. Fix: set both to Host-only.
- **Subnet collision** — host-only `192.168.56.0/24` clashes with an existing network on the laptop; VMs get odd IPs. Fix: change the host-only subnet in VMware Virtual Network Editor and re-check.
- **Firewall on target confuses discovery** — Metasploitable2 has none, so if a host "isn't up," it's almost always the adapter or subnet, not a firewall.
- **Forgetting the snapshot before labs** — you'll pollute the target across sessions. Always snapshot at `baseline-clean` first.
- **`nc` hangs and looks frozen** — that's a connected banner session; it's working. `Ctrl+C` to exit.
- **Running scans outside the lab** — out of scope. Only ever touch `<CIDR>` / `<MSF2_IP>`.
