#!/bin/bash
# Wrapper script to run kai with its virtual environment

VENV_DIR="/opt/kai-assistant/venv"

if [ -d "$VENV_DIR" ]; then
    # Ensure system binaries are in PATH
    export PATH="/usr/bin:/usr/local/bin:${PATH}"
    
    # Use the virtual environment (kai package is copied there during install)
    exec "$VENV_DIR/bin/python3" -m kai.cli "$@"
else
    # Fallback to system python
    exec python3 -m kai.cli "$@"
fi
