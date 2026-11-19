"""
Cross-check each time-to-event block against its paired body-weight block.
Death is inferred from a weight trace when (a) cells go blank before day 14, or
(b) the trace ends in >=2 identical carried-forward values (LOCF) -- both conventions
are used in the workbook.  Output: per block/group, deaths per survival table vs deaths per weights.
"""
from paths import TABLES, FIGS, OUT as OUTDIR, BUILD, PANDOC
import pandas as pd, numpy as np, psln_blocks as pb
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 2000); pd.set_option('display.max_colwidth', 200)
df = pb.tidy()

PAIRS = [  # (survival block, weight block, description)
 ('S03-I', 'S13-F', 'aged BALB/c, bivalent vacc, 10xLD50 CA09 H1N1 d14'),
 ('S03-J', 'S13-G', 'rgH5N1 vacc, wt VN04 H5N1 d2'),
 ('S06-A', 'S15-A', 'Aichi H3N2 vacc, PR8 H1N1 d14'),
 ('S06-B', 'S15-B', 'Aichi H3N2 vacc, PR8 H1N1 d3'),
 ('S06-C', 'S15-C', 'bivalent vacc, rgH5N1 d14'),
 ('S06-D', 'S15-D', 'bivalent vacc, rgH5N1 d3'),
 ('S06-E (rows 34-68)', 'S15-E', 'Aichi vacc, PR8 d60'),
 ('S06-F (rows 34-68)', 'S15-F', 'bivalent vacc, rgH5N1 d60'),
 ('S06-G', 'S15-G', 'CA09 vacc, Perth H3N2 d60'),
 ('S06-E (rows 71-105)', 'S15-J', 'imprinting, PR8'),
 ('S06-F (rows 71-105)', 'S15-K', 'imprinting, Perth H3N2'),
 ('S09-B', 'S09-C', 'young, Aichi vacc, PR8 d21'),
 ('S09-D', 'S09-E', 'young, CA09 vacc, Perth d21'),
 ('S09-F', 'S09-G', 'young, bivalent, rgH5N1 d180'),
 ('S15-H', 'S15-I', 'aged, 3d, rgH5N1'),
 ('S15-L', 'S15-M', 'C57BL/6'),
 ('S15-N', 'S15-O', 'Swiss Webster'),
]

def weight_traces(block):
    w = df[(df.block == block)].copy()
    w['x'] = w.x.astype(float)
    w['col'] = w.cell.str.extract(r'!([A-Z]+)\d+')[0]
    out = []
    for (g, col), t in w.groupby(['group', 'col'], sort=False):
        t = t.sort_values('x')
        xs = list(t.x); vs = list(t.value)
        last_x = xs[-1]
        # LOCF run at the end
        run = 1
        for i in range(len(vs) - 1, 0, -1):
            if vs[i] == vs[i - 1]:
                run += 1
            else:
                break
        status = 'alive'
        death_after = None
        if last_x < 14:
            status = 'dead(blank)'; death_after = last_x
        elif run >= 2 and vs[-1] < 99.95:   # carried-forward tail
            status = 'dead(LOCF)' if run >= 3 or vs[-1] < 90 else 'ambiguous(2 equal)'
            death_after = xs[len(vs) - run]
        out.append(dict(group=g, col=col, status=status, last_weigh_day=death_after, nadir=min(vs), final=vs[-1], n=len(vs)))
    return pd.DataFrame(out)

rows = []
for sb, wb_, desc in PAIRS:
    s = df[df.block == sb]
    w = weight_traces(wb_)
    groups = list(dict.fromkeys(list(s.group.unique()) + list(w.group.unique())))
    for g in groups:
        sg = s[s.group == g]; wg = w[w.group == g]
        rows.append(dict(surv_block=sb, weight_block=wb_, desc=desc, group=g,
                         surv_n=len(sg) if len(sg) else None,
                         surv_deaths=int((sg.event == 1).sum()) if len(sg) else None,
                         surv_death_days=sorted(sg[sg.event == 1].value.tolist()) if len(sg) else None,
                         wt_n=len(wg) if len(wg) else None,
                         wt_deaths=int(wg.status.str.startswith('dead').sum()) if len(wg) else None,
                         wt_ambig=int((wg.status == 'ambiguous(2 equal)').sum()) if len(wg) else None,
                         wt_last_weigh_days=sorted(wg[wg.status.str.startswith('dead')].last_weigh_day.tolist()) if len(wg) else None,
                         wt_convention=','.join(sorted(set(x.split('(')[1].rstrip(')') for x in wg.status if x.startswith('dead')))) if len(wg) else None))
res = pd.DataFrame(rows)
def verdict(r):
    if r.surv_n is None or pd.isna(r.surv_n): return 'group only in weight block'
    if r.wt_n is None or pd.isna(r.wt_n): return 'group only in survival block'
    if r.surv_n != r.wt_n: return f'N MISMATCH ({int(r.surv_n)} vs {int(r.wt_n)})'
    if r.surv_deaths == r.wt_deaths: return 'agree'
    if r.wt_ambig and abs(r.surv_deaths - r.wt_deaths) <= r.wt_ambig: return 'agree if ambiguous traces are deaths'
    return f'DEATH COUNT MISMATCH ({int(r.surv_deaths)} vs {int(r.wt_deaths)})'
res['verdict'] = res.apply(verdict, axis=1)
res.to_csv(TABLES + 'T2_survival_vs_weight_crosscheck.csv', index=False)
print(res[['surv_block','weight_block','group','surv_n','surv_deaths','surv_death_days','wt_n','wt_deaths','wt_ambig','wt_last_weigh_days','wt_convention','verdict']].to_string())
