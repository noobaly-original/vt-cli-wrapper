# Windows Installation Guide

This guide will help you install VirusTotal CLI Wrapper on Windows 10/11.

## Prerequisites

- **Windows 10 or Windows 11**
- **Python 3.8+** (or will be installed via uv)
- **uv Package Manager** (fast Python package manager)

## Installation Methods

### Method 1: PowerShell (Recommended) 🚀

**PowerShell** is the modern shell on Windows and provides the best experience.

#### Step 1: Open PowerShell

1. Press `Win + X` and select **Windows PowerShell (Admin)** or **Windows Terminal (Admin)**
2. Navigate to the vt-cli_wrapper directory:
   ```powershell
   cd C:\Path\To\vt-cli_wrapper
   ```

#### Step 2: Run the Installation Script

```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

The script will:
- ✅ Check for uv (install if missing)
- ✅ Create a Python virtual environment
- ✅ Install all dependencies
- ✅ Create wrapper scripts
- ✅ Optionally add to PATH or create PowerShell alias
- ✅ Optionally configure your API key

#### Step 3: Verify Installation

Open a **new PowerShell window** and run:
```powershell
vt-cli --version
```

---

### Method 2: Command Prompt (Batch)

If you prefer Command Prompt, use the batch installation script.

#### Step 1: Open Command Prompt as Administrator

1. Press `Win + R`
2. Type `cmd` and press **Ctrl + Shift + Enter** to run as admin
3. Navigate to the installation directory:
   ```cmd
   cd C:\Path\To\vt-cli_wrapper
   ```

#### Step 2: Run the Installation Script

```cmd
install.cmd
```

The script will:
- ✅ Check for uv
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Create batch wrapper script

#### Step 3: Add to PATH (Optional)

To use `vt-cli` from any directory, add it to your system PATH:

```cmd
setx PATH "%PATH%;C:\Path\To\vt-cli_wrapper"
```

Then restart Command Prompt and verify:
```cmd
vt-cli --version
```

---

### Method 3: Manual Installation

If the automated scripts have issues, follow these steps:

#### Step 1: Install uv

1. Download and install from: [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)
2. Or use Scoop/Chocolatey:
   ```cmd
   scoop install uv
   REM or
   choco install uv
   ```

#### Step 2: Create Virtual Environment

```cmd
cd C:\Path\To\vt-cli_wrapper
uv venv
```

#### Step 3: Activate Virtual Environment

**PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Command Prompt:**
```cmd
.venv\Scripts\activate.bat
```

#### Step 4: Install the Application

```cmd
uv pip install -e .
```

#### Step 5: Verify Installation

```cmd
vt-cli --version
```

---

## Using vt-cli

Once installed, you can use the application from PowerShell or Command Prompt:

### Basic Commands

```powershell
# Configure your API key
vt-cli setup

# Scan a file
vt-cli scan C:\path\to\file.exe

# Check your quota
vt-cli quota

# Show help
vt-cli --help
```

### Scanning Files

**Example 1: Scan a file in current directory**
```powershell
vt-cli scan malware.exe
```

**Example 2: Scan a file with full path**
```powershell
vt-cli scan C:\Downloads\suspicious.zip
```

**Example 3: Check API quota before scanning**
```powershell
vt-cli quota
```

---

## Advanced Setup

### Adding to Windows PATH Permanently

#### Via PowerShell (Admin)

```powershell
$scriptDir = "C:\Path\To\vt-cli_wrapper"
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
if ($currentPath -notlike "*$scriptDir*") {
    [Environment]::SetEnvironmentVariable(
        "PATH",
        "$currentPath;$scriptDir",
        "Machine"
    )
}
```

Then restart PowerShell.

#### Via Environment Variables GUI

1. Press `Win + Pause/Break` to open System Properties
2. Click **Environment Variables**
3. Under "System variables", select **PATH** and click **Edit**
4. Click **New** and add: `C:\Path\To\vt-cli_wrapper`
5. Click **OK** and restart your shell

### Creating a Desktop Shortcut

Create a `.bat` file on your desktop:

```batch
@echo off
cd C:\Path\To\vt-cli_wrapper
powershell -ExecutionPolicy Bypass -File .vt-cli-wrapper.ps1 %*
pause
```

---

## Troubleshooting

### "uv command not found"

**Solution 1:** Install uv manually
- Visit: https://github.com/astral-sh/uv#installation
- Download the Windows installer
- Run the installer

**Solution 2:** Use Scoop (if installed)
```powershell
scoop install uv
```

**Solution 3:** Use Chocolatey (if installed)
```powershell
choco install uv
```

### "Python version not found"

The script will automatically use uv to install Python if needed. If this fails:
- Install Python 3.8+ from https://www.python.org/
- Make sure to check "Add Python to PATH" during installation

### "ExecutionPolicy: File cannot be loaded"

This error occurs when running PowerShell scripts. Solutions:

**Quick fix (one-time):**
```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

**Permanent fix (in admin PowerShell):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Access Denied" errors

Make sure you're running PowerShell or Command Prompt **as Administrator**:
1. Right-click PowerShell/CMD
2. Select **Run as administrator**

### Virtual environment activation fails

**Try this:**
```powershell
# Use absolute path
C:\Path\To\vt-cli_wrapper\.venv\Scripts\Activate.ps1
```

### "vt-cli: The term is not recognized"

The command is not in your PATH. Either:
1. Use full path: `C:\Path\To\.vt-cli-wrapper.bat`
2. Add directory to PATH (see "Advanced Setup" section)
3. Use alias in PowerShell:
   ```powershell
   Set-Alias -Name vt-cli -Value "C:\Path\To\.vt-cli-wrapper.ps1"
   ```

---

## Getting Your VirusTotal API Key

1. Visit [VirusTotal.com](https://www.virustotal.com/)
2. Sign up for a free account (or login if you have one)
3. Go to **My Profile** → **API Key**
4. Copy your API key
5. Run: `vt-cli setup` and paste your key

---

## Windows-Specific Notes

### File Paths

Windows uses backslashes (`\`) for file paths:
```powershell
# Correct
vt-cli scan C:\Users\YourName\Downloads\file.exe

# Also works (forward slashes)
vt-cli scan C:/Users/YourName/Downloads/file.exe
```

### Long File Paths

Windows has a 260-character path limit. If you get path errors, enable long paths:

**PowerShell (Admin):**
```powershell
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
  -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

### Running in Windows Terminal

Windows Terminal is recommended for the best experience:
- Download: https://www.microsoft.com/store/productId/9N0DX20HK701
- Uses PowerShell or Command Prompt with better features

```powershell
# In Windows Terminal
vt-cli setup
vt-cli scan file.exe
```

---

## Next Steps

1. **Configure API Key:** `vt-cli setup`
2. **Check Your Quota:** `vt-cli quota`
3. **Scan Your First File:** `vt-cli scan C:\path\to\file`
4. **Read Documentation:** See [README.md](README.md)

---

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the main [INSTALL.md](INSTALL.md) guide
3. Check the [README.md](README.md) for general information
4. Ensure Python 3.8+ and uv are installed

---

**Enjoy scanning with VirusTotal! 🚀**
