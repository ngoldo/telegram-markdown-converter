"""
Tests for the streaming Markdown converter.
"""

from telegram_markdown_converter import (
    StreamingMarkdownConverter,
    convert_markdown,
    convert_streaming_markdown,
)


# ---------------------------------------------------------------------------
# Equivalence: complete well-formed text produces identical output
# ---------------------------------------------------------------------------


class TestEquivalence:
    """For complete, well-formed markdown, streaming == standard conversion."""

    def test_plain_text(self) -> None:
        text = "Hello world."
        assert convert_streaming_markdown(text) == convert_markdown(text)

    def test_bold(self) -> None:
        text = "This is **bold** text"
        assert convert_streaming_markdown(text) == convert_markdown(text)

    def test_italic_underscore(self) -> None:
        text = "This is _italic_ text"
        assert convert_streaming_markdown(text) == convert_markdown(text)

    def test_italic_asterisk(self) -> None:
        text = "This is *italic* text"
        assert convert_streaming_markdown(text) == convert_markdown(text)

    def test_strikethrough(self) -> None:
        text = "This is ~~strikethrough~~ text"
        assert convert_streaming_markdown(text) == convert_markdown(text)

    def test_underline(self) -> None:
        text = "This is __underline__ text"
        assert convert_streaming_markdown(text) == convert_markdown(text)

    def test_spoiler(self) -> None:
        text = "This is ||spoiler|| text"
        assert convert_streaming_markdown(text) == convert_markdown(text)

    def test_inline_code(self) -> None:
        text = "This is `code` text"
        assert convert_streaming_markdown(text) == convert_markdown(text)

    def test_code_block(self) -> None:
        text = "```python\nprint('hi')\n```"
        assert convert_streaming_markdown(text) == convert_markdown(text)

    def test_link(self) -> None:
        text = "[example](https://example.com)"
        assert convert_streaming_markdown(text) == convert_markdown(text)

    def test_mixed_complete(self) -> None:
        text = "**bold** and _italic_ with `code` and [link](https://x.com)"
        assert convert_streaming_markdown(text) == convert_markdown(text)

    def test_blockquote(self) -> None:
        text = "> This is a quote"
        assert convert_streaming_markdown(text) == convert_markdown(text)

    def test_empty_string(self) -> None:
        assert convert_streaming_markdown("") == convert_markdown("")


# ---------------------------------------------------------------------------
# Partial bold / italic / underline / strike / spoiler
# ---------------------------------------------------------------------------


class TestPartialFormatting:
    """Auto-closing produces valid MarkdownV2 for incomplete markers."""

    def test_partial_bold(self) -> None:
        result = convert_streaming_markdown("Hello **bold text")
        assert result  # should not raise
        assert "bold text" in result

    def test_partial_italic_underscore(self) -> None:
        result = convert_streaming_markdown("Hello _italic text")
        assert result
        assert "italic text" in result

    def test_partial_italic_asterisk(self) -> None:
        result = convert_streaming_markdown("Hello *italic text")
        assert result
        assert "italic text" in result

    def test_partial_strikethrough(self) -> None:
        result = convert_streaming_markdown("Hello ~~strike text")
        assert result
        assert "strike text" in result

    def test_partial_underline(self) -> None:
        result = convert_streaming_markdown("Hello __underline text")
        assert result
        assert "underline text" in result

    def test_partial_spoiler(self) -> None:
        result = convert_streaming_markdown("Hello ||spoiler text")
        assert result
        assert "spoiler text" in result


# ---------------------------------------------------------------------------
# Partial code blocks and inline code
# ---------------------------------------------------------------------------


class TestPartialCode:
    """Unclosed code fences / backticks are auto-closed."""

    def test_partial_code_block(self) -> None:
        result = convert_streaming_markdown("```python\nprint('hi')")
        assert result
        assert "print" in result

    def test_partial_inline_code(self) -> None:
        result = convert_streaming_markdown("This is `incomplete code")
        assert result
        assert "incomplete code" in result

    def test_partial_code_block_no_newline(self) -> None:
        result = convert_streaming_markdown("```\nsome code")
        assert result


# ---------------------------------------------------------------------------
# Partial links
# ---------------------------------------------------------------------------


class TestPartialLinks:
    """Unclosed [ and [text](url handled gracefully."""

    def test_unclosed_bracket(self) -> None:
        result = convert_streaming_markdown("Check [this link")
        assert result
        assert "Check" in result

    def test_unclosed_url(self) -> None:
        result = convert_streaming_markdown("Check [link](https://exam")
        assert result
        assert "Check" in result


# ---------------------------------------------------------------------------
# Ambiguous trailing characters
# ---------------------------------------------------------------------------


class TestTrailingChars:
    """Trailing marker-like characters are stripped and escaped."""

    def test_trailing_asterisks(self) -> None:
        result = convert_streaming_markdown("Hello **")
        assert result
        # The ** should be escaped, not treated as empty bold
        assert "Hello" in result

    def test_trailing_single_asterisk(self) -> None:
        result = convert_streaming_markdown("Hello *")
        assert result

    def test_trailing_underscore(self) -> None:
        result = convert_streaming_markdown("Hello _")
        assert result

    def test_trailing_tilde(self) -> None:
        result = convert_streaming_markdown("Hello ~")
        assert result

    def test_trailing_double_tilde(self) -> None:
        result = convert_streaming_markdown("Hello ~~")
        assert result

    def test_trailing_pipe(self) -> None:
        result = convert_streaming_markdown("Hello |")
        assert result

    def test_trailing_double_pipe(self) -> None:
        result = convert_streaming_markdown("Hello ||")
        assert result

    def test_trailing_backtick(self) -> None:
        result = convert_streaming_markdown("Hello `")
        assert result

    def test_trailing_triple_backtick(self) -> None:
        result = convert_streaming_markdown("Hello ```")
        assert result

    def test_trailing_backslash(self) -> None:
        result = convert_streaming_markdown("Hello \\")
        assert result


# ---------------------------------------------------------------------------
# Mixed incomplete markers
# ---------------------------------------------------------------------------


class TestMixedIncomplete:
    """Multiple nesting levels of incomplete formatting."""

    def test_bold_and_italic_incomplete(self) -> None:
        result = convert_streaming_markdown("**bold _ital")
        assert result
        assert "bold" in result

    def test_nested_incomplete(self) -> None:
        result = convert_streaming_markdown("**bold _italic_ still bold")
        assert result

    def test_code_then_bold_incomplete(self) -> None:
        result = convert_streaming_markdown("`code` and **bold")
        assert result
        assert "code" in result


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    """Edge cases: empty, whitespace, only markers."""

    def test_empty(self) -> None:
        assert convert_streaming_markdown("") == ""

    def test_whitespace(self) -> None:
        result = convert_streaming_markdown("   ")
        assert result  # whitespace is preserved (escaped)

    def test_only_asterisks(self) -> None:
        result = convert_streaming_markdown("***")
        assert result  # should not crash

    def test_only_backticks(self) -> None:
        result = convert_streaming_markdown("```")
        assert result

    def test_only_tilde(self) -> None:
        result = convert_streaming_markdown("~")
        assert result


# ---------------------------------------------------------------------------
# StreamingMarkdownConverter (stateful class)
# ---------------------------------------------------------------------------


class TestStreamingMarkdownConverter:
    """Tests for the stateful StreamingMarkdownConverter wrapper."""

    def test_feed_accumulates(self) -> None:
        c = StreamingMarkdownConverter()
        r1 = c.feed("Hello ")
        r2 = c.feed("**world**")
        assert "Hello" in r1
        assert "world" in r2
        assert c.raw_text == "Hello **world**"

    def test_finish_uses_standard_converter(self) -> None:
        c = StreamingMarkdownConverter()
        c.feed("**bold**")
        final = c.finish()
        assert final == convert_markdown("**bold**")

    def test_reset_clears_state(self) -> None:
        c = StreamingMarkdownConverter()
        c.feed("some text")
        c.reset()
        assert c.raw_text == ""
        assert c.converted_text == ""

    def test_properties(self) -> None:
        c = StreamingMarkdownConverter()
        c.feed("Hello")
        assert c.raw_text == "Hello"
        assert c.converted_text != ""

    def test_reuse_after_reset(self) -> None:
        c = StreamingMarkdownConverter()
        c.feed("first")
        c.finish()
        c.reset()
        r = c.feed("second")
        assert "second" in r
        assert c.raw_text == "second"

    def test_feed_partial_then_finish(self) -> None:
        """Simulate streaming tokens then finishing."""
        c = StreamingMarkdownConverter()
        c.feed("**bo")
        c.feed("ld**")
        final = c.finish()
        assert final == convert_markdown("**bold**")

    def test_converted_text_updated_on_feed(self) -> None:
        c = StreamingMarkdownConverter()
        c.feed("Hello")
        first = c.converted_text
        c.feed(" world")
        second = c.converted_text
        assert first != second
