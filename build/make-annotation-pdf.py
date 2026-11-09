import re, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

src, out = sys.argv[1], sys.argv[2]
body = ParagraphStyle('body', fontName='Helvetica', fontSize=9.5, leading=13,
                      alignment=TA_LEFT, spaceAfter=4, splitLongWords=0, hyphenationLang='')
bullet = ParagraphStyle('bullet', parent=body, leftIndent=10*mm, bulletIndent=4*mm, spaceAfter=2)
h1 = ParagraphStyle('h1', parent=body, fontName='Helvetica-Bold', fontSize=16, leading=20, spaceBefore=14, spaceAfter=8)
h2 = ParagraphStyle('h2', parent=body, fontName='Helvetica-Bold', fontSize=13, leading=17, spaceBefore=12, spaceAfter=6)
h3 = ParagraphStyle('h3', parent=body, fontName='Helvetica-Bold', fontSize=10.5, leading=14, spaceBefore=9, spaceAfter=3)

def inline(t):
    t = t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    return t

flow, buf = [], []
def flush():
    if buf:
        flow.append(Paragraph(inline(' '.join(buf)), body)); buf.clear()

for raw in open(src).read().split('\n'):
    line = raw.rstrip()
    if line.startswith('### '):   flush(); flow.append(Paragraph(inline(line[4:]), h3))
    elif line.startswith('## '):  flush(); flow.append(Paragraph(inline(line[3:]), h2))
    elif line.startswith('# '):   flush(); flow.append(Paragraph(inline(line[2:]), h1))
    elif line.startswith('- '):   flush(); flow.append(Paragraph(inline(line[2:]), bullet, bulletText='•'))
    elif line.startswith('  ') and flow and isinstance(flow[-1], Paragraph) and not buf:
        flow[-1] = Paragraph(flow[-1].text + ' ' + inline(line.strip()), bullet, bulletText='•')
    elif line.strip()=='':        flush()
    else:                         buf.append(line.strip())
flush()

SimpleDocTemplate(out, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm,
                  topMargin=18*mm, bottomMargin=18*mm,
                  title='Study annotation', author='').build(flow)
print('wrote', out)
