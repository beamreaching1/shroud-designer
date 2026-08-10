#!/usr/bin/env bash
# Install Shroud Designer for the current user under ~/.local
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_SRC="$SCRIPT_DIR/ShroudDesigner"
BIN_NAME="ShroudDesigner"
APP_ID="shroud-designer"

PREFIX="${PREFIX:-$HOME/.local}"
APP_DIR="$PREFIX/share/shroud-designer"
BIN_DIR="$PREFIX/bin"
DESKTOP_DIR="$PREFIX/share/applications"
ICON_DIR="$PREFIX/share/icons/hicolor/256x256/apps"

if [[ ! -x "$APP_SRC/$BIN_NAME" ]]; then
  echo "Missing packaged app at: $APP_SRC/$BIN_NAME" >&2
  echo "Run ./build.sh from the project root first, or use a release folder." >&2
  exit 1
fi

echo "Installing Shroud Designer to $PREFIX ..."
mkdir -p "$APP_DIR" "$BIN_DIR" "$DESKTOP_DIR" "$ICON_DIR"
rm -rf "$APP_DIR"
mkdir -p "$APP_DIR"
cp -a "$APP_SRC/." "$APP_DIR/"
chmod +x "$APP_DIR/$BIN_NAME"

# Wrapper so PATH lookup works and working directory is stable.
# Prefer GLX/desktop OpenGL (more reliable than EGL with NVIDIA/X11).
cat > "$BIN_DIR/$BIN_NAME" <<EOF
#!/usr/bin/env bash
export QT_QPA_PLATFORM="\${QT_QPA_PLATFORM:-xcb}"
export QT_XCB_GL_INTEGRATION="\${QT_XCB_GL_INTEGRATION:-xcb_glx}"
export QT_OPENGL="\${QT_OPENGL:-desktop}"
export PYOPENGL_PLATFORM="\${PYOPENGL_PLATFORM:-glx}"
exec "$APP_DIR/$BIN_NAME" "\$@"
EOF
chmod +x "$BIN_DIR/$BIN_NAME"

# Icon
if [[ -f "$SCRIPT_DIR/shroud-designer.png" ]]; then
  cp "$SCRIPT_DIR/shroud-designer.png" "$ICON_DIR/$APP_ID.png"
elif [[ -f "$APP_DIR/_internal/assets/shroud-designer.png" ]]; then
  cp "$APP_DIR/_internal/assets/shroud-designer.png" "$ICON_DIR/$APP_ID.png"
fi

# Desktop entry with absolute Exec path
DESKTOP_OUT="$DESKTOP_DIR/$APP_ID.desktop"
sed \
  -e "s|^Exec=.*|Exec=$BIN_DIR/$BIN_NAME|" \
  -e "s|^Icon=.*|Icon=$APP_ID|" \
  "$SCRIPT_DIR/shroud-designer.desktop" > "$DESKTOP_OUT"
chmod 644 "$DESKTOP_OUT"

if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "$DESKTOP_DIR" >/dev/null 2>&1 || true
fi
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
  gtk-update-icon-cache -f -t "$PREFIX/share/icons/hicolor" >/dev/null 2>&1 || true
fi

echo
echo "Installed."
echo "  Binary:  $BIN_DIR/$BIN_NAME"
echo "  Desktop: $DESKTOP_OUT"
echo
echo "Launch with:  $BIN_NAME"
echo "Or open \"Shroud Designer\" from your application menu."
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
  echo
  echo "Note: $BIN_DIR is not on your PATH. Add this to your shell profile:"
  echo "  export PATH=\"$BIN_DIR:\$PATH\""
fi
