"""Render the proposal Markdown to a committee-ready PDF with reportlab (figures inserted after the relevant sections)."""
import re, os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak,
                                KeepTogether, ListFlowable, ListItem, HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping

FD = '/opt/conda/envs/core/lib/python3.11/site-packages/matplotlib/mpl-data/fonts/ttf/'
pdfmetrics.registerFont(TTFont('DV', FD + 'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DV-B', FD + 'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DV-I', FD + 'DejaVuSans-Oblique.ttf'))
pdfmetrics.registerFont(TTFont('DV-BI', FD + 'DejaVuSans-BoldOblique.ttf'))
pdfmetrics.registerFont(TTFont('DVM', FD + 'DejaVuSansMono.ttf'))
addMapping('DV', 0, 0, 'DV'); addMapping('DV', 1, 0, 'DV-B'); addMapping('DV', 0, 1, 'DV-I'); addMapping('DV', 1, 1, 'DV-BI')

SRC = '/tmp/outputs/PSLN-344_portfolio_review_proposal.md'
OUT = '/tmp/outputs/PSLN-344_portfolio_review_proposal.pdf'
FIG = '/tmp/outputs/figures/'

ss = getSampleStyleSheet()
base = ParagraphStyle('base', parent=ss['Normal'], fontName='DV', fontSize=8.6, leading=11.4, spaceAfter=3)
h1 = ParagraphStyle('h1', parent=base, fontName='DV-B', fontSize=15, leading=19, spaceAfter=6, textColor=colors.HexColor('#1F3864'))
h2 = ParagraphStyle('h2', parent=base, fontName='DV-B', fontSize=11.5, leading=15, spaceBefore=8, spaceAfter=4, textColor=colors.HexColor('#1F3864'))
h3 = ParagraphStyle('h3', parent=base, fontName='DV-B', fontSize=9.6, leading=12.5, spaceBefore=6, spaceAfter=3, textColor=colors.HexColor('#2F5496'))
cell = ParagraphStyle('cell', parent=base, fontSize=7.1, leading=8.9, spaceAfter=0)
cellh = ParagraphStyle('cellh', parent=cell, fontName='DV-B', textColor=colors.white)
cap = ParagraphStyle('cap', parent=base, fontSize=7.4, leading=9.2, textColor=colors.HexColor('#404040'))
box = ParagraphStyle('box', parent=base, fontSize=8.8, leading=11.8)


def inline(t):
    t = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    t = re.sub(r'`([^`]+)`', r'<font name="DVM">\1</font>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'(?<![*\w])\*([^*\n]+?)\*(?!\*)', r'<i>\1</i>', t)
    return t


def make_table(rows, width):
    hdr = [c.strip() for c in rows[0].strip().strip('|').split('|')]
    body = []
    for r in rows[2:]:
        cells = [c.strip() for c in r.strip().strip('|').split('|')]
        body.append(cells)
    ncol = len(hdr)
    # column widths heuristic: proportional to max text length, with bounds
    from reportlab.pdfbase.pdfmetrics import stringWidth
    def strip(x): return re.sub(r'[*`]', '', x)
    # minimum width = widest single word (bold header words measured in bold) + padding
    minw = []
    for i in range(ncol):
        words = strip(hdr[i]).split() or ['']
        w = max(stringWidth(wd, 'DV-B', 7.1) for wd in words)
        for b in body:
            if i < len(b):
                for wd in strip(b[i]).split():
                    w = max(w, stringWidth(wd, 'DV-B' if '**' in b[i] else 'DV', 7.1))
        minw.append(w + 8)
    lens = [max([len(strip(hdr[i]))] + [len(strip(b[i])) if i < len(b) else 0 for b in body]) for i in range(ncol)]
    lens = [min(max(l, 6), 90) for l in lens]
    cw = [max(minw[i], width * lens[i] / sum(lens)) for i in range(ncol)]
    # rescale the flexible columns so the total fits the page width
    excess = sum(cw) - width
    if excess > 0:
        flex = [i for i in range(ncol) if cw[i] > minw[i]]
        room = sum(cw[i] - minw[i] for i in flex)
        for i in flex: cw[i] -= excess * (cw[i] - minw[i]) / room if room > 0 else 0
    data = [[Paragraph(inline(h), cellh) for h in hdr]] + [[Paragraph(inline(c), cell) for c in b] for b in body]
    tbl = Table(data, colWidths=cw, repeatRows=1)
    st = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#305496')), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                     ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#A6A6A6')), ('LEFTPADDING', (0, 0), (-1, -1), 3), ('RIGHTPADDING', (0, 0), (-1, -1), 3),
                     ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2)])
    for i in range(1, len(data)):
        if i % 2 == 0: st.add('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F2F2F2'))
    # colour severity cells
    for i, b in enumerate(body, start=1):
        for j, c in enumerate(b):
            if c in ('Critical',): st.add('BACKGROUND', (j, i), (j, i), colors.HexColor('#F8CBAD'))
            if c in ('Major',): st.add('BACKGROUND', (j, i), (j, i), colors.HexColor('#FFE699'))
    tbl.setStyle(st)
    return tbl


FIGS_AFTER = {}
FIGURES = [
    ('fig1_forest_PSLN344_vs_PSLN212.png', "Fig. 1. Hedges' g for PSLN-344 vs PSLN-212 in aged mice across 53 continuous readouts (ET2). Filled = Welch p<0.05."),
    ('fig2_restoration_index.png', 'Fig. 2. Restoration index: share of the aged-vs-young deficit closed by PSLN-344, for the 43 readouts with a significant age gap (ET7).'),
    ('fig3_survival_KM.png', 'Fig. 3. Kaplan–Meier curves for each aged challenge experiment as recorded, with integrity flags (ET3, ET4, ET8).'),
    ('fig4_pooled_survival_tiers.png', 'Fig. 4. Pooled survival by integrity sensitivity tier (ET5).'),
    ('fig5_data_integrity_evidence.png', 'Fig. 5. Integrity evidence (ET8–ET12).'),
    ('fig6_MoA_schematic.png', 'Fig. 6. Mechanism of action assembled from the dataset; colour = strength of evidence.'),
    ('fig7_safety_readouts.png', 'Fig. 7. Tolerability and safety-relevant readouts (S08-D, S10-A, S09-A).'),
]


def build():
    lines = open(SRC, encoding='utf-8').read().split('\n')
    W = A4[0] - 30 * mm
    story = []
    i = 0
    pending_figs = []
    in_list = []

    def flush_list():
        nonlocal in_list
        if in_list:
            k = 0
            for x, num, ind in in_list:
                k += 1
                st = ParagraphStyle('li', parent=base, leftIndent=12 + ind * 10, bulletIndent=3 + ind * 10, spaceAfter=1.5)
                story.append(Paragraph(inline(x), st, bulletText=(f'{k}.' if num else ('•' if ind == 0 else '–'))))
            story.append(Spacer(1, 2))
            in_list = []

    def insert_figs(figs):
        for fn, caption, wmm in figs:
            p = FIG + fn
            if not os.path.exists(p): continue
            from PIL import Image as PI
            im = PI.open(p); w, h = im.size
            ww = min(wmm * mm, W); hh = ww * h / w
            maxh = A4[1] - 40 * mm
            if hh > maxh: hh = maxh; ww = hh * w / h
            story.append(KeepTogether([Image(p, width=ww, height=hh), Paragraph(caption, cap), Spacer(1, 4)]))

    while i < len(lines):
        ln = lines[i]
        s = ln.rstrip()
        # figure insertion triggers at next section heading
        if s.startswith('#'):
            flush_list()
            if pending_figs:
                insert_figs(pending_figs); pending_figs = []
            for key, figs in FIGS_AFTER.items():
                if s.startswith(key):
                    pending_figs = figs
        if s.startswith('# '):
            story.append(Paragraph(inline(s[2:]), h1)); i += 1; continue
        if s.startswith('## '):
            story.append(Paragraph(inline(s[3:]), h2)); i += 1; continue
        if s.startswith('### '):
            story.append(Paragraph(inline(s[4:]), h3)); i += 1; continue
        if s.strip() == '---':
            flush_list(); story.append(HRFlowable(width='100%', thickness=0.6, color=colors.HexColor('#A6A6A6'), spaceBefore=3, spaceAfter=5)); i += 1; continue
        if s.startswith('|'):
            flush_list()
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append(lines[i]); i += 1
            story.append(make_table(rows, W)); story.append(Spacer(1, 5)); continue
        m = re.match(r'^(\s*)[-•] (.*)', s)
        n = re.match(r'^(\s*)\d+\. (.*)', s)
        if m or n:
            txt = (m or n).group(2); ind = len((m or n).group(1)) // 2
            in_list.append((txt, bool(n), ind)); i += 1; continue
        if s.strip() == '':
            flush_list(); i += 1; continue
        flush_list()
        story.append(Paragraph(inline(s), base)); i += 1
    flush_list()
    if pending_figs: insert_figs(pending_figs)
    from PIL import Image as PI
    for fn, caption in FIGURES:
        p = FIG + fn
        im = PI.open(p); w, h = im.size
        landscape_fig = w / h > 1.25
        ww = W; hh = ww * h / w
        maxh = A4[1] - 45 * mm
        if hh > maxh: hh = maxh; ww = hh * w / h
        story.append(PageBreak())
        if fn.startswith('fig1'):
            story.append(Paragraph('Appendix C – Figures', h2))
        story.append(Image(p, width=ww, height=hh)); story.append(Paragraph(caption, cap))

    def onpage(c, d):
        c.saveState(); c.setFont('DV', 7); c.setFillColor(colors.HexColor('#7F7F7F'))
        c.drawString(15 * mm, 8 * mm, 'PSLN-344 portfolio review — recommendation & next steps — 1 Nov 2026 — CONFIDENTIAL')
        c.drawRightString(A4[0] - 15 * mm, 8 * mm, f'page {d.page}')
        c.restoreState()
    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=15 * mm, rightMargin=15 * mm, topMargin=13 * mm, bottomMargin=14 * mm,
                            title='PSLN-344 Portfolio Review Proposal', author='Portfolio review analysis')
    doc.build(story, onFirstPage=onpage, onLaterPages=onpage)
    print('PDF written', OUT)


build()
