import pandas as pd, numpy as np
from scipy import stats
c = pd.read_csv('tidy_continuous.csv'); c['level'] = c.level.fillna('').astype(str)
PAIRS = [
 ('S01-B', 'AECII/PSLN-SRB', 'AECII/FreeSRB', 'AECII uptake: liposome vs free dye'),
 ('S01-B', 'AECI/PSLN-SRB', 'AECI/FreeSRB', 'AECI uptake: liposome vs free dye'),
 ('S01-B', 'AECII/PSLN-SRB', 'AECI/PSLN-SRB', 'Liposome uptake AECII vs AECI'),
 ('S01-C', 'WT', 'SPA/D', 'AM uptake WT vs Sftpa1/Sftpd KO'),
 ('S08-C', 'AECII-PSLN-344-SRB', 'AECII-PSLN-SRB', 'AECII uptake with vs without Mn'),
 ('S08-C', 'AECI-PSLN-344-SRB', 'AECI-PSLN-SRB', 'AECI uptake with vs without Mn'),
 ('S11-C', 'CBX+', 'CBX-', 'Gap-junction blockade (CBX) on monocyte recruitment'),
 ('S12-A', 'IFNAR-/- to WT', 'WT to WT', 'IFNAR-deficient BM monocyte infiltration'),
 ('S02-H', 'IFN w/o cDC', 'WT w/o cDC', 'moDC from IFNAR-/- vs WT BM (no cDC precursors)'),
 ('S02-H', 'GMCSF', 'IFN w/o cDC', 'GM-CSF rescue of IFNAR-/- moDC'),
 ('S02-H', 'WT w/ cDC', 'WT w/o cDC', 'WT BM with vs without cDC precursors'),
 ('S02-G', 'PSLN-212+GM-CSF', 'PSLN-212', 'GM-CSF added to PSLN-212 (moDC-like cells)'),
 ('S02-G', 'PSLN-212+GM-CSF', 'GM-CSF', 'PSLN-212+GM-CSF vs GM-CSF alone'),
 ('S07-B_mono', 'PSLN-344+INCB3344', 'PSLN-344', 'CCR2 antagonist on monocytes'),
 ('S07-B_Ly6CMac', 'PSLN-344+INCB3344', 'PSLN-344', 'CCR2 antagonist on Ly6C+ macrophages'),
 ('S02-I', 'PSLN-344(Y)+INCB3344', 'PSLN-344(Y)', 'CCR2 antagonist on lung GZMB+ CD8 (young)'),
 ('S05-C', 'MLN+PTX', 'MLN', 'Pertussis toxin on MLN OT-I proliferation'),
 ('S05-C', 'Lung+PTX', 'Lung', 'Pertussis toxin on lung OT-I proliferation'),
 ('S02-C', 'PTX', 'PSLN-344', 'PTX group vs PSLN-344 (antigen+ MLN DC)'),
 ('S02-E', 'PTX', 'PSLN-344', 'PTX group vs PSLN-344 (OT-I priming)'),
 ('S02-C', 'PSLN-344(Y)', 'PSLN-212(Y)', 'Mn effect in young: antigen+ MLN DC'),
 ('S02-E', 'PSLN-344(Y)', 'PSLN-212(Y)', 'Mn effect in young: OT-I priming'),
 ('S01-A_16h', 'PSLN-344(Y)', 'PSLN-212(Y)', 'Mn effect in young: Ifnb1 16 h'),
 ('S01-F', 'PSLN-344(Y)', 'PSLN-212(Y)', 'Mn effect in young: cDC1'),
 ('S01-A_16h', 'PSLN-212/R848', 'PSLN-212', 'R848 added to PSLN-212: Ifnb1 16 h'),
 ('S01-A_16h', 'CMP-204', 'PSLN-212', 'cGAMP (CMP-204) vs CDN-1807 (PSLN-212): Ifnb1 16 h'),
]
LOGB = {'S01-A_16h'}
rows = []
for blk, g1, g2, lab in PAIRS:
    a = c[(c.block == blk) & (c.group == g1)].value.values; b = c[(c.block == blk) & (c.group == g2)].value.values
    if blk in LOGB:
        p = stats.ttest_ind(np.log2(a), np.log2(b), equal_var=False).pvalue; eff = 2 ** (np.log2(a).mean() - np.log2(b).mean()); et = 'geo fold'
    else:
        p = stats.ttest_ind(a, b, equal_var=False).pvalue; eff = a.mean() / b.mean(); et = 'ratio of means'
    rows.append(dict(block=blk, comparison=lab, g1=g1, n1=len(a), mean1=a.mean(), sd1=a.std(ddof=1), g2=g2, n2=len(b), mean2=b.mean(), sd2=b.std(ddof=1),
                     effect=eff, effect_type=et, diff=a.mean() - b.mean(), p_welch=p))
T = pd.DataFrame(rows)
pd.set_option('display.width', 260); pd.set_option('display.max_colwidth', 55)
print(T.round(4).to_string(index=False))
T.to_csv('mechanism_contrasts.csv', index=False)
