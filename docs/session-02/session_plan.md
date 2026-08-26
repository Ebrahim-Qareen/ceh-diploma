---
session: 2
title: Footprinting & Reconnaissance
module_ref: Module 2 pt2 (footprinting & recon techniques)
duration: 4 hours
---

# Session 2 — Session Plan

## Title
Footprinting & Reconnaissance

## Module reference
- Module 2 pt2 — Footprinting and Reconnaissance techniques (passive + active).
  Part 1 of Module 2 (the lab build) was delivered in Session 1.

## Learning objectives
By the end of this session, students will be able to:
1. **Distinguish** passive from active reconnaissance by whether a packet reaches the target, and state the authorization each requires.
2. **Apply** the reconnaissance funnel — narrowing from everything public down to a ranked target list — and place any recon tool at its correct stage.
3. **Use** search-engine operators and the GHDB to find a target's unintentionally-published data (T1593/T1594).
4. **Query** open technical databases — Shodan, Netcraft, certificate transparency — to map a target's estate without contacting it (T1596).
5. **Read** a WHOIS/RDAP record and DNS records (incl. SPF/DMARC) as intelligence, and explain the 2025 WHOIS→RDAP transition.
6. **Derive** an organisation's email/username convention from one confirmed address plus public data (T1589), and explain how it feeds Session 4.
7. **Perform** active DNS reconnaissance including a live zone transfer, and route tracing and web crawling against authorised targets (T1590/T1595).
8. **Distinguish** subdomain from subdirectory brute-force, run both against authorised targets, and read the status codes.
9. **Assemble** the findings into a ranked recon report — the session deliverable and Session 3's input.
10. **State**, for each technique, the SOC detection angle (or explain why it is undetectable) and the countermeasure.

## Time distribution (240 min)

| Block | Activity | Format | Min |
|---|---|---|---|
| Where we left off + funnel + engagement | Recall, recon funnel, target & scope, ATT&CK TA0043 | Theory (interactive) | 15 |
| Search engines & dorks | Crawler/index model, operators, GHDB, robots.txt | Theory (interactive) | 7 |
| **Lab 1** | Dork the target — SERP, documents, GHDB, the pivot | Hands-on (everyone) | 14 |
| Shodan · Netcraft · crt.sh | Banner census, hosting history, certificate transparency | Theory (interactive) | 14 |
| **Lab 2** | The web-services sweep — resolve, pivot, enumerate, merge | Hands-on (everyone) | 16 |
| WHOIS→RDAP · people & email recon | Registration data, conventions, the psychology | Theory (interactive) | 13 |
| **Lab 3** | Registration data + derive the email convention | Hands-on (everyone) | 10 |
| Break | — | — | 10 |
| theHarvester · subdomains · stack | Aggregation, passive vs brute-force, fingerprinting, tool rot | Theory (interactive) | 16 |
| **Lab 4** | Automate the sweep + fingerprint a real target | Hands-on (everyone) | 16 |
| Crossing the line · DNS & zone transfer | Passive→active, DNS record map, AXFR misconfiguration | Theory (interactive + animated) | 13 |
| **Lab 5** | DNS record sweep + a live zone transfer | Hands-on (everyone) | 16 |
| Route tracing & crawling | TTL trick, Photon, tool rot | Theory (interactive) | 8 |
| **Lab 6** | Traceroute + robots.txt + crawl a real target | Hands-on (everyone) | 10 |
| Subdomain vs subdirectory | Two namespaces, tool-state table | Theory (interactive) | 7 |
| **Lab 7** | Both brute-forces + smart-vs-generic wordlist | Hands-on (everyone) | 16 |
| Countermeasures | The three-layer defensive doctrine | Defender (interactive) | 7 |
| **Lab 8** | Assemble the ranked recon report | Hands-on (everyone) | 14 |
| Into Session 3 + wrap | Bridge, quiz, practice plan, homework | Wrap-up | 16 |

**Total: 240 min.** Hands-on across 8 blocks = **112 min (47%)**.

### If you run over
The theory blocks compress before the labs do — the labs are the session. In order, trim:
1. Route tracing & crawling theory (8→5) — the lab carries it.
2. The practice-plan page — run it as a link-only sign-off.
3. Merge the "crossing the line" page into the DNS page's intro if the room is moving fast.
Do **not** cut a hands-on block to save time; drop a theory page's depth instead and point at the
knowledge_base file for the rest.

## Delivery notes
- **One target, followed all the way down.** `tryhackme.com` carries every passive block, so students
  watch one picture assemble rather than seeing twelve disconnected demos. Active techniques switch to
  authorised stand-ins (`zonetransfer.me`, `scanme.nmap.org`, the Acunetix vulnweb sites) — say the authorization
  basis out loud each time.
- **Method before syntax.** Every tool page gives what-it-is / why-it-exists / **the method** / real
  syntax / how-to-read-the-output / what-it-feeds / SOC flip. A student who memorises
  `theHarvester -d target -b all` has learned nothing; teach the decision, then the command.
- **The passive/active line is the spine.** The session is deliberately built so the free, undetectable
  work comes first and every active technique is justified by what passive recon already found.
- **Currency corrections matter.** Three things the courseware gets wrong are called out on the page and
  are worth stressing: WHOIS→RDAP (Jan 2025), Google `cache:` retired (Sep 2024), and tool rot
  (Sublist3r/Photon dormant; knockpy/ffuf/wfuzz current).
- **Practice blocks are self-study**, not class time — point at them, don't work through them.

## Prerequisites (student background)
- MCSA + Linux + CCNA assumed. DNS, HTTP and TCP/IP are referenced as attacker leverage, not re-taught.
- Session 1 complete: passive-vs-active *concept*, the 5-phase methodology, ATT&CK basics, and a built
  Kali box.

## Prerequisites (from earlier sessions)
- Session 1's KALI-ATK01 up on the host-only network, with `dig`, `whois`, `nmap`, `nc` available.
- Internet access from Kali (or the student's laptop) for the passive OSINT blocks — these query public
  third parties, not the target.

## Tools / VMs needed
See `labs/lab_design.md` and `labs/setup_guide.md`.
- **In class:** KALI-ATK01 for the active labs; a browser (Kali's or the laptop's) for the passive OSINT.
- **Active targets (Labs 4/6/7):** the Acunetix **vulnweb family** — `http://testphp.vulnweb.com` (directory/
  content/crawl/fingerprint) and `vulnweb.com` (subdomain enumeration). Live, authorised, no setup. Zone
  transfer uses `zonetransfer.me`; route tracing uses `scanme.nmap.org`. *Optional:* `scripts/lab_recon_target.sh`
  builds a local offline zone if the internet isn't available.
- **API keys:** none required. Shodan free (≈50 queries/mo, limited filters), hunter.io free (50
  credits/mo), DNSDumpster free (50 req/day) — all used within free tiers; say so before the labs.

## Deliverable
`recon_report.md` — a nine-section, ranked, sourced recon report on `tryhackme.com`, built section by
section across the eight labs and assembled in Lab 8. It is Session 3's scan list.

## Open items
- 2 of 9 screenshot slots ship as labelled placeholders: `crtsh-results` (crt.sh was returning 502 at
  build time — a real, and teachable, example of the service's flakiness) and `hunterio-domain-search`
  (needs a logged-in account; left for the instructor to capture without exposing account details).
  The page is safe to project without them.
- Active recon uses the live Acunetix vulnweb family (no local lab needed); `scripts/lab_recon_target.sh` + its `labs/lab_design.md` section are kept as an optional offline alternative.
