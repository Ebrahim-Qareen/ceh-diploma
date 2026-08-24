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

### Footprinting & Reconnaissance (Session 2) — verified live 2026-08-24

Verified by fetching each room logged-out (a premium room states *"only available for
Premium or Max subscribers"*; reading a room while logged in proves nothing about tier).

| Room | Slug | Tier | Time | Use |
|---|---|---|---|---|
| **Passive Reconnaissance** | `passiverecon` | **Free** | ~60 min · easy | **Best free companion to S2.** whois→RDAP, dig vs nslookup + TTL, DNSDumpster, crt.sh `%.domain`, Shodan. Uses `tryhackme.com` as its example target |
| **Active Reconnaissance** | `activerecon` | **Free** | ~60 min · easy | The active half: browser dev tools, ping/TTL, traceroute, telnet, netcat. Do before Session 3 |
| **Google Dorking** | `googledorking` | **Free** | ~45 min · easy | Crawler→index→robots→sitemap model, then operators. Note: still teaches `cache:` (retired by Google Sep 2024). Legal dork target: `googledorking.cmnatic.co.uk` |
| **DNS in Detail** | `dnsindetail` | **Free** | ~45 min · easy | Hierarchy + record types; prereq for the DNS-recon lab |
| **Shodan.io** | `shodan` | **Free** | ~45 min · easy | ASN pivoting, Shodan dorking, Monitor. Honest that CVE search / some features need a paid account |
| **OhSINT** | `ohsint` | **Free** | ~60 min · easy | Pure OSINT challenge — how much one image leaks. Homework |
| **Sakura Room** | `sakura` | **Free** | ~45 min · easy | Best free OSINT investigation on the platform. Homework |
| **Searchlight — IMINT** | `searchlightosint` | **Free** | — · easy | Image-intelligence OSINT. Homework |
| Red Team Recon | `redteamrecon` | **Premium** | ~120 min | Recon-ng + Maltego. Excellent; needs subscription — optional, not required |
| Content Discovery | `contentdiscovery` | **Premium** | ~30 min | Directory brute-force — Lab 7 covers it free |
| Subdomain Enumeration | `subdomainenumeration` | **Premium** | ~30 min | Subdomain brute-force — Lab 7 covers it free |
| WebOSINT | `webosint` | **Premium** | — | — |

⚠️ **Dead slugs (do not use):** `sublist3r` and `windowsuserfundamentals` both return
"the room you tried to access doesn't exist."

**Nmap rooms** (`nmap01`–`nmap03`, `nmap`) are **Premium** — see the Scanning section;
they belong to Session 3, not Session 2.

**Non-THM targets used in Session 2 labs (verified authorised):**
- `zonetransfer.me` (DigiNinja) — published for zone-transfer training. NS: `nsztm1.digi.ninja`, `nsztm2.digi.ninja`.
- `scanme.nmap.org` — "authorized to scan… a few scans in a day is fine."
- `crt.sh`, `sitereport.netcraft.com`, `exploit-db.com/google-hacking-database` — free, public, no account for basic use (crt.sh is frequently 502 — have the `curl|jq` fallback and `subfinder` ready).

## Standing rule for students

Every one of these platforms hands the learner a target **and** written authorization
to attack it. That authorization does not travel. This warning appears on every page
carrying a practice block, and in full on the practice-plan page.
