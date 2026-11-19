#!/usr/bin/env python
"""
13_build_html.py -- render ../PSLN-344_portfolio_proposal.md to
   (a) ../PSLN-344_portfolio_proposal.html : self-contained (figures embedded), for reading / printing from a browser
   (b) build/proposal_qt.html              : simplified HTML consumed by 14_build_pdf.py
Run: micromamba run -n chem python 13_build_html.py
"""
import os, re, base64, markdown
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..'))
md = open(os.path.join(ROOT, 'PSLN-344_portfolio_proposal.md'), encoding='utf-8').read()
body = markdown.markdown(md, extensions=['tables', 'sane_lists'])
CAP = {'fig1_survival_overview.png': 'Figure 1', 'fig2_moa_map.png': 'Figure 2', 'fig3_data_integrity.png': 'Figure 3',
       'figA1_km_grid.png': 'Figure A1', 'figA2_safety_dose.png': 'Figure A2', 'figA3_restoration_cascade.png': 'Figure A3'}
CSS = '''
body{font-family:"Segoe UI",Helvetica,Arial,sans-serif;font-size:14px;line-height:1.45;color:#1a1a1a;max-width:980px;margin:28px auto;padding:0 18px}
h1{font-size:24px;border-bottom:2px solid #1f5fa8;padding-bottom:6px} h2{font-size:19px;margin-top:30px;color:#0b2f5b} h3{font-size:15px;margin-top:20px;color:#0b2f5b}
table{border-collapse:collapse;width:100%;margin:12px 0;font-size:12.5px} th,td{border:1px solid #c8c8c8;padding:5px 7px;vertical-align:top;text-align:left} th{background:#eef3fa}
tr:nth-child(even) td{background:#fafafa} img{max-width:100%;height:auto;display:block;margin:14px auto} code{background:#f2f2f2;padding:1px 4px;border-radius:3px;font-size:12px}
hr{border:0;border-top:1px solid #ddd;margin:26px 0} em{color:#333}
@media print{body{max-width:none;margin:0;font-size:11px} table{font-size:9.5px} h2{page-break-after:avoid} tr,img{page-break-inside:avoid}}
'''
def embed(m):
    path = os.path.join(ROOT, m.group(1)); b64 = base64.b64encode(open(path, 'rb').read()).decode()
    return f'<img alt="{CAP.get(os.path.basename(path), "figure")}" src="data:image/png;base64,{b64}"'
html = re.sub(r'<img alt="[^"]*" src="([^"]+)"', embed, body)
open(os.path.join(ROOT, 'PSLN-344_portfolio_proposal.html'), 'w', encoding='utf-8').write(
    f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>PSLN-344 portfolio review proposal</title><style>{CSS}</style></head><body>{html}</body></html>')
os.makedirs(os.path.join(HERE, 'build'), exist_ok=True)
open(os.path.join(HERE, 'build', 'proposal_body.html'), 'w', encoding='utf-8').write(body)
print('html written;', len(html) // 1024, 'kB; tables:', body.count('<table>'), 'images:', body.count('<img'))
