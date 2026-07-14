#!/usr/bin/env python3
"""Insert an auto-generating List of Figures and List of Tables.

Right after the main Table of Contents, drop in two Word field-based lists:
  - List of Figures  -> TOC field built from the 'Image Caption' style
  - List of Tables   -> TOC field built from the 'Table Caption' style

The fields are marked dirty and ``updateFields`` is enabled, so Word (re)builds
all three lists when the document is opened. Runs on build/SRS_Document.docx
after the cover/TOC have been composed in.
"""

from docx import Document
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCX = "build/SRS_Document.docx"

W = nsdecls("w")


def _page_break():
    return parse_xml(f'<w:p {W}><w:r><w:br w:type="page"/></w:r></w:p>')


def _heading(text):
    return parse_xml(
        f'<w:p {W}><w:pPr><w:pStyle w:val="TOCHeading"/></w:pPr>'
        f"<w:r><w:t>{text}</w:t></w:r></w:p>"
    )


def _toc_field(instr, placeholder):
    return parse_xml(
        f"<w:p {W}>"
        f'<w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
        f'<w:r><w:instrText xml:space="preserve"> {instr} </w:instrText></w:r>'
        f'<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
        f"<w:r><w:t>{placeholder}</w:t></w:r>"
        f'<w:r><w:fldChar w:fldCharType="end"/></w:r>'
        f"</w:p>"
    )


def _find_toc_sdt(body):
    for child in body:
        if child.tag == qn("w:sdt"):
            gallery = child.find(".//" + qn("w:docPartGallery"))
            if gallery is not None and gallery.get(qn("w:val")) == "Table of Contents":
                return child
    return None


def main():
    doc = Document(DOCX)
    body = doc.element.body

    # Idempotency guard.
    if any("List of Figures" in p.text for p in doc.paragraphs):
        print("Lists already present; skipping insert.")
        return

    toc_sdt = _find_toc_sdt(body)
    if toc_sdt is None:
        print("Main TOC not found; cannot place lists.")
        return

    blocks = [
        _page_break(),
        _heading("List of Figures"),
        _toc_field(
            'TOC \\h \\z \\t "Image Caption,1"',
            'Right-click and choose "Update Field" to build the List of Figures.',
        ),
        _page_break(),
        _heading("List of Tables"),
        _toc_field(
            'TOC \\h \\z \\t "Table Caption,1"',
            'Right-click and choose "Update Field" to build the List of Tables.',
        ),
    ]

    anchor = toc_sdt
    for elem in blocks:
        anchor.addnext(elem)
        anchor = elem

    # Ask Word to refresh all fields (TOC + both lists) on open.
    settings = doc.settings.element
    if settings.find(qn("w:updateFields")) is None:
        uf = OxmlElement("w:updateFields")
        uf.set(qn("w:val"), "true")
        settings.insert(0, uf)

    doc.save(DOCX)
    print(f"Inserted List of Figures + List of Tables in {DOCX}")


if __name__ == "__main__":
    main()
