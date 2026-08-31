---
session: 3
title: Scanning & Enumeration
---

# Session 3 — Guided Lab: Scan It, Enumerate It, Then Catch Yourself

The exact commands for every hands-on block. Replace `192.168.56.0/24` and the target IPs with your
own host-only network throughout. Each lab maps to a section of the **target profile** deliverable.

## Objective
Turn Session 2's recon report into a confirmed, enumerated, ranked target profile — and write one
working detection rule from evidence you generate yourself.

## Targets & authorization (read before anything)
- **Every hands-on block runs against YOUR lab VMs** on the host-only network. That is the only lawful
  place for a full subnet sweep, every scan type, UDP scans and service enumeration.
- Public hosts (`scanme.nmap.org`) appear for one contrast only, rate-limited — its owner allows "a few
  scans a day." Never point today's scans at anything else you don't own.

## Environment / setup
```bash
# confirm tools (install any that are missing)
nmap --version; nxc --version; enum4linux-ng -h >/dev/null && echo ok
rustscan --version; masscan --version; onesixtyone; which snmpwalk ldapsearch showmount smtp-user-enum
# common installs on Kali if needed:
sudo apt update && sudo apt install -y netexec enum4linux-ng onesixtyone snmp smbmap nbtscan rustscan seclists
```

## Lab pre-flight (5 min)
```bash
ip a | grep -A2 'ens\|eth'                 # your host-only IP
sudo nmap -sn 192.168.56.0/24              # expect: MSF2 + both Windows (one may hide — see Lab 1)
```
✓ All three targets found (a Windows box missing is expected — Windows Firewall drops ICMP).

## Lab 1 — Host discovery (12 min) → Profile: "live/dead + how confirmed"
```bash
sudo nmap -sn 192.168.56.0/24 | tee hosts_arp.txt                          # ground truth (ARP)
sudo nmap -sn -PE --send-ip --disable-arp-ping 192.168.56.0/24 | tee hosts_icmp.txt   # ICMP only
diff <(grep report hosts_arp.txt) <(grep report hosts_icmp.txt)            # a Windows host differs
sudo nmap -Pn -p 135,139,445,3389 192.168.56.X                            # scan the "dead" one anyway
sudo arp-scan --localnet                                                   # cross-check
```
✓ A Windows host present via ARP is absent via ICMP; `-Pn` proves it's alive.

## Lab 2 — Scan types + Wireshark (20 min) → Profile: "open ports" · SAVE THE PCAP
```bash
# start capture (keep the file — Lab 7 needs it)
sudo tcpdump -i eth0 -w lab2_syn.pcap host 192.168.56.102 &
sudo nmap -sS -p 22,80,443,445 192.168.56.102     # SYN → SYN/ACK → RST on open ports
sudo nmap -sT -p 22,80,443,445 192.168.56.102     # + the ACK; app logs it
sudo nmap -sX -p 22,80,443,445 192.168.56.102     # FIN,PSH,URG; open→silence
# defender view — watch the scan signature:
#   Wireshark filter:  tcp.flags.syn==1 and tcp.flags.ack==0
```
✓ You can point at SYN→SYN/ACK→RST (SYN), the extra ACK + banner (connect), and silent open ports (Xmas) in your own capture. `lab2_syn.pcap` saved.

## Lab 3 — Full scan (15 min) → Profile: "service + version, OS"
```bash
rustscan -a 192.168.56.102 --range 1-65535 -- -Pn        # breadth
sudo nmap -sS -sV -O -T4 -p 21,22,23,25,53,80,139,445,3306 192.168.56.102 -oN depth.txt   # depth
# failures on purpose:
sudo nmap -sU 192.168.56.102        # watch the ETA balloon → Ctrl-C
sudo nmap -sU -p 53,111,161,137 192.168.56.102            # the right way
#   note any 'tcpwrapped' or 'version?' — confirm by hand in Lab 6
```
✓ `depth.txt` has exact service+version per port; you saw the full UDP scan crawl and scoped it.

## Lab 4 — SMB: 2012 vs today (16 min) → Profile: "shares, users"
```bash
# rich target
enum4linux-ng -A 192.168.56.102 | tee smb_msf.txt
smbclient -L //192.168.56.102/ -N
# legacy target (Windows 7) — the classic dump STILL appears
enum4linux-ng -A 192.168.56.X | tee smb_win7.txt
nmap -p445 --script smb-protocols,smb-vuln-ms17-010 192.168.56.X   # SMBv1 + EternalBlue
# hardened target (Windows 10) — same command, near-silence
enum4linux-ng -A 192.168.56.X | tee smb_win.txt
nxc smb 192.168.56.X                              # still shows version/domain/signing
# what still works: authenticated
nxc smb 192.168.56.X -u '<LAB_USER>' -p '<LAB_PASS>' --shares --users --pass-pol
```
✓ Rich dump from Metasploitable2; "null session refused" from modern Windows; creds restore it. Finding = "hardened, enumerate with creds" — never "no findings."

## Lab 5 — SNMP + LDAP (15 min) → Profile: "SNMP/LDAP findings"
```bash
# SNMP
sudo nmap -sU -p161 192.168.56.X
onesixtyone -c /usr/share/seclists/Discovery/SNMP/snmp.txt 192.168.56.X    # find the community string
snmpwalk -v2c -c <SNMP_COMMUNITY> 192.168.56.X 1.3.6.1.2.1.1               # system
snmpwalk -v2c -c <SNMP_COMMUNITY> 192.168.56.X 1.3.6.1.2.1.25.4.2.1.2      # processes
# LDAP (against the DC)
ldapsearch -x -H ldap://192.168.56.X -s base namingContexts                # → DC=ceh,DC=lab
windapsearch -d ceh.lab --dc-ip 192.168.56.X -U | tee ldap_users.txt       # users
windapsearch -d ceh.lab --dc-ip 192.168.56.X -G                            # groups
```
✓ Community string found + tree walked; base context = `DC=ceh,DC=lab`; seeded users listed. (DC declined? Part B runs against THM `networkservices2`, LDAP concept-only.)

## Lab 6 — Service sweep (12 min) → Profile: "notable services" [absorb-to-homework option]
```bash
showmount -e 192.168.56.102                                    # NFS exports
nmap --script ftp-anon -p21 192.168.56.102 ; ftp 192.168.56.102  # anonymous FTP (vsftpd 2.3.4)
smtp-user-enum -M VRFY -U /usr/share/seclists/Usernames/top-usernames-shortlist.txt -t 192.168.56.102
rpcclient -U "" -N 192.168.56.102     # then: enumdomusers ; srvinfo ; querydominfo
nbtscan 192.168.56.0/24
nc -nv 192.168.56.102 22 ; nc -nv 192.168.56.102 25            # confirm a version by hand
```
✓ Each service enumerated; one version confirmed manually against what `-sV` reported.

## Lab 7 — Write the detection rule (16 min) → the signature exercise
```bash
# identify the scan from evidence alone
tshark -r lab2_syn.pcap -Y 'tcp.flags.syn==1 && tcp.flags.ack==0' -T fields -e tcp.dstport | sort -un | wc -l
```
Then write ONE working rule (Sigma / SPL / KQL) for "one source → many distinct ports → short window."
Worked Sigma is on the teaching page (P22); complete an SPL or KQL skeleton yourself.
✓ Deliverable: a complete rule + stated threshold/window + one false-positive sentence + the ATT&CK mapping (T1046/T1595) + one sentence on beating a `-T0` scan.

## Lab 8 — Assemble the target profile (12 min) → the deliverable
Fill `exercises/session-03/target_profile_template.md`, one block per live host, from your Lab 1–6
output files, plus the ranked "most likely way in" and the Lab 7 rule as an appendix.
✓ Ranked, sourced, exact versions, stated confidence — not raw nmap dumps.

## Success check (show your instructor)
- Host present via ARP but absent via ICMP, and you scanned it with `-Pn`.
- Your own three-scan Wireshark comparison, `lab2_syn.pcap` saved.
- `depth.txt` with exact versions; you scoped the UDP scan after watching it crawl.
- Rich SMB dump on Metasploitable2 AND Windows 7 (SMBv1) vs "null session refused" on Windows 10, and the authenticated re-run.
- Community string found + LDAP users listed.
- One complete, working detection rule.
- A ranked target profile for all three hosts.

## Common mistakes
- Turning off Windows Firewall to "fix" the missing host — use `-Pn`, that's the lesson.
- Running `nmap -sU -p-` and waiting forever — scope UDP.
- Reporting "no SMB findings" when a null session is refused — that's a hardening finding.
- Trusting a `tcpwrapped`/`version?` guess — confirm with netcat.
- Forgetting to save `lab2_syn.pcap` — Lab 7 needs it.
- A detection rule with no threshold or time window — that's not a rule, it's a wish.
