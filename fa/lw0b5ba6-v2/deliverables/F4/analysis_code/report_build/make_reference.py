import zipfile, re, shutil
src = 'default-reference.docx'; dst = 'reference.docx'
zin = zipfile.ZipFile(src); zout = zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED)
for item in zin.infolist():
    data = zin.read(item.filename)
    if item.filename == 'word/styles.xml':
        s = data.decode()
        # default font + size
        s = s.replace('<w:rFonts w:asciiTheme="minorHAnsi" w:eastAsiaTheme="minorEastAsia" w:hAnsiTheme="minorHAnsi" w:cstheme="minorBidi" />\n        <w:sz w:val="24" />\n        <w:szCs w:val="24" />',
                      '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Calibri" />\n        <w:sz w:val="21" />\n        <w:szCs w:val="21" />')
        s = s.replace('<w:spacing w:after="200" />', '<w:spacing w:after="120" />', 1)
        s = s.replace('<w:spacing w:before="180" w:after="180" />', '<w:spacing w:before="80" w:after="100" w:line="264" w:lineRule="auto" />')
        # headings: explicit font, sizes, color
        def fix_heading(s, sid, size, before, after):
            i = s.find(f'w:styleId="{sid}"'); j = s.find('</w:style>', i); block = s[i:j]
            block = re.sub(r'<w:rFonts[^>]*/>', '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri" />', block, flags=re.S)
            block = re.sub(r'<w:color[^>]*/>', '<w:color w:val="1F3F6E" />', block, flags=re.S)
            block = re.sub(r'<w:sz w:val="\d+" />', f'<w:sz w:val="{size}" />', block); block = re.sub(r'<w:szCs w:val="\d+" />', f'<w:szCs w:val="{size}" />', block)
            block = re.sub(r'<w:spacing w:before="\d+" w:after="\d+" />', f'<w:spacing w:before="{before}" w:after="{after}" />', block)
            if '<w:b />' not in block: block = block.replace('<w:rPr>', '<w:rPr>\n      <w:b />', 1)
            return s[:i] + block + s[j:]
        s = fix_heading(s, 'Heading1', 32, 320, 100); s = fix_heading(s, 'Heading2', 25, 220, 80); s = fix_heading(s, 'Heading3', 22, 160, 60)
        for sid, size in [('Title', 40), ('TitleChar', 40)]:
            i = s.find(f'w:styleId="{sid}"'); j = s.find('</w:style>', i); block = s[i:j]
            block = re.sub(r'<w:rFonts[^>]*/>', '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri" />', block, flags=re.S)
            block = re.sub(r'<w:sz w:val="\d+" />', f'<w:sz w:val="{size}" />', block); block = re.sub(r'<w:szCs w:val="\d+" />', f'<w:szCs w:val="{size}" />', block)
            block = block.replace('<w:jc w:val="center" />', '<w:jc w:val="left" />')
            if sid == 'Title': block = block.replace('<w:rPr>', '<w:rPr>\n      <w:b />\n      <w:color w:val="1F3F6E" />', 1)
            s = s[:i] + block + s[j:]
        i = s.find('w:styleId="Subtitle"'); j = s.find('</w:style>', i); block = s[i:j]
        block = re.sub(r'<w:sz w:val="\d+" />', '<w:sz w:val="24" />', block); block = re.sub(r'<w:szCs w:val="\d+" />', '<w:szCs w:val="24" />', block)
        s = s[:i] + block + s[j:]
        # caption: smaller
        s = s.replace('<w:pPr>\n      <w:spacing w:before="0" w:after="120" />\n    </w:pPr>\n    <w:rPr>\n      <w:i />\n    </w:rPr>',
                      '<w:pPr>\n      <w:spacing w:before="40" w:after="160" />\n    </w:pPr>\n    <w:rPr>\n      <w:sz w:val="18" />\n      <w:szCs w:val="18" />\n    </w:rPr>')
        # table style: grid borders + header shading
        old = s[s.find('<w:style w:type="table" w:default="1" w:styleId="Table">'): s.find('</w:style>', s.find('w:styleId="Table"'))+len('</w:style>')]
        new = '''<w:style w:type="table" w:default="1" w:styleId="Table">
    <w:name w:val="Table" />
    <w:basedOn w:val="TableNormal" />
    <w:semiHidden />
    <w:unhideWhenUsed />
    <w:qFormat />
    <w:tblPr>
      <w:tblInd w:w="0" w:type="dxa" />
      <w:tblBorders>
        <w:top w:val="single" w:sz="4" w:space="0" w:color="A6A6A6" />
        <w:left w:val="single" w:sz="4" w:space="0" w:color="A6A6A6" />
        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="A6A6A6" />
        <w:right w:val="single" w:sz="4" w:space="0" w:color="A6A6A6" />
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="A6A6A6" />
        <w:insideV w:val="single" w:sz="4" w:space="0" w:color="A6A6A6" />
      </w:tblBorders>
      <w:tblCellMar>
        <w:top w:w="30" w:type="dxa" />
        <w:left w:w="70" w:type="dxa" />
        <w:bottom w:w="30" w:type="dxa" />
        <w:right w:w="70" w:type="dxa" />
      </w:tblCellMar>
    </w:tblPr>
    <w:tblStylePr w:type="firstRow">
      <w:rPr>
        <w:b />
      </w:rPr>
      <w:tcPr>
        <w:shd w:val="clear" w:color="auto" w:fill="DCE6F2" />
        <w:vAlign w:val="bottom"/>
      </w:tcPr>
    </w:tblStylePr>
  </w:style>
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
        assert old in s; s = s.replace(old, new)
        data = s.encode()
    if item.filename == 'word/document.xml':
        d = data.decode()
        d = d.replace('<w:sectPr>', '<w:sectPr>\n      <w:pgSz w:w="11906" w:h="16838" />\n      <w:pgMar w:top="1134" w:right="1077" w:bottom="1134" w:left="1077" w:header="567" w:footer="567" w:gutter="0" />')
        data = d.encode()
    zout.writestr(item, data)
zout.close(); print('reference.docx written')
