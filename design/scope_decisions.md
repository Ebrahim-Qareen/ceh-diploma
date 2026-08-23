# Scope Decisions

## Resolved

- **Course locked at 10 sessions × 4h = 40h** (2026-08-22).
- **Gap topics (Session Hijacking, IDS/Firewall/Honeypot Evasion, Mobile,
  IoT/OT, Cloud) will be added from official EC-Council material**, not
  skipped (2026-08-22).

## Open — needs your input

The official EC-Council module PDFs for those specific gap topics
(Ch11, Ch12, Ch17, Ch18, Ch19) are **not yet in `Resources/EC-Council
Materials/`** — only Ch1, Ch4, Ch5 are present. To build sessions 9-10
properly, add the matching official CEHv13 module PDFs to that folder;
`ceh-material-intake` will process them the same way as everything else.

## Course Design Brief (instructor interview, 2026-08-22)

### 1. Students
- Come in having completed **MCSA, Linux, and CCNA** — solid IT/networking/OS
  foundation, no prior offensive-security exposure. CEH is their first
  attacker-mindset course.

### 2. Why they take it / next steps
- Goal: **SOC Analyst** entry-level role.
- Path after this diploma: **eCIR** → **eCDFP**.
- CEH here = building the attacker mindset (how attacks work, tools, targets,
  steps) so they can detect/respond later, not a pure red-team track.

### 3. 10-session coverage
- Current `design/topic_map.md` breakdown stands as a draft, **but instructor
  wants to re-review all topics and re-split them across the 10 sessions**
  before treating it as final. Do this re-check before/at Session 1 build if
  not already done — don't silently keep the old split if it's changed.

### 4-7. Delivery format
- **No hard theory/practice split** — integrated: short theory chunk →
  immediately followed by hands-on for that chunk, repeated through the
  session.
- Heavy skew toward **practice** — students must personally try each attack:
  tools, targets, steps, and attacker mindset for every technique covered,
  not just watch a demo.
- Theory chunks: **simple, short, clear** — favor **live/diagrammed
  explanations** over text-heavy slides; slides used but kept minimal, diagram
  and live-demo led.
- Practice style is **flexible per topic/time available** (guided steps,
  guided-then-free, live demo-then-repeat — instructor picks per session), but
  two fixed rules:
  1. Every student must **personally do the hands-on work** every session —
     no session where they only watch.
  2. If the class is split into **teams/pairs**, that assignment starts from
     **Session 1** and is decided then, not introduced later.

### 8. Homework
- **Every session** produces a **short, simple lab report** — students write
  up what they did, what worked, what didn't (right vs. wrong), for whatever
  they did in that session's lab/exercise.
- Instructor wants a **report template/example shown starting Session 1** so
  students know the expected format from day one.
- Beyond the report: any other reasonable homework form (quiz, redo task,
  etc.) is fine — the report is the one fixed requirement.

### 9. Projects
- **No fixed capstone/mini-project plan decided yet** — open, TBD later.
- Fixed requirement instead: **every session has a live practice setup** —
  Kali attacker box + victim machine(s) appropriate to the topic (AD, Linux,
  Windows of various versions, known vulnerable boxes like Metasploitable2,
  or a vulnerable web app/site). This is a standing lab requirement per
  session, not a "project."
  - Note: current `labs/lab_design.md` baseline has Kali, Win10, WinSrv2019,
    Metasploitable2 — **no AD domain environment yet**. Since SOC/CEH attacks
    commonly target AD, revisit with `ceh-lab-build` whether/when to add a
    domain controller setup as sessions progress.

### 10. Assessment
- **Quiz per session only** — no midterm/final exam, no separate practical
  exam. Grading model beyond the quiz not otherwise formalized.

### 11. Lab environment
- **Each student builds their own VMs locally** (not classroom machines, not
  pre-built images handed out) — following the setup guide in `labs/`.

### 12. Course materials
- Delivered as a **public GitHub Pages–style course website**, same pattern
  as the instructor's prior course: https://ecir-diploma.vercel.app/
- Site includes, per session: materials, setup instructions, homework, and
  practice/lab links — everything for that session in one place.
- This confirms `ceh-github-publish` is the intended delivery mechanism, not
  handing out separate files.

### 13. Certificates
- **Out of scope for course design** — certificate issuance is an ITGate
  Academy administrative matter, not something the instructor is deciding
  here. No certificate requirements to build into session content.

### 14. Still open (flag, don't block Session 1 on these)
- Final per-session topic split (re-review pending, see §3).
- Team/pair assignment mechanics for Session 1 (random vs. skill-balanced,
  team size) — instructor hasn't fixed the method yet, just that it starts
  Session 1 if used.
- Whether an AD lab environment gets added and when.
- Capstone/per-session project shape — deferred, no decision yet.
