<?php
// Handler: cart + coupons.
// Lab: bizlogic-coupon (business logic — coupon reuse, negative quantity, price from client).

function cart_page(): void {
    require_login();
    if (!isset($_SESSION['cart'])) $_SESSION['cart'] = ['qty'=>1, 'product'=>1, 'discount'=>0, 'coupons'=>[]];
    if ($_SERVER['REQUEST_METHOD'] === 'POST') { apply_coupon(); return; }

    $c = $_SESSION['cart'];
    $st = db()->prepare('SELECT * FROM products WHERE id = ?'); $st->execute([$c['product']]);
    $p = $st->fetch() ?: ['name'=>'Item','price'=>10];
    $subtotal = $p['price'] * $c['qty'];
    $total = max(0, $subtotal - $c['discount']);

    $body  = lab_banner('bizlogic-coupon')."<h1>Cart</h1>";
    $body .= "<p>".e($p['name'])." &times; ".(int)$c['qty']." = $".e(number_format($subtotal,2))."</p>";
    $body .= "<p>Discount: -$".e(number_format($c['discount'],2))."</p>";
    $body .= "<p><b>Total: $".e(number_format($total,2))."</b></p>";
    $body .= "<form class=accform method=post action='/cart'>
        <label>Quantity <input name=qty value='".(int)$c['qty']."'></label>
        <label>Coupon <input name=coupon placeholder='SAVE10'></label>
        <button>Update</button></form>";
    $body .= "<p class=hint>Try quantity <code>-5</code>, or apply <code>SAVE10</code> several times.</p>";
    render('Cart', $body);
}

function apply_coupon(): void {
    require_login();
    $c = $_SESSION['cart'];
    $qty = (int)($_POST['qty'] ?? $c['qty']);
    $code = strtoupper(trim($_POST['coupon'] ?? ''));

    if (is_secure('bizlogic-coupon')) {
        // FIX:BIZLOGIC — quantity must be positive; each coupon counts once.
        $c['qty'] = max(1, $qty);
        if ($code && !in_array($code, $c['coupons'], true)) {
            $st = db()->prepare('SELECT percent FROM coupons WHERE code = ?'); $st->execute([$code]);
            if ($pct = $st->fetchColumn()) { $c['coupons'][] = $code; }
        }
        // recompute discount once from the single applied coupon set
        $pct = 0; foreach ($c['coupons'] as $cc) { $st=db()->prepare('SELECT percent FROM coupons WHERE code=?'); $st->execute([$cc]); $pct = max($pct,(int)$st->fetchColumn()); }
        $st = db()->prepare('SELECT price FROM products WHERE id=?'); $st->execute([$c['product']]);
        $c['discount'] = ($st->fetchColumn() * $c['qty']) * $pct/100;
    } else {
        // ===== VULN:BIZLOGIC | CWE-840 | LAB:bizlogic-coupon =====
        $c['qty'] = $qty; // <-- the bug: negative quantity allowed (turns the total into a credit)
        if ($code) {
            $st = db()->prepare('SELECT percent FROM coupons WHERE code = ?'); $st->execute([$code]);
            if ($pct = $st->fetchColumn()) {
                $st2 = db()->prepare('SELECT price FROM products WHERE id=?'); $st2->execute([$c['product']]);
                $c['discount'] += ($st2->fetchColumn() * max(0,$qty)) * $pct/100; // <-- the bug: stacks every time
            }
        }
        // ===== END VULN:BIZLOGIC =====
    }
    $_SESSION['cart'] = $c;
    redirect('/cart');
}
