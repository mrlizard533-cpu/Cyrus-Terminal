#!/bin/bash

set -e

APP_NAME="Cyrus Pro"
APP_DIR="/opt/cyrus-pro"
BIN_PATH="/usr/local/bin/cyrus-pro"
DESKTOP_FILE="/usr/share/applications/cyrus-pro.desktop"
ICON_DIR="/usr/share/icons/hicolor/256x256/apps"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[+] Installing Cyrus Pro..."

if [ "$EUID" -ne 0 ]; then
    echo "[!] Run this script with sudo:"
    echo "    sudo ./install.sh"
    exit 1
fi

echo "[+] Checking Python..."

if ! command -v python3 >/dev/null 2>&1; then
    echo "[!] Python 3 is not installed."
    exit 1
fi

echo "[+] Installing Python dependency..."

python3 -m pip install --break-system-packages -r "$SCRIPT_DIR/requirements.txt"

echo "[+] Creating application directories..."

mkdir -p "$APP_DIR"
mkdir -p "$ICON_DIR"

echo "[+] Installing Cyrus Pro..."

cp "$SCRIPT_DIR/cyrus-pro.py" "$APP_DIR/cyrus-pro.py"
chmod 755 "$APP_DIR/cyrus-pro.py"

cat > "$BIN_PATH" <<EOF
#!/bin/bash
exec python3 "$APP_DIR/cyrus-pro.py" "\$@"
EOF

chmod 755 "$BIN_PATH"

if [ -f "$SCRIPT_DIR/assets/icon.png" ]; then
    cp "$SCRIPT_DIR/assets/icon.png" "$ICON_DIR/cyrus-pro.png"
fi

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Cyrus Pro
Comment=Cyrus Terminal
Exec=$BIN_PATH
Icon=cyrus-pro
Terminal=true
Categories=System;Utility;TerminalEmulator;
StartupNotify=true
EOF

chmod 644 "$DESKTOP_FILE"

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database /usr/share/applications >/dev/null 2>&1 || true
fi

echo
echo "[+] Cyrus Pro installed successfully!"
echo "[+] Launch it from the Kali application menu."
