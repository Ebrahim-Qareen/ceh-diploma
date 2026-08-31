# Practice Platforms — Verified Room Reference

> Every entry below was **fetched live and confirmed** (exact name, access tier,
> duration) on 2026-08-23, with the Session 2 set added 2026-08-24 and the Session 3
> set added — and the Session 1 Nmap tiers corrected — on 2026-08-28. Do not link a room from memory — tiers change and slugs die.
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

### Scanning & Enumeration (Session 3) — re-verified 2026-08-28

> ⚠️ **This section corrects the Session 1 record.** Session 1 listed the whole Nmap
> family as Premium. That was wrong for three of them. See the verification method below.

**Verification method (better than the logged-out page scrape):**
`https://tryhackme.com/api/v2/rooms/details?roomCode=<slug>` returns the authoritative
tier fields — `freeToUse: true` + `displaySubscriptionTier: null` = **free**;
`freeToUse: false` + `displaySubscriptionTier: "premium"` = **premium**;
`{"status":"fail","message":"This room is private."}` = **unusable**. The logged-out
HTML page sometimes returns `{"status":"error","message":"Unauthorized"}` for free rooms
(bot protection), so the page alone gives false premium readings.

#### Free — the Session 3 path

| Room | Slug | Tier | Time · difficulty | Why this room |
|---|---|---|---|---|
| **Nmap** | `furthernmap` | **Free** ✅ | ~50 min · easy | **The single best free companion to Session 3.** 15 tasks: switches, scan-type overview, TCP connect, SYN, UDP, NULL/FIN/Xmas, ICMP network scanning, NSE overview/usage/searching, firewall evasion, practical. Covers our whole scanning half |
| **Nmap Basic Port Scans** | `nmap02` | **Free** ✅ | ~120 min · easy | Depth on TCP connect / SYN / UDP + TCP flags + fine-tuning scope and performance. Do after `furthernmap` |
| **Network Services** | `networkservices` | **Free** ✅ | ~60 min · easy | The enumeration half: SMB (enum4linux, smbclient), Telnet, FTP + hydra. Maps directly to our Lab 4 and Lab 6 |
| **Network Services 2** | `networkservices2` | **Free** ✅ | ~60 min · easy | NFS, SMTP and MySQL enumeration — the services our Lab 6 sweeps on Metasploitable2 |
| **RustScan** | `rustscan` | **Free** ✅ | ~45 min · easy | The breadth-then-depth workflow we teach: rustscan finds ports fast, hands off to nmap |
| **Vulnversity** | `vulnversity` | **Free** ✅ | ~45 min · easy | Nmap recon → service enumeration → foothold. The first room that uses scanning for something |
| **Basic Pentesting** | `basicpentestingjt` | **Free** ✅ | ~45 min · easy (challenge) | SMB + service enumeration with no walkthrough hand-holding. Good homework |
| **Blue** | `blue` | **Free** ✅ | ~30 min · easy | The motivation room: scan → find MS17-010 → exploit → SYSTEM. Runs the exact arc Sessions 1–5 build |

#### Premium / unusable — do not link as required work

| Room | Slug | Status | Note |
|---|---|---|---|
| Nmap: The Basics | `nmap` | **Premium** | `freeToUse:false`, tier `premium` |
| Nmap Advanced Port Scans | `nmap03` | **Premium** | Fragmentation, decoys, spoofing — our S3 evasion preview covers the concepts free |
| Nmap Post Port Scans | `nmap04` | **Premium** | — |
| Nmap Live Host Discovery | `nmap01` | ⚠️ **Conflicting** | API reports `freeToUse:true` (medium, ~75 min) but the logged-out page returns `Unauthorized`. **Re-check on the day before assigning.** Not linked as required |
| Enumeration | `enumeration` | **Private** | `{"status":"fail","message":"This room is private."}` |
| RP: Nmap | `rpnmap` | **Private** | Same response |
| Wireshark 101 | `wireshark101` | **Premium** | So the Wireshark work in Session 3 happens **in our own lab**, not in a THM room |
| Wireshark: The Basics | `wiresharkthebasics` | **Premium** | ~60 min. Same conclusion |

⚠️ **Dead slug (do not use):** `nmapthebasics` — returns the "room you tried to access
doesn't exist" search page.

**Also re-confirmed free (Session 1 networking prereqs, still valid):**
`whatisnetworking` (info · 30 min) · `introtolan` (info · 15 min).

**Non-THM targets used in Session 3 labs:**
- **Tier A — the local host-only lab** (`KALI-ATK01` → `METASPLOITABLE2`, `WIN10-TGT01`,
  `WINSRV19-TGT01`). The only place a full subnet sweep, every scan type, UDP scans and
  real SMB/SNMP/LDAP/NFS enumeration are legal. Every hands-on block runs here.
- `scanme.nmap.org` — Nmap's own host. Verified live 2026-08-28, still says
  *"You are authorized to scan this machine with Nmap or other port scanners"* and
  *"A few scans in a day is fine."* **Rate-limit it and say so on the page.**
- `testphp.vulnweb.com` / vulnweb siblings, `demo.testfire.net` — Acunetix/HCL test
  targets, used only for the LAN-vs-internet contrast. Both were unreachable to our
  fetcher during this build (vulnweb robots timeout, testfire expired certificate) —
  treat as flaky and always have the lab fallback, exactly as Session 2 teaches.

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

**Nmap rooms** belong to Session 3, not Session 2 — and the tiers were re-verified on
2026-08-28: `furthernmap` and `nmap02` are **free**, not premium. See the Scanning &
Enumeration (Session 3) section above.

**Non-THM targets used in Session 2 labs (verified authorised):**
- `zonetransfer.me` (DigiNinja) — published for zone-transfer training. NS: `nsztm1.digi.ninja`, `nsztm2.digi.ninja`.
- `scanme.nmap.org` — "authorized to scan… a few scans in a day is fine."
- `crt.sh`, `sitereport.netcraft.com`, `exploit-db.com/google-hacking-database` — free, public, no account for basic use (crt.sh is frequently 502 — have the `curl|jq` fallback and `subfinder` ready).

### Vulnerability Analysis & Password Attacks (Session 4) — verified 2026-08-28

> Verified via the API method (`https://tryhackme.com/api/v2/rooms/details?roomCode=<slug>`): `freeToUse:true`
> + `displaySubscriptionTier:null` = free; `freeToUse:false` = premium/max; `"This room is private."` = unusable.

#### Free — the Session 4 path

| Room | Slug | Tier | Time · difficulty | Why this room |
|---|---|---|---|---|
| **Vulnerabilities 101** | `vulnerabilities101` | **Free** ✅ | ~20 min · easy | CVE, CVSS and vuln research — the vuln-analysis half. Do it first. |
| **OpenVAS** | `openvas` | **Free** ✅ | ~45 min · easy | Automated scanning with Greenbone/GVM — the free stand-in for the Nessus demo (the `nessus` room is private). |
| **Crack the Hash** | `crackthehash` | **Free** ✅ | ~45 min · easy | Identify + crack every common hash type (hashcat + John). Pure reps on the cracking pipeline. |
| **Hydra** | `hydra` | **Free** ✅ | ~45 min · easy | Online brute-force against real services — the hydra block, hands-on. |
| **Attacktive Directory** | `attacktivedirectory` | **Free** ✅ | ~75 min · medium | **The gem — and it's free.** kerbrute user-enum → GetNPUsers (AS-REP) → GetUserSPNs (Kerberoast) → secretsdump → evil-winrm: the exact Labs 5–6 chain against a fresh domain. |
| **Network Services 2** | `networkservices2` | **Free** ✅ | ~60 min · easy | Service enumeration + hydra (carryover from S3) — good warm-up for the online-attack half. |

#### Premium / private / dead — do not link as required work

| Room | Slug | Status | Note |
|---|---|---|---|
| Hashing - Crypto 101 | `hashingcrypto101` | **Premium** | `freeToUse:false`, tier `premium` |
| John the Ripper: The Basics | `johntheripperbasics` | **Premium** | `johntheripper0` is a **dead slug** (404) |
| Password Attacks | `passwordattacks` | **Max** | tier `max` (hard, ~120 min) |
| Attacking Kerberos | `attackingkerberos` | **Premium** | Kerberoast/AS-REP walkthrough — our local DC covers it free |
| Nessus | `nessus` | **Private** | `{"status":"fail","message":"This room is private."}` |
| Responder | `responder` | **Private** | Same response |
| RP: Vulnerability Scanning | `rpvulnerabilityscanning` | **Dead** | 404 |
| Holo | `holo` | ⚠️ **Unreliable / premium** | API returns inconsistent data (title "Throwback"); a heavy premium red-team network — out of scope, not linked |

**Honest framing:** the strongest *dedicated* AD-credential rooms (Attacking Kerberos, Password Attacks,
Breaching AD, Holo) are mostly premium. **Attacktive Directory being free is the exception** — and the local
`ceh.lab` DC is exactly why we don't depend on paid rooms for this session.

**Non-THM targets used in Session 4 labs:**
- **Tier A — the local host-only lab** (`KALI-ATK01` → `METASPLOITABLE2`, `WIN7-TGT01`, `WIN10-TGT01`, the
  `ceh.lab` DC `WINSRV19-TGT01`). The only lawful place to crack, spray, poison and roast. Every hands-on block runs here.
- **Practice range (from S3):** Metasploitable 3 (weak "Star Wars" accounts → spray + SAM crack), Stapler 1
  (enum4linux user list → spray list), Kioptrix 1 (mod_ssl/Samba versions → CVE→exploit reading).
- **Research sources (free, no account for basic use):** `nvd.nist.gov`, `cve.org`, `exploit-db.com`,
  `first.org/cvss/calculator`.


## Standing rule for students

Every one of these platforms hands the learner a target **and** written authorization
to attack it. That authorization does not travel. This warning appears on every page
carrying a practice block, and in full on the practice-plan page.
