<?php
// Handlers: DOM-XSS welcome page, information disclosure, SSRF internal target, instructor console.

function welcome_page(): void {
    // DOM-XSS lab lives in /assets/app.js (renderWelcome). The server only passes the current level.
    $secure = is_secure('xss-dom') ? '1' : '0';
    $body  = lab_banner('xss-dom');
    $body .= "<h1>Welcome</h1><div id=welcome data-secure='$secure'>Loading…</div>";
    $body .= "<p class=hint>Open <code>/welcome#name=Sam</code>, then <code>/welcome#name=&lt;img src=x onerror=alert(1)&gt;</code>. The part after # never reaches the server.</p>";
    render('Welcome', $body, ['dom_xss_js'=>true]);
}

function debug_page(): void {
    // ===== VULN:INFODISC | CWE-200 | LAB:infodisc-debug =====
    if (is_secure('infodisc-debug')) { http_response_code(404); render('Not found','<h1>404</h1>'); return; }
    header('Content-Type: text/plain');
    echo "GateShop DEBUG (should never be enabled in production)\n\n";
    echo "PHP: ".PHP_VERSION."\n";
    echo "DB_DRIVER: ".(getenv('DB_DRIVER')?:'mysql')."\n";
    echo "DB_HOST: ".(getenv('DB_HOST')?:'db')."  DB_NAME: ".(getenv('DB_NAME')?:'gateshop')."\n";
    echo "DB_USER: ".(getenv('DB_USER')?:'gateshop')."  DB_PASS: ".(getenv('DB_PASS')?:'gateshop')."\n";
    echo "REMEMBER_KEY: ".(getenv('REMEMBER_KEY')?:'lab-hmac-key-change-me')."\n";
    echo "Backup left in web root: /config.php.bak\n";
    // ===== END VULN:INFODISC =====
}

function backup_leak(): void {
    // A forgotten backup of a config file, served as text (classic info disclosure).
    if (is_secure('infodisc-debug')) { http_response_code(404); echo 'Not found'; return; }
    header('Content-Type: text/plain');
    echo "<?php\n// config.php.bak — left behind by mistake\n";
    echo "define('DB_PASS','gateshop');\n";
    echo "define('REMEMBER_KEY','".(getenv('REMEMBER_KEY')?:'lab-hmac-key-change-me')."');\n";
    echo "define('GATEBOT_SECRET','GATEBOT{internal-coupon-ADMIN50}');\n";
}

function internal_flag(): void {
    // SSRF target. In a real deployment this lives on an internal-only host the browser can't reach,
    // but the application server can — which is the whole point of SSRF.
    header('Content-Type: text/plain');
    echo "GateShop internal metadata service\n";
    echo "flag: GATEFLAG{ssrf-reached-the-internal-service}\n";
    echo "db_root_password: super-secret-root\n";
}

function instructor_console(): void {
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        if (($_POST['action'] ?? '') === 'reset') { seed_database(); flash('Lab reset to a clean state.'); redirect('/instructor'); }
        if (!empty($_POST['lab'])) { set_lab_level($_POST['lab'], $_POST['level'] ?? 'insecure'); redirect('/instructor'); }
    }
    $groups = [];
    foreach (labs() as $l) $groups[$l['group']][] = $l;

    $body = "<h1>Instructor console</h1><p class=lede>Every lab, its goal, the vulnerable code location, and a per-lab security toggle.</p>";
    $body .= "<form method=post action='/instructor' style='margin:12px 0'><button name=action value=reset class=danger>↺ Reset labs &amp; data</button></form>";
    foreach ($groups as $g => $items) {
        $body .= "<h2>$g</h2><table class=tbl><tr><th>lab<th>goal<th>vulnerable code<th>session<th>level</tr>";
        foreach ($items as $l) {
            $lvl = lab_level($l['slug']);
            $other = $lvl === 'secure' ? 'insecure' : 'secure';
            $toggle = "<form method=post action='/instructor' style='display:inline'>
                <input type=hidden name=lab value='".e($l['slug'])."'>
                <input type=hidden name=level value='$other'>
                <button class='pill $lvl'>$lvl → set $other</button></form>";
            $body .= "<tr>";
            $body .= "<td><a href='".e($l['url'])."'>".e($l['title'])."</a>";
            $body .= "<td>".e($l['goal']);
            $body .= "<td><code>".e($l['file'])."</code><br>".e($l['func'])." · <a href='/code?lab=".e($l['slug'])."' target=_blank>show</a>";
            $body .= "<td>".e($l['session']);
            $body .= "<td>$toggle</tr>";
        }
        $body .= "</table>";
    }
    render('Instructor', $body);
}
