# CEH Lab — Student Setup Guide (current — edit in place, see ceh-lab-build)

Build your own lab locally. This is the guide referenced by every session.
Full specs and topology: `lab_design.md`. **Hypervisor: VMware Workstation Pro.**

> Do the Kali + Metasploitable2 builds before Session 1 if you can — Session 1
> class time is for verifying and fixing, then doing first contact, not sitting
> through installs. Windows targets can be built as Session 1 homework.

## Host requirements (your laptop)
| Resource | Minimum |
|---|---|
| CPU | 4 cores with virtualization (VT-x/AMD-V) enabled in BIOS |
| RAM | 16 GB total (you'll run 2-3 VMs at once) |
| Disk | 100 GB free |
| Software | VMware Workstation Pro |

**Verify first:** VMware ▸ Help ▸ About shows Workstation Pro; in BIOS,
virtualization is enabled (if VMware warns "VT-x disabled," fix it in BIOS).

## Network — create the host-only network once (do this first)
1. VMware ▸ Edit ▸ **Virtual Network Editor** (run as admin).
2. Add/confirm a **Host-only** network, e.g. `VMnet1`, subnet `192.168.56.0/24`.
   - If `192.168.56.0/24` collides with something already on your laptop, pick
     another private range and use it consistently everywhere.
3. Leave DHCP on (simplest) or note it; either way you'll read each VM's IP.
- **You know this worked when:** the host-only VMnet shows subnet
  `192.168.56.0` and status "connected."

> Every VM below uses **Host-only** on this VMnet. Never NAT/Bridged — the
> vulnerable targets must never reach the real network or internet.

## VM 1 — KALI-ATK01 (attacker)
1. Download the official **Kali Linux VMware image** (prebuilt) or the ISO.
2. Prebuilt: extract, open the `.vmx` in VMware. ISO: create a new VM (2 vCPU,
   4 GB RAM, 40 GB disk) and install.
3. VM ▸ Settings ▸ Network Adapter ▸ **Host-only (VMnet1)**.
4. Boot, log in, update once (needs temporary internet — see note below):
   ```
   sudo apt update && sudo apt -y full-upgrade
   ```
5. Confirm the core tools are present: `nmap`, `nc` (netcat), `netdiscover`.
   ```
   which nmap nc netdiscover
   ```
- **You know this worked when:** `ip a` shows a `192.168.56.x` address and the
  three tools resolve to paths.

> **Internet for updates:** to run `apt update` you may temporarily switch Kali
> to NAT, update, then switch **back to Host-only** before any lab. Targets stay
> Host-only always.

## VM 2 — METASPLOITABLE2 (vulnerable Linux target)
1. Download the official **Metasploitable2** image (a ready `.vmdk`).
2. Create a new VM ▸ "I will install the OS later" ▸ Linux ▸ use the existing
   Metasploitable2 disk (1 vCPU, 1 GB RAM, ~10 GB).
3. Network Adapter ▸ **Host-only (VMnet1)**.
4. Boot. Default login is the well-known Metasploitable2 account (see the image's
   own documentation — **do not** write credentials into any course file).
5. Get its IP:
   ```
   ifconfig
   ```
- **You know this worked when:** from Kali, `ping -c 3 <MSF2_IP>` gets replies
  and `sudo nmap -sn 192.168.56.0/24` lists the target as up.

## VM 3 — WIN10-TGT01 (Windows 10 target) — Session 1 homework
1. Get a Windows 10 evaluation VM (Microsoft's free eval / dev image) or install
   from ISO. 2 vCPU, 4 GB RAM, 40 GB.
2. Network Adapter ▸ **Host-only (VMnet1)**.
3. Boot, complete setup with a local account. Use a placeholder password you
   record **outside** this repo (`<STUDENT_PASSWORD>`).
4. Allow ping so discovery works later: enable "File and Printer Sharing
   (Echo Request - ICMPv4-In)" in Windows Defender Firewall, or for lab
   simplicity set the host-only adapter profile so ICMP is allowed.
- **You know this worked when:** from Kali, `ping -c 3 <WIN10_IP>` replies (after
  allowing ICMP) and the VM has a `192.168.56.x` address.

## VM 4 — WINSRV19-TGT01 (Windows Server 2019 target) — Session 1 homework
1. Get the Windows Server 2019 evaluation ISO (180-day eval). 2 vCPU, 4 GB RAM, 40 GB.
2. Install **Desktop Experience** edition. Network Adapter ▸ **Host-only (VMnet1)**.
3. Set a local admin password (placeholder, recorded outside the repo).
4. Allow ICMP as above so host discovery finds it.
- **You know this worked when:** the VM has a `192.168.56.x` address and Kali can
  ping it.
- **Note:** this is a standalone server for now — **no Active Directory domain is
  configured**. Whether/when an AD domain gets added is an open lab decision
  (see `lab_design.md` ▸ Open items); it is **not** required for Session 1.

## Snapshots (do this for EVERY VM after it's built)
1. Power the VM to a clean, working state.
2. VM ▸ Snapshot ▸ **Take Snapshot** ▸ name it `baseline-clean`.
3. Before each session, revert to `baseline-clean` so old labs don't interfere.
- **You know this worked when:** the snapshot appears in VM ▸ Snapshot ▸
  Snapshot Manager, and after making a test file and reverting, the file is gone.

## Credentials
Never write real passwords here or anywhere in `CEH_Course/`. Keep a local
`lab_credentials.txt` **outside** this folder. Use `<STUDENT_PASSWORD>` etc. in
any note you keep in the repo.

## Troubleshooting (failure modes actually hit while building)
| Symptom | Likely cause | Fix |
|---|---|---|
| Target not found by `nmap -sn` | VM on NAT/Bridged, not Host-only | Set adapter to Host-only (VMnet1), re-check `ip a`/`ifconfig` |
| VMs get 192.168.x but can't ping each other | Different host-only VMnets, or Windows firewall blocks ICMP | Put all on the same VMnet; allow ICMPv4 echo on Windows |
| "VT-x is disabled" on VM start | Virtualization off in BIOS | Enable VT-x/AMD-V in BIOS/UEFI |
| Subnet collision, odd IPs | 192.168.56.0/24 already used on host | Change host-only subnet in Virtual Network Editor, reuse it everywhere |
| Kali can't `apt update` | Kali is on Host-only (by design) | Temporarily switch to NAT, update, switch back to Host-only |
| Windows target invisible to discovery | ICMP blocked by default | Enable "File and Printer Sharing (Echo Request - ICMPv4-In)" |
