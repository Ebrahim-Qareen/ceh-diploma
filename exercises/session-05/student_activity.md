---
session: 5
title: Student Activity — Session 5
---

# Session 5 — Student Activity

## Activity 1 — Manual vs framework (pairs, 12 min)
Pair A exploits vsftpd 2.3.4 **by hand** (nc); Pair B exploits it **via Metasploit**. Then swap notes and jointly write: (1) the three things the framework automated, (2) the one thing it did not, (3) one situation where you would prefer manual. Present in two sentences.

## Activity 2 — Bind or reverse? (individual, 8 min)
For each scenario, choose bind or reverse and say why in one line:
1. Target is a workstation behind a corporate firewall, can browse the web.
2. Target is an internal server you can reach on any port, but it has no outbound internet.
3. You control an egress-filtered network that only allows 443 out.
4. You have RCE on a public web server that NATs all outbound through one IP.

## Activity 3 — Staged, stageless, or it won't run (individual, 8 min)
Match each to the right call and predict the failure:
1. Unreliable link, you cannot guarantee the handler is up at the exact moment.
2. Tiny buffer in a BOF, every byte counts.
3. You started the payload but forgot to run the handler — what happens, and with which of the two?

## Activity 4 — Read the shell, name the attack (pairs, 12 min)
Given three log snippets (a service spawning cmd.exe; powershell making an outbound connection to a strange IP on 443; an ET EXPLOIT MS17-010 alert), name the attack behind each and the one field you would key a detection on.
