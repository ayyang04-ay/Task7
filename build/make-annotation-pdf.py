import re, sys, os

# The info dictionary previously read Creator "(unspecified)", a /Title that did not
# match the filename, and a creation stamp of the moment of generation. Titles are
# keyed on the output filename so each document names itself; SOURCE_DATE_EPOCH gives
# reportlab a fixed creation date instead of "now".
TITLES = {
    'trial_summary.pdf':   ('Dataset annotation',
                            'Per-block annotation of the AMnESTI preclinical dataset'),
    'golden-response.pdf': ('Portfolio review analysis',
                            'Reference analysis of the AMnESTI preclinical dataset'),
}
TITLE, SUBJECT = TITLES.get(os.path.basename(sys.argv[2]) if len(sys.argv) > 2 else '',
                            ('Dataset annotation', 'Annotation of a preclinical dataset'))
os.environ.setdefault('SOURCE_DATE_EPOCH', '1772900460')
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Helvetica's bullet glyph carries no ToUnicode mapping, so every bullet in the
# extracted text came out as "(cid:127)" -- 521 of them in a document whose content
# is almost entirely bulleted. A solver reading this file programmatically, which is
# the normal case for a data room, saw that noise instead of the list structure.
# DejaVuSans is embedded with a ToUnicode map, so the bullet round-trips. It is used
# for the bullet glyph alone; the body font is unchanged.
pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

src, out = sys.argv[1], sys.argv[2]
body = ParagraphStyle('body', fontName='Helvetica', fontSize=9.5, leading=13,
                      alignment=TA_LEFT, spaceAfter=4, splitLongWords=0, hyphenationLang='')
bullet = ParagraphStyle('bullet', parent=body, leftIndent=10*mm, bulletIndent=4*mm, spaceAfter=2,
                        bulletFontName='DejaVuSans', bulletFontSize=8)
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
                  title=TITLE, author='Preclinical Data Management',
                  creator='Preclinical Data Management', subject=SUBJECT).build(flow)
print('wrote', out)
