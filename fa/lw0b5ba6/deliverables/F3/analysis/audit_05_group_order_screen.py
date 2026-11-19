"""Audit 5: header-plausibility screen.  In every single-time-point block that contains aged PSLN-212, aged PSLN-344 and
young PSLN-212, where does the PSLN-344 mean sit relative to the other two (0 = aged PSLN-212, 1 = young PSLN-212)?
A block whose headers have been shifted shows up as a value far outside 0-1.  Run after analysis_02.
Output: audit_05_group_order_screen.csv"""
import numpy as np, pandas as pd
D=pd.read_csv('immunology_descriptives.csv'); rows=[]
for b,a in D.groupby('block',sort=False):
    if 'RECOMPUTED' in b: continue
    g=a.set_index('group').centre_on_test_scale
    if {'PSLN-212','PSLN-344','PSLN-212(Y)'}<=set(g.index) and g['PSLN-212(Y)']!=g['PSLN-212']:
        pos=(g['PSLN-344']-g['PSLN-212'])/(g['PSLN-212(Y)']-g['PSLN-212'])
        rows.append(dict(block=b,aged_PSLN212=g['PSLN-212'],aged_PSLN344=g['PSLN-344'],young_PSLN212=g['PSLN-212(Y)'],position=pos,inside_0_1=bool(0<=pos<=1)))
R=pd.DataFrame(rows); R.to_csv('audit_05_group_order_screen.csv',index=False)
print(len(R),'blocks;',int(R.inside_0_1.sum()),'with PSLN-344 between aged PSLN-212 and young PSLN-212'); print(R[~R.inside_0_1].to_string())
