import pandas as pd, numpy as np, json
S = pd.read_csv('block_group_summary.csv'); S['level'] = S.level.fillna('').astype(str)
C = pd.read_csv('block_contrasts.csv'); C['level'] = C.level.fillna('').astype(str)
M = pd.read_csv('mechanism_contrasts.csv')
SV = pd.read_csv('survival_tests.csv'); SC = pd.read_csv('survival_counts.csv'); PO = pd.read_csv('survival_pooled_sensitivity.csv')
K = {}
def g(block, group, level='', field='mean'):
    r = S[(S.block == block) & (S.group == group) & (S.level == level)]
    return float(r[field].iloc[0])
def cells(block, group, level=''):
    r = S[(S.block == block) & (S.group == group) & (S.level == level)]
    return r.cells.iloc[0]
def con(block, prefix, level=''):
    r = C[(C.block == block) & (C.level == level) & C.contrast.str.startswith(prefix)].iloc[0]
    return dict(effect=float(r.effect), lo=float(r.ci_low) if pd.notna(r.ci_low) else None, hi=float(r.ci_high) if pd.notna(r.ci_high) else None,
                p=float(r.p_welch) if pd.notna(r.p_welch) else None, g=float(r.hedges_g) if pd.notna(r.hedges_g) else None)
blocks = [('S01-A_16h', ''), ('S01-A_72h', ''), ('S01-D', '4'), ('S01-D', '6'), ('S01-D', '8'), ('S01-E', '4'), ('S01-F', ''), ('S01-G', ''),
          ('S02-A', ''), ('S02-B', ''), ('S02-C', ''), ('S02-D_CD40', ''), ('S02-D_CD86', ''), ('S02-E', ''), ('S02-F', '16h'), ('S02-F', '36h'), ('S02-F', '72h'),
          ('S03-A', ''), ('S03-C', ''), ('S03-D', ''), ('S03-E', ''), ('S03-G', ''), ('S03-H', ''), ('S03-K', ''), ('S03-L_Aicda', ''), ('S03-L_E47', ''),
          ('S04-A_ICOShi', ''), ('S04-A_ICOSlo', ''), ('S04-B_Foxp3', ''), ('S04-C', ''), ('S04-D', ''),
          ('S05-D', ''), ('S05-E', ''), ('S05-F', ''), ('S05-G', ''), ('S05-H', ''), ('S05-I', ''), ('S07-A', '5'), ('S07-A', '10'), ('S11-E', ''),
          ('S13-A', ''), ('S13-B', ''), ('S13-C', ''), ('S13-D', ''), ('S13-I', ''), ('S13-J', ''), ('S13-H', ''), ('S14-A_H1N1', ''), ('S14-A_H3N2', ''),
          ('S09-A_panel1', 'Ifnb1'), ('S09-A_panel1', 'Il6'), ('S09-A_panel1', 'Ccl2'), ('S09-A_panel1', 'Ccl3'), ('S09-A_panel1', 'Ccl5'), ('S09-A_panel1', 'Tnf'), ('S09-A_panel1', 'Il10'),
          ('S09-A_panel2', 'Il6'), ('S09-A_panel2', 'Tnf'), ('S09-A_panel2', 'Il10'), ('S09-A_panel2', 'Ccl2'),
          ('S08-A', '5'), ('S08-A', '10'), ('S08-A', '20'), ('S08-A', '40'), ('S08-B', '')]
for b, l in blocks:
    key = b + ('_' + l if l else '')
    d = {}
    for grp in S[(S.block == b) & (S.level == l)].group.unique():
        r = S[(S.block == b) & (S.group == grp) & (S.level == l)].iloc[0]
        d[grp] = dict(n=int(r.n), mean=float(r['mean']), sd=float(r.sd) if pd.notna(r.sd) else None,
                      gm=float(r.geo_mean) if pd.notna(r.get('geo_mean', np.nan)) else None, cells=r.cells)
    K[key] = dict(groups=d)
    for pre, name in [('Mn effect in aged', 'mn'), ('Aged PSLN-344 vs young', 'vsY'), ('Adjuvant vs vehicle', 'vsSham'), ('Restoration', 'ri'), ('Mn effect in young', 'mnY'), ('PSLN-344 vs cGAMP', 'vsCMP')]:
        try:
            K[key][name] = con(b, pre, l)
        except IndexError:
            pass
# mechanism
K['mech'] = {r.comparison: dict(block=r.block, m1=r.mean1, sd1=r.sd1, m2=r.mean2, sd2=r.sd2, n1=int(r.n1), n2=int(r.n2), eff=r.effect, p=r.p_welch) for r in M.itertuples()}
# survival
K['surv'] = {f'{r.block}|{r.group}': dict(n=int(r.n), surv=int(r.survivors), deaths=int(r.deaths)) for r in SC.itertuples()}
K['surv_tests'] = {f'{r.block}|{r.g1}|{r.g2}': dict(p_logrank=(None if pd.isna(r.p_logrank) else float(r.p_logrank)), p_fisher=float(r.p_fisher)) for r in SV[SV.kind == 'comparison'].itertuples()}
K['pooled'] = PO.to_dict('records')
ri = C[C.contrast.str.startswith('Restoration')]
json.dump(K, open('keynums.json', 'w'), indent=1, default=float)
print('keys:', len(K))
# print a compact digest to eyeball
def pr(key, grp):
    d = K[key]['groups'][grp]; return f"{d['mean']:.3g}±{d['sd']:.2g}" + (f" (GM {d['gm']:.3g})" if d['gm'] else '')
for key in ['S01-A_16h', 'S02-F_36h', 'S01-D_4', 'S01-F', 'S02-A', 'S02-C', 'S02-D_CD40', 'S04-A_ICOShi', 'S04-B_Foxp3', 'S03-K', 'S03-A', 'S03-C', 'S03-E', 'S03-G', 'S05-F', 'S05-G', 'S05-I', 'S05-E']:
    gs = K[key]['groups']
    print(key, {k: pr(key, k) for k in gs}, 'mn:', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in K[key].get('mn', {}).items()})
