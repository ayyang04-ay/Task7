# -*- coding: utf-8 -*-
import pandas as pd, os, re, sys, importlib
sys.path.insert(0, '/tmp/work')
import content; importlib.reload(content)
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, Image,
                                PageBreak, KeepTogether, ListFlowable, ListItem)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib
FD = os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data', 'fonts', 'ttf')
pdfmetrics.registerFont(TTFont('DV', os.path.join(FD, 'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DVB', os.path.join(FD, 'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFont(TTFont('DVI', os.path.join(FD, 'DejaVuSans-Oblique.ttf')))
pdfmetrics.registerFont(TTFont('DVBI', os.path.join(FD, 'DejaVuSans-BoldOblique.ttf')))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily('DV', normal='DV', bold='DVB', italic='DVI', boldItalic='DVBI')

OUT = '/tmp/outputs'; FIGD = '/tmp/outputs/figures'
st = {
 'title': ParagraphStyle('title', fontName='DVB', fontSize=15.5, leading=19, spaceAfter=4, textColor=colors.HexColor('#0b2e59')),
 'sub': ParagraphStyle('sub', fontName='DV', fontSize=10, leading=13, spaceAfter=6, textColor=colors.HexColor('#333333')),
 'meta': ParagraphStyle('meta', fontName='DVI', fontSize=7.6, leading=10, spaceAfter=10, textColor=colors.HexColor('#555555')),
 'h1': ParagraphStyle('h1', fontName='DVB', fontSize=12.5, leading=16, spaceBefore=10, spaceAfter=5, textColor=colors.HexColor('#0b2e59')),
 'h2': ParagraphStyle('h2', fontName='DVB', fontSize=10.5, leading=13, spaceBefore=6, spaceAfter=3),
 'p': ParagraphStyle('p', fontName='DV', fontSize=8.9, leading=12.2, spaceAfter=5),
 'b': ParagraphStyle('b', fontName='DV', fontSize=8.9, leading=12.0),
 'call': ParagraphStyle('call', fontName='DV', fontSize=9.6, leading=13.2, textColor=colors.HexColor('#0b2e59')),
 'cell': ParagraphStyle('cell', fontName='DV', fontSize=7.4, leading=9.0),
 'cellh': ParagraphStyle('cellh', fontName='DVB', fontSize=7.4, leading=9.0, textColor=colors.white),
}
def cellstyle(size):
    return (ParagraphStyle('c%s'%size, fontName='DV', fontSize=size, leading=size*1.22),
            ParagraphStyle('ch%s'%size, fontName='DVB', fontSize=size, leading=size*1.22, textColor=colors.white))

def esc(t):
    # allow our simple inline tags; escape stray ampersands
    t = re.sub(r'&(?!amp;|lt;|gt;|#)', '&amp;', t)
    # protect '<' that are not tags
    t = re.sub(r'<(?!/?(b|i|super|sub|font|br)\b)', '&lt;', t)
    return t

def mk_table(header, rows, widths, size):
    cs, chs = cellstyle(size)
    data = [[Paragraph(esc(h), chs) for h in header]] + [[Paragraph(esc(str(c)), cs) for c in r] for r in rows]
    tw = [w*cm for w in widths] if widths else None
    t = Table(data, colWidths=tw, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0b2e59')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#b0b0b0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f2f5f9')]),
        ('LEFTPADDING', (0,0), (-1,-1), 3), ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2)]))
    return t

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('DV', 7)
    canvas.setFillColor(colors.HexColor('#777777'))
    canvas.drawString(1.6*cm, 1.0*cm, 'PSLN program | portfolio review proposal | 1 Nov 2026 | refs: E# = Appendix A, I-## = Appendix B')
    canvas.drawRightString(A4[0]-1.6*cm, 1.0*cm, f'page {doc.page}')
    canvas.restoreState()

def build_pdf(path):
    doc = BaseDocTemplate(path, pagesize=A4, leftMargin=1.6*cm, rightMargin=1.6*cm, topMargin=1.4*cm, bottomMargin=1.6*cm,
                          title=content.TITLE, author='Portfolio analysis', subject=content.SUBTITLE)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='f')
    doc.addPageTemplates([PageTemplate(id='p', frames=[frame], onPage=footer)])
    el = [Paragraph(content.TITLE, st['title']), Paragraph(content.SUBTITLE, st['sub']), Paragraph(esc(content.META), st['meta'])]
    EV = pd.read_csv('/tmp/work/evidence_register.csv'); IR = pd.read_csv('/tmp/work/integrity_register.csv')
    for kind, pl in content.S:
        if kind=='h1': el.append(Paragraph(esc(pl), st['h1']))
        elif kind=='h2': el.append(Paragraph(esc(pl), st['h2']))
        elif kind=='p': el.append(Paragraph(esc(pl), st['p']))
        elif kind=='bullets':
            el.append(ListFlowable([ListItem(Paragraph(esc(x), st['b']), leftIndent=10, value='•') for x in pl],
                                   bulletType='bullet', start='•', leftIndent=12, bulletFontName='DV', bulletFontSize=8, spaceAfter=4))
            el.append(Spacer(1,3))
        elif kind=='callout':
            t = Table([[Paragraph(esc(pl), st['call'])]], colWidths=[doc.width])
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#e8f0fa')),('BOX',(0,0),(-1,-1),1.2,colors.HexColor('#0b2e59')),
                                   ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
            el += [t, Spacer(1,6)]
        elif kind=='table':
            h, rows, w, size = pl
            el += [mk_table(h, rows, w, size), Spacer(1,6)]
        elif kind=='fig':
            fpth, cap, width = pl
            from PIL import Image as PI
            im = PI.open(os.path.join(FIGD, fpth)); ratio = im.size[1]/im.size[0]
            wcm = min(width, doc.width/cm)
            el += [Image(os.path.join(FIGD, fpth), width=wcm*cm, height=wcm*ratio*cm), Spacer(1,6)]
        elif kind=='pagebreak': el.append(PageBreak())
        elif kind=='evidence_table':
            rows = [[r.id, r.area, r.claim, r.value, f'{r.blocks}<br/><font size="6">{r.cells}</font>', r.method, r.tier] for r in EV.itertuples()]
            el.append(mk_table(['ID','Area','Claim','Result','Blocks / cells','Method','Tier'], rows, [0.9,2.0,3.0,5.1,2.9,2.1,0.8], 6.3))
        elif kind=='integrity_table':
            rows = [[r.id, r.severity, r.blocks, r.finding, r.evidence_cells, r.decision_impact] for r in IR.itertuples()]
            el.append(mk_table(['ID','Severity','Blocks','Finding','Evidence (cells, statistics)','Decision impact'], rows, [0.9,1.3,2.3,4.1,5.0,3.2], 6.3))
    doc.build(el)

def md_clean(t):
    t = t.replace('<super>2+</super>','2+').replace('<super>','^').replace('</super>','')
    t = re.sub(r'</?b>','**',t); t = re.sub(r'</?i>','*',t); t = t.replace('<br/>',' ')
    t = re.sub(r'<font[^>]*>','',t).replace('</font>','')
    return t

def build_md(path):
    EV = pd.read_csv('/tmp/work/evidence_register.csv'); IR = pd.read_csv('/tmp/work/integrity_register.csv')
    L = [f'# {content.TITLE}', f'### {content.SUBTITLE}', f'*{content.META}*', '']
    for kind, pl in content.S:
        if kind=='h1': L += ['', f'## {md_clean(pl)}', '']
        elif kind=='h2': L += [f'### {md_clean(pl)}', '']
        elif kind=='p': L += [md_clean(pl), '']
        elif kind=='bullets': L += [f'- {md_clean(x)}' for x in pl] + ['']
        elif kind=='callout': L += [f'> {md_clean(pl)}', '']
        elif kind=='table':
            h, rows, w, size = pl
            L += ['| ' + ' | '.join(md_clean(x) for x in h) + ' |', '|' + '---|'*len(h)]
            L += ['| ' + ' | '.join(md_clean(str(c)).replace('|','/') for c in r) + ' |' for r in rows] + ['']
        elif kind=='fig': L += [f'![{pl[0]}](figures/{pl[0]})', '']
        elif kind=='evidence_table':
            L += ['| ID | Area | Claim | Result | Blocks | Cells | Method | Tier |', '|---|---|---|---|---|---|---|---|']
            L += [f'| {r.id} | {r.area} | {md_clean(r.claim)} | {md_clean(r.value)} | {r.blocks} | {r.cells} | {r.method} | {r.tier} |' for r in EV.itertuples()] + ['']
        elif kind=='integrity_table':
            L += ['| ID | Severity | Blocks | Finding | Evidence | Decision impact |', '|---|---|---|---|---|---|']
            L += [f'| {r.id} | {r.severity} | {r.blocks} | {md_clean(r.finding)} | {md_clean(r.evidence_cells)} | {md_clean(r.decision_impact)} |' for r in IR.itertuples()] + ['']
    open(path,'w').write('\n'.join(L))

if __name__ == '__main__':
    build_pdf(f'{OUT}/PSLN_portfolio_proposal.pdf')
    build_md(f'{OUT}/PSLN_portfolio_proposal.md')
    print('built')
