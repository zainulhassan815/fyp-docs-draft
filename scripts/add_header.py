#!/usr/bin/env python3
"""Put a running chapter-name header on the body pages only.

The front matter (title page, certificates, declaration, abstract, contents and
the three lists) must stay bare, so the document is split into two Word sections
at Chapter 1.  The split reuses the page-break paragraph pandoc already emits
there, so no blank page appears.

The body header is a STYLEREF field pointing at Heading 1, so each page shows
whichever chapter it belongs to.  Word and LibreOffice both resolve it live.
"""

import copy

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

DOC = 'build/SRS_Document.docx'
BODY_START = 'CHAPTER 1'
FIELD = 'STYLEREF "Heading 1" \\* MERGEFORMAT'


def text_of(para):
    return ''.join(node.text or '' for node in para.iter(qn('w:t')))


def split_at_body(doc):
    """Turn the page break before Chapter 1 into a next-page section break."""
    body = doc.element.body
    paras = body.findall(qn('w:p'))
    for i, para in enumerate(paras):
        if not text_of(para).strip().startswith(BODY_START):
            continue
        if i == 0:
            return False
        breaker = paras[i - 1]
        if breaker.find('.//' + qn('w:sectPr')) is not None:
            return False  # already split on an earlier run

        sect = copy.deepcopy(body.find(qn('w:sectPr')))
        kind = sect.find(qn('w:type'))
        if kind is None:
            kind = OxmlElement('w:type')
            sect.insert(0, kind)
        kind.set(qn('w:val'), 'nextPage')

        pPr = breaker.find(qn('w:pPr'))
        if pPr is None:
            pPr = OxmlElement('w:pPr')
            breaker.insert(0, pPr)
        pPr.append(sect)

        # the section break already starts a new page; drop the manual one
        for run in breaker.findall(qn('w:r')):
            if run.find(qn('w:br')) is not None:
                breaker.remove(run)
        return True
    raise SystemExit(f'ERROR: no paragraph starting with {BODY_START!r}')


def styleref(paragraph):
    run = paragraph.add_run()
    for kind, instr in (('begin', None), (None, FIELD), ('end', None)):
        if kind:
            node = OxmlElement('w:fldChar')
            node.set(qn('w:fldCharType'), kind)
        else:
            node = OxmlElement('w:instrText')
            node.set(qn('xml:space'), 'preserve')
            node.text = f' {instr} '
        run._r.append(node)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11)
    return run


def rule_below(paragraph):
    pPr = paragraph._p.get_or_add_pPr()
    borders = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    for key, value in (('val', 'single'), ('sz', '6'), ('space', '4'), ('color', '000000')):
        bottom.set(qn('w:' + key), value)
    borders.append(bottom)
    pPr.append(borders)


def main():
    doc = Document(DOC)
    split_at_body(doc)
    doc.save(DOC)

    doc = Document(DOC)
    if len(doc.sections) < 2:
        raise SystemExit('ERROR: section split did not take effect.')

    front, body = doc.sections[0], doc.sections[1]

    # front matter carries no header at all
    front.header.is_linked_to_previous = False
    for para in front.header.paragraphs:
        para.clear()

    body.header.is_linked_to_previous = False
    body.different_first_page_header_footer = False
    para = body.header.paragraphs[0] if body.header.paragraphs else body.header.add_paragraph()
    for run in list(para.runs):
        run._r.getparent().remove(run._r)
    para.text = ''
    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    styleref(para)
    rule_below(para)

    doc.save(DOC)
    print(f"Chapter-name header on the body section ({len(doc.sections)} sections) in {DOC}")


if __name__ == '__main__':
    main()
