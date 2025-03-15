#!/bin/bash
# Financial Screener GUI Utility Wrapper
# Usage: ./financial_screener_gui.sh

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "Error: pip is not installed or not in PATH"
    exit 1
fi

# Check if tkinter is installed
python -c "import tkinter" &> /dev/null
if [ $? -ne 0 ]; then
    echo "Error: tkinter is not installed. Please install the python3-tk package."
    echo "On Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "On Fedora: sudo dnf install python3-tkinter"
    echo "On macOS: brew install python-tk"
    exit 1
fi

# Navigate to the financial_screener directory
cd "$(dirname "$0")/financial_screener" || exit 1

# Check if requirements are installed
if [ ! -f ".requirements_installed" ]; then
    echo "Installing required dependencies..."
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        touch .requirements_installed
    else
        echo "Error: Failed to install dependencies"
        exit 1
    fi
fi

# Run the financial screener GUI
echo "Starting Financial Screener GUI..."
python gui.py
