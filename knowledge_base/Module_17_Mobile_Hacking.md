---
source: web research (official CEH v13 syllabus + InfoSecTrain CEH Module 17)
session: 10
gap_topic: true
---

# Module 17 — Hacking Mobile Platforms

> **Gap topic:** no instructor-deck PDF exists for this module. Content
> built from official CEH syllabus topics and verified web sources.

## Official learning objectives (CEH Ch.17)

1. Explain Mobile Platform Attack Vectors
2. Explain Android Hacking
3. Explain iOS Hacking
4. Explain Mobile Device Management (MDM)
5. Explain Mobile Security Guidelines and Tools

## 1. Mobile Attack Vectors

### By category

| Category | Attack vectors |
|---|---|
| Device-based | Phishing, malware, rootkits, buffer overflow, data caching, SMiShing |
| App-based | Insecure data storage, weak encryption, runtime manipulation, malicious apps |
| Network-based | Rogue Wi-Fi APs, MITM, Bluetooth attacks (Bluesnarfing, Bluebugging), SS7 vuln, SIMjacker |
| Cloud/backend | Platform vulns, SQL injection, server-side exploits |

### Specific attack types

- **Agent Smith attack:** malware replaces legitimate apps with infected copies
- **OTP hijacking:** intercept one-time passwords via SIM swapping or SS7
- **Camfecting:** hijack camera/microphone via RAT malware
- **Jailbreaking/Rooting:** remove manufacturer security restrictions to gain full access

## 2. OWASP Mobile Top 10 (2024)

| # | Vulnerability | Impact |
|---|---|---|
| M1 | Improper credential usage | Hardcoded credentials, insecure API keys |
| M2 | Inadequate supply chain security | Compromised third-party SDKs/libraries |
| M3 | Insecure authentication/authorization | Weak auth mechanisms, broken access controls |
| M4 | Insufficient input/output validation | Injection attacks, data corruption |
| M5 | Insecure communication | Cleartext traffic, certificate pinning bypass |
| M6 | Inadequate privacy controls | Data leakage, excessive permissions |
| M7 | Insufficient binary protections | Reverse engineering, code tampering |
| M8 | Security misconfiguration | Debug flags enabled, improper permissions |
| M9 | Insecure data storage | Sensitive data in plaintext on device |
| M10 | Insufficient cryptography | Weak algorithms, poor key management |

## 3. Android Hacking

### Android architecture

Linux kernel → HAL → Native libraries + Android Runtime (ART) → Java API
Framework → Applications. APK = Android application package.

### Attack techniques

| Technique | Description |
|---|---|
| Reverse engineering APK | Decompile with `apktool`, `jadx`, `dex2jar` → analyze source |
| Repackaging | Modify APK, re-sign, redistribute with malware injected |
| ADB exploitation | Android Debug Bridge enabled → remote shell, file extraction |
| Drozer | Security assessment framework for Android apps |
| Exploit kits | Metasploit `android/meterpreter/reverse_tcp` payload |
| Intent sniffing | Intercept inter-component communication |
| Side-loading | Install malicious apps from outside Play Store |

### Android security model

App sandboxing, SELinux, permission system, Google Play Protect, verified
boot, encryption at rest.

## 4. iOS Hacking

### iOS architecture

Cocoa Touch → Media → Core Services → Core OS → Kernel (XNU).
Apps run in sandboxes. App Store is the primary distribution channel.

### Attack techniques

| Technique | Description |
|---|---|
| Jailbreaking | Remove iOS restrictions (unc0ver, checkra1n, Palera1n) |
| Malicious profiles | Install configuration profiles that change device settings |
| Side-loading | Install apps via enterprise certificates or AltStore |
| Keychain attacks | Extract stored credentials from jailbroken device |
| Network-based | Same MITM/proxy attacks as Android |

### iOS security model

App Store review, code signing, sandboxing, data protection API, Secure
Enclave (hardware), FaceID/TouchID.

## 5. Mobile Device Management (MDM) & BYOD

**MDM** = centralized management of mobile devices in an organization.
Capabilities: remote wipe, app management, policy enforcement, encryption,
geofencing.

**BYOD** (Bring Your Own Device) risks: data leakage, lost/stolen devices,
insecure networks, mixing personal and corporate data.

**Solutions:** MDM (VMware Workspace ONE, Microsoft Intune, MobileIron),
MAM (Mobile Application Management), containerization (separate work/
personal profiles).

## 6. Mobile Security Guidelines

- Keep OS and apps updated
- Don't jailbreak/root devices
- Use strong authentication (biometrics + PIN/passcode)
- Install apps only from official stores
- Review app permissions before installing
- Use VPN on public Wi-Fi
- Enable remote wipe capability
- Implement MDM for organizational devices
- Encrypt device storage
- Disable unnecessary features (Bluetooth, NFC when not in use)

## 7. Tools

**Android:** apktool, jadx, dex2jar, Drozer, Frida, MobSF, ADB.
**iOS:** Objection, Frida, Cydia, Clutch, class-dump.
**Both:** Burp Suite (proxy), Metasploit, Wireshark.
**MDM:** VMware Workspace ONE, Microsoft Intune, MobileIron, Jamf.
