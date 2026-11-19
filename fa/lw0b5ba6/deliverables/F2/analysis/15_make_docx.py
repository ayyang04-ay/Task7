#!/usr/bin/env python
"""Step 15 - build a styled reference.docx, then convert report_src/proposal.html to DOCX with pandoc."""
import zipfile, re, os, shutil, subprocess, sys
SRC = "/tmp/outputs/analysis/report_src"; REF0 = f"{SRC}/reference_default.docx"; REF = f"{SRC}/reference.docx"
PANDOC = ["micromamba", "run", "-n", "genomics", "pandoc"]
subprocess.run(PANDOC + ["-o", REF0, "--print-default-data-file", "reference.docx"], check=True)
z = zipfile.ZipFile(REF0); files = {i.filename: z.read(i.filename) for i in z.infolist()}; z.close()
st = files["word/styles.xml"].decode("utf8")

def replace_style(xml, style_id, new_block):
    pat = re.compile(r'<w:style\b[^>]*w:styleId="%s"[^>]*>.*?</w:style>' % re.escape(style_id), re.S)
    assert pat.search(xml), style_id
    return pat.sub(lambda m_: new_block, xml, count=1)

FONT = '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Calibri" />'
# document defaults: Calibri 10.5 pt
st = re.sub(r"<w:rPrDefault>.*?</w:rPrDefault>", f'<w:rPrDefault><w:rPr>{FONT}<w:sz w:val="21" /><w:szCs w:val="21" /><w:lang w:val="en-GB" w:eastAsia="en-US" w:bidi="ar-SA" /></w:rPr></w:rPrDefault>', st, flags=re.S)
st = re.sub(r"<w:pPrDefault>.*?</w:pPrDefault>", '<w:pPrDefault><w:pPr><w:spacing w:after="100" w:line="259" w:lineRule="auto" /></w:pPr></w:pPrDefault>', st, flags=re.S)
st = replace_style(st, "BodyText", '<w:style w:type="paragraph" w:styleId="BodyText"><w:name w:val="Body Text" /><w:basedOn w:val="Normal" /><w:link w:val="BodyTextChar" /><w:qFormat /><w:pPr><w:spacing w:before="60" w:after="100" /></w:pPr></w:style>')
st = replace_style(st, "Compact", '<w:style w:type="paragraph" w:customStyle="1" w:styleId="Compact"><w:name w:val="Compact" /><w:basedOn w:val="BodyText" /><w:qFormat /><w:pPr><w:spacing w:before="20" w:after="20" /></w:pPr></w:style>')
st = replace_style(st, "Title", f'<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title" /><w:basedOn w:val="Normal" /><w:next w:val="BodyText" /><w:link w:val="TitleChar" /><w:qFormat /><w:pPr><w:keepNext /><w:spacing w:before="0" w:after="120" /><w:jc w:val="left" /></w:pPr><w:rPr>{FONT}<w:b /><w:color w:val="0B3954" /><w:sz w:val="40" /><w:szCs w:val="40" /></w:rPr></w:style>')
def heading(n, size, color, before, after):
    return (f'<w:style w:type="paragraph" w:styleId="Heading{n}"><w:name w:val="heading {n}" /><w:basedOn w:val="Normal" /><w:next w:val="BodyText" /><w:link w:val="Heading{n}Char" /><w:uiPriority w:val="9" /><w:qFormat />'
            f'<w:pPr><w:keepNext /><w:keepLines /><w:spacing w:before="{before}" w:after="{after}" /><w:outlineLvl w:val="{n-1}" /></w:pPr><w:rPr>{FONT}<w:b /><w:color w:val="{color}" /><w:sz w:val="{size}" /><w:szCs w:val="{size}" /></w:rPr></w:style>')
st = replace_style(st, "Heading1", heading(1, 30, "0B3954", 320, 100)); st = replace_style(st, "Heading2", heading(2, 24, "0B3954", 220, 80)); st = replace_style(st, "Heading3", heading(3, 22, "333333", 160, 60))
BORD = "".join(f'<w:{s} w:val="single" w:sz="4" w:space="0" w:color="9AA5B1" />' for s in ["top", "left", "bottom", "right", "insideH", "insideV"])
st = replace_style(st, "Table", '<w:style w:type="table" w:default="1" w:styleId="Table"><w:name w:val="Table" /><w:basedOn w:val="TableNormal" /><w:semiHidden /><w:unhideWhenUsed /><w:qFormat />'
    '<w:rPr><w:sz w:val="17" /><w:szCs w:val="17" /></w:rPr>'
    f'<w:tblPr><w:tblInd w:w="0" w:type="dxa" /><w:tblBorders>{BORD}</w:tblBorders><w:tblCellMar><w:top w:w="40" w:type="dxa" /><w:left w:w="85" w:type="dxa" /><w:bottom w:w="40" w:type="dxa" /><w:right w:w="85" w:type="dxa" /></w:tblCellMar></w:tblPr>'
    '<w:tblStylePr w:type="firstRow"><w:rPr><w:b /><w:color w:val="FFFFFF" /></w:rPr><w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="0B3954" /><w:vAlign w:val="center" /></w:tcPr></w:tblStylePr></w:style>')
for sid, nm in [("ImageCaption", "Image Caption"), ("TableCaption", "Table Caption")]:
    st = replace_style(st, sid, f'<w:style w:type="paragraph" w:customStyle="1" w:styleId="{sid}"><w:name w:val="{nm}" /><w:basedOn w:val="Normal" /><w:pPr><w:spacing w:before="40" w:after="160" /></w:pPr><w:rPr><w:i /><w:color w:val="333333" /><w:sz w:val="18" /><w:szCs w:val="18" /></w:rPr></w:style>')
files["word/styles.xml"] = st.encode("utf8")

# page setup (A4, 1.9 cm margins) + centred page-number footer
footer = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:p><w:pPr><w:jc w:val="center" /></w:pPr>'
          '<w:r><w:rPr><w:sz w:val="16" /><w:color w:val="666666" /></w:rPr><w:t xml:space="preserve">PSLN-344 portfolio proposal · page </w:t></w:r>'
          '<w:r><w:rPr><w:sz w:val="16" /><w:color w:val="666666" /></w:rPr><w:fldChar w:fldCharType="begin" /></w:r><w:r><w:rPr><w:sz w:val="16" /><w:color w:val="666666" /></w:rPr><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
          '<w:r><w:rPr><w:sz w:val="16" /><w:color w:val="666666" /></w:rPr><w:fldChar w:fldCharType="separate" /></w:r><w:r><w:rPr><w:sz w:val="16" /><w:color w:val="666666" /></w:rPr><w:t>1</w:t></w:r>'
          '<w:r><w:rPr><w:sz w:val="16" /><w:color w:val="666666" /></w:rPr><w:fldChar w:fldCharType="end" /></w:r></w:p></w:ftr>')
files["word/footer1.xml"] = footer.encode("utf8")
rels = files["word/_rels/document.xml.rels"].decode("utf8")
rels = rels.replace("</Relationships>", '<Relationship Id="rIdFooterPSLN" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml" /></Relationships>')
files["word/_rels/document.xml.rels"] = rels.encode("utf8")
ct = files["[Content_Types].xml"].decode("utf8")
ct = ct.replace("</Types>", '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml" /></Types>')
files["[Content_Types].xml"] = ct.encode("utf8")
docx = files["word/document.xml"].decode("utf8")
if "xmlns:r=" not in docx.split(">", 2)[1] and "xmlns:r=" not in docx[:2000]:
    docx = docx.replace("<w:document ", '<w:document xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ', 1)
docx = re.sub(r"<w:sectPr\b.*?</w:sectPr>", '<w:sectPr><w:footerReference w:type="default" r:id="rIdFooterPSLN" /><w:pgSz w:w="11906" w:h="16838" /><w:pgMar w:top="1077" w:right="1077" w:bottom="1077" w:left="1077" w:header="510" w:footer="510" w:gutter="0" /></w:sectPr>', docx, flags=re.S)
files["word/document.xml"] = docx.encode("utf8")
with zipfile.ZipFile(REF, "w", zipfile.ZIP_DEFLATED) as zo:
    for k, v in files.items(): zo.writestr(k, v)

open(f"{SRC}/pagebreak.lua", "w").write('''
function Div(el)
  if el.classes:includes("pagebreak") then
    return pandoc.RawBlock("openxml", '<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
  end
end
''')
OUT = "/tmp/outputs/PSLN-344_portfolio_proposal.docx"
cmd = PANDOC + [f"{SRC}/proposal.html", "-f", "html", "-t", "docx", "-o", OUT, f"--reference-doc={REF}", f"--lua-filter={SRC}/pagebreak.lua",
                "--resource-path=/tmp/outputs/figures:/tmp/outputs"]
r = subprocess.run(cmd, capture_output=True, text=True); print(r.stdout, r.stderr)
# ---- post-process: give every table explicit column widths that sum to the text width (A4 minus margins)
TEXTW = 11906 - 2 * 1077
zin = zipfile.ZipFile(OUT); parts = {i.filename: zin.read(i.filename) for i in zin.infolist()}; zin.close()
dx = parts["word/document.xml"].decode("utf8")
def fix_table(mt):
    t = mt.group(0)
    cols = [int(x) for x in re.findall(r'<w:gridCol w:w="(\d+)"', t)]
    if not cols: return t
    sc = TEXTW / sum(cols); new = [int(round(c * sc)) for c in cols]; new[-1] += TEXTW - sum(new)
    grid = "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{c}" />' for c in new) + "</w:tblGrid>"
    t = re.sub(r"<w:tblGrid>.*?</w:tblGrid>", grid, t, count=1, flags=re.S)
    t = t.replace('<w:tblW w:type="pct" w:w="5000" />', f'<w:tblW w:type="dxa" w:w="{TEXTW}" />')
    def fix_row(mr):
        r_ = mr.group(0); k = [0]
        def fix_cell(mc):
            i = k[0]; k[0] += 1
            return f'<w:tcPr><w:tcW w:w="{new[i] if i < len(new) else new[-1]}" w:type="dxa" /></w:tcPr>'
        return re.sub(r"<w:tcPr />|<w:tcPr></w:tcPr>", fix_cell, r_)
    return re.sub(r"<w:tr>.*?</w:tr>", fix_row, t, flags=re.S)
dx2 = re.sub(r"<w:tbl>.*?</w:tbl>", fix_table, dx, flags=re.S)
parts["word/document.xml"] = dx2.encode("utf8")
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zo:
    for k_, v_ in parts.items(): zo.writestr(k_, v_)
os.remove(REF0)
print("written", OUT, os.path.getsize(OUT), "bytes")
