"""Build a pandoc reference .docx (styles only): 10 pt body, compact tables with rules, narrower margins, smaller headings."""
import zipfile, re, shutil, subprocess, os, sys
src = sys.argv[1]; dst = sys.argv[2]
zin = zipfile.ZipFile(src); zout = zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED)
for item in zin.infolist():
    data = zin.read(item.filename)
    if item.filename == 'word/styles.xml':
        s = data.decode()
        s = s.replace('<w:sz w:val="24" />\n        <w:szCs w:val="24" />', '<w:sz w:val="20" />\n        <w:szCs w:val="20" />')
        s = s.replace('<w:spacing w:before="180" w:after="180" />', '<w:spacing w:before="80" w:after="100" />')
        for sid, old, new in [('Title', 56, 34), ('Heading1', 40, 28), ('Heading2', 32, 24), ('Heading3', 28, 21)]:
            m = re.search(r'(<w:style [^>]*w:styleId="%s".*?</w:style>)' % sid, s, re.S); blk = m.group(1)
            s = s.replace(blk, blk.replace(f'<w:sz w:val="{old}" />', f'<w:sz w:val="{new}" />').replace(f'<w:szCs w:val="{old}" />', f'<w:szCs w:val="{new}" />'))
        m = re.search(r'(<w:style [^>]*w:styleId="Title".*?</w:style>)', s, re.S); blk = m.group(1)
        s = s.replace(blk, blk.replace('<w:jc w:val="center" />', '<w:jc w:val="left" />'))
        # table style: borders, 8.5 pt text, shaded bold header row
        m = re.search(r'(<w:style w:type="table" w:default="1" w:styleId="Table">.*?</w:style>)', s, re.S); blk = m.group(1)
        new = blk.replace('<w:tblInd w:w="0" w:type="dxa" />', '''<w:tblInd w:w="0" w:type="dxa" />
      <w:tblBorders>
        <w:top w:val="single" w:sz="6" w:space="0" w:color="7F7F7F" />
        <w:bottom w:val="single" w:sz="6" w:space="0" w:color="7F7F7F" />
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="BFBFBF" />
        <w:insideV w:val="single" w:sz="4" w:space="0" w:color="E0E0E0" />
      </w:tblBorders>''')
        new = new.replace('<w:left w:w="108" w:type="dxa" />', '<w:left w:w="70" w:type="dxa" />').replace('<w:right w:w="108" w:type="dxa" />', '<w:right w:w="70" w:type="dxa" />')
        new = new.replace('</w:tblPr>', '</w:tblPr>\n    <w:rPr>\n      <w:sz w:val="17" />\n      <w:szCs w:val="17" />\n    </w:rPr>', 1)
        new = new.replace('''<w:tblStylePr w:type="firstRow">
      <w:tcPr>''', '''<w:tblStylePr w:type="firstRow">
      <w:rPr>
        <w:b />
      </w:rPr>
      <w:tcPr>
        <w:shd w:val="clear" w:color="auto" w:fill="EDF2F7" />''')
        assert new != blk
        s = s.replace(blk, new)
        data = s.encode()
    if item.filename == 'word/document.xml':
        d = data.decode()
        d = d.replace('<w:sectPr>', '<w:sectPr>\n      <w:pgSz w:w="12240" w:h="15840" />\n      <w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080" w:header="600" w:footer="600" w:gutter="0" />')
        data = d.encode()
    zout.writestr(item, data)
zout.close()
print('reference written', dst)
