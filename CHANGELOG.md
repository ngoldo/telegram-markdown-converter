# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial repository organization and packaging setup
- Comprehensive test suite
- CI/CD pipeline with GitHub Actions
- Development tooling (black, isort, flake8, mypy)
- Pre-commit hooks
- Documentation and README

## [1.0.0] - 2025-01-19

### Added
- Initial implementation of `convert_markdown` function
- Support for standard Markdown to Telegram MarkdownV2 conversion
- Proper escaping of special characters
- Preservation of code blocks and inline code
- Support for nested markdown formatting
- Support for links, bold, italic, strikethrough, underline, and spoiler text
- Recursive processing of markdown structures
- Type hints for better IDE support
