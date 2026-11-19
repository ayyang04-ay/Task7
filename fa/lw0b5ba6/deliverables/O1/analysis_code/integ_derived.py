import pandas as pd, numpy as np
df = pd.read_csv('/tmp/work/tidy.csv')
def vals(b,g): return df[(df.block==b)&(df.group==g)].sort_values('rep').value.values
print('--- S03-B (printed ratio) vs IgG2a/IgG1 computed from S13-A/S13-B, per animal (same row order)')
groups = ['PSLN-212','PSLN-344','PSLN-212(Y)']
comp = {g: vals('S13-A',g)/vals('S13-B',g) for g in groups}
for g in groups:
    pr = vals('S03-B',g)
    best = min(groups, key=lambda h: np.max(np.abs(pr-comp[h])))
    print(f'S03-B printed "{g}": {np.round(pr,4)}  -> matches S13 computed "{best}" (max abs diff {np.max(np.abs(pr-comp[best])):.2e})')
print('--- S03-F vs S13-C/S13-D')
comp = {g: vals('S13-C',g)/vals('S13-D',g) for g in groups}
for g in groups:
    pr = vals('S03-F',g)
    best = min(groups, key=lambda h: np.max(np.abs(pr-comp[h])))
    print(f'S03-F printed "{g}": {np.round(pr,4)}  -> matches S13 computed "{best}" (max abs diff {np.max(np.abs(pr-comp[best])):.2e})')
print('--- S04-B Tfh:Tfr vs (100 - Foxp3%)/Foxp3%')
for g in ['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']:
    f = vals('S04-B_Foxp3',g); r = vals('S04-B_TfhTfr',g)
    print(g, 'max abs diff', np.max(np.abs((100-f)/f - r)).round(6))
print('--- S04-A ICOS subsets: do lo+hi relate to anything?')
for g in ['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']:
    print(g, vals('S04-A_ICOSlo',g), vals('S04-A_ICOShi',g))
