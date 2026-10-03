<?php
// Reseed the database from the command line (used by scripts/reset.sh).
$root = '/var/www/html';
require $root.'/app/src/core/db.php';
require $root.'/app/src/core/helpers.php';
require $root.'/app/src/core/labs.php';
require $root.'/app/src/core/seed.php';
seed_database();
echo "GateShop: database reseeded to a clean state.\n";
