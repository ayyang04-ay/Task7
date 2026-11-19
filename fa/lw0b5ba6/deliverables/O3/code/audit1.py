import pandas as pd, numpy as np, itertools
C = pd.read_csv('/tmp/work/tidy/continuous.csv')
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 500); pd.set_option('display.max_colwidth', 80)

# ---------- 1. Positional duplicate values between different series (same rep index, same value) ----------
C['series'] = C['block'] + ' | ' + C['measurand'] + ' | ' + C['group'] + ' | t=' + C['time'].astype(str)
ser = {k: g.set_index('rep')['value'] for k, g in C.groupby('series')}
rows = []
keys = list(ser)
for a, b in itertools.combinations(keys, 2):
    sa, sb = ser[a], ser[b]
    common = sa.index.intersection(sb.index)
    if len(common) < 2:
        continue
    same = [(i, sa[i]) for i in common if abs(sa[i] - sb[i]) < 1e-9 and not float(sa[i]).is_integer()]
    if len(same) >= 2:
        rows.append(dict(series_a=a, series_b=b, n_common=len(common), n_identical=len(same),
                         values=[round(x, 4) for _, x in same]))
D = pd.DataFrame(rows).sort_values('n_identical', ascending=False)
print('=== Positional identical non-integer values between series (>=2) ===')
print(D.to_string(index=False))

# ---------- 2. Any-position shared non-trivial values between blocks of different measurands ----------
print('\n=== Shared non-integer values across DIFFERENT blocks (any position, >=2 shared) ===')
rows = []
blocks = C.groupby(['block', 'group', 'time'], dropna=False)
bl = {k: set(np.round(g['value'].values, 6)) for k, g in blocks}
for a, b in itertools.combinations(bl, 2):
    if a[0] == b[0]:
        continue
    sh = {x for x in bl[a] & bl[b] if not float(x).is_integer()}
    if len(sh) >= 2:
        rows.append(dict(a=a, b=b, shared=sorted(sh)))
print(pd.DataFrame(rows).to_string(index=False))
