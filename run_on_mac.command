#!/bin/bash
# Double-click this file in Finder to start StyleBot on a Mac.
# (First time only: right-click it → Open → Open, because macOS blocks
#  scripts downloaded from the internet until you allow them.)

cd "$(dirname "$0")" || exit 1

if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 is not installed."
    echo "Install it from https://www.python.org/downloads/ and try again."
    read -r -p "Press Enter to close..."
    exit 1
fi

python3 stylebot.py
echo
read -r -p "Press Enter to close this window..."
