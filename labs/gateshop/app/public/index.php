<?php
// GateShop — front controller. Routes a request to a small handler function.
// Deliberately simple so the data flow (request -> handler -> sink -> response) is easy to follow in class.

$ROOT = dirname(__DIR__, 2);
require $ROOT.'/app/src/core/db.php';
require $ROOT.'/app/src/core/helpers.php';
require $ROOT.'/app/src/core/labs.php';
require $ROOT.'/app/src/core/view.php';
require $ROOT.'/app/src/core/seed.php';
foreach (glob($ROOT.'/app/src/handlers/*.php') as $h) require $h;

app_start();
seed_if_needed();       // build + seed the DB on first boot
load_remember_cookie(); // deserialization lab (sets $_SESSION if a valid remember cookie exists)

$path = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH) ?: '/';
$path = rtrim($path, '/') ?: '/';

try {
    switch ($path) {
        case '/':                  home_page(); break;
        case '/search':            search_products(); break;
        case '/product':           product_page(); break;
        case '/review':            post_review(); break;
        case '/welcome':           welcome_page(); break;

        case '/login':             do_login(); break;
        case '/logout':            do_logout(); break;
        case '/register':          do_register(); break;
        case '/forgot':            forgot_password(); break;

        case '/account':           account_page(); break;
        case '/account/signature': render_signature(); break;
        case '/account/avatar-url':fetch_avatar_url(); break;
        case '/account/delete':    delete_page(); break;

        case '/cart':              cart_page(); break;
        case '/order':             view_order(); break;
        case '/download':          download_file(); break;

        case '/admin':             admin_page(); break;
        case '/admin/tools':       net_ping(); break;
        case '/admin/import':      import_xml(); break;

        case '/api/me':            api_me(); break;
        case '/support':           support_page(); break;

        case '/about':             about_page(); break;
        case '/contact':           contact_page(); break;
        case '/terms':             terms_page(); break;
        case '/faq':               faq_page(); break;
        case '/careers':           careers_page(); break;
        case '/blog':              blog_page(); break;
        case '/dev':               dev_page(); break;
        case '/old':               old_page(); break;
        case '/status':            status_page(); break;
        case '/phpinfo':           phpinfo_page(); break;
        case '/users':             users_directory(); break;
        case '/user':              user_profile(); break;
        case '/admin-portal':      admin_portal(); break;

        case '/instructor':        instructor_console(); break;
        case '/code':              show_code($_GET['lab'] ?? ''); break;

        case '/debug':             debug_page(); break;
        case '/config.php.bak':    backup_leak(); break;
        case '/internal/flag':     internal_flag(); break;   // SSRF target (block at web layer in real life)
        case '/health':            header('Content-Type: text/plain'); echo 'ok'; break;

        default:
            http_response_code(404);
            render('Not found', "<h1>404</h1><p>No page at ".e($path).".</p>");
    }
} catch (Throwable $ex) {
    // Information-disclosure lab: verbose errors at insecure level.
    if (is_secure('infodisc-debug')) {
        http_response_code(500);
        render('Error', "<h1>Something went wrong</h1><p>Please try again later.</p>");
    } else {
        http_response_code(500);
        header('Content-Type: text/plain');
        echo "GateShop error (debug on):\n".$ex->getMessage()."\n\n".$ex->getTraceAsString();
    }
}
