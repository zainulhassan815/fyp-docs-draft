#!/bin/bash

# Change to project root directory
cd "$(dirname "$0")/.."

# Generate document from markdown
pandoc src/SRS_Document.md -o build/output.docx \
  --reference-doc=templates/custom-reference.docx \
  --lua-filter=scripts/docx-filter.lua \
  --toc --toc-depth=3

# Merge cover page and apply styles
python3 scripts/merge_cover.py

echo "Done: build/output.docx"
