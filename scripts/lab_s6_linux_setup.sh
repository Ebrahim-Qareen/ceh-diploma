#!/usr/bin/env bash
# CEH Diploma lab - Session 6 Linux privesc seeding (SUID / sudo / cron)
# Run on the Linux teaching box (Metasploitable2 or a dedicated Ubuntu) as root.
# Seeds three DEMONSTRABLE vectors, one per mini-lab. LAB ONLY - never on a real host.
# NO CREDENTIALS IN THIS FILE. Idempotent. Placeholders only.
#
# Usage:
#   sudo ./lab_s6_linux_setup.sh <student_user>
#
set -euo pipefail
STUDENT_USER="${1:-student}"

if [ "$(id -u)" -ne 0 ]; then echo "[-] Run as root."; exit 1; fi
echo "[*] Seeding Linux privesc vectors for student user: ${STUDENT_USER}"

# 1) SUID / GTFOBins  (Lab 1: find -exec /bin/sh -p)
chmod u+s /usr/bin/find
echo "[+] SUID bit set on /usr/bin/find (GTFOBins vector)."

# 2) Sudo misconfig  (NOPASSWD on a GTFOBins binary)
SUDO_LINE="${STUDENT_USER} ALL=(ALL) NOPASSWD: /usr/bin/less"
if ! grep -qF "$SUDO_LINE" /etc/sudoers.d/ceh-lab 2>/dev/null; then
    echo "$SUDO_LINE" > /etc/sudoers.d/ceh-lab
    chmod 440 /etc/sudoers.d/ceh-lab
    visudo -cf /etc/sudoers.d/ceh-lab
    echo "[+] NOPASSWD sudo on /usr/bin/less for ${STUDENT_USER} (GTFOBins vector)."
fi

# 3) Writable cron  (root cron runs a world-writable script)
cat > /opt/backup.sh <<'SH'
#!/bin/bash
# lab placeholder backup job - intentionally world-writable
echo "backup ran at $(date)" >> /var/log/ceh-backup.log
SH
chmod 777 /opt/backup.sh
CRON_LINE="* * * * * root /opt/backup.sh"
if ! grep -qF "/opt/backup.sh" /etc/crontab; then
    echo "$CRON_LINE" >> /etc/crontab
    echo "[+] Root cron runs world-writable /opt/backup.sh every minute (writable-cron vector)."
fi

echo "[i] Snapshot the box as 'pre-s6' AFTER seeding so you can revert between student attempts."
echo "[i] Run linPEAS first in each lab so students correlate tool output with the vector."
