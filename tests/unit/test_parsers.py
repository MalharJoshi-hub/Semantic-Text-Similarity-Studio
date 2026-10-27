"""Unit tests for document format parsers."""

import pytest
from src.chunking.parsers.markdown_parser import parse_markdown
from src.chunking.parsers.plaintext_parser import parse_plaintext
from src.chunking.parsers.html_parser import parse_html


def test_parse_markdown():
    md = """# My Document Title

Here is a paragraph of content.

```python
# code snippet
print("hello")
```

Another concluding sentence.
"""
    res = parse_markdown(md)
    assert res["title"] == "My Document Title"
    assert "Here is a paragraph" in res["content"]
    assert "print(\"hello\")" in res["content"]
    assert "```" not in res["content"]
    assert res["format"] == "markdown"


def test_parse_plaintext():
    text = "First line acting as document header.\nSecond line with details.\nThird line."
    res = parse_plaintext(text)
    assert res["title"] == "First line acting as document header."
    assert res["word_count"] > 0
    assert res["format"] == "text"


def test_parse_html():
    html = """<html>
<head><title>Web Page Title</title></head>
<body>
<h1>Main Heading</h1>
<p>First paragraph of text.</p>
<div>Additional container content.</div>
</body>
</html>"""
    res = parse_html(html)
    assert res["title"] == "Web Page Title"
    assert "Main Heading" in res["content"]
    assert "First paragraph of text." in res["content"]
    assert "<p>" not in res["content"]
    assert res["format"] == "html"
