#!/usr/bin/env bash
# Launch the portable Linux build from this folder.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export QT_QPA_PLATFORM="${QT_QPA_PLATFORM:-xcb}"
export QT_XCB_GL_INTEGRATION="${QT_XCB_GL_INTEGRATION:-xcb_glx}"
export QT_OPENGL="${QT_OPENGL:-desktop}"
export PYOPENGL_PLATFORM="${PYOPENGL_PLATFORM:-glx}"
exec "$SCRIPT_DIR/ShroudDesigner/ShroudDesigner" "$@"
