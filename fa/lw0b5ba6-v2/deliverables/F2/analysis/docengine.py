"""Minimal document engine: one content list -> PDF (reportlab) and Markdown."""
import re, os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, CondPageBreak)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib
FD = os.path.join(matplotlib.get_data_path(), 'fonts', 'ttf')
pdfmetrics.registerFont(TTFont('DV', os.path.join(FD, 'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DV-B', os.path.join(FD, 'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFont(TTFont('DV-I', os.path.join(FD, 'DejaVuSans-Oblique.ttf')))
pdfmetrics.registerFont(TTFont('DV-BI', os.path.join(FD, 'DejaVuSans-BoldOblique.ttf')))
pdfmetrics.registerFontFamily('DV', normal='DV', bold='DV-B', italic='DV-I', boldItalic='DV-BI')

NAVY = colors.HexColor('#12324f'); GREY = colors.HexColor('#555555'); LIGHT = colors.HexColor('#eef3f8'); RULE = colors.HexColor('#9aa7b4'); RED = colors.HexColor('#a3262a')
ST = {
 'title': ParagraphStyle('title', fontName='DV-B', fontSize=17, leading=21, textColor=NAVY, spaceAfter=3),
 'subtitle': ParagraphStyle('subtitle', fontName='DV', fontSize=9.5, leading=13, textColor=GREY, spaceAfter=5),
 'note': ParagraphStyle('note', fontName='DV', fontSize=7.6, leading=10.4, textColor=GREY, spaceAfter=6),
 'h1': ParagraphStyle('h1', fontName='DV-B', fontSize=12.5, leading=16, textColor=NAVY, spaceBefore=11, spaceAfter=5, keepWithNext=1),
 'h2': ParagraphStyle('h2', fontName='DV-B', fontSize=10, leading=13, textColor=NAVY, spaceBefore=8, spaceAfter=3, keepWithNext=1),
 'p': ParagraphStyle('p', fontName='DV', fontSize=8.9, leading=12.4, spaceAfter=5, alignment=TA_LEFT),
 'lead': ParagraphStyle('lead', fontName='DV-B', fontSize=9.8, leading=13.6, spaceAfter=6, textColor=colors.black),
 'bul': ParagraphStyle('bul', fontName='DV', fontSize=8.9, leading=12.2, leftIndent=13, bulletIndent=3, spaceAfter=2.5, bulletFontName='DV', bulletFontSize=8.9),
 'num': ParagraphStyle('num', fontName='DV', fontSize=8.9, leading=12.2, leftIndent=15, bulletIndent=1, spaceAfter=2.5, bulletFontName='DV', bulletFontSize=8.9),
 'cap': ParagraphStyle('cap', fontName='DV', fontSize=7.8, leading=10.4, textColor=colors.HexColor('#333333'), spaceBefore=2, spaceAfter=8),
 'tcap': ParagraphStyle('tcap', fontName='DV-B', fontSize=8.3, leading=11, textColor=NAVY, spaceBefore=5, spaceAfter=3),
 'cell': ParagraphStyle('cell', fontName='DV', fontSize=7.5, leading=9.7),
 'cellb': ParagraphStyle('cellb', fontName='DV-B', fontSize=7.5, leading=9.7, textColor=colors.white),
 'cells': ParagraphStyle('cells', fontName='DV', fontSize=6.5, leading=8.3),
 'cellsb': ParagraphStyle('cellsb', fontName='DV-B', fontSize=6.5, leading=8.3, textColor=colors.white),
 'box': ParagraphStyle('box', fontName='DV', fontSize=8.7, leading=12.0, spaceAfter=3),
}
def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def rl(s):
    """inline markup: **bold**, *italic*, [[red]]...[[/red]] -> reportlab tags"""
    s = esc(str(s))
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<![\*\w])\*(?!\s)(.+?)(?<!\s)\*(?!\*)', r'<i>\1</i>', s)
    s = s.replace('\n', '<br/>')
    return s
def md_inline(s): return str(s).replace('\n', '<br>')

class Doc:
    def __init__(self): self.items = []
    def title(self, t, sub, note): self.items.append(('title', t, sub, note))
    def h1(self, t): self.items.append(('h1', t))
    def h2(self, t): self.items.append(('h2', t))
    def p(self, t): self.items.append(('p', t))
    def lead(self, t): self.items.append(('lead', t))
    def bullets(self, lst, numbered=False): self.items.append(('bul', lst, numbered))
    def table(self, caption, header, rows, widths, small=False, note=None, zebra=True, keep=False): self.items.append(('table', caption, header, rows, widths, small, note, zebra, keep))
    def fig(self, path, caption, width=7.0): self.items.append(('fig', path, caption, width))
    def box(self, title, paras): self.items.append(('box', title, paras))
    def pagebreak(self): self.items.append(('pb',))
    def space(self, h=4): self.items.append(('sp', h))

    # ---------------- PDF ----------------
    def to_pdf(self, path, footer_text):
        W, H = letter; M = 0.75*inch
        def on_page(c, d):
            c.saveState(); c.setFont('DV', 7); c.setFillColor(GREY)
            c.drawString(M, 0.45*inch, footer_text); c.drawRightString(W-M, 0.45*inch, f'Page {d.page}')
            c.setStrokeColor(RULE); c.setLineWidth(0.4); c.line(M, 0.6*inch, W-M, 0.6*inch); c.restoreState()
        doc = BaseDocTemplate(path, pagesize=letter, leftMargin=M, rightMargin=M, topMargin=0.7*inch, bottomMargin=0.78*inch, title='PSLN program: portfolio recommendation and next-step proposal', author='Portfolio analysis')
        doc.addPageTemplates([PageTemplate(id='main', frames=[Frame(M, 0.78*inch, W-2*M, H-0.7*inch-0.78*inch, id='f', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], onPage=on_page)])
        fl = []
        for it in self.items:
            k = it[0]
            if k == 'title':
                fl += [Paragraph(rl(it[1]), ST['title']), Paragraph(rl(it[2]), ST['subtitle']), Paragraph(rl(it[3]), ST['note'])]
            elif k == 'h1': fl += [CondPageBreak(1.3*inch), Paragraph(rl(it[1]), ST['h1'])]
            elif k == 'h2': fl += [Paragraph(rl(it[1]), ST['h2'])]
            elif k == 'p': fl.append(Paragraph(rl(it[1]), ST['p']))
            elif k == 'lead': fl.append(Paragraph(rl(it[1]), ST['lead']))
            elif k == 'bul':
                for i, b in enumerate(it[1]):
                    fl.append(Paragraph(rl(b), ST['num' if it[2] else 'bul'], bulletText=(f'{i+1}.' if it[2] else '•')))
                fl.append(Spacer(1, 3))
            elif k == 'table':
                _, cap, header, rows, widths, small, note, zebra, bfc = it
                cs, cb = (ST['cells'], ST['cellsb']) if small else (ST['cell'], ST['cellb'])
                data = [[Paragraph(rl(h), cb) for h in header]] + [[Paragraph(rl(c), cs) for c in r] for r in rows]
                t = Table(data, colWidths=[w*inch for w in widths], repeatRows=1, splitByRow=1)
                sty = [('BACKGROUND', (0,0), (-1,0), NAVY), ('VALIGN', (0,0), (-1,-1), 'TOP'), ('LINEBELOW', (0,0), (-1,-1), 0.3, RULE),
                       ('LEFTPADDING', (0,0), (-1,-1), 3.5), ('RIGHTPADDING', (0,0), (-1,-1), 3.5), ('TOPPADDING', (0,0), (-1,-1), 2.2), ('BOTTOMPADDING', (0,0), (-1,-1), 2.6)]
                if zebra:
                    for i in range(1, len(data)):
                        if i % 2 == 0: sty.append(('BACKGROUND', (0,i), (-1,i), LIGHT))
                t.setStyle(TableStyle(sty))
                tail = Paragraph(rl(note), ST['cap']) if note else Spacer(1, 7)
                if bfc:   # keep small tables whole
                    fl.append(KeepTogether(([Paragraph(rl(cap), ST['tcap'])] if cap else []) + [t, tail]))
                else:
                    if cap: fl += [CondPageBreak(1.25*inch), Paragraph(rl(cap), ST['tcap'])]
                    fl += [t, tail]
            elif k == 'fig':
                from PIL import Image as PI
                im = PI.open(it[1]); w = it[3]*inch; h = w*im.size[1]/im.size[0]
                fl.append(KeepTogether([Image(it[1], width=w, height=h), Paragraph(rl(it[2]), ST['cap'])]))
            elif k == 'box':
                inner = [Paragraph(rl(it[1]), ParagraphStyle('bt', parent=ST['box'], fontName='DV-B', textColor=NAVY, spaceAfter=4))] if it[1] else []
                for p_ in it[2]:
                    if isinstance(p_, tuple): inner.append(Paragraph(rl(p_[1]), ParagraphStyle('bb', parent=ST['box'], leftIndent=12, bulletIndent=2, bulletFontName='DV'), bulletText=p_[0]))
                    else: inner.append(Paragraph(rl(p_), ST['box']))
                t = Table([[inner]], colWidths=[7.0*inch])
                t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), LIGHT), ('BOX', (0,0), (-1,-1), 0.8, NAVY), ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8), ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 5)]))
                fl += [t, Spacer(1, 8)]
            elif k == 'pb': fl.append(PageBreak())
            elif k == 'sp': fl.append(Spacer(1, it[1]))
        doc.build(fl)

    # ---------------- Markdown ----------------
    def to_md(self, path, figdir_rel='figures'):
        out = []
        for it in self.items:
            k = it[0]
            if k == 'title': out += [f'# {it[1]}', '', f'*{it[2]}*', '', f'<sub>{md_inline(it[3])}</sub>', '']
            elif k == 'h1': out += ['', f'## {it[1]}', '']
            elif k == 'h2': out += ['', f'### {it[1]}', '']
            elif k == 'p': out += [md_inline(it[1]), '']
            elif k == 'lead': out += [f'**{md_inline(it[1]).replace("**","")}**', '']
            elif k == 'bul':
                for i, b in enumerate(it[1]): out.append((f'{i+1}. ' if it[2] else '- ') + md_inline(b))
                out.append('')
            elif k == 'table':
                _, cap, header, rows, widths, small, note, zebra, bfc = it
                if cap: out += [f'**{cap}**', '']
                out.append('| ' + ' | '.join(md_inline(h) for h in header) + ' |'); out.append('|' + '|'.join(['---']*len(header)) + '|')
                for r in rows: out.append('| ' + ' | '.join(md_inline(c).replace('|','\\|') for c in r) + ' |')
                out.append('')
                if note: out += [f'<sub>{md_inline(note)}</sub>', '']
            elif k == 'fig': out += [f'![{os.path.basename(it[1])}]({figdir_rel}/{os.path.basename(it[1])})', '', f'<sub>{md_inline(it[2])}</sub>', '']
            elif k == 'box':
                if it[1]: out.append(f'> **{it[1]}**  ')
                for p_ in it[2]:
                    out.append('> ' + (f'{p_[0]} {md_inline(p_[1])}' if isinstance(p_, tuple) else md_inline(p_)) + '  ')
                out.append('')
            elif k == 'pb': out += ['', '---', '']
        open(path, 'w').write('\n'.join(out))
