---
source: web research (official CEH v13 syllabus + InfoSecTrain CEH Module 12 parts 1-2)
session: 9
gap_topic: true
---

# Module 12 — Evading IDS, Firewalls, and Honeypots

> **Gap topic:** no instructor-deck PDF exists for this module. Content
> built from official CEH syllabus topics and verified web sources. Note
> that the instructor deck's Module 3 (Scanning) already covers some
> evasion basics (fragmentation, decoys, source-port manipulation) — this
> module expands on those.

## Official learning objectives (CEH Ch.12)

1. Explain IDS, IPS, Firewall, and Honeypot Concepts
2. Describe IDS, IPS, Firewall, and Honeypot Solutions
3. Explain Evading IDS Techniques
4. Explain Evading Firewalls Techniques
5. Explain IDS/Firewall Evading Tools
6. Explain Detecting Honeypots
7. Explain IDS/Firewall Evasion Countermeasures

## 1. Intrusion Detection Systems (IDS)

Monitors network or system activity for malicious behavior or policy
violations. Generates alerts for security personnel.

### IDS Types

| Type | Scope | Strengths |
|---|---|---|
| NIDS (Network-Based) | Monitors entire network traffic | Detects network-wide attacks, distributed deployment |
| HIDS (Host-Based) | Monitors individual host activity | Detects insider threats, file integrity monitoring |

### Detection Methods

| Method | How it works | Limitation |
|---|---|---|
| Signature-based | Matches traffic against known attack patterns | Cannot detect zero-days (no signature exists) |
| Anomaly-based | Learns normal baseline, flags deviations | Higher false positive rate |
| Stateful protocol analysis | Compares observed traffic against protocol specifications | Resource intensive |

### IDS vs IPS

| | IDS | IPS |
|---|---|---|
| Action | Detects and alerts (passive) | Detects and blocks (active, inline) |
| Placement | Out of band (mirrored traffic) | Inline (all traffic passes through it) |
| Impact of failure | Missed alerts | May block legitimate traffic |

### Alert Types

| Type | Description |
|---|---|
| True Positive | Attack detected correctly |
| False Positive | Normal activity flagged as attack (alert fatigue) |
| True Negative | Normal activity correctly ignored |
| False Negative | Attack not detected (most dangerous) |

## 2. Firewalls

Control incoming/outgoing network traffic based on security rules.

### Firewall Technologies

| Type | Layer | Description |
|---|---|---|
| Packet filtering | Network (L3) | Checks source/destination IP, ports, protocol |
| Circuit-level gateway | Session (L5) | Validates TCP handshakes, masks internal IPs |
| Application-level proxy | Application (L7) | Inspects application commands, content filtering |
| Stateful multilayer inspection | L3-L7 | Tracks active connections across multiple layers |
| NAT firewall | Network (L3) | Translates internal IPs, hides network topology |
| Next-Gen Firewall (NGFW) | L3-L7 | Deep packet inspection + application awareness + threat intelligence |

### Firewall Architecture

- **Bastion host:** hardened single entry point exposed to the internet
- **Screened subnet (DMZ):** buffer zone between internal network and internet
- **Multi-homed firewall:** multiple interfaces for network segmentation

## 3. Honeypots

Decoy systems designed to attract attackers and study their behavior.

| Interaction level | Detail | Examples |
|---|---|---|
| Low-interaction | Simulates few services (easy to deploy, limited data) | Honeyd, KFSensor, Specter |
| Medium-interaction | Simulates broader service range | Cowrie, Kippo |
| High-interaction | Full real OS/services (maximum data, high risk) | Real servers with monitoring |
| Pure | Replicates entire production network | Honeynet |

**Specialized:** malware honeypots, database honeypots, spam traps, spider
honeypots (detect web crawlers).

## 4. IDS Evasion Techniques

| Technique | Description |
|---|---|
| Packet fragmentation | Split malicious payload across fragments — IDS may not reassemble |
| Session splicing | Break attack across multiple small packets below IDS threshold |
| Unicode/polymorphic encoding | Encode payload so signature doesn't match |
| Insertion attack | Craft packets accepted by IDS but rejected by target — IDS sees benign; target sees attack |
| Evasion attack | Craft packets rejected by IDS but accepted by target |
| TTL manipulation | Set TTL so packets expire after IDS but before target (or vice versa) |
| Obfuscation | Use encrypted protocols (SSH tunnel, VPN) to hide traffic from IDS |
| Protocol-level evasion | Exploit differences in how IDS and target handle protocol ambiguities |
| Denial of service | Overwhelm IDS with traffic so it drops packets |
| Slow-rate attacks | Send attack traffic slowly enough that rate-based detection misses it |

## 5. Firewall Evasion Techniques

| Technique | Description |
|---|---|
| Port hopping | Use allowed ports (80, 443) for non-web traffic |
| Source port manipulation | Forge source port to appear as trusted service traffic |
| IP address spoofing | Forge source IP to bypass IP-based ACLs |
| Tunneling | Encapsulate blocked traffic inside allowed protocols (HTTP tunnel, DNS tunnel, ICMP tunnel) |
| Proxy chains | Route traffic through multiple proxies to obscure origin |
| Fragmentation | Fragment packets to bypass packet-filtering rules |
| Application-layer tunneling | Use allowed applications (SSH, SSL) to carry attack traffic |

## 6. Detecting Honeypots

- Probe for known honeypot signatures (default banners, response patterns)
- Check MAC address OUI against known VM vendors
- Analyze response times (honeypots often respond differently than real systems)
- Port scan for telltale honeypot service patterns
- Tools: Send-Safe Honeypot Hunter, Nessus honeypot detection plugins

## 7. Tools

**IDS:** Snort, Suricata, OSSEC (HIDS), Wazuh, Zeek (Bro).
**Firewalls:** iptables/nftables, pfSense, Cisco ASA, Palo Alto, FortiGate.
**Evasion:** Nmap (fragmentation, decoys, timing), fragroute, hping3,
Scapy (custom packet crafting), cryptcat (encrypted netcat).

## 8. Countermeasures

- Keep IDS/IPS signatures updated
- Use both signature and anomaly-based detection
- Deploy defense-in-depth (IDS + firewall + HIDS + SIEM)
- Implement full packet reassembly in IDS
- Use encrypted traffic inspection (SSL/TLS inspection) where policy allows
- Regularly test IDS/firewall rules with penetration testing
- Monitor for honeypot evasion attempts
- Implement proper network segmentation
