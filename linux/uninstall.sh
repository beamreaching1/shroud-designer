#!/usr/bin/env bash
# Remove a user-level Shroud Designer install created by install.sh
set -euo pipefail

PREFIX="${PREFIX:-$HOME/.local}"
BIN_NAME="ShroudDesigner"
APP_ID="shroud-designer"

APP_DIR="$PREFIX/share/shroud-designer"
BIN_PATH="$PREFIX/bin/$BIN_NAME"
DESKTOP_PATH="$PREFIX/share/applications/$APP_ID.desktop"
ICON_PATH="$PREFIX/share/icons/hicolor/256x256/apps/$APP_ID.png"

echo "Removing Shroud Designer from $PREFIX ..."
rm -rf "$APP_DIR"
rm -f "$BIN_PATH" "$DESKTOP_PATH" "$ICON_PATH"

if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "$PREFIX/share/applications" >/dev/null 2>&1 || true
fi

echo "Uninstalled."
