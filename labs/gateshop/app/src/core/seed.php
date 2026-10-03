<?php
// GateShop — schema + seed data. Idempotent: drops and recreates everything.
// Called on first boot and by the instructor console "Reset" button. Works on MySQL and SQLite.

function seed_database(): void {
    $pdo = db();
    $sqlite = db_driver() === 'sqlite';
    $AI = $sqlite ? 'INTEGER PRIMARY KEY AUTOINCREMENT' : 'INT AUTO_INCREMENT PRIMARY KEY';
    $eng = $sqlite ? '' : ' ENGINE=InnoDB DEFAULT CHARSET=utf8mb4';

    foreach (['order_items','orders','reviews','products','users','coupons','lab_levels'] as $t) {
        $pdo->exec("DROP TABLE IF EXISTS $t");
    }

    $pdo->exec("CREATE TABLE users (
        id $AI, username VARCHAR(64) UNIQUE, email VARCHAR(190), password VARCHAR(64),
        role VARCHAR(16), balance DECIMAL(10,2) DEFAULT 0, avatar VARCHAR(190),
        display_name VARCHAR(190), signature TEXT)$eng");
    $pdo->exec("CREATE TABLE products (
        id $AI, name VARCHAR(190), category VARCHAR(64), price DECIMAL(10,2), description TEXT)$eng");
    $pdo->exec("CREATE TABLE reviews (
        id $AI, product_id INT, author VARCHAR(190), body TEXT, created VARCHAR(32))$eng");
    $pdo->exec("CREATE TABLE orders (
        id $AI, user_id INT, total DECIMAL(10,2), created VARCHAR(32))$eng");
    $pdo->exec("CREATE TABLE coupons (code VARCHAR(32) PRIMARY KEY, percent INT)$eng");
    $pdo->exec("CREATE TABLE lab_levels (lab VARCHAR(64) PRIMARY KEY, level VARCHAR(16))$eng");

    // --- users (passwords stored as sha1 so the SQLi lab can 'dump the hashes') ---
    $adminPass = getenv('ADMIN_PASSWORD') ?: 'admin123'; // instructor sets this in .env
    $users = [
        ['admin','admin@gateshop.test',$adminPass,'admin',0],
        ['carlos','carlos@gateshop.test','carlos123','user',250],
        ['instructor','teacher@gateshop.test','teach123','admin',0],
        ['wiener','wiener@gateshop.test','peter','user',40],
        ['alice','alice@gateshop.test','alice2024','user',15],
        ['bob','bob@gateshop.test','qwerty','user',0],
        ['mike.dev','mike@gateshop.test','devpass','user',0],
        ['support','support@gateshop.test','support123','user',0],
    ];
    $st = $pdo->prepare('INSERT INTO users(username,email,password,role,balance,display_name) VALUES(?,?,?,?,?,?)');
    foreach ($users as $u) $st->execute([$u[0],$u[1],sha1($u[2]),$u[3],$u[4],ucfirst($u[0])]);

    // --- products ---
    $products = [
        ['Mechanical Keyboard','Peripherals',89.00,'Clicky switches, RGB, the works.'],
        ['Noise-cancelling Headphones','Audio',199.00,'Block out the open-plan office.'],
        ['USB-C Hub','Accessories',39.00,'Seven ports of productivity.'],
        ['4K Monitor','Displays',349.00,'27-inch, factory calibrated.'],
        ['Ergonomic Mouse','Peripherals',59.00,'Your wrist will thank you.'],
        ['Webcam 1080p','Accessories',69.00,'Look sharp on every call.'],
        ['Standing Desk','Furniture',429.00,'Sit, stand, repeat.'],
        ['Blue Coffee Mug','Gifts',12.00,'Ceramic, 350ml. In stock.'],
    ];
    $st = $pdo->prepare('INSERT INTO products(name,category,price,description) VALUES(?,?,?,?)');
    foreach ($products as $p) $st->execute($p);

    // --- reviews ---
    $st = $pdo->prepare('INSERT INTO reviews(product_id,author,body,created) VALUES(?,?,?,?)');
    $st->execute([1,'carlos','Best keyboard I have owned.','2026-09-20 09:00:00']);
    $st->execute([1,'wiener','A bit loud but great.','2026-09-21 14:30:00']);
    $st->execute([8,'carlos','Holds coffee. Does not disappoint.','2026-09-22 08:15:00']);

    // --- orders (order 1 = carlos, order 2 = admin, etc. so IDOR crosses users) ---
    $st = $pdo->prepare('INSERT INTO orders(user_id,total,created) VALUES(?,?,?)');
    $st->execute([2,261.00,'2026-09-18 11:00:00']); // carlos
    $st->execute([1,349.00,'2026-09-19 16:20:00']); // admin
    $st->execute([4,101.00,'2026-09-20 10:05:00']); // wiener
    $st->execute([2,12.00,'2026-09-25 13:45:00']);  // carlos

    // --- coupons ---
    $pdo->prepare('INSERT INTO coupons(code,percent) VALUES(?,?)')->execute(['SAVE10',10]);

    // --- all labs start insecure ---
    $st = $pdo->prepare('INSERT INTO lab_levels(lab,level) VALUES(?,?)');
    foreach (labs() as $l) $st->execute([$l['slug'],'insecure']);

    // --- invoices on disk (path-traversal lab reads from here) ---
    $inv = dirname(__DIR__, 3).'/data/invoices';
    @mkdir($inv, 0777, true);
    foreach ([1=>'carlos',2=>'admin',3=>'wiener',4=>'carlos'] as $i=>$who) {
        file_put_contents("$inv/invoice-$i.txt", "GateShop INVOICE #$i\nCustomer: $who\nThank you for your order.\n");
    }
    // --- uploads dir ---
    @mkdir(dirname(__DIR__, 2).'/public/uploads', 0777, true);
}

// Seed on first boot if the users table is missing/empty.
function seed_if_needed(): void {
    try {
        $n = db()->query('SELECT COUNT(*) FROM users')->fetchColumn();
        if ((int)$n === 0) seed_database();
    } catch (Throwable $e) {
        seed_database();
    }
}
