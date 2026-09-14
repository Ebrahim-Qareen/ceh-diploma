# Session 10 — Homework (FINAL)

## Core (everyone)
1. **Evasion.** Against a lab host running Snort/Suricata, run a normal scan (confirm alerts), then evade with fragmentation, decoys, source-port, and slow timing. Then harden the IDS (full reassembly + anomaly) and re-run. Write up what beat what.
2. **Wireless.** On your own test AP (weak passphrase), capture and crack a WPA2 handshake with the aircrack-ng chain. Then set a 20-char random passphrase (or WPA3) and confirm it no longer cracks. (No adapter? Crack `saved/wpa2_handshake.cap`.)
3. **Emerging surface.** Create a test bucket, make it public, detect it anonymously, then fix it. Test a lab device for default creds. One-line finding + fix for each.
4. **Crypto audit.** Run `nmap --script ssl-enum-ciphers` (or testssl.sh) against an authorised host and list every weak protocol/cipher with the modern replacement.

## The capstone (graduation deliverable)
5. **Defence-in-depth capstone report.** Assess a lab environment across all ten sessions and write the report (attack narrative, findings by layer, what failed/held, prioritised remediation, detections). This is your portfolio piece — invest in it.

## Next steps (do at least one)
6. Complete a TryHackMe/HTB room on your chosen track (offensive or SOC), and outline your next certification (OSCP / BTL1 / CySA+ / etc.).

## Submit
- The evasion write-up, the wireless before/after, the cloud/IoT findings, the crypto audit
- **The capstone report** (the big one)
- Your chosen-track next-step plan

**Reminder:** lab hosts, your own AP/adapter, and your own cloud/devices ONLY. Everything else is a crime.

---
**Congratulations on completing the CEH Diploma. 🎓**
