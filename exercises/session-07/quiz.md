# Session 7 — Quiz (answers at the bottom)

1. What single difference defines a worm vs a virus, and why does it matter for containment?
2. Why is static analysis always performed before dynamic analysis?
3. A PE sample has almost no imports (just LoadLibrary/GetProcAddress). What does this indicate and what do you do next?
4. Which Sysmon Event ID + condition best detects Mimikatz-style credential dumping?
5. On the Pyramid of Pain, which indicator gives the most durable detection, and which is the most brittle?
6. Why is a rule on `vssadmin delete shadows` valuable against ransomware?
7. What are the five stages of the malware lifecycle, and name one detection for each?
8. Fileless malware defeats which analysis technique, and how do you detect it instead?
9. YARA vs Sigma — what does each match, and why pair them?
10. Name the three non-negotiable steps before detonating a live sample.

---
## Answers
1. Worm self-propagates (no user click) → outbreak speed → contain by segmentation/patching; virus needs a click → contain by stopping execution.
2. Static never executes the file → zero risk; you learn safely first. Dynamic must be isolated.
3. Packed/obfuscated — real imports resolved at runtime. Next: dynamic analysis in a sandbox.
4. Sysmon Event ID 10 (ProcessAccess) on lsass.exe with a dump GrantedAccess mask (0x1010/0x1410) — T1003.001.
5. Most durable: behaviour/TTP. Most brittle: the file hash (one byte = new hash).
6. It runs before encryption to kill backups; catching it can save the data while files are still intact.
7. Delivery (email filtering), Execution (Sysmon 1/4688 parent-child), Persistence (Sysmon 13/7045), C2 (Sysmon 3 beacon), Actions (Sysmon 10 / mass file-write).
8. Defeats static/hash-based analysis (no file). Detect via behaviour: command lines, Script Block Logging (4104), process trees.
9. YARA matches file content; Sigma matches log behaviour. Pair them so re-encoding cannot beat both.
10. Snapshot, isolate the network (host-only/fake-internet), arm the monitoring tools — before detonation, every time.
