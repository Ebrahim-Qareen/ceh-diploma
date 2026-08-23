---
session: 1
title: Foundations, Lab Build & First Contact
module_ref: Module 1 (Intro to Ethical Hacking), Module 2 pt1 (virtualization & lab), Module 3 (first-contact scanning)
duration: 4 hours
---

# Session 1 — Session Plan

## Title
Foundations, Lab Build & First Contact

## Module reference
- Module 1 — Introduction to Ethical Hacking (attacker mindset, IS concepts, methodology, frameworks, law)
- Module 2 pt1 — Virtualization concepts + host-only lab design
- Module 3 — first-contact host discovery + banner grabbing (intro slice only; full scanning is Session 3)

## Learning objectives
By the end of this session, students will be able to:
1. **Relate** their existing networking, OS and web knowledge to the attack surface it represents, and name the session where each becomes an attack.
2. **Explain** the attacker mindset: how an attack is composed (motive + method + vulnerability) and the 5-phase hacking methodology.
3. **Map** a real intrusion story to the Cyber Kill Chain and MITRE ATT&CK tactics.
4. **Define** engagement authorization and scope, and write a minimal rules-of-engagement (RoE) statement.
5. **Explain** virtualization — hypervisor types, VM hardware allocation, and the three network modes — and justify why the lab must be host-only with baseline snapshots.
6. **Perform** first contact against a live target — host discovery and service banner grabbing — and record it in a standard lab report.

## Time distribution (240 min)

| Block | Activity | Format | Min |
|---|---|---|---|
| Welcome | Cover, agenda, ground rules | — | 3 |
| Who's in the room | Instructor intro, student round, pair assignment, how the course runs | Ice-breaker | 15 |
| Incident story | "The breach nobody stopped" — every step left evidence | Story + pair discussion | 7 |
| Recall A | Networking you'll weaponise — OSI layers → attacks, TCP handshake → SYN scan, ports → target list | Ask-first, then diagram | 10 |
| Recall B | Linux & Windows — filesystem and credential stores read as an attacker | Ask-first, then diagram | 8 |
| Recall C | Web & identity — HTTP anatomy, authN vs authZ | Ask-first, then diagram | 7 |
| Recall D | Your knowledge mapped to the 10 sessions | Diagram | 5 |
| Theory A | How an attack is built: motive + method + vulnerability; attack classification | Theory (diagram) | 10 |
| Theory B | Who attacks — hacker classes on the authorization axis | Theory (diagram) | 8 |
| Theory C | The 5-phase methodology as a loop, with SOC detection surface per phase | Theory (diagram) | 12 |
| Theory D | Frameworks — Kill Chain, MITRE ATT&CK hierarchy, Diamond Model | Theory (3 diagrams) | 12 |
| Hands-on A | Map a real breach to Kill Chain + ATT&CK tactics | Activity (pairs) | 13 |
| Theory E + Hands-on B | Authorization, scope, RoE, law — then write your own RoE | Theory + activity | 20 |
| Break | — | — | 10 |
| Theory F | Virtualization — hardware vs software, VM concept, Type 1 vs Type 2, VT-x check, VM hardware settings | Theory (diagram + screenshots) | 18 |
| Theory G | Lab topology, the three network modes, why host-only is a safety control | Theory (2 diagrams) | 12 |
| Theory H | Snapshot discipline and the revert loop | Theory + live demo | 7 |
| Theory I | Passive vs active footprinting → what "first contact" means | Theory (diagram) | 7 |
| Hands-on C | **First contact** — `ip a`, `nmap -sn`, `ping`, `nmap -sV`, manual banner grabbing | Hands-on (everyone) | 30 |
| Wrap A | Lab report format and evidence standards | Wrap-up | 6 |
| Wrap B | Knowledge check — 10 interactive MCQ + 2 short answer | Quiz | 15 |
| Wrap C | Takeaways and homework brief | Wrap-up | 5 |

**Total: 240 min.**

## Delivery notes
- **Integrated, not blocked.** Topics run as one narrative: recall → what attacks it enables → the
  methodology that orders them → the frameworks that name them → the law that permits them → the
  lab that hosts them → the attack itself. Every page opens with an intro box saying why it follows
  the previous one.
- **Ask-first mechanic.** Each recall block opens with a question to the room; the diagram is the
  reveal. This doubles as the ice-breaker and lets the instructor map the room's real level early.
- **VM build is homework**, not class time. Class covers virtualization and lab design as theory so
  students build with understanding; the freed hands-on time goes to first contact.

## Prerequisites (student background)
- Completed MCSA, Linux, and CCNA (assumed). No networking/OS 101 is taught — prior knowledge is
  re-framed as attack surface, never re-taught.
- No prior offensive-security experience required.

## Prerequisites (from earlier sessions)
- None (this is Session 1).

## Tools / VMs needed
See `labs/lab_design.md` and `labs/setup_guide.md` — do not redefine the lab here.
- **In class:** KALI-ATK01 and METASPLOITABLE2 for the instructor demo and for students who
  pre-built. VMware host-only network (VMnet1, `192.168.56.0/24`).
- **Homework build:** KALI-ATK01, METASPLOITABLE2, then WIN10-TGT01 and WINSRV19-TGT01.
- **No AD domain** required for this session (flagged: revisit AD before Session 4 per
  `design/topic_map.md` open items).

## Team / pair assignment (starts this session)
- Class splits into **pairs**, assigned **randomly** — all students share the same MCSA/Linux/CCNA
  baseline, so skill-balancing adds nothing.
- **Each student builds their own VMs and personally runs every attack on their own Kali.** The pair
  is a peer-check unit (verify each other's lab, cross-read lab reports, rubber-duck troubleshooting),
  never shared execution.
- **Open — instructor may override:** pair vs. trio, random vs. self-chosen, fixed vs. rotating.
  Logged in DECISIONS.md as a default, not a lock.

## Assessment
- One knowledge check (10 interactive MCQ + 2 short answer) at the end — the only formal assessment.
- Homework lab report graded pass / needs-review (rubric in `exercises/session-01/homework.md`).

## Session assets
- `sessions/session-01/index.html` — 22-page interactive teaching page (17 inline SVG diagrams,
  8 screenshot slots, break timer, self-scoring quiz).
- Screenshots live in `sessions/session-01/assets/img/`. Missing files degrade to a labelled
  placeholder rather than a broken image, so the page is safe to present incomplete.
