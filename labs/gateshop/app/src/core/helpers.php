<?php
// GateShop core — shared helpers (session, escaping, routing, flash, security levels).

function app_start(): void {
    if (session_status() !== PHP_SESSION_ACTIVE) {
        session_name('GATESESS');
        session_start();
    }
}

// Output escaping. Labs that are intentionally vulnerable deliberately DO NOT call this.
function e($s): string { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }

function current_user(): ?array {
    if (empty($_SESSION['uid'])) return null;
    $st = db()->prepare('SELECT * FROM users WHERE id = ?');
    $st->execute([$_SESSION['uid']]);
    $u = $st->fetch();
    return $u ?: null;
}

function require_login(): array {
    $u = current_user();
    if (!$u) { header('Location: /login?next=' . urlencode($_SERVER['REQUEST_URI'] ?? '/')); exit; }
    return $u;
}

function is_admin(): bool { $u = current_user(); return $u && ($u['role'] ?? '') === 'admin'; }

function flash(?string $msg = null): ?string {
    if ($msg !== null) { $_SESSION['flash'] = $msg; return null; }
    $m = $_SESSION['flash'] ?? null; unset($_SESSION['flash']); return $m;
}

function redirect(string $to): void { header('Location: ' . $to); exit; }

// ---- Per-lab security level (DVWA-style). Stored in DB, settable in the instructor console. ----
function lab_level(string $lab): string {
    static $cache = null;
    if ($cache === null) {
        $cache = [];
        foreach (db()->query('SELECT lab, level FROM lab_levels') as $r) $cache[$r['lab']] = $r['level'];
    }
    return $cache[$lab] ?? 'insecure';
}
function is_secure(string $lab): bool { return lab_level($lab) === 'secure'; }

function set_lab_level(string $lab, string $level): void {
    $level = $level === 'secure' ? 'secure' : 'insecure';
    if (db_driver() === 'sqlite') {
        $st = db()->prepare('INSERT INTO lab_levels(lab,level) VALUES(?,?) ON CONFLICT(lab) DO UPDATE SET level=excluded.level');
    } else {
        $st = db()->prepare('INSERT INTO lab_levels(lab,level) VALUES(?,?) ON DUPLICATE KEY UPDATE level=VALUES(level)');
    }
    $st->execute([$lab, $level]);
}
