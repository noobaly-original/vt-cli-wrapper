# Security Policy

## Sensitive Information Protection

This project has been audited and verified to contain NO hardcoded credentials, API keys, or other sensitive information.

### What is Protected

✅ **API Keys**
- Stored locally in platform-specific directories (NOT in repository)
- Never hardcoded in source code
- Encrypted with file permissions (0600 on Unix systems)
- Stored locations:
  - Windows: `%APPDATA%\vt-cli-wrapper\vt_config.json`
  - macOS/Linux: `~/.config/vt-cli-wrapper/vt_config.json`

✅ **Configuration Files**
- Local config files are in `.gitignore`
- Never committed to repository
- `.env` files excluded from version control

✅ **Credentials**
- No hardcoded passwords or tokens in code
- No test credentials exposed
- Environment variables used for sensitive data
- `.env.example` provided as template only

### Files Excluded from Repository

The following files containing sensitive information are NEVER committed:

```
.venv/                  # Virtual environment
.env                    # Environment variables
vt_config.json         # User configuration with API key
.venv/                 # Python packages
```

### Security Best Practices

1. **API Key Management**
   - Keys are stored with restricted permissions (0600)
   - Only accessible by the user who created them
   - HTTPS-only communication with VirusTotal API

2. **No Sensitive Logging**
   - API keys are never logged
   - Credentials never appear in debug output
   - File paths handled securely

3. **Code Review**
   - All code audited for hardcoded credentials
   - No secrets in documentation
   - Clean git history

## Reporting Security Issues

If you discover a security vulnerability, please email your findings to your security contact instead of using the public issue tracker.

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested remediation

Do NOT open a public GitHub issue for security vulnerabilities.

## Dependency Security

This project uses minimal dependencies:
- `requests>=2.31.0` - HTTP client library
- `click>=8.1.0` - CLI framework
- `tabulate>=0.9.0` - Table formatting

All dependencies:
- Are actively maintained
- Have security patches applied
- Are verified on installation

Monitor dependency updates with:
```bash
pip list --outdated
```

## Update Policy

Security patches will be released as soon as vulnerabilities are discovered and fixed.

## HTTPS Communication

All communication with VirusTotal API is encrypted using HTTPS with certificate validation.

## Local File Permissions

Configuration files are created with secure permissions:
- UNIX/Linux: 0600 (read/write owner only)
- Windows: Restricted ACL (user only)

---

**Last Updated:** 2026-07-09
