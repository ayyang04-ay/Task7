"""Render the proposal (Markdown + PDF) and the evidence workbook from report_content.py and the analysis CSVs."""
import re, os, json, numpy as np, pandas as pd
from PIL import Image as PILImage
import report_content as rc
OUT = '/tmp/outputs/'

# ------------------------------------------------------------------ reference integrity -------------------------------
def expand(t):
    out = set()
    for m in re.finditer(r'([LQ])(\d+)([a-d]?) to \1(\d+)([a-d]?)', t):
        p, a, sa, b, sb = m.groups()
        if a == b and sa and sb:
            for ch in 'abcd'['abcd'.index(sa):'abcd'.index(sb) + 1]: out.add(f'{p}{a}{ch}')
        else:
            for i in range(int(a), int(b) + 1): out.add(f'{p}{i:02d}')
    return out
alltext = ' '.join(str(x) for b in rc.DOC for x in (b[1:] if b[0] != 'table' else [b[2]]))
refs = set(re.findall(r'\b([LQ]\d+[a-d]?)\b', alltext)) | expand(alltext); ids = {e['id'] for e in rc.LEDGER}
assert not (refs - ids), f'references missing from ledger: {sorted(refs - ids)}'

# ------------------------------------------------------------------ Markdown ------------------------------------------
def md_cell(t): return str(t).replace('<br/>', ' ').replace('|', '\\|').replace('\n', ' ')
md = [f'# {rc.TITLE}', '', f'*{rc.SUBTITLE}*', '', rc.META, '']
def md_block(b):
    k = b[0]
    if k == 'h1': return ['', f'## {b[1]}', '']
    if k == 'h2': return ['', f'### {b[1]}', '']
    if k == 'p': return [b[1], '']
    if k == 'note': return [f'*{b[1]}*', '']
    if k == 'bullets': return [f'- {x}' for x in b[1]] + ['']
    if k == 'box': return [f'> **{b[1]}**', '>'] + [f'> - {x}' for x in b[2]] + ['']
    if k == 'img': return [f'![{b[3]}]({b[1].replace("../", "")})', '', f'*{b[3]}*', '']
    if k == 'pagebreak': return ['']
    if k == 'table':
        _, header, rows, widths, caption, fs = b
        out = ([f'**{caption}**', ''] if caption else []) + ['| ' + ' | '.join(header) + ' |', '|' + '---|' * len(header)]
        for r in rows: out.append('| ' + ' | '.join(md_cell(c) for c in r) + ' |')
        return out + ['']
for b in rc.DOC: md += md_block(b)
md += ['', '## Appendix A. Evidence ledger', '', 'Each entry gives the statement, the workbook cells it is computed from and the analysis that produced it. build_ledger.py recomputes every value from the cited cells.', '',
       '| ID | Statement | Workbook cells | Analysis |', '|---|---|---|---|']
for e in rc.LEDGER: md.append(f"| {e['id']} | {md_cell(e['statement'])} | {md_cell(e['cells'])} | {md_cell(e['analysis'])} |")
md += ['', '## Appendix B. Survival by experiment', '', 'Survivors / animals as printed in the survival tables. Square brackets give the count implied by the paired body-weight table where it differs. The p-value is the exact permutation log-rank test for PSLN-344 against PSLN-212 (or the comparison named).', '',
       '| Exp. | Block and cells | Design | Survivors / animals | Exact log-rank p |', '|---|---|---|---|---|']
for r in rc.APP_B: md.append('| ' + ' | '.join(md_cell(c) for c in r) + ' |')
md += ['', '## Appendix C. Methods and files', '']
for b in rc.APP_C: md += md_block(b)
open(OUT + 'PSLN-344_portfolio_proposal.md', 'w').write('\n'.join(md))

# ------------------------------------------------------------------ PDF ----------------------------------------------
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image, PageBreak, LongTable, Table, TableStyle, KeepTogether, ListFlowable, ListItem, CondPageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib
fd = os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data', 'fonts', 'ttf')
for name, f in [('DV', 'DejaVuSans.ttf'), ('DV-B', 'DejaVuSans-Bold.ttf'), ('DV-I', 'DejaVuSans-Oblique.ttf'), ('DV-BI', 'DejaVuSans-BoldOblique.ttf')]:
    pdfmetrics.registerFont(TTFont(name, os.path.join(fd, f)))
pdfmetrics.registerFontFamily('DV', normal='DV', bold='DV-B', italic='DV-I', boldItalic='DV-BI')
NAVY = colors.HexColor('#1f3a5f'); GREY = colors.HexColor('#f1f3f5'); LINE = colors.HexColor('#c9ced4')
def st(name, **kw):
    base = dict(fontName='DV', fontSize=9.2, leading=12.6, textColor=colors.HexColor('#1a1a1a'), alignment=TA_LEFT, spaceAfter=5)
    base.update(kw); return ParagraphStyle(name, **base)
S = dict(title=st('title', fontName='DV-B', fontSize=19, leading=23, textColor=NAVY, spaceAfter=3),
         sub=st('sub', fontSize=10.5, leading=14, textColor=colors.HexColor('#444444'), spaceAfter=6),
         meta=st('meta', fontSize=7.8, leading=10.6, textColor=colors.HexColor('#555555'), spaceAfter=8),
         h1=st('h1', fontName='DV-B', fontSize=13, leading=16, textColor=NAVY, spaceBefore=10, spaceAfter=5),
         h2=st('h2', fontName='DV-B', fontSize=10.2, leading=13, textColor=NAVY, spaceBefore=6, spaceAfter=3),
         p=st('p'), bullet=st('bullet', leftIndent=0, spaceAfter=2.5),
         cap=st('cap', fontSize=7.6, leading=10, textColor=colors.HexColor('#444444'), spaceAfter=8, spaceBefore=2),
         tcap=st('tcap', fontName='DV-B', fontSize=8.2, leading=10.5, textColor=NAVY, spaceAfter=3, spaceBefore=5),
         note=st('note', fontName='DV-I', fontSize=8, leading=10.5, textColor=colors.HexColor('#555555')))
def rl(t):
    t = str(t).replace('<br/>', '\x00')
    t = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\x00', '<br/>')
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<i>\1</i>', t)
    return t
def bullets(items, style=None, fs=None):
    stl = style or S['bullet']
    return ListFlowable([ListItem(Paragraph(rl(x), stl), leftIndent=11, bulletColor=NAVY) for x in items], bulletType='bullet', start='•', bulletFontName='DV', bulletFontSize=7, leftIndent=11, bulletOffsetY=-1)
FRAME_W = 174 * mm
def table(header, rows, widths, fs=7.4, longt=True):
    cs = st(f'c{fs}', fontSize=fs, leading=fs * 1.28, spaceAfter=0); hs = st(f'h{fs}', fontName='DV-B', fontSize=fs, leading=fs * 1.28, spaceAfter=0, textColor=colors.white)
    tot = sum(widths); cw = [w / tot * FRAME_W for w in widths]
    data = [[Paragraph(rl(h), hs) for h in header]]; style = [('BACKGROUND', (0, 0), (-1, 0), NAVY), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LINEBELOW', (0, 0), (-1, -1), 0.35, LINE),
             ('LEFTPADDING', (0, 0), (-1, -1), 3.2), ('RIGHTPADDING', (0, 0), (-1, -1), 3.2), ('TOPPADDING', (0, 0), (-1, -1), 2.6), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.8)]
    for i, r in enumerate(rows, 1):
        if str(r[0]).startswith('**Gate'): style += [('BACKGROUND', (0, i), (-1, i), GREY)]
        if all(str(c) == '' for c in r[1:]) and str(r[0]).startswith('**'):          # section row
            data.append([Paragraph(rl(r[0]), cs)] + [''] * (len(r) - 1)); style += [('SPAN', (0, i), (-1, i)), ('BACKGROUND', (0, i), (-1, i), GREY)]
        else:
            data.append([Paragraph(rl(c), cs) for c in r])
    T_ = (LongTable if longt else Table)(data, colWidths=cw, repeatRows=1); T_.setStyle(TableStyle(style)); return T_
def box(title, items):
    inner = [Paragraph(rl(f'**{title}**'), st('bt', fontSize=9.2, spaceAfter=3, textColor=NAVY))] + [bullets(items, st('bb', fontSize=8.6, leading=11.6, spaceAfter=2))]
    t = Table([[inner]], colWidths=[FRAME_W]); t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#eef3fb')), ('BOX', (0, 0), (-1, -1), 0.6, NAVY),
            ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7), ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 5)])); return t
def image(path, width_mm, caption):
    p = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), path)); w, h = PILImage.open(p).size
    W = width_mm * mm; H = W * h / w
    maxH = 225 * mm
    if H > maxH: W = W * maxH / H; H = maxH
    im = Image(p, width=W, height=H); im.hAlign = 'CENTER'
    return KeepTogether([im, Paragraph(rl(caption), S['cap'])])
PREV = {'k': None}
def flow(b):
    k = b[0]; prev = PREV['k']; PREV['k'] = k
    if k == 'h1': return [CondPageBreak(48 * mm), Paragraph(rl(b[1]), S['h1'])]
    if k == 'h2': return [CondPageBreak(30 * mm), Paragraph(rl(b[1]), S['h2'])]
    if k == 'p': return [Paragraph(rl(b[1]), S['p'])]
    if k == 'note': return [Paragraph(rl(b[1]), S['note'])]
    if k == 'bullets': return [bullets(b[1]), Spacer(1, 3)]
    if k == 'box': return [box(b[1], b[2]), Spacer(1, 6)]
    if k == 'img': return [image(b[1], b[2], b[3])]
    if k == 'pagebreak': return [PageBreak()]
    if k == 'table':
        _, header, rows, widths, caption, fs = b
        pre = [] if prev in ('h1', 'h2') else [CondPageBreak(42 * mm)]
        return pre + ([Paragraph(rl(caption), S['tcap'])] if caption else []) + [table(header, rows, widths, fs), Spacer(1, 7)]
story = [Paragraph(rl(rc.TITLE), S['title']), Paragraph(rl(rc.SUBTITLE), S['sub']), Paragraph(rl(rc.META), S['meta'])]
for b in rc.DOC: story += flow(b)
story += [PageBreak(), Paragraph('Appendix A. Evidence ledger', S['h1']),
          Paragraph(rl('Each entry gives the statement, the workbook cells it is computed from, and the analysis that produced it. The script build_ledger.py recomputes every value directly from the cited cells and stops if it disagrees with the analysis output. L = evidence; Q = data quality. The same ledger is in PSLN-344_evidence_ledger.xlsx.'), S['p']),
          table(['ID', 'Statement', 'Workbook cells', 'Analysis and method'], [[e['id'], e['statement'], e['cells'].replace(';', '; ').replace('  ', ' '), e['analysis'] + (('. ' + e['method']) if e['method'] else '')] for e in rc.LEDGER], [9, 92, 40, 33], fs=6.3)]
story += [PageBreak(), Paragraph('Appendix B. Survival by experiment', S['h1']),
          Paragraph(rl('Survivors / animals as printed in the survival tables. Square brackets give the count implied by the paired body-weight table where it differs. The p-value is the exact permutation log-rank test for PSLN-344 against PSLN-212 unless another comparison is named. E05 is excluded from pooled figures.'), S['p']),
          table(['Exp.', 'Block and cells', 'Design', 'Survivors / animals', 'Exact log-rank p'], rc.APP_B, [9, 27, 54, 60, 24], fs=6.8)]
story += [Spacer(1, 8), Paragraph('Appendix C. Methods and files', S['h1'])]
for b in rc.APP_C: story += flow(b)
def deco(canvas, doc):
    canvas.saveState(); canvas.setFont('DV', 7); canvas.setFillColor(colors.HexColor('#777777'))
    canvas.drawString(18 * mm, 10 * mm, 'PSLN-344 portfolio review proposal'); canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f'Page {doc.page}')
    canvas.setStrokeColor(LINE); canvas.setLineWidth(0.4); canvas.line(18 * mm, 13.5 * mm, A4[0] - 18 * mm, 13.5 * mm); canvas.restoreState()
doc = BaseDocTemplate(OUT + 'PSLN-344_portfolio_proposal.pdf', pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=18 * mm,
                      title=rc.TITLE, author='Portfolio analysis', subject='PSLN-344 portfolio review')
doc.addPageTemplates([PageTemplate(id='main', frames=[Frame(18 * mm, 18 * mm, FRAME_W, A4[1] - 34 * mm, id='f', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], onPage=deco)])
doc.build(story)
print('PDF pages:', doc.page)

# ------------------------------------------------------------------ Excel --------------------------------------------
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
sheets = [
 ('Ledger', pd.DataFrame(rc.LEDGER)[['id', 'section', 'statement', 'cells', 'analysis', 'method']], [8, 14, 110, 60, 55, 45]),
 ('Survival_by_arm', pd.read_csv('survival_per_experiment.csv'), None), ('Survival_tests', pd.read_csv('survival_tests.csv'), None), ('Survival_pooled', pd.read_csv('survival_pooled.csv'), None),
 ('Survival_by_window', pd.read_csv('survival_by_window.csv'), None), ('Survival_sensitivity', pd.read_csv('survival_sensitivity.csv'), None), ('Table_vs_weights_by_arm', pd.read_csv('survival_table_vs_weight_by_arm.csv'), None),
 ('Immunology_descriptives', pd.read_csv('immunology_descriptives.csv'), None), ('Immunology_contrasts', pd.read_csv('immunology_contrasts.csv'), None), ('Age_gap_closed', pd.read_csv('immunology_restoration_index.csv'), None),
 ('Timecourse_descriptives', pd.read_csv('timecourse_descriptives.csv'), None), ('Timecourse_contrasts', pd.read_csv('timecourse_contrasts.csv'), None), ('Timecourse_anova', pd.read_csv('timecourse_anova.csv'), None),
 ('Safety_weight', pd.read_csv('safety_weight_after_vaccination.csv'), None), ('Safety_cytokines', pd.read_csv('safety_cytokines.csv'), None), ('Safety_cytokine_tests', pd.read_csv('safety_cytokines_tests.csv'), None),
 ('Safety_CNS', pd.read_csv('safety_cns.csv'), None), ('Safety_CNS_tests', pd.read_csv('safety_cns_tests.csv'), None), ('Challenge_morbidity', pd.read_csv('challenge_morbidity.csv'), None),
 ('Age_by_manganese', pd.read_csv('age_by_manganese_interaction.csv'), None), ('Dose_response_fit', pd.read_csv('dose_response_fit.csv'), None), ('Dose_response_by_dose', pd.read_csv('dose_response_by_dose.csv'), None), ('Biomarker_separation', pd.read_csv('biomarker_separation.csv'), None), ('Power', pd.read_csv('power_table.csv'), None),
 ('QC_stated_vs_observed_n', pd.read_csv('audit_01_stated_vs_observed_n.csv'), None), ('QC_survival_vs_weight', pd.read_csv('audit_02_survival_vs_weight.csv'), None),
 ('QC_duplicate_vectors', pd.read_csv('audit_03a_duplicate_vectors.csv'), None), ('QC_positional_overlap', pd.read_csv('audit_03c_positional_overlap.csv'), None), ('QC_group_order_screen', pd.read_csv('audit_05_group_order_screen.csv'), None), ('QC_weights_per_animal', pd.read_csv('weights_decoded_per_animal.csv'), None),
]
readme = pd.DataFrame({'Sheet': ['README'] + [s[0] for s in sheets], 'Content': ['This workbook supports PSLN-344_portfolio_proposal.pdf. Every [L..]/[Q..] reference in the proposal is a row of the Ledger sheet. Source data: psln_program_dataset.xlsx; cell references are sheet!range in that workbook.',
  'Evidence ledger: statement, workbook cells, analysis output and method for every number used in the proposal', 'Survival per experiment and arm (n, deaths, survivors, exact CI, death days, cells)', 'Within-experiment Fisher and exact log-rank tests', 'Pooled analyses with experiments as strata',
  'Survival by interval between dose and challenge', 'Sensitivity analyses, including weight-table-implied outcomes and the adverse bound', 'Survival table vs body-weight table, arm by arm (aged experiments)',
  'Group descriptives for every single-time-point block (with cells and raw values)', 'Contrasts: effect, CI, Welch, Mann-Whitney, Tukey, ANOVA', 'Share of the aged-to-young gap closed by PSLN-344, with bootstrap CI',
  'Time-course descriptives', 'Per-time-point contrasts', 'Two-way ANOVA per time-course block', 'Body weight after vaccination (S08-D)', 'Lung cytokine transcripts (S09-A)', 'Tests on S09-A', 'CNS transcripts (S10-A)', 'Tests on S10-A',
  'Post-challenge weight nadir and recovery using real observations only', 'Two-way ANOVA, age x formulation: does manganese add more in aged than in young animals', 'Emax model fits (S08-A)', 'Means by dose (S08-A)', 'Protected vs unprotected group separation by read-out', 'Sample sizes for the proposed studies',
  'Audit: n printed in block labels vs observations present', 'Audit: survival tables vs body-weight tables', 'Audit: identical or near-identical value vectors in different places', 'Audit: identical values in identical positions between blocks of the same layout', 'Audit: where the PSLN-344 mean sits between aged PSLN-212 (0) and young PSLN-212 (1) in every block with all three groups', 'Body-weight tables decoded per animal']})
with pd.ExcelWriter(OUT + 'PSLN-344_evidence_ledger.xlsx', engine='openpyxl') as xw:
    readme.to_excel(xw, sheet_name='README', index=False)
    for name, df_, widths in sheets: df_.to_excel(xw, sheet_name=name, index=False)
    for ws in xw.book.worksheets:
        for c in ws[1]: c.font = Font(bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor='1F3A5F'); c.alignment = Alignment(wrap_text=True, vertical='top')
        ws.freeze_panes = 'A2'
        if ws.title in ('Ledger', 'README'):
            for i, w in enumerate([8, 14, 110, 60, 55, 45] if ws.title == 'Ledger' else [28, 140], 1): ws.column_dimensions[get_column_letter(i)].width = w
            for row in ws.iter_rows(min_row=2):
                for c in row: c.alignment = Alignment(wrap_text=True, vertical='top')
        else:
            for i, col in enumerate(ws.iter_cols(min_row=1, max_row=min(ws.max_row, 60)), 1):
                ws.column_dimensions[get_column_letter(i)].width = max(9, min(48, max(len(str(c.value)) if c.value is not None else 0 for c in col) + 2))
print('written: md, pdf, xlsx')
