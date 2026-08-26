---
session: 2
status: built — awaiting review
---

# Session 2 — Build Log

What was built, what changed, and what is still open. Rationale for each decision lives in
`DECISIONS.md`; this file is the working detail. Same shape as Session 1's build log.

## Current state

- **29 pages**, ~285 KB single HTML file at `docs/session-02/index.html`
- **~24 hand-authored inline SVG diagrams** — **13 click-to-reveal**, **8 animated with replay**
- **9 screenshot slots** — 6 filled with our own captures, 2 labelled placeholders (crt.sh was 502; hunter.io needs login)
- **6 practice blocks** linking verified external rooms; consolidated practice-plan page
- **Active targets switched to the Acunetix vulnweb family** (`testphp.vulnweb.com` web/dir, `vulnweb.com` subdomains) — the local `ceh-lab.local` lab is now an OPTIONAL offline alternative, not required (instructor hasn't built it). Log-reading defender exercise adapted to a throwaway local `python3 -m http.server`
- **Expanded "more authorized practice targets" table** on P22 (vulnweb siblings · demo.testfire.net · ginandjuice.shop · brokencrystals.com · google-gruyere · hackthissite · scanme · zonetransfer + structured platforms)
- **P22 brute-force tool reference** — per-tool cheatsheets (subfinder/amass/knockpy/ffuf/gobuster/feroxbuster/dirsearch/dirb/wfuzz/dnsenum/fierce/dnsrecon), wordlists table, decision guide; real legal target `testphp.vulnweb.com` for directory work
- Break timer, 10-question self-scoring quiz + 2 short-answer, sidebar nav, progress bar, keyboard nav
- Full 7-doc package + a lab recon-target script
- Not yet published to GitHub (awaiting review)

## What makes this session different from Session 1

Session 1 was foundations with one lab at the end (~30 min hands-on in 240). Session 2 is a
**tool-by-tool, hands-on recon session**: **8 hands-on blocks, ~112 min (47%)**, spread through the
session after each tool group. Every tool is taught with the instructor's required 7-part frame —
what it is / why it exists / **the method** / real syntax / how to read the output / what it feeds /
the SOC flip — because "focus on the methods" was the explicit priority.

Visuals are a **mix** rather than Session 1's 100% hand-authored SVG: hand-authored diagrams for every
concept, plus real captured screenshots of live tools, because recon is a visual, tool-driven topic.

## Build history

### Outline first, then build (approved)
Presented a page-by-page outline with timings, the own-block-vs-grouped tool split, the single
carry-through target, the verified TryHackMe rooms, and the visual-sourcing plan. Instructor approved
`tryhackme.com` as the carry-through target and a local DNS zone for the subdomain-brute-force lab, then
the build proceeded — same gate as Session 1.

### The page (29 pages)
Built in 10 HTML fragments and concatenated. Structure: recall/funnel/engagement (P2–4) → search
engines + Lab 1 (P5–6) → Shodan/Netcraft/crt.sh + Lab 2 (P7–9) → WHOIS/RDAP + people + Lab 3 (P10–12)
→ break (P13) → theHarvester/subdomains + Lab 4 (P14–16) → crossing-the-line + DNS/zone-transfer + Lab 5
(P17–19) → route-tracing/crawling + Lab 6 (P20–21) → brute-force + Lab 7 (P22–23) → countermeasures +
report Lab 8 (P24–25) → bridge/quiz/practice/wrap (P26–29). Every page opens with a `.box.intro` tying
it to the previous one; every attack page carries the SOC flip; techniques map to ATT&CK TA0043.

### Dynamic diagrams (instructor asked for "a lot")
Reused the shared `.dgm.interactive` (click-to-reveal) and `.dgm.animate-run` / `data-replay`
(animated) mechanics from Session 1's design system — no new CSS/JS. 13 diagrams are click-to-reveal
(recon funnel, dork paths, Shodan indirection, certificate-transparency leak, theHarvester fan-out,
subdomain expansion, crossing-the-line, DNS record map, zone-transfer correct-vs-misconfigured, route
tracing, subdomain-vs-subdirectory, countermeasure layers, email-convention chain); 8 also animate
their flow paths with a replay button.

### Screenshots (captured via Chrome, our own queries)
Captured through the instructor's logged-in Chrome against the public carry-through target, saved as
compressed progressive JPG under `docs/session-02/assets/img/` (~306 KB total, well under the page-weight
budget), each wrapped in `<figure class="shot">` so a missing file degrades to a labelled placeholder:
- `google-dork-serp.jpg` — `site:tryhackme.com filetype:pdf` (real leaked PDFs on assets.tryhackme.com; account avatar blurred)
- `shodan-host-detail.jpg` — Shodan host view of `1.1.1.1` (public Cloudflare DNS; shows Last Seen, ASN, org, ports, banners)
- `shodan-results.jpg` — Shodan's "log in to use search filters" (documents the free-tier limitation the page describes)
- `ghdb-category.jpg` — the Google Hacking Database category listing (7,944 entries)
- `netcraft-sitereport.jpg` — Netcraft site report for tryhackme.com (Vercel hosting, Cloudflare NS, Namecheap registrar)
- `attack-navigator-ta0043.jpg` — the ATT&CK Enterprise matrix with the Reconnaissance column boxed in red

### The 7-document package
- `docs/session-02/`: `session_plan.md`, `instructor_guide.md`, `student_guide.md`, `guided_lab.md`
- `exercises/session-02/`: `student_activity.md`, `quiz.md`, `homework.md`
All follow the exact section shapes of the Session 1 package.

### Lab addition
`scripts/lab_recon_target.sh` stands up a `ceh-lab.local` dnsmasq zone + python web root on Kali (not a
new VM) as the authorised target for the active brute-force/crawl labs. `labs/lab_design.md` updated with
a Session 2 section and a VM-table row. No secrets; all served content is deliberately fake. Zone-transfer
practice uses the public `zonetransfer.me`; route tracing uses `scanme.nmap.org`.

## Research performed (TryHackMe, via Chrome)
Read actual task content of `passiverecon`, `activerecon`, `googledorking` logged into the instructor's
account; verified tier logged-out for all candidate rooms. Extracted real technique detail used to sharpen
the teaching: the whois→RDAP migration and `curl rdap… | jq` pattern, `dig` vs `nslookup` + TTL, crt.sh
`%.domain` wildcard, Shodan filters, the crawler→index→robots model, and the mistakes their tasks are
built to catch. No room text reproduced verbatim — technique extracted and taught in our own voice.

## Verification performed
Playwright (design_system §8 recipe, `viewport:` not `viewportSize:`) across 1400/1100/900/700/480px:
- Document-level horizontal overflow: **none at any width**
- Elements wider than viewport outside a scroll container: **none**
- SVG text escaping its viewBox: **none**
- Interactive diagrams: **58 `data-node`s, 58 `data-detail` panels, 0 orphans**; every node opens exactly one panel
- Console/page errors: **0 real errors** (only the expected image-404s for the 2 placeholder slots + 1 not-yet-copied logo in the isolated test tree)
- Page count 29, snum sequence P02–P29 contiguous, all four SVG arrow markers defined before first use

Also confirmed: **no instructor-only text in the student HTML** (no "ask the room", no "what to listen for");
every external room fetched and its tier confirmed; the `.box.intro`-per-page rule holds.

## Open items

1. **2 screenshot slots are placeholders.** `crtsh-results` — crt.sh returned HTTP 502 throughout the
   build (the exact flakiness the page warns about); `hunterio-domain-search` — needs a logged-in account,
   left uncaptured to avoid exposing account/credit details. Both degrade to labelled placeholders; the
   page is safe to project. The instructor can drop replacements into `docs/session-02/assets/img/`.
2. **Carried over from Session 1 — MITRE ATT&CK Navigator screenshot.** Captured a fresh Navigator image
   for Session 2's TA0043 diagram (`attack-navigator-ta0043.jpg`). It can also fill Session 1 page 12's
   missing Navigator slot if the instructor wants — offered, not silently applied.
3. **Carried over from Session 1 — GitHub Pages still not enabled.** Settings → Pages → `main` / `/docs`.
4. **Continuity target that can be *attacked* end to end** (S3→S6) still open — S2 only establishes the
   passive-recon carry-through target. Needs an instructor-owned domain or dedicated lab company.

## Files owned by this session

```
docs/session-02/index.html            the teaching page (29 pages)
docs/session-02/assets/img/           6 screenshots (2 slots pending)
docs/session-02/session_plan.md
docs/session-02/instructor_guide.md
docs/session-02/student_guide.md
docs/session-02/guided_lab.md
exercises/session-02/                  quiz, homework, student_activity
scripts/lab_recon_target.sh           the local recon lab target
```

Shared (not forked per session): `docs/assets/css/ceh.css`, `docs/assets/js/session.js`,
`docs/index.html` (dashboard — needs a Session 2 card wired; see below).

## Still to wire before/at publish
- Add a **Session 2 card** to the course dashboard `docs/index.html` (mark delivered) and confirm the
  Session 1 "next" link points to `session-02/`.
