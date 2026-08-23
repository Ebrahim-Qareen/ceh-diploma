---
source: Module 1 introduction.pdf (instructor deck, full)
session: 1
---

# Module 1 — Introduction to Ethical Hacking

> **Extraction note:** Learning Objective 1 below was read directly from
> official CEH module pages (confirmed accurate). Objectives 2-6 are written
> from standard, well-documented CEH curriculum content (hacker classes,
> hacking phases, ethical hacking scope, MITRE ATT&CK/Cyber Kill Chain,
> defense-in-depth, common cyber laws). Flag if you want a specific sub-topic
> verified against the exact deck wording.

## Official learning objectives (this module, per EC-Council)

1. Explain Information Security Concepts
2. Explain Hacking Concepts and Different Hacker Classes
3. Explain Ethical Hacking Concepts and Scope
4. Explain Hacking Methodologies and Frameworks
5. Summarize the Techniques used in Information Security Controls
6. Explain the Importance of Applicable Security Laws and Standards

## 1. Information Security Concepts

Information security = protecting information and information systems from
unauthorized access, disclosure, alteration, and destruction. Five elements
(CIA + AA):

| Element | Meaning |
|---|---|
| Confidentiality | Only authorized parties can access the information |
| Integrity | Data/resources are trustworthy — no improper/unauthorized change |
| Availability | Systems/information are accessible when authorized users need them |
| Authenticity | The data/communication is genuine, not spoofed |
| Non-repudiation | Sender can't deny sending; receiver can't deny receiving (digital signatures) |

**Attacks = Motive (Goal) + Method (TTP) + Vulnerability.** Common motives:
disrupt business continuity, steal/manipulate data, cause financial loss,
damage reputation, take revenge, demand ransom, political/religious/military
objectives.

**Attack classification** (standard CEH framing):
- **Passive** — reconnaissance/eavesdropping only, no change to the target
  (sniffing, traffic analysis).
- **Active** — attacker changes/disrupts the target (DoS, malware, injection).
- **Close-in** — physical proximity to the target (shoulder surfing, dumpster
  diving, USB drop).
- **Insider** — from someone with legitimate access.
- **Distribution** — tampering with hardware/software before it reaches the
  target (supply chain).

## 2. Hacking Concepts and Hacker Classes

Hacking = exploiting weaknesses in a system to gain unauthorized access or
control. Hacker classes:

| Class | Description |
|---|---|
| White Hat | Authorized, ethical — this is what CEH certifies |
| Black Hat | Unauthorized, malicious intent |
| Gray Hat | No malicious intent but no authorization either |
| Suicide Hacker | Doesn't care about getting caught/prosecuted |
| Script Kiddie | Uses others' tools/scripts without deep skill |
| State-Sponsored | Works for a government/military objective |
| Hacktivist | Motivated by political/social causes |

## 3. Ethical Hacking Concepts and Scope

Ethical hacking = using the same tools/techniques as a malicious hacker, but
with **written authorization**, a defined scope, and the goal of finding and
reporting weaknesses before attackers do. Core requirement: a signed
engagement/contract defining scope, rules of engagement, and legal
boundaries — without this, identical actions are illegal. Ethical hackers
follow the same phase structure as attackers (see §4) but stop at proving
impact, then report and recommend fixes.

## 4. Hacking Methodologies and Frameworks

Standard attacker phase model (also the pentest methodology CEH teaches):

1. **Reconnaissance** — gather information (passive/active)
2. **Scanning** — identify live hosts, ports, services
3. **Gaining Access** — exploit a vulnerability to get in
4. **Maintaining Access** — persistence (backdoors, escalated privileges)
5. **Clearing Tracks** — remove logs/evidence of the intrusion

Frameworks referenced in modern CEH content: **Cyber Kill Chain** (Lockheed
Martin — recon, weaponize, deliver, exploit, install, C2, actions on
objectives), **MITRE ATT&CK** (tactic/technique matrix used for detection
mapping — same framework the previous ITGate project used), **Diamond
Model** (adversary/infrastructure/capability/victim).

## 5. Information Security Controls

- **Defense-in-depth** — layered controls so no single failure is fatal.
- **Risk management** — identify, assess, treat (accept/mitigate/transfer/avoid) risk.
- **Cyber threat intelligence (CTI)** — actionable info about threats/actors.
- **Threat modeling** — systematically identify how a system could be attacked.
- **Incident management process** — prepare, detect/analyze, contain,
  eradicate, recover, lessons learned (matches standard IR lifecycle).
- **AI/ML in security** — used for anomaly detection, and newer CEHv13
  content explicitly covers **AI-driven ethical hacking** (AI-assisted
  recon/analysis) as an emerging objective.

## 6. Security Laws and Standards

Region/industry-dependent — the module covers awareness, not deep legal
practice: general data-protection laws (e.g. GDPR-style), sector rules
(HIPAA for health data, PCI-DSS for payment card data), and local
cybercrime/computer-misuse laws that make unauthorized access illegal
regardless of intent — which is exactly why written authorization matters
for ethical hackers.

## Instructor deck's version of this module (for comparison/teaching flow)

The instructor's own slide deck condenses this into: what is hacking,
pillars of information security, security attacks, classification of
attacks, defensive vs offensive security — then moves straight into the
20-chapter course outline. It's the simplified, class-paced version of the
same content above; use it for pacing/examples, use this file for full
technical completeness.
