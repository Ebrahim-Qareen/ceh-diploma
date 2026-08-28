---
session: 4
title: System Hacking I — Vulnerability Analysis, Authentication & Password Attacks
---

# Session 4 — Student Activity

Two in-class activities. The first is done in pairs; the second is individual. Neither needs a working VM —
both run on evidence, so they double as the fallback for anyone whose lab is down.

## Activity 1 — Name that attack (pairs, 15 min)
Your instructor hands each pair three short log/output extracts, labelled A, B, C. For each, decide the
**attack** from the evidence alone, name the **Event ID(s) / artefact**, and give the **ATT&CK technique**.

**Extract A** (DC Security log, seconds apart)
```
4625  Target: a.fahmy   Source: 192.168.56.50   Status: 0xC000006A
4625  Target: m.said    Source: 192.168.56.50   Status: 0xC000006A
4625  Target: n.gamal   Source: 192.168.56.50   Status: 0xC000006A
4625  Target: h.rashad  Source: 192.168.56.50   Status: 0xC000006A
```

**Extract B** (DC Security log, one user, many services)
```
4769  Account: a.fahmy  Service: MSSQLSvc/win10-tgt01  Ticket Encryption Type: 0x17
4769  Account: a.fahmy  Service: MSSQLSvc/win10-tgt01:1434  Ticket Encryption Type: 0x17
```

**Extract C** (attacker terminal)
```
[SMB] NTLMv2-SSP Client   : 192.168.56.20
[SMB] NTLMv2-SSP Username : ceh.lab\j.doe
[SMB] NTLMv2-SSP Hash     : j.doe::CEH:1122...:<hash>
```

For each write: (1) the attack, (2) the Event ID or artefact that identifies it, (3) the ATT&CK technique,
(4) one sentence on the detection signature. Then answer: **which of the three leaves no server-side Windows
Event ID at all, and why?**

> Answer key (instructor): A = password spraying — 4625, many distinct accounts + one source + status
> 0xC000006A (bad password) → T1110.003. B = Kerberoasting — 4769 with encryption type 0x17 (RC4), one user
> many SPNs → T1558.003. C = LLMNR/NBT-NS poisoning — a captured NetNTLMv2 (Responder), no single Windows
> Event ID on the DC → T1557.001; it's detected on the network / by canary lookups, because the "auth" went to
> a rogue host, not the DC.

## Activity 2 — Which hash, which mode, real or not? (individual, 12 min)
For each item, state what it is and the **hashcat mode** (or the correct call), and whether the described
result is a **real finding**, a **false positive**, or a **wrong tool/mode**.

1. `impacket-secretsdump` gives `labuser:1001:aad3b...:31d6cfe0d16ae931b73c59d7e0c089c0:::`.
2. Responder captured `ceh.lab\j.doe:::<hash>`; a student runs `hashcat -m 1000` on it and it never matches.
3. `GetUserSPNs -request` returns `$krb5tgs$23$*svc_sql*...`; hashcat runs to `Exhausted` against rockyou + best64.
4. A Nessus report shows "Critical — Samba badlock" on a box whose real version is Samba 3.0.20.
5. A student dumped an NT hash they can't crack, then logged into another host with it directly.

> Answer key (instructor): 1 = local NT hash from the SAM → `-m 1000` (the 4th field; note the 3rd is the empty
> LM). 2 = wrong mode — a NetNTLMv2 capture is `-m 5600`, not 1000. 3 = not a false positive — a *real* roast of a
> *strong* password; the countermeasure (long/random service password or gMSA) worked. Record "roastable, not
> cracked." 4 = likely a false positive — confirm the real version; the proven way in on that box is
> usermap_script (CVE-2007-2447). 5 = pass-the-hash (T1550.002) — the NT hash *is* the credential; no crack needed.

**Close:** in one sentence each, why is "the crack failed" never, by itself, a conclusion — and what are the two
things you check before writing "uncrackable"?
