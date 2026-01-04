-- Lua filter for docx output

-- Handle \pagebreak and \linebreak (pandoc treats them as LaTeX)
function RawBlock(el)
  if el.format == "tex" then
    if el.text:match("^\\pagebreak") then
      return pandoc.RawBlock('openxml', '<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
    elseif el.text:match("^\\linebreak") then
      -- Minimal line break: tiny font (1pt) + zero spacing to override styles
      return pandoc.RawBlock('openxml', '<w:p><w:pPr><w:spacing w:after="0" w:before="0" w:line="60" w:lineRule="exact"/><w:rPr><w:sz w:val="2"/><w:szCs w:val="2"/></w:rPr></w:pPr></w:p>')
    end
  end
end

-- Make standalone images block-level figures
function Para(para)
  if #para.content == 1 and para.content[1].t == "Image" then
    local img = para.content[1]
    return pandoc.Div({para}, pandoc.Attr("", {"figure"}))
  end
end

-- Make tables auto-fit to window width
function Table(tbl)
  if tbl.colspecs then
    for i, colspec in ipairs(tbl.colspecs) do
      tbl.colspecs[i] = {colspec[1], nil}
    end
  end
  return tbl
end
