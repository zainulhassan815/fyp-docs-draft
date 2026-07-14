#!/bin/bash
# Build templates/custom-reference.docx (the pandoc reference doc) from the
# official SCET FYP report template.
#
# The reference doc must carry three things so the generated report is styled
# correctly and merge_cover.py's styles.xml swap leaves nothing undefined:
#   1. SCET template styles + page geometry (Normal = Times New Roman 12, headings,
#      Letter page, template margins).  -> pandoc, using the template as reference.
#   2. Pandoc's own required styles that the SCET template lacks (Compact,
#      FirstParagraph, Image/Table Caption, SourceCode, VerbatimChar, FootnoteText,
#      BlockText, Definition, Abstract, ...).  -> merged from pandoc's default doc.
#   3. The cover page's custom 'line' style (title-page separator).  -> merged from
#      templates/cover.docx.
#
# Usage: scripts/build-reference.sh [path-to-template.docx]
#   defaults to ~/Downloads/SCET_FYP_Report_Template_.docx

set -euo pipefail
cd "$(dirname "$0")/.."

TEMPLATE="${1:-$HOME/Downloads/SCET_FYP_Report_Template_.docx}"
OUT="templates/custom-reference.docx"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

if [ ! -f "$TEMPLATE" ]; then
  echo "ERROR: template not found: $TEMPLATE" >&2
  exit 1
fi

echo "Template: $TEMPLATE"

# Keep a copy of the template in the repo.
cp "$TEMPLATE" "templates/$(basename "$TEMPLATE")"

# 1. Sample markdown exercising every construct so pandoc emits all style hooks.
cat > "$TMP/sample.md" <<'MD'
---
title: Sample
subtitle: Sample
author: Sample
date: Sample
abstract: Sample abstract.
---
# H1
## H2
### H3
#### H4
##### H5
###### H6
Body paragraph with a [link](https://example.com) and `inline code`.

Second body paragraph.

- tight one
- tight two

- loose one.

- loose two.

1. num one
2. num two

> Block quote line one.
> Block quote line two.

```python
def sample():
    return "code"
```

Term
:   Definition.

![Figure caption.](nonexistent.png)

: Table caption.

| A | B |
|---|---|
| 1 | 2 |

Paragraph with a footnote.[^1]

[^1]: Footnote text.

---
End.
MD

# 2. Generate base reference doc from the template (SCET styles + geometry).
pandoc "$TMP/sample.md" -o "$OUT" --reference-doc="$TEMPLATE" 2>/dev/null || \
  pandoc "$TMP/sample.md" -o "$OUT" --reference-doc="$TEMPLATE"

# 3. Pandoc's default reference doc (source of the pandoc-only styles).
pandoc -o "$TMP/pandoc-default.docx" --print-default-data-file reference.docx

# 4. Merge missing pandoc styles + cover's 'line' style into the reference doc.
python3 - "$OUT" "$TMP/pandoc-default.docx" templates/cover.docx <<'PY'
import sys, re, zipfile, shutil, tempfile, os

out, pandoc_default, cover = sys.argv[1], sys.argv[2], sys.argv[3]

def styles_xml(path):
    with zipfile.ZipFile(path) as z:
        return z.read('word/styles.xml').decode('utf-8')

def blocks(xml):
    for b in re.findall(r'<w:style\b.*?</w:style>', xml, re.S):
        yield re.search(r'w:styleId="([^"]+)"', b).group(1), b

cur = styles_xml(out)
cur_ids = set(re.findall(r'w:styleId="([^"]+)"', cur))

inject = ''
added = []
# pandoc-only styles
for sid, blk in blocks(styles_xml(pandoc_default)):
    if sid not in cur_ids:
        inject += blk; cur_ids.add(sid); added.append(sid)
# cover 'line' style (any cover style still missing)
cover_xml = styles_xml(cover)
cover_doc = zipfile.ZipFile(cover).read('word/document.xml').decode('utf-8')
cover_used = set(re.findall(r'<w:(?:p|r|tbl)Style w:val="([^"]+)"', cover_doc))
for sid, blk in blocks(cover_xml):
    if sid in cover_used and sid not in cur_ids:
        inject += blk; cur_ids.add(sid); added.append(sid)

merged = cur.replace('</w:styles>', inject + '</w:styles>')

# Replace pandoc's borderless default `Table` style with a full-grid, shaded-header
# style so content tables render like the previous reference doc (full width, all
# borders) with a bold, lightly shaded header row.
TABLE_STYLE = (
    '<w:style w:type="table" w:default="1" w:styleId="Table">'
    '<w:name w:val="Table"/><w:basedOn w:val="TableNormal"/><w:uiPriority w:val="59"/>'
    '<w:tblPr><w:tblInd w:w="0" w:type="dxa"/>'
    '<w:tblBorders>'
    '<w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '</w:tblBorders>'
    '<w:tblCellMar>'
    '<w:top w:w="40" w:type="dxa"/><w:left w:w="108" w:type="dxa"/>'
    '<w:bottom w:w="40" w:type="dxa"/><w:right w:w="108" w:type="dxa"/>'
    '</w:tblCellMar></w:tblPr>'
    '<w:tblStylePr w:type="firstRow"><w:rPr><w:b/><w:bCs/></w:rPr>'
    '<w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="D9D9D9"/></w:tcPr></w:tblStylePr>'
    '</w:style>'
)
merged = re.sub(
    r'<w:style w:type="table" w:default="1" w:styleId="Table">.*?</w:style>',
    TABLE_STYLE, merged, count=1, flags=re.S,
)

tmp = tempfile.mktemp(suffix='.docx')
with zipfile.ZipFile(out) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
    for it in zin.infolist():
        data = zin.read(it.filename)
        if it.filename == 'word/styles.xml':
            data = merged.encode('utf-8')
        zout.writestr(it, data)
shutil.move(tmp, out)
print("  merged styles:", ', '.join(added))
PY

# 5. Report result.
python3 - "$OUT" <<'PY'
import sys, re, zipfile
z = zipfile.ZipFile(sys.argv[1])
ids = set(re.findall(r'w:styleId="([^"]+)"', z.read('word/styles.xml').decode()))
doc = z.read('word/document.xml').decode()
normal = re.search(r'styleId="Normal".*?</w:style>', z.read('word/styles.xml').decode(), re.S).group(0)
font = re.search(r'w:ascii="([^"]+)"', normal)
pg = re.search(r'<w:pgSz[^>]*/>', doc)
print(f"Built {sys.argv[1]}: {len(ids)} styles | Normal={font.group(1) if font else '?'} | {pg.group(0) if pg else ''}")
PY

echo "Done."
