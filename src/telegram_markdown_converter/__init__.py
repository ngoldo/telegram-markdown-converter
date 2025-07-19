"""
Telegram Markdown Converter - A Python package for converting Markdown to Telegram-safe formatting.

This package provides functionality to convert standard Markdown formatting to
Telegram's MarkdownV2 format, handling proper escaping of special characters.
"""

from .converter import convert_markdown

__version__ = "1.0.0"
__author__ = "Evan Bulatoff"
__email__ = "ngoldo@gmail.com"

__all__ = ["convert_markdown"]
