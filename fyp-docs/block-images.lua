-- Lua filter to make images block-level in docx output
function Para(para)
  if #para.content == 1 and para.content[1].t == "Image" then
    local img = para.content[1]
    return pandoc.Div({para}, pandoc.Attr("", {"figure"}))
  end
end
