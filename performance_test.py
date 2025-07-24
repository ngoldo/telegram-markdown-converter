#!/usr/bin/env python3
"""
Simple performance test to measure optimization improvements.
"""

import time
from src.telegram_markdown_converter.converter import convert_markdown


def generate_test_text(size_multiplier: int = 1) -> str:
    """Generate a complex test text for performance testing."""
    base_text = """
# This is a header

This is **bold text** with _italic text_ and __underlined text__.

Here's some code: `print("Hello, world!")` and here's a block:

```python
def example_function():
    return "This is a **test** with special chars: [](){}#+-=|.!"
```

> This is a blockquote with **bold** and _italic_ text.

Some text with ~~strikethrough~~ and ||spoiler|| content.

[Link text](https://example.com) with **bold** inside.

More special characters: _*[]()~`>#+-=|{}.!
And escaped characters: \\_\\*\\[\\]\\(\\)\\~\\`\\>\\#\\+\\-\\=\\|\\{\\}\\.\\!

Complex formatting: ***bold and italic*** and ___underlined italic___.
"""
    return base_text * size_multiplier


def performance_test() -> None:
    """Run performance tests with different text sizes."""
    print("Performance Test Results:")
    print("=" * 50)

    for multiplier in [1, 10, 50, 100]:
        test_text: str = generate_test_text(multiplier)
        text_size: int = len(test_text)

        # Warm up
        convert_markdown(test_text)

        # Time the conversion
        start_time: float = time.perf_counter()
        iterations = 10

        for _ in range(iterations):
            convert_markdown(test_text)

        end_time: float = time.perf_counter()
        avg_time: float = (end_time - start_time) / iterations

        print(f"Text size: {text_size:6d} chars | "
              f"Avg time: {avg_time*1000:7.2f}ms | "
              f"Rate: {text_size/avg_time:8.0f} chars/sec")


if __name__ == "__main__":
    performance_test()
