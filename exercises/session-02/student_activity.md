---
session: 2
title: Footprinting & Reconnaissance
doc: Student Activity
---

# Session 2 — Student Activity

Two short independent tasks that build on the guided labs, with less hand-holding. Run them in the
gaps between lab blocks, or as a consolidation exercise near the end.

## Activity 1 — The pivot chain (pairs, 20 min)

You have a host table from Lab 2 and an email convention from Lab 3. Now practise the move that separates
recon from data collection: **pivoting**.

Starting from the single fact `tryhackme.com`, write the **chain of pivots** you used (or could use) to
reach each of the following, naming the tool and the field you pivoted on at each step:

1. A subdomain that never appears on the main website.
2. The organisation that owns the IP address (not the hosting provider — or a statement that it *is* the provider).
3. An employee's likely username.
4. A third-party service the organisation trusts (hint: read an SPF record).

**Deliverable:** a 4-row table — *goal → starting fact → tool → field pivoted on → result*. Each row must
show a **pivot** (fact A used to reach fact B), not just "I searched for it".

**Success criteria:** every row names the specific field that carried the pivot (an ASN, a SAN entry, an
SPF `include:`, a naming convention) — not just the tool. At least one chain is two pivots deep.

## Activity 2 — Passive or active? (individual, 15 min)

For each action below, decide **passive or active**, state **who receives the packet**, and if active,
**which authorised target** you would run it against in this session. Then write one line on **whether a
defender could detect it**.

| # | Action |
|---|---|
| 1 | `dig +short MX tryhackme.com @1.1.1.1` |
| 2 | `dig axfr @nsztm1.digi.ninja zonetransfer.me` |
| 3 | Searching `%.tryhackme.com` on crt.sh |
| 4 | `curl http://tryhackme.com/robots.txt` |
| 5 | `knockpy ceh-lab.local` |
| 6 | Reading a target employee's public LinkedIn profile |
| 7 | `whatweb -a 3 https://tryhackme.com` |

**Success criteria:** all seven classified correctly with the *reason* (who gets the packet), every active
one assigned to an authorised target, and the "detectable?" column correct — note that #1, #3 and #6 are
**not** detectable by the target because a third party (or nobody) receives them, while #2, #4, #5 and #7
are. (#4 and #7 against `tryhackme.com` as written are **not authorised** — the correct answer names the
lab target or flags them as out of scope.)

**Answer key (instructor):**
1. Passive — query goes to Cloudflare's resolver; not detectable by target.
2. Active — packet to `zonetransfer.me`'s authoritative NS (authorised training zone); detectable (AXFR in DNS log).
3. Passive — query goes to crt.sh/CT logs; not detectable.
4. Active — packet to the web server; **as written, against the client, out of scope** → run against the lab target; detectable (access log).
5. Active — DNS queries to the lab zone (authorised lab); detectable (NXDOMAIN spike).
6. Passive — reading a public page; not detectable (LinkedIn's view metrics aside, the target org can't see it).
7. Active — HTTP requests to the target; **against the client, out of scope** → lab target only; detectable (access log, tool User-Agent).

**Time box:** 35 min total for both. Turn in with your recon report.
