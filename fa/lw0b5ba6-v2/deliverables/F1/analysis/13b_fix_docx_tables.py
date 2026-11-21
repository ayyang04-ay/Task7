"""Post-process the pandoc .docx: give every table explicit column widths that fill the text width (7.0 in = 10080 twips),
so Word and LibreOffice lay the tables out identically instead of guessing from a 5.5-in grid."""
import zipfile, re, sys, shutil, os
path = sys.argv[1]; TEXT_W = 10080
zin = zipfile.ZipFile(path); tmp = path + '.tmp'; zout = zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED)
n_tab = 0
def fix_table(m):
    global n_tab
    t = m.group(0)
    g = re.search(r'<w:tblGrid>(.*?)</w:tblGrid>', t, re.S)
    w = [int(x) for x in re.findall(r'w:w="(\d+)"', g.group(1))]
    scale = TEXT_W / sum(w); w2 = [round(x * scale) for x in w]; w2[-1] += TEXT_W - sum(w2)
    t = t.replace(g.group(0), '<w:tblGrid>' + ''.join(f'<w:gridCol w:w="{x}" />' for x in w2) + '</w:tblGrid>')
    t = t.replace('<w:tblW w:type="pct" w:w="5000" />', f'<w:tblW w:type="dxa" w:w="{TEXT_W}" />')
    def fix_row(rm):
        cells = re.split(r'(?=<w:tc>)', rm.group(0)); out = [cells[0]]; k = 0
        for c in cells[1:]:
            assert k < len(w2), 'more cells than grid columns'
            c = c.replace('<w:tcPr />', f'<w:tcPr><w:tcW w:w="{w2[k]}" w:type="dxa" /></w:tcPr>', 1); out.append(c); k += 1
        assert k == len(w2), (k, len(w2))
        return ''.join(out)
    t = re.sub(r'<w:tr>.*?</w:tr>', fix_row, t, flags=re.S)
    n_tab += 1
    return t
for item in zin.infolist():
    data = zin.read(item.filename)
    if item.filename == 'word/document.xml':
        d = data.decode(); d = re.sub(r'<w:tbl>.*?</w:tbl>', fix_table, d, flags=re.S); data = d.encode()
    zout.writestr(item, data)
zout.close(); zin.close(); shutil.move(tmp, path)
print('tables fixed:', n_tab)
