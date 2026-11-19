"""Audit 1: stated n (as printed in each block label) versus observations actually present."""
import re, pandas as pd
from psln_blocks import df, wb

# stated n by block label -------------------------------------------------------------
label_cells = {
 'S01-A/16h':('S01','A1'),'S01-A/72h':('S01','A1'),'S01-B':('S01','A13'),'S01-C':('S01','A19'),'S01-D':('S01','A23'),
 'S01-E':('S01','A29'),'S01-F':('S01','A35'),'S01-G':('S01','A37'),
 'S02-A':('S02','A1'),'S02-B':('S02','F1'),'S02-C':('S02','K1'),'S02-D CD40':('S02','A8'),'S02-D CD86':('S02','F8'),
 'S02-E':('S02','K8'),'S02-F':('S02','A15'),'S02-G':('S02','A20'),'S02-H':('S02','A28'),'S02-I':('S02','G28'),
 'S03-A':('S03','A1'),'S03-B':('S03','G1'),'S03-C':('S03','K1'),'S03-D':('S03','Q1'),'S03-E':('S03','A8'),
 'S03-F':('S03','G8'),'S03-G':('S03','K8'),'S03-H':('S03','Q8'),'S03-I':('S03','A15'),'S03-J':('S03','G15'),
 'S03-K':('S03','K15'),'S03-L/Aicda':('S03','K25'),'S03-L/E47':('S03','K25'),
 'S04-A/ICOSlo':('S04','A1'),'S04-A/ICOShi':('S04','A1'),'S04-B Foxp3':('S04','A6'),'S04-B Tfh:Tfr':('S04','A13'),
 'S04-C':('S04','A20'),'S04-D':('S04','A27'),
 'S05-A':('S05','A1'),'S05-B':('S05','A6'),'S05-C':('S05','A11'),'S05-D':('S05','A17'),'S05-E':('S05','A24'),
 'S05-F':('S05','A31'),'S05-G':('S05','A38'),'S05-H':('S05','A45'),'S05-I':('S05','A52'),
 'S06-A':('S06','A1'),'S06-B':('S06','G1'),'S06-C':('S06','M1'),'S06-D':('S06','A32'),'S06-E(r34)':('S06','G32'),
 'S06-F(r34)':('S06','M32'),'S06-G':('S06','A69'),'S06-E(r71)':('S06','G69'),'S06-F(r71)':('S06','M69'),
 'S07-A':('S07','A1'),'S07-B/Mono':('S07','A8'),'S07-B/Ly6C+Mac':('S07','A8'),'S07-C':('S07','A15'),
 'S08-A':('S08','A1'),'S08-B':('S08','A9'),'S08-C':('S08','A12'),'S08-D':('S08','A19'),
 'S09-A/panel1(A-V)':('S09','A1'),'S09-A/panel2(X-AS)':('S09','X1'),'S09-B':('S09','A10'),'S09-C':('S09','E10'),
 'S09-D':('S09','A37'),'S09-E':('S09','F37'),'S09-F':('S09','A64'),'S09-G':('S09','F64'),
 'S10-A/Ifnb1':('S10','A1'),'S10-A/Tnf':('S10','A1'),'S10-A/Isg15':('S10','A1'),
 'S11-A':('S11','A1'),'S11-B':('S11','A8'),'S11-C':('S11','A15'),'S11-D':('S11','A22'),'S11-E':('S11','A29'),
 'S12-A':('S12','A1'),
 'S13-A':('S13','A1'),'S13-B':('S13','E1'),'S13-C':('S13','I1'),'S13-D':('S13','M1'),'S13-E':('S13','R1'),
 'S13-F':('S13','A31'),'S13-G':('S13','A42'),'S13-H':('S13','A51'),'S13-I':('S13','E51'),'S13-J':('S13','K51'),
 'S14-A H1N1':('S14','A1'),'S14-A H3N2':('S14','E1'),
 'S15-A':('S15','A1'),'S15-B':('S15','A11'),'S15-C':('S15','A21'),'S15-D':('S15','A31'),'S15-E':('S15','A41'),
 'S15-F':('S15','A51'),'S15-G':('S15','A61'),'S15-H':('S15','A71'),'S15-I':('S15','G71'),'S15-J':('S15','G81'),
 'S15-K':('S15','G91'),'S15-L':('S15','A101'),'S15-M':('S15','G101'),'S15-N':('S15','A132'),'S15-O':('S15','G132'),
}
rows=[]
for blk,(sh,cell) in label_cells.items():
    lab = wb[sh][cell].value
    m = re.search(r'n\s*=\s*(\d+)', str(lab))
    stated = int(m.group(1)) if m else None
    d = df[df.block==blk]
    if d.kind.iloc[0]=='survival':
        cnt = d.groupby('group').size()
    elif 'time' in d and d.time.notna().any() and d.kind.iloc[0] in ('timecourse','weight'):
        # count at first timepoint (baseline) and min across timepoints
        cnt0 = d[d.time==d.time.iloc[0]].groupby('group').size()
        cntmin = d.groupby(['group','time']).size().groupby('group').min()
        cnt = cnt0
    else:
        if 'analyte' in d and d.analyte.notna().any() and blk.startswith('S09-A'):
            cnt = d.groupby(['group','analyte']).size().groupby('group').max()
        else:
            cnt = d.groupby('group').size()
    obs = sorted(set(cnt.values))
    rows.append(dict(block=blk,label_cell=f'{sh}!{cell}',label=lab,stated_n=stated,
                     observed_n_by_group='; '.join(f'{g}={n}' for g,n in cnt.items()),
                     match = (obs==[stated])))
out = pd.DataFrame(rows)
out.to_csv('audit_01_stated_vs_observed_n.csv',index=False)
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',120)
print(out[~out.match].to_string())
print('\nblocks checked:',len(out),' mismatches:',(~out.match).sum())
