#Requires -RunAsAdministrator
<#
    CEH Diploma lab - Session 3 target prep (part 2 of 2)
    Installs the SNMP Service on a Windows target and configures a READ-ONLY
    community string so snmpwalk / onesixtyone have something to enumerate.

    This is DELIBERATELY a weak configuration. It exists to be found in class.
    Say so out loud - a stock Windows Server does NOT ship like this.

    NO CREDENTIALS IN THIS FILE. The community string is prompted for.
    Idempotent: safe to re-run.

    Usage:  .\lab_s3_snmp_setup.ps1
#>

[CmdletBinding()]
param(
    [string]$Contact  = 'lab-admin',
    [string]$Location = 'CEH Lab - host-only network'
)

$ErrorActionPreference = 'Stop'

# --- 1. install the feature -------------------------------------------------
$feat = Get-WindowsFeature -Name SNMP-Service -ErrorAction SilentlyContinue
if ($feat -and -not $feat.Installed) {
    Write-Host '[+] Installing SNMP-Service...' -ForegroundColor Cyan
    Install-WindowsFeature -Name SNMP-Service -IncludeManagementTools | Out-Null
} else {
    Write-Host '[=] SNMP-Service already installed.' -ForegroundColor DarkGray
}

# --- 2. community string ----------------------------------------------------
Write-Host '[!] Use a GUESSABLE community string - the brute-force lab depends on it.' -ForegroundColor Yellow
$community = Read-Host 'Read-only SNMP community string'
if ([string]::IsNullOrWhiteSpace($community)) { throw 'Community string cannot be empty.' }

$commKey = 'HKLM:\SYSTEM\CurrentControlSet\Services\SNMP\Parameters\ValidCommunities'
New-Item -Path $commKey -Force | Out-Null
# 4 = READ ONLY
New-ItemProperty -Path $commKey -Name $community -PropertyType DWord -Value 4 -Force | Out-Null
Write-Host "[+] Community string configured read-only." -ForegroundColor Cyan

# --- 3. accept SNMP packets from the host-only network ----------------------
$permKey = 'HKLM:\SYSTEM\CurrentControlSet\Services\SNMP\Parameters\PermittedManagers'
New-Item -Path $permKey -Force | Out-Null
New-ItemProperty -Path $permKey -Name '1' -PropertyType String -Value 'localhost' -Force | Out-Null
# Any manager may query. Lab-only: never do this on a production host.
Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\SNMP\Parameters' `
                 -Name 'EnableAuthenticationTraps' -Value 1 -Force -ErrorAction SilentlyContinue

# --- 4. sysContact / sysLocation, so the MIB walk returns readable strings ---
$rfcKey = 'HKLM:\SYSTEM\CurrentControlSet\Services\SNMP\Parameters\RFC1156Agent'
New-Item -Path $rfcKey -Force | Out-Null
New-ItemProperty -Path $rfcKey -Name 'sysContact'  -PropertyType String -Value $Contact  -Force | Out-Null
New-ItemProperty -Path $rfcKey -Name 'sysLocation' -PropertyType String -Value $Location -Force | Out-Null
New-ItemProperty -Path $rfcKey -Name 'sysServices' -PropertyType DWord  -Value 79        -Force | Out-Null

# --- 5. firewall + restart ---------------------------------------------------
if (-not (Get-NetFirewallRule -DisplayName 'CEH Lab - SNMP UDP 161' -ErrorAction SilentlyContinue)) {
    New-NetFirewallRule -DisplayName 'CEH Lab - SNMP UDP 161' -Direction Inbound `
        -Protocol UDP -LocalPort 161 -Action Allow -Profile Any | Out-Null
    Write-Host '[+] Firewall rule added for UDP/161.' -ForegroundColor Cyan
}

Restart-Service -Name SNMP -Force
Write-Host '[OK] SNMP configured.' -ForegroundColor Green
Write-Host '     Verify from Kali:  snmpwalk -v2c -c <SNMP_COMMUNITY> <TARGET_IP> 1.3.6.1.2.1.1' -ForegroundColor Green
Write-Host '     Or find it:        onesixtyone -c /usr/share/wordlists/.../snmp.txt <TARGET_IP>' -ForegroundColor Green
