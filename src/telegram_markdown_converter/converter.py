"""
Module for converting text to safe Markdown formatting for Telegram.
"""

import re


def convert_markdown(text: str) -> str:
    """Function to convert markdown and escape special characters for Telegram,
    preserving code blocks and inline code. This function is designed to be
    called recursively to handle nested markdown structures.

    :param str text: The text to convert.
    :return str: The converted text.
    :rtype: str
    """

    # Placeholders for code blocks and markdown entities
    code_items: list[str] = []
    md_items: list[tuple[str, str | tuple[str, str]]] = []

    # Isolate code blocks and inline code first, as they are not processed for markdown.
    def isolate_code(match: re.Match[str]) -> str:
        """Isolate code block with placeholder.

        :param `re.Match[str]` match: The regex match object.
        :return: A placeholder for the code block.
        :rtype: str
        """
        # Escape backslashes and backticks inside code as per Telegram spec
        content: str = match.group(1).replace('\\', '\\\\').replace('`', '\\`')

        if match.group(0).startswith('```'):
            code_items.append(f'```{content}```')
        else:
            code_items.append(f'`{content}`')

        # Return a placeholder for the code block
        return f'PLACEHOLDERCODE{len(code_items)-1}'

    text = re.sub(
        pattern=r'```(.*?)```',
        repl=isolate_code,
        string=text,
        flags=re.DOTALL
    )
    text = re.sub(
        pattern=r'`(.*?)`',
        repl=isolate_code,
        string=text
    )

    # Isolate markdown entities and process their content recursively.
    def isolate_md(
            match: re.Match[str],
            md_type: str
    ) -> str:
        """Isolate markdown entity with placeholder and recurse on content.

        :param `re.Match[str]` match: The regex match object.
        :param str md_type: The type of markdown entity (e.g., 'bold', 'italic', etc.).
        :return: A placeholder for the markdown entity.
        :rtype: str
        """
        if md_type == 'link':
            link_text: str = convert_markdown(match.group(1))
            # The URL should not be processed or escaped
            link_url: str = match.group(2)
            md_items.append((md_type, (link_text, link_url)))
        else:
            content: str = convert_markdown(match.group(1))
            md_items.append((md_type, content))

        # Return a placeholder for the markdown entity
        return f'PLACEHOLDERMD{len(md_items)-1}'

    # The order of replacement is important to handle nested and combined styles.
    # Handle links first.
    text = re.sub(
        pattern=r'(?<!\\)\[([^\]]+)\]\(([^)]+)\)',
        repl=lambda m: isolate_md(m, 'link'),
        string=text,
        flags=re.DOTALL
    )
    # Handle standard markdown bold/italic combinations first.
    text = re.sub(
        pattern=r'(?<!\\)\*\*\*(.*?)(?<!\\)\*\*\*',
        repl=lambda m: isolate_md(m, 'bold_italic'),
        string=text,
        flags=re.DOTALL
    )
    text = re.sub(
        pattern=r'(?<!\\)\*\*(.*?)(?<!\\)\*\*',
        repl=lambda m: isolate_md(m, 'bold'),
        string=text,
        flags=re.DOTALL
    )
    text = re.sub(
        pattern=r'(?<!\\)\*(.*?)(?<!\\)\*',
        repl=lambda m: isolate_md(m, 'italic'),
        string=text,
        flags=re.DOTALL
    )
    text = re.sub(
        pattern=r'(?<!\\)~~(.*?)~~',
        repl=lambda m: isolate_md(m, 'strike'),
        string=text,
        flags=re.DOTALL
    )
    text = re.sub(
        pattern=r'(?<!\\)__(.*?)__',
        repl=lambda m: isolate_md(m, 'underline'),
        string=text,
        flags=re.DOTALL
    )
    text = re.sub(
        pattern=r'(?<!\\)\|\|(.*?)\|\|',
        repl=lambda m: isolate_md(m, 'spoiler'),
        string=text,
        flags=re.DOTALL
    )

    # Escape any remaining special characters in the text.
    special_chars = r'_*[]()~`>#+-=|{}.!'
    text = re.sub(
        pattern=f'(?<!\\\\)([{re.escape(special_chars)}])',
        repl=r'\\\1',
        string=text
    )

    # Restore markdown entities with the correct Telegram formatting.
    for i, (md_type, content) in enumerate(md_items):
        placeholder: str = f"PLACEHOLDERMD{i}"
        if md_type == 'link':
            link_text: str
            link_url: str
            link_text, link_url = content
            text = text.replace(placeholder, f'[{link_text}]({link_url})')
        elif md_type == 'bold_italic':
            text = text.replace(placeholder, f'*_{content}_*')
        elif md_type == 'bold':
            text = text.replace(placeholder, f'*{content}*')
        elif md_type == 'italic':
            text = text.replace(placeholder, f'_{content}_')
        elif md_type == 'strike':
            text = text.replace(placeholder, f'~{content}~')
        elif md_type == 'underline':
            text = text.replace(placeholder, f'__{content}__')
        elif md_type == 'spoiler':
            text = text.replace(placeholder, f'||{content}||')

    # Restore code blocks.
    for i, code in enumerate(code_items):
        text = text.replace(f'PLACEHOLDERCODE{i}', code)

    return text
