#!/usr/bin/env python3
"""
Setup verification script for telegram-markdown-converter.

This script verifies that the package is properly installed and functional.
"""

import sys
from collections.abc import Callable


def test_import() -> Callable[..., str] | None:
    """Test that the package can be imported."""
    try:
        from telegram_markdown_converter import convert_markdown
        print('✅ Package import successful')
        return convert_markdown
    except ImportError as e:
        print(f'❌ Package import failed: {e}')
        return None


def test_basic_functionality(convert_markdown: Callable[..., str]) -> bool:
    """Test basic functionality of the converter."""
    test_cases: list[tuple[str, str]] = [
        ('**bold**', '*bold*'),
        ('*italic*', '_italic_'),
        ('Hello world!', 'Hello world\\!'),
        ('`code`', '`code`'),
        ('[link](https://example.com)', '[link](https://example.com)'),
    ]

    all_passed = True
    for input_text, expected in test_cases:
        result: str = convert_markdown(input_text)
        if result == expected:
            print(f"✅ '{input_text}' -> '{result}'")
        else:
            print(f"❌ '{input_text}' -> '{result}' (expected '{expected}')")
            all_passed = False

    return all_passed


def main() -> None:
    """Main verification function."""
    print('Telegram Markdown Converter - Setup Verification')
    print('=' * 50)

    # Test import
    convert_markdown: Callable[..., str] | None = test_import()
    if not convert_markdown:
        sys.exit(1)

    # Test basic functionality
    print('\nTesting basic functionality:')
    if test_basic_functionality(convert_markdown):
        print('\n✅ All tests passed! Package is ready to use.')
        sys.exit(0)
    else:
        print('\n❌ Some tests failed. Please check the installation.')
        sys.exit(1)


if __name__ == '__main__':
    main()
