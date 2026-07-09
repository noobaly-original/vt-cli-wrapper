@echo off
REM VirusTotal CLI Wrapper Installation Script for Windows (Batch Version)
REM This is a simplified installation script using batch
REM For better experience, use: powershell -ExecutionPolicy Bypass -File install.ps1

setlocal enabledelayedexpansion
cls

echo ========================================
echo VirusTotal CLI Wrapper - Installation
echo ========================================
echo.

REM Get current directory
cd /d "%~dp0"
set "SCRIPT_DIR=%CD%"

echo [1/4] Detected OS: Windows
echo.

REM Check if uv is installed
echo [2/4] Checking for uv package manager...
where uv >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ⚠ uv not found.
    echo.
    echo Please install uv from: https://github.com/astral-sh/uv
    echo Then run this script again.
    echo.
    pause
    exit /b 1
) else (
    echo ✓ uv found
)
echo.

REM Create virtual environment
echo [3/4] Creating virtual environment...
if not exist ".venv\" (
    call uv venv
    if %ERRORLEVEL% NEQ 0 (
        echo ✗ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)
echo.

REM Activate and install
echo [4/4] Installing dependencies...
call .venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo ✗ Failed to activate virtual environment
    pause
    exit /b 1
)

call uv pip install -e .
if %ERRORLEVEL% NEQ 0 (
    echo ✗ Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

REM Create batch wrapper
set "WRAPPER_PATH=%SCRIPT_DIR%\.vt-cli-wrapper.bat"
(
    echo @echo off
    echo setlocal enabledelayedexpansion
    echo.
    echo for /f "delims=" %%%%A in ('cd /d "%%~dp0" ^& cd') do set "SCRIPT_DIR=%%%%A"
    echo set "VENV_PATH=!SCRIPT_DIR!\.venv"
    echo.
    echo call "!VENV_PATH!\Scripts\activate.bat"
    echo python -m vt_cli_wrapper.cli %%%%*
) > "%WRAPPER_PATH%"

echo.
echo ========================================
echo Installation Complete! ✓
echo ========================================
echo.

echo Wrapper script created at:
echo   %WRAPPER_PATH%
echo.

echo To use vt-cli from any directory:
echo.
echo Option 1: Add to PATH (requires admin)
echo   setx PATH "%%PATH%%;%SCRIPT_DIR%"
echo   (Then restart Command Prompt)
echo.
echo Option 2: Run directly with full path
echo   %WRAPPER_PATH% setup
echo   %WRAPPER_PATH% scan file.exe
echo.
echo Quick commands:
echo   vt-cli setup   - Configure your API key
echo   vt-cli scan    - Scan a file
echo   vt-cli quota   - Check your quota
echo   vt-cli --help  - Show all commands
echo.

echo Tip: For a better experience, use PowerShell:
echo   powershell -ExecutionPolicy Bypass -File install.ps1
echo.

pause
