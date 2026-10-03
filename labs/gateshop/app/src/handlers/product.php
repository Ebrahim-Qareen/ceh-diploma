<?php
// Handlers: product page + reviews.
// Lab here: xss-stored (stored XSS via reviews).

function product_page(): void {
    $id = (int)($_GET['id'] ?? 1);
    $st = db()->prepare('SELECT * FROM products WHERE id = ?');
    $st->execute([$id]);
    $p = $st->fetch();
    if (!$p) { http_response_code(404); render('Not found', '<h1>No such product</h1>'); return; }

    $rv = db()->prepare('SELECT * FROM reviews WHERE product_id = ? ORDER BY id DESC');
    $rv->execute([$id]);
    $reviews = $rv->fetchAll();

    $list = '';
    foreach ($reviews as $r) {
        if (is_secure('xss-stored')) {
            $bodyTxt = e($r['body']); // FIX:XSS — encode stored content on output.
        } else {
            // ===== VULN:XSS (stored) | CWE-79 | LAB:xss-stored =====
            $bodyTxt = $r['body']; // <-- the bug: stored review rendered as raw HTML for every visitor.
            // ===== END VULN:XSS =====
        }
        $list .= "<div class=review><b>".e($r['author'])."</b><div>$bodyTxt</div></div>";
    }

    $body  = lab_banner('xss-stored');
    $body .= "<div class=product><div class=cat>".e($p['category'])."</div>";
    $body .= "<h1>".e($p['name'])."</h1><div class=price>$".e(number_format($p['price'],2))."</div>";
    $body .= "<p>".e($p['description'])."</p></div>";
    $body .= "<h2>Reviews</h2>".($list ?: "<p>No reviews yet.</p>");
    $u = current_user();
    $author = $u ? e($u['username']) : 'guest';
    $body .= "<form class=reviewform method=post action='/review'>
                <input type=hidden name=product_id value='".(int)$id."'>
                <input name=author value='$author'>
                <textarea name=body placeholder='Write a review…'></textarea>
                <button>Post review</button></form>";
    render('Product', $body);
}

function post_review(): void {
    $pid = (int)($_POST['product_id'] ?? 0);
    $author = trim($_POST['author'] ?? 'guest');
    $body = trim($_POST['body'] ?? '');
    if ($pid && $body !== '') {
        // Stored verbatim; the vulnerability is on OUTPUT (see product_page), which is where XSS is decided.
        $st = db()->prepare('INSERT INTO reviews(product_id,author,body) VALUES(?,?,?)');
        $st->execute([$pid, $author, $body]);
        flash('Review posted.');
    }
    redirect('/product?id='.$pid);
}
