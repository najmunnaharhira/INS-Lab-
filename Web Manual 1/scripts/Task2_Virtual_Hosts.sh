#!/usr/bin/env bash
set -euo pipefail

# Task2: Create virtual hosts and enable them
# Usage: sudo bash Task2_Virtual_Hosts.sh

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SITES_DIR="$REPO_ROOT/sites"
CONFIGS_DIR="$REPO_ROOT/configs"

echo "Creating site directories under /var/www and copying sample pages..."
for site in example.com webserverlab.com anothervhost.com; do
  sudo mkdir -p /var/www/${site}/html
  sudo chown -R $USER:$USER /var/www/${site}
  sudo chmod -R 755 /var/www/${site}
  if [ -f "$SITES_DIR/$site/html/index.html" ]; then
    sudo cp "$SITES_DIR/$site/html/index.html" "/var/www/${site}/html/index.html"
  fi
done

echo "Copying config templates to /etc/apache2/sites-available..."
for cfg in example.com.conf webserverlab.com.conf anothervhost.com.conf; do
  if [ -f "$CONFIGS_DIR/$cfg" ]; then
    sudo cp "$CONFIGS_DIR/$cfg" /etc/apache2/sites-available/
  else
    echo "Warning: $CONFIGS_DIR/$cfg not found in repo."
  fi
done

echo "Disable default site (optional) and enable our sites..."
sudo a2dissite 000-default.conf || true
sudo a2ensite example.com.conf
sudo a2ensite webserverlab.com.conf
sudo a2ensite anothervhost.com.conf

echo "Checking configuration..."
sudo apache2ctl configtest

echo "Restarting Apache..."
sudo systemctl restart apache2

echo ""
echo "Important: For local testing map hostnames to 127.0.0.1 in /etc/hosts, e.g.:"
echo "  127.0.0.1 example.com webserverlab.com anothervhost.com"
echo ""
echo "Then visit http://example.com, http://webserverlab.com, http://anothervhost.com"
echo "Checkpoint 2/3/4: Show the working virtual hosts to your teacher."
