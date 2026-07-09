#!/bin/bash

# VirusTotal CLI Wrapper Installation Script
# This script automates the installation and setup of vt-cli-wrapper

set -e

echo "========================================"
echo "VirusTotal CLI Wrapper - Installation"
echo "========================================"
echo ""

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    OS="Windows"
else
    OS="Unknown"
fi

echo "[1/5] Detected OS: $OS"
echo ""

# Check if uv is installed
echo "[2/5] Checking for uv package manager..."
if ! command -v uv &> /dev/null; then
    echo "⚠ uv not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
else
    echo "✓ uv found"
fi
echo ""

# Create virtual environment
echo "[3/5] Creating virtual environment..."
if [ ! -d ".venv" ]; then
    uv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "[4/5] Installing dependencies..."
source .venv/bin/activate
uv pip install -e .
echo "✓ Dependencies installed"
echo ""

# Create convenience wrapper script
echo "[5/5] Creating convenience wrapper..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WRAPPER_PATH="/usr/local/bin/vt-cli"

cat > "$SCRIPT_DIR/.vt-cli-wrapper" << 'WRAPPER_EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/.venv/bin/activate"
python -m vt_cli_wrapper.cli "$@"
WRAPPER_EOF

chmod +x "$SCRIPT_DIR/.vt-cli-wrapper"

# Try to create symlink for global access
if [ -w /usr/local/bin ]; then
    ln -sf "$SCRIPT_DIR/.vt-cli-wrapper" "$WRAPPER_PATH"
    echo "✓ Global command created at $WRAPPER_PATH"
    GLOBAL_AVAILABLE=1
else
    echo "⚠ Cannot create global command (no permission to /usr/local/bin)"
    echo "  You can add this to your shell profile instead:"
    echo "  alias vt-cli='$SCRIPT_DIR/.vt-cli-wrapper'"
    GLOBAL_AVAILABLE=0
fi
echo ""

echo "========================================"
echo "Installation Complete! ✓"
echo "========================================"
echo ""

if [ $GLOBAL_AVAILABLE -eq 1 ]; then
    echo "You can now use 'vt-cli' from any directory:"
    echo "  vt-cli setup   - Configure your API key"
    echo "  vt-cli scan    - Scan a file"
    echo "  vt-cli quota   - Check your quota"
    echo "  vt-cli --help  - Show all commands"
else
    echo "To use the app from any directory, add this to your shell profile:"
    echo "  alias vt-cli='$SCRIPT_DIR/.vt-cli-wrapper'"
    echo ""
    echo "Or use it directly:"
    echo "  $SCRIPT_DIR/.vt-cli-wrapper setup"
fi
echo ""

# Offer to run setup
read -p "Would you like to configure your API key now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ $GLOBAL_AVAILABLE -eq 1 ]; then
        vt-cli setup
    else
        "$SCRIPT_DIR/.vt-cli-wrapper" setup
    fi
fi
