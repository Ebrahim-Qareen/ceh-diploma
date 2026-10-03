<?php
// GateShop core — database access (PDO). Supports MySQL (Docker deploy) and SQLite (local dev/test).
// This file is infrastructure, not a lab. Lab code lives in app/src/handlers/.

function db(): PDO {
    static $pdo = null;
    if ($pdo !== null) return $pdo;

    $driver = getenv('DB_DRIVER') ?: 'mysql';
    if ($driver === 'sqlite') {
        $file = getenv('DB_SQLITE') ?: (dirname(__DIR__, 2) . '/data/gateshop.sqlite');
        $pdo = new PDO('sqlite:' . $file);
    } else {
        $host = getenv('DB_HOST') ?: 'db';
        $port = getenv('DB_PORT') ?: '3306';
        $name = getenv('DB_NAME') ?: 'gateshop';
        $user = getenv('DB_USER') ?: 'gateshop';
        $pass = getenv('DB_PASS') ?: 'gateshop';
        $dsn  = "mysql:host=$host;port=$port;dbname=$name;charset=utf8mb4";
        // Retry: MySQL may still be starting when the app boots.
        $tries = 0;
        while (true) {
            try { $pdo = new PDO($dsn, $user, $pass); break; }
            catch (PDOException $e) {
                if (++$tries > 60) throw $e;
                sleep(1);
            }
        }
    }
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
    return $pdo;
}

function db_driver(): string { return getenv('DB_DRIVER') ?: 'mysql'; }
