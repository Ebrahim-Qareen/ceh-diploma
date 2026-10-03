<?php
// Handlers: authentication.
// Labs: sqli-login, auth-enum, deserial-remember, openredirect-next, hosthdr-reset.

define('REMEMBER_KEY', getenv('REMEMBER_KEY') ?: 'lab-hmac-key-change-me');

// Demonstrative gadget for the deserialization lab: an object whose __destruct writes a file.
// Forging this object inside the remember cookie (insecure) => arbitrary file write => RCE.
class AuditLog {
    public $file = '';
    public $data = '';
    public function __destruct() {
        if ($this->file !== '') @file_put_contents($this->file, $this->data);
    }
}

function safe_next(string $default = '/'): string {
    $next = $_GET['next'] ?? $_POST['next'] ?? $default;
    if (is_secure('openredirect-next')) {
        // FIX:OPENREDIRECT — only allow local paths (single leading slash, no scheme/host).
        if (!preg_match('#^/[^/]#', $next)) return $default;
        return $next;
    }
    // ===== VULN:OPENREDIRECT | CWE-601 | LAB:openredirect-next =====
    return $next; // <-- the bug: redirect target taken from input with no validation.
    // ===== END VULN:OPENREDIRECT =====
}

function do_login(): void {
    $next = $_GET['next'] ?? $_POST['next'] ?? '/';
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        $body  = lab_banner('sqli-login');
        $body .= "<form class=authform method=post action='/login'>
            <input type=hidden name=next value='".e($next)."'>
            <h1>Login</h1>
            <input name=username placeholder=username>
            <input name=password type=password placeholder=password>
            <label><input type=checkbox name=remember value=1> remember me</label>
            <button>Log in</button>
            <p class=hint>Try: <code>admin</code> / <code>admin123</code> — or bypass it.</p>
            </form>";
        render('Login', $body);
        return;
    }

    $user = $_POST['username'] ?? '';
    $pass = $_POST['password'] ?? '';
    $pdo = db();
    $row = null;

    if (is_secure('sqli-login')) {
        // FIX:SQLI — look the user up with a bound parameter, verify the hash in PHP.
        $st = $pdo->prepare('SELECT * FROM users WHERE username = ?');
        $st->execute([$user]);
        $cand = $st->fetch();
        if ($cand && hash_equals($cand['password'], sha1($pass))) $row = $cand;
    } else {
        // ===== VULN:SQLI (login bypass) | CWE-89 | LAB:sqli-login =====
        // Both username and password are concatenated in. `admin'-- -` comments out the password check.
        $sql = "SELECT * FROM users WHERE username = '$user' AND password = '".sha1($pass)."'"; // <-- the bug
        $row = $pdo->query($sql)->fetch() ?: null;
        // ===== END VULN:SQLI =====
    }

    if ($row) {
        $_SESSION['uid'] = $row['id'];
        if (!empty($_POST['remember'])) set_remember_cookie((int)$row['id']);
        redirect(safe_next('/'));
    }

    // auth-enum lab: distinct vs generic error messages.
    $existsStmt = $pdo->prepare('SELECT 1 FROM users WHERE username = ?');
    $existsStmt->execute([$user]);
    $exists = (bool)$existsStmt->fetchColumn();
    if (is_secure('auth-enum')) {
        $err = 'Invalid username or password.'; // FIX:ENUM — one generic message.
    } else {
        // ===== VULN:USERNAME-ENUM | CWE-204 | LAB:auth-enum =====
        $err = $exists ? 'Wrong password.' : 'No such username.'; // <-- the bug: leaks which usernames exist.
        // ===== END VULN:USERNAME-ENUM =====
    }
    flash($err);
    redirect('/login?next='.urlencode($next));
}

function do_logout(): void {
    $_SESSION = [];
    setcookie('remember', '', time()-3600, '/');
    redirect('/');
}

function do_register(): void {
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        render('Register', "<form class=authform method=post action='/register'><h1>Create account</h1>
            <input name=username placeholder=username><input name=email placeholder=email>
            <input name=password type=password placeholder=password><button>Register</button></form>");
        return;
    }
    $u = trim($_POST['username'] ?? ''); $em = trim($_POST['email'] ?? ''); $pw = $_POST['password'] ?? '';
    if ($u && $pw) {
        try {
            $st = db()->prepare('INSERT INTO users(username,email,password,role,balance) VALUES(?,?,?,?,?)');
            $st->execute([$u, $em, sha1($pw), 'user', 0]);
            flash('Account created — please log in.');
        } catch (Throwable $e) { flash('That username is taken.'); }
    }
    redirect('/login');
}

// ---- remember-me cookie (deserialization lab) ----
function set_remember_cookie(int $uid): void {
    if (is_secure('deserial-remember')) {
        // FIX:DESERIAL — signed, non-executable token: base64(json)|hmac.
        $payload = base64_encode(json_encode(['uid'=>$uid]));
        $sig = hash_hmac('sha256', $payload, REMEMBER_KEY);
        setcookie('remember', "$payload.$sig", time()+86400, '/');
    } else {
        // ===== VULN:DESERIAL | CWE-502 | LAB:deserial-remember =====
        // A PHP-serialized object is placed in the cookie and later unserialize()'d (see load_remember_cookie).
        setcookie('remember', base64_encode(serialize(['uid'=>$uid])), time()+86400, '/');
        // ===== END VULN:DESERIAL =====
    }
}

function load_remember_cookie(): void {
    if (!empty($_SESSION['uid']) || empty($_COOKIE['remember'])) return;
    $raw = $_COOKIE['remember'];
    if (is_secure('deserial-remember')) {
        // FIX:DESERIAL — verify HMAC, parse JSON only (no object instantiation).
        $parts = explode('.', $raw, 2);
        if (count($parts) === 2 && hash_equals($parts[1], hash_hmac('sha256', $parts[0], REMEMBER_KEY))) {
            $d = json_decode(base64_decode($parts[0]), true);
            if (!empty($d['uid'])) $_SESSION['uid'] = (int)$d['uid'];
        }
        return;
    }
    // ===== VULN:DESERIAL | CWE-502 | LAB:deserial-remember =====
    $d = @unserialize(base64_decode($raw)); // <-- the bug: untrusted input is unserialize()'d (object injection).
    if (is_array($d) && !empty($d['uid'])) $_SESSION['uid'] = (int)$d['uid'];
    // ===== END VULN:DESERIAL =====
}

// ---- password reset (host header lab) ----
function forgot_password(): void {
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        render('Forgot password', lab_banner('hosthdr-reset').
          "<form class=authform method=post action='/forgot'><h1>Reset password</h1>
           <input name=email placeholder='your email'><button>Send reset link</button></form>");
        return;
    }
    $email = trim($_POST['email'] ?? '');
    $token = bin2hex(random_bytes(8));
    if (is_secure('hosthdr-reset')) {
        // FIX:HOSTHDR — build the URL from a fixed configured base, not the request Host.
        $base = getenv('APP_BASE_URL') ?: 'http://localhost:8080';
    } else {
        // ===== VULN:HOSTHDR | CWE-644 | LAB:hosthdr-reset =====
        $base = 'http://'.($_SERVER['HTTP_HOST'] ?? 'localhost'); // <-- the bug: link host comes from the request.
        // ===== END VULN:HOSTHDR =====
    }
    $link = "$base/reset?token=$token";
    $body = lab_banner('hosthdr-reset');
    $body .= "<p>(Lab: no real email is sent.) The reset link that would be emailed to <b>".e($email)."</b> is:</p>";
    $body .= "<pre class=code>".e($link)."</pre>";
    $body .= "<p class=hint>Send <code>Host: evil.com</code> on this request and watch the link change.</p>";
    render('Forgot password', $body);
}
