<?php
// Handlers: home page + product search.
// Labs here: sqli-search (SQL injection), xss-reflected (reflected XSS).

function home_page(): void {
    $rows = db()->query('SELECT id,name,category,price FROM products ORDER BY id')->fetchAll();
    $cards = '';
    foreach ($rows as $p) {
        $cards .= "<a class=card href='/product?id=".(int)$p['id']."'>";
        $cards .= "<div class=cat>".e($p['category'])."</div><div class=pname>".e($p['name'])."</div>";
        $cards .= "<div class=price>$".e(number_format($p['price'],2))."</div></a>";
    }
    $body = "<h1>GateShop</h1><p class=lede>Everything a real shop has — and every bug Session 8 teaches.</p>";
    $body .= "<form class=searchbar action='/search'><input name=q placeholder='Search products…'><button>Search</button></form>";
    $body .= "<div class=grid>$cards</div>";
    render('Home', $body);
}

function search_products(): void {
    $q = $_GET['q'] ?? '';
    $pdo = db();

    if (is_secure('sqli-search')) {
        // FIX:SQLI — parameterised query; input is data, never query structure.
        $stmt = $pdo->prepare("SELECT id,name,category,price FROM products WHERE name LIKE ? OR category LIKE ?");
        $stmt->execute(["%$q%", "%$q%"]);
        $rows = $stmt->fetchAll();
    } else {
        // ===== VULN:SQLI | CWE-89 | LAB:sqli-search =====
        // Root cause: the search term is concatenated straight into the SQL string.
        $sql = "SELECT id,name,category,price FROM products WHERE name LIKE '%$q%' OR category LIKE '%$q%'"; // <-- the bug
        $rows = $pdo->query($sql)->fetchAll();
        // ===== END VULN:SQLI =====
    }

    $cards = '';
    foreach ($rows as $p) {
        // A UNION injection returns columns that aren't products; show them generically.
        $name = $p['name'] ?? reset($p);
        $cards .= "<div class=card><div class=cat>".e($p['category'] ?? '')."</div>";
        $cards .= "<div class=pname>".e($name)."</div>";
        if (isset($p['price'])) $cards .= "<div class=price>".e($p['price'])."</div>";
        $cards .= "</div>";
    }

    if (is_secure('xss-reflected')) {
        $echo = e($q); // FIX:XSS — HTML-encode on output.
    } else {
        // ===== VULN:XSS (reflected) | CWE-79 | LAB:xss-reflected =====
        $echo = $q; // <-- the bug: user input echoed into HTML unescaped.
        // ===== END VULN:XSS =====
    }

    $body  = lab_banner('sqli-search');
    $body .= "<form class=searchbar action='/search'><input name=q value='".e($q)."'><button>Search</button></form>";
    $body .= "<p>Results for: <b>$echo</b></p>";
    $body .= "<div class=grid>".($cards ?: "<p>No products found.</p>")."</div>";
    render('Search', $body);
}
