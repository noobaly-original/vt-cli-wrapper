# Contributing to VirusTotal CLI Wrapper

First off, thank you for considering contributing to VirusTotal CLI Wrapper! It's people like you that make this tool such a great utility.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs if possible**
* **Include your OS version and Python version**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and expected behavior**

### Pull Requests

* Follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
* Use meaningful commit messages
* Update documentation as needed
* End all files with a newline
* Avoid platform-specific code in core functionality

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/vt-cli-wrapper.git
   cd vt-cli-wrapper
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

4. Run tests:
   ```bash
   pytest tests/
   ```

## Code Style

We use PEP 8 style guide. You can check your code with:

```bash
flake8 src/
black src/ --check
```

Format code with Black:

```bash
black src/
```

## Testing

- Write tests for new features
- Ensure all tests pass before submitting a PR
- Maintain or improve code coverage

```bash
pytest tests/ -v
```

## Documentation

- Update README.md if you change functionality
- Add docstrings to new functions
- Update installation guides if needed

## Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Example:
```
Add support for file scanning with custom parameters

- Add new parameter to scan() function
- Update documentation
- Add test cases

Closes #123
```

## Additional Notes

### Issue and Pull Request Labels

* `bug` - Something isn't working
* `enhancement` - New feature or request
* `documentation` - Improvements or additions to documentation
* `good first issue` - Good for newcomers
* `help wanted` - Extra attention is needed

## Recognition

Contributors will be recognized in:
- The README.md contributors section
- Release notes for significant contributions

---

Thank you for contributing! 🎉
