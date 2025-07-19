# Contributing to Telegram Markdown Converter

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Development Setup

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/telegram-markdown-converter.git
   cd telegram-markdown-converter
   ```

2. **Set Up the Development Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

## Development Workflow

### Making Changes

1. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write your code following the project's coding standards
   - Add tests for new functionality
   - Update documentation as needed

3. **Run Tests and Linting**
   ```bash
   make test-cov      # Run tests with coverage
   make lint          # Check linting
   make type-check    # Run type checking
   ```

4. **Format Your Code**
   ```bash
   make format        # Format code with black and isort
   ```

### Submitting Changes

1. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add descriptive commit message"
   ```

2. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request**
   - Go to GitHub and create a pull request
   - Provide a clear description of your changes
   - Reference any related issues

## Code Standards

### Python Code Style
- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Write comprehensive docstrings for all public functions and classes
- Keep line length to 88 characters (Black's default)

### Testing
- Write tests for all new functionality
- Aim for high test coverage (>90%)
- Use descriptive test names that explain what is being tested
- Group related tests in classes when appropriate

### Documentation
- Update README.md if adding new features
- Add docstrings to all public functions
- Update CHANGELOG.md following the Keep a Changelog format

## Project Structure

```
telegram-markdown-converter/
├── src/
│   └── telegram_markdown_converter/
│       ├── __init__.py
│       └── converter.py
├── tests/
│   ├── __init__.py
│   └── test_converter.py
├── .github/
│   └── workflows/
│       └── tests.yml
├── pyproject.toml
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── Makefile
├── .pre-commit-config.yaml
├── .gitignore
└── requirements-dev.txt
```

## Testing Guidelines

### Running Tests
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=telegram_markdown_converter --cov-report=html

# Run specific test file
pytest tests/test_converter.py

# Run specific test function
pytest tests/test_converter.py::test_simple_bold
```

### Writing Tests
- Place tests in the `tests/` directory
- Name test files with the `test_` prefix
- Name test functions with the `test_` prefix
- Use descriptive assertions with clear error messages

Example:
```python
def test_bold_conversion():
    """Test that bold markdown is correctly converted."""
    result = convert_markdown('**bold text**')
    assert result == '*bold text*', f"Expected '*bold text*', got '{result}'"
```

## Code Review Process

1. **All Changes Must Be Reviewed**
   - No direct commits to the main branch
   - All changes must go through pull requests

2. **Review Criteria**
   - Code follows project standards
   - Tests pass and coverage is maintained
   - Documentation is updated as needed
   - Changes are backward compatible (unless it's a major version)

3. **Merging**
   - Use "Squash and merge" for feature branches
   - Delete feature branches after merging

## Release Process

1. **Update Version**
   - Update version in `pyproject.toml`
   - Update version in `src/telegram_markdown_converter/__init__.py`

2. **Update Changelog**
   - Add new version section to CHANGELOG.md
   - List all changes in the appropriate categories

3. **Create Release**
   - Tag the release: `git tag -a v1.0.0 -m "Release v1.0.0"`
   - Push tags: `git push origin --tags`
   - Create GitHub release with changelog

## Getting Help

- **Issues**: Open an issue on GitHub for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions and general discussion
- **Email**: Contact the maintainers directly for sensitive issues

## Code of Conduct

Please be respectful and professional in all interactions. We welcome contributions from everyone and are committed to providing a friendly, safe, and welcoming environment for all contributors.

## License

By contributing to this project, you agree that your contributions will be licensed under the same MIT license that covers the project.
