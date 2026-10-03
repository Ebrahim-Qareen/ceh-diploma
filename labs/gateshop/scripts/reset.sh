#!/usr/bin/env bash
# Reset GateShop to a clean seeded state (DB + invoices + lab levels). Run from the project root.
set -e
docker compose exec -T app php /var/www/html/scripts/seed_cli.php
# wipe uploaded webshells/avatars from previous classes
docker compose exec -T app sh -c 'rm -f /var/www/html/app/public/uploads/* 2>/dev/null || true'
echo "Done. (You can also click Reset in /instructor.)"
