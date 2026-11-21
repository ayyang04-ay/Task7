"""postprocess_docx.py - tidy the pandoc DOCX so that tables render the same in every word processor:
explicit column widths scaled to the text width, 9-pt 'Compact' text in every table cell, rows not split across pages."""
import zipfile, re, sys, shutil
SRC, DST = sys.argv[1], sys.argv[2]
TEXT_W = 12240 - 2 * 1224          # twips (US Letter, 0.85 in margins; must match make_reference_docx.py)
zin = zipfile.ZipFile(SRC); zout = zipfile.ZipFile(DST, 'w', zipfile.ZIP_DEFLATED)
ntab = 0
def fix_table(m):
    global ntab
    tbl = m.group(0); ntab += 1
    assert tbl.count('<w:tbl>') == 1, 'nested table'
    cols = [int(x) for x in re.findall(r'<w:gridCol w:w="(\d+)" />', tbl)]
    mt = re.search(r'<w:tblW w:type="pct" w:w="(\d+)" />', tbl)
    pct = int(mt.group(1)) if mt else 5000
    total = round(TEXT_W * min(pct, 5000) / 5000)
    new = [round(c * total / sum(cols)) for c in cols]
    tbl = re.sub(r'<w:tblW [^>]*/>', f'<w:tblW w:type="dxa" w:w="{sum(new)}" />', tbl, count=1)
    it = iter(new); tbl = re.sub(r'<w:gridCol w:w="\d+" />', lambda _: f'<w:gridCol w:w="{next(it)}" />', tbl)
    borders = ('<w:tblBorders><w:top w:val="single" w:sz="6" w:space="0" w:color="7F7F7F" /><w:left w:val="single" w:sz="4" w:space="0" w:color="BFBFBF" />'
               '<w:bottom w:val="single" w:sz="6" w:space="0" w:color="7F7F7F" /><w:right w:val="single" w:sz="4" w:space="0" w:color="BFBFBF" />'
               '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="BFBFBF" /><w:insideV w:val="single" w:sz="4" w:space="0" w:color="BFBFBF" /></w:tblBorders>')
    assert tbl.count('<w:tblLayout') == 1
    tbl = tbl.replace('<w:tblLayout', borders + '<w:tblLayout', 1)
    def fix_row(mr):
        row = mr.group(0); k = [0]
        header = '<w:tblHeader' in row
        shd = '<w:shd w:val="clear" w:color="auto" w:fill="DCE6F1" />' if header else ''
        def fix_cell(_):
            w = new[k[0]]; k[0] += 1
            return f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa" />{shd}</w:tcPr>'
        n_cells = row.count('<w:tc>')
        assert n_cells == len(new) and row.count('<w:tc><w:tcPr />') == n_cells, (n_cells, len(new), row[:300])
        row = re.sub(r'<w:tc><w:tcPr />', fix_cell, row)
        if header:      # direct formatting so that the header stays bold in applications that ignore table styles
            row = row.replace('<w:r><w:t', '<w:r><w:rPr><w:b /><w:bCs /></w:rPr><w:t')
        if '<w:trPr>' in row: row = row.replace('<w:trPr>', '<w:trPr><w:cantSplit />', 1)
        else: row = row.replace('<w:tr>', '<w:tr><w:trPr><w:cantSplit /></w:trPr>', 1)
        return row
    tbl = re.sub(r'<w:tr>.*?</w:tr>', fix_row, tbl, flags=re.S)
    tbl = tbl.replace('<w:pStyle w:val="FirstParagraph" />', '<w:pStyle w:val="Compact" />').replace('<w:pStyle w:val="BodyText" />', '<w:pStyle w:val="Compact" />')
    return tbl
for item in zin.infolist():
    data = zin.read(item.filename)
    if item.filename == 'word/document.xml':
        d = data.decode('utf-8')
        d = re.sub(r'<w:tbl>.*?</w:tbl>', fix_table, d, flags=re.S)
        d = d.replace('descr="/tmp/outputs/figures/', 'descr="')
        data = d.encode('utf-8')
    zout.writestr(item, data)
zout.close()
import xml.dom.minidom as md
z = zipfile.ZipFile(DST)
for n in z.namelist():
    if n.endswith('.xml') or n.endswith('.rels'): md.parseString(z.read(n))
print(f'post-processed {ntab} tables; all XML parts well-formed ->', DST)
