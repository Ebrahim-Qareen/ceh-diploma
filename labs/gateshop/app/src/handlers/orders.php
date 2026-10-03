<?php
// Handlers: orders.
// Labs: idor-order (IDOR), pathtrav-invoice (path traversal).

function view_order(): void {
    $u = require_login();
    $id = (int)($_GET['id'] ?? 1);
    $st = db()->prepare('SELECT o.*, us.username FROM orders o JOIN users us ON us.id=o.user_id WHERE o.id = ?');
    $st->execute([$id]);
    $o = $st->fetch();

    if (!$o) { http_response_code(404); render('Not found', '<h1>No such order</h1>'); return; }

    if (is_secure('idor-order')) {
        // FIX:IDOR — the order must belong to the logged-in user.
        if ((int)$o['user_id'] !== (int)$u['id']) {
            http_response_code(403); render('Forbidden', '<h1>403</h1><p>That order isn\'t yours.</p>'); return;
        }
    }
    // ===== VULN:IDOR | CWE-639 | LAB:idor-order =====
    // At insecure level there is no ownership check — any id is shown. <-- the bug

    $body  = lab_banner('idor-order')."<h1>Order #".(int)$o['id']."</h1>";
    $body .= "<p>Customer: <b>".e($o['username'])."</b></p>";
    $body .= "<p>Total: <b>$".e(number_format($o['total'],2))."</b></p>";
    $body .= "<p>Placed: ".e($o['created'])."</p>";
    $body .= "<p><a href='/download?file=invoice-".(int)$o['id'].".txt'>Download invoice</a></p>";
    $body .= "<p class=hint>Change the id in the URL to read someone else's order.</p>";
    render('Order', $body);
}

function download_file(): void {
    require_login();
    $file = $_GET['file'] ?? 'invoice-1.txt';
    $dir = dirname(__DIR__, 3).'/data/invoices';

    if (is_secure('pathtrav-invoice')) {
        // FIX:PATHTRAV — strip any path, then confirm the resolved path stays inside the invoices dir.
        $path = $dir.'/'.basename($file);
        $real = realpath($path);
        if ($real === false || strpos($real, realpath($dir)) !== 0) {
            http_response_code(404); echo 'Not found'; return;
        }
    } else {
        // ===== VULN:PATHTRAV | CWE-22 | LAB:pathtrav-invoice =====
        $path = $dir.'/'.$file; // <-- the bug: user input joined to a path with no sanitisation (../ escapes the dir)
        // ===== END VULN:PATHTRAV =====
    }
    if (!is_file($path)) { http_response_code(404); echo 'Not found'; return; }
    header('Content-Type: text/plain');
    readfile($path);
}
