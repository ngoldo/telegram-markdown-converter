"""
A Python package for converting Markdown to Telegram-safe formatting.

This package converts standard Markdown to Telegram's MarkdownV2 format,
handling proper escaping of special characters.
"""

from .converter import convert_markdown

__version__ = "1.0.0"
__author__ = "Evan Boulatoff"
__email__ = "ngoldo@gmail.com"

__all__: list[str] = ["convert_markdown"]
