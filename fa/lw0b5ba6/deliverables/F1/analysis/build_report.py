"""
build_report.py -- renders the proposal from proposal_template.md:
  * fills every {{evidence}} placeholder from evidence.py and assigns the [E#] tags in order of first use
  * generates Table 2 (sensitivity), Table 5 (defects), Appendix A (ledger), Appendix C (survival by block)
  * writes the Markdown, converts it to Word with pandoc, and writes the evidence workbook
"""
import re, os, subprocess, zipfile, shutil, math
import pandas as pd, numpy as np
from scipy import stats
import evidence as EV
from evidence import E, R, RANGE, sv, surv, prop, pfmt, AGED11, CLEAN8
from defects import DEF
from stats_util import clopper_pearson

from paths import OUT, TABLES as T, BUILD, PANDOC, ROOT
tmpl = open(os.path.join(ROOT, 'proposal_template.md'), encoding='utf8').read()

# ---------------------------------------------------------------- evidence tags in order of first use
pat = re.compile(r'\{\{([a-z0-9_]+)(?:\.([a-z0-9_]+))?(\|[vt])?\}\}')
order = []
for m in pat.finditer(tmpl):
    assert m.group(1) in E, f'unknown evidence key {m.group(1)}'
    if m.group(1) not in order: order.append(m.group(1))
unused = [k for k in E if k not in order]
num = {k: i + 1 for i, k in enumerate(order + unused)}
def sub(m):
    key, val, mode = m.group(1), m.group(2), m.group(3)
    tag = f'[E{num[key]}]'
    if mode == '|t' or val is None:
        assert mode == '|t', f'{{{{{key}}}}} needs .value or |t'
        return tag
    assert val in E[key]['vals'], f'{key}.{val} not defined'
    return E[key]['vals'][val] if mode == '|v' else f"{E[key]['vals'][val]} {tag}"
body = pat.sub(sub, tmpl)

# ---------------------------------------------------------------- generated tables
def md_table(header, rows, widths):
    esc = lambda s: str(s).replace('|', '/').replace('\n', ' ')
    out = ['| ' + ' | '.join(header) + ' |', '|' + '|'.join(':' + '-' * max(3, w) for w in widths) + '|']
    out += ['| ' + ' | '.join(esc(c) for c in r) + ' |' for r in rows]
    return '\n'.join(out)

P7 = pd.read_csv(T + 'T7_survival_pooled.csv')
def p7row(label, analysis):
    r = P7[(P7.analysis == analysis) & (P7.contrast == 'PSLN-344 vs PSLN-212')].iloc[0]
    return [label, int(r.k_experiments), f"{r.surv_a.replace('/', ' of ')} ({r.pct_a:.0f}%)", f"{r.surv_b.replace('/', ' of ')} ({r.pct_b:.0f}%)",
            f"{r.MH_risk_diff_pct:.0f} ({r.rd_lo:.0f} to {min(r.rd_hi, 100):.0f})", pfmt(r.p_strat_logrank)]
wa, wb = int(E['worst']['vals']['a'].split()[0]), int(E['worst']['vals']['b'].split()[0])
rdw = 100 * (wa - wb) / 80; sew = 100 * math.sqrt(wa / 80 * (1 - wa / 80) / 80 + wb / 80 * (1 - wb / 80) / 80)
sens = [p7row('As printed', 'ALL aged experiments, as printed (11)'),
        p7row('Duplicated table counted once (D1)', 'excluding S06-D (duplicate of S06-C) (10)'),
        p7row('**Duplicated table counted once and both label-conflicted tables removed (D1–D3): headline**', 'excluding S06-D and label-conflicted S03-I/S03-J (8)'),
        p7row('Both copies of the duplicated table and both label-conflicted tables removed', 'excluding both copies S06-C/S06-D and S03-I/S03-J (7)'),
        ['Worst case: every table-versus-weight conflict resolved against PSLN-344', 11, f"{wa} of 80 ({100*wa/80:.0f}%)", f"{wb} of 80 ({100*wb/80:.0f}%)", f"{rdw:.0f} ({rdw-1.96*sew:.0f} to {rdw+1.96*sew:.0f})",
         pfmt(stats.fisher_exact([[wa, 80 - wa], [wb, 80 - wb]])[1]) + ' (Fisher)'],
        p7row('Challenge 2–3 days after dosing (S06-D removed; the comparator label in S03-J is in doubt, D3)', 'timing d2-3 excluding S06-D'),
        p7row('Challenge on day 14 (includes the duplicated table)', 'timing d14, as printed'),
        p7row('Challenge on day 60', 'timing d60, as printed'),
        p7row('C57BL/6 and Swiss Webster', 'timing other strain (timing n.s.), as printed')]
sens_md = md_table(['Reading of the record', 'Experiments', 'PSLN-344 survived', 'PSLN-212 survived', 'Difference, points (95% CI)', 'p (stratified log-rank)'], sens, [33, 13, 14, 14, 14, 12])
sens_md += f"\n\nSource: T7; worst case from T2 [E{num['worst']}]. Aged animals only. The difference is the Mantel–Haenszel risk difference across experiments (simple difference for the worst-case row)."

def_rows = [[f"**{d.id}** ({d.sev})", d.where, d.what, f"{d.effect} *Handling:* {d.handling}"] for d in DEF.itertuples()]
def_md = md_table(['ID (severity)', 'Blocks (cells)', 'What is wrong', 'Effect on conclusions, and how I handled it'], def_rows, [9, 19, 38, 34])

led_rows = [[f"E{num[k]}", E[k]['statement'], E[k]['data'], E[k]['analysis']] for k in order + unused]
led_md = md_table(['Tag', 'Statement supported', 'Workbook cells', 'Analysis'], led_rows, [5, 50, 25, 20])

S5 = pd.read_csv(T + 'T5_survival_by_block.csv')
GL = {'Sham': 'vehicle', 'PSLN-212(Y)': 'young PSLN-212', 'PSLN-344Y': 'young PSLN-344', 'PSLN-212Y': 'young PSLN-212', 'PSLN-344(Y)': 'young PSLN-344', 'CMP-204(Y)': 'young CMP-204',
      'Untreated': 'untreated, not challenged', 'Naive': 'unvaccinated'}
srows = []
for blk, t in S5.groupby('block', sort=False):
    r0 = t.iloc[0]
    cells = []
    for r in t.itertuples():
        dd = eval(r.death_days) if isinstance(r.death_days, str) else []
        dtxt = f" [deaths on days {', '.join(str(int(x)) for x in dd)}]" if dd else ''
        cells.append(f"{GL.get(r.group, r.group)} {int(r.survivors)}/{int(r.n)}{dtxt}")
    day = {'not stated': 'day not stated'}.get(r0.day, 'day ' + str(r0.day)[1:] + ' after dosing')
    chal = 'challenge not stated' if r0.challenge == 'not stated' else f"challenge: {r0.challenge.replace('5x ', '5 × ').replace('10x ', '10 × ')}, {day}"
    vac = {'bivalent / none': 'bivalent, or none', 'rgH5N1, single dose': 'rgH5N1'}.get(r0.vaccine, r0.vaccine)
    srows.append([blk.replace(' (rows 34-68)', ' [rows 34–68]').replace(' (rows 71-105)', ' [rows 71–105]') + f" ({RANGE[blk]})", f"{r0.strain}; vaccine: {vac}; {chal}", '; '.join(cells)])
surv_md = md_table(['Block (cells)', 'Animals, vaccine, challenge', 'Survived / n by group'], srows, [16, 28, 56])
surv_md += ("\n\nSource: T5. Group names as printed in the workbook, except 'vehicle' for 'Sham' and 'unvaccinated' for 'Naive' in S13-E. In S06 rows 71–105, 'Naive' and 'Imprinting' mean not infected and infected with PR8 four months before vaccination. "
            "Defects D1 to D3 apply to S06-C/S06-D, S03-I and S03-J. In S03-J the tenth PSLN-344 record has no day value.")

body = body.replace('<<TABLE:sensitivity>>', sens_md).replace('<<TABLE:defects>>', def_md).replace('<<TABLE:ledger>>', led_md).replace('<<TABLE:survival>>', surv_md)
assert '<<TABLE' not in body and '{{' not in body
md_path = BUILD + 'PSLN-344_portfolio_proposal.md'
open(md_path, 'w', encoding='utf8').write(body)
print('evidence items:', len(E), '| cited in text:', len(order), '| not cited:', unused)

# ---------------------------------------------------------------- Word
docx = OUT + 'PSLN-344_portfolio_proposal.docx'
subprocess.run([PANDOC, md_path, '-o', docx, '--from', 'markdown+pipe_tables+yaml_metadata_block+implicit_figures', '--reference-doc', BUILD + 'psln_reference.docx',
                '--resource-path', OUT], check=True)
# post-process: 9-pt paragraph style inside tables; keep header rows with next; fixed full-width tables
zin = zipfile.ZipFile(docx); files = {n: zin.read(n) for n in zin.namelist()}; zin.close()
doc = files['word/document.xml'].decode('utf8')
def fix_tbl(m):
    return m.group(0).replace('<w:pStyle w:val="Compact" />', '<w:pStyle w:val="TableText" />').replace('<w:pStyle w:val="Compact"/>', '<w:pStyle w:val="TableText"/>')
doc2, ntbl = re.subn(r'<w:tbl>.*?</w:tbl>', fix_tbl, doc, flags=re.S)
TEXT_W = 11906 - 2 * 1077          # A4 width minus the margins set in make_reference.py (twips)
def fix_grid(m):
    ws = [int(x) for x in re.findall(r'w:w="(\d+)"', m.group(1))]
    f = TEXT_W / sum(ws)
    return '<w:tblGrid>' + ''.join(f'<w:gridCol w:w="{round(w * f)}" />' for w in ws) + '</w:tblGrid>'
doc2 = re.sub(r'<w:tblGrid>(.*?)</w:tblGrid>', fix_grid, doc2, flags=re.S)
files['word/document.xml'] = doc2.encode('utf8')
import xml.dom.minidom as minidom
for n, b in files.items():
    if n.endswith('.xml') or n.endswith('.rels'): minidom.parseString(b)
with zipfile.ZipFile(docx, 'w', zipfile.ZIP_DEFLATED) as zout:
    zout.writestr('[Content_Types].xml', files['[Content_Types].xml'])
    for n, b in files.items():
        if n != '[Content_Types].xml': zout.writestr(n, b)
print('docx written; tables restyled:', ntbl)

# ---------------------------------------------------------------- evidence workbook
led = pd.DataFrame([dict(tag=f"E{num[k]}", key=k, statement=E[k]['statement'], workbook_cells=E[k]['data'], analysis=E[k]['analysis'], cited_in_text=k in order) for k in order + unused])
led.to_csv(T + 'T18_evidence_ledger.csv', index=False)
DEF.rename(columns={'id': 'ID', 'sev': 'severity', 'where': 'blocks_cells', 'what': 'what_is_wrong', 'effect': 'effect_on_conclusions', 'handling': 'how_handled'}).to_csv(T + 'T17_record_defects.csv', index=False)
