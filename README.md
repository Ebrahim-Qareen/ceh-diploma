<p align="center"><img src="assets/readme/banner.svg" alt="CEH Diploma — ITGate Academy" width="100%"></p>

<p align="center">
  <img src="https://skillicons.dev/icons?i=kali,linux,windows,bash,py,html,css,js,md&perline=9" alt="Stack">
</p>
<p align="center">
  <img src="https://img.shields.io/badge/exam-CEH%20v13%20%28312--50%29-E63946?style=for-the-badge" alt="CEH v13">
  <img src="https://img.shields.io/badge/Metasploit-lab-2A6478?style=for-the-badge&logo=metasploit&logoColor=white" alt="Metasploit">
  <img src="https://img.shields.io/badge/Burp_Suite-web-FF6633?style=for-the-badge&logo=burpsuite&logoColor=white" alt="Burp">
  <img src="https://img.shields.io/badge/Nmap-recon-4682B4?style=for-the-badge" alt="Nmap">
  <a href="https://ebrahim-qareen.github.io/ceh-diploma/"><img src="https://img.shields.io/badge/live%20site-open-22D3EE?style=for-the-badge&logo=githubpages&logoColor=white" alt="Live site"></a>
</p>

Instructor-led **Certified Ethical Hacker** (312-50) diploma. Every attack is taught with its detection. Third course in the ITGate path: SOC Analyst → **CEH** → eCIR → eCDFP.

**Live site →** https://ebrahim-qareen.github.io/ceh-diploma/

## How every topic is taught

<p align="center"><img src="assets/readme/teaching-loop.svg" alt="Teaching loop" width="100%"></p>

## Lab

<p align="center"><img src="assets/readme/lab-topology.svg" alt="Lab topology" width="100%"></p>

Same `nmap`, four different answers — that contrast is the lesson. Setup: [`labs/`](labs/).

## Layout

```
docs/                        # site: index.html + docs/session-XX/
design/topic_map.md          # topic → session, dependencies
design/design_system.md      # one look for every page
design/practice_platforms.md # THM / HTB / OTW rooms, access tier verified
labs/  exercises/  knowledge_base/
```

```bash
python3 -m http.server --directory docs 8000
```

© ITGate Academy · EC-Council CEH v13 referenced, not republished.
**Ebrahim Mohamed** — Lead Cybersecurity Instructor · SOC Analyst · [LinkedIn](https://linkedin.com/in/EbrahimMohamed)
