# Telegram Markdown Converter

A Python library for converting standard Markdown formatting to Telegram's MarkdownV2 format, with proper escaping of special characters.

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/ngoldo/telegram-markdown-converter/workflows/Tests/badge.svg)](https://github.com/ngoldo/telegram-markdown-converter/actions)

## Features

- ✅ Convert standard Markdown to Telegram MarkdownV2 format
- ✅ Proper escaping of special characters
- ✅ Preserve code blocks and inline code without modification
- ✅ Handle nested markdown formatting
- ✅ Support for links, bold, italic, strikethrough, underline, and spoiler text
- ✅ Recursive processing of nested markdown structures
- ✅ Type hints for better IDE support

## Installation

### From PyPI (coming soon)

```bash
pip install telegram-markdown-converter
```

### From Source

```bash
git clone https://github.com/ngoldo/telegram-markdown-converter.git
cd telegram-markdown-converter
pip install -e .
```

## Quick Start

```python
from telegram_markdown_converter import convert_markdown

# Basic usage
text = "This is **bold** and *italic* text with a [link](https://example.com)"
converted = convert_markdown(text)
print(converted)  # Output: This is *bold* and _italic_ text with a [link](https://example.com)

# Handle special characters
text = "Special chars: . ! - = + will be escaped"
converted = convert_markdown(text)
print(converted)  # Output: Special chars: \. \! \- \= \+ will be escaped

# Code blocks and inline code are preserved
text = "Here's some `inline code` and a code block:\n```python\nprint('hello')\n```"
converted = convert_markdown(text)
# Code sections remain unchanged
```

## Supported Markdown Elements

| Standard Markdown                     | Telegram MarkdownV2        | Description          |
| ------------------------------------- | -------------------------- | -------------------- |
| `**bold**`                            | `*bold*`                   | Bold text            |
| `***bold italic***`                   | `*\_bold italic\_*`        | Bold and Italic text |
| `*italic*`/`_italic_`                 | `_italic_`                 | Italic text          |
| `~~strikethrough~~`/`~strikethrough~` | `~strikethrough~`          | Strikethrough text   |
| `__underline__`                       | `__underline__`            | Underlined text      |
| `\|\|spoiler\|\|`                     | `\|\|spoiler\|\|`          | Spoiler text         |
| `> blockquote`                        | `>blockquote`              | Blockquotes          |
| `[link](url)`                         | `[link](url)`              | Hyperlinks           |
| `` `inline code` ``                   | `` `inline code` ``        | Inline code          |
| ```` ```code block``` ````            | ```` ```code block``` ```` | Code blocks          |

## API Reference

### `convert_markdown(text: str) -> str`

Converts standard Markdown text to Telegram MarkdownV2 format.

**Parameters:**
- `text` (str): The input text with standard Markdown formatting

**Returns:**
- `str`: The converted text with Telegram MarkdownV2 formatting and properly escaped special characters

**Example:**
```python
result = convert_markdown("**Hello** *world*!")
# Returns: "*Hello* _world_\\!"
```

## Development

### Setting up the development environment

```bash
git clone https://github.com/ngoldo/telegram-markdown-converter.git
cd telegram-markdown-converter
pip install -e ".[dev]"
```

### Running tests

```bash
pytest
```

### Running tests with coverage

```bash
pytest --cov=telegram_markdown_converter --cov-report=html
```

### Code formatting

```bash
black src/ tests/
isort src/ tests/
```

### Type checking

```bash
mypy src/
```

### Pre-commit hooks

```bash
pre-commit install
pre-commit run --all-files
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass (`pytest`)
6. Format your code (`black . && isort .`)
7. Commit your changes (`git commit -am 'Add some amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for use with the Telegram Bot API
- Follows Telegram's MarkdownV2 specification
- Inspired by the need for safe markdown formatting in Telegram bots
