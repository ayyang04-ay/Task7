#!/usr/bin/env python
"""
11_build_proposal.py -- fills proposal_template.md with numbers from tables/T10_numbers_cited.json
(so that no number in the proposal is typed by hand) and writes ../PSLN-344_portfolio_proposal.md
Run: micromamba run -n core python 11_build_proposal.py
"""
import os, re, json, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); T = os.path.join(HERE, 'tables')
N = json.load(open(os.path.join(T, 'T10_numbers_cited.json')))
S2 = pd.read_csv(os.path.join(T, 'T02_survival_by_group.csv'))
def sg(b, g):
    x = S2[(S2.block == b) & (S2.group == g)]
    return '—' if not len(x) else f"{int(x.survivors.iloc[0])}/{int(x.n_rows.iloc[0])}"
rows = [
 ('S03-I', 'Aged BALB/c', 'H1N1+H3N2 → CA09 H1N1, 10× LD50 (d14)', 'Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)', [('CMP-204', 'CMP-204')]),
 ('S03-J', 'BALB/c, age not stated', 'rgH5N1 → wild-type H5N1 (d2), 22-day follow-up', 'Sham', 'PSLN-212', 'PSLN-344', None, []),
 ('S06-A', 'Aged BALB/c', 'H3N2 → PR8 H1N1, 5× LD50 (d14)', 'Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)', []),
 ('S06-B', 'Aged BALB/c', 'H3N2 → PR8 H1N1 (d3)', 'Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)', []),
 ('S06-C', 'Aged BALB/c', 'H1N1+H3N2 → rgH5N1 (d14)', 'Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)', []),
 ('S06-D', 'Aged BALB/c', 'H1N1+H3N2 → rgH5N1 (d3)', 'Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)', []),
 ('S06-E', 'Aged BALB/c', 'H3N2 → PR8 H1N1 (d60)', 'Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)', [('Untreated', 'unchallenged')]),
 ('S06-F', 'Aged BALB/c', 'H1N1+H3N2 → rgH5N1 (d60)', 'Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)', [('Untreated', 'unchallenged')]),
 ('S06-G', 'Aged BALB/c', 'H1N1 → Perth H3N2 (d60)', 'Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)', [('Untreated', 'unchallenged')]),
 ('S15-L', 'Aged C57BL/6', 'H1N1+H3N2 → not stated', 'Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)', []),
 ('S15-N', 'Aged Swiss Webster', 'H1N1+H3N2 → not stated', 'Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)', []),
 ('S15-H', 'Aged BALB/c', 'H1N1+H3N2 or none → rgH5N1 (d3)', None, None, '3d Vaccine+PSLN-344', None, [('3d Vaccine', 'vaccine alone'), ('3d PSLN-344', 'PSLN-344 alone')]),
 ('S06-E(r71)', '14-month BALB/c', 'H1N1+H3N2 → PR8 H1N1; naive / PR8-imprinted', None, ('Naive+PSLN-212', 'Imprinting+PSLN-212'), ('Naive+PSLN-344', 'Imprinting+PSLN-344'), None, []),
 ('S06-F(r71)', '14-month BALB/c', 'H1N1+H3N2 → Perth H3N2 (d14); naive / PR8-imprinted', None, ('Naive+PSLN-212', 'Imprinting+PSLN-212'), ('Naive+PSLN-344', 'Imprinting+PSLN-344'), None, []),
 ('S09-B', 'Young BALB/c', 'H3N2 → PR8 H1N1 (d21)', 'Sham', None, None, 'PSLN-212Y', [('PSLN-344Y', 'young + PSLN-344')]),
 ('S09-D', 'Young BALB/c', 'H1N1 → Perth H3N2 (d21)', 'Sham', None, None, 'PSLN-212Y', [('PSLN-344Y', 'young + PSLN-344')]),
 ('S09-F', 'Young BALB/c', 'H1N1+H3N2 → rgH5N1 (d180)', 'Sham', None, None, 'PSLN-212Y', [('PSLN-344Y', 'young + PSLN-344')]),
 ('S13-E', 'Young BALB/c', 'H1N1+H3N2 → CA09 H1N1, 10× LD50 (d14)', 'Sham', None, None, None, [('PSLN-344(Y)', 'young + PSLN-344'), ('CMP-204(Y)', 'young + CMP-204'), ('Naive', 'naive')]),
]
def cell(b, g):
    if g is None: return '—'
    if isinstance(g, tuple): return ' / '.join(sg(b, x) for x in g)
    return sg(b, g)
lines = []
for b, host, design, sham, p212, p344, y, other in rows:
    oth = '; '.join(f'{lab} {sg(b, g)}' for g, lab in other) or '—'
    p344c = cell(b, p344)
    lines.append(f"| {b.replace('(r71)', ' (rows 71–105)')} | {host} | {design} | {cell(b, sham)} | {cell(b, p212)} | **{p344c}** | {cell(b, y)} | {oth} |" if p344c != '—'
                 else f"| {b} | {host} | {design} | {cell(b, sham)} | {cell(b, p212)} | — | {cell(b, y)} | {oth} |")
N['SURVIVAL_ROWS'] = '\n'.join(lines)
tpl = open(os.path.join(HERE, 'proposal_template.md'), encoding='utf-8').read()
appA = tpl[tpl.index('## Appendix A'):tpl.index('## Appendix B')]
N['n_dq'] = str(len(re.findall(r'^\| \d+ \|', appA, flags=re.M)))
missing = sorted(set(k for k in re.findall(r'\{\{(\w+)\}\}', tpl) if k not in N))
assert not missing, f'placeholders without a registered number: {missing}'
used = set(re.findall(r'\{\{(\w+)\}\}', tpl))
out = re.sub(r'\{\{(\w+)\}\}', lambda m: str(N[m.group(1)]), tpl)
SUP = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')
out = re.sub(r'×10\^(-?\d+)', lambda m: '×10' + m.group(1).translate(SUP), out)
dst = os.path.join(HERE, '..', 'PSLN-344_portfolio_proposal.md')
open(dst, 'w', encoding='utf-8').write(out)
# register: keep only the numbers that appear in the proposal, and say where they appear
sections = re.split(r'^## ', tpl, flags=re.M)
where = {}
for s_ in sections[1:]:
    title = s_.split('\n', 1)[0].strip()
    for k in set(re.findall(r'\{\{(\w+)\}\}', s_)): where.setdefault(k, []).append(title.split(':')[0].split(' — ')[0])
reg = pd.read_csv(os.path.join(T, 'T10_numbers_cited.csv'))
if 'used_in_proposal' in reg.columns: reg = reg.drop(columns=['used_in_proposal'])
if 'section' in reg.columns: reg = reg.drop(columns=['section'])
reg = reg[reg.key.isin(used)].copy(); reg.insert(2, 'section', reg.key.map(lambda k: '; '.join(where.get(k, []))))
reg.to_csv(os.path.join(T, 'T10_numbers_cited.csv'), index=False)
print('written', os.path.abspath(dst), '|', len(used) - 1, 'registered numbers used |', len(out.split()), 'words')
assert '{{' not in out
