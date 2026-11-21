import json, sys, os
from xml.sax.saxutils import escape
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, ListFlowable, ListItem, CondPageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage

FD = '/opt/conda/envs/core/lib/python3.11/site-packages/matplotlib/mpl-data/fonts/ttf/'
for name, f in [('DV','DejaVuSans.ttf'),('DV-B','DejaVuSans-Bold.ttf'),('DV-I','DejaVuSans-Oblique.ttf'),('DV-BI','DejaVuSans-BoldOblique.ttf'),('DVM','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name, FD+f))
pdfmetrics.registerFontFamily('DV', normal='DV', bold='DV-B', italic='DV-I', boldItalic='DV-BI')

NAVY = colors.HexColor('#1F3F6E'); GREY = colors.HexColor('#555555'); HDR = colors.HexColor('#DCE6F2'); LINE = colors.HexColor('#A6A6A6')
S = {
 'title': ParagraphStyle('title', fontName='DV-B', fontSize=17, leading=21, textColor=NAVY, spaceAfter=3),
 'subtitle': ParagraphStyle('subtitle', fontName='DV', fontSize=9.5, leading=12, textColor=GREY, spaceAfter=8),
 'h1': ParagraphStyle('h1', fontName='DV-B', fontSize=13.5, leading=17, textColor=NAVY, spaceBefore=13, spaceAfter=5, keepWithNext=1),
 'h2': ParagraphStyle('h2', fontName='DV-B', fontSize=10.8, leading=14, textColor=NAVY, spaceBefore=9, spaceAfter=4, keepWithNext=1),
 'h3': ParagraphStyle('h3', fontName='DV-B', fontSize=9.6, leading=12.5, textColor=NAVY, spaceBefore=7, spaceAfter=3, keepWithNext=1),
 'body': ParagraphStyle('body', fontName='DV', fontSize=8.8, leading=12.1, spaceAfter=5),
 'bodykeep': ParagraphStyle('bodykeep', fontName='DV', fontSize=8.8, leading=12.1, spaceAfter=5, keepWithNext=1),
 'bullet': ParagraphStyle('bullet', fontName='DV', fontSize=8.8, leading=12.1, spaceAfter=2.5),
 'cell': ParagraphStyle('cell', fontName='DV', fontSize=6.9, leading=8.7),
 'cellc': ParagraphStyle('cellc', fontName='DV', fontSize=6.9, leading=8.7, alignment=TA_CENTER),
 'cellh': ParagraphStyle('cellh', fontName='DV-B', fontSize=6.9, leading=8.7),
 'cellhc': ParagraphStyle('cellhc', fontName='DV-B', fontSize=6.9, leading=8.7, alignment=TA_CENTER),
 'caption': ParagraphStyle('caption', fontName='DV', fontSize=7.6, leading=10, textColor=colors.HexColor('#333333'), spaceBefore=3, spaceAfter=9),
}

def inl(xs):
    out = []
    for x in xs:
        t = x['t']; c = x.get('c')
        if t == 'Str': out.append(escape(c))
        elif t in ('Space','SoftBreak'): out.append(' ')
        elif t == 'LineBreak': out.append('<br/>')
        elif t == 'Strong': out.append('<b>'+inl(c)+'</b>')
        elif t == 'Emph': out.append('<i>'+inl(c)+'</i>')
        elif t == 'Code': out.append('<font face="DVM" size="-0.6">'+escape(c[1])+'</font>')
        elif t == 'Quoted': out.append('“'+inl(c[1])+'”')
        elif t == 'Superscript': out.append('<super>'+inl(c)+'</super>')
        elif t == 'Subscript': out.append('<sub>'+inl(c)+'</sub>')
        elif t == 'Link': out.append(inl(c[1]))
        elif t == 'Span': out.append(inl(c[1]))
        elif t == 'Image': pass
        elif t in ('RawInline','Note'): pass
        else: raise ValueError('inline '+t)
    return ''.join(out)

def find_image(xs):
    for x in xs:
        if x['t'] == 'Image': return x
        if isinstance(x.get('c'), list):
            for y in x['c']:
                if isinstance(y, dict) and y.get('t') == 'Image': return y
    return None

class Builder:
    def __init__(self, width):
        self.W = width; self.story = []
    def flow(self, b, level=0, keep=False):
        """flowables for one block, built in a scratch builder"""
        sub = Builder(self.W)
        if keep and b['t'] == 'Para':
            sub.story.append(Paragraph(inl(b['c']), S['bodykeep']))
        else:
            sub.block(b, level)
        out = []
        for f in sub.story:                      # flatten nested KeepTogether and drop conditional breaks inside groups
            if isinstance(f, CondPageBreak): continue
            if isinstance(f, KeepTogether): out.extend(f._content)
            else: out.append(f)
        return out
    @staticmethod
    def small_table(b, max_rows=16):
        if b['t'] != 'Table': return False
        return sum(len(tb[3]) for tb in b['c'][4]) <= max_rows
    @staticmethod
    def lead_in(b):
        return b['t'] == 'Para' and len(inl(b['c'])) < 260
    def blocks(self, bs, level=0):
        i = 0; n = len(bs)
        while i < n:
            b = bs[i]
            if b['t'] == 'Header':
                group = self.flow(b, level); j = i + 1
                while j < n and bs[j]['t'] == 'Header':          # consecutive headings stay together
                    group += self.flow(bs[j], level); j += 1
                if j < n and self.lead_in(bs[j]) and j + 1 < n and bs[j+1]['t'] in ('Table', 'BulletList', 'OrderedList'):
                    group += self.flow(bs[j], level, keep=True); j += 1
                if j < n and (self.small_table(bs[j]) or bs[j]['t'] in ('Para', 'Figure')):
                    group += self.flow(bs[j], level); j += 1
                    if bs[j-1]['t'] == 'Para' and j < n and bs[j]['t'] == 'Figure':
                        group += self.flow(bs[j], level); j += 1
                if b['c'][0] == 1 and inl(b['c'][2]).startswith('Appendix A'):
                    self.story.append(PageBreak())
                self.story.append(KeepTogether(group)); i = j; continue
            if self.lead_in(b) and i + 1 < n and bs[i+1]['t'] in ('Table', 'BulletList', 'OrderedList'):
                if self.small_table(bs[i+1]):
                    self.story.append(KeepTogether(self.flow(b, level, keep=True) + self.flow(bs[i+1], level))); i += 2; continue
                self.story.append(Paragraph(inl(b['c']), S['bodykeep'])); i += 1; continue
            if self.small_table(b):
                self.story.append(KeepTogether(self.flow(b, level))); i += 1; continue
            self.block(b, level); i += 1
    def para_in_cell(self, blocks, style):
        txt = []
        for b in blocks:
            if b['t'] in ('Plain','Para'): txt.append(inl(b['c']))
            else: raise ValueError('cell block '+b['t'])
        return Paragraph('<br/>'.join(txt) if txt else '', style)
    def block(self, b, level=0):
        t = b['t']; c = b.get('c')
        if t == 'Header':
            lvl = c[0]
            self.story.append(CondPageBreak((34 if lvl == 1 else 28)*mm))
            self.story.append(Paragraph(inl(c[2]), S['h%d' % min(lvl,3)]))
        elif t in ('Para','Plain'):
            self.story.append(Paragraph(inl(c), S['body']))
        elif t == 'BulletList':
            ind = 13 * (level + 1)
            st = ParagraphStyle('bl%d' % level, parent=S['bullet'], leftIndent=ind, bulletIndent=ind - 10, bulletFontName='DV', bulletFontSize=8.8, bulletColor=NAVY)
            for it in c:
                first = True
                for bb in it:
                    if bb['t'] in ('Plain','Para'):
                        self.story.append(Paragraph(inl(bb['c']), st, bulletText='•' if first else None)); first = False
                    else:
                        self.block(bb, level + 1)
            self.story.append(Spacer(1, 3))
        elif t == 'OrderedList':
            ind = 15 * (level + 1)
            st = ParagraphStyle('ol%d' % level, parent=S['bullet'], leftIndent=ind, bulletIndent=ind - 15, bulletFontName='DV-B', bulletFontSize=8.8, spaceAfter=3.5)
            for k, it in enumerate(c[1], start=c[0][0]):
                first = True
                for bb in it:
                    if bb['t'] in ('Plain','Para'):
                        self.story.append(Paragraph(inl(bb['c']), st, bulletText=('%d.' % k) if first else None)); first = False
            self.story.append(Spacer(1, 3))
        elif t == 'Figure':
            cap_blocks = c[1][1]; content = c[2]
            img = None
            for bb in content:
                if bb['t'] in ('Plain','Para'):
                    img = find_image(bb['c'])
            attr, alt, (src, _title) = img['c']
            pct = 1.0
            for k, v in attr[2]:
                if k == 'width' and v.endswith('%'): pct = float(v[:-1])/100
            w0, h0 = PILImage.open(src).size
            w = self.W * pct; h = w * h0 / w0
            maxh = 225*mm
            if h > maxh: w = w * maxh / h; h = maxh
            im = Image(src, width=w, height=h); im.hAlign = 'CENTER'
            cap = Paragraph(' '.join(inl(bb['c']) for bb in cap_blocks), S['caption'])
            self.story.append(KeepTogether([Spacer(1, 4), im, cap]))
        elif t == 'Table':
            attr, caption, colspecs, thead, tbodies, tfoot = c
            n = len(colspecs)
            ws = [cs[1].get('c') if cs[1]['t'] == 'ColWidth' else None for cs in colspecs]
            if any(w is None for w in ws): ws = [1.0/n]*n
            tot = sum(ws); colw = [self.W * w / tot for w in ws]
            aligns = [cs[0]['t'] for cs in colspecs]
            data = []; nhead = 0
            for row in thead[1]:
                cells = row[1]
                data.append([self.para_in_cell(cell[4], S['cellhc'] if aligns[j]=='AlignCenter' else S['cellh']) for j, cell in enumerate(cells)]); nhead += 1
            header_empty = all(len(cell[4]) == 0 for row in thead[1] for cell in row[1])
            if header_empty: data = []; nhead = 0
            for tb in tbodies:
                for row in tb[3]:
                    cells = row[1]
                    data.append([self.para_in_cell(cell[4], S['cellc'] if aligns[j]=='AlignCenter' else S['cell']) for j, cell in enumerate(cells)])
            st = [('GRID', (0,0), (-1,-1), 0.4, LINE), ('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 3), ('RIGHTPADDING', (0,0), (-1,-1), 3),
                  ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2.5)]
            if nhead: st += [('BACKGROUND', (0,0), (-1,nhead-1), HDR), ('VALIGN', (0,0), (-1,nhead-1), 'BOTTOM')]
            tb = Table(data, colWidths=colw, repeatRows=nhead, splitByRow=1)
            tb.setStyle(TableStyle(st)); tb.hAlign = 'LEFT'
            self.story.append(Spacer(1, 2)); self.story.append(tb); self.story.append(Spacer(1, 7))
        elif t == 'BlockQuote':
            self.blocks(c, level+1)
        elif t == 'HorizontalRule':
            self.story.append(Spacer(1, 6))
        elif t == 'RawBlock':
            if 'w:br' in c[1] and 'page' in c[1]: self.story.append(PageBreak())
        elif t == 'Div':
            self.blocks(c[1], level)
        else:
            raise ValueError('block '+t)

def meta_inl(m):
    return inl(m['c']) if m['t'] == 'MetaInlines' else ''

def build(json_path, out_path, short_title):
    d = json.load(open(json_path))
    LM = RM = 17*mm; TM = 17*mm; BM = 16*mm
    W = A4[0] - LM - RM
    def on_page(canv, doc):
        canv.saveState(); canv.setFont('DV', 7); canv.setFillColor(GREY)
        canv.drawString(LM, 9*mm, short_title); canv.drawRightString(A4[0]-RM, 9*mm, 'Page %d' % doc.page)
        canv.setStrokeColor(LINE); canv.setLineWidth(0.3); canv.line(LM, 12*mm, A4[0]-RM, 12*mm)
        canv.restoreState()
    doc = BaseDocTemplate(out_path, pagesize=A4, leftMargin=LM, rightMargin=RM, topMargin=TM, bottomMargin=BM, title=meta_inl(d['meta']['title']).replace('&amp;','&'), author='Portfolio analysis')
    doc.addPageTemplates([PageTemplate(id='p', frames=[Frame(LM, BM, W, A4[1]-TM-BM, id='f', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], onPage=on_page)])
    b = Builder(W)
    b.story.append(Paragraph(meta_inl(d['meta']['title']), S['title']))
    if 'subtitle' in d['meta']: b.story.append(Paragraph(meta_inl(d['meta']['subtitle']), S['subtitle']))
    b.blocks(d['blocks'])
    doc.build(b.story)
    return doc.page

if __name__ == '__main__':
    n = build(sys.argv[1], sys.argv[2], sys.argv[3])
    print('pages:', n)
