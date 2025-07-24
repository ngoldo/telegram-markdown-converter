"""
Pytest tests for the telegram_markdown_converter module.
"""

from src.telegram_markdown_converter.converter import convert_markdown


def test_no_markdown() -> None:
    """Test that text with no markdown is correctly escaped."""
    assert convert_markdown("Hello world.") == "Hello world\\."


def test_simple_bold() -> None:
    """Test simple bold conversion."""
    assert convert_markdown("**bold text**") == "*bold text*"


def test_simple_italic() -> None:
    """Test simple italic conversion."""
    assert convert_markdown("_italic text_") == "_italic text_"
    assert convert_markdown("*italic text*") == "_italic text_"


def test_simple_strikethrough() -> None:
    """Test simple strikethrough conversion."""
    assert convert_markdown("~strikethrough text~") == "~strikethrough text~"


def test_double_tilde_strikethrough() -> None:
    """Test GitHub-style double tilde strikethrough conversion."""
    assert convert_markdown("~~strikethrough text~~") == "~strikethrough text~"
    assert (
        convert_markdown("Text with ~~strikethrough~~ in middle")
        == "Text with ~strikethrough~ in middle"
    )
    assert (
        convert_markdown("~~Multiple~~ ~~strikethrough~~ sections")
        == "~Multiple~ ~strikethrough~ sections"
    )


def test_simple_underline() -> None:
    """Test simple underline conversion."""
    assert convert_markdown("__underline text__") == "__underline text__"


def test_simple_spoiler() -> None:
    """Test simple spoiler conversion."""
    assert convert_markdown("||spoiler text||") == "||spoiler text||"


def test_simple_blockquote() -> None:
    """Test simple blockquote conversion."""
    assert convert_markdown("> blockquote") == ">blockquote"
    assert convert_markdown(">blockquote") == ">blockquote"
    assert (
        convert_markdown("> blockquote\n> another line") == ">blockquote\n>another line"
    )


def test_inline_code() -> None:
    """Test that inline code is preserved and not escaped."""
    assert convert_markdown("This is `inline code`.") == "This is `inline code`\\."


def test_code_block() -> None:
    """Test that code blocks are preserved and not escaped."""
    assert convert_markdown("```\ncode block\n```") == "```\ncode block\n```"
    assert (
        convert_markdown("```\ncode block with `inline code`\n```")
        == "```\ncode block with \\`inline code\\`\n```"
    )


def test_code_block_with_lang() -> None:
    """Test that code blocks with language are preserved."""
    assert (
        convert_markdown("```python\nprint('Hello')\n```")
        == "```python\nprint('Hello')\n```"
    )


def test_nested_markdown() -> None:
    """Test nested markdown conversion."""
    assert convert_markdown("**bold and _italic_ text**") == "*bold and _italic_ text*"
    assert convert_markdown("*italic **bold** text*") == "_italic *bold* text_"
    assert convert_markdown("_italic **bold** text_") == "_italic *bold* text_"
    assert convert_markdown("***bold italic text***") == "*_bold italic text_*"
    assert (
        convert_markdown("_italic and __underline__ text_")
        == "_italic and __underline__ text_"
    )
    assert convert_markdown(
        (
            "**bold _italic bold ~italic bold strikethrough ||italic bold"
            "strikethrough spoiler||~ __underline italic bold___ bold**"
        )
    ) == (
        "**bold _italic bold ~italic bold strikethrough ||italic bold"
        "strikethrough spoiler||~ __underline italic bold___ bold**"
    )
    assert (
        convert_markdown("\n*Italic with ~~strikethrough~~ inside*")
        == "\n*Italic with ~strikethrough~ inside*"
    )


def test_link() -> None:
    """Test simple link conversion."""
    assert (
        convert_markdown("[link 2](https://google.com)")
        == "[link 2](https://google.com)"
    )


def test_link_with_markdown() -> None:
    """Test link with markdown in the text."""
    assert (
        convert_markdown("[**bold link**](https://google.com)")
        == "[*bold link*](https://google.com)"
    )


def test_special_characters() -> None:
    """Test that special characters are correctly escaped."""
    assert (
        convert_markdown("Characters: _*[]()~`>#+-=|{}.!")
        == "Characters: \\_\\*\\[\\]\\(\\)\\~\\`\\>\\#\\+\\-\\=\\|\\{\\}\\.\\!"
    )


def test_slash_handling() -> None:
    """Test that slashes are correctly handled."""
    assert (
        convert_markdown("Path: C:\\Users\\user\\Documents")
        == "Path: C:\\\\Users\\\\user\\\\Documents"
    )
    assert convert_markdown("C:\\test\\") == "C:\\\\test\\\\"
    assert convert_markdown("C:/test/") == "C:/test/"
    assert convert_markdown("C:\\test\\file.txt") == "C:\\\\test\\\\file\\.txt"
    assert convert_markdown("```python\nprint('Hello')\nC:\\test\\```") == (
        "```python\nprint('Hello')\nC:\\\\test\\\\```"
    )


def test_code_with_special_chars() -> None:
    """Test that special characters inside code are not escaped,
    but backticks and backslashes are.
    """
    assert convert_markdown("`code with * and _`") == "`code with * and _`"
    assert (
        convert_markdown("```\n**bold in code block**\n```")
        == "```\n**bold in code block**\n```"
    )
    assert (
        convert_markdown("`code with \\ and ` backticks`")
        == "`code with \\\\ and ` backticks`"
    )
    assert (
        convert_markdown("`code with ( ) special [.] characters!`")
        == "`code with ( ) special [.] characters!`"
    )


def test_empty_string() -> None:
    """Test that an empty string remains empty."""
    assert convert_markdown("") == ""


def test_already_escaped() -> None:
    """Test that already escaped characters are not double-escaped."""
    assert (
        convert_markdown("This is \\*already escaped\\*")
        == "This is \\*already escaped\\*"
    )


def test_complex_text_with_code() -> None:
    """Test text with code snippets."""
    text = (
        "Of course! Here’s the Python maze shortest path example in English:"
        "\n\n---\n\n### 🧭 Example: Shortest Path in a "
        "Maze using BFS (Python)\n\n```python\nfrom collections import deque\n\n"
        "def shortest_path(maze, start, end):\n"
        "    rows, cols = len(maze), len(maze[0])\n"
        "    queue = deque([(start, [start])])\n"
        "    directions = [(-1,0), (1,0), (0,-1), (0,1)]\n"
        "    visited = {start}\n"
        "```\n\n---\n\n"
        "**What does this do?**\n\n- **Input:**\n"
        "  - A maze (`sample_maze`) as a 2D list: `0` is open, `1` is a wall.\n"
        "  - `start` and `end` points as (row, col) tuples.\n\n"
        "- **How:**\n"
        "  - Uses Breadth-First Search to find from `start` to `end`.\n"
        "  - Moves only up/down/left/right (no diagonals).\n"
        "  - Tracks visited cells to avoid loops.\n\n"
        "- **Output:**\n"
        "  - Prints the list of coordinates, or `None` if not found.\n\n"
        "---\n\n"
        "If you want another code example"
        "(e.g., **bold**, _italic_, ~strikethrough~"
        "\n"
        ">blockquotes"
        "\n"
        "[links](http://example.com)), just let me know—happy to help!"
    )
    expected = (
        "Of course\\! Here’s the Python maze shortest path example in English:\n"
        "\n"
        "\\-\\-\\-\n"
        "\n"
        "\\#\\#\\# 🧭 Example: Shortest Path in a Maze using BFS \\(Python\\)\n"
        "\n"
        "```python\n"
        "from collections import deque\n"
        "\n"
        "def shortest_path(maze, start, end):\n"
        "    rows, cols = len(maze), len(maze[0])\n"
        "    queue = deque([(start, [start])])\n"
        "    directions = [(-1,0), (1,0), (0,-1), (0,1)]\n"
        "    visited = {start}\n"
        "```\n"
        "\n"
        "\\-\\-\\-\n"
        "\n"
        "*What does this do?*\n"
        "\n"
        "\\- *Input:*\n"
        "  \\- A maze \\(`sample_maze`\\) as a 2D list: `0` is open, `1` is a wall\\.\n"
        "  \\- `start` and `end` points as \\(row, col\\) tuples\\.\n"
        "\n"
        "\\- *How:*\n"
        "  \\- Uses Breadth\\-First Search to find from `start` to `end`\\.\n"
        "  \\- Moves only up/down/left/right \\(no diagonals\\)\\.\n"
        "  \\- Tracks visited cells to avoid loops\\.\n"
        "\n"
        "\\- *Output:*\n"
        "  \\- Prints the list of coordinates, or `None` if not found\\.\n"
        "\n"
        "\\-\\-\\-\n"
        "\n"
        "If you want another code example"
        "\\(e\\.g\\., *bold*, _italic_, ~strikethrough~"
        "\n"
        ">blockquotes"
        "\n"
        "[links](http://example.com)\\), just let me know—happy to help\\!"
    )
    assert convert_markdown(text) == expected


def test_path_inline_code() -> None:
    """Test that Windows paths in inline code are correctly escaped."""
    assert (
        convert_markdown("`C:\\Users\\user\\Documents\\Project\\ver_2.3\\`")
        == "`C:\\\\Users\\\\user\\\\Documents\\\\Project\\\\ver_2.3\\\\`"
    )
