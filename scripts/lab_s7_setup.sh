#!/usr/bin/env bash
# CEH Diploma lab - Session 7 analysis-chamber prep (malware threats & analysis)
# Run on the ISOLATED Linux analysis VM. Installs static+dynamic analysis tooling
# and verifies containment. There is NOTHING to seed - the sample is built in Lab A.
# NO CREDENTIALS IN THIS FILE. Idempotent.
#
# Stages:
#   tools    - install yara, pefile, strings, ssdeep, network monitors (default)
#   isolate  - READ-ONLY containment check: the chamber must NOT reach the real internet
#
# Usage:
#   sudo ./lab_s7_setup.sh tools
#        ./lab_s7_setup.sh isolate
set -euo pipefail
STAGE="${1:-tools}"

install_tools() {
  if [ "$(id -u)" -ne 0 ]; then echo "[-] Run 'tools' as root."; exit 1; fi
  echo "[*] Installing malware-analysis tooling on the chamber..."
  if command -v apt-get >/dev/null 2>&1; then
    apt-get update -y
    apt-get install -y yara python3-pefile binutils ssdeep tcpdump net-tools || true
  else
    echo "[!] Non-apt distro: install yara, python3-pefile, binutils, ssdeep, tcpdump manually."
  fi
  echo "[+] Verify:"
  for t in yara strings tcpdump ss; do
    if command -v "$t" >/dev/null 2>&1; then echo "    [ok] $t"; else echo "    [MISSING] $t"; fi
  done
  python3 -c "import pefile; print('    [ok] python3 pefile', pefile.__version__)" 2>/dev/null || echo "    [MISSING] python3-pefile"
  echo "[i] Static: sha256sum / strings / pefile. Dynamic: 'watch -n1 ss -tnp' + tcpdump. File rules: yara."
}

check_isolation() {
  echo "[*] Containment check - the chamber must NOT reach the real internet."
  if ping -c1 -W2 8.8.8.8 >/dev/null 2>&1; then
    echo "[FAIL] 8.8.8.8 is reachable - DO NOT DETONATE. Switch to host-only / INetSim first."
    exit 2
  else
    echo "[ok] 8.8.8.8 unreachable - good. (A fake-internet like INetSim may still answer locally.)"
  fi
  echo "[i] Also confirm: clean snapshot taken, no shared folders/clipboard, host-only NIC."
  echo "[i] Only when this passes: arm ProcMon/TCPView (or 'watch ss'), then detonate."
}

case "$STAGE" in
  tools)   install_tools ;;
  isolate) check_isolation ;;
  *) echo "Unknown stage '$STAGE' (use: tools | isolate)"; exit 1 ;;
esac
