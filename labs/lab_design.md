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
├── WIN10-TGT01        — Windows 10 — target
├── WINSRV19-TGT01     — Windows Server 2019 — target
└── METASPLOITABLE2    — Metasploitable2 — deliberately vulnerable target
```

## VM specs (minimum, per source material's stated lab requirement)

| VM | OS | vCPU | RAM | Disk | Role |
|---|---|---|---|---|---|
| Host (student laptop) | any | 4 cores | 16 GB total | 100 GB free | Runs all VMs + is the analyst workstation |
| KALI-ATK01 | Kali Linux (latest) | 2 | 4 GB | 40 GB | Attacker tools |
| WIN10-TGT01 | Windows 10 | 2 | 4 GB | 40 GB | Target — auth, exploitation, privesc labs |
| WINSRV19-TGT01 | Windows Server 2019 | 2 | 4 GB | 40 GB | Target — enumeration, AD-adjacent services |
| METASPLOITABLE2 | Metasploitable2 | 1 | 1 GB | 10 GB | Target — classic vulnerable services |

## Snapshot strategy

Take a clean "baseline" snapshot of every VM right after setup, before any
attack lab touches it. Revert to baseline before each new session that
reuses a VM, so labs don't interfere with each other.

## Which session introduces what

| VM | First needed | Notes |
|---|---|---|
| KALI-ATK01 | Session 1 (build) | Used every session after |
| WIN10-TGT01 | Session 1 (build) | Target from Session 3 onward |
| WINSRV19-TGT01 | Session 1 (build) | Target from Session 3 onward |
| METASPLOITABLE2 | Session 1 (build) | Target from Session 2 onward |

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
- DVWA/BWAPP and named CTF boxes (Blue, Academy, DoubleTrouble, Blackpearl)
  not yet added — add via `ceh-lab-build` when Sessions 6 and 8 are built.
