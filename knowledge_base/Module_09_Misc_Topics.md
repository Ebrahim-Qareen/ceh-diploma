---
source: Module 9 miscellaneous topics.pdf (instructor deck, full)
session: 9, 10
---

# Module 9 — Miscellaneous Topics (Sniffing, Social Engineering, Wireless, DoS, Cloud/IoT)

> The instructor deck bundles several CEH chapters into one "miscellaneous"
> module. This maps to CEH Ch.8 (Sniffing), Ch.9 (Social Engineering),
> Ch.10 (DoS/DDoS), Ch.16 (Wireless), and brief coverage of Ch.19 (Cloud)
> and Ch.18 (IoT). Sessions 9 and 10 in our course draw from this material
> plus gap-topic supplements.

## Official learning objectives covered

- Ch.8: Sniffing concepts, MAC/ARP/DHCP attacks, spoofing, tools, countermeasures
- Ch.9: Social engineering concepts, techniques, insider threats, countermeasures
- Ch.10: DoS/DDoS concepts, botnets, attack techniques, countermeasures
- Ch.16: Wireless network concepts, encryption, threats, hacking methodology, tools
- Ch.18-19: IoT/Cloud basics (partial — gap topics need supplementing)

---

## 1. Social Engineering (CEH Ch.9)

The art of convincing people to reveal confidential information. Exploits
human psychology, not technical vulnerabilities. Depends on unaware
employees.

**Tool:** Social Engineering Toolkit (**SET** / `setoolkit` on Kali) —
automates phishing pages, credential harvesting, payload delivery.

**Attack types:** phishing (email), spear phishing (targeted), vishing
(voice), smishing (SMS), pretexting, baiting, tailgating, quid pro quo,
watering hole.

**Countermeasures:** security awareness training, verify requests through
separate channels, multi-factor authentication, clear policies for
sensitive information disclosure.

---

## 2. DoS and DDoS Attacks (CEH Ch.10)

**DoS** = Denial of Service — overwhelm a target to make it unavailable.
**DDoS** = Distributed DoS — multiple attacking systems (botnet).

**Techniques:** volumetric (bandwidth flooding), protocol (SYN flood,
Ping of Death), application-layer (HTTP flood, Slowloris).

**Countermeasures:** rate limiting, traffic filtering, CDN/DDoS protection
services, redundancy, incident response planning.

---

## 3. Sniffing Attacks (CEH Ch.8)

Capturing data in transit on a network.

| Type | Description |
|---|---|
| Passive sniffing | Monitor traffic on a shared medium (hub) — just listen |
| Active sniffing | On switched networks — requires ARP spoofing/poisoning to redirect traffic |

### Man-in-the-Middle (MITM) Attack

**ARP Spoofing/Poisoning:** attacker sends forged ARP replies to associate
their MAC with the gateway's IP → all traffic flows through attacker.

**Practical flow (from deck):**
1. Open Wireshark, filter for ARP
2. Open Ettercap, scan for hosts
3. Add target1 (victim) and target2 (gateway)
4. Launch ARP poisoning
5. Sniff HTTP credentials in transit

**Sniffing HTTPS:** SSL Strip / SSL Redirect — downgrade HTTPS to HTTP
to intercept credentials. Modern HSTS headers mitigate this.

**Tools:** Wireshark, Ettercap, arpspoof, Bettercap.

**Countermeasures:** use HTTPS everywhere, HSTS, encrypted protocols,
static ARP entries, port security, network segmentation, VPN.

---

## 4. Wireless Attacks (CEH Ch.16)

### Wireless Security Protocols

| Protocol | Security level | Notes |
|---|---|---|
| WEP | Broken | Crackable in minutes; never use |
| WPA/WPA2 | Standard | WPA2 with AES is current standard; vulnerable to handshake capture + offline cracking |
| WPA3 | Strongest | SAE (Simultaneous Authentication of Equals) — resistant to offline dictionary attacks |

### Wireless Attack Techniques

| Attack | Description |
|---|---|
| Deauthentication | Flood AP with deauth frames → disconnect all clients (DoS on wireless) |
| Evil twin | Clone target AP, deauth real AP → force clients to connect to fake AP |
| Handshake capture | Deauth → capture WPA2 4-way handshake during reconnection → crack offline |
| Replay attack | Replay captured authentication packets |

### Wireless Attack Flow (from deck)

1. `airmon-ng start wlan0` — put adapter in monitor mode
2. `airodump-ng wlan0mon` — scan for wireless networks
3. `airodump-ng -w capture -c <channel> --bssid <AP_MAC> wlan0mon` — target specific AP
4. `aireplay-ng --deauth 0 -a <AP_MAC> wlan0mon` — deauthentication attack
5. `aircrack-ng capture-01.cap -w rockyou.txt` — crack captured handshake

**Tools:** airmon-ng, airodump-ng, aireplay-ng, aircrack-ng (Aircrack-ng
suite), Wifite, Hashcat (GPU cracking).

---

## 5. Cloud Computing (CEH Ch.19 — partial)

On-demand computer services over the internet.

### Deployment Models

| Model | Access |
|---|---|
| Public | Accessible to all (AWS, Azure, GCP) |
| Private | Accessible to authorized org members only |
| Hybrid | Mix of public and private |
| Community | Shared among specific organizations |

### Service Models

| Model | What you get | Examples |
|---|---|---|
| SaaS | Software | Gmail, Salesforce, Office 365 |
| PaaS | Platform | Heroku, Google App Engine |
| IaaS | Infrastructure | AWS EC2, Azure VMs |

> **Note:** Cloud security topics (shared responsibility, S3 bucket
> misconfiguration, IAM, container security) need supplementing from
> official CEH Ch.19 material — the instructor deck only covers basics.

---

## 6. IoT (CEH Ch.18 — partial)

> **Note:** The instructor deck mentions IoT/OT only briefly in the course
> outline. Full IoT hacking content (MQTT, Zigbee, firmware analysis,
> Shodan for IoT) needs supplementing from official CEH Ch.18 material.

---

## Gap Topics Not Covered by Instructor Deck

The following CEH chapters have NO instructor-deck material and need to be
built from official sources + web research:

- **Ch.11 — Session Hijacking** (session tokens, cookie theft, CSRF, session fixation)
- **Ch.12 — Evading IDS, Firewalls, and Honeypots** (evasion techniques, tools, honeypot detection)
- **Ch.17 — Hacking Mobile Platforms** (Android/iOS attack vectors, OWASP Mobile Top 10)
- **Ch.18 — IoT and OT Hacking** (full content — only brief mention in deck)
- **Ch.19 — Cloud Computing** (full security content — only basics in deck)
