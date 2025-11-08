#!/usr/bin/env bash
set -euo pipefail

# Task3: Copy two dynamic sample sites (HTML+JS) into the sites if not already done
# Usage: sudo bash Task3_Dynamic_Sites.sh

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# For this lab we have simple JS form handlers included in sample sites (you can edit them)
# Copy them into /var/www if not present
for site in example.com webserverlab.com; do
  SRC="$REPO_ROOT/sites/$site/html/index.html"
  DST="/var/www/$site/html/index.html"
  if [ -f "$SRC" ]; then
    echo "Copying $SRC to $DST"
    sudo cp "$SRC" "$DST"
    sudo chown $USER:www-data "$DST"
  else
    echo "No source dynamic site at $SRC; skipping."
  fi
done

echo ""
echo "Visit the dynamic pages now and test the JS forms in your browser."
echo "Checkpoint 5: Show the two dynamic websites to your teacher."
