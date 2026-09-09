#!/bin/bash
# Stop at the first failing step.  Without this a missing Python dependency
# (docxcompose, say) lets merge_cover.py die quietly and the build still
# reports success, having silently dropped the whole cover and front matter.
set -euo pipefail

# Change to project root directory
cd "$(dirname "$0")/.."

# Generate document from markdown
pandoc src/SRS_Document.md -o build/SRS_Document.docx \
  --reference-doc=templates/custom-reference.docx \
  --lua-filter=scripts/docx-filter.lua \
  --toc --toc-depth=3

# Merge cover page and apply styles
python3 scripts/merge_cover.py

# Auto-fit all tables to window width
python3 scripts/autofit_tables.py

# Give below-table caption paragraphs the 'Table Caption' style (for List of Tables)
python3 scripts/style_captions.py

# Justify body-text paragraphs (leaves headings, code, captions, tables alone)
python3 scripts/justify_paragraphs.py

# Draw a bordered box around fenced code blocks
python3 scripts/box_code.py

# Insert auto-generating List of Figures and List of Tables after the TOC
python3 scripts/add_lists.py

# Outline the UI screenshots so their white edges are visible
python3 scripts/border_screenshots.py

# Split off the front matter and give body pages a running chapter-name header
python3 scripts/add_header.py

# Right-aligned page number in the footer of every section
python3 scripts/add_page_numbers.py

# Bake real entries + page numbers into the TOC and the two lists, so they
# display without needing Word to refresh the fields (renders via LibreOffice,
# repeating until the page numbers settle)
python3 scripts/fill_lists.py

echo "Done: build/SRS_Document.docx"
