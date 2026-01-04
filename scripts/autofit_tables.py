#!/usr/bin/env python3
"""Make all tables auto-fit to window width in a Word document."""

from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Twips
import sys


def set_table_autofit_window(table):
    """Set a table to auto-fit to window width."""
    tbl = table._tbl

    # Get or create tblPr element
    tblPr = tbl.tblPr
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tbl.insert(0, tblPr)

    # Remove existing width settings
    for child in tblPr.findall(qn('w:tblW')):
        tblPr.remove(child)

    # Set table width to 100% (5000 = 100% in fiftieths of a percent)
    tblW = OxmlElement('w:tblW')
    tblW.set(qn('w:w'), '5000')
    tblW.set(qn('w:type'), 'pct')
    tblPr.append(tblW)

    # Remove fixed layout if present, set to autofit
    for child in tblPr.findall(qn('w:tblLayout')):
        tblPr.remove(child)

    tblLayout = OxmlElement('w:tblLayout')
    tblLayout.set(qn('w:type'), 'autofit')
    tblPr.append(tblLayout)


def autofit_tables(docx_path, output_path=None):
    """Process all tables in a document to auto-fit to window."""
    if output_path is None:
        output_path = docx_path

    doc = Document(docx_path)
    table_count = len(doc.tables)

    for table in doc.tables:
        set_table_autofit_window(table)

    doc.save(output_path)
    print(f"Processed {table_count} table(s) in {docx_path}")


def main():
    if len(sys.argv) < 2:
        # Default: process the SRS document
        docx_path = 'build/SRS_Document.docx'
    else:
        docx_path = sys.argv[1]

    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    autofit_tables(docx_path, output_path)


if __name__ == '__main__':
    main()
