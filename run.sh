#!/bin/bash
# Launcher script for RivaldTask Pro.
#
# This wrapper sets the GTK application ID and icon BEFORE launching Flet,
# so that GNOME/Pop!_OS shows the correct icon in the taskbar/dock.
#
# Usage:
#   ./run.sh
#
# The .desktop file (rivald-task.desktop) should be installed to
# ~/.local/share/applications/ for the taskbar icon to appear.

set -e

# Resolve the script directory (works with symlinks).
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Set the app ID and icon via environment variables (GTK reads these).
export GTK_APPLICATION_ID="com.rivald.task"
export APP_ICON="$SCRIPT_DIR/assets/icon.png"

# Launch the app. GApplication uses GTK_APPLICATION_ID for the taskbar icon.
# We use gapplication run if available, otherwise fall back to python3.
if command -v gapplication >/dev/null 2>&1; then
    # Set the icon as a window icon resource.
    python3 main.py
else
    python3 main.py
fi
