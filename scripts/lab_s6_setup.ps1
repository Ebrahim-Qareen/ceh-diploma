#Requires -RunAsAdministrator
<#
    CEH Diploma lab - Session 6 target prep (privilege escalation & CTF capstone)
    Windows side. Sibling to the S3/S4/S5 seed scripts - it does NOT replace them.
    Most S6 Windows targets are already prepared by S4/S5; this only reports the
    privesc surface and stages the credential-access mini-lab context. It does NOT
    weaken the host - the privilege abuse is what the STUDENT demonstrates.

    Linux privesc seeding (SUID / sudo / cron) lives in lab_s6_linux_setup.sh.

    Stages:
      CheckToken   - READ-ONLY: reports whether the current context holds
                     SeImpersonatePrivilege (PrintSpoofer / Potato prerequisite).
                     Changes nothing.
      CredContext  - Ensures a cached domain logon exists so Mimikatz
                     sekurlsa::logonpasswords returns material in Lab 4. Prompts
                     for the lab account - NO CREDENTIALS IN THIS FILE.
      CheckAll     - Runs both read-only reports.

    NO CREDENTIALS IN THIS FILE. Idempotent. Placeholders only.

    Usage (WIN10-TGT01):
      .\lab_s6_setup.ps1 -Stage CheckToken
      .\lab_s6_setup.ps1 -Stage CredContext
#>
[CmdletBinding()]
param(
    [ValidateSet('CheckToken','CredContext','CheckAll')]
    [string]$Stage = 'CheckAll'
)
$ErrorActionPreference = 'Stop'

function Show-TokenPrivs {
    Write-Host '[*] Privilege surface for the current context (token-abuse prerequisite):' -ForegroundColor Yellow
    $privs = (whoami /priv) 2>$null
    $imp = $privs | Select-String -Pattern 'SeImpersonatePrivilege','SeAssignPrimaryTokenPrivilege'
    if ($imp) {
        $imp
        Write-Host '[+] Impersonation privilege present -> PrintSpoofer / Potato is viable from this shell.' -ForegroundColor Green
    } else {
        Write-Host '[-] No impersonation privilege in this context. Get a service-account shell first (Lab 3 flow).' -ForegroundColor Red
    }
}

function Set-CredContext {
    Write-Host '[*] Credential-access mini-lab (Lab 4 / Mimikatz).' -ForegroundColor Yellow
    Write-Host '    A cached interactive logon for the lab account must exist so LSASS holds material.' -ForegroundColor Gray
    $u = Read-Host 'Lab domain account to cache (e.g. CEH\svc_backup) - placeholder, not stored'
    Write-Host "[i] Log in interactively once as $u (RunAs / RDP), then run Mimikatz from an elevated post-token shell." -ForegroundColor Cyan
    Write-Host '[i] This script deliberately does NOT store or set the password - seed it manually from the local creds file.' -ForegroundColor Gray
}

switch ($Stage) {
    'CheckToken'  { Show-TokenPrivs }
    'CredContext' { Set-CredContext }
    'CheckAll'    { Show-TokenPrivs; Write-Host ''; Write-Host '[i] Run -Stage CredContext to prep the Mimikatz mini-lab.' -ForegroundColor Gray }
}
Write-Host ''
Write-Host '[i] Capstone VMs (DoubleTrouble, Blackpearl) are VulnHub imports - no host seeding needed. Snapshot pre-s6 first.' -ForegroundColor Gray
