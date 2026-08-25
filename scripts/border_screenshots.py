#!/usr/bin/env python3
"""Outline the UI screenshots so their white edges are visible against the page.

Which figures count as screenshots is read from the markdown (any image whose path
is under images/screenshots/), so adding one there needs no change here.  Diagrams
are left alone: they are line art and already read as bounded.
"""

import re
from docx import Document
from docx.oxml.ns import qn

SRC = 'src/SRS_Document.md'
DOC = 'build/SRS_Document.docx'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
BORDER_EMU = 6350  # 0.5 pt


def screenshot_figures(path):
    """{'4.10', '6.1', ...} for every markdown image under images/screenshots/."""
    md = open(path, encoding='utf-8').read()
    return {
        m.group(1)
        for m in re.finditer(r'!\[Figure ([\d.]+):[^\]]*\]\([^)]*images/screenshots/', md)
    }


def outline(paragraph):
    """Give every picture in the paragraph a thin black outline."""
    drawn = 0
    for spPr in paragraph._p.iter(qn('pic:spPr')):
        for ln in spPr.findall(qn('a:ln')):
            spPr.remove(ln)
        ln = spPr.makeelement(qn('a:ln'), {'w': str(BORDER_EMU)})
        fill = ln.makeelement(qn('a:solidFill'), {})
        clr = fill.makeelement(qn('a:srgbClr'), {'val': '000000'})
        fill.append(clr)
        ln.append(fill)
        spPr.append(ln)
        drawn += 1
    return drawn


def main():
    wanted = screenshot_figures(SRC)
    doc = Document(DOC)
    pending = None
    bordered = 0
    for para in doc.paragraphs:
        if para._p.find('.//' + qn('pic:pic')) is not None:
            pending = para
            continue
        caption = re.match(r'Figure ([\d.]+):', para.text.strip())
        if pending is not None and caption:
            if caption.group(1) in wanted:
                bordered += outline(pending)
            pending = None
    doc.save(DOC)
    print(f"Bordered {bordered} screenshot(s) of {len(wanted)} in {DOC}")


if __name__ == '__main__':
    main()
