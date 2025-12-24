#!/bin/bash

# Change to project root directory
cd "$(dirname "$0")/.."

pandoc src/SRS_Document.md -o build/output.docx \
  --reference-doc=templates/custom-reference.docx \
  --lua-filter=scripts/docx-filter.lua \
  --toc --toc-depth=3

python3 << 'EOF'
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docxcompose.composer import Composer
import zipfile
import os
import shutil

cover = Document('templates/cover.docx')
content = Document('build/output.docx')

# Add page break at end of cover
p = cover.add_paragraph()
run = p.add_run()
br = OxmlElement('w:br')
br.set(qn('w:type'), 'page')
run._r.append(br)

# Compose with cover as base (stable)
composer = Composer(cover)
composer.append(content)
composer.save('build/output.docx')

# Replace styles.xml with reference-doc styles
temp_dir = 'build/temp_docx'
with zipfile.ZipFile('templates/custom-reference.docx', 'r') as ref:
    styles_xml = ref.read('word/styles.xml')

with zipfile.ZipFile('build/output.docx', 'r') as z:
    z.extractall(temp_dir)

with open(os.path.join(temp_dir, 'word', 'styles.xml'), 'wb') as f:
    f.write(styles_xml)

os.remove('build/output.docx')
with zipfile.ZipFile('build/output.docx', 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            path = os.path.join(root, file)
            z.write(path, os.path.relpath(path, temp_dir))

shutil.rmtree(temp_dir)
EOF

echo "Done: build/output.docx"
