<?php
// Handlers: realistic content pages + recon/enumeration surface.
// Labs: recon-discovery (content discovery), enum-user-profile (user enumeration).

function content_page(string $title, string $html): void {
    render($title, "<article class=content-page><h1>".e($title)."</h1>$html</article>");
}

function about_page(): void {
    content_page('About GateShop', "<p>GateShop has been shipping keyboards, monitors and questionable coffee mugs since 2019. We are a small team with a big backlog.</p>
    <p>Looking for our team? See the <a href='/users'>people directory</a>.</p>
    <!-- TODO before launch: lock down /admin-portal and delete /dev and /backup.zip -->");
}
function contact_page(): void {
    content_page('Contact us', "<p>Email: support@gateshop.test · Phone: +20 100 000 0000</p>
    <p>Prefer chat? Try <a href='/support'>GateBot</a>.</p>
    <form class=accform method=post action='/contact'><input name=name placeholder='Your name'><input name=email placeholder=email><textarea name=msg placeholder='Message'></textarea><button>Send</button></form>");
}
function terms_page(){ content_page('Terms & Privacy', "<p>Use the shop lawfully. We store your data about as carefully as this lab suggests.</p>"); }
function faq_page(){ content_page('FAQ', "<p><b>Do you ship internationally?</b> Yes.</p><p><b>Where is my order?</b> Check <a href='/order?id=1'>your orders</a>.</p><p><b>Is this site secure?</b> …that is the whole point of the lab.</p>"); }
function careers_page(){ content_page('Careers', "<p>We are hiring a <b>Senior PHP Developer</b> (must enjoy fixing legacy code) and a <b>Security Engineer</b>.</p><p>Send your CV to hr@gateshop.test.</p>"); }

function blog_page(){
    $posts = ['launching-gateshop'=>'Launching GateShop','our-stack'=>'A look at our stack','black-friday'=>'Black Friday is coming'];
    $list=''; foreach($posts as $slug=>$t) $list.="<li><a href='/blog?post=".e($slug)."'>".e($t)."</a></li>";
    if (!empty($_GET['post'])) {
        $s = $_GET['post'];
        $body = [
            'launching-gateshop'=>'We are live! Thanks to everyone who tested the beta.',
            'our-stack'=>'GateShop runs on PHP and MySQL behind Apache. Yes, we know. It works. <!-- admin panel is at /admin-portal -->',
            'black-friday'=>'Huge deals. Use coupon SAVE10 at checkout.',
        ][$s] ?? 'Post not found.';
        content_page($posts[$s] ?? 'Post', "<p>$body</p><p><a href='/blog'>&larr; all posts</a></p>");
        return;
    }
    content_page('Blog', "<ul>$list</ul>");
}

// ---- recon / discovery surface ----
function dev_page(){ content_page('GateShop (staging)', "<p>⚠️ Internal staging build. Do not share.</p><p>DB: gateshop@db · build: dev-2026-09</p><p>Admin login: <a href='/admin-portal'>/admin-portal</a></p>"); }
function old_page(){ content_page('Legacy site', "<p>This is the old GateShop. The new admin panel moved to <code>/admin-portal</code>.</p>"); }
function status_page(){ header('Content-Type: text/plain'); echo "GateShop status\nserver: Apache/2.4 (Debian)\nphp: ".PHP_VERSION."\napp: up\ndb: up\n"; }
function phpinfo_page(){ // a dev left phpinfo exposed — classic recon finding
    phpinfo();
}

function users_directory(){
    // "People" page — leaks valid usernames (enumeration surface).
    $rows = db()->query('SELECT id,username,display_name,role FROM users ORDER BY id')->fetchAll();
    $list='';
    foreach($rows as $u){
        $list.="<a class=card href='/user?id=".(int)$u['id']."'><div class=pname>".e($u['display_name']?:$u['username'])."</div><div class=cat>@".e($u['username'])." · ".e($u['role'])."</div></a>";
    }
    render('People', lab_banner('enum-user-profile')."<h1>People directory</h1><div class=grid>$list</div>");
}

function user_profile(){
    $id = (int)($_GET['id'] ?? 0);
    $st = db()->prepare('SELECT id,username,display_name,role FROM users WHERE id = ?');
    $st->execute([$id]);
    $u = $st->fetch();
    if (is_secure('enum-user-profile')) {
        // FIX:ENUM — public profiles don't expose the account list; require auth / use opaque handles.
        if (!current_user()) { http_response_code(403); render('Members only','<h1>Members only</h1><p>Log in to view profiles.</p>'); return; }
    }
    // ===== VULN:ENUM | CWE-204 | LAB:enum-user-profile =====
    // Sequential ids + a public profile => walk /user?id=1..N and harvest every valid username. <-- the bug
    if (!$u) { http_response_code(404); render('No such user','<h1>404</h1><p>No user with that id.</p>'); return; }
    // ===== END VULN:ENUM =====
    render('Profile', lab_banner('enum-user-profile')."<h1>".e($u['display_name']?:$u['username'])."</h1>
        <p>username: <b>@".e($u['username'])."</b></p><p>role: ".e($u['role'])."</p>
        <p class=hint>Change the id to walk every account. Then feed the usernames to the login-enumeration lab.</p>");
}

// ---- discoverable admin portal (password is set by YOU via .env ADMIN_PASSWORD) ----
function admin_portal(){
    $body = lab_banner('recon-discovery');
    $body .= "<div class=authform><h1>🔒 GateShop Admin Portal</h1>
        <form method=post action='/login'>
          <input type=hidden name=next value='/admin'>
          <input name=username placeholder='admin username'>
          <input name=password type=password placeholder='admin password'>
          <button>Sign in</button>
        </form>
        <p class=hint>Staff only. (Password is set by the instructor in <code>.env</code>.)</p></div>";
    render('Admin Portal', $body);
}

function recon_hint(){ // /.hidden page listing what's discoverable — only for the recon lab write-up
    header('Content-Type: text/plain');
    echo "Recon surface (for instructors):\n/robots.txt /sitemap.xml /.well-known/security.txt\n/dev /old /status /phpinfo /backup.zip /config.php.bak\n/admin-portal /users /user?id=N /api/me\n";
}
