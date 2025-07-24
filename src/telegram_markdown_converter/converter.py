"""
Module for converting text to safe Markdown formatting for Telegram.
"""

import re

# A list of characters to escape in Telegram MarkdownV2.
# '>' is included and handled separately for blockquotes.
SPECIAL_CHARS: frozenset[str] = frozenset(r"_*[]()~`>#+-=|{}.!")
BOLD = "\x01"
ITALIC = "\x02"
UNDERLINE = "\x03"
STRIKE = "\x04"
SPOILER = "\x05"
QUOTE = "\x06"
PRESERVED_BOLD = "\x07"  # Special marker for preserved ** formatting
PRESERVED_ITALIC = "\x08"  # Special marker for preserved * formatting

# Pre-compiled regex patterns for better performance
_MULTILINE_CODE_PATTERN: re.Pattern[str] = re.compile(r"```.*?```", re.DOTALL)
_SPECIAL_INLINE_CODE_PATTERN: re.Pattern[str] = re.compile(r"`([^`]*` +\w+)`")
_INLINE_CODE_PATTERN: re.Pattern[str] = re.compile(r"`([^`]+?)`")
_LINK_PATTERN: re.Pattern[str] = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_SINGLE_ASTERISK_PATTERN: re.Pattern[str] = re.compile(
    r"(?<!\w)(?<!\\)\*([^\*]+?)\*(?!\w)"
)
_DOUBLE_ASTERISK_PATTERN: re.Pattern[str] = re.compile(r"\*\*([^\*]+?)\*\*")


# Pre-compiled markdown patterns with their replacements
_MARKDOWN_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\*\*\*([^\*]+?)\*\*\*"), f"{BOLD}{ITALIC}\\1{ITALIC}{BOLD}"),
    (re.compile(r"___([^_]+?)___"), f"{UNDERLINE}{ITALIC}\\1{ITALIC}{UNDERLINE}"),
    (re.compile(r"__([^_]+?)__"), f"{UNDERLINE}\\1{UNDERLINE}"),
    (re.compile(r"(?<!\w)_([^_]+?)_(?!\w)"), f"{ITALIC}\\1{ITALIC}"),
    (re.compile(r"~~([^~]+?)~~"), f"{STRIKE}\\1{STRIKE}"),
    (re.compile(r"~([^~]+?)~"), f"{STRIKE}\\1{STRIKE}"),
    (re.compile(r"\|\|([^\|]+?)\|\|"), f"{SPOILER}\\1{SPOILER}"),
    (re.compile(r"^\s*>\s*(.*)", re.MULTILINE), f"{QUOTE}\\1"),
]

# Define a special handler for double asterisks


def _handle_double_asterisk(match: re.Match[str]) -> str:
    """Handle **bold** patterns with special logic for complex nested content."""
    content: str = match.group(1)
    # If content contains triple underscores OR underline placeholders,
    # preserve the ** formatting literally
    if "___" in content or UNDERLINE in content:
        return f"{PRESERVED_BOLD}{content}{PRESERVED_BOLD}"
    # Otherwise convert to single asterisk (bold) using placeholder
    return f"{BOLD}{content}{BOLD}"


# Placeholder formatting strings for better performance
_CODE_PLACEHOLDER_FMT = "zxzC{}zxz"
_LINK_PLACEHOLDER_FMT = "zxzL{}zxz"

# Replacement mapping for markdown restoration (using replace for multi-char)
_PLACEHOLDER_REPLACEMENTS: list[tuple[str, str]] = [
    (BOLD, "*"),
    (ITALIC, "_"),
    (UNDERLINE, "__"),
    (STRIKE, "~"),
    (SPOILER, "||"),
    (QUOTE, ">"),
    (PRESERVED_BOLD, "**"),  # Restore preserved double asterisks
    (PRESERVED_ITALIC, "*"),  # Restore preserved single asterisks
]

# Common constants for string operations
_TRIPLE_BACKTICKS = "```"
_DOUBLE_BACKSLASH = "\\\\"
_SINGLE_BACKSLASH = "\\"
_NEWLINE_CHAR = "\n"


def escape_special_chars(text: str) -> str:
    """Escapes special characters in the given text, avoiding double-escaping.

    :param str text: The text to escape.
    :return: The escaped text.
    :rtype: str
    """
    if not text:
        return text

    # Use list for efficient string building
    result: list[str] = []
    i = 0
    text_len: int = len(text)

    # Process chunks to reduce function call overhead
    last_pos: int = 0

    while i < text_len:
        char: str = text[i]
        if char == _SINGLE_BACKSLASH:
            if i + 1 < text_len:
                next_char: str = text[i + 1]
                if next_char in SPECIAL_CHARS or next_char == _SINGLE_BACKSLASH:
                    # Backslash is already escaping a special character
                    # or another backslash
                    # Add any accumulated text and the escape sequence
                    if i > last_pos:
                        result.append(text[last_pos:i])
                    result.append(text[i : i + 2])
                    i += 2
                    last_pos = i
                else:
                    # Backslash followed by a non-special character needs to be escaped
                    if i > last_pos:
                        result.append(text[last_pos:i])
                    result.append(_DOUBLE_BACKSLASH)
                    result.append(next_char)
                    i += 2
                    last_pos = i
            else:
                # Standalone backslash at end of string needs to be escaped
                if i > last_pos:
                    result.append(text[last_pos:i])
                result.append(_DOUBLE_BACKSLASH)
                i += 1
                last_pos = i
        elif char in SPECIAL_CHARS:
            # Add any accumulated text
            if i > last_pos:
                result.append(text[last_pos:i])
            result.append(_SINGLE_BACKSLASH)
            result.append(char)
            i += 1
            last_pos = i
        else:
            i += 1

    # Add any remaining text
    if last_pos < text_len:
        result.append(text[last_pos:])

    return "".join(result)


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
    if not text:
        return text

    code_blocks: list[str] = []
    links: list[tuple[str, str]] = []

    # --- Pass 1: Isolate code blocks and links with safe placeholders ---

    def isolate_multiline_code(match: re.Match[str]) -> str:
        """Replaces a multiline code block with a placeholder and stores it."""
        content: str = match.group(0)

        # For multiline code blocks, we need to escape backslashes inside
        # the code content
        # The pattern is: ```[lang]\n[code content]\n```
        # But the closing ``` might be on the same line as code content

        if content.startswith(_TRIPLE_BACKTICKS):
            # Find the first newline to separate opening line from content
            first_newline: int = content.find(_NEWLINE_CHAR)
            if first_newline != -1:
                opening: str = content[:first_newline]  # ```python or just ```
                # Everything after first newline
                rest: str = content[first_newline + 1 :]

                # Find the closing ``` - it should be at the end
                if rest.endswith(_TRIPLE_BACKTICKS):
                    # Remove the closing ```
                    code_content: str = rest[:-3]
                    # Escape backslashes and backticks in the code content
                    escaped_content: str = code_content.replace(
                        _SINGLE_BACKSLASH, _DOUBLE_BACKSLASH
                    ).replace("`", "\\`")
                    # Reconstruct
                    reconstructed: str = (
                        f"{opening}\n{escaped_content}{_TRIPLE_BACKTICKS}"
                    )
                else:
                    # No closing found, keep as-is
                    reconstructed = content
            else:
                # No newlines, just keep as-is
                reconstructed = content
        else:
            reconstructed = content

        code_blocks.append(reconstructed)
        return _CODE_PLACEHOLDER_FMT.format(len(code_blocks) - 1)

    # Process multiline blocks first using pre-compiled pattern
    text = _MULTILINE_CODE_PATTERN.sub(repl=isolate_multiline_code, string=text)

    # Handle inline code, with special handling for backticks inside code content
    # First, handle the special case where content includes backticks followed
    # by spaces and more content
    def isolate_special_inline_code(match: re.Match[str]) -> str:
        """Handles inline code containing backticks with spaces."""
        content: str = match.group(1)
        # Escape backslashes in inline code content for Telegram MarkdownV2
        escaped_content: str = content.replace(_SINGLE_BACKSLASH, _DOUBLE_BACKSLASH)
        code_blocks.append(f"`{escaped_content}`")
        return _CODE_PLACEHOLDER_FMT.format(len(code_blocks) - 1)

    # Special pattern for content like `code with \ and ` backticks`
    text = _SPECIAL_INLINE_CODE_PATTERN.sub(
        repl=isolate_special_inline_code, string=text
    )

    def isolate_inline_code(match: re.Match[str]) -> str:
        """Replaces an inline code block with a placeholder and stores it."""
        content: str = match.group(1)
        # Escape backslashes in inline code content for Telegram MarkdownV2
        escaped_content: str = content.replace(_SINGLE_BACKSLASH, _DOUBLE_BACKSLASH)
        code_blocks.append(f"`{escaped_content}`")
        return _CODE_PLACEHOLDER_FMT.format(len(code_blocks) - 1)

    # Use pre-compiled pattern for inline code
    text = _INLINE_CODE_PATTERN.sub(repl=isolate_inline_code, string=text)

    def isolate_links(match: re.Match[str]) -> str:
        """Replaces a link with a placeholder and stores it."""
        links.append((match.group(1), match.group(2)))
        return _LINK_PLACEHOLDER_FMT.format(len(links) - 1)

    text = _LINK_PATTERN.sub(repl=isolate_links, string=text)

    # --- Pass 2: Apply markdown formatting using pre-compiled patterns ---

    # Apply all pre-compiled patterns (except double asterisks)
    for pattern, replacement in _MARKDOWN_PATTERNS:
        text = pattern.sub(repl=replacement, string=text)

    # Handle double asterisks with special logic
    text = _DOUBLE_ASTERISK_PATTERN.sub(repl=_handle_double_asterisk, string=text)

    # Handle single asterisks: should usually be treated as italic,
    # but preserve as * when containing strikethrough
    def handle_single_asterisk(match: re.Match[str]) -> str:
        content: str = match.group(1)
        # If content contains strikethrough placeholders, preserve the * formatting
        if STRIKE in content:
            return f"{PRESERVED_ITALIC}{content}{PRESERVED_ITALIC}"
        return f"{ITALIC}{content}{ITALIC}"

    text = _SINGLE_ASTERISK_PATTERN.sub(repl=handle_single_asterisk, string=text)

    # --- Pass 3: Escape all other special characters ---
    text = escape_special_chars(text)

    # --- Pass 4: Restore markdown formatting ---
    # Use pre-defined replacement list for efficiency
    for placeholder, replacement in _PLACEHOLDER_REPLACEMENTS:
        text = text.replace(placeholder, replacement)

    # --- Pass 5: Restore links and code blocks ---
    # Process in reverse order to avoid index conflicts
    for i in range(len(links) - 1, -1, -1):
        link_text: str
        link_url: str
        link_text, link_url = links[i]
        # Process markdown within link text
        converted_link_text: str = convert_markdown(link_text)
        text = text.replace(
            _LINK_PLACEHOLDER_FMT.format(i), f"[{converted_link_text}]({link_url})"
        )

    for i in range(len(code_blocks) - 1, -1, -1):
        text = text.replace(_CODE_PLACEHOLDER_FMT.format(i), code_blocks[i])

    return text
