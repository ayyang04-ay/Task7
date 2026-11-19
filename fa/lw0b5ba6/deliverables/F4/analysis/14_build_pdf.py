#!/usr/bin/env python
"""
14_build_pdf.py -- typeset build/proposal_body.html (from 13_build_html.py) into ../PSLN-344_portfolio_proposal.pdf
with Qt's rich-text engine, and write page previews (build/preview/page_XX.png) from the SAME layout so that the PDF
can be checked visually. Figures that would be pushed to the next page are shrunk (never below 72 % of their
preferred size) when that lets them fit in the space left on the current page; headings stranded at the foot of a
page are moved to the next one.   Run: micromamba run -n core python 14_build_pdf.py
"""
import os, re, sys, glob
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QTextDocument, QFontDatabase, QFont, QPdfWriter, QPageSize, QPageLayout, QImage, QPainter, QColor, QPen
from PySide6.QtCore import QSizeF, QMarginsF, QRectF, Qt
import matplotlib
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..'))
app = QApplication(sys.argv)
for f in glob.glob(os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data', 'fonts', 'ttf', 'DejaVuSans*.ttf')): QFontDatabase.addApplicationFont(f)

RES = 96
pdf_path = os.path.join(ROOT, 'PSLN-344_portfolio_proposal.pdf')
w = QPdfWriter(pdf_path); w.setPageSize(QPageSize(QPageSize.A4)); w.setPageMargins(QMarginsF(16, 15, 16, 17), QPageLayout.Millimeter); w.setResolution(RES)
w.setTitle('PSLN-344 portfolio review: recommendation and next-step proposal'); w.setCreator('analysis/14_build_pdf.py')
paint = w.pageLayout().paintRectPixels(RES); full = w.pageLayout().fullRectPixels(RES)
PW, PH = paint.width(), paint.height()

RAW = open(os.path.join(HERE, 'build', 'proposal_body.html'), encoding='utf-8').read()
PREF = {'fig1_survival_overview.png': 0.49, 'fig2_moa_map.png': 0.72, 'fig3_data_integrity.png': 0.57, 'figA3_restoration_cascade.png': 0.84,
        'figA1_km_grid.png': 0.66, 'figA2_safety_dose.png': 0.57}      # preferred maximum height as a fraction of the text block
KEEP = {'fig2_moa_map.png': 0.86}                                      # figures that must stay (nearly) full size
FORCE_BREAK = ['Appendix B — Supporting figures and tables']
MINSCALE = 0.72
WIDTHS = [[15, 33, 38, 14], [14, 61, 25], [23, 45, 32], [20, 45, 15, 20], [17, 17, 28, 9, 29], [29, 13, 58], [4, 15, 58, 23], [11, 13, 27, 7, 10, 10, 9, 13], [42, 58]]
CSS = '''
body { font-family: "DejaVu Sans"; font-size: 8.6pt; color: #161616; }
h1 { font-size: 16pt; color: #0b2f5b; margin-top: 0px; margin-bottom: 6px; }
h2 { font-size: 12pt; color: #0b2f5b; margin-top: 14px; margin-bottom: 4px; }
h3 { font-size: 9.6pt; color: #0b2f5b; margin-top: 10px; margin-bottom: 2px; }
p { margin-top: 4px; margin-bottom: 5px; }
li { margin-top: 1px; margin-bottom: 2px; }
td, th { font-size: 7.3pt; }
code { font-family: "DejaVu Sans Mono"; font-size: 7.4pt; }
hr { color: #c8c8c8; }
'''
natural = {}
for m in re.finditer(r'<img alt="[^"]*" src="([^"]+)"', RAW):
    path = os.path.join(ROOT, m.group(1)); iw, ih = Image.open(path).size; name = os.path.basename(path)
    hmax = min(PW * ih / iw, PREF.get(name, 0.6) * PH); natural[name] = (path, iw, ih, hmax)
heights = {k: v[3] for k, v in natural.items()}
breaks = set(FORCE_BREAK)                                             # heading texts that get a page break before them

def build():
    body = RAW
    def img(m):
        name = os.path.basename(m.group(1)); path, iw, ih, _ = natural[name]; hpx = int(heights[name]); wpx = int(hpx * iw / ih)
        return f'<img src="{path}" width="{wpx}" height="{hpx}"'
    body = re.sub(r'<img alt="[^"]*" src="([^"]+)"', img, body).replace('<p><img', '<p align="center"><img')
    parts = re.split(r'(<table>.*?</table>)', body, flags=re.S); k = 0
    for i, p in enumerate(parts):
        if p.startswith('<table>'):
            ws = WIDTHS[k]; k += 1
            first = 'page-break-before:always; ' if k == 1 else ''          # the gate table opens page 2
            p = p.replace('<table>', f'<table border="1" cellspacing="0" cellpadding="4" width="100%" style="{first}border-collapse:collapse; border-color:#b5b5b5; margin-top:6px; margin-bottom:8px;">', 1)
            j = [0]
            def th(m):
                wv = ws[j[0]] if j[0] < len(ws) else 10; j[0] += 1
                return f'<th width="{wv}%" bgcolor="#e8eff8" align="left">'
            parts[i] = re.sub(r'<th>', th, p)
    assert k == len(WIDTHS), (k, len(WIDTHS))
    body = ''.join(parts)
    def head(m):
        tag, txt = m.group(1), m.group(2)
        return f'<{tag} style="page-break-before:always">{txt}</{tag}>' if re.sub('<[^>]+>', '', txt) in breaks else m.group(0)
    body = re.sub(r'<(h[23])>(.*?)</\1>', head, body, flags=re.S)
    doc = QTextDocument(); doc.setDefaultFont(QFont('DejaVu Sans', 9)); doc.setDocumentMargin(0); doc.setDefaultStyleSheet(CSS)
    doc.setPageSize(QSizeF(PW, PH)); doc.setHtml(f'<html><head><style>{CSS}</style></head><body>{body}</body></html>')
    return doc

def scan(doc):
    """returns list of (kind, name/text, top, bottom, prev_bottom, next_top) for image blocks and headings"""
    lay = doc.documentLayout(); out = []; blocks = []
    b = doc.begin()
    while b.isValid():
        r = lay.blockBoundingRect(b); kind = None; name = None
        it = b.begin()
        while not it.atEnd():
            fr = it.fragment()
            if fr.isValid() and fr.charFormat().isImageFormat():
                kind = 'img'; name = os.path.basename(fr.charFormat().toImageFormat().name())
            it += 1
        if kind is None and b.blockFormat().headingLevel() in (2, 3): kind = 'head'; name = b.text()
        blocks.append((kind, name, r.top(), r.bottom())); b = b.next()
    for i, (kind, name, top, bot) in enumerate(blocks):
        if kind:
            prev_bot = max((x[3] for x in blocks[:i] if x[3] <= top + 1), default=0)
            nxt = next((x[2] for x in blocks[i + 1:] if x[3] - x[2] > 1), None)
            out.append((kind, name, top, bot, prev_bot, nxt))
    return out

for _ in range(20):
    doc = build(); changed = False
    for kind, name, top, bot, prev_bot, nxt in scan(doc):
        page_top = (top // PH) * PH
        if kind == 'img' and (top // PH) != ((bot - 1) // PH):               # Qt pushed the figure to the next page, leaving a gap here
            avail = PH - (top - page_top) - 30
            if avail >= KEEP.get(name, MINSCALE) * natural[name][3] and avail < heights[name] - 2:
                heights[name] = avail; changed = True; print(f'  shrink {name} -> {int(avail)} px ({100 * avail / natural[name][3]:.0f}% of preferred)'); break
        if kind == 'head' and name not in breaks and (top // PH) == ((bot - 1) // PH) and PH - (bot - page_top) < 70:
            breaks.add(name); changed = True; print(f'  page break before stranded heading: {name[:60]}'); break
    if not changed: break

n = doc.pageCount()
foot = QFont('DejaVu Sans'); foot.setPixelSize(9)
def draw_page(p, i, ox, oy):
    p.save(); p.translate(ox, oy - i * PH); doc.drawContents(p, QRectF(0, i * PH, PW, PH)); p.restore()
    p.save(); p.setFont(foot); p.setPen(QPen(QColor('#777777')))
    p.drawText(QRectF(ox, oy + PH + 8, PW, 16), Qt.AlignLeft, 'PSLN-344 portfolio review — prepared 1 Nov 2026 from the 3 Sep 2026 data cut')
    p.drawText(QRectF(ox, oy + PH + 8, PW, 16), Qt.AlignRight, f'page {i + 1} of {n}'); p.restore()
p = QPainter(w)
for i in range(n):
    if i: w.newPage()
    draw_page(p, i, 0, 0)
p.end()
prev = os.path.join(HERE, 'build', 'preview'); os.makedirs(prev, exist_ok=True)
for f in glob.glob(prev + '/page_*.png'): os.remove(f)
S = 1.6
for i in range(n):
    im = QImage(int(full.width() * S), int(full.height() * S), QImage.Format_ARGB32); im.fill(QColor('white'))
    q = QPainter(im); q.setRenderHint(QPainter.Antialiasing); q.setRenderHint(QPainter.SmoothPixmapTransform); q.scale(S, S); draw_page(q, i, paint.x(), paint.y()); q.end()
    im.save(os.path.join(prev, f'page_{i + 1:02d}.png'))
# report blank space at the foot of each page (for layout QA)
lay = doc.documentLayout(); ends = {}
b = doc.begin()
while b.isValid():
    r = lay.blockBoundingRect(b)
    if r.height() > 1: ends[int(r.bottom() - 1) // PH] = max(ends.get(int(r.bottom() - 1) // PH, 0), r.bottom() - (int(r.bottom() - 1) // PH) * PH)
    b = b.next()
print('pdf:', pdf_path, '| pages:', n, '| size kB:', os.path.getsize(pdf_path) // 1024)
print('figure heights (px):', {k: int(v) for k, v in heights.items()})
if os.environ.get('PDF_DEBUG'):
    for kind, name, top, bot, prev_bot, nxt in scan(doc):
        print(f'{kind:5s} {str(name)[:45]:45s} page {int(top // PH) + 1} top_in_page {top - (top // PH) * PH:7.1f} bottom_in_page {bot - (bot // PH) * PH:7.1f} prev_bot {prev_bot:8.1f} top {top:8.1f} next {nxt}')
