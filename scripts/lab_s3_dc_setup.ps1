#Requires -RunAsAdministrator
<#
    CEH Diploma lab - Session 3 target prep (part 1 of 2)
    Promotes WINSRV19-TGT01 to a domain controller for ceh.lab and seeds
    throwaway directory objects so LDAP/SMB enumeration returns something.

    NO CREDENTIALS IN THIS FILE. Every secret is prompted for at run time.
    Run on WINSRV19-TGT01 only. Idempotent: safe to re-run.

    Usage:
      .\lab_s3_dc_setup.ps1 -Stage Promote      # step 1, reboots
      .\lab_s3_dc_setup.ps1 -Stage Seed         # step 2, after reboot
#>

[CmdletBinding()]
param(
    [ValidateSet('Promote','Seed')][string]$Stage = 'Promote',
    [string]$DomainName    = 'ceh.lab',
    [string]$NetbiosName   = 'CEH',
    [string]$ForestMode    = 'WinThreshold'
)

$ErrorActionPreference = 'Stop'

function Invoke-Promote {
    if ((Get-WmiObject Win32_ComputerSystem).DomainRole -ge 4) {
        Write-Host '[=] Already a domain controller - nothing to do.' -ForegroundColor Yellow
        return
    }

    Write-Host '[+] Installing AD DS + DNS roles...' -ForegroundColor Cyan
    Install-WindowsFeature -Name AD-Domain-Services, DNS -IncludeManagementTools | Out-Null

    Write-Host "[+] Promoting to domain controller for $DomainName" -ForegroundColor Cyan
    $dsrm = Read-Host -AsSecureString 'DSRM (Directory Services Restore Mode) password'

    Import-Module ADDSDeployment
    Install-ADDSForest `
        -DomainName                    $DomainName `
        -DomainNetbiosName             $NetbiosName `
        -ForestMode                    $ForestMode `
        -DomainMode                    $ForestMode `
        -SafeModeAdministratorPassword $dsrm `
        -InstallDns:$true `
        -CreateDnsDelegation:$false `
        -NoRebootOnCompletion:$false `
        -Force:$true
}

function Invoke-Seed {
    Import-Module ActiveDirectory

    $base = (Get-ADDomain).DistinguishedName
    $ouName = 'CEH-Lab'
    $ouPath = "OU=$ouName,$base"

    if (-not (Get-ADOrganizationalUnit -Filter "Name -eq '$ouName'" -ErrorAction SilentlyContinue)) {
        Write-Host "[+] Creating OU $ouName" -ForegroundColor Cyan
        New-ADOrganizationalUnit -Name $ouName -Path $base -ProtectedFromAccidentalDeletion $false
    }

    Write-Host '[!] Set one lab password for all seeded accounts (throwaway, lab-only).' -ForegroundColor Yellow
    $labPw = Read-Host -AsSecureString 'Lab account password'

    # Deliberately mundane, fictional accounts. Nothing real, nothing sensitive.
    $users = @(
        @{ S='a.fahmy';  N='A. Fahmy';   T='Helpdesk Technician'   ; D='IT'      },
        @{ S='m.said';   N='M. Said';    T='Systems Administrator' ; D='IT'      },
        @{ S='n.gamal';  N='N. Gamal';   T='Accounts Payable'      ; D='Finance' },
        @{ S='h.rashad'; N='H. Rashad';  T='HR Coordinator'        ; D='HR'      },
        @{ S='svc_backup'; N='svc_backup'; T='Service Account'     ; D='IT'      }
    )

    foreach ($u in $users) {
        if (Get-ADUser -Filter "SamAccountName -eq '$($u.S)'" -ErrorAction SilentlyContinue) {
            Write-Host "[=] user $($u.S) exists" -ForegroundColor DarkGray
            continue
        }
        Write-Host "[+] Creating user $($u.S)" -ForegroundColor Cyan
        New-ADUser -Name $u.N -SamAccountName $u.S -Title $u.T -Department $u.D `
                   -Path $ouPath -AccountPassword $labPw -Enabled $true `
                   -ChangePasswordAtLogon $false -Description "CEH lab account - $($u.T)"
    }

    foreach ($g in @('Lab-Helpdesk','Lab-Finance','Lab-ServerAdmins')) {
        if (-not (Get-ADGroup -Filter "Name -eq '$g'" -ErrorAction SilentlyContinue)) {
            Write-Host "[+] Creating group $g" -ForegroundColor Cyan
            New-ADGroup -Name $g -GroupScope Global -GroupCategory Security -Path $ouPath
        }
    }

    Add-ADGroupMember -Identity 'Lab-Helpdesk'     -Members 'a.fahmy'  -ErrorAction SilentlyContinue
    Add-ADGroupMember -Identity 'Lab-Finance'      -Members 'n.gamal'  -ErrorAction SilentlyContinue
    Add-ADGroupMember -Identity 'Lab-ServerAdmins' -Members 'm.said'   -ErrorAction SilentlyContinue

    # A readable share so SMB enumeration has a non-default share to find.
    $share = 'C:\LabShare'
    if (-not (Test-Path $share)) { New-Item -ItemType Directory -Path $share | Out-Null }
    if (-not (Get-SmbShare -Name 'LabDocs' -ErrorAction SilentlyContinue)) {
        Write-Host '[+] Creating SMB share LabDocs' -ForegroundColor Cyan
        New-SmbShare -Name 'LabDocs' -Path $share -ReadAccess 'Domain Users' | Out-Null
    }
    'Lab file - nothing sensitive here.' | Set-Content (Join-Path $share 'readme.txt')

    Write-Host '[OK] Directory seeded.' -ForegroundColor Green
    Write-Host '     Verify from Kali:  ldapsearch -x -H ldap://<DC_IP> -b "DC=ceh,DC=lab" -s base' -ForegroundColor Green
}

switch ($Stage) {
    'Promote' { Invoke-Promote }
    'Seed'    { Invoke-Seed }
}
