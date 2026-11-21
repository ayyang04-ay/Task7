"""Minimal Markdown -> PDF (reportlab) for the proposal: headings, paragraphs, bullets, blockquote, pipe tables, images."""
import re, os, sys
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
                                Image, KeepTogether, PageBreak, NextPageTemplate)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
import matplotlib
FD = os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data', 'fonts', 'ttf')
pdfmetrics.registerFont(TTFont('DV', os.path.join(FD, 'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DV-B', os.path.join(FD, 'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFont(TTFont('DV-I', os.path.join(FD, 'DejaVuSans-Oblique.ttf')))
pdfmetrics.registerFont(TTFont('DV-BI', os.path.join(FD, 'DejaVuSans-BoldOblique.ttf')))
pdfmetrics.registerFont(TTFont('DVM', os.path.join(FD, 'DejaVuSansMono.ttf')))
addMapping('DV', 0, 0, 'DV'); addMapping('DV', 1, 0, 'DV-B'); addMapping('DV', 0, 1, 'DV-I'); addMapping('DV', 1, 1, 'DV-BI')

SRC, OUT, BASE = sys.argv[1], sys.argv[2], os.path.dirname(os.path.abspath(sys.argv[1]))
ss = getSampleStyleSheet()
body = ParagraphStyle('body', parent=ss['BodyText'], fontName='DV', fontSize=9, leading=12, spaceAfter=4)
small = ParagraphStyle('small', parent=body, fontSize=7.2, leading=8.8, spaceAfter=0)
smallb = ParagraphStyle('smallb', parent=small, fontName='DV-B')
h1 = ParagraphStyle('h1', parent=body, fontName='DV-B', fontSize=14, leading=17, spaceBefore=10, spaceAfter=6, textColor=colors.HexColor('#3f007d'))
h2 = ParagraphStyle('h2', parent=body, fontName='DV-B', fontSize=11, leading=14, spaceBefore=8, spaceAfter=4, textColor=colors.HexColor('#54278f'))
title = ParagraphStyle('title', parent=body, fontName='DV-B', fontSize=18, leading=22, spaceAfter=4)
subtitle = ParagraphStyle('subtitle', parent=body, fontName='DV', fontSize=11, leading=14, textColor=colors.HexColor('#555555'))
bullet = ParagraphStyle('bullet', parent=body, leftIndent=12, bulletIndent=3, spaceAfter=2)
bullet2 = ParagraphStyle('bullet2', parent=body, leftIndent=24, bulletIndent=15, spaceAfter=2)
quote = ParagraphStyle('quote', parent=body, fontSize=9.5, leading=12.5, leftIndent=8, rightIndent=8, backColor=colors.HexColor('#f2f0f7'),
                       borderColor=colors.HexColor('#54278f'), borderWidth=0.8, borderPadding=6, spaceBefore=6, spaceAfter=8)
quoteb = ParagraphStyle('quoteb', parent=quote, leftIndent=20, bulletIndent=10, spaceBefore=0, spaceAfter=0, borderWidth=0)
caption = ParagraphStyle('caption', parent=body, fontName='DV-I', fontSize=8, leading=10, textColor=colors.HexColor('#333333'))

def inline(t):
    t = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    t = re.sub(r'`([^`]+)`', r'<font face="DVM">\1</font>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'(?<![\w*])\*([^*\n]+?)\*(?![\w*])', r'<i>\1</i>', t)
    return t

def parse_table(lines):
    rows = [[c.strip() for c in l.strip().strip('|').split('|')] for l in lines]
    sep = rows[1]; widths = [len(x.strip(':')) for x in sep]
    return rows[0], rows[2:], widths

lines = open(SRC, encoding='utf-8').read().split('\n')
# front matter
meta = {}
if lines[0].strip() == '---':
    j = 1
    while lines[j].strip() != '---':
        k, v = lines[j].split(':', 1); meta[k.strip()] = v.strip().strip('"'); j += 1
    lines = lines[j+1:]
story = []
PW = A4[0] - 30*mm
story += [Paragraph(inline(meta.get('title', '')), title), Paragraph(inline(meta.get('subtitle', '')), subtitle),
          Paragraph(inline(meta.get('date', '')), subtitle), Spacer(1, 8)]
i = 0; para = []
def flush():
    global para
    if para:
        story.append(Paragraph(inline(' '.join(para)), body)); para = []
while i < len(lines):
    l = lines[i]; s = l.strip()
    if not s:
        flush(); i += 1; continue
    if s.startswith('# '):
        flush(); story.append(Paragraph(inline(s[2:]), h1)); i += 1; continue
    if s.startswith('## '):
        flush(); story.append(Paragraph(inline(s[3:]), h2)); i += 1; continue
    if s.startswith('!['):
        flush(); m = re.match(r'!\[(.*)\]\((.*)\)', s); cap, path = m.group(1), m.group(2)
        from reportlab.lib.utils import ImageReader
        ir = ImageReader(os.path.join(BASE, path)); iw, ih = ir.getSize()
        w = PW; h = ih * w / iw
        maxh = 235*mm
        if h > maxh: h = maxh; w = iw * h / ih
        story.append(KeepTogether([Image(os.path.join(BASE, path), width=w, height=h), Paragraph(inline(cap), caption), Spacer(1, 6)]))
        i += 1; continue
    if s.startswith('>'):
        flush(); q = []
        while i < len(lines) and lines[i].strip().startswith('>'):
            q.append(lines[i].strip()[1:].strip()); i += 1
        # group into paragraphs / bullets inside quote
        blocks = []; cur = []
        for x in q:
            if not x:
                if cur: blocks.append(('p', ' '.join(cur))); cur = []
            elif x.startswith('* ') or x.startswith('- '):
                if cur: blocks.append(('p', ' '.join(cur))); cur = []
                blocks.append(('b', x[2:]))
            else: cur.append(x)
        if cur: blocks.append(('p', ' '.join(cur)))
        cells = []
        for typ, txt in blocks:
            if typ == 'p': cells.append(Paragraph(inline(txt), ParagraphStyle('qp', parent=body, fontSize=9.5, leading=12.5)))
            else: cells.append(Paragraph(inline(txt), ParagraphStyle('qb', parent=body, fontSize=9.5, leading=12.5, leftIndent=12, bulletIndent=3), bulletText='•'))
        t = Table([[cells]], colWidths=[PW])
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f2f0f7')), ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#54278f')),
                               ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8), ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
        story += [t, Spacer(1, 6)]; continue
    if s.startswith('|'):
        flush(); tl = []
        while i < len(lines) and lines[i].strip().startswith('|'):
            tl.append(lines[i]); i += 1
        hdr, rows, widths = parse_table(tl)
        tot = sum(widths); cw = [PW * w / tot for w in widths]
        data = [[Paragraph(inline(c), smallb) for c in hdr]] + [[Paragraph(inline(c), small) for c in r] for r in rows]
        t = Table(data, colWidths=cw, repeatRows=1)
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dadaeb')), ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#999999')),
                               ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 3), ('RIGHTPADDING', (0, 0), (-1, -1), 3),
                               ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                               ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7f7f7')])]))
        story += [t, Spacer(1, 6)]; continue
    m = re.match(r'^(\s*)([*-]|\d+\.)\s+(.*)$', l)
    if m:
        flush(); ind = len(m.group(1)); mark = m.group(2); txt = m.group(3)
        # continuation lines
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(\s*)([*-]|\d+\.)\s+', lines[i]) and not lines[i].strip().startswith(('|', '#', '>', '![')):
            txt += ' ' + lines[i].strip(); i += 1
        st = bullet if ind < 2 else bullet2
        story.append(Paragraph(inline(txt), st, bulletText=('•' if mark in '*-' else mark) if ind < 2 else ('–' if mark in '*-' else mark)))
        continue
    para.append(s); i += 1
flush()

def onpage(c, d):
    c.saveState(); c.setFont('DV', 7); c.setFillColor(colors.HexColor('#777777'))
    c.drawString(15*mm, 8*mm, 'PSLN-344 portfolio review proposal - 1 Nov 2026 - based solely on psln_program_dataset.xlsx and psln_program_annotation.pdf')
    c.drawRightString(A4[0]-15*mm, 8*mm, f'page {d.page}'); c.restoreState()
doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=15*mm, rightMargin=15*mm, topMargin=14*mm, bottomMargin=14*mm,
                      title=meta.get('title', ''), author='Portfolio analysis')
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='f')
doc.addPageTemplates([PageTemplate(id='p', frames=[frame], onPage=onpage)])
doc.build(story)
print('wrote', OUT)
