"""
Streaming-aware Markdown to Telegram MarkdownV2 converter.

Provides ``convert_streaming_markdown`` (stateless) and
``StreamingMarkdownConverter`` (stateful wrapper) for converting
partial / in-progress Markdown that may contain incomplete formatting
markers — e.g. tokens arriving from an LLM.
"""

from __future__ import annotations

import re
from typing import Final

from .converter import convert_markdown, escape_special_chars

# Characters / sequences that could be the start of an incomplete marker
# when they appear at the very end of partial text.
_TRAILING_MARKER_RE: Final[re.Pattern[str]] = re.compile(
    r"(?:"
    r"\\$"            # trailing backslash (incomplete escape)
    r"|`{1,3}$"       # 1-3 trailing backticks
    r"|\*{1,3}$"      # 1-3 trailing asterisks
    r"|_{1,2}$"       # 1-2 trailing underscores
    r"|~{1,2}$"       # 1-2 trailing tildes
    r"|\|{1,2}$"      # 1-2 trailing pipes
    r")"
)

# Patterns for detecting partial (unclosed) links at the end of text.
# Matches: [text  or  [text](url  (no closing paren)
_PARTIAL_LINK_RE: Final[re.Pattern[str]] = re.compile(
    r"\[[^\]]*$"      # unclosed [
    r"|\[[^\]]*\]\([^)]*$"  # [text](url  without closing )
)

# Paired formatting markers we track via a stack.
_PAIRED_MARKERS: Final[list[str]] = ["**", "__", "~~", "||", "*", "_"]


def _strip_trailing_markers(text: str) -> tuple[str, str]:
    """Remove ambiguous trailing characters that could start an incomplete marker.

    Returns ``(clean_text, stripped_chars)``.
    """
    m = _TRAILING_MARKER_RE.search(text)
    if m:
        return text[: m.start()], m.group()

    m = _PARTIAL_LINK_RE.search(text)
    if m:
        return text[: m.start()], m.group()

    return text, ""


def _auto_close_formatting(text: str) -> str:
    """Close any unmatched formatting markers so the text is well-formed.

    1. Balance code fences (````` ``` `````) — if odd count, append a closing fence.
    2. Balance inline backticks (outside fences) — if odd count, append one.
    3. Stack-scan for paired markers and close any still-open ones in LIFO order.
    """
    # --- code fences ---
    fence_count = text.count("```")
    if fence_count % 2 == 1:
        # Ensure closing fence is on its own line
        if not text.endswith("\n"):
            text += "\n"
        text += "```\n"

    # --- inline backticks (outside fences) ---
    # Remove fenced regions before counting stray backticks
    defenced = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    backtick_count = defenced.count("`")
    if backtick_count % 2 == 1:
        text += "`"

    # --- paired markers (stack scan) ---
    # Work on defenced+de-backticked text for scanning purposes only.
    scan = re.sub(r"`[^`]*`", "", defenced)

    stack: list[str] = []
    i = 0
    scan_len = len(scan)

    while i < scan_len:
        matched = False
        # Try longer markers first so ** is matched before *
        for marker in _PAIRED_MARKERS:
            mlen = len(marker)
            if scan[i : i + mlen] == marker:
                if stack and stack[-1] == marker:
                    stack.pop()
                else:
                    stack.append(marker)
                i += mlen
                matched = True
                break
        if not matched:
            i += 1

    # Close remaining open markers in LIFO order
    for marker in reversed(stack):
        text += marker

    return text


def convert_streaming_markdown(text: str) -> str:
    """Convert partial / streaming Markdown to Telegram MarkdownV2.

    This is a stateless function: pass the *full accumulated text so far*
    (not just the latest token).

    It pre-processes the text to handle incomplete formatting before
    delegating to :func:`convert_markdown`:

    1. Strip ambiguous trailing characters that could be the start of a
       new formatting marker.
    2. Auto-close any still-open formatting markers so the text is
       well-formed Markdown.
    3. Call ``convert_markdown()`` on the resulting text.

    For any complete, well-formed Markdown string ``T``,
    ``convert_streaming_markdown(T) == convert_markdown(T)``.

    :param str text: The accumulated Markdown text so far.
    :return: Telegram-safe MarkdownV2 string.
    :rtype: str
    """
    if not text:
        return text

    clean, stripped = _strip_trailing_markers(text)

    if not clean and not stripped:
        return ""

    if clean:
        clean = _auto_close_formatting(clean)
        result = convert_markdown(clean)
    else:
        result = ""

    # Append stripped characters as escaped text so they still appear
    if stripped:
        result += escape_special_chars(stripped)

    return result


class StreamingMarkdownConverter:
    """Stateful wrapper for incremental streaming conversion.

    Usage::

        converter = StreamingMarkdownConverter()
        for token in llm_stream:
            telegram_text = converter.feed(token)
            bot.send_message_draft(chat_id, text=telegram_text)
        final_text = converter.finish()
        bot.send_message(chat_id, text=final_text)
    """

    def __init__(self) -> None:
        self._raw: str = ""
        self._converted: str = ""

    def feed(self, new_text: str) -> str:
        """Append *new_text* and return the full converted result so far."""
        self._raw += new_text
        self._converted = convert_streaming_markdown(self._raw)
        return self._converted

    def finish(self) -> str:
        """Return the final conversion using :func:`convert_markdown`.

        Call this once the full text is available (stream finished).
        """
        self._converted = convert_markdown(self._raw)
        return self._converted

    def reset(self) -> None:
        """Clear accumulated state so the instance can be reused."""
        self._raw = ""
        self._converted = ""

    @property
    def raw_text(self) -> str:
        """The accumulated raw Markdown text."""
        return self._raw

    @property
    def converted_text(self) -> str:
        """The most recent converted result."""
        return self._converted
