"""Observation counts per block/group (as found in the workbook)."""
from paths import TABLES, FIGS, OUT as OUTDIR, BUILD, PANDOC
import pandas as pd, psln_blocks as pb
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 2000); pd.set_option('display.max_columns', 50)
df = pb.tidy()
# counts: for series/weight -> per timepoint
def summarize(g):
    if g.kind.iloc[0] in ('series', 'weight'):
        per_x = g.groupby('x', sort=False).size()
        return pd.Series({'n_obs': f"{per_x.min()}-{per_x.max()}" if per_x.min()!=per_x.max() else str(per_x.max()),
                          'timepoints': len(per_x), 'detail': ' '.join(f'{k}:{v}' for k, v in per_x.items())})
    elif g.kind.iloc[0] == 'surv':
        return pd.Series({'n_obs': str(len(g)), 'timepoints': 1,
                          'detail': f"events={int((g.event==1).sum())} censored={int((g.event==0).sum())} days={list(g.value)}"})
    else:
        return pd.Series({'n_obs': str(len(g)), 'timepoints': 1, 'detail': ''})
out = df.groupby(['sheet', 'block', 'analyte', 'group'], sort=False).apply(summarize, include_groups=False).reset_index()
out.to_csv(TABLES + 'T1_observation_counts.csv', index=False)
print(out.to_string())
