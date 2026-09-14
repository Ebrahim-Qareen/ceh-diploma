#!/usr/bin/env bash
# CEH Diploma lab - Session 9 prep (sniffing/MITM/hijacking/social-eng/DoS)
# Adds the small pieces the session needs on top of the existing lab, and reprints
# the isolation gate. NOTHING here attacks anything - attacks are run by hand in the
# labs, on the isolated host-only network only. NO CREDENTIALS. Idempotent.
#
# Stages:
#   detect      - install arpwatch on the monitor/victim VM (ARP-anomaly detection)
#   dos-target  - start a throwaway lab web server (Docker) as the DoS target
#   gate        - reprint the isolation / ethics gate (default)
#   stop        - stop the DoS target
#
# Usage:
#   sudo ./lab_s9_setup.sh detect
#        ./lab_s9_setup.sh dos-target
#        ./lab_s9_setup.sh gate
set -euo pipefail
STAGE="${1:-gate}"

print_gate() {
  echo "=================== SESSION 9 ISOLATION / ETHICS GATE ==================="
  echo " MITM, phishing, and DoS against systems you do NOT own are serious crimes."
  echo "  * Host-only lab network ONLY. Confirm no bridge to a real network."
  echo "  * Phishing (SET): clone a LAB login page; use consenting test accounts."
  echo "  * DoS (hping3/slowhttptest): the throwaway lab web VM ONLY, short bursts."
  echo "  * Always stop ARP spoofing cleanly (bettercap: arp.spoof off)."
  echo "========================================================================"
}

case "$STAGE" in
  detect)
    if [ "$(id -u)" -ne 0 ]; then echo "[-] Run 'detect' as root."; exit 1; fi
    echo "[*] Installing arpwatch (ARP-anomaly detection for Lab A defender step)..."
    if command -v apt-get >/dev/null 2>&1; then apt-get update -y && apt-get install -y arpwatch || true; fi
    echo "[+] arpwatch installed. Watch for 'changed ethernet address' on the gateway IP."
    echo "[i] It logs to syslog / mail; a gateway MAC change = ARP poisoning in progress."
    ;;
  dos-target)
    if ! command -v docker >/dev/null 2>&1; then echo "[-] Docker not found (apt install docker.io)."; exit 1; fi
    print_gate
    echo "[*] Starting a throwaway lab web server (nginx) as the DoS target on :80..."
    docker rm -f s9-dos-target >/dev/null 2>&1 || true
    docker run -d --name s9-dos-target -p 80:80 nginx:alpine
    echo "[+] DoS target up. Point hping3 / slowhttptest at THIS host only."
    ;;
  stop)
    docker rm -f s9-dos-target >/dev/null 2>&1 || true
    echo "[+] Stopped the DoS target."
    ;;
  gate) print_gate ;;
  *) echo "Unknown stage '$STAGE' (use: detect | dos-target | gate | stop)"; exit 1 ;;
esac
