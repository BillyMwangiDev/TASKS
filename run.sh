#!/usr/bin/env zsh
# ─────────────────────────────────────────────
#  TASKY — launcher
#  Usage: ./run.sh
# ─────────────────────────────────────────────

set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
VENV="$DIR/.venv"
PYTHON="$VENV/bin/python"
PIP="$VENV/bin/pip"

# 1. Create venv if it doesn't exist
if [ ! -f "$PYTHON" ]; then
    echo "→ Creating virtual environment..."
    python3 -m venv "$VENV"
fi

# 2. Install / upgrade dependencies if requirements.txt changed
STAMP="$VENV/.deps_installed"
REQ="$DIR/requirements.txt"

if [ ! -f "$STAMP" ] || [ "$REQ" -nt "$STAMP" ]; then
    echo "→ Installing dependencies..."
    "$PIP" install --quiet --upgrade pip
    "$PIP" install --quiet -r "$REQ" || {
        # requirements.txt has Windows-only packages; install just PyQt6 as fallback
        "$PIP" install --quiet PyQt6
    }
    touch "$STAMP"
fi

# 3. Launch
echo "→ Launching TASKY..."
exec "$PYTHON" "$DIR/main.py" "$@"
