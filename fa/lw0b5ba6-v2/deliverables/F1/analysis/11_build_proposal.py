"""Fill the proposal template from the evidence ledger, build the tables that sit in the text, and write the Markdown.
Fails if any placeholder is unknown.  Marks which ledger entries the text actually uses."""
import json, re
import pandas as pd
N = json.load(open('../tables/numbers.json'))
LED = pd.read_csv('../tables/T0_evidence_ledger.csv')
used = set()
def n(k):
    if k not in N: raise KeyError(f'unknown number key: {k}')
    used.add(k); v = N[k]
    if re.fullmatch(r'[-+0-9., to]+', v):       # signed plain numbers and "a to b" intervals: typographic minus
        v = v.replace('-', '−')
    return v

# ------------------------------------------------------------------ table: survival by experiment
def sv(block, group):
    k = re.sub(r'[^A-Za-z0-9]+', '', block) + '_' + re.sub(r'[^A-Za-z0-9]+', '', group)
    return n(k)
rows = ['| Experiment | Vaccine → challenge virus; days from dose to challenge | Vaccine alone (sham) | PSLN-212, aged | PSLN-344, aged | PSLN-212, young | Notes |', '|---|---|---|---|---|---|---|']
def r4(b, desc, note=''):
    rows.append(f"| {b} | {desc} | {sv(b,'Sham')} | {sv(b,'PSLN-212')} | **{sv(b,'PSLN-344')}** | {sv(b,'PSLN-212(Y)')} | {note} |")
r4('S06-A', 'H3N2 → H1N1 (PR8); 14 d')
r4('S06-B', 'H3N2 → H1N1 (PR8); 3 d')
r4('S06-C', 'H1N1 + H3N2 → H5N1 (reverse-genetics); 14 d', 'One of an identical pair with S06-D (Q4); counted once')
rows.append(f"| **Core experiments, total** | | **{n('rob_sham')}** | **{n('rob_212')}** | **{n('rob_344')}** | **{n('rob_y212')}** | |")
r4('S03-I', 'H1N1 + H3N2 → H1N1 (CA09, matched strain); 14 d', f"Labels disputed (Q2); CMP-204 {sv('S03-I','CMP-204')}")
rows.append(f"| S03-J | H5N1 → wild-type H5N1; 2 d | {sv('S03-J','Sham')} | {sv('S03-J','PSLN-212')} | **{sv('S03-J','PSLN-344')}** | not tested | Labels disputed (Q3) |")
r4('S06-D', 'H1N1 + H3N2 → H5N1; 3 d', 'Identical to S06-C (Q4)')
rows.append(f"| **All six as printed, total** | | **{n('acute_sham')}** | **{n('acute_212')}** | **{n('acute_344')}** | **{n('acute_y212')}** | |")
rows.append(f"| S15-H | H1N1 + H3N2 → H5N1; 3 d | {sv('S15-H','3d Vaccine')} (no liposome) | not tested | **{sv('S15-H','3d Vaccine+PSLN-344')}** | not tested | PSLN-344 without vaccine: {sv('S15-H','3d PSLN-344')} |")
for b, desc in [('S06-E', 'H3N2 → H1N1 (PR8); 60 d'), ('S06-F', 'H1N1 + H3N2 → H5N1; 60 d'), ('S06-G', 'H1N1 → H3N2 (Perth); 60 d')]:
    r4(b, desc, f"Untreated, unchallenged: {sv(b,'Untreated')}")
rows.append(f"| **Day 60, total** | | **{n('d60_sham')}** | **{n('d60_212')}** | **{n('d60_344')}** | **{n('d60_y212')}** | Untreated, unchallenged: {n('d60_untreated')} |")
r4('S15-L', 'C57BL/6, 20 months; challenge not stated', 'Q5, Q15')
r4('S15-N', 'Swiss Webster, 20 months; challenge not stated', 'Q5, Q15')
for b, lab, desc in [('S06-E[r71]', 'S06-E, rows 71–105', '14-month BALB/c; H1N1 + H3N2 → H1N1 (PR8)'), ('S06-F[r71]', 'S06-F, rows 71–105', '14-month BALB/c; H1N1 + H3N2 → H3N2 (Perth); 14 d')]:
    rows.append(f"| {lab} | {desc} | not tested | {sv(b,'Naive+PSLN-212')} ({sv(b,'Imprinting+PSLN-212')} if previously infected) | **{sv(b,'Naive+PSLN-344')}** ({sv(b,'Imprinting+PSLN-344')} if previously infected) | not tested | Label used twice (Q13) |")
T_SURV = 'Survivors / animals at the end of observation. Bold totals are the figures used in section 1.\n\n' + '\n'.join(rows)

# ------------------------------------------------------------------ table: immune read-outs
spec = json.load(open('_imm_table_spec.json'))
rows = ['| Read-out [block] | Vaccine alone | PSLN-212, aged | PSLN-344, aged | PSLN-212, young | PSLN-344 ÷ PSLN-212 | p |', '|---|---|---|---|---|---|---|']
for r in spec:
    k = r['key']; g = lambda s_: n(f'imm_{k}_{s_}') if f'imm_{k}_{s_}' in N else '—'
    rows.append(f"| {r['label']} [{r['block']}] | {g('sham')} | {g('a212')} | **{g('a344')}** | {g('y212')} | {n(f'imm_{k}_fold')} | {n(f'imm_{k}_p')} |")
rows.append(f"| IgG2a / IgG1 quotient, H1N1 (recomputed) [S13-A ÷ S13-B] | — | {n('ratio_h1_a212')} | **{n('ratio_h1_a344')}** | {n('ratio_h1_y212')} | — | — |")
rows.append(f"| IgG2a / IgG1 quotient, H3N2 (recomputed) [S13-C ÷ S13-D] | — | {n('ratio_h3_a212')} | **{n('ratio_h3_a344')}** | {n('ratio_h3_y212')} | — | — |")
T_IMM = 'Group means (geometric mean titres, GMT, for antibody; HAI = haemagglutination inhibition). p: Tukey test within the block, on log2 titres for antibody. n = 5 per group.\n\n' + '\n'.join(rows)

# ------------------------------------------------------------------ table: biomarkers
spec = json.load(open('_bm_table_spec.json'))
rows = ['| Stage | Marker [block] | PSLN-212, aged: mean (range) | PSLN-344, aged: mean (range) | PSLN-212, young: mean | Overlap between the two aged groups | Accessible equivalent in people |', '|---|---|---|---|---|---|---|']
for r in spec:
    k = r['key']
    y = n(f'bmt_{k}_y') if f'bmt_{k}_y' in N else 'not measured'
    rows.append(f"| {r['stage']} | {r['label']} [{r['block'].split(' (')[0]}] | {n(f'bmt_{k}_m212')} ({n(f'bm_{k}_r212')}) | {n(f'bmt_{k}_m344')} ({n(f'bm_{k}_r344')}) | {y} | {n(f'bmt_{k}_sep')} | {r['human']} |")
T_BM = 'Means are geometric for titres. n = 5 per group. The right-hand column is a proposal; none of these equivalents has been measured by us.\n\n' + '\n'.join(rows)

# ------------------------------------------------------------------ fill
t = open('proposal_template.md').read()
t = t.replace('⟦TABLE:survival⟧', T_SURV).replace('⟦TABLE:immune⟧', T_IMM).replace('⟦TABLE:biomarkers⟧', T_BM)
t = re.sub(r'⟦([A-Za-z0-9_]+)⟧', lambda m: n(m.group(1)), t)
assert '⟦' not in t, re.findall(r'⟦[^⟧]*⟧', t)[:5]
t = re.sub(r'(\d)%–(\d+)%', r'\1–\2%', t)          # '41%–87%' -> '41–87%'
# relative column widths for Word / HTML (pandoc reads them from the dash counts of the separator row)
WIDTHS = {'| Question | Answer |': [22, 78], '| Experiment | Vaccine': [13, 25, 10, 13, 13, 9, 17], '| Read-out [block] |': [36, 9, 10, 10, 10, 12, 13],
          '| Question | What the data show |': [13, 50, 37], '| Dimension | Assessment |': [24, 14, 62], '| Step | Evidence': [15, 72, 13],
          '| Stage | Marker [block] |': [12, 22, 13, 13, 9, 9, 22], '| Segment | Include': [22, 14, 32, 32], '| Element | Plan |': [14, 86],
          '| Option | Verdict | Why |': [22, 13, 65], '| Study | Question it must answer |': [17, 22, 15, 20, 14, 12], '| Gate | When |': [6, 13, 42, 39], '| Explanation | Verdict | Why |': [22, 13, 65], '| ID | Where |': [5, 13, 32, 30, 20], '| File | Content |': [35, 65]}
lines = t.split('\n'); n_set = 0
for i in range(len(lines) - 1):
    if lines[i].startswith('|') and re.fullmatch(r'\|(-+\|)+', lines[i + 1].strip()):
        for head, w in WIDTHS.items():
            if lines[i].startswith(head):
                assert lines[i + 1].count('|') - 1 == len(w), (head, lines[i + 1])
                lines[i + 1] = '|' + '|'.join('-' * max(3, x) for x in w) + '|'; n_set += 1
                break
        else:
            raise ValueError('no width spec for table: ' + lines[i][:60])
t = '\n'.join(lines)
open('../PSLN_portfolio_proposal.md', 'w').write(t)
LED['used_in_proposal'] = LED.key.isin(used)
LED = LED.sort_values(['used_in_proposal', 'id'], ascending=[False, True])
LED.to_csv('../tables/T0_evidence_ledger.csv', index=False)
print('tables with widths:', n_set, '| placeholders filled:', len(used), '| ledger entries:', len(LED), '| words:', len(re.findall(r'\w+', t)))
