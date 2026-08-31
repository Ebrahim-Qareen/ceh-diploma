# CEH Lab Design (current — edit in place, see ceh-lab-build)

Local VMs only. **Hypervisor: VMware Workstation Pro** (matches the source
material's own lab-build session).

## Topology

Single host-only network, all VMs on it, student's own laptop is the
"analyst workstation" (no separate DFIR VM — matches the ECIR lab's L6
decision, which held up well).

```
Host-only network: 192.168.56.0/24 (adjust if it collides with existing labs)
├── KALI-ATK01        — Kali Linux — attacker box
├── WIN7-TGT01         — Windows 7 (unpatched) — legacy Windows target (SMBv1, MS17-010)
├── WIN10-TGT01        — Windows 10 — modern hardened Windows target
├── WINSRV19-TGT01     — Windows Server 2019 — DOMAIN CONTROLLER for ceh.lab + target
└── METASPLOITABLE2    — Metasploitable2 — deliberately vulnerable Linux target
```

## The target zoo — why four different OSes

Session 3 teaches scanning and enumeration across **every OS type**, so the lab
deliberately spans the range. The same `nmap` command returns a different story on
each, and that contrast *is* the lesson:

| Target | OS era | What it teaches | Signature ports |
|---|---|---|---|
| **METASPLOITABLE2** | Linux, 2012 | Everything open — the richest possible enumeration; the classic textbook output | 21,22,23,25,53,80,111,139,445,2049,3306,5432,5900,6667,8180 |
| **WIN7-TGT01** | Windows, legacy | The Windows box where classic NetBIOS/SMB enumeration *still works* — SMBv1 on, MS17-010 vulnerable | 135,139,445,3389 (+ SMBv1) |
| **WIN10-TGT01** | Windows, modern | Hardened defaults — why the textbook SMB output is now empty | 135,139,445,3389 |
| **WINSRV19-TGT01** | Windows Server, DC | How a domain controller looks from a scan | 53,88,135,139,389,445,464,636,3268 |

**The teaching arc:** Metasploitable2 (Linux, ancient, wide open) → Windows 7 (legacy
Windows, SMBv1/EternalBlue) → Windows 10 (modern, hardened) → Server 2019 DC (the domain).
A student who scans all four learns that scanning is OS-agnostic but *results are not* —
and learns to read a machine's role from its port signature alone.

## Building Metasploitable2 (the primary example target)

Metasploitable2 is the machine every Session 3 example uses. It is a purpose-built
vulnerable Ubuntu 8.04 image — no install, just import.

1. **Download** the ~800 MB zip from Rapid7 (rapid7.com/products/metasploit/metasploitable-download)
   or SourceForge (sourceforge.net/projects/metasploitable/). It ships as a **VMDK** in a zip.
2. **Unzip**, then in VMware: *File → Open →* the `.vmx` (or *New VM → use an existing virtual disk*
   pointing at `Metasploitable.vmdk`).
3. **Set the network adapter to Host-only** (VMware) — the same host-only network as Kali.
4. **Power on**, log in `msfadmin` / `msfadmin`, run `ip a` (or `ifconfig`) and record the IP.
5. **Snapshot** as `baseline` before any lab touches it.

> **Safety — non-negotiable.** Metasploitable2 is intentionally, deeply insecure. Rapid7's own
> warning: *"the image should never be exposed to a hostile network."* **Host-only or isolated NAT
> only — never Bridged, never internet-facing.** An exposed Metasploitable2 is compromised in minutes.

Default credentials are `msfadmin` / `msfadmin` (also `user`/`user`, `service`/`service`) — lab-only,
throwaway, and never reused anywhere real.

## Session 3 practice range (added 2026-08-28 — downloaded and in use)

Three extra vulnerable machines the instructor downloaded, used as a **practice range** for Session 3:
students run the full scan→enumerate workflow on them for reps, beyond the four core teaching targets.
Not part of the graded labs; each drills one skill best. All run **host-only** under the same safety
rule as Metasploitable2 — **never Bridged, never internet-facing.**

| Machine | Source | OS | Signature scan / enum | Drills |
|---|---|---|---|---|
| **METASPLOITABLE3** | GitHub `rapid7/metasploitable3` | Windows Server 2008 R2 | 21,22,80,445,3306,3389,4848,8020,8080,8484,9200 + SNMP 161 (public); SMB "Star Wars" accounts (leia_organa, luke_skywalker, han_solo, vagrant…). **Scan with `-Pn`** — Windows Firewall drops ICMP + some ports | Modern Windows + web-service + SNMP + SMB-user enumeration |
| **KIOPTRIX 1** | VulnHub | Linux | 22 (OpenSSH 2.9p2), 80/443 (Apache 1.3.20 + mod_ssl 2.8.4 → OpenFuck), 111 rpcbind, 139 (Samba 2.2.1a → trans2open), 32768 | Version → known-exploit reading (feeds Session 4) |
| **STAPLER 1** | VulnHub | Linux | 21,22,53,80,139,445,666,3306, **12380 (only a full `-p-` finds it)**; `enum4linux` dumps a big user list (peter, RNunemaker, elly, kathy, tim…) | SMB user enumeration + banner intel + full-range discovery |

**Setup:** Kioptrix 1 and Stapler 1 are VulnHub `.ova` files — *File ▸ Import* into VMware, set adapter to
host-only, snapshot. Metasploitable3 is built from its Rapid7 GitHub repo (Packer/Vagrant) or a prebuilt
image; the Windows flavour is the one used here. Per-machine steps are in `setup_guide.md`.

Still-optional extras (not downloaded, self-study only): **Kioptrix 2–5**, **VulnOS 2 / SickOs 1.2**
(VulnHub, Linux, directory-discovery practice), and TryHackMe **Blue** (the Win7/EternalBlue arc, free,
in-browser). For **Active Directory** beyond our `ceh.lab` DC, **GOAD (Game of Active Directory)** is a
reference only — several VMs, too heavy for this diploma. Don't pre-build GOAD.

## VM specs (minimum, per source material's stated lab requirement)

| VM | OS | vCPU | RAM | Disk | Role |
|---|---|---|---|---|---|
| Host (student laptop) | any | 4 cores | 16 GB total | 100 GB free | Runs all VMs + is the analyst workstation |
| KALI-ATK01 | Kali Linux (latest) | 2 | 4 GB | 40 GB | Attacker tools |
| WIN7-TGT01 | Windows 7 (unpatched, SMBv1 on) | 1 | 2 GB | 40 GB | Target — the **legacy Windows** box: classic NetBIOS/SMB enumeration still works, MS17-010 (EternalBlue) vulnerable. The middle ground between Metasploitable2 (2012 Linux) and hardened Win10/2019 |
| WIN10-TGT01 | Windows 10 | 2 | 4 GB | 40 GB | Target — modern hardened Windows: auth, exploitation, privesc labs |
| WINSRV19-TGT01 | Windows Server 2019 | 2 | 4 GB | 40 GB | **Domain controller** (`ceh.lab`) + target — LDAP/SNMP/SMB enumeration (S3), NTLM/Kerberos/LLMNR (S4), privesc (S6) |
| METASPLOITABLE2 | Metasploitable2 | 1 | 1 GB | 10 GB | Target — classic vulnerable services |

## Optional — local recon target (`ceh-lab.local`) for offline use

> **Not required.** Session 2 active recon now runs against the **Acunetix vulnweb
> family** (`http://testphp.vulnweb.com` for directory/content/crawl/fingerprint,
> `vulnweb.com` for subdomain enumeration) — live, authorised, no setup. This local
> target is kept only as an **optional offline alternative** for classrooms without
> internet access.

If you want a fully offline target you control, `scripts/lab_recon_target.sh` stands
up a lightweight service **on KALI-ATK01 itself**, reachable only on the host-only
network:

- **DNS zone `ceh-lab.local`** served by `dnsmasq` — a handful of published hosts
  and several *unpublished* ones, so subdomain brute-force has something to find and
  misses return `NXDOMAIN` (the exact defender signal). Includes MX, SPF and DMARC
  TXT records for the DNS record-sweep lab.
- **Web root** served by `python3 -m http.server` — linked pages, a `robots.txt`
  naming hidden directories, plus unlinked directories that only directory
  brute-force finds. Access log exposed so students can read their own noise.

Stand it up with `scripts/lab_recon_target.sh up` (idempotent; `down` removes it,
`status` shows state). Zone transfer practice does **not** use this — it uses the
public `zonetransfer.me`, which is published for training; route tracing uses the
authorised `scanme.nmap.org`. No new VM, no persistent state, no secrets — everything
the target serves is deliberately fake.

## Session 3 target preparation (scanning & enumeration)

Session 3 is the first session that *touches* the targets, and several textbook
enumeration commands return **nothing** against a default modern Windows box. A class
where six commands in a row come back empty is a lost class, so three things are decided
here — two builds and one deliberate non-build.

### 1. `WINSRV19-TGT01` is promoted to a domain controller (`ceh.lab`)

Decided 2026-08-28. A standalone Windows Server has **no LDAP service at all**, so
`ldapsearch` and `windapsearch` have nothing to talk to and LDAP enumeration cannot be
taught honestly. Promoting the existing server:

- makes LDAP enumeration real in Session 3 (naming contexts, users, groups, computers),
- gives SMB enumeration a domain to report instead of a workgroup,
- **unblocks Session 4** (NTLM, Kerberos, LLMNR/NBT-NS poisoning) and **Session 6**
  (Mimikatz, token abuse), which `design/topic_map.md` had flagged as taught against
  standalone Windows only,
- closes the standing "no AD lab" open item in `topic_map.md`.

Cost: one promotion + reboot (~30–45 min) and one extra baseline snapshot. No new VM.

| Setting | Value |
|---|---|
| Domain (FQDN) | `ceh.lab` |
| NetBIOS name | `CEH` |
| Forest / domain functional level | Windows Server 2016 or later |
| DNS | Installed with the role (the DC is the lab's DNS server) |
| DSRM password | `<DSRM_PASSWORD>` — placeholder, set locally, never written in this repo |
| Domain admin | `<DOMAIN_ADMIN>` / `<DOMAIN_ADMIN_PASSWORD>` |

`WIN10-TGT01` is **joined to `ceh.lab`** so Sessions 4 and 6 have a domain member to
attack. Point its DNS at `WINSRV19-TGT01` first, or the join fails.

Seed the directory with a handful of throwaway users and groups so enumeration returns
something worth reading — `scripts/lab_s3_dc_setup.ps1` does this idempotently. No real
names, no real passwords.

### 2. SNMP is installed on `WINSRV19-TGT01`

SNMP is **not installed by default** on Windows Server, so `snmpwalk` and `onesixtyone`
teach nothing against a stock build. Install the SNMP Service feature and configure a
**read-only** community string (placeholder `<SNMP_COMMUNITY>`; use a guessable value
such as the classic default so the community-string brute-force lab has a target that
actually falls). `scripts/lab_s3_snmp_setup.ps1` does this.

This is deliberately a *weak* configuration — it exists to be found. Say that out loud in
class rather than letting students think a modern Windows box ships this way.

### 3. SMB policy is deliberately NOT loosened

SMBv1 and null sessions are **off by default** on Windows 10 and Server 2019 and later
(Microsoft: *"SMBv1 isn't installed by default in any edition of Windows 11 or Windows
Server 2019 and later versions"*). The tempting move is to re-enable SMBv1 so the classic
`enum4linux` output appears. **Don't.**

Teaching the contrast is worth more than a pre-broken target:

- **METASPLOITABLE2** — Samba from 2012, null sessions wide open. `enum4linux-ng` returns
  users, shares, groups and the password policy. This is what the textbook describes.
- **WIN10-TGT01 / WINSRV19-TGT01** — modern defaults. The same command returns almost
  nothing, and students learn *why*, and what still works (authenticated enumeration with
  `netexec`, RPC over an authenticated session, LDAP against the DC).

A student who has only ever seen the 2012 output will report "no SMB findings" on a real
engagement and be wrong. A student who has seen both knows the difference between
*hardened* and *not reachable*.

### Session 3 lab pre-flight (built into the session)

Session 3 opens with a five-minute check: all four VMs running, correct host-only
adapter, `ip a` / `ipconfig` recorded, and `nmap -sn` on the lab subnet returning all
three targets. Troubleshooting table lives in the session's guided lab.

## Session 4 target preparation (vulnerability analysis, authentication & password attacks)

Session 4 turns the Session 3 target profile into working credentials, and several of
today's attacks return **nothing** unless the `ceh.lab` domain and the workstations are
seeded for them. All automation is in `scripts/lab_s4_dc_setup.ps1` (a **sibling** to the
Session 3 scripts — it does not replace them). No credentials in the repo; every password is
prompted at run time. Take a third snapshot (`baseline-s4`) on the DC after this prep.

### 1. Kerberoasting needs a Service Principal Name (`-Stage Kerberoast`, on the DC)
The S3 seed created `svc_backup` but gave it no SPN and the shared lab password, so
`GetUserSPNs` finds nothing to roast. The S4 script:

- registers an SPN on `svc_backup` (`MSSQLSvc/win10-tgt01.ceh.lab:1433`) and sets it a
  **deliberately weak, wordlist-crackable** password → `GetUserSPNs` → `hashcat -m 13100`
  cracks in class;
- adds a second service account `svc_sql` with an SPN **and a strong random password** → the
  honest **"Kerberoast that never cracks"** case (a strong service password is the countermeasure).

### 2. Password spraying needs a shared weak password + a lockout policy (`-Stage SprayPolicy`, DC)
A spray finds nothing unless several accounts share one guessable password — but an *all-same*
seed is unrealistic. The S4 script sets **one weak password on a defined subset** (`a.fahmy`,
`n.gamal`, `h.rashad`) and gives `m.said` a **distinct strong** password, so the spray hits 3/5
and misses 1. It then enables a shallow **account-lockout policy (5 tries / 15-min window)** so
the "spraying is designed to stay *under* lockout" lesson — and the deliberate lockout-trip
failure case — are both real.

### 3. LLMNR/NBT-NS must still be on for the poisoning victim (`-Stage CheckLLMNR`, on Win10)
LLMNR + NBT-NS are **still enabled by default on Windows 10/11 as of 2026** (Microsoft is
"ramping down" toward mDNS but has not disabled them) — so `WIN10-TGT01` is a valid Responder
victim out of the box. The script **reports** their status (read-only) and prints the GPO
countermeasure. Teach disabling LLMNR (`EnableMulticast=0`) + NBT-NS as *the* fix — but do
**not** apply it in the lab, it kills the demo. Note mDNS is now also a Responder surface.

### 4. Crackable local accounts for the SAM lab (`-Stage LocalAccounts`, on Win7 **and** Win10)
Adds 2–3 **local** accounts (`labuser`, `helpdesk`, `svc_local`) with prompted weak passwords so
`secretsdump` → `hashcat -m 1000` (NTLM) has SAM hashes to crack. Local only, nothing domain.

### 5. Automated vulnerability scanner — Nessus Essentials (recommended) or Greenbone/GVM
- **Nessus Essentials** is the classroom primary (industry-standard; students meet it on the job).
  **Currency note: the free tier is now 5 IPs, not the old 16** — enough for our four targets
  (MSF2 · Win7 · Win10 · DC), leave Kali out of scope. Installs on Kali or a light host; the
  plugin download is large — do it **before** class. Run as a **guided demo**, not a per-student
  scan (every student downloading plugins is not worth the time).
- **Greenbone / GVM** (the OpenVAS engine lives inside GVM now) is the FOSS alternative — no
  licence, but a slow feed sync and heavier. The free THM `openvas` room covers it for self-study.

### 6. Kali wordlist
`rockyou.txt` ships **gzipped** on current Kali. Unpack it once before class:
`sudo gunzip -k /usr/share/wordlists/rockyou.txt.gz` (leaves the `.gz` in place with `-k`).


## Snapshot strategy

Take a clean "baseline" snapshot of every VM right after setup, before any
attack lab touches it. **Take a second baseline on `WINSRV19-TGT01` after the domain
promotion and SNMP install** (`baseline-dc`) — reverting to the pre-promotion snapshot
silently removes the domain and breaks every Session 3–6 AD lab. After the Session 4 prep (SPN, spray subset, lockout, local accounts) take a **third** snapshot `baseline-s4` — reverting past it removes the Kerberoast SPN and the spray passwords. Revert to baseline before each new session that
reuses a VM, so labs don't interfere with each other.

## Which session introduces what

| VM | First needed | Notes |
|---|---|---|
| KALI-ATK01 | Session 1 (build) | Used every session after |
| WIN10-TGT01 | Session 1 (build) | Target from Session 3 onward; **domain-joined to `ceh.lab`** before Session 3 |
| WINSRV19-TGT01 | Session 1 (build) | Target from Session 3 onward; **promoted to DC + SNMP installed** before Session 3 |
| WIN7-TGT01 | Session 1 (homework build) | Target from Session 3 onward — the legacy-Windows scanning/enumeration example; reused in Session 4/5 (EternalBlue) |
| METASPLOITABLE2 | Session 1 (build) | Target from Session 2 onward |
| `ceh-lab.local` (on Kali) | Session 2 (optional) | OPTIONAL offline recon target via `scripts/lab_recon_target.sh`; Session 2 uses the live Acunetix vulnweb sites by default — not a VM |

Sessions 6 (privesc/capstone) and 8 (web app) may need additional
deliberately-vulnerable targets (the source material's named CTF boxes —
Blue, Academy, DoubleTrouble, Blackpearl, and a DVWA/BWAPP web target).
Add those as needed when building those sessions — **don't pre-build VMs
a session doesn't use yet.**

## Credentials

Never written here or anywhere in this project tree. Use placeholders like
`<STUDENT_PASSWORD>` in any doc. Actual lab credentials go in a local file
outside `CEH_Course/`, excluded from git.

## Open items

- Confirm host-only subnet doesn't collide with anything else on student
  laptops.
- ~~No AD lab~~ **closed 2026-08-28** — `WINSRV19-TGT01` promoted to a domain
  controller for `ceh.lab` and `WIN10-TGT01` joined to it (see the Session 3
  section above). Sessions 4 and 6 no longer teach AD attacks against
  standalone Windows.
- DVWA/BWAPP and named CTF boxes (Blue, Academy, DoubleTrouble, Blackpearl)
  not yet added — add via `ceh-lab-build` when Sessions 6 and 8 are built.
