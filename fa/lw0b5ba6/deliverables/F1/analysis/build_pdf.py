"""
build_pdf.py -- renders the finished Markdown proposal to PDF with reportlab (no LaTeX needed).
Handles the Markdown subset used by the proposal: YAML title block, #/## headings, paragraphs, bullet and numbered lists,
pipe tables, images with captions, **bold**, *italic*, `code`, and page-break blocks.
"""
import re, os, sys, html
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib
from PIL import Image as PILImage

FD = os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data', 'fonts', 'ttf')
for name, f in [('DV', 'DejaVuSans.ttf'), ('DV-B', 'DejaVuSans-Bold.ttf'), ('DV-I', 'DejaVuSans-Oblique.ttf'), ('DV-BI', 'DejaVuSans-BoldOblique.ttf'), ('DVM', 'DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(FD, f)))
pdfmetrics.registerFontFamily('DV', normal='DV', bold='DV-B', italic='DV-I', boldItalic='DV-BI')

WARN = []
def build(md_path, pdf_path, base_dir):
    src = open(md_path, encoding='utf8').read()
    meta = {}
    if src.startswith('---'):
        head, src = src[3:].split('\n---', 1)
        for line in head.strip().splitlines():
            k, v = line.split(':', 1); meta[k.strip()] = v.strip().strip('"')
    NAVY = colors.HexColor('#1F3A5F')
    S = dict(
        body=ParagraphStyle('body', fontName='DV', fontSize=9, leading=12.6, spaceAfter=5.5, alignment=TA_LEFT),
        h1=ParagraphStyle('h1', fontName='DV-B', fontSize=13.5, leading=17, spaceBefore=13, spaceAfter=6, textColor=NAVY, keepWithNext=1),
        h2=ParagraphStyle('h2', fontName='DV-B', fontSize=11, leading=14, spaceBefore=9, spaceAfter=4, textColor=NAVY, keepWithNext=1),
        title=ParagraphStyle('title', fontName='DV-B', fontSize=18, leading=22, spaceAfter=5, textColor=NAVY),
        sub=ParagraphStyle('sub', fontName='DV', fontSize=10.5, leading=14, spaceAfter=3, textColor=colors.HexColor('#404040')),
        date=ParagraphStyle('date', fontName='DV', fontSize=9, leading=12, spaceAfter=10, textColor=colors.HexColor('#404040')),
        li=ParagraphStyle('li', fontName='DV', fontSize=9, leading=12.6, spaceAfter=3.5, leftIndent=15, bulletIndent=3, bulletFontName='DV', bulletFontSize=9),
        h3=ParagraphStyle('h3', fontName='DV-B', fontSize=9.3, leading=12.6, spaceBefore=7, spaceAfter=3.5, keepWithNext=1),
        cap=ParagraphStyle('cap', fontName='DV-I', fontSize=7.8, leading=10.2, spaceAfter=9, textColor=colors.HexColor('#404040')),
        cell=ParagraphStyle('cell', fontName='DV', fontSize=7.3, leading=9.3),
        cellh=ParagraphStyle('cellh', fontName='DV-B', fontSize=7.3, leading=9.3),
        cells=ParagraphStyle('cells', fontName='DV', fontSize=6.6, leading=8.3),
        cellsh=ParagraphStyle('cellsh', fontName='DV-B', fontSize=6.6, leading=8.3),
    )
    def inline(t):
        t = html.escape(t, quote=False)
        t = re.sub(r'`([^`]+)`', r'<font face="DVM" size="-0.5">\1</font>', t)
        t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
        t = re.sub(r'(?<![\*\w])\*([^\*\n]+?)\*(?!\*)', r'<i>\1</i>', t)
        return t
    W = A4[0] - 2 * 1.9 * cm
    story = [Paragraph(inline(meta.get('title', '')), S['title']), Paragraph(inline(meta.get('subtitle', '')), S['sub']), Paragraph(inline(meta.get('date', '')), S['date'])]
    lines = src.split('\n'); i = 0
    def flush_par(buf):
        if buf:
            txt = ' '.join(buf)
            story.append(Paragraph(inline(txt), S['h3'] if re.fullmatch(r'\*\*[^*]+\*\*', txt) else S['body']))
    buf = []
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('```{=openxml}'):
            flush_par(buf); buf = []
            while not lines[i + 1].startswith('```'): i += 1
            i += 2; story.append(PageBreak()); continue
        if ln.startswith('# '):
            flush_par(buf); buf = []; story.append(Paragraph(inline(ln[2:]), S['h1'])); i += 1; continue
        if ln.startswith('## '):
            flush_par(buf); buf = []; story.append(Paragraph(inline(ln[3:]), S['h2'])); i += 1; continue
        m = re.match(r'!\[(.*)\]\(([^)]+)\)\{width=([\d.]+)in\}\s*$', ln)
        if m:
            flush_par(buf); buf = []
            cap, path, w = m.group(1), os.path.join(base_dir, m.group(2)), float(m.group(3)) * inch
            w = min(w, W); pw, ph = PILImage.open(path).size; h = w * ph / pw
            maxh = A4[1] - 2 * 1.9 * cm - 70
            if h > maxh: w, h = w * maxh / h, maxh
            story.append(KeepTogether([Image(path, width=w, height=h), Spacer(1, 3), Paragraph(inline(cap), S['cap'])])); i += 1; continue
        if ln.startswith('|'):
            flush_par(buf); buf = []
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')]); i += 1
            sep = rows[1]; widths = [max(3, len(c.strip(':'))) for c in sep]; rows = [rows[0]] + rows[2:]
            tot = sum(widths); cw = [W * x / tot for x in widths]
            nchar = sum(len(c) for r in rows for c in r)
            small = nchar > 6000
            cs, ch = (S['cells'], S['cellsh']) if small else (S['cell'], S['cellh'])
            # layout guard: the longest unbreakable word of every column must fit its width
            for ci in range(len(cw)):
                for ri, r in enumerate(rows):
                    font = (ch if ri == 0 else cs)
                    for tok in re.sub(r'[*`]', '', r[ci]).split():
                        tw = pdfmetrics.stringWidth(tok, 'DV-B' if (ri == 0 or '**' in r[ci]) else 'DV', font.fontSize)
                        if tw > cw[ci] - 7.5:
                            WARN.append(f'table col {ci} ({rows[0][ci][:25]}): token "{tok}" {tw:.0f}pt > {cw[ci]-7.5:.0f}pt')
            data = [[Paragraph(inline(c), ch) for c in rows[0]]] + [[Paragraph(inline(c), cs) for c in r] for r in rows[1:]]
            tb = Table(data, colWidths=cw, repeatRows=1, splitByRow=1)
            tb.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8EEF4')), ('LINEABOVE', (0, 0), (-1, 0), 0.7, colors.HexColor('#7F7F7F')),
                                    ('LINEBELOW', (0, 0), (-1, 0), 0.7, colors.HexColor('#7F7F7F')), ('LINEBELOW', (0, 1), (-1, -1), 0.3, colors.HexColor('#BFBFBF')),
                                    ('LINEBELOW', (0, -1), (-1, -1), 0.7, colors.HexColor('#7F7F7F')), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                    ('LEFTPADDING', (0, 0), (-1, -1), 3.5), ('RIGHTPADDING', (0, 0), (-1, -1), 3.5), ('TOPPADDING', (0, 0), (-1, -1), 2.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5)]))
            story.append(tb); story.append(Spacer(1, 7)); continue
        m = re.match(r'(\d+)\.\s+(.*)', ln); mb = re.match(r'-\s+(.*)', ln)
        if m or mb:
            flush_par(buf); buf = []
            text = [(m.group(2) if m else mb.group(1))]; bullet = (m.group(1) + '.') if m else '•'
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r'(\d+\.|-)\s+', lines[i]) and not lines[i].startswith(('|', '#', '!', '```')):
                text.append(lines[i].strip()); i += 1
            story.append(Paragraph(inline(' '.join(text)), S['li'], bulletText=bullet))
            nxt = next((l for l in lines[i:] if l.strip()), '')
            if not re.match(r'(\d+\.|-)\s+', nxt): story.append(Spacer(1, 4))     # a little air after the last item of a list
            continue
        if not ln.strip():
            flush_par(buf); buf = []; i += 1; continue
        buf.append(ln.strip()); i += 1
    flush_par(buf)
    def footer(canvas, doc):
        canvas.saveState(); canvas.setFont('DV', 7); canvas.setFillColor(colors.HexColor('#595959'))
        canvas.drawCentredString(A4[0] / 2, 1.05 * cm, f'PSLN-344 portfolio proposal  |  1 November 2026  |  page {doc.page}'); canvas.restoreState()
    doc = BaseDocTemplate(pdf_path, pagesize=A4, leftMargin=1.9 * cm, rightMargin=1.9 * cm, topMargin=1.8 * cm, bottomMargin=1.9 * cm,
                          title=meta.get('title', ''), author='Portfolio analysis', subject=meta.get('subtitle', ''))
    doc.addPageTemplates([PageTemplate(id='p', frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='f', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], onPage=footer)])
    doc.build(story)
    return doc.page

if __name__ == '__main__':
    from paths import OUT, BUILD
    n = build(BUILD + 'PSLN-344_portfolio_proposal.md', OUT + 'PSLN-344_portfolio_proposal.pdf', OUT)
    print('pdf pages:', n)
    for w_ in sorted(set(WARN)): print('LAYOUT WARNING', w_)
