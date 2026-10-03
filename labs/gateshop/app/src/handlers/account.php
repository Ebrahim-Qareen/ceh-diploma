<?php
// Handlers: account area.
// Labs: massassign-profile, csrf-email, ssti-template, upload-avatar, ssrf-fetch, clickjacking.

function csrf_token(): string {
    if (empty($_SESSION['csrf'])) $_SESSION['csrf'] = bin2hex(random_bytes(16));
    return $_SESSION['csrf'];
}

function account_page(): void {
    $u = require_login();
    if ($_SERVER['REQUEST_METHOD'] === 'POST') { update_profile(); return; }

    $avatar = $u['avatar'] ? "<img class=avatar src='/uploads/".e($u['avatar'])."'>" : '';
    $body  = lab_banner('massassign-profile');
    $body .= "<h1>My account</h1>$avatar";
    $body .= "<p>Role: <b>".e($u['role'])."</b> · Balance: <b>$".e(number_format($u['balance'],2))."</b></p>";

    // Profile form. The CSRF lab: a hidden token is only required at secure level.
    $tok = is_secure('csrf-email') ? "<input type=hidden name=csrf value='".e(csrf_token())."'>" : '';
    $body .= "<form class=accform method=post action='/account'>$tok
        <label>Display name <input name=display_name value='".e($u['display_name'] ?? '')."'></label>
        <label>Email <input name=email value='".e($u['email'])."'></label>
        <button>Save profile</button></form>";
    $body .= "<p class=hint>Mass-assignment: try adding <code>role=admin</code> to this POST.</p>";

    // Signature (SSTI)
    $body .= "<h2>Email signature</h2>".lab_banner('ssti-template');
    $body .= "<form class=accform method=post action='/account/signature'>
        <textarea name=signature placeholder='Hi, {{ name }} here…'>".e($u['signature'] ?? '')."</textarea>
        <button>Preview &amp; save</button></form>";

    // Avatar upload + from URL
    $body .= "<h2>Avatar</h2>".lab_banner('upload-avatar');
    $body .= "<form class=accform method=post action='/account' enctype='multipart/form-data'>
        <input type=file name=avatar><button name=do value=upload>Upload file</button></form>";
    $body .= lab_banner('ssrf-fetch');
    $body .= "<form class=accform method=post action='/account/avatar-url'>
        <input name=url placeholder='https://…/photo.png'><button>Import from URL</button></form>";

    $body .= "<h2 class=danger>Danger zone</h2>".lab_banner('clickjacking');
    $body .= "<p><a href='/account/delete'>Delete my account…</a></p>";
    render('Account', $body);
}

function update_profile(): void {
    $u = require_login();
    // CSRF lab: token checked only at secure level.
    if (is_secure('csrf-email')) {
        // FIX:CSRF — require a per-session token on state-changing requests.
        if (!hash_equals($_SESSION['csrf'] ?? '', $_POST['csrf'] ?? '')) {
            http_response_code(403); render('Blocked', '<h1>403</h1><p>Missing/invalid CSRF token.</p>'); return;
        }
    }
    // ===== VULN:CSRF | CWE-352 | LAB:csrf-email =====
    // At insecure level the above check is skipped, so any cross-site POST can change the email. <-- the bug

    if (!empty($_FILES['avatar']['name'])) { upload_avatar(); return; }

    if (is_secure('massassign-profile')) {
        // FIX:MASSASSIGN — allow-list the fields a user may change.
        $allowed = ['display_name','email'];
        foreach ($allowed as $f) {
            if (isset($_POST[$f])) {
                $st = db()->prepare("UPDATE users SET `$f` = ? WHERE id = ?");
                $st->execute([$_POST[$f], $u['id']]);
            }
        }
    } else {
        // ===== VULN:MASSASSIGN | CWE-915 | LAB:massassign-profile =====
        // Every posted field is written to the user row — including role/balance. <-- the bug
        $cols = ['display_name','email','role','balance'];
        foreach ($cols as $f) {
            if (array_key_exists($f, $_POST)) {
                $st = db()->prepare("UPDATE users SET `$f` = ? WHERE id = ?");
                $st->execute([$_POST[$f], $u['id']]);
            }
        }
        // ===== END VULN:MASSASSIGN =====
    }
    flash('Profile saved.');
    redirect('/account');
}

function render_signature(): void {
    $u = require_login();
    $tpl = $_POST['signature'] ?? ($u['signature'] ?? '');
    db()->prepare('UPDATE users SET signature = ? WHERE id = ?')->execute([$tpl, $u['id']]);

    if (is_secure('ssti-template')) {
        // FIX:SSTI — treat the template as data: only substitute a known safe placeholder.
        $out = str_replace('{{ name }}', e($u['username']), e($tpl));
    } else {
        // ===== VULN:SSTI | CWE-1336 | LAB:ssti-template =====
        // Anything inside {{ }} is evaluated as PHP — template injection => RCE.
        $out = preg_replace_callback('/\{\{(.+?)\}\}/', function($m){
            return (string)@eval('return '.$m[1].';'); // <-- the bug
        }, $tpl);
        // ===== END VULN:SSTI =====
    }
    $body = lab_banner('ssti-template')."<h1>Signature preview</h1><div class=sigbox>$out</div>";
    $body .= "<p><a href='/account'>&larr; back</a></p><p class=hint>Try <code>{{ 7*7 }}</code> then <code>{{ system('id') }}</code>.</p>";
    render('Signature', $body);
}

function upload_avatar(): void {
    $u = require_login();
    if (empty($_FILES['avatar']['name'])) { redirect('/account'); }
    $name = $_FILES['avatar']['name'];
    $tmp  = $_FILES['avatar']['tmp_name'];
    $uploads = dirname(__DIR__, 2).'/public/uploads';
    @mkdir($uploads, 0777, true);

    if (is_secure('upload-avatar')) {
        // FIX:UPLOAD — allow-list real image types, ignore the client name, randomise.
        $info = @getimagesize($tmp);
        $okTypes = [IMAGETYPE_PNG=>'png', IMAGETYPE_JPEG=>'jpg', IMAGETYPE_GIF=>'gif'];
        if (!$info || !isset($okTypes[$info[2]])) { flash('Only PNG/JPG/GIF images allowed.'); redirect('/account'); }
        $safe = bin2hex(random_bytes(6)).'.'.$okTypes[$info[2]];
        move_uploaded_file($tmp, "$uploads/$safe");
    } else {
        // ===== VULN:UPLOAD | CWE-434 | LAB:upload-avatar =====
        // The client-supplied filename is trusted, so a .php file lands in a web-served dir => webshell.
        $safe = basename($name); // <-- the bug: keeps attacker's extension (e.g. shell.php)
        move_uploaded_file($tmp, "$uploads/$safe");
        // ===== END VULN:UPLOAD =====
    }
    db()->prepare('UPDATE users SET avatar = ? WHERE id = ?')->execute([$safe, $u['id']]);
    flash('Avatar updated: /uploads/'.$safe);
    redirect('/account');
}

function fetch_avatar_url(): void {
    $u = require_login();
    $url = $_POST['url'] ?? '';
    $result = '';
    if ($url !== '') {
        if (is_secure('ssrf-fetch')) {
            // FIX:SSRF — allow-list scheme + public host; block localhost/private ranges.
            $host = parse_url($url, PHP_URL_HOST) ?: '';
            $scheme = parse_url($url, PHP_URL_SCHEME) ?: '';
            $ip = $host ? gethostbyname($host) : '';
            $blocked = !in_array($scheme, ['http','https'], true)
                || filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_NO_PRIV_RANGE|FILTER_FLAG_NO_RES_RANGE) === false;
            if ($blocked) { $result = 'Blocked: only public http(s) hosts are allowed.'; }
            else { $result = @file_get_contents($url, false, stream_context_create(['http'=>['timeout'=>3]])); }
        } else {
            // ===== VULN:SSRF | CWE-918 | LAB:ssrf-fetch =====
            // The server fetches any URL the user supplies — including internal-only endpoints. <-- the bug
            $result = @file_get_contents($url, false, stream_context_create(['http'=>['timeout'=>3]]));
            // ===== END VULN:SSRF =====
        }
    }
    $body  = lab_banner('ssrf-fetch')."<h1>Import from URL</h1>";
    $body .= "<p>Server fetched: <code>".e($url)."</code></p><pre class=code>".e(substr((string)$result,0,2000))."</pre>";
    $body .= "<p class=hint>Try <code>http://127.0.0.1:8080/internal/flag</code> — the browser can't reach it, but the server can.</p>";
    $body .= "<p><a href='/account'>&larr; back</a></p>";
    render('Import URL', $body);
}

function delete_page(): void {
    require_login();
    $body = lab_banner('clickjacking')."<h1 class=danger>Delete account</h1>
        <p>This permanently deletes your account.</p>
        <form method=post action='/account/delete'><button class=danger>Yes, delete everything</button></form>";
    // Clickjacking lab: at insecure level this sensitive page allows framing (no X-Frame-Options/CSP).
    $allowFraming = !is_secure('clickjacking');
    // ===== VULN:CLICKJACKING | CWE-1021 | LAB:clickjacking =====
    // allow_framing => the page omits frame-busting headers, so it can be overlaid under a decoy. <-- the bug
    render('Delete account', $body, ['allow_framing'=>$allowFraming]);
}
