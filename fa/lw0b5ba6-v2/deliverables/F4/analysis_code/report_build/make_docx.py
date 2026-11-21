import zipfile, re, subprocess, sys, shutil, os
src_md = 'proposal.md'; raw = 'proposal_raw.docx'; out = sys.argv[1]
subprocess.run(['micromamba','run','-n','genomics','pandoc', src_md, '-f','markdown','-t','docx','--reference-doc=reference.docx','-o', raw], check=True)
zin = zipfile.ZipFile(raw); zout = zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED)
for item in zin.infolist():
    data = zin.read(item.filename)
    if item.filename == 'word/document.xml':
        d = data.decode()
        def fix_tbl(m):
            t = m.group(0)
            t = t.replace('<w:pStyle w:val="Compact" />', '<w:pStyle w:val="TableText" />')
            # rows should not split across pages
            t = t.replace('<w:tr><w:tc>', '<w:tr><w:trPr><w:cantSplit /></w:trPr><w:tc>')
            t = t.replace('<w:trPr><w:tblHeader w:val="on" /></w:trPr>', '<w:trPr><w:cantSplit /><w:tblHeader w:val="on" /></w:trPr>')
            return t
        d, n = re.subn(r'<w:tbl>.*?</w:tbl>', fix_tbl, d, flags=re.S)
        print('tables post-processed:', n)
        # rebuild the section properties in schema order: footerReference, footnotePr, pgSz, pgMar
        sp = re.search(r'<w:sectPr>(.*?)</w:sectPr>', d, flags=re.S)
        inner = sp.group(1)
        pgsz = re.search(r'<w:pgSz[^>]*/>', inner).group(0); pgmar = re.search(r'<w:pgMar[^>]*/>', inner).group(0)
        fn = re.search(r'<w:footnotePr>.*?</w:footnotePr>', inner, flags=re.S)
        fn = re.sub(r'\s+', ' ', fn.group(0)) if fn else ''
        new_sp = '<w:sectPr><w:footerReference w:type="default" r:id="rIdFooter1" />' + fn + pgsz + pgmar + '</w:sectPr>'
        d = d[:sp.start()] + new_sp + d[sp.end():]
        data = d.encode()
    if item.filename == '[Content_Types].xml':
        c = data.decode()
        if 'footer1.xml' not in c:
            c = c.replace('</Types>', '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml" /></Types>')
        data = c.encode()
    if item.filename == 'word/_rels/document.xml.rels':
        c = data.decode()
        c = c.replace('</Relationships>', '<Relationship Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Id="rIdFooter1" Target="footer1.xml" /></Relationships>')
        data = c.encode()
    if item.filename == 'docProps/core.xml':
        c = data.decode()
        c = re.sub(r'<dc:creator>.*?</dc:creator>', '<dc:creator>Portfolio analysis</dc:creator>', c)
        data = c.encode()
    zout.writestr(item, data)
FOOTER = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><w:p><w:pPr><w:jc w:val="right" /></w:pPr><w:r><w:rPr><w:sz w:val="16" /><w:color w:val="666666" /></w:rPr><w:t xml:space="preserve">PSLN program: portfolio recommendation and next steps · 1 November 2026 · Page </w:t></w:r><w:r><w:rPr><w:sz w:val="16" /><w:color w:val="666666" /></w:rPr><w:fldChar w:fldCharType="begin" /></w:r><w:r><w:rPr><w:sz w:val="16" /><w:color w:val="666666" /></w:rPr><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r><w:r><w:rPr><w:sz w:val="16" /><w:color w:val="666666" /></w:rPr><w:fldChar w:fldCharType="end" /></w:r></w:p></w:ftr>'''
zout.writestr('word/footer1.xml', FOOTER.encode('utf-8'))
zout.close(); os.remove(raw)
# structural check
z = zipfile.ZipFile(out); d = z.read('word/document.xml').decode()
print('tables:', d.count('<w:tbl>'), 'images:', d.count('<w:drawing>'), 'TableText paras:', d.count('w:val="TableText"'), 'Compact paras (lists):', d.count('w:val="Compact"'))
print('media:', sorted(i.filename for i in z.infolist() if 'media' in i.filename))
ext = re.findall(r'<wp:extent cx="(\d+)" cy="(\d+)"', d); print('image sizes (in):', [(round(int(a)/914400,2), round(int(b)/914400,2)) for a,b in ext])
print('sectPr:', re.findall(r'<w:pgSz[^>]*/>|<w:pgMar[^>]*/>', d))
