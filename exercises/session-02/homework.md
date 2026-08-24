---
session: 2
title: Footprinting & Reconnaissance
doc: Homework
---

# Session 2 — Homework

> The session deliverable is a **recon report**, not a lab build. Most of tonight is
> finishing and polishing what you started in the eight class labs, plus two rooms
> that self-pace the same material, plus one exercise that makes the privacy lesson
> personal.

## Tasks

1. **Finish `recon_report.md` on `tryhackme.com`.**
   All nine sections, built from your class notes:
   §0 executive summary · §1 search-engine footprint · §2 hosts & infrastructure ·
   §3 ownership & people · §4 automated OSINT · §5 DNS & zone data · §6 path & content ·
   §7 discovered by brute-force · §8 **ranked target list**.
   Every finding cites its source and a confidence level; every claim is marked **fact or
   hypothesis** (a Shodan banner is "reported, last seen <date>", not "confirmed"). End with a
   scope statement: no unauthorised active recon touched the client.

2. **Complete two free TryHackMe rooms — in this order:**
   - **Passive Reconnaissance** (`passiverecon`) — today's passive half, self-paced.
   - **Active Reconnaissance** (`activerecon`) — the active half; do it before Session 3.
   For each, write one paragraph: what it added beyond class, and one flag or answer you had to work for.

3. **Run the recon funnel against *yourself* (or a domain you own).**
   Dork your own name, check `crt.sh` for a domain you control, look yourself up on Shodan and
   Netcraft, and see what a hunter.io / people search returns. Write **half a page**: what you found,
   what surprised you, and one thing you'll change about what you publish. This is the exercise that
   turns "reduce your attack surface" from a slogan into something you've felt.

4. **Write three detection rules.**
   Pick any **three** of the ten techniques from today and, for each, write the exact detection you'd
   deploy: **log source · field · threshold/condition**. At least one must be for a *passive* technique
   (hint: the honest answer there is a monitoring/exposure control, not a SIEM rule — say so).

## Deliverables
- Completed `recon_report.md` (from `lab_report_template.md`, expanded to the nine sections above).
- Two TryHackMe room completions + one paragraph each.
- Half-page "recon against myself" write-up.
- Three detection rules.

## Grading rubric (pass / needs-review)

| Criterion | Pass |
|---|---|
| Report is conclusions, not dumps | Findings are interpreted and ranked, not raw tool output pasted in |
| Sourcing | Every finding cites where it came from; a host found by two sources is rated above one found four times by the same source |
| Honesty | Facts and hypotheses are separated; time-sensitive claims are dated; ≥1 finding is explicitly low-confidence |
| Scope discipline | Passive work provably sent zero packets to the client; active work (in the rooms) stayed on authorised targets |
| Self-recon | The "against myself" task is done honestly and produces one concrete change |
| Detection thinking | Three rules are specific (source/field/threshold); the passive one correctly reframes as monitoring, not alerting |

Needs-review = any criterion missing; revise and resubmit. No numeric grade — the quiz is the graded
assessment.

## Looking ahead to Session 3
Bring your **ranked target list** — Session 3 (Scanning & Enumeration) scans it for real. Also make sure
your **WIN10-TGT01 / WINSRV19-TGT01** targets from Session 1's homework are built and snapshotted; they
become scan/enumeration targets next session.
