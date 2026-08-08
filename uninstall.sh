#!/bin/bash

set -e

APP_DIR="/opt/cyrus-pro"
BIN_PATH="/usr/local/bin/cyrus-pro"
DESKTOP_FILE="/usr/share/applications/cyrus-pro.desktop"
ICON_FILE="/usr/share/icons/hicolor/256x256/apps/cyrus-pro.png"

if [ "$EUID" -ne 0 ]; then
    echo "[!] Run with sudo:"
    echo "    sudo ./uninstall.sh"
    exit 1
fi

echo "[+] Removing Cyrus Pro..."

rm -rf "$APP_DIR"
rm -f "$BIN_PATH"
rm -f "$DESKTOP_FILE"
rm -f "$ICON_FILE"

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database /usr/share/applications >/dev/null 2>&1 || true
fi

echo "[+] Cyrus Pro removed successfully."
