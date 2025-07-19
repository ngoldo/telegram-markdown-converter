#!/usr/bin/env python3
"""
Example usage of telegram-markdown-converter.

This script demonstrates various uses of the convert_markdown function.
"""

from telegram_markdown_converter import convert_markdown


def main():
    """Demonstrate various markdown conversions."""
    print("Telegram Markdown Converter - Examples")
    print("=" * 40)

    examples = [
        # Basic formatting
        "**Bold text**",
        "*Italic text*",
        "***Bold and italic***",
        "~~Strikethrough~~",
        "__Underline__",
        "||Spoiler text||",

        # Links
        "[GitHub](https://github.com)",
        "[**Bold link**](https://example.com)",

        # Code
        "`inline code`",
        "```\ncode block\nwith multiple lines\n```",

        # Mixed content
        "This is **bold**, this is *italic*, and this has `code`!",
        "Check out [this **amazing** repository](https://github.com/ngoldo/telegram-markdown-converter)",

        # Special characters
        "Characters that need escaping: . ! - = + ( ) { } [ ]",

        # Complex nested example
        "**This is bold with *nested italic* and `code`** - amazing!",
    ]

    for i, example in enumerate(examples, 1):
        print(f"\nExample {i}:")
        print(f"Input:  {example!r}")
        result = convert_markdown(example)
        print(f"Output: {result!r}")


if __name__ == "__main__":
    main()
