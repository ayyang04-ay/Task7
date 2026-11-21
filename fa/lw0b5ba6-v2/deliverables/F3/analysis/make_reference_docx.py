"""make_reference_docx.py - derive a Word style template from pandoc's default reference.docx
(fonts, heading sizes, bordered tables with shaded header row, compact 9-pt table text, 1-inch margins)."""
import zipfile, re, shutil, sys
SRC = '/tmp/work/docx/ref_default.docx'; DST = '/tmp/work/docx/reference.docx'
zin = zipfile.ZipFile(SRC); zout = zipfile.ZipFile(DST, 'w', zipfile.ZIP_DEFLATED)
for item in zin.infolist():
    data = zin.read(item.filename)
    if item.filename == 'word/styles.xml':
        s = data.decode()
        # base font and size
        s = s.replace('<w:rFonts w:asciiTheme="minorHAnsi" w:eastAsiaTheme="minorEastAsia" w:hAnsiTheme="minorHAnsi" w:cstheme="minorBidi" />\n        <w:sz w:val="24" />\n        <w:szCs w:val="24" />',
                      '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Calibri" />\n        <w:sz w:val="21" />\n        <w:szCs w:val="21" />')
        assert 'w:ascii="Calibri"' in s
        s = s.replace('<w:spacing w:after="200" />', '<w:spacing w:after="120" />', 1)
        s = s.replace('<w:spacing w:before="180" w:after="180" />', '<w:spacing w:before="80" w:after="110" />', 1)      # BodyText
        # Compact (used inside tables and tight lists): 9 pt
        s = s.replace('<w:pPr>\n      <w:spacing w:before="36" w:after="36" />\n    </w:pPr>', '<w:pPr>\n      <w:spacing w:before="20" w:after="20" />\n    </w:pPr>\n    <w:rPr>\n      <w:sz w:val="18" />\n      <w:szCs w:val="18" />\n    </w:rPr>', 1)
        assert '<w:sz w:val="18" />' in s
        # headings: fonts and sizes
        def restyle(s, sid, size, color, before, after, extra_ppr=None):
            m = re.search(r'(<w:style w:type="paragraph" w:styleId="%s">.*?</w:style>)' % sid, s, flags=re.S)
            blk = m.group(1)
            rpr = (f'<w:rPr>\n      <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri" />\n      <w:b />\n      <w:bCs />\n      <w:color w:val="{color}" />\n'
                   f'      <w:sz w:val="{size}" />\n      <w:szCs w:val="{size}" />\n    </w:rPr>')
            new = re.sub(r'<w:rPr>.*?</w:rPr>', rpr, blk, flags=re.S)
            new = re.sub(r'<w:spacing w:before="\d+" w:after="\d+" />', f'<w:spacing w:before="{before}" w:after="{after}" />', new)
            if extra_ppr:
                for a, b in extra_ppr: new = new.replace(a, b)
            return s.replace(blk, new)
        s = restyle(s, 'Heading1', 30, '17365D', 300, 100)
        s = restyle(s, 'Heading2', 24, '17365D', 220, 80)
        s = restyle(s, 'Heading3', 21, '1F1F1F', 160, 60)
        s = restyle(s, 'Title', 40, '17365D', 0, 80, extra_ppr=[('<w:jc w:val="center" />', '<w:jc w:val="left" />')])
        # table style
        m = re.search(r'(<w:style w:type="table" w:default="1" w:styleId="Table">.*?</w:style>)', s, flags=re.S)
        table = '''<w:style w:type="table" w:default="1" w:styleId="Table">
    <w:name w:val="Table" />
    <w:basedOn w:val="TableNormal" />
    <w:semiHidden />
    <w:unhideWhenUsed />
    <w:qFormat />
    <w:tblPr>
      <w:tblInd w:w="0" w:type="dxa" />
      <w:tblBorders>
        <w:top w:val="single" w:sz="6" w:space="0" w:color="7F7F7F" />
        <w:left w:val="single" w:sz="4" w:space="0" w:color="BFBFBF" />
        <w:bottom w:val="single" w:sz="6" w:space="0" w:color="7F7F7F" />
        <w:right w:val="single" w:sz="4" w:space="0" w:color="BFBFBF" />
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="BFBFBF" />
        <w:insideV w:val="single" w:sz="4" w:space="0" w:color="BFBFBF" />
      </w:tblBorders>
      <w:tblCellMar>
        <w:top w:w="45" w:type="dxa" />
        <w:left w:w="85" w:type="dxa" />
        <w:bottom w:w="45" w:type="dxa" />
        <w:right w:w="85" w:type="dxa" />
      </w:tblCellMar>
    </w:tblPr>
    <w:tblStylePr w:type="firstRow">
      <w:rPr>
        <w:b />
      </w:rPr>
      <w:tcPr>
        <w:shd w:val="clear" w:color="auto" w:fill="DCE6F1" />
        <w:vAlign w:val="bottom" />
      </w:tcPr>
    </w:tblStylePr>
  </w:style>'''
        s = s.replace(m.group(1), table)
        # captions: 9 pt italic grey
        for sid in ['ImageCaption', 'TableCaption', 'Caption']:
            m = re.search(r'(<w:style w:type="paragraph"[^>]*w:styleId="%s">.*?</w:style>)' % sid, s, flags=re.S)
            if m and '<w:sz ' not in m.group(1):
                blk = m.group(1)
                if '<w:rPr>' in blk: new = blk.replace('</w:rPr>', '  <w:sz w:val="18" />\n      <w:szCs w:val="18" />\n    </w:rPr>', 1)
                else: new = blk.replace('</w:style>', '<w:rPr><w:sz w:val="18" /><w:szCs w:val="18" /></w:rPr></w:style>')
                s = s.replace(blk, new)
        data = s.encode()
    if item.filename == 'word/document.xml':
        d = data.decode()
        d = d.replace('</w:footnotePr>', '</w:footnotePr>\n      <w:pgSz w:w="12240" w:h="15840" />\n      <w:pgMar w:top="1224" w:right="1224" w:bottom="1224" w:left="1224" w:header="708" w:footer="708" w:gutter="0" />')
        assert 'w:pgMar' in d
        data = d.encode()
    if item.filename == 'word/document.xml':
        d = data.decode()
        assert 'xmlns:r=' in d.split('>')[1] or 'xmlns:r=' in d[:2000]
        d = d.replace('<w:sectPr>', '<w:sectPr>\n      <w:footerReference w:type="default" r:id="rId9" />', 1)
        data = d.encode()
    if item.filename == 'word/_rels/document.xml.rels':
        d = data.decode()
        assert 'Id="rId9"' not in d
        d = d.replace('</Relationships>', '<Relationship Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Id="rId9" Target="footer1.xml" /></Relationships>')
        data = d.encode()
    if item.filename == '[Content_Types].xml':
        d = data.decode()
        d = d.replace('</Types>', '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml" /></Types>')
        data = d.encode()
    zout.writestr(item, data)
RPR = '<w:rPr><w:color w:val="7F7F7F" /><w:sz w:val="16" /><w:szCs w:val="16" /></w:rPr>'
FOOTER = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
          '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
          '<w:p><w:pPr><w:jc w:val="center" /></w:pPr>'
          f'<w:r>{RPR}<w:t xml:space="preserve">PSLN program: portfolio recommendation and proposal for next steps, 1 November 2026  |  page </w:t></w:r>'
          f'<w:r>{RPR}<w:fldChar w:fldCharType="begin" /></w:r><w:r>{RPR}<w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
          f'<w:r>{RPR}<w:fldChar w:fldCharType="separate" /></w:r><w:r>{RPR}<w:t>1</w:t></w:r><w:r>{RPR}<w:fldChar w:fldCharType="end" /></w:r>'
          '</w:p></w:ftr>')
zout.writestr('word/footer1.xml', FOOTER)
zout.close()
print('reference written', DST)
