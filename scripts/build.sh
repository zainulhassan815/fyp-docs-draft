#!/bin/bash

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

echo "Done: build/SRS_Document.docx"
