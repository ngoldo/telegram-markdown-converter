"""
Module for converting text to safe Markdown formatting.
"""

import re


def convert_markdown(text: str) -> str:
    """
    Function to escape special Markdown characters in text,
    preserving code blocks and inline code.

    :param str text: The text to convert.
    :return str: The converted text.
    """

    # Patterns for code blocks and inline code
    code_block_pattern: re.Pattern[str] = re.compile(
        pattern=r'```(.*?)```',
        flags=re.DOTALL
    )
    inline_code_pattern: re.Pattern[str] = re.compile(pattern=r'`([^`]*?)`')

    # Placeholders for code blocks and inline code
    code_blocks: list[str] = []
    inline_codes: list[str] = []

    def replace_code_block(match: re.Match[str]) -> str:
        """Replace code block with placeholder """
        code_content: str = match.group(1)
        code_blocks.append(code_content)
        return f'CODEBLOCK{len(code_blocks) - 1}'

    text = code_block_pattern.sub(repl=replace_code_block, string=text)

    def replace_inline_code(match: re.Match[str]) -> str:
        """Replace inline code with placeholder"""
        code_content: str = match.group(1)
        inline_codes.append(code_content)
        return f'INLINECODE{len(inline_codes) - 1}'

    text = inline_code_pattern.sub(repl=replace_inline_code, string=text)

    # Escape special markdown characters in text
    special_chars = r'_*[]()~`>#-|=+{}.!'

    def escape_special_chars(match: re.Match[str]) -> str:
        return '\\' + match.group(0)

    def escape_spec(text: str) -> str:
        return re.sub(
            pattern=f'([{re.escape(special_chars)}])',
            repl=escape_special_chars,
            string=text
        )

    text = escape_spec(text)

    def escape_backticks(code: str) -> str:
        """Escape backticks inside code"""
        return code.replace('\\', '\\\\').replace('`', '\\`')

    # Restore code block placeholders with triple backticks
    for i, code_block in enumerate(code_blocks):
        placeholder = f'CODEBLOCK{i}'
        code_block: str = inline_code_pattern.sub(
            repl=replace_inline_code,
            string=code_block
        )
        escaped_code_block: str = escape_backticks(code_block)
        final_code_block: str = escape_spec(escaped_code_block)
        text = text.replace(
            placeholder,
            f'\\`\\`\\`{final_code_block}\\`\\`\\`'
        )

    # Restore inline code placeholders with backticks
    for i, code in enumerate(inline_codes):
        placeholder: str = f'INLINECODE{i}'
        escaped_code: str = escape_backticks(code)
        final_code: str = escape_spec(escaped_code)
        text = text.replace(placeholder, f'\\`{final_code}\\`')

    return text
