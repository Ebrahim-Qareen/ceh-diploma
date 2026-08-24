#!/usr/bin/env bash
# ============================================================================
# CEH Diploma — Session 2 recon lab target
# Stands up a local DNS zone (ceh-lab.local) + a small web root on THIS Kali
# box, reachable only from the host-only network. It is the AUTHORISED target
# for every active-recon technique in Session 2 (zone transfer practice uses
# the public zonetransfer.me; subdomain/dir brute-force + crawling use this).
#
#   sudo ./lab_recon_target.sh up      # build + start
#   sudo ./lab_recon_target.sh down    # stop + remove
#   sudo ./lab_recon_target.sh status  # show state
#   ./lab_recon_target.sh log          # tail the web access log (no sudo)
#
# No secrets live in this file. Everything it serves is deliberately fake.
# Idempotent: re-running "up" rebuilds cleanly.
# ============================================================================
set -euo pipefail

ZONE="ceh-lab.local"
WEB_ROOT="/var/www/ceh-lab"
LOG_DIR="${HOME}/ceh-lab/logs"
DNSMASQ_CONF="/etc/dnsmasq.d/ceh-lab.conf"
HOSTS_FILE="/etc/ceh-lab.hosts"
WEB_PORT=80
LAB_IP="127.0.0.1"   # replaced with the host-only IP at runtime

need_root() { [ "$(id -u)" -eq 0 ] || { echo "run with sudo"; exit 1; }; }

detect_ip() {
  # first 192.168.56.x / 10.x / 172.x address, else loopback
  LAB_IP=$(ip -4 -o addr show 2>/dev/null | awk '{print $4}' | cut -d/ -f1 \
    | grep -E '^(192\.168\.56\.|10\.|172\.)' | head -1 || true)
  [ -n "$LAB_IP" ] || LAB_IP="127.0.0.1"
}

up() {
  need_root; detect_ip
  echo "[*] Lab IP: $LAB_IP"

  # --- deps ---
  command -v dnsmasq >/dev/null || { apt-get update -qq && apt-get install -y dnsmasq >/dev/null; }
  command -v python3  >/dev/null || { apt-get install -y python3 >/dev/null; }

  # --- hidden hostnames: some published, several NOT (the point of brute-force) ---
  cat > "$HOSTS_FILE" <<EOF
$LAB_IP  www.$ZONE
$LAB_IP  recon.$ZONE
$LAB_IP  mail.$ZONE
$LAB_IP  dev.$ZONE
$LAB_IP  vpn.$ZONE
$LAB_IP  uat-payroll.$ZONE
$LAB_IP  old-intranet.$ZONE
$LAB_IP  backup.$ZONE
$LAB_IP  admin.$ZONE
$LAB_IP  jenkins-internal.$ZONE
EOF

  # --- dnsmasq zone (answers the lab zone, NXDOMAIN for misses = brute-force signal) ---
  cat > "$DNSMASQ_CONF" <<EOF
# CEH lab recon zone — host-only use only
no-resolv
local=/$ZONE/
addn-hosts=$HOSTS_FILE
# MX + TXT so the record sweep has something to read
mx-host=$ZONE,mail.$ZONE,10
txt-record=$ZONE,"v=spf1 include:mail.$ZONE include:_spf.thirdparty.example -all"
txt-record=$ZONE,"ceh-lab flag: recon-was-here"
txt-record=_dmarc.$ZONE,"v=DMARC1; p=none; rua=mailto:dmarc@$ZONE"
log-queries
log-facility=$LOG_DIR/dns.log
EOF

  # --- web root: a few linked pages, a robots.txt that names hidden dirs,
  #     and several UNLINKED dirs that only directory brute-force will find ---
  rm -rf "$WEB_ROOT"; mkdir -p "$WEB_ROOT"/{admin,backup,uploads,api}
  cat > "$WEB_ROOT/index.html" <<'EOF'
<!doctype html><title>CEH Lab</title><h1>ceh-lab.local</h1>
<p>Authorised recon target. See <a href="/about.html">about</a>.</p>
EOF
  cat > "$WEB_ROOT/about.html" <<'EOF'
<!doctype html><title>About</title><h1>About</h1>
<p>Contact: firstname.lastname@ceh-lab.local (convention: first.last)</p>
EOF
  cat > "$WEB_ROOT/robots.txt" <<'EOF'
User-agent: *
Disallow: /admin/
Disallow: /backup/
Disallow: /api/
EOF
  cat > "$WEB_ROOT/sitemap.xml" <<EOF
<?xml version="1.0"?><urlset><url><loc>http://www.$ZONE/</loc></url>
<url><loc>http://www.$ZONE/about.html</loc></url></urlset>
EOF
  echo '<!doctype html><h1>admin panel</h1>' > "$WEB_ROOT/admin/index.html"
  echo 'db_backup_2026.sql (placeholder — no real data)' > "$WEB_ROOT/backup/notes.txt"
  echo '{"api":"v1","status":"ok"}' > "$WEB_ROOT/api/index.html"

  mkdir -p "$LOG_DIR"; : > "$LOG_DIR/access.log"; : > "$LOG_DIR/dns.log"
  chmod -R a+rX "$WEB_ROOT"

  # --- start DNS ---
  systemctl restart dnsmasq 2>/dev/null || { pkill dnsmasq 2>/dev/null || true; dnsmasq; }

  # --- start web server (python http.server, logging to access.log) ---
  pkill -f "http.server $WEB_PORT" 2>/dev/null || true
  ( cd "$WEB_ROOT" && nohup python3 -m http.server "$WEB_PORT" \
      >> "$LOG_DIR/access.log" 2>&1 & echo $! > "$LOG_DIR/web.pid" )

  echo "[*] DNS zone $ZONE served via dnsmasq (query it with: dig @$LAB_IP recon.$ZONE)"
  echo "[*] Web root at http://recon.$ZONE/  (add '$LAB_IP recon.$ZONE' to /etc/hosts if not using the lab resolver)"
  echo "[*] Logs: $LOG_DIR/{access.log,dns.log}"
  echo "LAB TARGET READY"
}

down() {
  need_root
  rm -f "$DNSMASQ_CONF" "$HOSTS_FILE"
  systemctl restart dnsmasq 2>/dev/null || pkill dnsmasq 2>/dev/null || true
  [ -f "$LOG_DIR/web.pid" ] && kill "$(cat "$LOG_DIR/web.pid")" 2>/dev/null || true
  pkill -f "http.server $WEB_PORT" 2>/dev/null || true
  echo "LAB TARGET STOPPED"
}

status() {
  detect_ip
  echo "Zone:  $ZONE   Lab IP: $LAB_IP"
  echo -n "DNS:   "; pgrep -x dnsmasq >/dev/null && echo "running" || echo "stopped"
  echo -n "Web:   "; pgrep -f "http.server $WEB_PORT" >/dev/null && echo "running on :$WEB_PORT" || echo "stopped"
}

case "${1:-}" in
  up) up ;;
  down) down ;;
  status) status ;;
  log) tail -n 40 -f "${LOG_DIR}/access.log" ;;
  *) echo "usage: sudo $0 {up|down|status} | $0 log"; exit 1 ;;
esac
