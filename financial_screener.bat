@echo off
REM Financial Screener Utility Wrapper for Windows
REM Usage: financial_screener.bat SYMBOL [--delay SECONDS]

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

REM Check if a symbol was provided
if "%~1"=="" (
    echo Usage: financial_screener.bat SYMBOL [--delay SECONDS]
    echo Example: financial_screener.bat TATAMOTORS
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

REM Run the financial screener
echo Running Financial Screener for symbol: %1
echo Use --help for more options (e.g., --delay, --standalone)
python main.py %*
