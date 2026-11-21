import json, re, shutil, os, subprocess
W = '/tmp/work/'; O = '/tmp/outputs/'
t = open(W + 'proposal_template.md').read()
F = json.load(open(W + 'facts.json'))
tables = {'TABLE1': 't1_headline', 'TABLE2': 't2_survival', 'TABLE3': 't3_pooled', 'TABLE4': 't4_restoration', 'TABLE5': 't5_moa',
          'TABLE6': 't6_biomarkers', 'TABLE7': 't7_integrity', 'TABLE8': 't8_h2h_full', 'TABLE9': 't9_excluded'}
for k, f in tables.items():
    t = t.replace(f'[[{k}]]', open(W + f'snippets/{f}.md').read())
used = set()
def sub(m):
    k = m.group(1)
    if k not in F: raise KeyError(f'missing fact: {k}')
    used.add(k); return str(F[k])
t = re.sub(r'\[\[([A-Za-z0-9_\-\[\]]+?)\]\]', sub, t)
left = re.findall(r'\[\[.*?\]\]', t)
assert not left, left
open(O + 'PSLN_portfolio_proposal.md', 'w').write(t)
json.dump(sorted(used), open(W + 'facts_used.json', 'w'))
print('facts used in text:', len(used), 'of', len(F))

# ---- package outputs ----
import pandas as pd, glob
A = O + 'analysis/'; os.makedirs(A + 'tidy', exist_ok=True); os.makedirs(A + 'audit_logs', exist_ok=True); os.makedirs(O + 'code', exist_ok=True)
for f in ['values.csv', 'tte.csv', 'bw.csv', 's08_unlabeled.csv']: shutil.copy(W + 'tidy/' + f, A + 'tidy/' + f)
shutil.copy(W + 'h2h.csv', A + 'h2h_endpoints.csv')
for f in ['survival_by_group.csv', 'survival_pairwise.csv', 'survival_pooled.csv', 'survival_pooled_arms.csv', 'survival_loo.csv',
          'restoration_index.csv', 'restoration_by_layer.csv', 'biomarker_table.csv', 'moa_contrasts.csv', 'dose_response.csv',
          'reactogenicity_s08d.csv', 'integrity_register.csv', 'bw_vs_tte.csv']:
    shutil.copy(W + f, A + f)
for f in glob.glob(W + 'logs/*.log'): shutil.copy(f, A + 'audit_logs/')
Lg = pd.read_csv(W + 'evidence_ledger.csv'); Lg['used_in_proposal_text'] = Lg.key.isin(used)
Lg.to_csv(A + 'evidence_ledger.csv', index=False)
for f in ['parse.py', 'audit.py', 'fingerprint.py', 'fp_breakdown.py', 'bw_recycle.py', 'tte_bw_check.py', 'crosscheck.py', 'h2h.py', 'survival.py',
          'newcombe.py', 'strat.R', 'moa.py', 'restoration.py', 'biomarkers.py', 'power.py', 'extra_checks.py', 'integrity_register.py',
          'build_tables.py', 'facts.py', 'figures.py', 'fig5.py', 'render.py', 'proposal_template.md', 'run_all.sh', 'dump.py', 'fp_breakdown.py', 'qa_independent.py', 'style.css']:
    shutil.copy(W + f, O + 'code/' + f)
print('packaged')
