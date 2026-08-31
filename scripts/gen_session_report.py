#!/usr/bin/env python3
"""
Generate the interactive per-session team report page (docs/session-NN/report.html)
from one shared template + per-session step data. Uses the shared design system
(assets/css/ceh.css) and the report engine (assets/js/report.js).

  python3 scripts/gen_session_report.py            # regenerate every session below
  python3 scripts/gen_session_report.py s3-scan    # just one

Each step's data fields (example / collect / why / name / cmd) are RAW HTML — write
entities where needed. Regenerating a page never changes its data-report id, so a
team's saved progress (localStorage) survives edits to the reference text.
One report per session; add a new key to SESSIONS to give a future session its own.
"""
import os, sys, io

DOCS = os.environ.get('CEH_DOCS') or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs')

TEAM_FIELDS = '''      <div class="rep-fields">
        <div class="rep-field"><label>Team name</label><input data-field="team" data-label="Team" placeholder="e.g. Team Nightowl" autocomplete="off"></div>
        <div class="rep-field"><label>Date</label><input data-field="date" data-label="Date" placeholder="2026-09-01" autocomplete="off"></div>
        <div class="rep-field wide"><label>Members</label><input data-field="members" data-label="Members" placeholder="Names of everyone on the team" autocomplete="off"></div>
        <div class="rep-field"><label>Target (in-scope host/domain)</label><input data-field="target" data-label="Target" placeholder="target.com" autocomplete="off"></div>
        <div class="rep-field"><label>Program / engagement</label><input data-field="program" data-label="Program" placeholder="HackerOne / Bugcrowd / lab engagement" autocomplete="off"></div>
        <div class="rep-field wide"><label>Scope URL (the policy / authorisation you read)</label><input data-field="scope_url" data-label="Scope URL" placeholder="https://…/security  ·  or the lab authorisation note" autocomplete="off"></div>
      </div>'''


def step_html(s):
    active = ' data-active' if s.get('active') else ''
    exlbl = s.get('exlabel', 'Example output')
    lis = ''.join('\n              <li>%s</li>' % x for x in s['collect'])
    return '''
      <div class="rep-step" data-step="{id}">
        <label class="rep-check"><input type="checkbox" data-check="{id}"{active}><span class="rep-box"></span></label>
        <div class="rep-main">
          <div class="rep-row"><span class="rep-name">{name}</span><code class="rep-cmd">{cmd}</code><button class="rep-toggle" aria-expanded="false"></button></div>
          <div class="rep-detail">
            <div class="rep-out"><div class="rep-lbl">{exlbl}</div><pre>{example}</pre></div>
            <div class="rep-collect"><div class="rep-lbl">Collect</div><ul>{lis}
            </ul></div>
            <div class="rep-why"><b>Why it matters later:</b> {why}</div>
          </div>
          <textarea class="rep-notes" data-notes="{id}" placeholder="{ph}"></textarea>
        </div>
      </div>'''.format(id=s['id'], active=active, name=s['name'], cmd=s['cmd'],
                       exlbl=exlbl, example=s['example'], lis=lis, why=s['why'], ph=s['ph'])


def free_html(f):
    return '''
      <div class="rep-free">
        <span class="rep-free-label">{label}</span>
        <p class="rep-free-hint">{hint}</p>
        <textarea data-notes="{id}" placeholder="{ph}"></textarea>
      </div>'''.format(label=f['label'], hint=f['hint'], id=f['id'], ph=f['ph'])


def build(key, d):
    n_steps = sum(1 for sec in d['sections'] for it in sec['items'] if it.get('t', 'step') == 'step')
    body = []
    for sec in d['sections']:
        body.append('\n      <h3 class="rep-sec">%s</h3>' % sec['name'])
        for it in sec['items']:
            body.append(free_html(it) if it.get('t') == 'free' else step_html(it))
    body = ''.join(body)

    return '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Session {num} — {title} | CEH · ITGate Academy</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="../assets/css/ceh.css">
<link rel="icon" href="../assets/img/itgate-logo.jpg">
</head>
<body>

<header class="topbar">
  <div class="wrap topbar-inner">
    <a class="brand" href="../index.html">
      <img src="../assets/img/itgate-logo.jpg" alt="ITGate Academy">
      <span class="brand-text">
        <span class="brand-name">ITGate Academy</span>
        <span class="brand-sub">CEH · Session {num} Report</span>
      </span>
    </a>
    <nav class="topnav">
      <a href="index.html">Session {snum_short}</a>
      <a href="../index.html">All sessions</a>
      <a href="../index.html#reports">All reports</a>
    </nav>
  </div>
</header>

<main class="wrap section">
  <div data-report="{key}" data-report-title="{report_title}">

    <div class="page-head">
      <div class="kicker"><span class="snum">S{num}</span><span class="tag lab">Team deliverable</span><span class="time">⏱ fill as you work</span></div>
      <h1>{title}</h1>
      <p class="lede">{lede}</p>
    </div>

    <div class="rep-head">
      <h2>Engagement header</h2>
      <p>Fill this once. It prints at the top of your exported report.</p>
{team}
    </div>

    <div class="rep-bar">
      <div class="rep-prog"><b data-progress>0 / {n} steps</b><span class="pbar"><span data-progress-bar></span></span></div>
      <div class="rep-actions">
        <span class="rep-saved" data-saved>saved ✓</span>
        <button class="rep-btn primary" data-export-html>⭳ Download HTML</button>
        <button class="rep-btn" data-export-pdf>🖨 Save as PDF</button>
        <button class="rep-btn ghost" data-clear>Clear</button>
      </div>
    </div>

    <div class="rep-gate" data-gate="{gate}"><b>⚠ Stop.</b> You have ticked an <b>active</b> step but your scope &amp; authorization check ({gate_up}) is not signed off. Confirm you are authorised to test this target first — active testing outside an authorised scope is illegal and voids safe harbour.</div>

    <div data-report-body>
{body}
    </div>

    <div class="box tip" style="margin-top:22px">
      <span class="box-t">How your team keeps this</span>
      <p>This report saves automatically in <strong>the browser you are using now</strong> — reopen the page on the same machine and it is still here. To hand it in or share it between teammates, use <strong>Download HTML</strong> (a single file) or <strong>Save as PDF</strong>. It does not sync between devices on its own.</p>
    </div>

  </div>
</main>

<footer class="footer">
  <div class="wrap footer-inner">
    <span>CEH Diploma · ITGate Academy · Session {snum_short} team deliverable</span>
    <span><a href="index.html">← Back to Session {snum_short}</a></span>
  </div>
</footer>

<script src="../assets/js/report.js"></script>
</body>
</html>
'''.format(num=d['num'], snum_short=str(int(d['num'])), title=d['title'], desc=d['desc'],
           key=key, report_title=d['report_title'], lede=d['lede'], team=TEAM_FIELDS,
           n=n_steps, gate=d['gate'], gate_up=d['gate'].upper(), body=body)


# ==========================================================================
#  Per-session data
# ==========================================================================
SESSIONS = {}

# ---- placeholder; real data appended below by data module ----

SESSIONS['s2-recon'] = {
  'num': '02', 'gate': 'a1',
  'title': 'Team Recon Report',
  'report_title': 'CEH Session 2 — Team Recon Report',
  'desc': 'CEH Diploma Session 2 team deliverable — an interactive recon checklist your team fills in against an authorised target, saves in the browser, and exports to HTML or PDF.',
  'lede': 'Work in your team against <strong>one authorised target</strong>. Tick each step as you do it, paste what you found, and click <em>example</em> to see what good output looks like and why it matters later. Everything saves in <strong>this browser</strong> — export to HTML or PDF to submit.',
  'sections': [
    {'name': 'A · Setup &amp; scope — do this first', 'items': [
      {'id':'a1','name':'Scope &amp; authorization check','cmd':'read the program policy — before any tool',
       'exlabel':'Example — what a scope page tells you',
       'example':'In scope:      *.target.com, api.target.com\nOut of scope:  blog.target.com (hosted WordPress)\nTesting:       automated scanning ALLOWED, max 5 req/s\nSafe harbour:  yes, if you stay in scope',
       'collect':['The exact <strong>in-scope</strong> domains/IPs — and the <strong>out-of-scope</strong> ones','Whether <strong>automated scanning is allowed</strong>, and any rate limit','Any required identifying header / test account','Whether the program offers <strong>safe harbour</strong>'],
       'why':'every step below must stay inside this scope. Touch an out-of-scope host and it is not a finding — it is unauthorised access. This line is what makes the whole engagement legal.',
       'ph':'In-scope: … | Out-of-scope: … | Scanning allowed? rate limit? | Safe harbour? …'},
    ]},
    {'name': 'B · Passive recon — no packets to the target', 'items': [
      {'id':'b1','name':'WHOIS / RDAP — who owns it','cmd':'whois target.com',
       'example':'Registrar:        MarkMonitor Inc.\nCreation Date:    2004-03-15\nRegistrant Org:   Target Holdings Ltd\nName Server:      NS1.TARGET.COM',
       'collect':['Registrant <strong>org name</strong> (pivot for cert / subdomain search)','The <strong>name servers</strong> — your AXFR targets in step C3','Domain <strong>age</strong> — old domains carry forgotten infrastructure'],
       'why':'the org name widens your subdomain hunt, and the name servers are exactly what you try a zone transfer against.',
       'ph':'Registrar / org / creation date / name servers…'},
      {'id':'b2','name':'DNS records','cmd':'dig target.com A MX NS TXT +noall +answer',
       'example':'target.com.  300 IN A    203.0.113.10\ntarget.com.  300 IN MX 10 mail.target.com.\ntarget.com.  300 IN TXT  "v=spf1 include:_spf.google.com ~all"',
       'collect':['<strong>A / AAAA</strong> IPs — the entry point for scanning','<strong>MX</strong> — the mail path','<strong>SPF / DMARC</strong> TXT — is spoofing possible?'],
       'why':'the IPs become Session 3&rsquo;s scan list; a missing/weak SPF or no DMARC is a phishing lead for Session 9.',
       'ph':'A/AAAA IPs / MX / NS / SPF-DMARC posture…'},
      {'id':'b3','name':'Certificate transparency — subdomains','cmd':"curl -s 'https://crt.sh/?q=%25.target.com&amp;output=json' | jq -r '.[].name_value' | sort -u",
       'example':'api.target.com\ndev.target.com\nuat.target.com\nvpn.target.com\nwww.target.com',
       'collect':['Every <strong>unique subdomain</strong> — especially <span class="mono">dev</span>, <span class="mono">uat</span>, <span class="mono">staging</span>, <span class="mono">vpn</span>','Names that hint at <strong>forgotten / internal</strong> systems'],
       'why':'subdomains ARE the attack surface. The old <span class="mono">uat</span> box is usually softer than the hardened homepage — you resolve and rank these in C1 and D1.',
       'ph':'Paste the subdomain list (or the interesting ones)…'},
      {'id':'b4','name':'Passive subdomain enumeration','cmd':'subfinder -d target.com -silent',
       'example':'www.target.com\napi.target.com\ncdn.target.com\nlegacy.target.com',
       'collect':['Merge with the crt.sh list into <strong>one master set</strong> of hosts','Note anything crt.sh did <strong>not</strong> already show'],
       'why':'different passive sources see different names — the union is your real host list, and it is the input to every active step.',
       'ph':'New hosts beyond crt.sh / total unique count…'},
      {'id':'b5','name':'Search-engine dorking','cmd':'site:target.com (ext:pdf | intitle:"index of" | inurl:admin)',
       'exlabel':'Example — dorks that pay off',
       'example':'site:target.com ext:pdf ext:xls    → exposed documents\nsite:target.com intitle:"index of"  → open directory listings\nsite:target.com inurl:admin|login   → portals\nsite:target.com "SQL syntax"        → leaky error pages',
       'collect':['Exposed <strong>documents</strong>, directory listings, <strong>admin / login</strong> portals','Error pages, exposed <strong>API docs</strong> / Swagger'],
       'why':'you found sensitive endpoints without a single packet at the app — these become web-testing targets in Session 8 and login targets in Session 4.',
       'ph':'Interesting URLs the dorks surfaced…'},
      {'id':'b6','name':'Exposed hosts &amp; tech — Shodan / Netcraft','cmd':'shodan host &lt;ip&gt;   ·   netcraft site report',
       'exlabel':'Example — Shodan host view',
       'example':'203.0.113.10  (Target Holdings Ltd, AS64500)\n  22/tcp   OpenSSH 7.4\n  443/tcp  nginx 1.18.0\n  8080/tcp Apache Tomcat 8.5.31   ← old',
       'collect':['Ports/services Shodan <strong>already</strong> saw (a free pre-scan)','<strong>Product + version</strong> banners, tech stack, hosting / ASN'],
       'why':'this is a no-touch preview of Session 3&rsquo;s scan, and every version string is a Session 4 CVE lookup (that Tomcat 8.5.31 is a lead).',
       'ph':'Ports / versions / tech / hosting seen passively…'},
      {'id':'b7','name':'Emails &amp; people OSINT','cmd':'theHarvester -d target.com -b bing,crtsh,duckduckgo',
       'example':'[emails]\na.hassan@target.com\nm.said@target.com\n[pattern] first-initial + lastname @ target.com',
       'collect':['Employee <strong>emails</strong> and the <strong>naming convention</strong> (predict the rest)','Likely <strong>usernames</strong>; any extra hosts (OWA / portal)'],
       'why':'the username convention is your Session 4 password-spray list, and the people are your Session 9 social-engineering targets. Mark generated emails "predicted", not "valid".',
       'ph':'Emails / naming convention / usernames…'},
    ]},
    {'name': 'C · Active recon — packets to the target (scope must be signed off)', 'items': [
      {'id':'c1','active':True,'name':'Resolve to live hosts','cmd':'subfinder -d target.com -silent | dnsx -silent -a -resp | httpx -silent -sc -title -td',
       'example':'https://www.target.com [200] [Target] [nginx]\nhttps://uat.target.com [200] [Staging Login] [Apache,PHP]\nhttps://vpn.target.com [200] [SSL VPN] [Fortinet]',
       'collect':['Which subdomains <strong>resolve AND are live</strong> (kill the dead ones)','Per host: <strong>status code, title, detected tech</strong>'],
       'why':'this turns a long passive list into the short list of <strong>real, reachable</strong> targets Session 3 actually scans.',
       'ph':'Live hosts + status + title + tech…'},
      {'id':'c2','active':True,'name':'Tech fingerprint','cmd':'whatweb -a3 https://uat.target.com',
       'example':'https://uat.target.com [200]\n  Apache[2.4.29], PHP[5.6.40], WordPress[5.2], WAF[none]',
       'collect':['Web server, <strong>CMS</strong>, frameworks, JS libs — <strong>with versions</strong>','Whether a <strong>WAF</strong> is present'],
       'why':'PHP 5.6 / WordPress 5.2 are direct CVE leads for Session 4; the CMS decides your Session 8 web attack path; "WAF: none" shapes Session 10 evasion.',
       'ph':'Server / CMS / frameworks / versions / WAF per host…'},
      {'id':'c3','active':True,'name':'Zone transfer attempt','cmd':'dig AXFR target.com @ns1.target.com',
       'exlabel':'Example — usually refused, occasionally a jackpot',
       'example':'# refused (the normal, secure case):\n; Transfer failed.\n\n# misconfigured (a high-severity finding):\nintranet.target.com. IN A 10.0.5.20  ← internal, leaked',
       'collect':['<strong>Refused</strong> or <strong>allowed</strong> — record it either way','If allowed: <strong>every record</strong>, especially internal names/IPs'],
       'why':'a successful AXFR dumps the whole host list at once — one of the highest-value recon findings there is. Try every name server from B1.',
       'ph':'Per name server: refused / allowed. If allowed, what leaked…'},
      {'id':'c4','active':True,'name':'Content / directory discovery','cmd':'ffuf -u https://uat.target.com/FUZZ -w common.txt -mc 200,301,403 -ac',
       'example':'admin        [Status: 301]\nbackup.zip   [Status: 200, Size: 4.1M]  ← !\n.git/        [Status: 403]\napi/v1       [Status: 200]',
       'collect':['Hidden <strong>dirs</strong>, <strong>admin/login</strong>, <strong>backups</strong> (.zip/.bak), config, <strong>API</strong> endpoints','<strong>403</strong>s — present but restricted (e.g. exposed <span class="mono">.git</span>)'],
       'why':'these endpoints are Session 8&rsquo;s web-testing surface and Session 4&rsquo;s login targets — a <span class="mono">backup.zip</span> or exposed <span class="mono">.git</span> can be the whole engagement.',
       'ph':'Paths found + status codes + anything juicy…'},
    ]},
    {'name': 'D · The deliverable — this is what you submit', 'items': [
      {'t':'free','id':'d1','label':'D1 · Ranked target list','hint':'Every live host, ordered by attacker interest — not by discovery order. This is the literal input to Session 3 scanning.',
       'ph':'# | host | IP | what it appears to be | why interesting | confidence | source\n1. uat.target.com | 203.0.113.20 | old staging login | PHP 5.6, no WAF, backup.zip exposed | high | httpx+ffuf'},
      {'t':'free','id':'d2','label':'D2 · Executive summary','hint':'3–5 sentences a non-technical manager reads. Overall exposure, the single worst finding, what to do this week. No jargon.','ph':'In three to five sentences…'},
      {'t':'free','id':'d3','label':'D3 · Scope statement','hint':'Confirm your work stayed inside the authorised scope.','ph':'All activity stayed within the in-scope domains listed in A1. No out-of-scope host was touched.'},
    ]},
  ],
}

SESSIONS['s3-scan'] = {
  'num': '03', 'gate': 'a1',
  'title': 'Team Scanning &amp; Enumeration Report',
  'report_title': 'CEH Session 3 — Team Scanning & Enumeration Report',
  'desc': 'CEH Diploma Session 3 team deliverable — an interactive scanning and enumeration checklist your team fills in against an authorised target, saves in the browser, and exports to HTML or PDF.',
  'lede': 'Take your Session 2 host list and make the target <strong>see you</strong>. Scanning is the loudest attacker stage — tick each step, paste what you found, click <em>example</em> for what good output looks like and why it matters next. Saves in <strong>this browser</strong>; export to HTML or PDF.',
  'sections': [
    {'name': 'A · Setup &amp; scope — do this first', 'items': [
      {'id':'a1','name':'Scope &amp; authorization check','cmd':'confirm scanning is allowed — before any packet',
       'exlabel':'Example — the line that authorises a scan',
       'example':'In scope:      203.0.113.0/24, *.target.com\nOut of scope:  shared/hosted assets\nTesting:       port scanning ALLOWED, max 5 req/s, no DoS\nWindow:        any time, identify with X-Bug-Hunter header',
       'collect':['That <strong>active scanning is explicitly allowed</strong>, and the <strong>rate limit</strong>','The in-scope <strong>IP ranges / hosts</strong> (scan nothing else)','Any forbidden test types (DoS, brute-force) and required test window'],
       'why':'a port scan is the first thing that reaches the target and the first thing its IDS logs. Everything below is active — outside an authorised scope it is an attack, not a test.',
       'ph':'Scanning allowed? rate limit? | In-scope ranges: … | Forbidden: DoS/brute? | Window …'},
    ]},
    {'name': 'B · Host discovery &amp; port scanning — packets to the target', 'items': [
      {'id':'b1','active':True,'name':'Live-host discovery','cmd':'nmap -sn 203.0.113.0/24 -oA sweep',
       'example':'Nmap scan report for 203.0.113.10  Host is up (0.011s)\nNmap scan report for 203.0.113.20  Host is up (0.009s)\nNmap done: 256 hosts, 4 up',
       'collect':['Which of your Session 2 hosts are actually <strong>up</strong>','New live IPs in-scope you did not have from recon'],
       'why':'you only scan live hosts — this trims the range so the loud full scan hits real targets, not dead space.',
       'ph':'Live IPs (from the sweep + your S2 list)…'},
      {'id':'b2','active':True,'name':'Full TCP port scan (SYN)','cmd':'nmap -sS -p- --min-rate 2000 -Pn 203.0.113.20 -oA allports',
       'example':'PORT     STATE SERVICE\n22/tcp   open  ssh\n80/tcp   open  http\n443/tcp  open  https\n3389/tcp open  ms-wbt-server\n8080/tcp open  http-proxy',
       'collect':['<strong>Every open TCP port</strong> per host (all 65535, not just top 1000)','Note the odd/high ports — they are where the interesting services hide'],
       'why':'this open-port list is the map for the rest of the session; each port becomes a service you enumerate in C, and a lead you rank in D.',
       'ph':'Open ports per host…'},
      {'id':'b3','active':True,'name':'Service &amp; version detection','cmd':'nmap -sV -sC -p22,80,443,3389,8080 203.0.113.20 -oA services',
       'example':'22/tcp   OpenSSH 7.4 (protocol 2.0)\n80/tcp   Apache httpd 2.4.29 ((Ubuntu))\n8080/tcp Apache Tomcat 8.5.31\n|_http-title: Staging Portal',
       'collect':['<strong>Service + exact version</strong> on every open port','Default-script findings (titles, certs, anonymous access)'],
       'why':'the version string is the whole game for Session 4 — <span class="mono">Tomcat 8.5.31</span> maps straight to a CVE. Vague "http" is useless; "Apache 2.4.29" is a lead.',
       'ph':'Service + version per port + any -sC script hits…'},
      {'id':'b4','active':True,'name':'OS detection','cmd':'nmap -O 203.0.113.20',
       'example':'Running: Linux 4.X\nOS CPE: cpe:/o:linux:linux_kernel:4.15\nOS details: Linux 4.15 - 5.6',
       'collect':['Best-guess <strong>OS and version</strong> per host','Whether it is Windows vs Linux — it changes every enumeration tool in C'],
       'why':'OS decides your toolset: SMB/LDAP for Windows, NFS/SSH for Linux — and Windows version hints at MS17-010-class exposure.',
       'ph':'OS guess per host…'},
      {'id':'b5','active':True,'name':'UDP top ports','cmd':'nmap -sU --top-ports 20 203.0.113.20',
       'example':'PORT    STATE         SERVICE\n53/udp  open          domain\n161/udp open          snmp   ← enumerate this\n500/udp open|filtered isakmp',
       'collect':['Open <strong>UDP</strong> services — especially <strong>161 (SNMP)</strong>, 53, 123, 500','TCP-only scans miss these entirely'],
       'why':'SNMP on 161 is a goldmine you enumerate in C3, and it is invisible to every TCP scan — this is the step teams forget.',
       'ph':'Open UDP ports (SNMP? DNS? IKE?)…'},
    ]},
    {'name': 'C · Enumeration — turn each service into detail', 'items': [
      {'id':'c1','active':True,'name':'Web (80/443/8080)','cmd':'whatweb https://203.0.113.20 ; nmap --script http-enum -p80,443,8080 203.0.113.20',
       'example':'HTTP/1.1 200  Apache/2.4.29  PHP/7.2\n/admin/    (Status: 401)\n/backup/   (Status: 200)\n/robots.txt (Status: 200)',
       'collect':['Server, framework, CMS + versions; <strong>directories &amp; admin panels</strong>','robots.txt, default pages, exposed backups'],
       'why':'feeds Session 8 web testing and Session 4 login targets; the version confirms your CVE leads from B3.',
       'ph':'Web tech / dirs / admin / backups per host…'},
      {'id':'c2','active':True,'name':'SMB (139/445)','cmd':'enum4linux-ng -A 203.0.113.20 ; nmap --script "smb-os-discovery,smb-enum-shares,smb-enum-users" -p445 203.0.113.20',
       'example':'OS: Windows Server 2019\nShares: ADMIN$, C$, IPC$, Backups (READ)\nUsers: administrator, svc_backup, m.said\n[note] modern Windows: null session refused',
       'collect':['<strong>Shares</strong> (readable ones especially), <strong>users</strong>, OS build, domain','Whether null/guest sessions work (legacy) or are refused (modern)'],
       'why':'usernames feed Session 4 spraying/Kerberoast; a readable share can hold creds; the modern-vs-legacy result tells you which attacks are even possible.',
       'ph':'Shares / users / OS / domain / null-session result…'},
      {'id':'c3','active':True,'name':'SNMP (161/udp)','cmd':'onesixtyone 203.0.113.20 public ; snmpwalk -v2c -c public 203.0.113.20',
       'example':'public   → community string valid\nsysDescr: Linux target 4.15\nhrSWRunName: /usr/sbin/sshd, mysqld, apache2\ninstalled software, listening ports, user accounts…',
       'collect':['A valid <strong>community string</strong> (try public/private/community)','Running processes, software, ports, user accounts, ARP tables'],
       'why':'a weak SNMP community string leaks the whole host inventory without a login — one of the fastest wins on the exam and in the field.',
       'ph':'Community string / sysDescr / processes / users leaked…'},
      {'id':'c4','active':True,'name':'LDAP / Active Directory (389/636)','cmd':'nmap --script ldap-rootdse -p389 dc.ceh.lab ; ldapsearch -x -H ldap://dc.ceh.lab -b "dc=ceh,dc=lab"',
       'example':'namingContext: DC=ceh,DC=lab\nCN=Administrator,CN=Users,DC=ceh,DC=lab\nCN=svc_sql,...  servicePrincipalName: MSSQL/...\nsAMAccountName: m.said, a.hassan',
       'collect':['The <strong>domain naming context</strong>, <strong>users</strong>, groups','Accounts with a <strong>servicePrincipalName</strong> (SPN) — Kerberoast targets'],
       'why':'this is the Session 4 attack surface: the user list is your spray list, and any SPN account is a Kerberoasting target.',
       'ph':'Domain / users / groups / SPN accounts…'},
      {'id':'c5','active':True,'name':'Other services (FTP/NFS/SMTP/RPC)','cmd':'showmount -e 203.0.113.30 ; smtp-user-enum -M VRFY -U users.txt -t 203.0.113.30 ; ftp 203.0.113.30',
       'example':'NFS: /home *  (world-readable export!)\nSMTP: 252 a.hassan (user exists)\nFTP: anonymous login ALLOWED',
       'collect':['Anonymous <strong>FTP</strong>, exported <strong>NFS</strong> shares, <strong>SMTP</strong> user enumeration','Any service that answers without a credential'],
       'why':'a world-readable NFS export or anonymous FTP is often a direct foothold, and SMTP VRFY confirms which usernames are real before you spray them.',
       'ph':'FTP anon? / NFS exports / SMTP valid users / RPC…'},
    ]},
    {'name': 'D · The deliverable — this is what you submit', 'items': [
      {'t':'free','id':'d1','label':'D1 · Target profile','hint':'One block per live host — the picture Session 4 attacks. This replaces a pile of tool dumps.',
       'ph':'host | IP | OS | open ports | service+version per port | key enum findings\n203.0.113.20 | Win2019 | 445,3389,8080 | SMB(2019), Tomcat 8.5.31 | shares: Backups(R); users: svc_backup,m.said'},
      {'t':'free','id':'d2','label':'D2 · Ranked exploitation leads','hint':'Version → likely weakness → which host. This is the direct input to Session 4 vulnerability analysis.',
       'ph':'1. Tomcat 8.5.31 on 203.0.113.20:8080 → known CVEs, check searchsploit\n2. svc_backup has SPN → Kerberoast candidate\n3. weak SNMP community on .30 → full inventory leak'},
      {'t':'free','id':'d3','label':'D3 · Detection note (the SOC flip)','hint':'What did your scans look like from the defender side? One line per noisy step — this is the tier-1 SOC skill.',
       'ph':'SYN scan → many SYNs, no ACK, from one source (firewall/IDS)\nSMB enum → 4625/anonymous logon events\nSNMP walk → burst of 161/udp from one host'},
      {'t':'free','id':'d4','label':'D4 · Scope statement','hint':'Confirm every packet stayed in scope.','ph':'All scanning stayed within the in-scope ranges in A1, within the stated rate limit. No out-of-scope host was scanned; no DoS/brute-force was run.'},
    ]},
  ],
}

SESSIONS['s4-access'] = {
  'num': '04', 'gate': 'a1',
  'title': 'Team Vulnerability &amp; Access Report',
  'report_title': 'CEH Session 4 — Team Vulnerability & Access Report',
  'desc': 'CEH Diploma Session 4 team deliverable — an interactive vulnerability-analysis and credential-attack checklist for the authorised lab domain, saved in the browser, exported to HTML or PDF.',
  'lede': 'Turn Session 3&rsquo;s services and users into a <strong>way in</strong>. Match versions to weaknesses, then attack authentication on the <strong>authorised lab domain</strong>. Tick each step, paste evidence, click <em>example</em> for what good output looks like. Saves in <strong>this browser</strong>; export to HTML or PDF.',
  'sections': [
    {'name': 'A · Setup &amp; scope — do this first', 'items': [
      {'id':'a1','name':'Authorization check','cmd':'confirm you are on the authorised lab domain',
       'exlabel':'Example — what authorises a credential attack',
       'example':'Authorised targets:  ceh.lab domain — dc, WIN10-TGT01, WIN7-TGT01,\n                     Metasploitable2 (host-only lab network only)\nAllowed:             vuln scan, offline cracking, spray (lockout aware),\n                     Kerberoast, LLMNR poisoning\nNever:               a real bug-bounty target — password attacks are out of\n                     scope on every public program',
       'collect':['The exact <strong>authorised lab hosts</strong> — nothing outside the lab network','That the destructive/loud attacks (spray, poisoning) are <strong>lab-only</strong>','Lockout policy so a spray does not lock real accounts'],
       'why':'credential attacks (spray, Kerberoast, LLMNR poisoning) are <strong>never</strong> authorised on a bug-bounty target — they belong on the lab. This step is the line between a lab exercise and a crime.',
       'ph':'Authorised lab hosts: … | Attacks allowed: … | Lockout policy: … | NOT a public target'},
    ]},
    {'name': 'B · Vulnerability analysis', 'items': [
      {'id':'b1','name':'Version → exploit mapping','cmd':'searchsploit apache tomcat 8.5.31',
       'example':'Apache Tomcat 8.5.31 - ... | multiple/webapps/xxxxx.txt\n... Remote Code Execution ...\n(searchsploit -x <path> to read; -m <id> to copy)',
       'collect':['For each version from Session 3: <strong>is there a public exploit?</strong>','Exploit type (RCE / auth-bypass / info-leak) and whether it needs a login'],
       'why':'this is the offline half — searchsploit reads a local DB, so it touches nothing. A confirmed public RCE is a top-priority line in your access plan.',
       'ph':'Per service+version: public exploit? type? needs creds?…'},
      {'id':'b2','name':'CVE / CVSS triage','cmd':'lookup on nvd.nist.gov — record CVE + CVSS base + vector',
       'example':'CVE-2020-1938 (Ghostcat, Tomcat AJP)\nCVSS 3.1 base: 9.8 CRITICAL\nvector: AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H',
       'collect':['The <strong>CVE id</strong>, <strong>CVSS base score</strong> and the <strong>vector</strong> (not just the number)','Whether it is network-reachable and needs no privileges (the vector tells you)'],
       'why':'the score ranks your leads and the vector tells you if it is actually reachable — a 9.8 that needs local access is not your first move.',
       'ph':'CVE / CVSS base / vector / reachable?…'},
      {'id':'b3','active':True,'name':'Automated vulnerability scan','cmd':'Nessus Essentials  ·  or  openvas / gvm  (authorised lab hosts)',
       'example':'203.0.113.20\n  CRITICAL  Tomcat AJP Ghostcat (CVE-2020-1938)\n  HIGH      SMB signing not required\n  MEDIUM    TLS 1.0 enabled',
       'collect':['Confirmed findings by <strong>severity</strong>, with the plugin/CVE reference','False positives to weed out (cross-check with B1/B2)'],
       'why':'the scanner is fast but noisy and wrong sometimes — you confirm its criticals against your own version work before they enter the access plan. It is active, so lab-only.',
       'ph':'Critical/High findings + CVE refs + which are confirmed…'},
    ]},
    {'name': 'C · Authentication &amp; password attacks — lab domain only', 'items': [
      {'id':'c1','active':True,'name':'Capture / dump hashes','cmd':'impacket-secretsdump ceh.lab/user@dc  ·  or Responder capture on the wire',
       'example':'administrator:500:aad3b...:31d6cfe0d16ae931b73c59d7e0c089c0:::\nsvc_backup:1104:aad3b...:e19ccf75ee54e06b06a5907af13cef42:::\n[SMB] NTLMv2 hash captured from WIN10-TGT01\\m.said',
       'collect':['<strong>NT hashes</strong> (from SAM/NTDS) or <strong>NetNTLMv2</strong> hashes (from the wire)','Which account each hash belongs to, and its privilege'],
       'why':'hashes are the raw material for C2 cracking and C4 Kerberoast; a captured admin hash may also enable pass-the-hash straight into Session 5.',
       'ph':'Hashes captured + account + source (SAM/NTDS/wire)…'},
      {'id':'c2','active':True,'name':'Offline cracking','cmd':'hashcat -m 1000 hashes.txt rockyou.txt   # 1000=NTLM, 5600=NetNTLMv2',
       'example':'e19ccf75ee54e06b06a5907af13cef42:Summer2026!\nStatus: Cracked  1/4\nsvc_backup → Summer2026!',
       'collect':['Which hashes <strong>cracked</strong>, and the <strong>plaintext</strong>','The right mode (1000 NTLM · 5600 NetNTLMv2 · 13100 Kerberoast · 1800 sha512crypt)'],
       'why':'a cracked service-account password is often domain-wide reuse — it becomes the credential in your access plan and the spray value in C3.',
       'ph':'Cracked user:password pairs + hash mode used…'},
      {'id':'c3','active':True,'name':'Password spraying','cmd':'netexec smb dc.ceh.lab -u users.txt -p "Summer2026!" --continue-on-success',
       'example':'SMB  dc.ceh.lab  [+] ceh.lab\\a.hassan:Summer2026! \nSMB  dc.ceh.lab  [-] ceh.lab\\m.said:Summer2026! (STATUS_LOGON_FAILURE)',
       'collect':['Accounts where <strong>one password worked</strong> across many users','Lockout threshold — <strong>one</strong> password per round, wait out the window'],
       'why':'spraying turns one cracked/guessed password into many footholds. Get the lockout math wrong and you lock the domain — which is why A1 recorded the policy.',
       'ph':'Valid user:password hits + lockout policy respected…'},
      {'id':'c4','active':True,'name':'Kerberoasting','cmd':'impacket-GetUserSPNs ceh.lab/user -request -dc-ip dc.ceh.lab',
       'example':'ServicePrincipalName  Name       \nMSSQL/dc.ceh.lab      svc_sql\n$krb5tgs$23$*svc_sql*... (hash for offline crack, mode 13100)',
       'collect':['<strong>SPN accounts</strong> and their <strong>TGS hashes</strong>','Feed the hashes to <span class="mono">hashcat -m 13100</span>'],
       'why':'any domain user can request these tickets — crack one offline and you own a service account, often with high privilege. A top exam and real-world technique.',
       'ph':'SPN accounts / TGS hashes captured / cracked?…'},
      {'id':'c5','active':True,'name':'LLMNR / NBT-NS poisoning','cmd':'sudo responder -I eth0 -wv   (lab segment only)',
       'example':'[*] Poisoned answer sent to WIN10-TGT01 for name \\\\fileshare\n[SMB] NTLMv2-SSP Hash captured: m.said::CEH:...\nSaved to Responder logs → crack with -m 5600',
       'collect':['<strong>NetNTLMv2 hashes</strong> captured from broadcast name lookups','Which hosts were poisoned and which users'],
       'why':'LLMNR/NBT-NS are still on by default in 2026 — poisoning silently harvests hashes that feed C2, closing the loop back to cracking.',
       'ph':'Hashes captured via poisoning + hosts/users…'},
    ]},
    {'name': 'D · The deliverable — this is what you submit', 'items': [
      {'t':'free','id':'d1','label':'D1 · Access plan','hint':'Per host, the chosen way in — the literal input to Session 5 exploitation.',
       'ph':'host | CVE + public exploit? | creds obtained + how | chosen way in\ndc.ceh.lab | Ghostcat CVE-2020-1938 (PoC yes) | svc_backup:Summer2026! (cracked NTLM) | PtH as svc_backup, else Ghostcat\nWIN10-TGT01 | — | m.said NetNTLMv2 (Responder, cracking) | spray reuse'},
      {'t':'free','id':'d2','label':'D2 · Detection note (the SOC flip)','hint':'What each attack wrote to the auth logs — the tier-1→tier-2 SOC skill.',
       'ph':'Spray → many 4625 (0xC000006A) from one source in a short window\nKerberoast → 4769 with RC4 (0x17) enc type\nResponder → LLMNR/NBT-NS traffic, logons from an unexpected host'},
      {'t':'free','id':'d3','label':'D3 · Scope statement','hint':'Confirm this stayed on the authorised lab.','ph':'All vulnerability scanning and credential attacks ran only against the authorised ceh.lab lab hosts on the host-only network. No public/bug-bounty target was touched. Lockout policy was respected during spraying.'},
    ]},
  ],
}


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for key, d in sorted(SESSIONS.items()):
        if only and key != only:
            continue
        out = os.path.join(DOCS, 'session-%s' % d['num'], 'report.html')
        html = build(key, d)
        io.open(out, 'w', encoding='utf-8', newline='').write(html)
        n = sum(1 for sec in d['sections'] for it in sec['items'] if it.get('t', 'step') == 'step')
        print('wrote %-40s  (%d steps)  %d bytes' % (out, n, len(html)))


if __name__ == '__main__':
    main()
