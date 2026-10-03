<?php
// Handlers: admin panel.
// Labs: cmdi-ping (OS command injection), xxe-import (XXE).

function require_admin(): array {
    $u = require_login();
    if (($u['role'] ?? '') !== 'admin') {
        http_response_code(403);
        render('Forbidden', '<h1>403</h1><p>Admins only. (Tip: the SQLi-login and mass-assignment labs get you here.)</p>');
        exit;
    }
    return $u;
}

function admin_page(): void {
    require_admin();
    $rows = db()->query('SELECT id,username,email,role,balance FROM users ORDER BY id')->fetchAll();
    $t = "<table class=tbl><tr><th>id<th>username<th>email<th>role<th>balance</tr>";
    foreach ($rows as $r) $t .= "<tr><td>".(int)$r['id']."<td>".e($r['username'])."<td>".e($r['email'])."<td>".e($r['role'])."<td>".e($r['balance'])."</tr>";
    $t .= "</table>";
    $body  = "<h1>Admin panel</h1>$t";
    $body .= "<p><a href='/admin/tools'>Network tools</a> · <a href='/admin/import'>Import products (XML)</a></p>";
    render('Admin', $body);
}

function net_ping(): void {
    require_admin();
    $host = $_POST['host'] ?? '';
    $out = '';
    if ($host !== '') {
        if (is_secure('cmdi-ping')) {
            // FIX:CMDI — validate as a hostname/IP and pass as a single, escaped argument.
            if (!preg_match('/^[A-Za-z0-9._-]+$/', $host)) { $out = 'Invalid host.'; }
            else { $out = shell_exec('ping -c 1 '.escapeshellarg($host).' 2>&1'); }
        } else {
            // ===== VULN:CMDI | CWE-78 | LAB:cmdi-ping =====
            // The host is placed straight into a shell command — `;`, `|`, `$(…)` all run. <-- the bug
            $out = shell_exec('ping -c 1 '.$host.' 2>&1');
            // ===== END VULN:CMDI =====
        }
    }
    $body  = lab_banner('cmdi-ping')."<h1>Network tools</h1>";
    $body .= "<form class=accform method=post action='/admin/tools'><input name=host placeholder='127.0.0.1'><button>Ping</button></form>";
    $body .= "<pre class=code>".e((string)$out)."</pre>";
    $body .= "<p class=hint>Try <code>127.0.0.1; id</code> or <code>127.0.0.1 | cat /etc/passwd</code>.</p>";
    render('Network tools', $body);
}

function import_xml(): void {
    require_admin();
    $xml = $_POST['xml'] ?? '';
    $out = '';
    if ($xml !== '') {
        if (is_secure('xxe-import')) {
            // FIX:XXE — reject DOCTYPE and forbid network/entity loading.
            if (stripos($xml, '<!DOCTYPE') !== false) { $out = 'DOCTYPE is not allowed.'; }
            else {
                $dom = new DOMDocument();
                @$dom->loadXML($xml, LIBXML_NONET);
                $out = $dom->textContent;
            }
        } else {
            // ===== VULN:XXE | CWE-611 | LAB:xxe-import =====
            // A permissive external-entity loader is installed, so external entities resolve (file://…). <-- the bug
            libxml_set_external_entity_loader(function($p,$system,$c){ return $system ? @fopen($system,'r') : null; });
            $dom = new DOMDocument();
            @$dom->loadXML($xml, LIBXML_NOENT | LIBXML_DTDLOAD);
            $out = $dom->textContent;
            libxml_set_external_entity_loader(null);
            // ===== END VULN:XXE =====
        }
    }
    $sample = "<?xml version=\"1.0\"?>\n<!DOCTYPE product [<!ENTITY secret SYSTEM \"file:///etc/passwd\">]>\n<product><name>&secret;</name></product>";
    $body  = lab_banner('xxe-import')."<h1>Import products (XML)</h1>";
    $body .= "<form class=accform method=post action='/admin/import'><textarea name=xml rows=8>".e($xml ?: $sample)."</textarea><button>Import</button></form>";
    $body .= "<h3>Parsed result</h3><pre class=code>".e((string)$out)."</pre>";
    render('Import XML', $body);
}
