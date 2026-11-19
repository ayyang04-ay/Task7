"""Render proposal.md to DOCX (pandoc) and PDF (reportlab) with identical content."""
import re, os, subprocess, zipfile, shutil, html
SRC = '/tmp/work/proposal.md'
OUTD = '/tmp/outputs'
md = open(SRC, encoding='utf-8').read()

# ---------------- shared: proportional pipe-table separators ----------------
def split_row(line):
    s = line.strip()
    if s.startswith('|'): s = s[1:]
    if s.endswith('|'): s = s[:-1]
    return [c.strip() for c in s.split('|')]

def strip_md(c):
    return re.sub(r'[*`^]', '', c)

def col_weights(rows, total_chars=118):
    """relative widths: content-driven, but never narrower than the longest word in the column"""
    n = len(rows[0]); meas = []; mins = []
    for j in range(n):
        col = [strip_md(r[j]) if j < len(r) else '' for r in rows]
        lens = sorted(len(c) for c in col)
        mx = lens[-1]; p90 = lens[int(0.9 * (len(lens) - 1))]
        meas.append((0.5 * min(mx, 260) + 0.5 * min(p90, 260)) ** 0.8 + 1)
        words = [w for c in col[1:] for w in re.split(r'[\s/]+', c) if w]
        hwords = [w for w in re.split(r'[\s/]+', col[0]) if w]
        mw = max([len(w) for w in words] + [3]); hw = max([len(w) for w in hwords] + [3]) * 1.12
        mins.append((max(mw, hw) + 1.5) / total_chars)
    w = [m / sum(meas) for m in meas]
    for _ in range(20):
        w = [max(wi, mi) for wi, mi in zip(w, mins)]
        s = sum(w); w = [wi / s for wi in w]
    return w

def parse_blocks(text):
    """Yield blocks: ('h', level, text) ('p', text) ('ul', [(indent, text)]) ('ol', [...]) ('table', rows) ('img', cap, path) ('meta', dict)"""
    lines = text.split('\n'); i = 0; blocks = []
    if lines[0].strip() == '---':
        j = lines.index('---', 1); meta = {}
        for l in lines[1:j]:
            k, v = l.split(':', 1); meta[k.strip()] = v.strip().strip('"')
        blocks.append(('meta', meta)); i = j + 1
    while i < len(lines):
        l = lines[i]
        if not l.strip():
            i += 1; continue
        m = re.match(r'^(#{1,3}) (.*)', l)
        if m:
            blocks.append(('h', len(m.group(1)), m.group(2))); i += 1; continue
        m = re.match(r'^!\[(.*)\]\((.*)\)', l.strip())
        if m:
            blocks.append(('img', m.group(1), m.group(2))); i += 1; continue
        if l.lstrip().startswith('|'):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith('|'):
                r = split_row(lines[i])
                if not all(re.fullmatch(r':?-{3,}:?', c) for c in r):
                    rows.append(r)
                i += 1
            blocks.append(('table', rows)); continue
        if re.match(r'^\s*(- |\d+\. )', l):
            items = []
            while i < len(lines) and lines[i].strip():
                mm = re.match(r'^(\s*)(- |(\d+)\. )(.*)', lines[i])
                if mm:
                    items.append([len(mm.group(1)), mm.group(4), bool(mm.group(3))])
                else:  # continuation line
                    items[-1][1] += ' ' + lines[i].strip()
                i += 1
            blocks.append(('list', items)); continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#{1,3} |\s*\||!\[|\s*- |\s*\d+\. )', lines[i]):
            para.append(lines[i].strip()); i += 1
        blocks.append(('p', ' '.join(para)))
    return blocks

blocks = parse_blocks(md)

# ---------------- DOCX via pandoc ----------------
def md_with_widths(text):
    out = []; lines = text.split('\n'); i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith('|'):
            tbl = []
            while i < len(lines) and lines[i].lstrip().startswith('|'):
                tbl.append(lines[i]); i += 1
            rows = [split_row(l) for l in tbl if not all(re.fullmatch(r':?-{3,}:?', c) for c in split_row(l))]
            w = col_weights(rows, total_chars=100)
            sep = '|' + '|'.join('-' * max(3, int(round(x * 120))) for x in w) + '|'
            out.append(tbl[0]); out.append(sep); out.extend(tbl[2:])
            continue
        l = lines[i]
        m = re.match(r'^!\[(.*)\]\((.*)\)\s*$', l.strip())
        if m:
            l = f'![{m.group(1)}]({m.group(2)}){{width=6.5in}}'
        out.append(l); i += 1
    return '\n'.join(out)

tmp_md = '/tmp/work/proposal_docx.md'
open(tmp_md, 'w', encoding='utf-8').write(md_with_widths(md))
docx = f'{OUTD}/PSLN_portfolio_proposal.docx'
subprocess.run(['micromamba', 'run', '-n', 'genomics', 'pandoc', tmp_md, '-f', 'markdown+pipe_tables', '-t', 'docx', '--columns=80',
                '-o', docx], check=True)
# post-process: table borders + smaller table font + header shading
z = zipfile.ZipFile(docx); files = {n: z.read(n) for n in z.namelist()}; z.close()
doc = files['word/document.xml'].decode('utf-8')
borders = ('<w:tblBorders><w:top w:val="single" w:sz="4" w:space="0" w:color="999999"/><w:left w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
           '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="999999"/><w:right w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
           '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="999999"/><w:insideV w:val="single" w:sz="4" w:space="0" w:color="999999"/></w:tblBorders>')
doc = re.sub(r'(<w:tblPr>)', r'\1' + borders, doc)
files['word/document.xml'] = doc.encode('utf-8')
sty = files['word/styles.xml'].decode('utf-8')
# compact table text: set Compact style size 8.5pt if present; body text 10pt
sty = sty.replace('<w:style w:type="paragraph" w:customStyle="1" w:styleId="Compact">',
                  '<w:style w:type="paragraph" w:customStyle="1" w:styleId="Compact">')
sty = re.sub(r'(<w:style w:type="paragraph" w:customStyle="1" w:styleId="Compact">.*?<w:rPr>)', r'\1<w:sz w:val="17"/><w:szCs w:val="17"/>', sty, flags=re.S) \
      if re.search(r'w:styleId="Compact">.*?<w:rPr>', sty, flags=re.S) else sty
files['word/styles.xml'] = sty.encode('utf-8')
with zipfile.ZipFile(docx, 'w', zipfile.ZIP_DEFLATED) as zo:
    for n, b in files.items():
        zo.writestr(n, b)
print('DOCX written', docx, os.path.getsize(docx))

# ---------------- PDF via reportlab ----------------
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, ListFlowable, ListItem)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
FD = '/opt/conda/envs/chem/lib/python3.11/site-packages/matplotlib/mpl-data/fonts/ttf/'
pdfmetrics.registerFont(TTFont('DV', FD + 'DejaVuSans.ttf')); pdfmetrics.registerFont(TTFont('DVB', FD + 'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DVI', FD + 'DejaVuSans-Oblique.ttf')); pdfmetrics.registerFont(TTFont('DVBI', FD + 'DejaVuSans-BoldOblique.ttf'))
pdfmetrics.registerFont(TTFont('DVM', FD + 'DejaVuSansMono.ttf'))
addMapping('DV', 0, 0, 'DV'); addMapping('DV', 1, 0, 'DVB'); addMapping('DV', 0, 1, 'DVI'); addMapping('DV', 1, 1, 'DVBI')
ss = getSampleStyleSheet()
body = ParagraphStyle('body', parent=ss['Normal'], fontName='DV', fontSize=9, leading=12.2, spaceAfter=4)
h1 = ParagraphStyle('h1', parent=body, fontName='DVB', fontSize=13, leading=16, spaceBefore=10, spaceAfter=6, textColor=colors.HexColor('#1f4e79'), keepWithNext=1)
h2 = ParagraphStyle('h2', parent=body, fontName='DVB', fontSize=10.5, leading=13, spaceBefore=8, spaceAfter=4, textColor=colors.HexColor('#1f4e79'), keepWithNext=1)
li = ParagraphStyle('li', parent=body, spaceAfter=1.2, leading=11.6)
title = ParagraphStyle('title', parent=body, fontName='DVB', fontSize=15, leading=19, spaceAfter=4, textColor=colors.HexColor('#1f4e79'))
subtitle = ParagraphStyle('sub', parent=body, fontName='DVI', fontSize=8.5, leading=11, textColor=colors.HexColor('#555555'), spaceAfter=8)
cell = ParagraphStyle('cell', parent=body, fontSize=7.1, leading=8.6, spaceAfter=0)
cellh = ParagraphStyle('cellh', parent=cell, fontName='DVB', textColor=colors.white)
cap = ParagraphStyle('cap', parent=body, fontName='DVI', fontSize=7.8, leading=10, textColor=colors.HexColor('#444444'))

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<i>\1</i>', t)
    t = re.sub(r'`(.+?)`', r'<font face="DVM">\1</font>', t)
    t = re.sub(r'\^([^^\s]+?)\^', r'<super>\1</super>', t)
    return t

W, H = A4; margin = 1.6 * cm; avail = W - 2 * margin
story = []
for b in blocks:
    kind = b[0]
    if kind == 'meta':
        story.append(Paragraph(inline(b[1].get('title', '')), title))
        story.append(Paragraph(inline(b[1].get('subtitle', '')), subtitle))
    elif kind == 'h':
        st = h1 if b[1] == 1 else h2
        if b[1] == 1 and story and not b[2].startswith('1.'):
            pass
        story.append(Paragraph(inline(b[2]), st))
    elif kind == 'p':
        txt = b[1]
        if txt.startswith('*') and txt.endswith('*') and not txt.startswith('**'):
            story.append(Paragraph(inline(txt), cap))
        else:
            story.append(Paragraph(inline(txt), body))
    elif kind == 'list':
        items = b[1]
        # build nested lists: indent 0 vs >=4
        flow = []; i = 0
        def build(level_items, ordered):
            return ListFlowable([ListItem(x, leftIndent=12) for x in level_items], bulletType=('1' if ordered else 'bullet'), bulletFormat=('%s.' if ordered else None),
                                start=('1' if ordered else '•'), leftIndent=12, bulletFontName='DV', bulletFontSize=8)
        top = []; ordered_top = items[0][2]
        while i < len(items):
            ind, txt, ordd = items[i]
            para = Paragraph(inline(txt), li)
            sub = []
            j = i + 1
            while j < len(items) and items[j][0] > ind:
                sub.append(Paragraph(inline(items[j][1]), li)); j += 1
            if sub:
                top.append([para, build(sub, items[i + 1][2])])
            else:
                top.append(para)
            i = j
        lf = ListFlowable([ListItem(x if not isinstance(x, list) else x, leftIndent=12) for x in top],
                          bulletType=('1' if ordered_top else 'bullet'), bulletFormat=('%s.' if ordered_top else None), leftIndent=12, bulletFontName='DV', bulletFontSize=8)
        story.append(lf)
    elif kind == 'table':
        rows = b[1]; n = len(rows[0]); w = col_weights(rows)
        data = [[Paragraph(inline(c), cellh) for c in rows[0]]] + [[Paragraph(inline(c), cell) for c in r[:n]] for r in rows[1:]]
        t = Table(data, colWidths=[avail * x for x in w], repeatRows=1)
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4e79')), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                               ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#9a9a9a')),
                               ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f6fa')]),
                               ('LEFTPADDING', (0, 0), (-1, -1), 3), ('RIGHTPADDING', (0, 0), (-1, -1), 3),
                               ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2)]))
        story.append(t); story.append(Spacer(1, 4))
    elif kind == 'img':
        from reportlab.lib.utils import ImageReader
        ir = ImageReader(b[2]); iw, ih = ir.getSize()
        wd = avail; ht = wd * ih / iw
        if ht > 0.56 * H:
            ht = 0.56 * H; wd = ht * iw / ih
        story.append(KeepTogether([Image(b[2], width=wd, height=ht), Paragraph(inline(b[1]), cap), Spacer(1, 6)]))

def footer(canv, doc_):
    canv.saveState(); canv.setFont('DV', 7); canv.setFillColor(colors.HexColor('#777777'))
    canv.drawString(margin, 1.0 * cm, 'PSLN program - portfolio proposal - data cut 1 Nov 2026 - every number is traceable in PSLN_analysis_tables.xlsx')
    canv.drawRightString(W - margin, 1.0 * cm, f'page {doc_.page}'); canv.restoreState()
pdf = f'{OUTD}/PSLN_portfolio_proposal.pdf'
SimpleDocTemplate(pdf, pagesize=A4, leftMargin=margin, rightMargin=margin, topMargin=1.5 * cm, bottomMargin=1.6 * cm,
                  title='PSLN portfolio proposal', author='Portfolio analysis').build(story, onFirstPage=footer, onLaterPages=footer)
print('PDF written', pdf, os.path.getsize(pdf))
