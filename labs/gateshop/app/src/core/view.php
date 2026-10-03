<?php
// GateShop core — minimal view layer + the "show vulnerable code" panel.

function render(string $title, string $body, array $opts = []): void {
    $u = current_user();
    $flash = flash();
    // Clickjacking lab: the delete page intentionally omits frame protections at insecure level.
    // Every other page sets them.
    if (empty($opts['allow_framing'])) {
        header("X-Frame-Options: DENY");
        header("Content-Security-Policy: frame-ancestors 'none'");
    }
    echo "<!doctype html><html lang=en><head><meta charset=utf-8>";
    echo "<meta name=viewport content='width=device-width,initial-scale=1'>";
    echo "<title>" . e($title) . " · GateShop</title>";
    echo "<link rel=stylesheet href='/assets/style.css'></head><body>";
    echo "<header class=topbar><a class=brand href='/'>🛒 GateShop <small>LAB</small></a><nav>";
    echo "<a href='/'>Shop</a><a href='/support'>Support</a><a href='/instructor'>Instructor</a>";
    if ($u) {
        echo "<a href='/account'>".e($u['username'])."</a>";
        if (($u['role']??'')==='admin') echo "<a href='/admin'>Admin</a>";
        echo "<a href='/logout'>Logout</a>";
    } else { echo "<a href='/login'>Login</a>"; }
    echo "</nav></header><main>";
    if ($flash) echo "<div class=flash>".e($flash)."</div>";
    echo $body;
    echo "</main><footer><div class=fnav>";
    echo "<a href='/about'>About</a><a href='/contact'>Contact</a><a href='/blog'>Blog</a>";
    echo "<a href='/faq'>FAQ</a><a href='/careers'>Careers</a><a href='/terms'>Terms</a><a href='/users'>People</a>";
    echo "</div><div>GateShop — intentionally vulnerable training lab. Keep it off the internet.</div></footer>";
    if (!empty($opts['dom_xss_js'])) echo "<script src='/assets/app.js'></script>";
    echo "</body></html>";
}

// Lab banner shown on each lab page: goal + current level + "show vulnerable code" link.
function lab_banner(string $slug): string {
    $l = lab_by_slug($slug); if (!$l) return '';
    $lvl = lab_level($slug);
    $cls = $lvl === 'secure' ? 'secure' : 'insecure';
    $h  = "<div class='labbar $cls'>";
    $h .= "<div class='lb-top'><span class='lb-tag'>LAB</span><b>".e($l['title'])."</b>";
    $h .= "<span class='lb-lvl'>level: ".e($lvl)."</span></div>";
    $h .= "<div class='lb-goal'>🎯 <b>Goal:</b> ".e($l['goal'])."</div>";
    $h .= "<div class='lb-links'><a href='/code?lab=".e($slug)."' target=_blank>&lt;/&gt; Show vulnerable code</a>";
    $h .= "<span class='lb-map'>maps to Session 8: ".e($l['session'])."</span></div>";
    $h .= "</div>";
    return $h;
}

// Read the lab's source file and show the function with VULN markers highlighted.
function show_code(string $slug): void {
    $l = lab_by_slug($slug);
    if (!$l) { http_response_code(404); echo 'Unknown lab'; return; }
    $root = dirname(__DIR__, 3);
    $path = $root . '/' . $l['file'];
    $src  = is_file($path) ? file_get_contents($path) : "(source not found: {$l['file']})";
    $lines = explode("\n", $src);
    $html = "<div class='code-head'><b>".e($l['title'])."</b><br>";
    $html .= "file: <code>".e($l['file'])."</code> · function: <code>".e($l['func'])."</code></div>";
    $html .= "<p class='code-note'>Lines tagged <code>VULN:</code> are the bug. The matching <code>FIX:</code> block is the secure version used when the lab level is <b>secure</b>.</p>";
    $html .= "<pre class='code'>";
    foreach ($lines as $i => $ln) {
        $n = $i + 1;
        $isVuln = (stripos($ln, 'VULN:') !== false) || (stripos($ln, '<-- the bug') !== false);
        $isFix  = (stripos($ln, 'FIX:') !== false);
        $cls = $isVuln ? ' class=vuln' : ($isFix ? ' class=fix' : '');
        $html .= "<span$cls><span class=ln>".str_pad((string)$n,3,' ',STR_PAD_LEFT)."</span> ".e($ln)."</span>\n";
    }
    $html .= "</pre>";
    echo "<!doctype html><html><head><meta charset=utf-8><title>Code · ".e($l['title'])."</title>";
    echo "<link rel=stylesheet href='/assets/style.css'></head><body class=codepage><main>".$html."</main></body></html>";
}
