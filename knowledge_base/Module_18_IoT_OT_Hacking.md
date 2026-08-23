---
source: web research (official CEH v13 syllabus + InfoSecTrain CEH Module 18)
session: 10
gap_topic: true
---

# Module 18 — IoT and OT Hacking

> **Gap topic:** no instructor-deck PDF exists for this module (deck only
> mentions IoT briefly in Module 9). Content built from official CEH
> syllabus topics and verified web sources.

## Official learning objectives (CEH Ch.18)

1. Explain IoT Concepts and IoT Hacking
2. Explain IoT Attack Methodology
3. Explain IoT Hacking Countermeasures
4. Explain OT Concepts and OT Hacking
5. Explain OT Attack Methodology
6. Explain OT Hacking Countermeasures

---

## IoT Section

### 1. IoT Architecture (5-Layer Model)

| Layer | Function |
|---|---|
| Edge Technology | Sensors, actuators — collect data from physical world |
| Access Gateway | Bridges devices to network — protocol translation |
| Internet | Data transfer between gateway and cloud |
| Middleware | Data management, security, device management |
| Application | User-facing services, dashboards, controls |

### 2. IoT Communication Models

| Model | Description | Example |
|---|---|---|
| Device-to-Device | Direct wireless between devices | ZigBee light switch → bulb |
| Device-to-Cloud | Device connects directly to cloud | Smart thermostat → vendor cloud |
| Device-to-Gateway | Device connects via local hub | Z-Wave sensor → home hub → cloud |
| Back-End Data-Sharing | Cloud shares data across platforms | Health device → cloud → hospital system |

### 3. IoT Protocols

| Protocol | Layer | Use case |
|---|---|---|
| MQTT | Application | Lightweight pub/sub messaging (telemetry, sensors) |
| CoAP | Application | Constrained Application Protocol — REST-like for low-power devices |
| Zigbee | Network | Low-power mesh networking (home automation, 2.4GHz) |
| Z-Wave | Network | Low-power mesh (home automation, 900MHz, less interference) |
| BLE | Link | Bluetooth Low Energy — short-range, low power (wearables, beacons) |
| 6LoWPAN | Network | IPv6 over Low-Power Wireless — enables IP on constrained devices |
| LoRaWAN | Network | Long Range WAN — kilometers range, very low power |

### 4. IoT Attack Surface

| Surface | Examples |
|---|---|
| Device | Default/weak credentials, unpatched firmware, physical access (JTAG, UART) |
| Communication | Unencrypted traffic, protocol vulnerabilities, replay attacks |
| Cloud/backend | Insecure API, weak authentication, data leakage |
| Mobile app | Hardcoded credentials, insecure data storage, weak encryption |
| Ecosystem | Insecure updates (unsigned firmware), supply chain compromise |

### 5. IoT Hacking Methodology

1. **Information gathering** — Shodan, Censys, manufacturer docs, FCC ID lookup
2. **Vulnerability scanning** — Nmap, Nessus, firmware analysis
3. **Launching attacks** — exploit default creds, replay attacks, MITM, firmware modification
4. **Gaining access** — web interface exploitation, telnet/SSH brute-force, MQTT exploitation
5. **Maintaining access** — backdoor firmware, persistent malware

### 6. IoT Attack Types

| Attack | Description |
|---|---|
| DDoS via botnet | Compromise IoT devices into botnet (Mirai-style) |
| HVAC attacks | Manipulate building automation systems |
| Rolling code attack | Capture and replay garage door / car key signals |
| BlueBorne | Bluetooth vulnerability — RCE without pairing |
| Jamming | RF jamming to disrupt wireless communication |
| Sybil attack | Fake multiple identities to manipulate network behavior |
| MQTT exploitation | Subscribe to all topics (`#`), publish malicious commands |
| Firmware manipulation | Extract → reverse engineer → modify → reflash |
| Side-channel | Analyze power consumption or EM emissions to extract keys |

### 7. IoT Hacking Tools

- **Shodan / Censys** — search for exposed IoT devices
- **Firmware Mod Kit / Binwalk** — firmware extraction and analysis
- **Attify** — IoT pentesting framework
- **RFCrack** — RF signal capture and replay
- **HackRF** — software-defined radio for wireless attacks
- **MQTT Explorer** — connect to MQTT brokers, inspect topics
- **Nmap** — device discovery and service enumeration
- **Wireshark** — capture IoT traffic

### 8. IoT Countermeasures

- Change all default credentials
- Disable unnecessary services and ports
- Enable encrypted communication (TLS)
- Implement secure firmware update mechanisms (signed updates)
- Network segmentation (isolate IoT on separate VLAN)
- Regular vulnerability scanning
- Implement strong authentication (mutual TLS, certificates)
- Monitor IoT traffic for anomalies
- Physical security for device access points

---

## OT Section

### 9. OT/ICS/SCADA Concepts

| Term | Definition |
|---|---|
| OT (Operational Technology) | Hardware/software that monitors and controls physical devices and processes |
| ICS (Industrial Control Systems) | Systems used to control industrial processes (umbrella term) |
| SCADA (Supervisory Control and Data Acquisition) | Large-scale ICS for distributed processes (power grids, water systems) |
| PLC (Programmable Logic Controller) | Industrial computer that controls manufacturing equipment |
| DCS (Distributed Control System) | Automated control system distributed across a plant |
| RTU (Remote Terminal Unit) | Field device that interfaces with sensors/actuators |
| HMI (Human-Machine Interface) | Operator dashboard for monitoring/controlling processes |

### 10. IT vs OT

| | IT | OT |
|---|---|---|
| Priority | Confidentiality (CIA → C first) | Availability (AIC → A first) |
| Update cycle | Regular patching | Infrequent — uptime critical |
| Protocols | TCP/IP, HTTP | Modbus, DNP3, OPC, EtherNet/IP |
| Lifecycle | 3-5 years | 15-25+ years |
| Security maturity | Mature | Still evolving |

### 11. OT Attack Vectors

| Attack | Description |
|---|---|
| HMI exploitation | Gain access to operator interface to manipulate processes |
| PLC attacks | Reprogram PLCs to cause physical damage (Stuxnet-style) |
| Protocol exploitation | Abuse lack of authentication in Modbus/DNP3 |
| MITM on SCADA | Intercept and modify control commands |
| Spear-phishing OT staff | Target engineers with access to control networks |
| Supply chain | Compromise OT vendor software updates |

### 12. Notable OT Attacks

- **Stuxnet (2010)** — targeted Iranian nuclear centrifuges via PLC manipulation
- **Ukraine power grid (2015/2016)** — BlackEnergy/Industroyer malware caused blackouts
- **Colonial Pipeline (2021)** — ransomware disrupted US fuel supply
- **Triton/TRISIS (2017)** — targeted safety instrumented systems (SIS) in a petrochemical plant

### 13. OT Countermeasures

- Air-gap or strictly segment OT networks from IT networks
- Implement the Purdue Model for network architecture
- Use OT-specific IDS (e.g., Claroty, Dragos, Nozomi)
- Whitelisting over blacklisting for OT systems
- Regular security assessments by OT-aware teams
- Secure remote access (jump servers, MFA)
- Monitor for anomalous commands on industrial protocols
- Develop OT-specific incident response plans
