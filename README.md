# VirusTotal CLI Wrapper

A cross-platform Python command-line tool for the VirusTotal API that intelligently manages file scanning with automatic upload capabilities.

## Features

✨ **Smart File Analysis**
- Checks if file exists on VirusTotal before uploading
- Automatically uploads files not found in VirusTotal database
- Respects API rate limits and upload quotas

🔐 **Secure Configuration**
- Stores API keys securely in platform-specific config directories
- Cross-platform support (Windows, macOS, Linux)
- File permissions set to 600 for security

📊 **Quota Management**
- Tracks daily API request and upload limits
- Displays remaining quota
- Prevents exceeding rate limits
- Automatic daily quota reset

⚡ **Fast & Efficient**
- SHA256 hash calculation for quick lookups
- Progress indicators for long operations
- Formatted output with color coding
- Support for files up to 650 MB

## Installation

### Prerequisites

- Python 3.8 or higher
- VirusTotal API key (free from [virustotal.com](https://www.virustotal.com/))

### Installation from GitHub

Clone the repository and install from source:

```bash
git clone https://github.com/noobaly-original/vt-cli-wrapper.git
cd vt-cli-wrapper
```

**🪟 Windows 10/11:**
See [INSTALL_WINDOWS.md](INSTALL_WINDOWS.md) for detailed instructions. Quick start:

```powershell
# PowerShell (Recommended)
powershell -ExecutionPolicy Bypass -File install.ps1

# Or Command Prompt
install.cmd
```

**🍎 macOS / 🐧 Linux:**
```bash
# Using uv (recommended)
bash install.sh

# Or manual installation
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### Detailed Installation Guides

- See [INSTALL.md](INSTALL.md) for macOS/Linux detailed instructions
- See [INSTALL_WINDOWS.md](INSTALL_WINDOWS.md) for Windows detailed instructions

### Future: PyPI Installation

Once published to PyPI, installation will be as simple as:
```bash
pip install vt-cli-wrapper
```

Check back for updates!

## Quick Start

### 1. Setup Your API Key

```bash
vt-cli setup
```

You'll be prompted to enter your VirusTotal API key. It will be validated and stored securely.

### 2. Scan a File

```bash
vt-cli scan /path/to/your/file
```

The tool will:
- Calculate the file's SHA256 hash
- Check if it exists on VirusTotal
- Display results if found, or upload for analysis
- Show detection statistics and verdict

### 3. Check Your Quota

```bash
vt-cli quota
```

Displays your remaining API requests and upload quota for the day.

## Commands

### `vt-cli setup`
Configure your VirusTotal API key.

```bash
vt-cli setup
```

### `vt-cli scan`
Analyze a file using VirusTotal.

```bash
vt-cli scan <file_path> [OPTIONS]
```

**Options:**
- `--force-upload`: Force upload even if file exists on VirusTotal

**Example:**
```bash
vt-cli scan suspicious.exe
vt-cli scan document.pdf --force-upload
```

### `vt-cli quota`
Display API usage and remaining quota.

```bash
vt-cli quota
```

### `vt-cli reset`
Reset all configuration and API key.

```bash
vt-cli reset
```

### `vt-cli --version`
Display version information.

```bash
vt-cli --version
```

## Configuration

Configuration is stored in platform-specific directories:

- **Windows**: `%APPDATA%\vt-cli-wrapper\vt_config.json`
- **macOS**: `~/.config/vt-cli-wrapper/vt_config.json`
- **Linux**: `~/.config/vt-cli-wrapper/vt_config.json`

The configuration file includes:
- API key
- Daily request count
- Daily upload count
- Last reset date
- API limits

## API Rate Limits

The tool respects VirusTotal's API rate limits:

**Free Tier:**
- 4 requests per minute (approximately 5,760 per day)
- 4 file uploads per minute

**Premium Tier:**
- Higher limits available (configure in config file)

The tool tracks daily usage and prevents exceeding limits.

## File Size Limits

- **Maximum file size**: 650 MB
- Larger files will be rejected with an error message

## Error Handling

The tool provides clear error messages for:
- Invalid or missing API keys
- File not found errors
- Network connectivity issues
- Quota exceeded scenarios
- Upload failures

Example error handling:
```
✗ Daily request quota exceeded. Requests remaining: 0
```

## Platform Support

Tested and verified on:
- ✅ **Windows 10/11** - PowerShell or Command Prompt
  - See [INSTALL_WINDOWS.md](INSTALL_WINDOWS.md) for detailed setup
- ✅ **macOS 10.15+** - zsh, bash
  - Use `bash install.sh` for automated setup
- ✅ **Ubuntu 20.04+** - bash
- ✅ **CentOS 7+** - bash
- ✅ **Debian** - bash

All systems require Python 3.8+ and are fully cross-platform compatible.

## Security Considerations

1. **API Key Storage**: Keys are stored with restricted file permissions (0600)
2. **HTTPS Only**: All API communication uses HTTPS
3. **No Logging**: Sensitive information is never logged
4. **User-Agent**: Identifies as vt-cli-wrapper for API transparency

## Troubleshooting

### "API key not configured"
Run `vt-cli setup` to configure your API key.

### "File not found"
Ensure the file path exists and is readable.

### "Daily quota exceeded"
Your daily limit has been reached. Check back after the quota resets (typically at midnight UTC).

### "Network error"
Check your internet connection and firewall settings.

## Development

### Setup Development Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/
```

### Code Style

Uses PEP 8 with Black formatting:

```bash
black src/
```

## API Documentation

For more information about VirusTotal API:
- [VirusTotal API v3 Documentation](https://developers.virustotal.com/reference)
- [Getting Started Guide](https://developers.virustotal.com/docs)

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Disclaimer

This tool is provided as-is for security research and file scanning purposes. The authors are not responsible for misuse or any damages caused by this tool. Always respect VirusTotal's Terms of Service.

## Changelog

### Version 1.0.0 (Initial Release)
- ✨ Initial release
- 🔍 File lookup by SHA256
- 📤 Automatic file upload
- 📊 Quota tracking
- 🔐 Secure API key storage
- 🌐 Cross-platform support
