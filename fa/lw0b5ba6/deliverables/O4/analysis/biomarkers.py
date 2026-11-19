import pandas as pd, numpy as np
from scipy.stats import mannwhitneyu
from blocks import BLOCKS
c = pd.read_csv('tidy_continuous.csv'); c['level'] = c.level.fillna('').astype(str)
C = pd.read_csv('block_contrasts.csv'); C['level'] = C.level.fillna('').astype(str)
S = pd.read_csv('survival_counts.csv')

# Regimen protection status from the survival data (pooled):
PROTECTIVE = {'PSLN-344', 'PSLN-212(Y)', 'PSLN-344(Y)'}
NONPROTECTIVE = {'Sham', 'PSLN-212', 'Vaccine', 'PBS'}

CAND = [  # block, level, tier, compartment, human-accessible analogue, translatability, integrity
    ('S01-A_16h', '', 'A: innate PD (16 h)', 'lung tissue', 'nasal mucosal / blood IFN-I ISG score; IFN-b protein', 'high (surrogate)', 'ok (S09-A duplicates subset)'),
    ('S02-F', '16h', 'A: innate PD (16 h)', 'lung tissue', 'nasal GM-CSF (nasosorption)', 'moderate', 'ok'),
    ('S02-F', '36h', 'A: innate PD (36 h)', 'lung tissue', 'nasal GM-CSF (nasosorption)', 'moderate', 'ok'),
    ('S09-A_panel1', 'Ccl2', 'A: innate PD (16 h)', 'lung tissue', 'nasal/serum CCL2 (MCP-1)', 'high', 'caution: PBS/Sham label conflict'),
    ('S09-A_panel1', 'Il6', 'A: innate PD / reactogenicity (16 h)', 'lung tissue', 'serum/nasal IL-6', 'high', 'caution: PBS/Sham label conflict'),
    ('S01-D', '4', 'B: cellular (d4)', 'lung', 'none practical (BAL only)', 'low', 'ok'),
    ('S01-F', '', 'B: cellular (72 h)', 'lung', 'none practical', 'low', 'ok'),
    ('S02-A', '', 'B: cellular (72 h)', 'lung', 'none practical', 'low', 'ok'),
    ('S02-C', '', 'B: cellular (36 h)', 'MLN', 'none practical', 'low', 'caution: PTX arm undefined'),
    ('S02-D_CD86', '', 'B: cellular (d3)', 'MLN', 'blood DC activation (CD86) - weak', 'low', 'ok'),
    ('S04-A_ICOShi', '', 'B: Tfh (d7)', 'MLN', 'blood cTfh (ICOS+PD-1+CXCR5+) at d7', 'moderate-high', 'ok'),
    ('S04-B_Foxp3', '', 'B: Tfr (d7)', 'MLN', 'blood cTfr / cTfh:cTfr ratio at d7', 'moderate', 'ok'),
    ('S03-K', '', 'B: GC B (d7)', 'MLN', 'LN FNA (research only); blood plasmablasts d7 as proxy', 'low-moderate', 'ok'),
    ('S05-D', '', 'B: CD8 (d3)', 'lung', 'blood Ki-67+ / CD38+HLA-DR+ CD8 at d7-10', 'moderate', 'ok'),
    ('S05-E', '', 'B: CD8 (d3)', 'lung', 'blood GZMB+ CD8', 'moderate', 'ok'),
    ('S03-A', '', 'C: humoral (d14)', 'serum', 'serum IgG ELISA', 'high', 'ok'),
    ('S03-C', '', 'C: humoral (d14)', 'serum', 'HAI (regulatory-accepted surrogate)', 'high', 'ok'),
    ('S03-D', '', 'C: humoral (d14)', 'serum', 'microneutralisation', 'high', 'ok'),
    ('S03-G', '', 'C: humoral (d14)', 'serum', 'HAI (regulatory-accepted surrogate)', 'high', 'ok'),
    ('S05-F', '', 'C: cross-reactive CD8 (d14)', 'MLN', 'blood IFN-g ELISpot to conserved NP/M1 peptides', 'moderate-high', 'ok'),
    ('S14-A_H1N1', '', 'C: CD8 (timepoint not stated)', 'MLN', 'blood IFN-g ELISpot', 'moderate-high', 'caution: timepoint not stated'),
    ('S05-I', '', 'C: lung TRM (d25)', 'lung', 'nasal TRM (brush) - research', 'low', 'ok'),
    ('S05-G', '', 'D: durability (d60)', 'MLN', 'blood ELISpot at 6-12 months', 'moderate', 'ok'),
]
rows = []
for blk, lvl, tier, comp, human, transl, integ in CAND:
    d = c[(c.block == blk) & (c.level == lvl)]
    prot = d[d.group.isin(PROTECTIVE)].value.values
    nonp = d[d.group.isin(NONPROTECTIVE)].value.values
    if len(prot) == 0 or len(nonp) == 0:
        continue
    u = mannwhitneyu(prot, nonp, alternative='two-sided')
    auc = u.statistic / (len(prot) * len(nonp))
    # aged-only AUC: PSLN-344 vs (PSLN-212 + Sham/Vaccine/PBS)
    a344 = d[d.group == 'PSLN-344'].value.values; anp = d[d.group.isin({'PSLN-212', 'Sham', 'Vaccine', 'PBS'})].value.values
    auc_aged = mannwhitneyu(a344, anp, alternative='two-sided').statistic / (len(a344) * len(anp)) if len(a344) and len(anp) else np.nan
    mn = C[(C.block == blk) & (C.level == lvl) & C.contrast.str.startswith('Mn effect in aged')]
    ri = C[(C.block == blk) & (C.level == lvl) & C.contrast.str.startswith('Restoration')]
    rows.append(dict(block=blk, level=lvl, tier=tier, measurand=BLOCKS[blk]['measurand'], compartment=comp,
                     n_protective=len(prot), n_nonprotective=len(nonp), AUC_protective_vs_non=auc, AUC_aged_PSLN344_vs_aged_non=auc_aged,
                     p_MWU=u.pvalue,
                     Mn_effect=(mn.effect.iloc[0] if len(mn) else np.nan), Mn_effect_type=(mn.effect_type.iloc[0] if len(mn) else ''),
                     Mn_p=(mn.p_welch.iloc[0] if len(mn) else np.nan),
                     restoration_index=(ri.effect.iloc[0] if len(ri) else np.nan),
                     human_analogue=human, translatability=transl, integrity=integ))
B = pd.DataFrame(rows)
B.to_csv('biomarker_candidates.csv', index=False)
pd.set_option('display.width', 300); pd.set_option('display.max_colwidth', 40)
print(B[['block', 'level', 'tier', 'AUC_protective_vs_non', 'AUC_aged_PSLN344_vs_aged_non', 'p_MWU', 'Mn_effect', 'Mn_p', 'restoration_index', 'translatability']].to_string(index=False))

# HAI seroprotection-like threshold (>=1:40) counts
for blk in ['S03-C', 'S03-G']:
    d = c[c.block == blk]
    print(blk, {g: f"{int((x.value >= 40).sum())}/{len(x)}" for g, x in d.groupby('group', sort=False)})
