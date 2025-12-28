-- Lua filter for docx output

-- Handle \pagebreak (pandoc treats it as LaTeX)
function RawBlock(el)
  if el.format == "tex" and el.text:match("^\\pagebreak") then
    return pandoc.RawBlock('openxml', '<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
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
