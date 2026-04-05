"""
A Python package for converting Markdown to Telegram-safe formatting.

This package converts standard Markdown to Telegram's MarkdownV2 format,
handling proper escaping of special characters.
"""

from importlib.metadata import version

from .converter import convert_markdown, escape_special_chars
from .streaming import StreamingMarkdownConverter, convert_streaming_markdown

__version__ = version("telegram-markdown-converter")
__author__ = "Evan Boulatoff"
__email__ = "ngoldo@gmail.com"

__all__: list[str] = [
    "convert_markdown",
    "escape_special_chars",
    "convert_streaming_markdown",
    "StreamingMarkdownConverter",
]
