<?php
// Handler: JSON API.
// Lab: cors-api (CORS misconfiguration — origin reflection with credentials).

function api_me(): void {
    $origin = $_SERVER['HTTP_ORIGIN'] ?? '';
    if (is_secure('cors-api')) {
        // FIX:CORS — only allow-listed origins, and never pair reflection with credentials.
        $allow = ['http://localhost:8080'];
        if (in_array($origin, $allow, true)) {
            header("Access-Control-Allow-Origin: $origin");
            header('Access-Control-Allow-Credentials: true');
        }
    } else {
        // ===== VULN:CORS | CWE-942 | LAB:cors-api =====
        // Whatever Origin the request carries is reflected back, WITH credentials allowed. <-- the bug
        if ($origin !== '') {
            header("Access-Control-Allow-Origin: $origin");
            header('Access-Control-Allow-Credentials: true');
        }
        // ===== END VULN:CORS =====
    }
    header('Content-Type: application/json');
    $u = current_user();
    echo json_encode($u ? [
        'id'=>(int)$u['id'], 'username'=>$u['username'], 'email'=>$u['email'],
        'role'=>$u['role'], 'balance'=>$u['balance']
    ] : ['error'=>'not logged in']);
}
