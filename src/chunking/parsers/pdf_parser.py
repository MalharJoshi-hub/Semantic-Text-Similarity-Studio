"""PDF binary stream extraction parser."""

import io
from typing import Dict, Any


def parse_pdf_stream(stream_or_bytes) -> Dict[str, Any]:
    """Extract text and metadata from PDF bytes or stream using PyPDF2 / pypdf."""
    try:
        import PyPDF2
        reader_cls = PyPDF2.PdfReader
    except ImportError:
        import pypdf
        reader_cls = pypdf.PdfReader

    if isinstance(stream_or_bytes, bytes):
        stream = io.BytesIO(stream_or_bytes)
    else:
        stream = stream_or_bytes

    reader = reader_cls(stream)
    pages_text = []
    for idx, page in enumerate(reader.pages):
        page_content = page.extract_text() or ""
        if page_content.strip():
            pages_text.append(f"--- Page {idx + 1} ---\n{page_content.strip()}")

    full_text = "\n\n".join(pages_text).strip()
    title = "Extracted PDF Document"
    if reader.metadata and reader.metadata.title:
        title = str(reader.metadata.title)
    elif pages_text:
        first_line = pages_text[0].split("\n")[0]
        if first_line:
            title = first_line[:80]

    return {
        "title": title,
        "content": full_text,
        "page_count": len(reader.pages),
        "format": "pdf",
    }
