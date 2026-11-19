"""Builds the Word reference document (styles, A4 page, footer with page number) used by pandoc."""
import zipfile, subprocess, re, os, shutil
from paths import BUILD, PANDOC
OUT = BUILD + 'psln_reference.docx'
base = BUILD + 'default-reference.docx'
with open(base, 'wb') as f:
    f.write(subprocess.run([PANDOC, '--print-default-data-file', 'reference.docx'], capture_output=True, check=True).stdout)
zin = zipfile.ZipFile(base)
files = {n: zin.read(n) for n in zin.namelist()}
st = files['word/styles.xml'].decode('utf8')

# document defaults: Calibri 10.5 pt, tighter paragraph spacing
st = st.replace('<w:rFonts w:asciiTheme="minorHAnsi" w:eastAsiaTheme="minorEastAsia" w:hAnsiTheme="minorHAnsi" w:cstheme="minorBidi" />\n        <w:sz w:val="24" />\n        <w:szCs w:val="24" />',
                '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Calibri" />\n        <w:sz w:val="21" />\n        <w:szCs w:val="21" />')
assert 'w:val="21"' in st
st = st.replace('<w:pPrDefault>\n      <w:pPr>\n        <w:spacing w:after="200" />', '<w:pPrDefault>\n      <w:pPr>\n        <w:spacing w:after="120" w:line="264" w:lineRule="auto" />')

# table style: light borders, shaded bold header
old_tbl = st[st.index('<w:style w:type="table" w:default="1" w:styleId="Table">'):]
old_tbl = old_tbl[:old_tbl.index('</w:style>') + len('</w:style>')]
new_tbl = '''<w:style w:type="table" w:default="1" w:styleId="Table">
    <w:name w:val="Table" />
    <w:basedOn w:val="TableNormal" />
    <w:semiHidden />
    <w:unhideWhenUsed />
    <w:qFormat />
    <w:tblPr>
      <w:tblInd w:w="0" w:type="dxa" />
      <w:tblBorders>
        <w:top w:val="single" w:sz="6" w:space="0" w:color="7F7F7F" />
        <w:bottom w:val="single" w:sz="6" w:space="0" w:color="7F7F7F" />
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="BFBFBF" />
        <w:insideV w:val="single" w:sz="4" w:space="0" w:color="D9D9D9" />
      </w:tblBorders>
      <w:tblCellMar>
        <w:top w:w="40" w:type="dxa" />
        <w:left w:w="80" w:type="dxa" />
        <w:bottom w:w="40" w:type="dxa" />
        <w:right w:w="80" w:type="dxa" />
      </w:tblCellMar>
    </w:tblPr>
    <w:tblStylePr w:type="firstRow">
      <w:rPr>
        <w:b />
      </w:rPr>
      <w:tcPr>
        <w:tcBorders>
          <w:bottom w:val="single" w:sz="6" w:space="0" w:color="7F7F7F" />
        </w:tcBorders>
        <w:shd w:val="clear" w:color="auto" w:fill="E8EEF4" />
        <w:vAlign w:val="bottom" />
      </w:tcPr>
    </w:tblStylePr>
  </w:style>'''
st = st.replace(old_tbl, new_tbl)

# paragraph style for table cells (9 pt, tight); applied in post-processing
table_text = '''
  <w:style w:type="paragraph" w:customStyle="1" w:styleId="TableText">
    <w:name w:val="Table Text" />
    <w:basedOn w:val="Normal" />
    <w:qFormat />
    <w:pPr>
      <w:spacing w:before="20" w:after="20" w:line="240" w:lineRule="auto" />
    </w:pPr>
    <w:rPr>
      <w:sz w:val="17" />
      <w:szCs w:val="17" />
    </w:rPr>
  </w:style>'''
st = st.replace('</w:styles>', table_text + '\n</w:styles>')

# captions: 9 pt italic grey
def patch_style(st, sid, rpr_extra, ppr_extra=''):
    i = st.index(f'w:styleId="{sid}"'); j = st.index('</w:style>', i)
    block = st[i:j]
    if '<w:rPr>' in block:
        block2 = block.replace('<w:rPr>', '<w:rPr>' + rpr_extra, 1)
    else:
        block2 = block + '<w:rPr>' + rpr_extra + '</w:rPr>'
    return st[:i] + block2 + st[j:]
st = patch_style(st, 'Caption', '<w:sz w:val="18" /><w:szCs w:val="18" /><w:color w:val="404040" />')
# headings: dark blue-grey, sensible sizes
for sid, size in [('Heading1', 30), ('Heading2', 24), ('Heading3', 22)]:
    i = st.index(f'w:styleId="{sid}"'); j = st.index('</w:style>', i); block = st[i:j]
    block = re.sub(r'<w:sz w:val="\d+" />', f'<w:sz w:val="{size}" />', block); block = re.sub(r'<w:szCs w:val="\d+" />', f'<w:szCs w:val="{size}" />', block)
    block = re.sub(r'<w:color w:val="[0-9A-Fa-f]+"[^/]*/>', '<w:color w:val="1F3A5F" />', block)
    st = st[:i] + block + st[j:]

# title / body spacing
i = st.index('w:styleId="Title"'); j = st.index('</w:style>', i); block = st[i:j]
block = block.replace('<w:sz w:val="56" />', '<w:sz w:val="40" />').replace('<w:szCs w:val="56" />', '<w:szCs w:val="40" />').replace('<w:jc w:val="center" />', '<w:jc w:val="left" />')
block = block.replace('<w:rFonts w:asciiTheme="majorHAnsi"', '<w:b /><w:color w:val="1F3A5F" /><w:rFonts w:asciiTheme="majorHAnsi"') if '<w:color' not in block else block
st = st[:i] + block + st[j:]
i = st.index('w:styleId="BodyText"'); j = st.index('</w:style>', i); block = st[i:j]
block = block.replace('<w:spacing w:before="180" w:after="180" />', '<w:spacing w:before="60" w:after="110" />')
st = st[:i] + block + st[j:]
for sid in ('Subtitle', 'Date', 'Author'):
    i = st.index(f'w:styleId="{sid}"'); j = st.index('</w:style>', i); block = st[i:j]
    block = block.replace('<w:jc w:val="center" />', '<w:jc w:val="left" />')
    if '<w:rPr>' in block:
        block = block.replace('<w:rPr>', '<w:rPr><w:b w:val="0" /><w:color w:val="404040" />', 1)
    block = re.sub(r'<w:sz w:val="\d+" />', '<w:sz w:val="%d" />' % (24 if sid == 'Subtitle' else 20), block)
    block = re.sub(r'<w:szCs w:val="\d+" />', '<w:szCs w:val="%d" />' % (24 if sid == 'Subtitle' else 20), block)
    st = st[:i] + block + st[j:]
files['word/styles.xml'] = st.encode('utf8')

# footer with page number
footer = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><w:p><w:pPr><w:jc w:val="center" /></w:pPr><w:r><w:rPr><w:sz w:val="16" /><w:color w:val="595959" /></w:rPr><w:t xml:space="preserve">PSLN-344 portfolio proposal  |  1 November 2026  |  page </w:t></w:r><w:r><w:rPr><w:sz w:val="16" /><w:color w:val="595959" /></w:rPr><w:fldChar w:fldCharType="begin" /></w:r><w:r><w:rPr><w:sz w:val="16" /><w:color w:val="595959" /></w:rPr><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r><w:r><w:rPr><w:sz w:val="16" /><w:color w:val="595959" /></w:rPr><w:fldChar w:fldCharType="separate" /></w:r><w:r><w:rPr><w:sz w:val="16" /><w:color w:val="595959" /></w:rPr><w:t>1</w:t></w:r><w:r><w:rPr><w:sz w:val="16" /><w:color w:val="595959" /></w:rPr><w:fldChar w:fldCharType="end" /></w:r></w:p></w:ftr>'''
files['word/footer1.xml'] = footer.encode('utf8')
rels = files['word/_rels/document.xml.rels'].decode('utf8')
rels = rels.replace('</Relationships>', '<Relationship Id="rIdFooterPsln" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml" /></Relationships>')
files['word/_rels/document.xml.rels'] = rels.encode('utf8')
ct = files['[Content_Types].xml'].decode('utf8')
ct = ct.replace('</Types>', '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml" /></Types>')
files['[Content_Types].xml'] = ct.encode('utf8')
doc = files['word/document.xml'].decode('utf8')
assert 'xmlns:r=' in doc[:3000]
old_sect = doc[doc.rindex('<w:sectPr>'):doc.rindex('</w:sectPr>') + len('</w:sectPr>')]
new_sect = '''<w:sectPr>
      <w:footerReference w:type="default" r:id="rIdFooterPsln" />
      <w:footnotePr>
        <w:numRestart w:val="eachSect" />
      </w:footnotePr>
      <w:pgSz w:w="11906" w:h="16838" />
      <w:pgMar w:top="1134" w:right="1077" w:bottom="1134" w:left="1077" w:header="567" w:footer="567" w:gutter="0" />
    </w:sectPr>'''
doc = doc.replace(old_sect, new_sect)
files['word/document.xml'] = doc.encode('utf8')
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    # [Content_Types].xml first, as Word expects
    zout.writestr('[Content_Types].xml', files['[Content_Types].xml'])
    for n, b in files.items():
        if n != '[Content_Types].xml': zout.writestr(n, b)
# well-formedness check of every xml part
import xml.dom.minidom as md
for n, b in files.items():
    if n.endswith('.xml') or n.endswith('.rels'):
        md.parseString(b)
print('reference written:', OUT)
