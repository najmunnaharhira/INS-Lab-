#!/usr/bin/env bash
set -euo pipefail

# Task1: Install Apache and basic verification
# Usage: sudo bash Task1_Install_Apache.sh

echo "Updating package lists..."
sudo apt update

echo "Installing apache2..."
sudo apt install -y apache2

echo "Enabling Apache to start on boot..."
sudo systemctl enable apache2

echo "Allow 'Apache' profile in UFW (if UFW is active)..."
if command -v ufw >/dev/null 2>&1; then
  sudo ufw allow 'Apache' || true
  echo "ufw status:"
  sudo ufw status
else
  echo "ufw not found or not installed — skipping firewall steps."
fi

echo "Checking Apache status..."
sudo systemctl status apache2 --no-pager

echo ""
echo "Now open your browser and visit http://localhost or http://127.0.0.1"
echo "Checkpoint 1: Show the default Apache page to your teacher."
