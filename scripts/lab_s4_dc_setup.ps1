#Requires -RunAsAdministrator
<#
    CEH Diploma lab - Session 4 target prep
    Extends the Session 3 domain (ceh.lab) for the authentication & password
    attacks in Session 4. Sibling to scripts/lab_s3_dc_setup.ps1 - it does NOT
    replace it. Run AFTER the S3 DC promotion + seed are done.

    What it sets up, and why each attack needs it:
      Kerberoast    - registers an SPN on svc_backup and sets it a DELIBERATELY
                      weak (wordlist-crackable) password, so GetUserSPNs ->
                      hashcat -m 13100 actually cracks in class. Adds a SECOND
                      SPN account (svc_sql) with a STRONG password = the
                      "Kerberoast that never cracks" teaching case.
      Spray         - sets ONE weak password shared by a DEFINED subset
                      (a.fahmy, n.gamal, h.rashad) and leaves m.said on a
                      distinct strong password, so a password spray hits 3/5 and
                      misses 1 (realistic), then enables an account-lockout
                      policy so the "spray trips lockout" failure case is real.
      LocalAccounts - adds 2-3 weak LOCAL accounts on Win7/Win10 for the
                      SAM/hashcat lab (run this stage ON each workstation).
      CheckLLMNR    - REPORTS whether LLMNR + NBT-NS are still on (run ON Win10);
                      prints the GPO countermeasure. Read-only, changes nothing.

    NO CREDENTIALS IN THIS FILE. Every password is prompted for at run time.
    Idempotent: safe to re-run. Placeholders only - nothing sensitive is stored.

    Usage (Domain Controller - WINSRV19-TGT01):
      .\lab_s4_dc_setup.ps1 -Stage Kerberoast
      .\lab_s4_dc_setup.ps1 -Stage SprayPolicy
    Usage (each workstation - WIN7-TGT01, WIN10-TGT01):
      .\lab_s4_dc_setup.ps1 -Stage LocalAccounts
    Usage (WIN10-TGT01, verify the LLMNR victim is still poisonable):
      .\lab_s4_dc_setup.ps1 -Stage CheckLLMNR
#>

[CmdletBinding()]
param(
    [ValidateSet('Kerberoast','SprayPolicy','LocalAccounts','CheckLLMNR')]
    [string]$Stage = 'Kerberoast',
    [string]$DomainName = 'ceh.lab'
)

$ErrorActionPreference = 'Stop'

# ---------------------------------------------------------------------------
#  Kerberoast prep  (run on the DC)
# ---------------------------------------------------------------------------
function Invoke-Kerberoast {
    Import-Module ActiveDirectory

    Write-Host '[!] svc_backup gets a WEAK password that IS in your cracking wordlist' -ForegroundColor Yellow
    Write-Host '    (e.g. a rockyou word + a simple rule). This is what cracks in class.' -ForegroundColor Yellow
    $weak = Read-Host -AsSecureString 'Weak Kerberoastable password for svc_backup'

    # svc_backup already exists (created by the S3 seed). Give it an SPN + the weak password.
    if (-not (Get-ADUser -Filter "SamAccountName -eq 'svc_backup'" -ErrorAction SilentlyContinue)) {
        throw 'svc_backup not found - run scripts/lab_s3_dc_setup.ps1 -Stage Seed first.'
    }
    Set-ADAccountPassword -Identity 'svc_backup' -NewPassword $weak -Reset
    # A registered SPN is what makes any domain user able to request a service
    # ticket encrypted with this account's password hash = Kerberoastable.
    Set-ADUser -Identity 'svc_backup' -ServicePrincipalNames @{Add="MSSQLSvc/win10-tgt01.$DomainName:1433"}
    Write-Host '[+] svc_backup: SPN registered + weak password set (WILL crack).' -ForegroundColor Cyan

    # A second service account that will NEVER crack - the honest failure case.
    Write-Host '[!] svc_sql gets a STRONG random password - the Kerberoast that never cracks.' -ForegroundColor Yellow
    $strong = Read-Host -AsSecureString 'STRONG password for svc_sql (long + random)'
    if (-not (Get-ADUser -Filter "SamAccountName -eq 'svc_sql'" -ErrorAction SilentlyContinue)) {
        $base = (Get-ADDomain).DistinguishedName
        $ou = "OU=CEH-Lab,$base"
        New-ADUser -Name 'svc_sql' -SamAccountName 'svc_sql' -Title 'SQL Service Account' `
                   -Department 'IT' -Path $ou -AccountPassword $strong -Enabled $true `
                   -ChangePasswordAtLogon $false -Description 'CEH lab - strong-password Kerberoast (never cracks)'
    } else {
        Set-ADAccountPassword -Identity 'svc_sql' -NewPassword $strong -Reset
    }
    Set-ADUser -Identity 'svc_sql' -ServicePrincipalNames @{Add="MSSQLSvc/win10-tgt01.$DomainName:1434"}
    Write-Host '[+] svc_sql: SPN registered + strong password set (will NOT crack).' -ForegroundColor Cyan

    Write-Host '[OK] Kerberoast targets ready.' -ForegroundColor Green
    Write-Host '     Verify from Kali:' -ForegroundColor Green
    Write-Host '       impacket-GetUserSPNs -dc-ip <DC_IP> ceh.lab/<user> -request' -ForegroundColor Green
    Write-Host '       hashcat -m 13100 spn_hashes.txt /usr/share/wordlists/rockyou.txt --rules-file best64.rule' -ForegroundColor Green
}

# ---------------------------------------------------------------------------
#  Spray prep + lockout policy  (run on the DC)
# ---------------------------------------------------------------------------
function Invoke-SprayPolicy {
    Import-Module ActiveDirectory

    Write-Host '[!] ONE weak password is shared by a.fahmy, n.gamal, h.rashad (the spray hits these).' -ForegroundColor Yellow
    Write-Host '    Use something a spray wordlist contains, e.g. a Season+Year+symbol.' -ForegroundColor Yellow
    $spray = Read-Host -AsSecureString 'Shared WEAK spray password (3 accounts)'
    foreach ($s in @('a.fahmy','n.gamal','h.rashad')) {
        if (Get-ADUser -Filter "SamAccountName -eq '$s'" -ErrorAction SilentlyContinue) {
            Set-ADAccountPassword -Identity $s -NewPassword $spray -Reset
            Write-Host "[+] $s -> shared spray password" -ForegroundColor Cyan
        } else { Write-Host "[=] $s not found (run the S3 seed first)" -ForegroundColor DarkGray }
    }

    Write-Host '[!] m.said gets a DISTINCT strong password - the account the spray MISSES.' -ForegroundColor Yellow
    $distinct = Read-Host -AsSecureString 'DISTINCT strong password for m.said'
    if (Get-ADUser -Filter "SamAccountName -eq 'm.said'" -ErrorAction SilentlyContinue) {
        Set-ADAccountPassword -Identity 'm.said' -NewPassword $distinct -Reset
        Write-Host '[+] m.said -> distinct strong password (spray will miss it).' -ForegroundColor Cyan
    }

    # Account-lockout policy so the "spraying is designed to avoid lockout" lesson is real.
    # Deliberately shallow (5 tries / 15 min) so a careless brute-force locks accounts in class.
    Write-Host '[+] Setting account-lockout policy: 5 attempts / 15-min window / 15-min lockout.' -ForegroundColor Cyan
    net accounts /lockoutthreshold:5 /lockoutwindow:15 /lockoutduration:15 /domain | Out-Null

    Write-Host '[OK] Spray targets + lockout policy ready.' -ForegroundColor Green
    Write-Host '     Verify from Kali (ONE password, MANY users - stays under lockout):' -ForegroundColor Green
    Write-Host '       nxc smb <DC_IP> -u users.txt -p "<the spray password>" --continue-on-success' -ForegroundColor Green
    Write-Host '     Expect: 3 hits (a.fahmy,n.gamal,h.rashad), m.said + svc accounts miss.' -ForegroundColor Green
}

# ---------------------------------------------------------------------------
#  Local crackable accounts  (run on EACH workstation: WIN7 + WIN10)
# ---------------------------------------------------------------------------
function Invoke-LocalAccounts {
    Write-Host '[!] Creating 2-3 LOCAL accounts with weak passwords for the SAM/hashcat lab.' -ForegroundColor Yellow
    Write-Host '    Local accounts only - nothing domain. Passwords prompted, never stored.' -ForegroundColor Yellow

    $names = @('labuser','helpdesk','svc_local')
    foreach ($n in $names) {
        $pw = Read-Host -AsSecureString "Weak password for LOCAL account '$n'"
        $existing = Get-LocalUser -Name $n -ErrorAction SilentlyContinue
        if ($existing) {
            Set-LocalUser -Name $n -Password $pw
            Write-Host "[=] $n exists - password reset" -ForegroundColor DarkGray
        } else {
            New-LocalUser -Name $n -Password $pw -FullName "CEH lab $n" `
                          -Description 'CEH lab - crackable SAM account' -PasswordNeverExpires | Out-Null
            Write-Host "[+] local user $n created" -ForegroundColor Cyan
        }
    }
    Write-Host '[OK] Local accounts ready for SAM dumping.' -ForegroundColor Green
    Write-Host '     Verify from Kali (needs a local admin credential):' -ForegroundColor Green
    Write-Host '       impacket-secretsdump ./Administrator@<WKSTN_IP>' -ForegroundColor Green
    Write-Host '       hashcat -m 1000 sam_hashes.txt /usr/share/wordlists/rockyou.txt' -ForegroundColor Green
}

# ---------------------------------------------------------------------------
#  LLMNR / NBT-NS status report  (run on WIN10-TGT01 - the poisoning victim)
# ---------------------------------------------------------------------------
function Invoke-CheckLLMNR {
    Write-Host '[i] Read-only check - this changes nothing.' -ForegroundColor Cyan

    $key = 'HKLM:\SOFTWARE\Policies\Microsoft\Windows NT\DNSClient'
    $llmnr = (Get-ItemProperty -Path $key -Name 'EnableMulticast' -ErrorAction SilentlyContinue).EnableMulticast
    if ($null -eq $llmnr -or $llmnr -ne 0) {
        Write-Host '[+] LLMNR is ENABLED (default) - this host is a valid Responder victim.' -ForegroundColor Green
    } else {
        Write-Host '[!] LLMNR is DISABLED by policy - Responder LLMNR poisoning will NOT work here.' -ForegroundColor Yellow
    }

    # NetBIOS over TCP/IP per-interface (2 = disabled, 0/1 = enabled/default)
    $nbt = Get-ChildItem 'HKLM:\SYSTEM\CurrentControlSet\Services\NetBT\Parameters\Interfaces' |
           ForEach-Object { (Get-ItemProperty $_.PSPath -Name NetbiosOptions -ErrorAction SilentlyContinue).NetbiosOptions } |
           Where-Object { $_ -ne $null }
    if ($nbt -contains 2 -and -not ($nbt -contains 0) -and -not ($nbt -contains 1)) {
        Write-Host '[!] NBT-NS is DISABLED on all interfaces.' -ForegroundColor Yellow
    } else {
        Write-Host '[+] NBT-NS is ENABLED (default) - NBT-NS poisoning is available.' -ForegroundColor Green
    }

    Write-Host ''
    Write-Host '  COUNTERMEASURE (teach this - do NOT apply in the lab, it kills the demo):' -ForegroundColor Cyan
    Write-Host '   LLMNR:  GPO > Computer Config > Admin Templates > Network > DNS Client >' -ForegroundColor DarkGray
    Write-Host '           "Turn off multicast name resolution" = Enabled  (EnableMulticast=0)' -ForegroundColor DarkGray
    Write-Host '   NBT-NS: DHCP option 001 Microsoft Disable NetBIOS, or per-NIC WINS tab >' -ForegroundColor DarkGray
    Write-Host '           "Disable NetBIOS over TCP/IP"  (NetbiosOptions=2)' -ForegroundColor DarkGray
    Write-Host '   Note: mDNS is now the fallback Microsoft is moving to - Responder poisons it too.' -ForegroundColor DarkGray
}

switch ($Stage) {
    'Kerberoast'    { Invoke-Kerberoast }
    'SprayPolicy'   { Invoke-SprayPolicy }
    'LocalAccounts' { Invoke-LocalAccounts }
    'CheckLLMNR'    { Invoke-CheckLLMNR }
}
