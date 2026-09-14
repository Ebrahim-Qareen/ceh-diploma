---
session: 10
title: Evasion, Wireless & Emerging Tech — Instructor Guide (FINAL)
---

# Session 10 — Instructor Guide (FINAL SESSION)

## The one message
**Security is layers, and every attack is detectable if you know where to look.** This session sweeps the last of the surface and ties all ten together into defence-in-depth. If students leave thinking in layers (not isolated bugs) and can name a detection for anything, the diploma landed.

## It's a sweep — set the expectation
- This session is deliberately **broad**: evasion, wireless, mobile, IoT, cloud, crypto. Tell students up front it is a map, not deep dives — the goal is "you know this surface exists and where to go deeper," which is exactly what CEH breadth is for.
- Don't over-run any one block; the capstone (Lab E) and graduation are the point.

## Where students struggle / key insights
- **Evasion = matching method to blind spot** (P3-4). Hammer: signature→change bytes, anomaly→look normal/slow. Lab A shows evasion beats a *naive* sensor and a hardened one re-catches it — that's the lesson, not "evasion always wins."
- **Wireless needs hardware.** A monitor-mode adapter and a test AP are required for Lab B. Provide `saved/wpa2_handshake.cap` so anyone without an adapter still cracks a handshake. Stress: **your own AP only.**
- **Cloud/IoT = check, don't exploit** (P15-16). The findings are configuration (public bucket, default creds), found by inspection. This reframes "hacking" for a lot of students.
- **Crypto three tools / three jobs** (P17). The single most useful crypto slide: symmetric=confidentiality, asymmetric=key-exchange+signatures, hashing=integrity. Everything else builds on it.
- **Crypto fails in deployment, not math** (P19). Students expect to "break AES." Redirect to the real findings: MD5/SHA-1, weak passphrases, missing salt, unverified signatures.

## The capstone (Lab E) — this is graduation
- Hold real time for it. It spans all ten sessions and is the students' **portfolio piece**. Push them to frame findings as a *defence-in-depth chain* (what failed, what held), not a bug list.
- The "whole map" (P24) and "where next" (P25) pages are the emotional close — connect their first ping sweep to where they are now, then point at the next step (depth + a cert on their chosen track; the SOC path for this cohort).

## Board-worthy anchors
- The layers table (perimeter→identity→app→endpoint→network→data→detection) with each session mapped in.
- "Attackers chain weaknesses; defenders chain controls."
- The TLS hybrid handshake — it retroactively explains every S8-9 network defence.

## Assessment
- Formative: 6 MCQs (P26) + 14 mini-labs.
- Summative: the **defence-in-depth capstone report** (Lab E) against `exercises/session-10/capstone_report_template.md` — the diploma's culminating deliverable; rubric in student_activity.md.
