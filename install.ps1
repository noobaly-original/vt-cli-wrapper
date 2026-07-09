# VirusTotal CLI Wrapper Installation Script for Windows
# This script automates the installation and setup of vt-cli-wrapper
# Run with: powershell -ExecutionPolicy Bypass -File install.ps1

param(
    [switch]$NoPrompt = $false
)

# Color output helper
function Write-Success {
    Write-Host $args -ForegroundColor Green
}

function Write-Warning {
    Write-Host $args -ForegroundColor Yellow
}

function Write-Error {
    Write-Host $args -ForegroundColor Red
}

# Check if running as admin
function Test-Admin {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Main installation script
Write-Host "========================================"
Write-Host "VirusTotal CLI Wrapper - Installation"
Write-Host "========================================"
Write-Host ""

Write-Host "[1/5] Detected OS: Windows"
Write-Host ""

# Check if uv is installed
Write-Host "[2/5] Checking for uv package manager..."
$uvInstalled = $null -ne (Get-Command uv -ErrorAction SilentlyContinue)

if (-not $uvInstalled) {
    Write-Warning "⚠ uv not found. Installing uv..."
    
    # Download and run uv installer
    $uvInstallerUrl = "https://astral.sh/uv/install.ps1"
    $tempFile = [System.IO.Path]::GetTempFileName()
    
    try {
        Invoke-WebRequest -Uri $uvInstallerUrl -OutFile $tempFile
        & powershell -ExecutionPolicy Bypass -File $tempFile
        Write-Success "✓ uv installed successfully"
    } catch {
        Write-Error "✗ Failed to install uv: $_"
        Write-Host ""
        Write-Host "Please install uv manually from: https://github.com/astral-sh/uv"
        exit 1
    }
} else {
    Write-Success "✓ uv found"
}
Write-Host ""

# Create virtual environment
Write-Host "[3/5] Creating virtual environment..."
$venvPath = Join-Path $PSScriptRoot ".venv"

if (-not (Test-Path $venvPath)) {
    try {
        & uv venv
        Write-Success "✓ Virtual environment created"
    } catch {
        Write-Error "✗ Failed to create virtual environment: $_"
        exit 1
    }
} else {
    Write-Success "✓ Virtual environment already exists"
}
Write-Host ""

# Activate virtual environment and install dependencies
Write-Host "[4/5] Installing dependencies..."
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"

try {
    & $activateScript
    & uv pip install -e .
    Write-Success "✓ Dependencies installed"
} catch {
    Write-Error "✗ Failed to install dependencies: $_"
    exit 1
}
Write-Host ""

# Create convenience wrapper script
Write-Host "[5/5] Creating convenience wrapper..."
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$wrapperPath = Join-Path $scriptDir ".vt-cli-wrapper.bat"
$wrapperPsPath = Join-Path $scriptDir ".vt-cli-wrapper.ps1"

# Create PowerShell wrapper (preferred)
$psWrapperContent = @"
# VirusTotal CLI Wrapper - PowerShell Wrapper
`$scriptDir = Split-Path -Parent `$MyInvocation.MyCommand.Path
`$venvPath = Join-Path `$scriptDir ".venv"
`$activateScript = Join-Path `$venvPath "Scripts\Activate.ps1"

& `$activateScript
python -m vt_cli_wrapper.cli `@args
"@

try {
    Set-Content -Path $wrapperPsPath -Value $psWrapperContent
    Write-Success "✓ PowerShell wrapper created"
} catch {
    Write-Error "✗ Failed to create wrapper script: $_"
    exit 1
}

# Create batch wrapper (optional fallback)
$batWrapperContent = @"
@echo off
REM VirusTotal CLI Wrapper - Batch Wrapper
setlocal enabledelayedexpansion

REM Get the directory where this script is located
for /f "delims=" %%A in ('cd /d "%~dp0" ^& cd') do set "SCRIPT_DIR=%%A"
set "VENV_PATH=%SCRIPT_DIR%\.venv"

REM Activate virtual environment
call "%VENV_PATH%\Scripts\activate.bat"

REM Run the CLI
python -m vt_cli_wrapper.cli %*
"@

try {
    Set-Content -Path $wrapperPath -Value $batWrapperContent -Encoding ASCII
} catch {
    Write-Warning "⚠ Could not create batch wrapper (optional)"
}

Write-Host ""

# Add to PATH or create alias info
$userProfile = $PROFILE.CurrentUserAllHosts
$aliasName = "vt-cli"
$aliasCommand = "powershell -ExecutionPolicy Bypass -File '$wrapperPsPath'"

Write-Host "========================================"
Write-Host "Installation Complete! ✓"
Write-Host "========================================"
Write-Host ""

Write-Host "Available methods to run vt-cli:"
Write-Host ""
Write-Host "Method 1: Using PowerShell alias (Recommended)"
Write-Host "  Add this to your PowerShell profile:"
Write-Host "  Set-Alias -Name vt-cli -Value '$wrapperPsPath' -Scope CurrentUser"
Write-Host ""
Write-Host "  Then reload PowerShell or run: `$PROFILE"
Write-Host ""

Write-Host "Method 2: Using batch file directly"
Write-Host "  $wrapperPath"
Write-Host ""

Write-Host "Method 3: Add to PATH (requires admin)"
if (Test-Admin) {
    Write-Host "  Running as admin - offering to add to PATH..."
    Write-Host ""
    $addToPath = Read-Host "Add wrapper directory to system PATH? (y/n) [n]"
    
    if ($addToPath -eq 'y' -or $addToPath -eq 'Y') {
        try {
            $currentPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
            if ($currentPath -notlike "*$scriptDir*") {
                [Environment]::SetEnvironmentVariable(
                    "PATH",
                    "$currentPath;$scriptDir",
                    "Machine"
                )
                Write-Success "✓ Added to system PATH"
                Write-Host "  Please restart PowerShell to use 'vt-cli' command"
            } else {
                Write-Host "  Already in PATH"
            }
        } catch {
            Write-Error "✗ Failed to add to PATH: $_"
        }
    }
} else {
    Write-Warning "  (Requires administrator privileges)"
}
Write-Host ""

# Offer to add to current user PowerShell profile
if (Test-Path $userProfile) {
    $setupAlias = Read-Host "Add vt-cli alias to PowerShell profile? (y/n) [y]"
    
    if ($setupAlias -ne 'n' -and $setupAlias -ne 'N') {
        try {
            $aliasLine = "Set-Alias -Name vt-cli -Value '$wrapperPsPath' -Scope CurrentUser -Force"
            
            # Check if alias already exists in profile
            if ((Get-Content $userProfile -ErrorAction SilentlyContinue) -notcontains $aliasLine) {
                Add-Content -Path $userProfile -Value "`n# VirusTotal CLI Alias"
                Add-Content -Path $userProfile -Value $aliasLine
                Write-Success "✓ Added alias to PowerShell profile"
                Write-Host "  Run 'vt-cli --help' after restarting PowerShell"
            } else {
                Write-Host "  Alias already in profile"
            }
        } catch {
            Write-Warning "⚠ Could not update profile: $_"
        }
    }
}

Write-Host ""
Write-Host "Quick commands:"
Write-Host "  vt-cli setup   - Configure your API key"
Write-Host "  vt-cli scan    - Scan a file"
Write-Host "  vt-cli quota   - Check your quota"
Write-Host "  vt-cli --help  - Show all commands"
Write-Host ""

# Offer to run setup
if (-not $NoPrompt) {
    $runSetup = Read-Host "Would you like to configure your API key now? (y/n) [n]"
    
    if ($runSetup -eq 'y' -or $runSetup -eq 'Y') {
        & powershell -ExecutionPolicy Bypass -File $wrapperPsPath setup
    }
}

Write-Host ""
Write-Success "Installation complete! Enjoy scanning with VirusTotal! 🚀"
