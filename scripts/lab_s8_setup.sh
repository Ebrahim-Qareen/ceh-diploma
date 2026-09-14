#!/usr/bin/env bash
# CEH Diploma lab - Session 8 target prep (web app hacking & SQL injection)
# Stands up the deliberately-vulnerable web app(s) on the lab network (Docker).
# There is NOTHING to seed - the apps ship vulnerable. NO CREDENTIALS beyond the
# apps' own documented lab defaults. Idempotent.
#
# Stages:
#   dvwa       - run DVWA on :80  (default; the labs' primary target)
#   juiceshop  - run OWASP Juice Shop on :3000 (optional secondary)
#   stop       - stop both containers
#
# Usage:
#   ./lab_s8_setup.sh dvwa
#   ./lab_s8_setup.sh juiceshop
#   ./lab_s8_setup.sh stop
set -euo pipefail
STAGE="${1:-dvwa}"

need_docker() {
  if ! command -v docker >/dev/null 2>&1; then
    echo "[-] Docker not found. Install docker first (apt install docker.io)."; exit 1
  fi
}

case "$STAGE" in
  dvwa)
    need_docker
    echo "[*] Starting DVWA on http://<lab-ip>/  (image: vulnerables/web-dvwa)"
    docker rm -f dvwa >/dev/null 2>&1 || true
    docker run -d --name dvwa -p 80:80 vulnerables/web-dvwa
    echo "[+] DVWA up. Next:"
    echo "    1) browse to  http://<lab-ip>/setup.php  -> Create / Reset Database"
    echo "    2) login  admin / password   (lab default - documented, not a secret)"
    echo "    3) point your browser proxy at Burp (127.0.0.1:8080)"
    echo "[i] Use the DVWA Security page to switch Low/Medium/High per attack."
    ;;
  juiceshop)
    need_docker
    echo "[*] Starting OWASP Juice Shop on http://<lab-ip>:3000/ (image: bkimminich/juice-shop)"
    docker rm -f juiceshop >/dev/null 2>&1 || true
    docker run -d --name juiceshop -p 3000:3000 bkimminich/juice-shop
    echo "[+] Juice Shop up on :3000. Try the SQLi login bypass and an XSS challenge."
    ;;
  stop)
    docker rm -f dvwa juiceshop >/dev/null 2>&1 || true
    echo "[+] Stopped DVWA and Juice Shop."
    ;;
  *) echo "Unknown stage '$STAGE' (use: dvwa | juiceshop | stop)"; exit 1 ;;
esac
