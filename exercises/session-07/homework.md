# Session 7 — Homework

## Core (everyone)
1. **Analyse a real sample, safely.** In your isolated sandbox, pull one tagged sample from MalwareBazaar (abuse.ch) or theZoo, or detonate via Any.Run/Hybrid-Analysis online. Produce a one-page triage: class, lifecycle stages observed, 3+ IOCs, ATT&CK techniques. **Prove your isolation** (screenshot the failed `8.8.8.8` reachability / VM network config).
2. **Write one durable detection.** From your homework sample, write either a YARA rule (distinctive content + combining condition) or a Sigma rule (a behaviour) and show it fires correctly.

## Stretch
3. Complete one TryHackMe room: **Basic Malware RE** or **History of Malware** (both verified free).
4. Take the WannaCry write-up and map its full chain to the 5-stage lifecycle and ATT&CK — note which stage the killswitch domain interrupted.

## Submit
- The triage one-pager (with isolation proof)
- Your working detection rule + a screenshot of it matching
- (stretch) room completion + the WannaCry mapping

**Reminder:** never download or run a live sample on a machine you care about. Chamber only.
