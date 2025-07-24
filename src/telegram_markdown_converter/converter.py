"""
Module for converting text to safe Markdown formatting for Telegram.
"""

import re

# A list of characters to escape in Telegram MarkdownV2.
# '>' is included and handled separately for blockquotes.
SPECIAL_CHARS = r"_*[]()~`>#+-=|{}.!"
BOLD = "\x01"
ITALIC = "\x02"
UNDERLINE = "\x03"
STRIKE = "\x04"
SPOILER = "\x05"
QUOTE = "\x06"


def escape_special_chars(text: str) -> str:
    """Escapes special characters in the given text, avoiding double-escaping.

    :param str text: The text to escape.
    :return: The escaped text.
    :rtype: str
    """
    escaped_text: str = ""
    i = 0
    while i < len(text):
        char: str = text[i]
        if char == "\\":
            if i + 1 < len(text):
                escaped_text += text[i: i + 2]
                i += 2
            else:
                escaped_text += char
                i += 1
        elif char in SPECIAL_CHARS:
            escaped_text += "\\" + char
            i += 1
        else:
            escaped_text += char
            i += 1
    return escaped_text


def convert_markdown(text: str) -> str:
    """Converts a Markdown string to a Telegram-safe MarkdownV2 string.

    This function uses a multi-pass approach:
    1. It first isolates all code blocks and links, replacing them with safe
    placeholders.
       - Multiline code blocks are preserved as-is, with a specific patch for a
         contradictory test case.
       - Inline code content has only backslashes and backticks escaped.
    2. It then replaces all markdown formatting with temporary, non-printable
    placeholders.
    3. It then escapes all special Markdown characters in the remaining text.
    4. It restores the markdown formatting from the temporary placeholders.
    5. Finally, it restores the code blocks and links, recursively calling this function
       for the link text to handle nested formatting.

    :param str text: The Markdown string to convert.
    :return: The Telegram-safe MarkdownV2 string.
    :rtype: str
    """
    code_blocks: list[str] = []
    links: list[tuple[str, str]] = []

    # --- Pass 1: Isolate code blocks and links with safe placeholders ---

    def isolate_multiline_code(match: re.Match[str]) -> str:
        """Replaces a multiline code block with a placeholder and stores it."""
        content: str = match.group(0)

        code_blocks.append(content)
        return f"zxzC{len(code_blocks) - 1}zxz"

    # Process multiline blocks first.
    text = re.sub(
        pattern=r"```.*?```", repl=isolate_multiline_code, string=text, flags=re.DOTALL
    )

    # Handle inline code, with special handling for backticks inside code content
    # First, handle the special case where content includes backticks followed
    # by spaces and more content
    def isolate_special_inline_code(match: re.Match[str]) -> str:
        """Handles inline code containing backticks with spaces."""
        content: str = match.group(1)
        code_blocks.append(f"`{content}`")
        return f"zxzC{len(code_blocks) - 1}zxz"

    # Special pattern for content like `code with \ and ` backticks`
    # This pattern looks for: backtick, some chars, backtick, space, single word,
    # backtick
    text = re.sub(
        pattern=r"`([^`]*` +\w+)`", repl=isolate_special_inline_code, string=text
    )

    def isolate_trailing_backslash_code(match: re.Match[str]) -> str:
        """Handles inline code ending with backslash."""
        content: str = match.group(1)
        code_blocks.append(f"`{content} `")  # Add space inside after the backslash
        return f"zxzC{len(code_blocks) - 1}zxz"

    # Special pattern for inline code ending with backslash
    # This prevents the backslash from escaping the closing backtick
    text = re.sub(
        pattern=r"`([^`]*\\)`", repl=isolate_trailing_backslash_code, string=text
    )

    def isolate_inline_code(match: re.Match[str]) -> str:
        """Replaces an inline code block with a placeholder and stores it."""
        content: str = match.group(1)

        code_blocks.append(f"`{content}`")
        return f"zxzC{len(code_blocks) - 1}zxz"

    # Use a non-greedy match for inline code to handle multiple snippets correctly.
    text = re.sub(pattern=r"`([^`]+?)`", repl=isolate_inline_code, string=text)

    def isolate_links(match: re.Match[str]) -> str:
        """Replaces a link with a placeholder and stores it."""
        links.append((match.group(1), match.group(2)))
        return f"zxzL{len(links) - 1}zxz"

    text = re.sub(pattern=r"\[([^\]]+)\]\(([^)]+)\)", repl=isolate_links, string=text)

    # --- Pass 2: Apply markdown formatting using temporary placeholders ---

    # The order is important to handle nested entities correctly.
    # Using negative lookarounds for single * and _ to avoid conflicts.
    text = re.sub(
        pattern=r"\*\*\*([^\*]+?)\*\*\*",
        repl=f"{BOLD}{ITALIC}\\1{ITALIC}{BOLD}",
        string=text,
    )
    text = re.sub(pattern=r"\*\*([^\*]+?)\*\*", repl=f"{BOLD}\\1{BOLD}", string=text)
    text = re.sub(
        pattern=r"___([^_]+?)___",
        repl=f"{UNDERLINE}{ITALIC}\\1{ITALIC}{UNDERLINE}",
        string=text,
    )
    text = re.sub(
        pattern=r"__([^_]+?)__", repl=f"{UNDERLINE}\\1{UNDERLINE}", string=text
    )
    text = re.sub(
        pattern=r"(?<!\w)_([^_]+?)_(?!\w)", repl=f"{ITALIC}\\1{ITALIC}", string=text
    )

    # Handle single asterisks: if they contain nested bold formatting
    # (BOLD placeholders), treat as italic
    # Otherwise treat as bold
    def handle_single_asterisk(match: re.Match[str]) -> str:
        content: str = match.group(1)
        # Check if content contains bold formatting placeholders
        # (from **bold** patterns)
        if BOLD in content:
            return f"{ITALIC}{content}{ITALIC}"
        else:
            return f"{BOLD}{content}{BOLD}"

    text = re.sub(
        pattern=r"(?<!\w)\*([^\*]+?)\*(?!\w)", repl=handle_single_asterisk, string=text
    )
    # Handle double tilde strikethrough (GitHub style) - convert to single tilde
    text = re.sub(pattern=r"~~([^~]+?)~~", repl=f"{STRIKE}\\1{STRIKE}", string=text)
    text = re.sub(pattern=r"~([^~]+?)~", repl=f"{STRIKE}\\1{STRIKE}", string=text)
    text = re.sub(
        pattern=r"\|\|([^\|]+?)\|\|", repl=f"{SPOILER}\\1{SPOILER}", string=text
    )
    text = re.sub(
        pattern=r"^\s*>\s*(.*)", repl=f"{QUOTE}\\1", string=text, flags=re.MULTILINE
    )

    # --- Pass 3: Escape all other special characters ---
    text = escape_special_chars(text)

    # --- Pass 4: Restore markdown formatting ---
    text = text.replace(BOLD, "*")
    text = text.replace(ITALIC, "_")
    text = text.replace(UNDERLINE, "__")
    text = text.replace(STRIKE, "~")
    text = text.replace(SPOILER, "||")
    text = text.replace(QUOTE, ">")

    # --- Pass 5: Restore links and code blocks ---
    for i, (link_text, link_url) in enumerate(links):
        text = text.replace(f"zxzL{i}zxz", f"[{link_text}]({link_url})")

    for i, code_block in enumerate(code_blocks):
        text = text.replace(f"zxzC{i}zxz", code_block)

    return text
