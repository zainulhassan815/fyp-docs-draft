#!/usr/bin/env python3
"""Bake real entries into the TOC, List of Figures, and List of Tables.

Those three are Word fields.  Word populates them on open, but an unlicensed
Word (or LibreOffice, which cannot build a style-based TOC from an imported
field at all) leaves them showing an empty placeholder.  So we compute the
entries ourselves and write them into each field's *cached result*: viewers
render the cache directly, and Word can still refresh the field later.

Page numbers come from a LibreOffice render of the document, which is also
what produces the PDF, so the numbers match what the reader sees.  Filling the
lists changes pagination, so render and fill repeat until the numbers settle.
"""

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from docx import Document
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
from pypdf import PdfReader

DOCX = Path('build/SRS_Document.docx')
SOFFICE = '/Applications/LibreOffice.app/Contents/MacOS/soffice'
MAX_PASSES = 5
W = nsdecls('w')

# right-aligned, dot-leader tab at the right margin
TAB_POS = 8640
INDENT = {1: 0, 2: 220, 3: 440}


def render_pages(docx):
    """Return the extracted text of each page, as LibreOffice lays the file out."""
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            [SOFFICE, '--headless', '--norestore', '--convert-to', 'pdf',
             '--outdir', tmp, str(docx)],
            check=True, capture_output=True, timeout=600,
        )
        pdf = next(Path(tmp).glob('*.pdf'))
        return [(p.extract_text() or '') for p in PdfReader(str(pdf)).pages]


def squash(text):
    return re.sub(r'\s+', '', text)


def collect(doc):
    """(toc, figures, tables) entries as (text, level) in document order."""
    toc, figs, tbls = [], [], []
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        style = para.style.name
        if style.startswith('Heading') and style[-1].isdigit() and int(style[-1]) <= 3:
            toc.append((text, int(style[-1])))
        elif style == 'Image Caption':
            figs.append((text, 1))
        elif style == 'Table Caption':
            tbls.append((text, 1))
    return toc, figs, tbls


def list_pages(pages):
    """Page indexes occupied by the three generated lists, which must not be
    searched: once filled they contain every entry's text themselves."""
    starts = {}
    for name in ('Table of Contents', 'List of Figures', 'List of Tables'):
        key = squash(name)
        for i, text in enumerate(pages):
            # the footer page number extracts first, so the heading sits just
            # after it rather than at offset zero
            if key in squash(text)[:60]:
                starts[name] = i
                break
    if len(starts) < 3:
        sys.exit('ERROR: could not locate all three list sections in the render.')
    first, last = min(starts.values()), max(starts.values())
    # the Table of Contents can run past one page; everything from the first
    # list heading to the last one belongs to the front-matter lists
    return set(range(first, last + 1)), last


def locate(entries, pages, skip):
    """Map each entry to the 1-based page it appears on."""
    numbers = []
    for text, _level in entries:
        needle = squash(text)
        found = None
        for i, page in enumerate(pages):
            if i in skip:
                continue
            if needle in squash(page):
                found = i + 1
                break
        numbers.append(found)
    return numbers


def entry_paragraph(text, level, page, style):
    body = (
        f'<w:pPr><w:pStyle w:val="{style}"/>'
        f'<w:ind w:left="{INDENT.get(level, 0)}"/>'
        f'<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="{TAB_POS}"/></w:tabs>'
        f'</w:pPr>'
        f'<w:r><w:t xml:space="preserve">{escape(text)}</w:t></w:r>'
        f'<w:r><w:tab/><w:t>{page}</w:t></w:r>'
    )
    return parse_xml(f'<w:p {W}>{body}</w:p>')


def escape(text):
    return (text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def field_region(body, instr_prefix):
    """Paragraphs spanning one TOC field, from its 'begin' to its 'end'."""
    paras = body.findall('.//' + qn('w:p'))
    for i, para in enumerate(paras):
        instr = para.findall('.//' + qn('w:instrText'))
        if not instr or not (instr[0].text or '').strip().startswith(instr_prefix):
            continue
        region = [para]
        if para.findall('.//' + qn('w:fldChar')+'[@'+qn('w:fldCharType')+'="end"]'):
            return region
        for nxt in paras[i + 1:]:
            region.append(nxt)
            for fld in nxt.findall('.//' + qn('w:fldChar')):
                if fld.get(qn('w:fldCharType')) == 'end':
                    return region
        return region
    return None


def fill(doc, instr, entries, numbers, style):
    """Replace one field's cached result with the real entries."""
    region = field_region(doc.element.body, instr)
    if region is None:
        sys.exit(f'ERROR: field not found: {instr}')

    new = [
        entry_paragraph(text, level, page or '?', style)
        for (text, level), page in zip(entries, numbers)
    ]
    if not new:
        return 0

    # wrap the entries in the field so Word can still refresh them
    opener = parse_xml(
        f'<w:r {W}><w:fldChar w:fldCharType="begin"/>'
        f'<w:instrText xml:space="preserve"> {escape(instr)} </w:instrText>'
        f'<w:fldChar w:fldCharType="separate"/></w:r>'
    )
    closer = parse_xml(f'<w:r {W}><w:fldChar w:fldCharType="end"/></w:r>')
    new[0].insert(len(new[0].findall(qn('w:pPr'))), opener)
    new[-1].append(closer)

    anchor = region[0]
    for para in new:
        anchor.addprevious(para)
    for para in region:
        para.getparent().remove(para)
    return len(new)


FIELDS = [
    ('TOC \\o "1-3" \\h \\z \\u', 'toc', 'toc 1'),
    ('TOC \\h \\z \\t "Image Caption,1"', 'figs', 'toc 1'),
    ('TOC \\h \\z \\t "Table Caption,1"', 'tbls', 'toc 1'),
]


def main():
    previous = None
    for attempt in range(1, MAX_PASSES + 1):
        pages = render_pages(DOCX)
        doc = Document(str(DOCX))
        toc, figs, tbls = collect(doc)
        skip, _ = list_pages(pages)
        found = {
            'toc': locate(toc, pages, skip),
            'figs': locate(figs, pages, skip),
            'tbls': locate(tbls, pages, skip),
        }
        if found == previous:
            print(f"Lists stable after {attempt - 1} pass(es): "
                  f"{len(toc)} TOC, {len(figs)} figure, {len(tbls)} table entries")
            missing = [k for k, v in found.items() if None in v]
            if missing:
                print(f"  WARNING: unresolved page numbers in {missing}")
            return
        entries = {'toc': toc, 'figs': figs, 'tbls': tbls}
        for instr, key, style in FIELDS:
            fill(doc, instr, entries[key], found[key], style)
        doc.save(str(DOCX))
        previous = found
        print(f"  pass {attempt}: {len(toc)}/{len(figs)}/{len(tbls)} entries placed")
    print(f"WARNING: page numbers still shifting after {MAX_PASSES} passes.")


if __name__ == '__main__':
    if not shutil.which(SOFFICE) and not Path(SOFFICE).exists():
        sys.exit(f'ERROR: LibreOffice not found at {SOFFICE}')
    main()
