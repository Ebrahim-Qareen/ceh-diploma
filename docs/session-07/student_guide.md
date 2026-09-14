---
session: 7
title: Malware Threats & Analysis — Student Guide
---

# Session 7 — Student Guide

## What you will be able to do
Sit in both chairs on one malware sample: build it (attacker), take it apart static + dynamic (analyst), and write the YARA + Sigma rules that catch it (detection engineer) — then report it.

## The workflow to memorise
1. **Classify** by behaviour (how it spreads x what it is for).
2. **Static first** (safe): hash → VirusTotal, strings, PE imports.
3. **Dynamic second** (isolated): snapshot → host-only net → arm tools → detonate → watch processes/network/registry.
4. **Map** each behaviour to MITRE ATT&CK.
5. **Rank** IOCs on the Pyramid of Pain (host < network < behaviour).
6. **Detect**: YARA for the file, Sigma for the behaviour.
7. **Report**: verdict, behaviour, ATT&CK, IOCs, detections, hardening.

## The rule you never break
**Live malware runs only in a burn-it sandbox.** Snapshot, isolate the network, arm the tools — every time. Confirm the VM cannot reach `8.8.8.8` before you detonate anything.

## Key distinctions
- **Virus vs worm:** virus needs a click; worm self-spreads (outbreak speed).
- **Static vs dynamic:** static reads the file (safe); dynamic runs it (isolated). Packing hides strings but not behaviour.
- **YARA vs Sigma:** YARA matches file *content*; Sigma matches log *behaviour*. Use both.
- **Pyramid of Pain:** block the hash today, detect the behaviour forever.

## Deliverable
An **incident triage report** on your Lab A sample (template in `exercises/session-07/`). Six sections: summary/verdict, behaviour+ATT&CK, IOCs by durability, detections (your YARA+Sigma), containment, hardening.

## If you get stuck
Everything has a `saved/` fallback — a sample IOC sheet, a beacon pcap, event logs. You can complete every analysis and rule even if your sandbox misbehaves.
