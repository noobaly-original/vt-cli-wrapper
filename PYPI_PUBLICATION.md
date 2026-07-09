# Publishing to PyPI

This document explains how to publish the VirusTotal CLI Wrapper to PyPI (Python Package Index) so users can install it with a simple `pip install vt-cli-wrapper` command.

## Current Status

✅ **Code is ready for PyPI publication**
- Package structure is correct
- setup.py is properly configured
- All metadata is included
- Ready to build and publish

## Prerequisites

Before publishing, you'll need:

1. **PyPI Account**
   - Create account at https://pypi.org/account/register/
   - Verify your email

2. **Build Tools**
   ```bash
   pip install build twine
   ```

3. **PyPI Credentials**
   - Create API token at https://pypi.org/manage/account/token/
   - Save it safely (you'll only see it once)

## Step-by-Step Publication

### 1. Prepare Your Package

Update version number in `setup.py`:
```python
version="1.0.0",  # Update this for new releases
```

Update the version in `src/vt_cli_wrapper/__init__.py`:
```python
__version__ = "1.0.0"
```

### 2. Build Distribution Files

```bash
python -m build
```

This creates:
- `dist/vt-cli-wrapper-1.0.0.tar.gz` - Source distribution
- `dist/vt-cli-wrapper-1.0.0-py3-none-any.whl` - Wheel distribution

### 3. Test Your Package Locally (Optional)

Before uploading to PyPI, test with TestPyPI:

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ vt-cli-wrapper
```

### 4. Publish to PyPI

```bash
# Upload to production PyPI
python -m twine upload dist/*
```

When prompted, use:
- Username: `__token__`
- Password: Your PyPI API token (starts with `pypi-`)

### 5. Verify Publication

```bash
# Install from PyPI
pip install vt-cli-wrapper

# Verify it works
vt-cli --version
```

Check on PyPI: https://pypi.org/project/vt-cli-wrapper/

## Automated Publishing with GitHub Actions (Optional)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build distribution
      run: python -m build
    - name: Publish to PyPI
      run: |
        twine upload dist/*
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

Then:
1. Add your PyPI API token as a GitHub secret named `PYPI_API_TOKEN`
2. Create a release on GitHub
3. The action automatically publishes to PyPI

## After Publication

### Update Documentation

Once published to PyPI, update:
- README.md - Change installation instructions
- INSTALL.md - Add simple pip install
- Any examples using the GitHub install method

### Announce the Release

- Create a GitHub Release
- Update project description on PyPI
- Share on Python communities

## Version Numbering

Follow Semantic Versioning:
- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

Examples:
- 1.0.0 - Initial release
- 1.1.0 - New features added
- 1.1.1 - Bug fix
- 2.0.0 - Breaking changes

## Maintenance

After initial publication:

1. **Update for New Releases**
   - Update version in setup.py
   - Update __version__ in __init__.py
   - Create release notes
   - Publish new version

2. **Monitor Dependencies**
   - Keep requirements.txt updated
   - Test with latest Python versions
   - Address security issues promptly

3. **Handle Issues**
   - Fix bugs reported on GitHub
   - Release patches for critical issues
   - Maintain backward compatibility when possible

## Troubleshooting

### Upload fails with "invalid token"
- Verify API token is correct
- Check it hasn't expired
- Use new token if needed

### Version already exists
- Update version number in setup.py
- Can't re-upload same version
- Increment version even for test uploads

### Package name taken
- Choose different name in setup.py
- Check PyPI for similar packages
- Name must be unique on PyPI

### Test upload succeeds but production fails
- Verify you're using `twine upload` (not testpypi)
- Check API credentials
- Ensure no typos in token

## Additional Resources

- **PyPI Documentation:** https://packaging.python.org/
- **Setuptools Guide:** https://setuptools.pypa.io/
- **Twine Documentation:** https://twine.readthedocs.io/
- **Semantic Versioning:** https://semver.org/

## Quick Checklist

Before publishing:
- [ ] Update version number
- [ ] Run tests: `pytest tests/`
- [ ] Update CHANGELOG
- [ ] Build distribution: `python -m build`
- [ ] Test locally: `pip install dist/*.whl`
- [ ] Publish: `twine upload dist/*`
- [ ] Verify on PyPI
- [ ] Update documentation
- [ ] Create GitHub release

---

**Once published to PyPI, users can install with:**
```bash
pip install vt-cli-wrapper
```

This eliminates the need for GitHub cloning and manual installation! 🚀
