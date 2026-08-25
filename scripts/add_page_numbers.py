#!/usr/bin/env python3
"""Put a right-aligned PAGE field in the footer of every section of the built report."""

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

DOC = 'build/SRS_Document.docx'


def page_field(paragraph):
    """Append a { PAGE } field so Word renders the live page number."""
    run = paragraph.add_run()
    for kind, text in (('begin', None), (None, 'PAGE'), ('end', None)):
        if kind:
            fld = OxmlElement('w:fldChar')
            fld.set(qn('w:fldCharType'), kind)
        else:
            fld = OxmlElement('w:instrText')
            fld.set(qn('xml:space'), 'preserve')
            fld.text = f' {text} '
        run._r.append(fld)


def main():
    doc = Document(DOC)
    for section in doc.sections:
        section.different_first_page_header_footer = False
        footer = section.footer
        footer.is_linked_to_previous = False
        para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        for run in list(para.runs):
            run._r.getparent().remove(run._r)
        para.text = ''
        para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        page_field(para)
    doc.save(DOC)


if __name__ == '__main__':
    main()
