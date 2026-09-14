#Requires -RunAsAdministrator
<#
    CEH Diploma lab - Session 5 target prep (exploitation, shells & payloads)
    Sibling to the S3/S4 seed scripts - it does NOT replace them. Most S5 targets
    are already prepared by S3/S4; this only sets up the buffer-overflow target.

    Stages:
      Vulnserver   - starts vulnserver.exe on WIN10-TGT01 (port 9999) and opens an
                     inbound firewall rule for 9999 so the fuzzer reaches it. The
                     rest of the host firewall is LEFT ON on purpose (Lab 4 needs the
                     bind shell blocked). Immunity Debugger + mona.py are manual GUI
                     installs - this script does not automate them.
      CheckEB      - READ-ONLY: reports whether SMBv1 is on and the host looks
                     unpatched for MS17-010 (the EternalBlue target check). Changes nothing.

    NO CREDENTIALS IN THIS FILE. Idempotent. Placeholders only.

    Usage (WIN10-TGT01 - the BOF target):
      .\lab_s5_setup.ps1 -Stage Vulnserver
    Usage (WIN7-TGT01 - verify the EternalBlue target):
      .\lab_s5_setup.ps1 -Stage CheckEB
#>
[CmdletBinding()]
param(
    [ValidateSet('Vulnserver','CheckEB')]
    [string]$Stage = 'Vulnserver',
    [string]$VulnserverPath = 'C:\Tools\vulnserver\vulnserver.exe'
)
$ErrorActionPreference = 'Stop'

function Invoke-Vulnserver {
    Write-Host '[!] Starting vulnserver on 9999 (buffer-overflow lab target).' -ForegroundColor Yellow
    if (-not (Test-Path $VulnserverPath)) {
        throw "vulnserver.exe not found at $VulnserverPath - install vulnserver + Immunity + mona first (manual)."
    }
    # inbound rule for the fuzzer to reach 9999 (rest of firewall stays ON for Lab 4)
    if (-not (Get-NetFirewallRule -DisplayName 'CEH Lab vulnserver 9999' -ErrorAction SilentlyContinue)) {
        New-NetFirewallRule -DisplayName 'CEH Lab vulnserver 9999' -Direction Inbound `
            -Action Allow -Protocol TCP -LocalPort 9999 | Out-Null
        Write-Host '[+] Inbound TCP 9999 allowed for vulnserver.' -ForegroundColor Cyan
    }
    Start-Process -FilePath $VulnserverPath
    Write-Host '[OK] vulnserver started. Attach Immunity Debugger and load mona, then run the fuzzer from Kali.' -ForegroundColor Green
    Write-Host '     Keep the rest of the host firewall ON - Lab 4 relies on the bind shell being blocked.' -ForegroundColor Green
}

function Invoke-CheckEB {
    Write-Host '[i] Read-only EternalBlue target check - changes nothing.' -ForegroundColor Cyan
    $smb1 = (Get-SmbServerConfiguration).EnableSMB1Protocol
    if ($smb1) { Write-Host '[+] SMBv1 is ENABLED - required for EternalBlue.' -ForegroundColor Green }
    else       { Write-Host '[!] SMBv1 is DISABLED - EternalBlue will NOT work here. Re-enable on the WIN7 lab box only.' -ForegroundColor Yellow }
    $hotfix = Get-HotFix -Id KB4012212 -ErrorAction SilentlyContinue   # the MS17-010 patch
    if ($hotfix) { Write-Host '[!] MS17-010 patch (KB4012212) is INSTALLED - target is patched.' -ForegroundColor Yellow }
    else         { Write-Host '[+] MS17-010 patch not found - target looks vulnerable (confirm from Kali with the aux check).' -ForegroundColor Green }
    Write-Host '    From Kali: use auxiliary/scanner/smb/smb_ms17_010 ; set RHOSTS <win7> ; run' -ForegroundColor DarkGray
}

switch ($Stage) {
    'Vulnserver' { Invoke-Vulnserver }
    'CheckEB'    { Invoke-CheckEB }
}
