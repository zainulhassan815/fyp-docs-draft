#!/usr/bin/env python3
"""Justify body-text paragraphs and set them to 1.5 line spacing.

The department's preset asks for 1.5 spacing, but applying it document-wide via
``docDefaults`` would stretch table cells, captions and code blocks as well.
Running prose is the target, and it is exactly the set this script already
selects, so both the alignment and the spacing are applied here.

Headings, captions, code blocks, list items, and table-cell paragraphs are left
untouched (table cells are never in Document.paragraphs; the other cases are excluded
by style name)."""

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
import sys

LINE_SPACING = 1.5

# Only genuine running-prose body styles are justified.
BODY_STYLES = {"Normal", "Body Text", "First Paragraph"}


def justify(docx_path):
    doc = Document(docx_path)
    count = 0
    for p in doc.paragraphs:
        name = p.style.name if p.style is not None else "Normal"
        # Only justify running prose that has no explicit alignment. This leaves the
        # cover's centred title block (CENTER) and pre-justified declaration untouched.
        if name in BODY_STYLES and p.alignment is None:
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = LINE_SPACING
            count += 1
    doc.save(docx_path)
    print(f"Justified {count} body paragraph(s) at {LINE_SPACING} spacing in {docx_path}")


def main():
    justify(sys.argv[1] if len(sys.argv) > 1 else "build/SRS_Document.docx")


if __name__ == "__main__":
    main()
