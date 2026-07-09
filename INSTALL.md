# Installation Guide

## Platform-Specific Guides

- 🪟 **Windows 10/11**: See [INSTALL_WINDOWS.md](INSTALL_WINDOWS.md) for detailed Windows installation
- 🍎 **macOS**: See instructions below
- 🐧 **Linux**: See instructions below

---

## Prerequisites

- **Python**: 3.8 or higher
- **VirusTotal Account**: Free or paid account with API key from https://www.virustotal.com/

## Quick Installation (macOS/Linux)

### Option 1: Install from Source (Development)

```bash
# Clone the repository
git clone https://github.com/yourusername/vt-cli-wrapper.git
cd vt-cli-wrapper

# Create virtual environment (recommended)
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install in development mode
pip install -e .
```

### Option 2: Install via pip (when published)

```bash
pip install vt-cli-wrapper
```

## Getting Your API Key

1. Visit [VirusTotal](https://www.virustotal.com/)
2. Sign up for a free account (or login if you have one)
3. Go to your profile settings → API key
4. Copy your API key

## Initial Setup

After installation, configure your API key:

```bash
vt-cli setup
```

Follow the prompts to enter your API key securely.

## Verify Installation

Test the installation:

```bash
vt-cli --version
vt-cli quota
```

## Troubleshooting Installation

### "Command not found: vt-cli"

**Solution**: The command may not be in your PATH. Try:

```bash
python -m vt_cli_wrapper.cli --version
```

Or install with:

```bash
pip install --user -e .
```

### "ModuleNotFoundError" when running

**Solution**: Make sure you're in the correct virtual environment:

```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows
```

### Issues on Windows

If you encounter issues on Windows, try:

```bash
python -m pip install --upgrade pip
pip install -e .
```

### macOS / Linux Permissions

If you get permission errors:

```bash
sudo pip install -e .
# Or better, use a virtual environment as shown above
```

## Uninstall

To uninstall:

```bash
pip uninstall vt-cli-wrapper
```

## Next Steps

1. Read the [README.md](README.md) for usage instructions
2. Run `vt-cli --help` to see all available commands
3. Start scanning files: `vt-cli scan /path/to/file`
