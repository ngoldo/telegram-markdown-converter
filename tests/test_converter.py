"""
Pytest tests for the telegram_markdown_converter module.
"""

from telegram_markdown_converter import convert_markdown


def test_no_markdown() -> None:
    """Test that text with no markdown is correctly escaped."""
    assert convert_markdown('Hello world.') == 'Hello world\\.'


def test_simple_bold() -> None:
    """Test simple bold conversion."""
    assert convert_markdown('**bold text**') == '*bold text*'


def test_simple_italic() -> None:
    """Test simple italic conversion."""
    assert convert_markdown('*italic text*') == '_italic text_'


def test_simple_strikethrough() -> None:
    """Test simple strikethrough conversion."""
    assert convert_markdown('~~strikethrough text~~') == '~strikethrough text~'


def test_simple_underline() -> None:
    """Test simple underline conversion."""
    assert convert_markdown('__underline text__') == '__underline text__'


def test_simple_spoiler() -> None:
    """Test simple spoiler conversion."""
    assert convert_markdown('||spoiler text||') == '||spoiler text||'


def test_inline_code() -> None:
    """Test that inline code is preserved and not escaped."""
    assert convert_markdown(
        'This is `inline code`.') == 'This is `inline code`\\.'


def test_code_block() -> None:
    """Test that code blocks are preserved and not escaped."""
    assert convert_markdown('```\ncode block\n```') == '```\ncode block\n```'


def test_nested_markdown() -> None:
    """Test nested markdown conversion."""
    assert convert_markdown(
        '**bold and *italic* text**') == '*bold and _italic_ text*'
    assert convert_markdown(
        '*italic and __underline__ text*') == '_italic and __underline__ text_'


def test_link() -> None:
    """Test simple link conversion."""
    assert convert_markdown(
        '[link](https://google.com)') == '[link](https://google.com)'


def test_link_with_markdown():
    """Test link with markdown in the text."""
    assert convert_markdown(
        '[**bold link**](https://google.com)') == '[*bold link*](https://google.com)'


def test_special_characters() -> None:
    """Test that special characters are correctly escaped."""
    assert convert_markdown(
        'Characters to escape: `*_~|`') == 'Characters to escape: `*_~|`'
    assert convert_markdown(
        'Characters to escape: .!-=+') == 'Characters to escape: \\.\\!\\-\\=\\+'


def test_code_with_special_chars() -> None:
    """Test that special characters inside code are not escaped."""
    assert convert_markdown('`code with * and _`') == '`code with * and _`'
    assert convert_markdown(
        '```\n**bold in code block**\n```') == '```\n**bold in code block**\n```'


def test_empty_string() -> None:
    """Test that an empty string remains empty."""
    assert convert_markdown('') == ''


def test_already_escaped() -> None:
    """Test that already escaped characters are not double-escaped."""
    assert convert_markdown(
        'This is \\*already escaped\\*') == 'This is \\*already escaped\\*'
