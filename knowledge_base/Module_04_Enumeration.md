---
source: Module 4 Enumeration.pdf (instructor deck, full)
session: 3
---

# Module 4 — Enumeration

## Official learning objectives (CEH Ch.4)

1. Explain Enumeration Concepts
2. Perform NetBIOS Enumeration
3. Perform SNMP Enumeration
4. Perform LDAP Enumeration
5. Perform NFS Enumeration
6. Perform DNS Enumeration
7. Perform SMTP Enumeration
8. Perform SMB Enumeration
9. Perform RPC Enumeration
10. Explain Enumeration Countermeasures

## 1. Enumeration Concepts

Enumeration = creating active connections to a target system and performing
directed queries to extract detailed information. It's the third phase of
hacking (after recon → scanning → **enumeration** → gaining access).

Unlike scanning (which identifies what's alive and open), enumeration digs
deeper: usernames, shares, services, configurations, vulnerabilities.
Involves techniques like password attacks and brute-forcing.

## 2. HTTP Protocol (foundational for enumeration)

- **HTTP** = Hypertext Transfer Protocol — transfers web pages
- **HTTPS** = HTTP over SSL/TLS — encrypted
- Two main operations: **request** and **response**
- Main request types: **POST** (send data) and **GET** (retrieve data)

## 3. Enumeration Techniques and Tools

### Service-specific enumeration

| Service | Port(s) | Tool(s) | What you extract |
|---|---|---|---|
| HTTP/HTTPS | 80/443 | Nikto, Nmap NSE, Burp Suite | Directories, misconfigs, server info, vulns |
| NetBIOS | 137-139 | `nmap --script nbstat` | Hostnames, domain, MAC, logged-in users |
| SMB | 445 | enum4linux, Metasploit (`smb_enumshares`, `smb_version`) | Shares, users, OS version, domain info |
| NFS | 2049 | Metasploit (`nfs_showmount`) | Exported shares, mount points |
| SSH | 22 | Metasploit (`ssh_version`, `ssh_enumusers`) | SSH version, valid usernames |
| DNS | 53 | dnsrecon, nslookup, dig | Zone transfers, records, subdomains |

### Directory enumeration (advanced)

Using **SecLists** wordlists for comprehensive directory brute-forcing
(bigger and more targeted than default dirb/wfuzz lists).

### Manual enumeration

- **Banner grabbing** — connect to service, read the banner (version, OS
  info). Tools: netcat, telnet, curl.
- **Build your own enumeration tool** — instructor teaches writing a
  Python-based enumerator.

### Exploit searching

| Method | Tool/Resource | Notes |
|---|---|---|
| Local | `searchsploit` (Exploit-DB mirror on Kali) | Offline, fast |
| Public | Exploit-DB (exploit-db.com), CVE databases | Online, most current |

## 4. Countermeasures

- Disable unnecessary services and close unused ports
- Use firewalls to restrict access to enumerable services
- Rename default admin accounts
- Enforce strong authentication on all services
- **DNS:** disable zone transfers to unauthorized hosts
- Keep all services patched and updated
- Monitor for enumeration patterns (rapid queries, sequential probing)
