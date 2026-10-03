<?php
// Generates MANIFEST.md from the lab registry. Line numbers are read live from the VULN: markers.
$root = dirname(__DIR__);
require $root.'/app/src/core/labs.php';

function vuln_lines(string $root, array $l): string {
    $path = $root.'/'.$l['file'];
    if (!is_file($path)) return '?';
    $lines = explode("\n", file_get_contents($path));
    $slug = $l['slug']; $start = null; $end = null;
    foreach ($lines as $i => $ln) {
        if ($start === null && stripos($ln, 'VULN:') !== false && stripos($ln, $slug) !== false) $start = $i+1;
        elseif ($start !== null && stripos($ln, 'END VULN') !== false) { $end = $i+1; break; }
        elseif ($start !== null && stripos($ln, '<-- the bug') !== false) $end = $i+1;
    }
    // fall back: first VULN marker for this file's lab
    if ($start === null) {
        foreach ($lines as $i => $ln) if (stripos($ln,'VULN:')!==false && stripos($ln,strtoupper(explode('-',$slug)[0]))!==false){$start=$i+1;break;}
    }
    return $start ? ($end && $end>$start ? "$start-$end" : "$start") : '?';
}

$groups = [];
foreach (labs() as $l) $groups[$l['group']][] = $l;

$out  = "# GateShop — Lab Manifest\n\n";
$out .= "Generated from the lab registry. Paste this back into the CEH course chat to wire each\n";
$out .= "Session-8 \"Practical application\" slot: lab URL + goal + open `<file>` → `<function>` (the bug) + the fix.\n\n";
$out .= "**Base URL:** `http://<your-vm>:8080`  ·  **Instructor console:** `/instructor`  ·  **Show code:** `/code?lab=<slug>`\n\n";

$n = 0;
foreach ($groups as $g => $items) {
    $out .= "## $g\n\n";
    foreach ($items as $l) {
        $n++;
        $lines = vuln_lines($root, $l);
        $out .= "### {$l['session']} → {$l['title']}\n";
        $out .= "- lab_slug:      `{$l['slug']}`\n";
        $out .= "- url:           `{$l['url']}`\n";
        $out .= "- goal:          {$l['goal']}\n";
        $out .= "- vuln_file:     `{$l['file']}`\n";
        $out .= "- vuln_function: `{$l['func']}`\n";
        $out .= "- vuln_lines:    {$lines}\n";
        $out .= "- cwe/owasp:     {$l['cwe']} · {$l['owasp']}\n";
        $out .= "- exploit:       `{$l['exploit']}`\n";
        $out .= "- fix:           {$l['fix']}\n";
        $out .= "- toggle:        per-lab security level `insecure` | `secure` (instructor console)\n";
        $out .= "- status:        live\n\n";
    }
}

$out .= "## Quickstart (on the VM)\n\n";
$out .= "```bash\n";
$out .= "cp .env.example .env     # then edit the secrets\n";
$out .= "docker compose up -d --build\n";
$out .= "# open http://<vm-ip>:8080   ·   instructor console: /instructor\n";
$out .= "# reset between classes:\n";
$out .= "bash scripts/reset.sh     # or click \"Reset\" in /instructor\n";
$out .= "```\n\n";
$out .= "## Seeded accounts\n\n";
$out .= "| user | password | role |\n|---|---|---|\n";
$out .= "| admin | admin123 | admin |\n| instructor | teach123 | admin |\n| carlos | carlos123 | user (victim) |\n| wiener | peter | user |\n\n";
$out .= "Flags: SSRF → `GATEFLAG{...}` at `/internal/flag`; GateBot secret → `GATEBOT{...}`.\n\n";
$out .= "## Coverage\n\n";
$out .= "$n labs, all **live**. Not yet built (need extra services — ask for phase 2): NoSQL injection (MongoDB), LDAP injection (OpenLDAP), WebSocket CSWSH, web cache poisoning & HTTP request smuggling (caching/proxy tier), JWT & OAuth, prototype pollution (server-side), race conditions.\n";

file_put_contents($root.'/MANIFEST.md', $out);
echo "MANIFEST.md written: $n labs\n";
