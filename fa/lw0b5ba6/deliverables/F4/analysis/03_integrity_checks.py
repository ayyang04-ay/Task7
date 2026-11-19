#!/usr/bin/env python
"""
03_integrity_checks.py -- reproducible data-integrity checks on the workbook.
Run: micromamba run -n core python 03_integrity_checks.py
Writes tables/T01_integrity_evidence_*.csv and prints the evidence quoted in the proposal (Appendix A).
Nothing is "fixed" silently: each check prints what was found; the proposal states how each item was handled.
"""
import os, collections, itertools
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, 'parsed'); T = os.path.join(HERE, 'tables')
sc = pd.read_csv(f'{P}/scalar_long.csv', keep_default_na=False); sc['factor'] = sc.factor.astype(str)
sv = pd.read_csv(f'{P}/survival_long.csv', keep_default_na=False); sv['day'] = pd.to_numeric(sv.day, errors='coerce')
wt = pd.read_csv(f'{P}/weight_long.csv', keep_default_na=False)
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 500); pd.set_option('display.max_colwidth', 150)

def grp(block, level=None):
    d = sc[sc.block == block]
    if level is not None: d = d[d.factor == level]
    return {g: x.sort_values('rep').value.values for g, x in d.groupby('group', sort=False)}

print('=' * 100); print('CHECK 1  S03-B / S03-F (IgG2a:IgG1 quotient) recomputed from S13-A..D subclass titres')
rows = []
for ratio_blk, num, den, virus in [('S03-B', 'S13-A', 'S13-B', 'CA09 H1N1'), ('S03-F', 'S13-C', 'S13-D', 'Aichi H3N2')]:
    n, d, r = grp(num), grp(den), grp(ratio_blk)
    rec = {g: n[g] / d[g] for g in n}
    for g_print, vals in r.items():
        # which recomputed group does the printed column match?
        match = [g for g in rec if np.allclose(rec[g], vals, rtol=2e-3)]
        rows.append(dict(block=ratio_blk, virus=virus, printed_header=g_print, printed_values=np.round(vals, 3).tolist(),
                         matches_recomputed_group=match[0] if match else 'none',
                         recomputed_for_printed_header=np.round(rec[g_print], 3).tolist(),
                         mean_as_printed=round(float(np.mean(vals)), 3), mean_recomputed=round(float(np.mean(rec[g_print])), 3)))
c1 = pd.DataFrame(rows); print(c1.to_string()); c1.to_csv(f'{T}/T01a_integrity_S03B_S03F_label_rotation.csv', index=False)

print('=' * 100); print('CHECK 2  S09-A (log10) against S01-A (linear) -- timepoint of the second S09-A panel; control identity')
rows = []
for blk in ['S09-A(cols A-V)', 'S09-A(cols X-AS)']:
    d = sc[(sc.block == blk) & (sc.factor == 'Ifnb1')]
    for g, x in d.groupby('group', sort=False):
        lin = np.round(10 ** x.value.values, 2)
        g1 = {'PBS': 'Sham', 'PSLN-212(y)': 'PSLN-212(Y)'}.get(g, g)
        for tp in ['16h', '72h']:
            ref = np.round(grp('S01-A', tp)[g1], 2)
            rows.append(dict(S09A_panel=blk, group=g, back_transformed=lin.tolist(), S01A_panel=tp, S01A_group=g1,
                             n_values_found_in_S01A=int(sum(v in ref for v in lin))))
c2 = pd.DataFrame(rows); print(c2.to_string()); c2.to_csv(f'{T}/T01b_integrity_S09A_vs_S01A.csv', index=False)
print(c2.groupby(['S09A_panel', 'S01A_panel']).n_values_found_in_S01A.sum())

print('=' * 100); print('CHECK 3  S11-A (alveolar macrophages) vs S11-B (neutrophils): identical values in the same cell position')
a = sc[sc.block == 'S11-A'].set_index(['group', 'factor', 'rep']).value; b = sc[sc.block == 'S11-B'].set_index(['group', 'factor', 'rep']).value
d = pd.concat([a.rename('S11A'), b.rename('S11B')], axis=1); d['same'] = d.S11A == d.S11B
print('identical same-position values:', int(d.same.sum()), 'of', len(d)); print(d.groupby(['group', 'rep']).same.sum().unstack())
d.reset_index().to_csv(f'{T}/T01c_integrity_S11A_vs_S11B.csv', index=False)

print('=' * 100); print('CHECK 4  S08-C vs S01-B (alveolar epithelial SRB uptake)')
print('S01-B', {k: v.tolist() for k, v in grp('S01-B').items()}); print('S08-C', {k: v.tolist() for k, v in grp('S08-C').items()})
print('means S01-B', {k: round(v.mean(), 2) for k, v in grp('S01-B').items()}); print('means S08-C', {k: round(v.mean(), 2) for k, v in grp('S08-C').items()})

print('=' * 100); print('CHECK 5  survival tables: identical time-to-event vectors in different blocks; missing days')
vec = {(b, g): tuple(sorted(zip(x.day.fillna(-1).astype(int), x.event))) for (b, g), x in sv.groupby(['block', 'group'], sort=False)}
ks = list(vec)
for i, j in itertools.combinations(range(len(ks)), 2):
    if vec[ks[i]] == vec[ks[j]] and sum(e for _, e in vec[ks[i]]) >= 3 and ks[i][0] != ks[j][0]:
        print('  identical:', ks[i], ks[j], 'death days', [dd for dd, e in vec[ks[i]] if e == 1])
print('  records with event flag but no day:', sv[sv.day.isna()][['block', 'group', 'cell']].to_dict('records'))

print('=' * 100); print('CHECK 6  survival table vs paired body-weight table (deaths inferred from weights: blank-after or frozen/LOCF-to-end)')
pairs = [('S03-I', 'S13-F'), ('S03-J', 'S13-G'), ('S06-A', 'S15-A'), ('S06-B', 'S15-B'), ('S06-C', 'S15-C'), ('S06-D', 'S15-D'),
         ('S06-E', 'S15-E'), ('S06-F', 'S15-F'), ('S06-G', 'S15-G'), ('S15-H', 'S15-I'), ('S06-E(r71)', 'S15-J'), ('S06-F(r71)', 'S15-K'),
         ('S15-L', 'S15-M'), ('S15-N', 'S15-O'), ('S09-B', 'S09-C'), ('S09-D', 'S09-E'), ('S09-F', 'S09-G')]
def infer(series, days):
    obs = [x for x in days if x in series]; last = obs[-1]
    if last < days[-1]: return 'dead', last, 'blank'
    v_end = series[last]; k = len(obs) - 1
    while k > 0 and series[obs[k - 1]] == v_end: k -= 1
    run = len(obs) - 1 - k
    if run >= 2: return 'dead', obs[k], 'LOCF'
    if run == 1: return 'ambiguous', obs[k], 'last2equal'
    return 'alive', last, ''
rows = []; anim = []
for sb, wb_ in pairs:
    w = wt[wt.block == wb_]; days = sorted(w.day.unique()); s = sv[sv.block == sb]
    for g in list(dict.fromkeys(list(w.group.unique()) + list(s.group.unique()))):
        wg, sg = w[w.group == g], s[s.group == g]
        r = dict(surv_block=sb, weight_block=wb_, group=g)
        if len(wg):
            res = []
            for a_, x in wg.groupby('animal'):
                st = infer(dict(zip(x.day, x.value)), days); res.append(st)
                anim.append(dict(weight_block=wb_, group=g, animal=a_, status=st[0], last_real_day=st[1], how=st[2]))
            r.update(wt_n=len(res), wt_deaths=sum(x[0] == 'dead' for x in res), wt_ambiguous=sum(x[0] == 'ambiguous' for x in res),
                     wt_LOCF=sum(x[2] == 'LOCF' for x in res), wt_blank=sum(x[2] == 'blank' for x in res),
                     wt_last_real_days=' '.join(str(x[1]) for x in sorted(res, key=lambda z: z[1]) if x[0] == 'dead'))
        if len(sg):
            r.update(surv_n=len(sg), surv_deaths=int(sg.event.sum()), surv_death_days=' '.join(str(int(x)) for x in sorted(sg[sg.event == 1].day)))
        if len(wg) and len(sg):
            lo, hi = r['wt_deaths'], r['wt_deaths'] + r['wt_ambiguous']
            r['verdict'] = 'agree' if r['surv_deaths'] == lo else ('agree if ambiguous=dead' if lo < r['surv_deaths'] <= hi else 'DISAGREE')
        else:
            r['verdict'] = 'group present in only one of the two blocks'
        rows.append(r)
c6 = pd.DataFrame(rows); c6.to_csv(f'{T}/T01d_integrity_survival_vs_weight.csv', index=False)
print(c6.to_string())
print(c6.verdict.value_counts())
pd.DataFrame(anim).to_csv(f'{T}/T01e_weight_animal_status.csv', index=False)

print('=' * 100); print('CHECK 7  body-weight tables: trajectories re-used across experiments (identical or integer-shifted values at the same days)')
w = wt[wt.day > 0]
traj = {(b, g, a): dict(zip(x.day, x.value.round(5))) for (b, g, a), x in w.groupby(['block', 'group', 'animal'], sort=False)}
status = {(r['weight_block'], r['group'], r['animal']): r for r in anim}
def real_days(k):
    st = status.get(k); t = traj[k]
    if st and st['status'] == 'dead' and st['how'] == 'LOCF': return {d_: v for d_, v in t.items() if d_ <= st['last_real_day']}
    return t
keys = list(traj); rows = []
for i, j in itertools.combinations(range(len(keys)), 2):
    if keys[i][0] == keys[j][0]: continue                    # different blocks only
    A, B = real_days(keys[i]), real_days(keys[j]); common = sorted(set(A) & set(B))
    if len(common) < 4: continue
    same = [d_ for d_ in common if A[d_] == B[d_]]
    shifted = [d_ for d_ in common if A[d_] != B[d_] and abs(((A[d_] - B[d_]) + 0.5) % 1 - 0.5) < 1e-4 and round(A[d_], 2) != A[d_]]
    if len(same) >= 4 or len(same) + len(shifted) >= 4:
        rows.append(dict(a_block=keys[i][0], a_group=keys[i][1], a_animal=keys[i][2], b_block=keys[j][0], b_group=keys[j][1], b_animal=keys[j][2],
                         n_common_days=len(common), n_identical=len(same), n_integer_shifted=len(shifted)))
c7 = pd.DataFrame(rows).sort_values(['n_identical', 'n_integer_shifted'], ascending=False)
c7.to_csv(f'{T}/T01f_integrity_weight_trajectory_reuse.csv', index=False)
print(c7.to_string()); print('animal-trajectory pairs flagged:', len(c7))
bp = c7.groupby(['a_block', 'a_group', 'b_block', 'b_group']).size().reset_index(name='n_animal_pairs').sort_values('n_animal_pairs', ascending=False)
print(bp.to_string())
# within-block row duplication (same day, two groups identical)
for b_, x in wt.groupby('block'):
    for d_, y in x.groupby('day'):
        if d_ == 0: continue
        gs = {g: tuple(z.sort_values('animal').value) for g, z in y.groupby('group')}
        for g1, g2 in itertools.combinations(gs, 2):
            if gs[g1] == gs[g2] and len(gs[g1]) >= 4: print('  identical row within block:', b_, 'day', d_, g1, '==', g2, gs[g1])

print('=' * 100); print('CHECK 8  high-precision body-weight values: fractional parts recurring across blocks')
def ndec(x):
    s = repr(float(x)); return len(s.split('.')[1]) if '.' in s and s.split('.')[1] != '0' else 0
hp = wt[(wt.day > 0) & (wt.value.apply(ndec) >= 4)].copy(); hp['frac'] = (hp.value % 1).round(4)
g = hp.groupby('frac').agg(n_cells=('value', 'size'), n_blocks=('block', 'nunique'), where=('block', lambda s: ' '.join(sorted(set(s))))).reset_index()
print('values with >=4 decimals:', len(hp), '| distinct fractional parts:', len(g), '| fractional parts seen in >=2 blocks:', int((g.n_blocks >= 2).sum()),
      '| cells involved:', int(g[g.n_blocks >= 2].n_cells.sum()))
g.sort_values(['n_blocks', 'n_cells'], ascending=False).to_csv(f'{T}/T01g_integrity_weight_fraction_reuse.csv', index=False)
print(g.sort_values(['n_blocks', 'n_cells'], ascending=False).head(12).to_string())

print('=' * 100); print('CHECK 9  stated n vs observations; labels')
lab = {'S03-J': 9, 'S13-E': 5, 'S05-A': 3, 'S05-B': 3, 'S09-F': 8}
for b_, n in lab.items():
    if b_ in set(sv.block): print(' ', b_, 'stated n', n, '| rows per group', sv[sv.block == b_].groupby('group', sort=False).size().to_dict())
    else: print(' ', b_, 'stated n', n, '| obs per group per day', sc[sc.block == b_].groupby(['group', 'factor'], sort=False).size().unique().tolist())
print('  S07-C printed group labels are identical for both columns; S08 rows 89-101 carry no labels:', sv[sv.block == 'S08-unlabelled'].groupby('group').size().to_dict())

print('=' * 100); print('CHECK 10  terminal-digit distribution of values recorded to a fixed number of decimals (measured data should be near-uniform)')
from scipy import stats as _st
def _ndec(t):
    r = repr(float(t)).split('.')[1]; return 0 if r == '0' else len(r)
rows = []
for dec in (1, 2):
    cnt = np.zeros(10, int)
    for b_, y in sc.groupby('block'):
        nd = y.value.apply(_ndec)
        if (nd <= dec).mean() >= 0.95 and (nd == dec).mean() >= 0.5:        # block recorded to `dec` decimals
            v = y.value[nd <= dec]; cnt += np.bincount((np.round(v * 10 ** dec).astype(int) % 10), minlength=10)
    chi = _st.chisquare(cnt); rows.append(dict(data=f'immunology / qPCR blocks recorded to {dec} decimal(s)', n=int(cnt.sum()), counts_digit_0_to_9=cnt.tolist(), chi2=round(chi.statistic, 1), p=chi.pvalue))
_st_map = {(r['weight_block'], r['group'], r['animal']): r for r in anim}          # drop carried-forward repeats before counting digits
def _real(r):
    s_ = _st_map.get((r.block, r.group, r.animal))
    return not (s_ and s_['status'] == 'dead' and s_['how'] == 'LOCF' and r.day > s_['last_real_day'])
w1 = wt[(wt.day > 0) & (wt.value.apply(_ndec) <= 1)]
w1 = w1[[_real(r) for r in w1.itertuples()]]
cnt = np.bincount((np.round(w1.value * 10).astype(int) % 10), minlength=10); chi = _st.chisquare(cnt)
rows.append(dict(data='body weights recorded to 1 decimal (day > 0, carried-forward repeats removed)', n=int(cnt.sum()), counts_digit_0_to_9=cnt.tolist(), chi2=round(chi.statistic, 1), p=chi.pvalue))
c10 = pd.DataFrame(rows); c10.to_csv(f'{T}/T01h_integrity_terminal_digits.csv', index=False); print(c10.to_string())
