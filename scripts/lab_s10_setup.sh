#!/usr/bin/env bash
# CEH Diploma lab - Session 10 prep (evasion / wireless / emerging tech - FINAL)
# Adds the small pieces the final session needs and reprints the ownership gate.
# It creates NO cloud resources and cannot provide RF hardware - those are the
# student's own. NO CREDENTIALS. Idempotent.
#
# Stages:
#   ids             - start a lab Suricata IDS target for the evasion lab (Docker)
#   wireless-check  - verify an adapter supports monitor mode + reprint own-AP-only rule
#   bucket-note     - print the exact open-bucket create/detect/fix steps (student's own cloud)
#   gate            - reprint the ownership / ethics gate (default)
#   stop            - stop the IDS target
#
# Usage:
#   ./lab_s10_setup.sh ids
#   ./lab_s10_setup.sh wireless-check
#   ./lab_s10_setup.sh bucket-note
set -euo pipefail
STAGE="${1:-gate}"

print_gate() {
  echo "================== SESSION 10 OWNERSHIP / ETHICS GATE =================="
  echo " Evasion, wireless, cloud, and device attacks off-lab are serious crimes."
  echo "  * Evasion scans: the lab IDS host ONLY."
  echo "  * Wireless: YOUR OWN test AP + monitor-mode adapter ONLY."
  echo "  * Cloud/IoT: YOUR OWN test bucket / lab device ONLY."
  echo "  * Crypto audit: an AUTHORISED host ONLY."
  echo "======================================================================="
}

case "$STAGE" in
  ids)
    if ! command -v docker >/dev/null 2>&1; then echo "[-] Docker not found (apt install docker.io)."; exit 1; fi
    echo "[*] Starting a lab Suricata IDS target (evasion Lab A)..."
    docker rm -f s10-ids >/dev/null 2>&1 || true
    docker run -d --name s10-ids jasonish/suricata:latest -i eth0 >/dev/null 2>&1 || \
      echo "[i] If the image/iface differs, use your existing SOC-lab Suricata/Snort host instead."
    echo "[+] Point the baseline nmap scan at the IDS host; watch fast.log; then evade."
    ;;
  wireless-check)
    print_gate
    echo "[*] Checking for a monitor-mode-capable adapter..."
    if command -v iw >/dev/null 2>&1; then
      iw list 2>/dev/null | grep -A6 'Supported interface modes' | grep -i monitor \
        && echo "[+] An adapter supports monitor mode." \
        || echo "[-] No monitor-mode adapter detected. Use an Alfa-class USB adapter; or crack saved/wpa2_handshake.cap."
    else
      echo "[i] 'iw' not present; install wireless-tools/iw. Fallback: saved/wpa2_handshake.cap."
    fi
    echo "[i] Reminder: capture/crack YOUR OWN test AP only (weak WPA2 passphrase for the demo)."
    ;;
  bucket-note)
    print_gate
    cat <<'NOTE'
[*] Open-bucket lab (Lab C) — run against YOUR OWN cloud account/bucket:
    1) create:   aws s3 mb s3://ceh-lab-test-bucket-<you>
    2) misconfig (LAB ONLY): disable Block Public Access + a public-read policy
    3) detect:   aws s3 ls s3://ceh-lab-test-bucket-<you> --no-sign-request
                 curl -s https://ceh-lab-test-bucket-<you>.s3.amazonaws.com/
    4) FIX:      re-enable Block Public Access ; re-test -> access denied
    (This script does NOT create cloud resources — that is your own account.)
NOTE
    ;;
  stop)
    docker rm -f s10-ids >/dev/null 2>&1 || true
    echo "[+] Stopped the IDS target."
    ;;
  gate) print_gate ;;
  *) echo "Unknown stage '$STAGE' (use: ids | wireless-check | bucket-note | gate | stop)"; exit 1 ;;
esac
