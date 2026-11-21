"""docmodel.py -- tiny document model rendered to (a) pandoc Markdown (-> DOCX) and (b) reportlab PDF.
Blocks:
  ('h1'|'h2'|'h3', text)
  ('p', text)                      inline **bold** and _italic_ supported
  ('small', text)                  small-print paragraph
  ('bullets', [text,...])
  ('numbered', [text,...])
  ('callout', text_or_list, colour)
  ('table', dict(header=[...], rows=[[...]], widths=[fractions], font=7.5, caption=str, zebra=True))
  ('figure', path, width_fraction, caption)
  ('pagebreak',)
"""
import re, html

# ---------------------------------------------------------------- Markdown
def _md_inline(t):
    t = str(t)
    t = t.replace('~', '≈') if False else t
    return t

def to_markdown(blocks, title, subtitle):
    out = [f"---\ntitle: \"{title}\"\nsubtitle: \"{subtitle}\"\n---\n"]
    for b in blocks:
        k = b[0]
        if k == 'h1': out.append(f"\n# {b[1]}\n")
        elif k == 'h2': out.append(f"\n## {b[1]}\n")
        elif k == 'h3': out.append(f"\n### {b[1]}\n")
        elif k in ('p', 'small'): out.append(f"\n{_md_inline(b[1])}\n")
        elif k == 'bullets': out.append("\n" + "\n".join(f"- {_md_inline(x)}" for x in b[1]) + "\n")
        elif k == 'numbered': out.append("\n" + "\n".join(f"{i+1}. {_md_inline(x)}" for i, x in enumerate(b[1])) + "\n")
        elif k == 'callout':
            items = b[1] if isinstance(b[1], list) else [b[1]]
            out.append("\n" + "\n>\n".join(f"> {_md_inline(x)}" for x in items) + "\n")
        elif k == 'table':
            d = b[1]; hdr = d['header']; rows = d['rows']; w = d.get('widths') or [1/len(hdr)]*len(hdr)
            if d.get('noheader'): hdr = ['Item', 'Detail'] if len(hdr) == 2 else hdr
            if d.get('caption'): out.append(f"\n**{d['caption']}**\n")
            dashes = [max(3, int(round(x*120))) for x in w]
            def cell(x): return _md_inline(str(x)).replace('|', '/').replace('\n', ' ')
            lines = ["| " + " | ".join(cell(h) for h in hdr) + " |",
                     "|" + "|".join("-"*n for n in dashes) + "|"]
            for r in rows: lines.append("| " + " | ".join(cell(x) for x in r) + " |")
            # force long-line behaviour so pandoc wraps and honours relative widths
            out.append("\n" + "\n".join(lines) + "\n")
            if d.get('note'): out.append(f"\n_{d['note']}_\n")
        elif k == 'figure':
            out.append(f"\n![{b[3]}]({b[1]}){{width={int(b[2]*100)}%}}\n")
        elif k == 'pagebreak':
            out.append("\n```{=openxml}\n<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>\n```\n")
    return "\n".join(out)

# ---------------------------------------------------------------- reportlab
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
                                Image, PageBreak, KeepTogether, ListFlowable, ListItem)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('DV', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DVS', '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily('DV', normal='DV', bold='DVB', italic='DV', boldItalic='DVB')

BASE = ParagraphStyle('base', fontName='DV', fontSize=9, leading=12.2, spaceAfter=4)
ST = {
 'h1': ParagraphStyle('h1', parent=BASE, fontName='DVB', fontSize=14, leading=17, spaceBefore=10, spaceAfter=6, textColor=colors.HexColor('#1f3a5f'), keepWithNext=1),
 'h2': ParagraphStyle('h2', parent=BASE, fontName='DVB', fontSize=11.2, leading=14, spaceBefore=8, spaceAfter=4, textColor=colors.HexColor('#1f3a5f'), keepWithNext=1),
 'h3': ParagraphStyle('h3', parent=BASE, fontName='DVB', fontSize=9.6, leading=12.5, spaceBefore=6, spaceAfter=3, keepWithNext=1),
 'p': BASE,
 'small': ParagraphStyle('small', parent=BASE, fontSize=7.6, leading=9.8, textColor=colors.HexColor('#333333')),
 'bullet': ParagraphStyle('bullet', parent=BASE, leftIndent=0, spaceAfter=2),
 'cap': ParagraphStyle('cap', parent=BASE, fontName='DVB', fontSize=8.4, leading=10.5, spaceBefore=4, spaceAfter=3, keepWithNext=1),
 'figcap': ParagraphStyle('figcap', parent=BASE, fontSize=7.8, leading=10, textColor=colors.HexColor('#333333')),
}
def _rl_inline(t):
    t = html.escape(str(t), quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'(?<![A-Za-z0-9])_(.+?)_(?![A-Za-z0-9])', r'<i>\1</i>', t)
    return t

def _cellstyle(font, bold=False):
    return ParagraphStyle('c', parent=BASE, fontName='DVB' if bold else 'DV', fontSize=font, leading=font*1.22, spaceAfter=0)

def to_pdf(blocks, path, title, subtitle, header_text):
    doc = BaseDocTemplate(path, pagesize=A4, leftMargin=1.6*cm, rightMargin=1.6*cm, topMargin=1.7*cm, bottomMargin=1.5*cm,
                          title=title, author='Program analysis')
    W = A4[0] - 3.2*cm
    def onpage(c, d):
        c.saveState(); c.setFont('DV', 7); c.setFillColor(colors.HexColor('#666666'))
        c.drawString(1.6*cm, A4[1]-1.1*cm, header_text)
        c.drawRightString(A4[0]-1.6*cm, 1.0*cm, f"page {d.page}")
        c.restoreState()
    doc.addPageTemplates([PageTemplate(id='p', frames=[Frame(1.6*cm, 1.5*cm, W, A4[1]-3.2*cm, id='f')], onPage=onpage)])
    story = []
    story.append(Paragraph(_rl_inline(title), ParagraphStyle('t', parent=BASE, fontName='DVB', fontSize=17, leading=21, textColor=colors.HexColor('#1f3a5f'))))
    story.append(Paragraph(_rl_inline(subtitle), ParagraphStyle('st', parent=BASE, fontSize=9.5, leading=12.5, textColor=colors.HexColor('#444444'), spaceAfter=8)))
    for b in blocks:
        k = b[0]
        if k in ('h1', 'h2', 'h3', 'p', 'small'):
            story.append(Paragraph(_rl_inline(b[1]), ST[k]))
        elif k in ('bullets', 'numbered'):
            items = [ListItem(Paragraph(_rl_inline(x), ST['bullet']), leftIndent=12) for x in b[1]]
            story.append(ListFlowable(items, bulletType='bullet' if k == 'bullets' else '1', start=None if k=='bullets' else 1,
                                      bulletFontName='DV', bulletFontSize=8, leftIndent=12, bulletDedent=9))
            story.append(Spacer(1, 3))
        elif k == 'callout':
            items = b[1] if isinstance(b[1], list) else [b[1]]
            col = b[2] if len(b) > 2 else '#eaf2fb'
            paras = [Paragraph(_rl_inline(x), ParagraphStyle('co', parent=BASE, fontSize=9, leading=12, spaceAfter=3)) for x in items]
            t = Table([[paras]], colWidths=[W])
            t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor(col)), ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#1f3a5f')),
                                   ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8), ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 4)]))
            story.append(t); story.append(Spacer(1, 6))
        elif k == 'table':
            d = b[1]; f = d.get('font', 7.4); hdr = d['header']; rows = d['rows']
            w = d.get('widths') or [1/len(hdr)]*len(hdr); s = sum(w); cw = [W*x/s for x in w]
            nohdr = d.get('noheader', False)
            data = ([] if nohdr else [[Paragraph(_rl_inline(h), _cellstyle(f, True)) for h in hdr]]) + \
                   [[Paragraph(_rl_inline(x), _cellstyle(f)) for x in r] for r in rows]
            t = Table(data, colWidths=cw, repeatRows=0 if nohdr else 1)
            sty = [('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#9aa5b1'))] + \
                  ([('BACKGROUND', (0,0), (0,-1), colors.HexColor('#eef2f7'))] if nohdr else [('BACKGROUND', (0,0), (-1,0), colors.HexColor('#dbe5f1'))]) + [
                   ('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 3), ('RIGHTPADDING', (0,0), (-1,-1), 3),
                   ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2)]
            if d.get('zebra', True):
                for i in range(1, len(data)):
                    if i % 2 == 0: sty.append(('BACKGROUND', (0,i), (-1,i), colors.HexColor('#f5f7fa')))
            for (r, c0, c1, col) in d.get('highlight', []):
                sty.append(('BACKGROUND', (c0, r), (c1, r), colors.HexColor(col)))
            t.setStyle(TableStyle(sty))
            if d.get('caption'): story.append(Paragraph(_rl_inline(d['caption']), ST['cap']))
            story.append(t)
            if d.get('note'): story.append(Paragraph(_rl_inline(d['note']), ST['figcap']))
            story.append(Spacer(1, 6))
        elif k == 'figure':
            from PIL import Image as PI
            im = PI.open(b[1]); ar = im.size[1]/im.size[0]
            wd = W*b[2]; ht = wd*ar
            maxh = A4[1]-5.2*cm
            if ht > maxh: ht = maxh; wd = ht/ar
            story.append(KeepTogether([Image(b[1], width=wd, height=ht), Paragraph(_rl_inline(b[3]), ST['figcap'])]))
            story.append(Spacer(1, 6))
        elif k == 'pagebreak':
            story.append(PageBreak())
    doc.build(story)
