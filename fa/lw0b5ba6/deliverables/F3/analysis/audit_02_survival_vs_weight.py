"""Audit 2: reconcile every survival table with the body-weight table recorded for the same animals.

Body-weight tables use two conventions for animals that leave the study:
  (a) BLANK - cells are empty after the animal is gone (used for Sham / Naive / some other groups);
  (b) LOCF  - the last value is repeated unchanged to day 14 (a constant terminal run).
Decoding rule for (b): a terminal run of >=3 identical values, or of 2 identical values below 90 %, is
treated as an animal that has left the study.  (Three survivors end on two identical values >=97 %;
these are kept as survivors: S08!E25:E26, S15!Z19:Z20, S15!AA89:AA90.)
"""
import numpy as np, pandas as pd
from psln_blocks import df

pairs = [  # (survival block, weight block, description)
 ('S03-I','S13-F','aged BALB/c | bivalent vaccine | 10x mLD50 CA09 H1N1, day 14 (homologous)'),
 ('S03-J','S13-G','aged BALB/c | rgH5N1 vaccine | wild-type VN04 H5N1, day 2'),
 ('S06-A','S15-A','aged BALB/c | H3N2 vaccine | 5x mLD50 PR8 H1N1, day 14'),
 ('S06-B','S15-B','aged BALB/c | H3N2 vaccine | 5x mLD50 PR8 H1N1, day 3'),
 ('S06-C','S15-C','aged BALB/c | bivalent vaccine | 5x mLD50 rgH5N1, day 14'),
 ('S06-D','S15-D','aged BALB/c | bivalent vaccine | 5x mLD50 rgH5N1, day 3'),
 ('S06-E(r34)','S15-E','aged BALB/c | H3N2 vaccine | 5x mLD50 PR8 H1N1, day 60'),
 ('S06-F(r34)','S15-F','aged BALB/c | bivalent vaccine | 5x mLD50 rgH5N1, day 60'),
 ('S06-G','S15-G','aged BALB/c | H1N1 vaccine | 5x mLD50 Perth H3N2, day 60'),
 ('S15-H','S15-I','aged BALB/c | vaccine / PSLN-344 / both, 3 days before 5x mLD50 rgH5N1'),
 ('S06-E(r71)','S15-J','14-month BALB/c +/- PR8 imprinting | bivalent vaccine | 5x LD50 PR8 H1N1'),
 ('S06-F(r71)','S15-K','14-month BALB/c +/- PR8 imprinting | bivalent vaccine | 5x LD50 Perth H3N2, day 14'),
 ('S15-L','S15-M','aged C57BL/6 (20 mo) | bivalent vaccine | challenge not stated'),
 ('S15-N','S15-O','aged Swiss Webster (20 mo) | bivalent vaccine | challenge not stated'),
 ('S09-B','S09-C','young BALB/c | H3N2 vaccine | 5x mLD50 PR8 H1N1, day 21'),
 ('S09-D','S09-E','young BALB/c | H1N1 vaccine | 5x mLD50 Perth H3N2, day 21'),
 ('S09-F','S09-G','young BALB/c | bivalent vaccine | 5x mLD50 rgH5N1, day 180'),
]

def decode_weights(block):
    """Per-animal decode: exit mode, first day without a real measurement, nadir over real observations."""
    d = df[df.block==block]
    days = sorted(d.time.unique())
    out=[]
    for (g,rep),a in d.groupby(['group','rep'],sort=False):
        s = a.set_index('time')['value'].reindex(days).astype(float)
        v = s.values
        present = ~np.isnan(v)
        last_idx = np.where(present)[0].max()
        mode='survivor'; exit_from=None; n_real=len(days)
        if last_idx < len(days)-1:
            mode='BLANK'; exit_from=days[last_idx+1]; n_real=last_idx+1
        else:
            k=len(days)-1
            while k>0 and v[k-1]==v[k]: k-=1
            run=len(days)-k
            if run>=3 or (run==2 and v[-1]<90):
                mode='LOCF'; exit_from=days[k]; n_real=k+1      # first value of the run is kept as the last real weight
        real = s.iloc[:n_real]
        cells = a.sort_values('time').cell.tolist()
        out.append(dict(block=block,group=g,rep=rep,cells=f'{cells[0]}:{cells[-1]}',mode=mode,exit_from=exit_from,
                        last_value=v[present][-1],nadir=float(real.min()),nadir_day=real.idxmin(),
                        day14=(v[-1] if mode=='survivor' else np.nan),
                        trajectory=' '.join('-' if np.isnan(x) else f'{x:.1f}' for x in v)))
    return pd.DataFrame(out)

def timing_match(death_days, exits):
    """How many table deaths can be paired with a weight-table exit?  A BLANK exit first missing at day t means the
    animal was last weighed at t-2, so death in [t-2, t].  A LOCF run starting at day t is compatible with death in
    (t-2, t+2] (terminal weight taken at death, or last live weight carried forward)."""
    from itertools import permutations
    ivs=[]
    for mode,t in exits:
        ivs.append((t-2,t) if mode=='BLANK' else (t-1,t+2))
    dd=list(death_days); best=0
    # greedy bipartite matching (small n) via simple augmenting search
    import networkx as nx
    G=nx.Graph()
    for i,d in enumerate(dd):
        for j,(lo,hi) in enumerate(ivs):
            if lo<=d<=hi: G.add_edge(('d',i),('w',j))
    if G.number_of_edges()==0: return 0
    m=nx.algorithms.matching.max_weight_matching(G,maxcardinality=True)
    return len(m)

if __name__=='__main__':
    pd.set_option('display.width',260); pd.set_option('display.max_rows',500); pd.set_option('display.max_colwidth',90)
    rows=[]; allw=[]
    for sb,wbk,desc in pairs:
        s=df[df.block==sb]; w=decode_weights(wbk); w['paired_survival_block']=sb; allw.append(w)
        gs=list(dict.fromkeys(list(s.group.unique())+list(w.group.unique())))
        for g in gs:
            sg=s[s.group==g]; wg=w[w.group==g]
            has_s=len(sg)>0; has_w=len(wg)>0
            sd=sorted(int(t) for t,e in zip(sg.time,sg.event) if e==1) if has_s else []
            ex=[(m,int(x)) for m,x in zip(wg['mode'],wg.exit_from) if m!='survivor'] if has_w else []
            rows.append(dict(surv_block=sb,weight_block=wbk,design=desc,group=g,
                 surv_n=len(sg) if has_s else np.nan, surv_deaths=len(sd) if has_s else np.nan,
                 surv_death_days=','.join(map(str,sd)) if has_s else '(group absent)',
                 wt_n=len(wg) if has_w else np.nan, wt_exits=len(ex) if has_w else np.nan,
                 wt_exit_detail='; '.join(f'{m}@d{t}' for m,t in ex) if has_w else '(group absent)',
                 deaths_timing_matched=timing_match(sd,ex) if (has_s and has_w and sd and ex) else (0 if has_s and has_w else np.nan)))
    r=pd.DataFrame(rows)
    def status(x):
        if np.isnan(x.surv_n) or np.isnan(x.wt_n): return 'GROUP LABEL PRESENT IN ONLY ONE TABLE'
        if x.surv_n!=x.wt_n: return 'ANIMAL COUNT DIFFERS'
        if x.surv_deaths!=x.wt_exits: return 'DEATH COUNT DIFFERS'
        if x.deaths_timing_matched<x.surv_deaths: return f'count agrees; timing differs for {int(x.surv_deaths-x.deaths_timing_matched)}'
        return 'agree'
    r['status']=r.apply(status,axis=1)
    r.to_csv('audit_02_survival_vs_weight.csv',index=False)
    pd.concat(allw).to_csv('weights_decoded_per_animal.csv',index=False)
    print(r.drop(columns=['design']).to_string())
    print(r.status.value_counts())
