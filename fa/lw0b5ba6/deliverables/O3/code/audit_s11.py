import pandas as pd, numpy as np
C = pd.read_csv('/tmp/work/tidy/continuous.csv')
a = C[C.block == 'S11-A'][['group', 'time', 'rep', 'value', 'cell']].rename(columns={'value': 'S11A_alveolar_macrophage_pct', 'cell': 'S11A_cell'})
b = C[C.block == 'S11-B'][['group', 'time', 'rep', 'value', 'cell']].rename(columns={'value': 'S11B_neutrophil_pct', 'cell': 'S11B_cell'})
m = a.merge(b, on=['group', 'time', 'rep']); m['identical'] = np.isclose(m.S11A_alveolar_macrophage_pct, m.S11B_neutrophil_pct)
m.to_csv('/tmp/work/tidy/audit_s11.csv', index=False); print('S11-A vs S11-B identical:', int(m.identical.sum()), 'of', len(m))
