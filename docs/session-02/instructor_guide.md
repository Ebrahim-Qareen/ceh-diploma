---
session: 2
title: Footprinting & Reconnaissance
doc: Instructor Guide
---

# Session 2 — Instructor Guide

> **Deliver from `docs/session-02/index.html`.** 29 pages, arrow keys to navigate,
> sidebar to jump. Every diagram is on the page — 13 are click-to-reveal and 8
> animate, so click through them live rather than talking over a static image.

## Pre-class checklist

- [ ] **Stand up the lab recon target on your Kali** before class:
      `sudo ./scripts/lab_recon_target.sh up` — then confirm
      `dig +short recon.ceh-lab.local` answers and `curl -s http://recon.ceh-lab.local/` returns HTML.
      This is the authorised target for Labs 4, 6 and 7.
- [ ] Internet reachable from the machine you demo on — the passive blocks query public third parties.
- [ ] Confirm on your Kali: `dig`, `whois`, `theHarvester`, `subfinder`, `knockpy`, `gobuster`, `dirb`,
      `whatweb`, `traceroute`. Install anything missing tonight, not in front of the room
      (`sudo apt install -y theharvester dnsutils whois gobuster dirb whatweb subfinder`; `pip install knockpy`).
- [ ] Have a hunter.io free account ready if you want to demo Lab 3 step 3 live — or screen-share your
      own so students don't each burn credits.
- [ ] 6 of 9 screenshots ship filled; `crtsh-results` and `hunterio-domain-search` are placeholders.
      If you have a moment before class, capture crt.sh for `%.tryhackme.com` and a hunter.io domain
      search (blur your account details) and drop them in `docs/session-02/assets/img/`.
- [ ] Skim the three "your courseware is wrong" corrections below so you can defend them if challenged.

## The three currency corrections — know these cold

Students (and other instructors) will have older material. Be ready:

1. **WHOIS → RDAP.** ICANN sunsetted WHOIS for gTLDs on **28 January 2025**. `whois` still works via
   failover, but RDAP (HTTPS, JSON) is authoritative. The exam still tests WHOIS; the job hands you RDAP.
2. **Google `cache:` is gone.** Retired **September 2024**, operator and documentation removed. Use the
   Wayback Machine. If a practice question offers `cache:`, it is testing the syllabus, not the internet.
3. **Tool rot.** Sublist3r (last release 2020) and Photon (2019) are dormant; knockpy (v8, 2025),
   subfinder, ffuf and — contrary to rumour — wfuzz (v3.1.1, 2026) are current. The standing lesson is
   *check the release date*, not "Sublist3r bad".

## The one thing to get right all session: the passive/active line

The session is built around a single spine — **passive first, active only when justified**. Reinforce it
at every transition:
- Pages 5–16 are passive: nothing reaches the target, so there is nothing to detect.
- Page 17 ("Crossing the line") is the pivot. From there, every lab **names its authorised target before
  it names a command**, and the target changes off `tryhackme.com`.
- If a student proposes running an active tool against the client "just to check", that is the teachable
  moment — it is exactly the instinct that gets junior testers in legal trouble.

## Teaching flow

### Pages 2–4 — Where we left off, the funnel, the engagement (15 min)
Open by connecting to Session 1: they already crossed into active with `nmap`; today they go back and do
the phase they skipped. The **recon-funnel diagram (page 3) is click-to-reveal** — click each stage and
land the point that every tool lives at exactly one stage. Page 4 locks scope: one target, and the four
places where the target changes for active work. Read the authorization-basis table out loud.

### Page 5 — Search engines & dorks (7 min)
The **crawler→index→you diagram is click-to-reveal and animated** — replay the crawl, then click the
robots.txt box to show the amber path that skips the index (that is why fetching robots.txt is active).
Stress the three "shapes of mistake" over the operator list. Mention `cache:` is retired *here*.

### Lab 1 — Dork the target (14 min)
Pure browser + notebook, no VM. Walk the room. The step students undervalue is Step 5, the pivot
(`"tryhackme.com" -site:tryhackme.com`) — it finds the client's data on other people's servers, and it is
the finding that impresses real clients. Enforce the ground rule: **GHDB dorks only with `site:` attached**
— an unscoped GHDB dork opens strangers' exposed data and is where a legal exercise stops being legal.

### Page 6–7 — Shodan, Netcraft, crt.sh (14 min)
Three interactive diagrams. On Shodan, the teaching point is the **indirection** (their scanners hit the
target, you read the database) and the **freshness trade-off** (read "Last Seen" first). On crt.sh, the
**timing** is the attack — certificates are issued before hosts are hardened. Both diagrams animate; use
the replay.

### Lab 2 — The web-services sweep (16 min)
The longest passive lab. The single most-failed concept is **why `dig @1.1.1.1` is passive** — the query
goes to Cloudflare, not the target. Make a student explain it back. If Shodan demands login for
`hostname:` or crt.sh 502s (both common), have them swap order and use the Kali `curl | jq` line for
crt.sh — the lab is graded on the merged table, not on any one service being up.

### Page 10–11 — WHOIS→RDAP, people & email recon (13 min)
Run both `whois` and the RDAP `curl | jq` so students see the format difference. On page 11, the
**one-address-becomes-everyone diagram** is the emotional core of the session — spend a moment on the
*human* half (people leak because their incentives reward visibility, not because they're careless).

### Lab 3 — Registration & people (10 min)
Short. The deliverable is the **email convention as a rule**, not a list of addresses. Have students share
one hunter.io lookup per pair to conserve free credits. Keep LinkedIn strictly read-only — say it
explicitly, because someone will want to "just connect".

### Break (10 min)
The page has a working countdown timer.

### Page 14–15 — theHarvester, subdomains, stack (16 min)
theHarvester is taught *after* the manual work deliberately, so its output is interpretable rather than
magic. The **fan-out diagram** is interactive — click the keyed-sources box to explain why you plan for
those to fail in class. On page 15, the **one-domain-many-subdomains diagram** is the "real exposure is the
weakest of forty-one hosts" point — click each host row (each is a different failure mode found by a
different technique from today).

### Lab 4 — Automate the sweep (16 min)
**Step 0 stands up the lab target** (`sudo ./scripts/lab_recon_target.sh up`) — do this with them, it is
needed for Labs 6 and 7. The `whatweb -a 1` vs `-a 3` comparison at the end is the whole active-recon
discipline in miniature: more data costs more noise. Make sure no active command in anyone's history
points at the client.

### Page 17 — Crossing the line (4 min)
Short but pivotal. The **before/after diagram** is interactive — click each half. This is where you
re-state the rule for the back half of the session: every remaining lab uses an authorised stand-in.

### Page 18 — DNS & zone transfer (9 min)
Two interactive diagrams (the record map, and the correct-vs-misconfigured zone transfer, which animates).
The record-map point is that beginners run one `A` lookup; the value is in MX, TXT (SPF as a supply-chain
map, DMARC as a phishing forecast), NS and SRV. **This is one of the few recon events a defender can
actually detect** — flag that.

### Lab 5 — DNS & zone transfer (16 min)
The record sweep is passive; the AXFR is active against `zonetransfer.me` (published for training).
**Anticipate the three AXFR "failures"** and pre-empt them: (1) asking a recursive resolver — you must ask
an authoritative server, get it from NS first; (2) a correctly-restricted server refusing — that's a
finding; (3) outbound TCP/53 blocked on the campus network — try a different network. Reading the dump for
function-revealing hostnames and TXT records is the skill, not the host count.

### Page 20 + Lab 6 — Route tracing & crawling (18 min)
Traceroute against `scanme.nmap.org` (authorised, a few probes/day — do not hammer it). Crawling and
robots.txt against the **lab target**. The teaching beat in Lab 6 Step 2: fetching robots.txt yourself is
*active* (it's in the lab's access log), whereas reading it via Google in Lab 1 was passive — same file,
opposite side of the line. Photon is a 2019 tool; if it won't install, `katana` is the maintained fallback.

### Page 22 + Lab 7 — Brute-force (23 min)
The **subdomain-vs-subdirectory diagram** is interactive — left of the dot is DNS, right of the slash is a
web server. Lab 7 runs both against the lab zone (no external target for this — brute-forcing a stranger is
prosecuted). The headline experiment is **smart wordlist vs generic**: the convention students extracted
from crt.sh earlier beats a 5000-word list, which is the entire argument for doing passive recon first.
Step 4 has them read their own noise in the access log and write the detection rule — most of this class
will work blue-side, so this matters.

### Page 24 — Countermeasures (7 min)
The **three-layer doctrine diagram** is interactive and the pyramid is deliberately upside-down: the most
effective layer (reduce what you publish) has no alerts in it, and only ~3 of 10 techniques are detectable
at all. The ask-first question ("which could a SOC actually detect?") is the hook.

### Lab 8 — The recon report (14 min)
The session deliverable. Grade is on **conclusions, not dumps** — a ranked target list, an executive
summary a manager could read, and every claim marked fact or hypothesis. This report is literally
Session 3's scan list, so treat it as a handover, not homework.

### Pages 26–29 — Bridge, quiz, practice, wrap (16 min)
Quiz is self-scoring (10 MCQ + 2 short-answer). Stress homework task 3 — running the funnel against their
*own* name/domain — it is the exercise that makes the privacy lesson personal.

## Bridge to next session
Session 3 (Scanning & Enumeration) takes the ranked target list students built today and scans it for
real: host discovery, TCP/UDP scan types, version detection, and service enumeration. The continuity
target (`tryhackme.com` for recon → their lab targets for hands-on scanning) keeps the kill chain
assembling across sessions.
