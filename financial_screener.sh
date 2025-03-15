#!/bin/bash
# Financial Screener Utility Wrapper
# Usage: ./financial_screener.sh SYMBOL [--delay SECONDS]

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

# Check if a symbol was provided
if [ $# -eq 0 ]; then
    echo "Usage: ./financial_screener.sh SYMBOL [--delay SECONDS]"
    echo "Example: ./financial_screener.sh TATAMOTORS"
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

# Run the financial screener
echo "Running Financial Screener for symbol: $1"
echo "Use --help for more options (e.g., --delay, --standalone)"
python main.py "$@"
