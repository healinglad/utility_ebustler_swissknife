@echo off
REM Financial Screener GUI Utility Wrapper for Windows
REM Usage: financial_screener_gui.bat

REM Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

REM Check if pip is installed
where pip >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: pip is not installed or not in PATH
    exit /b 1
)

REM Check if tkinter is installed
python -c "import tkinter" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: tkinter is not installed.
    echo Python's tkinter module is required for the GUI.
    echo Please reinstall Python and select the tcl/tk option during installation.
    exit /b 1
)

REM Navigate to the financial_screener directory
cd /d "%~dp0financial_screener" || exit /b 1

REM Check if requirements are installed
if not exist ".requirements_installed" (
    echo Installing required dependencies...
    pip install -r requirements.txt
    if %ERRORLEVEL% EQU 0 (
        echo. > .requirements_installed
    ) else (
        echo Error: Failed to install dependencies
        exit /b 1
    )
)

REM Run the financial screener GUI
echo Starting Financial Screener GUI...
python gui.py
