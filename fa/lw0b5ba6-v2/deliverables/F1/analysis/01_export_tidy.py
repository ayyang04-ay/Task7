"""Export every block to one tidy CSV (+ a block index with stated-vs-observed n)."""
import pandas as pd, numpy as np
import psln_blocks as P

rows = []; idx = []
for bid, b in P.BLOCKS.items():
    df = P.load(bid).copy()
    df['sheet'] = b['sheet']; df['kind'] = b['kind']
    rows.append(df)
    if b['kind'] in ('tc', 'bw') and b.get('xcol'):
        n_by = df.groupby(['group', 'x'], sort=False).size()
        obs = {g: sorted(set(int(v) for v in n_by[g].values)) for g in df['group'].unique()}
    else:
        obs = {g: [int(n)] for g, n in df.groupby('group', sort=False).size().items()}
    idx.append(dict(block=bid, printed_label=b.get('printed_label', bid), sheet=b['sheet'], kind=b['kind'], stated_n=b['stated_n'],
                    observed_n_per_group='; '.join(f"{g}: {'/'.join(map(str, v))}" for g, v in obs.items()),
                    n_mismatch=any(any(x != b['stated_n'] for x in v) for v in obs.values()),
                    measurand=b.get('measurand', b.get('model', '')), time=b.get('time', ''), pair=b.get('pair', '')))
tidy = pd.concat(rows, ignore_index=True)
tidy.to_csv('../data_tidy/psln_tidy_all_blocks.csv', index=False)
pd.DataFrame(idx).to_csv('../data_tidy/psln_block_index.csv', index=False)
print(tidy.shape)
print(pd.DataFrame(idx)[['block', 'stated_n', 'observed_n_per_group', 'n_mismatch']].to_string())
