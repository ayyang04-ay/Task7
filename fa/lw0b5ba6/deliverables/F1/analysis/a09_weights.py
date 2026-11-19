"""
Body-weight analysis.
(1) post-challenge morbidity: per-animal nadir (% of day-0 weight) by block/group  -> T12
(2) post-immunisation tolerability (S08-D): nadir, day of nadir, recovery           -> T13
"""
from paths import TABLES, FIGS, OUT as OUTDIR, BUILD, PANDOC
import pandas as pd, numpy as np, warnings
from scipy import stats
import psln_blocks as pb
from stats_util import welch, mwu_exact
warnings.filterwarnings('ignore')
pd.set_option('display.width', 300); pd.set_option('display.max_rows', 4000); pd.set_option('display.max_colwidth', 60)
df = pb.tidy()
w = df[df.kind == 'weight'].copy()
w['col'] = w.cell.str.extract(r'!([A-Z]+)\d+')[0]; w['x'] = w.x.astype(float)

def animal_table(block):
    out = []
    for (g, col), t in w[w.block == block].groupby(['group', 'col'], sort=False):
        t = t.sort_values('x'); xs = t.x.tolist(); vs = t.value.tolist()
        run = 1
        for i in range(len(vs) - 1, 0, -1):
            if vs[i] == vs[i - 1]: run += 1
            else: break
        last = xs[-1]
        dead = (last < max(w[w.block == block].x)) or (run >= 3 and vs[-1] < 99.95) or (run == 2 and vs[-1] < 90)
        out.append(dict(block=block, group=g, col=col, nadir=min(vs), day_nadir=xs[int(np.argmin(vs))], final=vs[-1], inferred_dead=dead, n_points=len(vs)))
    return pd.DataFrame(out)

A = pd.concat([animal_table(b) for b in w.block.unique()], ignore_index=True)
A['max_loss'] = 100 - A.nadir
G = A.groupby(['block', 'group'], sort=False).agg(n=('nadir', 'size'), mean_nadir=('nadir', 'mean'), sd_nadir=('nadir', 'std'), worst=('nadir', 'min'),
                                                  n_loss_ge15=('max_loss', lambda s: int((s >= 15).sum())), n_loss_ge20=('max_loss', lambda s: int((s >= 20).sum())),
                                                  inferred_dead=('inferred_dead', 'sum'),
                                                  mean_nadir_survivors=('nadir', lambda s: np.nan)).reset_index()
for i, r in G.iterrows():
    s = A[(A.block == r.block) & (A.group == r.group) & (~A.inferred_dead)]
    G.loc[i, 'mean_nadir_survivors'] = s.nadir.mean() if len(s) else np.nan
    G.loc[i, 'n_survivors_by_weight'] = len(s)
G.to_csv(TABLES + 'T12_weight_nadir_by_group.csv', index=False)
A.to_csv(TABLES + 'T12b_weight_nadir_by_animal.csv', index=False)
print(G.round(1).to_string())

# --- contrasts on nadir: PSLN-344 aged vs young PSLN-212 benchmark, and vs aged PSLN-212, in every aged challenge block
print('\n--- nadir contrasts (all animals, Welch) ---')
rows = []
for blk in ['S13-F', 'S15-A', 'S15-B', 'S15-C', 'S15-D', 'S15-E', 'S15-F', 'S15-G', 'S15-M', 'S15-O']:
    for a, b in [('PSLN-344', 'PSLN-212(Y)'), ('PSLN-344', 'PSLN-212'), ('PSLN-344', 'Sham')]:
        va = A[(A.block == blk) & (A.group == a)].nadir.to_numpy(); vb = A[(A.block == blk) & (A.group == b)].nadir.to_numpy()
        if len(va) and len(vb):
            r = welch(va, vb); rows.append(dict(block=blk, contrast=f'{a} vs {b}', nadir_a=va.mean(), nadir_b=vb.mean(), diff=r['diff'], lo=r['lo'], hi=r['hi'], p=r['p']))
Cn = pd.DataFrame(rows); print(Cn.round(3).to_string())
Cn.to_csv(TABLES + 'T12c_weight_nadir_contrasts.csv', index=False)
# pooled paired-by-block: PSLN-344 aged vs young
t = Cn[Cn.contrast == 'PSLN-344 vs PSLN-212(Y)']
print('\nmean nadir across', len(t), 'aged-challenge blocks: PSLN-344 aged', t.nadir_a.mean().round(2), 'vs PSLN-212(Y)', t.nadir_b.mean().round(2),
      ' paired t across blocks p =', stats.ttest_rel(t.nadir_a, t.nadir_b).pvalue.round(4), ' sign: 344 lower in', int((t['diff'] < 0).sum()), 'of', len(t))
t2 = Cn[Cn.contrast == 'PSLN-344 vs PSLN-212']
print('mean nadir: PSLN-344 aged', t2.nadir_a.mean().round(2), 'vs PSLN-212 aged', t2.nadir_b.mean().round(2), ' paired t p =', stats.ttest_rel(t2.nadir_a, t2.nadir_b).pvalue.round(4))

# young: PSLN-344Y vs PSLN-212Y
print('\n--- young animals (S09-C/E/G): PSLN-344Y vs PSLN-212Y nadir ---')
for blk in ['S09-C', 'S09-E', 'S09-G']:
    va = A[(A.block == blk) & (A.group == 'PSLN-344Y')].nadir.to_numpy(); vb = A[(A.block == blk) & (A.group == 'PSLN-212Y')].nadir.to_numpy()
    r = welch(va, vb); print(blk, 'PSLN-344Y', va.mean().round(2), 'PSLN-212Y', vb.mean().round(2), 'diff', round(r['diff'], 2), f"[{r['lo']:.2f}, {r['hi']:.2f}]", 'p', round(r['p'], 3))

# --- (2) S08-D tolerability after immunisation (no challenge)
print('\n--- S08-D: weight after intranasal immunisation ---')
T = animal_table('S08-D'); T['max_loss'] = 100 - T.nadir
s = w[w.block == 'S08-D']
day_means = s.groupby(['group', 'x'], sort=False).value.agg(['mean', 'min', 'count']).unstack('x')
print(day_means.round(1).to_string())
tol = T.groupby('group', sort=False).agg(n=('nadir', 'size'), mean_nadir=('nadir', 'mean'), worst_animal=('nadir', 'min'), mean_day_of_nadir=('day_nadir', 'mean'),
                                         n_loss_ge5=('max_loss', lambda s: int((s >= 5).sum())), n_loss_ge10=('max_loss', lambda s: int((s >= 10).sum()))).reset_index()
d10 = s[s.x == 10].groupby('group', sort=False).value.agg(['mean', 'count']).rename(columns={'mean': 'mean_d10', 'count': 'n_d10'})
tol = tol.merge(d10, left_on='group', right_index=True)
print(tol.round(2).to_string())
tol.to_csv(TABLES + 'T13_tolerability_S08D.csv', index=False)
for a, b in [('PSLN-344', 'Vaccine'), ('PSLN-344', 'PSLN-212'), ('PSLN-212/R848', 'Vaccine'), ('PSLN-212/R848', 'PSLN-344'), ('PSLN-212', 'Vaccine'), ('CMP-204', 'Vaccine')]:
    va = T[T.group == a].nadir.to_numpy(); vb = T[T.group == b].nadir.to_numpy(); r = welch(va, vb)
    print(f'nadir {a} vs {b}: diff {r["diff"]:.2f} [{r["lo"]:.2f}, {r["hi"]:.2f}] p={r["p"]:.4f}  MWU exact p={mwu_exact(va, vb):.4f}')
