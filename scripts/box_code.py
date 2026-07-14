#!/usr/bin/env python3
"""Give fenced code blocks a bordered box (and subtle shading).

Pandoc renders each code block as a single paragraph in the ``Source Code``
style. Adding paragraph borders + light shading to that style draws a clean
box around every code snippet. Runs on build/SRS_Document.docx after the
reference styles have been merged in.
"""

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

DOCX = "build/SRS_Document.docx"
BORDER_COLOR = "808080"   # medium grey box
FILL = "F5F5F5"           # very light grey background
BORDER_SZ = "8"           # eighths of a point -> 1pt
BORDER_SPACE = "6"        # padding between text and border (points)


def _edge(tag: str) -> OxmlElement:
    e = OxmlElement(tag)
    e.set(qn("w:val"), "single")
    e.set(qn("w:sz"), BORDER_SZ)
    e.set(qn("w:space"), BORDER_SPACE)
    e.set(qn("w:color"), BORDER_COLOR)
    return e


def main() -> None:
    doc = Document(DOCX)
    styles = doc.styles.element

    target = None
    for style in styles.findall(qn("w:style")):
        if style.get(qn("w:styleId")) == "SourceCode":
            target = style
            break
    if target is None:
        print("SourceCode style not found; nothing to box.")
        return

    pPr = target.find(qn("w:pPr"))
    if pPr is None:
        pPr = OxmlElement("w:pPr")
        target.append(pPr)

    # Drop any prior border/shading so re-runs are idempotent.
    for tag in ("w:pBdr", "w:shd"):
        existing = pPr.find(qn(tag))
        if existing is not None:
            pPr.remove(existing)

    pBdr = OxmlElement("w:pBdr")
    for edge in ("top", "left", "bottom", "right"):
        pBdr.append(_edge("w:" + edge))

    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), FILL)

    # pBdr and shd must precede wordWrap in CT_PPr child order.
    pPr.insert(0, shd)
    pPr.insert(0, pBdr)

    doc.save(DOCX)
    print(f"Boxed code blocks via 'Source Code' style in {DOCX}")


if __name__ == "__main__":
    main()
