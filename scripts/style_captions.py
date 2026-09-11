#!/usr/bin/env python3
"""Style the table captions, and centre figures and captions.

Our table captions are written as plain paragraphs directly above each table, which is
where the department wants them. Pandoc styles them 'Body Text', which Word cannot
isolate for a List of Tables. This restyles every
paragraph that starts with 'Table N.N:' to 'Table Caption', so Word can build the list
from that style. Figure captions already use 'Image Caption', so they are left alone.

The figure paragraphs themselves are centred too. Pandoc leaves them unaligned, which
is invisible while a figure spans the full text width but puts a narrower one, such as
the methodology flowchart, hard against the left margin."""

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re
import sys

TABLE_CAPTION = re.compile(r"^Table \d+\.\d+:")


def style_captions(docx_path):
    doc = Document(docx_path)
    count = 0
    for p in doc.paragraphs:
        if TABLE_CAPTION.match(p.text.strip()):
            p.style = doc.styles["Table Caption"]
            count += 1

    # Centre the captions and the figures they belong to, at the style level.
    for style_name in ("Table Caption", "Image Caption", "Captioned Figure", "Figure"):
        try:
            doc.styles[style_name].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        except KeyError:
            pass

    doc.save(docx_path)
    print(f"Styled {count} table caption(s); captions and figures centred in {docx_path}")


def main():
    style_captions(sys.argv[1] if len(sys.argv) > 1 else "build/SRS_Document.docx")


if __name__ == "__main__":
    main()
