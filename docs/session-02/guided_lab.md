---
session: 2
title: Footprinting & Reconnaissance
doc: Guided Lab
---

# Session 2 — Guided Lab: Footprint One Target, End to End

This session is lab-heavy: **eight hands-on blocks (~112 min)**, not one lab at the end. Each block
fills one section of a single deliverable, `recon_report.md`. This document is the consolidated
reference for all eight; the session page carries each block inline with its `.verify` checks.

## Objective
Produce a ranked reconnaissance report on one target using only authorised methods — proving you can:
1. Separate passive from active recon and respect the authorization each requires.
2. Use search engines, open databases, DNS and brute-force to map a target.
3. Read tool output for the line that matters, not just collect it.
4. Assemble findings into a ranked target list an analyst could act on.

## Targets & authorization (read before anything)
| Block(s) | Target | Basis |
|---|---|---|
| Labs 1–4 (passive) | `tryhackme.com` | Reading public third-party data only — no packets to the target |
| Lab 5 zone transfer | `zonetransfer.me` | Published by DigiNinja explicitly for training |
| Lab 6 traceroute | `scanme.nmap.org` | Site authorises "a few scans in a day" |
| Labs 4/6/7 active | `testphp.vulnweb.com` / `vulnweb.com` | Acunetix's deliberately-vulnerable sites, published for testing tools |

> **The line:** passive OSINT on public data is legal against anyone. The moment a tool sends a packet
> to a target, it needs written authorization — which is why the active blocks change target.

## Environment / setup
- **KALI-ATK01** with internet access, and: `dig`, `whois`, `theHarvester`, `subfinder`, `knockpy`,
  `gobuster`, `dirb`, `whatweb`, `traceroute`, `jq`, `curl`.
- **Active targets** (for Labs 4/6/7): the **Acunetix vulnweb family** is already live and authorised —
  nothing to build. Confirm you can reach it: `curl -s http://testphp.vulnweb.com/ | head` returns HTML.
  *(Optional offline alternative: `scripts/lab_recon_target.sh` builds a local zone if you can't reach the internet.)*
- Open `recon_report.md` from the template now — every block writes into it.

---

## Lab 1 — Search-engine footprint (14 min) → Report §1
```
site:tryhackme.com
site:tryhackme.com -site:www.tryhackme.com     # non-www hosts = free subdomains
site:tryhackme.com filetype:pdf
site:tryhackme.com (filetype:xlsx OR filetype:docx OR filetype:csv)
site:tryhackme.com intitle:"index of"
"tryhackme.com" -site:tryhackme.com filetype:pdf   # the pivot — their data elsewhere
```
Open the GHDB (`exploit-db.com/google-hacking-database`), take 3 dorks from one category, **rescope each
with `site:tryhackme.com`**. Record hostnames, document hits (with *why it matters*), a tech inferred from
a URL path, and the 3 GHDB dorks.
**Verify:** ≥2 non-www hostnames · ≥1 document finding with a reason · ≥1 tech from a path · 3 GHDB dorks.
**Ground rule:** unscoped GHDB dorks (no `site:`) open strangers' data — never do it.

## Lab 2 — Web-services sweep (16 min) → Report §2
```
dig +short tryhackme.com A @1.1.1.1                       # passive: query a public resolver
# Shodan (web UI): hostname:tryhackme.com → paste the IP → pivot on org:"..."
# Netcraft: https://sitereport.netcraft.com/?url=https://tryhackme.com   (hosting history!)
curl -s 'https://crt.sh/?q=%25.tryhackme.com&output=json' \
  | jq -r '.[].name_value' | sed 's/^\*\.//' | sort -u | tee crtsh_hosts.txt
wc -l crtsh_hosts.txt
```
Merge Shodan + Netcraft + crt.sh into one deduplicated host table: *host · IP · source · what it is ·
confidence*. Read crt.sh for the **naming convention** and write it as a rule.
**Verify:** merged deduped table · every row cites a source · ≥1 low-confidence row · Shodan "Last Seen"
recorded · a historical IP (or a note there's only one) · zero packets to the target.

## Lab 3 — Ownership & people (10 min) → Report §3
```
whois tryhackme.com | tee whois_domain.txt
curl -s https://rdap.verisign.com/com/v1/domain/tryhackme.com | jq . | tee rdap.json
whois 104.26.10.229 | head -40                            # who owns the ADDRESS (different DB)
# hunter.io (web): https://hunter.io/search/tryhackme.com  → record the PATTERN, not addresses
```
Record registrar, dates, **all name servers** (needed in Lab 5), status codes, netblock owner, and the
**email convention as a rule**. On LinkedIn (read-only): 3 attacker-relevant roles + 1 tech from a job advert.
**Verify:** name servers recorded exactly · registrar-lock status stated · convention written as a rule ·
one tech from a dated advert · no outbound contact.

## Lab 4 — Automate + fingerprint a real target (16 min) → Report §4
```
# active targets are already live (Acunetix vulnweb) — no setup needed
theHarvester -d tryhackme.com -b crtsh,duckduckgo,rapiddns,hackertarget -l 200 -f s02_harvest
subfinder -d tryhackme.com -silent | sort -u > subfinder_hosts.txt
cat crtsh_hosts.txt subfinder_hosts.txt | tr 'A-Z' 'a-z' | sed 's/^\*\.//' \
  | grep -E '^[a-z0-9.-]+$' | sort -u > all_hosts.txt
while read h; do ip=$(dig +short "$h" A @1.1.1.1 | tail -1); printf '%-45s %s\n' "$h" "${ip:-DEAD}"; done \
  < all_hosts.txt | tee resolved_hosts.txt
whatweb -a 1 http://testphp.vulnweb.com/                 # active — authorised target ONLY
whatweb -a 3 http://testphp.vulnweb.com/
```
**Verify:** master list merged/deduped/resolved · live vs DEAD counts · ≥1 anomaly flagged (forgotten /
pre-prod / takeover candidate) · whatweb both levels captured · you can state what `-a 3` added over `-a 1`.

## Lab 5 — DNS & zone transfer (16 min) → Report §5
```
for t in A AAAA MX NS SOA TXT; do echo "== $t"; dig +short "$t" tryhackme.com @1.1.1.1; done | tee dns_sweep.txt
dig +short TXT tryhackme.com @1.1.1.1                     # SPF: read every include: as a 3rd party
dig +short TXT _dmarc.tryhackme.com @1.1.1.1              # p=none? that's a phishing forecast
# --- switch target: authorised training zone ---
dig +short NS zonetransfer.me @1.1.1.1
dig axfr @nsztm1.digi.ninja zonetransfer.me | tee axfr_dump.txt
dnsrecon -d zonetransfer.me -t axfr
dig axfr @1.1.1.1 zonetransfer.me                         # WILL fail — a resolver never serves AXFR
```
Read the dump: function-revealing hostnames, every TXT record, any RFC1918 address, the naming convention.
**Verify:** dump has dozens of records · ≥2 hosts whose name reveals their role · all TXT read · the
resolver-failure output captured and understood · no AXFR in history points at the client.

## Lab 6 — Path & pages (10 min) → Report §6
```
traceroute scanme.nmap.org | tee traceroute.txt          # authorised; a few probes only
tcptraceroute scanme.nmap.org 443                         # when ICMP is filtered
curl -s http://testphp.vulnweb.com/robots.txt            # fetching this IS active (authorised)
python3 photon.py -u http://testphp.vulnweb.com -l 2 -t 10 -o photon_out   # or: katana -u ... -d 2
```
**Verify:** traceroute tail interpreted · robots.txt paths recorded · you can say why Lab 1's robots read
was passive and this one is active · Photon by-products inspected · ≥1 URL parameter flagged for Session 8.

## Lab 7 — Brute-force (16 min) → Report §7  · authorised vulnweb targets ONLY
```
knockpy vulnweb.com                                      # subdomain: DNS → NXDOMAIN on misses
ffuf -u http://testphp.vulnweb.com -H "Host: FUZZ.vulnweb.com" \
     -w ~/my_convention_list.txt -mc 200,301,403         # your crt.sh-derived list
ffuf -u http://testphp.vulnweb.com -H "Host: FUZZ.vulnweb.com" \
     -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -mc 200,301,403
gobuster dir -u http://testphp.vulnweb.com -w /usr/share/wordlists/dirb/common.txt   # directory: 404 on misses
dirb http://testphp.vulnweb.com
# you can't read Acunetix's logs — see your own noise locally:
python3 -m http.server 8000 &                            # then: gobuster dir -u http://127.0.0.1:8000 -w ...
```
**Verify:** both brute-forces run against the authorised vulnweb targets only · smart-vs-generic result recorded with numbers ·
directory hits carry status codes with ≥1 `403`/`401` flagged · one detection rule written from the log.

## Lab 8 — Assemble the report (14 min) → Report §0 + §8
Build the **ranked target list** (host · IP · what · why interesting · confidence · source), ranked by
attacker interest not discovery order. Write a 3–5 sentence **executive summary** a manager could read.
Do the **honesty pass**: mark every claim fact or hypothesis, date anything time-sensitive.
**Verify:** all 9 sections as conclusions not dumps · ranked list Session 3 could scan · exec summary ·
fact/hypothesis marked throughout · scope statement confirming no unauthorised active recon touched the client.

---

## Success check (show your instructor)
- [ ] `recon_report.md` complete, all 9 sections, ranked target list + executive summary.
- [ ] Every finding cites a source; confidence stated; facts and hypotheses separated.
- [ ] Passive blocks provably sent zero packets to `tryhackme.com`.
- [ ] Active blocks touched only authorised targets (`zonetransfer.me`, `scanme.nmap.org`, the Acunetix vulnweb sites).
- [ ] A live zone transfer captured from `zonetransfer.me` and read for content.
- [ ] The smart-vs-generic wordlist result recorded with numbers.

## Common mistakes
- **`dig @1.1.1.1` thought to be active** — it's passive; the query goes to the resolver, not the target.
- **AXFR against a recursive resolver** — never works; ask the authoritative NS (get it from `dig NS` first).
- **Unscoped GHDB dorks** — opens strangers' exposed data; always add `site:yourtarget`.
- **Reporting a Shodan banner as fact** — it's "last seen <date>", a hypothesis until verified.
- **Brute-forcing anything outside the authorised targets** — thousands of unsolicited requests = prosecuted attack.
- **Trusting a dead tool's empty output** — Sublist3r/Photon are dormant; a tool that silently returns less is worse than one that errors. Check the release date.
- **Collecting instead of concluding** — twelve tool dumps stapled together is not a report; rank and reason.
