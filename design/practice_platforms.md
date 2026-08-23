# Practice Platforms — Verified Room Reference

> Every entry below was **fetched live and confirmed** (exact name, access tier,
> duration) on 2026-08-23. Do not link a room from memory — tiers change and slugs die.
> Re-verify anything older than ~3 months before putting it in front of students.

## Platform comparison

| Platform | Best at | Free-tier reality | When in this course |
|---|---|---|---|
| **TryHackMe** | Guided rooms with in-browser machines. Closest match to this course's sequence. | 650+ genuinely free rooms + a limited daily browser-VM allowance. Most rooms *inside structured learning paths* are Premium. | Throughout — primary platform |
| **OverTheWire** | Raw Linux/CLI skill as a puzzle ladder. No hand-holding. | **Entirely free, no account.** Best value available. | From Session 1 |
| **Hack The Box** | Realistic unguided machines, closer to a real engagement. | Free tier = Starting Point Tier 0 + rotating active machines. | **From Session 5** — earlier it just frustrates students |
| **picoCTF** | CTF challenges (crypto, forensics, web, rev) + permanent picoGym. | Free. | Optional — forensics/crypto side |

## Verified rooms

### Networking (Session 1 · prereq for Session 3)
| Room | Slug | Tier | Time |
|---|---|---|---|
| What is Networking? | `whatisnetworking` | Free | ~30 min |
| Intro to LAN | `introtolan` | Free | ~15 min |
| OSI Model | `osimodelzi` | **Premium** | ~30 min |
| Packets & Frames | `packetsframes` | **Premium** | ~30 min |

⚠️ `osimodelfun` **does not exist** — dead slug, do not use.

### Operating systems (Session 1)
| Room | Slug / URL | Tier | Time |
|---|---|---|---|
| Linux Fundamentals Part 1 | `linuxfundamentalspart1` | Free | ~20 min |
| Windows Fundamentals 1 | `windowsfundamentals1xbx` | Free | ~30 min |
| **OverTheWire Bandit** | `overthewire.org/wargames/bandit/` | **Free, no account** | levels 0–15 ≈ 2 h |

**Bandit is the single highest-value recommendation in the course.** It teaches the
exact skill students are weakest at — finding something on a box you did not configure —
with no signup, no VM, no subscription.

### Web & identity (Session 1 · prereq for Session 8)
| Room | Slug | Tier | Time |
|---|---|---|---|
| HTTP in Detail | `httpindetail` | Free | ~30 min |
| Web Application Basics | `webapplicationbasics` | Free | ~120 min |

### Frameworks (Session 1)
| Resource | URL | Tier |
|---|---|---|
| ATT&CK matrix | `attack.mitre.org` | Free, official |
| ATT&CK Navigator | `mitre-attack.github.io/attack-navigator/` | Free, official |
| Cyber Kill Chain | THM `cyberkillchain` | **Premium** (~50 min, medium) |
| MITRE | THM `mitre` | **Premium** (~60 min, medium; requires Kill Chain first) |

### Virtualization / careers (Session 1)
| Room | Slug | Tier | Time |
|---|---|---|---|
| Virtualization and Containers | `virtualizationandcontainers` | **Premium** | ~60 min |
| Careers in Cyber | `careersincyber` | Free | ~30 min |

### Scanning (Session 1 lab · Session 3)
| Room | Slug | Tier | Time |
|---|---|---|---|
| **Blue** (first full compromise) | `blue` | **Free** | ~30 min, easy |
| Nmap Live Host Discovery | `nmap01` | **Premium** | ~60 min |
| Nmap Basic Port Scans | `nmap02` | **Premium** | ~60 min |
| Nmap Advanced Port Scans | `nmap03` | **Premium** | ~60 min |
| Nmap: The Basics | `nmap` | **Premium** | ~60 min |
| RP: Nmap | `rpnmap` | **Premium** | — |

`Blue` is the motivation room: scan → find MS17-010 → exploit → SYSTEM. It runs the
exact arc Sessions 1–5 build. Free, and worth assigning early precisely because it
will feel like magic before students understand it.

### Candidates for Session 2 (footprinting/recon) — NOT YET VERIFIED
Verify each before use: `passiverecon`, `activerecon`, `googledorking`,
`ohsint`, `searchlightosint`, `redteamrecon`, `shodan`, `dnsindetail`,
`contentdiscovery`, `subdomainenumeration`, `sublist3r`.

## Standing rule for students

Every one of these platforms hands the learner a target **and** written authorization
to attack it. That authorization does not travel. This warning appears on every page
carrying a practice block, and in full on the practice-plan page.
