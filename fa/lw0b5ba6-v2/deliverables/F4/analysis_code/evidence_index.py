"""Builds the evidence index: every headline number in the proposal -> value, source cells, analysis table."""
import pandas as pd, numpy as np
G = pd.read_csv('surv_groups.csv'); D = pd.read_csv('desc_stats.csv'); D['time']=D['time'].astype(str)
PO = pd.read_csv('pooled_survival.csv'); SC = pd.read_csv('scorecard.csv'); SC['time']=SC['time'].astype(str)
def sg(block, group):
    r = G[(G.block==block)&(G.group==group)].iloc[0]; return f"{int(r.survivors)}/{int(r.n)}", r.cells
def ds(block, group, analyte=None, time=None, gm=False, nd=1):
    d = D[(D.block==block)&(D.group==group)]
    if analyte: d = d[d.analyte.str.contains(analyte, regex=False)]
    if time: d = d[d.time==time]
    assert len(d)==1, (block, group, analyte, time, len(d))
    r = d.iloc[0]; v = r.geomean if gm else r['mean']
    return (f"{v:.{nd}f}", r.cells)
E = []
def add(ref, claim, value, cells, analysis): E.append(dict(Ref=ref, Claim=claim, Value=value, Source_cells=cells, Analysis=analysis))
core7 = ['S03-I','S06-A','S06-B','S06-C','S06-E','S06-F','S06-G']
for sub, (g, lab) in zip('abcd', [('PSLN-344','PSLN-344'),('PSLN-212','PSLN-212'),('Sham','vaccine alone (Sham)'),('PSLN-212(Y)','young + PSLN-212')]):
    ks = [sg(b,g) for b in core7]
    tot = sum(int(k.split('/')[0]) for k,_ in ks); n = sum(int(k.split('/')[1]) for k,_ in ks)
    add('E1'+sub, f'Pooled survival, aged BALB/c, 7 experiments: {lab}', f"{tot}/{n} = {100*tot/n:.0f}%  ("+'; '.join(f"{b} {k}" for b,(k,_) in zip(core7,ks))+")", '; '.join(c for _,c in ks), 'Survival_by_block; Survival_pooled (stats_surv.py, pooled_surv.py)')
r = PO[PO.label.str.startswith('Aged BALB/c, single dose, excluding')].iloc[0]
add('E2','PSLN-344 minus PSLN-212 survival, Mantel–Haenszel, 7 experiments', f"+{r['PSLN-344 vs PSLN-212 MH_RD']:.0f} points (95% CI {r['PSLN-344 vs PSLN-212 MH_lo']:.0f} to {r['PSLN-344 vs PSLN-212 MH_hi']:.0f}); stratified log-rank chi2={r['PSLN-344 vs PSLN-212 strat_logrank_chi2']:.1f}, p={r['PSLN-344 vs PSLN-212 strat_logrank_p']:.1e}", 'as E1a and E1b', 'Survival_pooled')
r = PO[(PO.label=='Aged BALB/c, excl. S06-D')&(PO.source=='weights')].iloc[0]
add('E3','Same 7 experiments re-derived from body-weight records', f"PSLN-344 {r['PSLN-344']}, PSLN-212 {r['PSLN-212']}, Sham {r['Sham']}, young {r['PSLN-212(Y)']}; difference +{r['PSLN-344 vs PSLN-212 MH_RD']:.0f} ({r['PSLN-344 vs PSLN-212 MH_lo']:.0f} to {r['PSLN-344 vs PSLN-212 MH_hi']:.0f})", 'S13!A31:AJ40 (S13-F); S15!A1:AC30 (S15-A,B,C); S15!A41:AJ70 (S15-E,F,G)', 'Weight_status; Survival_vs_weights (wt_status.py)')
add('E4','Survival by challenge interval, PSLN-344 aged BALB/c', 'day 3: 5/7 (S06-B); day 14: 20/21 (S03-I, S06-A, S06-C); day 60: 14/21 (S06-E, S06-F, S06-G); day 14 vs day 60 Fisher p=0.045', '; '.join(sg(b,'PSLN-344')[1] for b in ['S06-B','S03-I','S06-A','S06-C','S06-E','S06-F','S06-G']), 'Survival_pooled')
add('E5','Unchallenged aged controls ("Untreated"), day-60 cohorts', '17/21 alive at 14 days (6/7, 7/7, 4/7); the 4 deaths followed only 3% to 6% weight loss', '; '.join(sg(b,'Untreated')[1] for b in ['S06-E','S06-F','S06-G'])+'; S15!AD43:AJ50, AD53:AJ60, AD63:AJ70', 'Survival_by_block; Weight_status')
add('E6','Antigen requirement (aged, rgH5N1 3 d after dosing)', f"vaccine + PSLN-344 {sg('S15-H','3d Vaccine+PSLN-344')[0]}; PSLN-344 alone {sg('S15-H','3d PSLN-344')[0]}; vaccine alone {sg('S15-H','3d Vaccine')[0]}", 'S15!A72:D93', 'Survival_by_block')
add('E7','Other strains, aged 20 months', f"C57BL/6 (S15-L): PSLN-344 {sg('S15-L','PSLN-344')[0]}, PSLN-212 {sg('S15-L','PSLN-212')[0]}, Sham {sg('S15-L','Sham')[0]}; Swiss Webster (S15-N): {sg('S15-N','PSLN-344')[0]}, {sg('S15-N','PSLN-212')[0]}, {sg('S15-N','Sham')[0]}", 'S15!A102:E130; S15!A133:E161', 'Survival_by_block')
add('E8','Wild-type H5N1, challenge 2 d after one dose', 'PSLN-344 9/9 with a recorded day (10 rows; 10/10 by weights); comparator arms 3/10 and 1/10', 'S03!G16:J46; S13!A42:AE50', 'Survival_by_block; Integrity_register DI-05')
add('E9','Prior-infection ("imprinting") study, 14 months old at vaccination', f"naive: PSLN-344 {sg('S06-E(r71)','Naïve+PSLN-344')[0]} and {sg('S06-F(r71)','Naïve+PSLN-344')[0]} vs PSLN-212 {sg('S06-E(r71)','Naïve+PSLN-212')[0]} and {sg('S06-F(r71)','Naïve+PSLN-212')[0]}; imprinted: PSLN-344 {sg('S06-E(r71)','Imprinting+PSLN-344')[0]} and {sg('S06-F(r71)','Imprinting+PSLN-344')[0]} vs PSLN-212 {sg('S06-E(r71)','Imprinting+PSLN-212')[0]} and {sg('S06-F(r71)','Imprinting+PSLN-212')[0]}", 'S06!G70:K98; S06!M70:Q98', 'Survival_by_block')
add('E10','Young animals, head to head', 'PSLN-344 24/24, PSLN-212 24/24, vaccine alone 0/23 (S09-B, S09-D, S09-F); maximum weight loss 10.7% vs 10.8%; day-14 weight after day-180 challenge 95.6% vs 99.2% (p=0.004)', 'S09!A11:D35; S09!A38:D62; S09!A65:D88; S09!F11:AD19, F38:AD46, F65:AD73', 'Survival_by_block; morbidity.py')
add('E11','Young animals, cGAMP comparator', f"CMP-204(Y) {sg('S13-E','CMP-204(Y)')[0]}, PSLN-344(Y) {sg('S13-E','PSLN-344(Y)')[0]}, vaccine alone {sg('S13-E','Sham')[0]}, naive {sg('S13-E','Naïve')[0]}", 'S13!R2:V30', 'Survival_by_block')
# immunology
for ref, blk, an, t, gm, nd, lab in [
 ('E12','S01-A','Ifnb1','16h',True,1,'Lung Ifnb1 at 16 h, fold (geometric mean)'), ('E13','S03-C','HAI','d14',True,0,'HAI GMT, H1N1, day 14'), ('E14','S03-G','HAI','d14',True,0,'HAI GMT, H3N2, day 14'),
 ('E15','S03-D','neutralizing','d14',True,0,'Neutralizing GMT, H1N1, day 14'), ('E16','S03-A','serum IgG','d14',True,0,'IgG GMT, H1N1, day 14'),
 ('E17','S05-F','MLN IFNg','d14',False,1,'IFN-γ+ CD8 T cells vs rgH5N1, day 14, %'), ('E18','S05-I','lung CD8 TRM','d25',False,1,'Lung resident-memory CD8 T cells, day 25, %'),
 ('E19','S03-K','MLN GC','d7',False,1,'Germinal-center B cells, day 7, %'), ('E20','S02-D CD40','CD40+','d3',False,1,'CD40+ lymph-node DC, day 3, %'), ('E21','S02-D CD86','CD86+','d3',False,1,'CD86+ lymph-node DC, day 3, %')]:
    vals=[]; cells=[]
    for g in ['Sham','PSLN-212','PSLN-344','PSLN-212(Y)']:
        try:
            v,c = ds(blk,g,an,t,gm,nd); vals.append(f"{g} {v}"); cells.append(c)
        except AssertionError: pass
    add(ref, lab+f' [{blk}]', '; '.join(vals), '; '.join(cells), 'Endpoint_descriptives; Scorecard (stats_quant.py)')
add('E22','IgG2a:IgG1 ratio recomputed from raw subclass titers (geometric mean)', 'H1N1: PSLN-212 0.54, PSLN-344 1.85, young 2.50; H3N2: 0.46, 2.30, 2.79', 'S13!A3:C7 ÷ S13!E3:G7; S13!I3:K7 ÷ S13!M3:O7', 'audit_derived.py; Integrity_register DI-01')
add('E23','Ifnb1 dose-response (Hill fit)', 'Emax PSLN-344 59×, PSLN-212 17×, CMP-204 8×; ED50 13, 11, 6 µg; 20 µg = 92% of 40-µg response for PSLN-344; PSLN-344 at 10 µg 21.0× vs PSLN-212 at 40 µg 14.7×', 'S08!A2:M7', 'Dose_response (dose_response.py)')
add('E24','Body weight after dosing, no challenge', 'PSLN-344 lowest mean 96.7% (day 4), 99.8% by day 10; vaccine alone 98.8% at day 4; PSLN-212/R848 90.65% at day 10 (4 of 5 recorded), lowest animal 84.7%', 'S08!A20:AE26', 'stats_misc.py')
add('E25','Lung cytokines, fold vs untreated (geometric mean, n=3)', 'Tnf 16 h: PSLN-344 40×, PSLN-212 16×, young 14×; Tnf 72 h: 8.4×, 5.2×, 0.5×; Il6 72 h: 7.2×, 1.9×, 3.1×; Ccl2 16 h: 590×, 7.6×, 1,390×', 'S09!B2:V9 (16 h); S09!Y2:AS9 (72 h, labeled 16h)', 'Endpoint_descriptives; Integrity_register DI-02')
add('E26','CNS transcripts at 36 h (mean fold, n=5)', 'Tnf: buffer 1.00, vaccine alone 1.32, PSLN-344 1.59, cholera toxin 3.50; Ifnb1: 1.00, 1.17, 1.32, 5.50; PSLN-344 vs buffer Tnf Tukey p=0.12, Welch p=0.03', 'S10!A2:N7', 'stats_misc.py')
add('E27','Encapsulation efficiency, % (mean, range, n=3)', 'PSLN-344 54.8 (49.3–59.4); PSLN-212 59.6 (54.9–64.0); CMP-204 65.2 (59.1–71.1)', 'S08!A10:O11', 'Endpoint_descriptives')
add('E28','Maximum weight loss among survivors of lethal challenge, 7 aged BALB/c experiments', 'PSLN-344 aged 11.9% (n=41) vs young + PSLN-212 9.7% (n=49); difference 2.2 points, Welch p=0.007', 'S13!A31:AJ40; S15!A1:AC30; S15!A41:AJ70', 'morbidity.py; Weight_status')
add('E29','IgG after a day-14 boost (GMT, day 28)', 'H1N1: PSLN-212 4,411; PSLN-344 15,651; young 40,739. H3N2: 1,086; 12,435; 43,472', 'S13!F52:J57; S13!L52:P57', 'Endpoint_descriptives')
add('E30','CDN-1807 vs cGAMP in the same vehicle, aged (PSLN-212 vs CMP-204)', 'Ifnb1 16 h 2.15× (Tukey p=0.001); HAI H1N1 2.0× (p=0.16); neutralizing H1N1 2.3× (p=0.29); survival 0/7 vs 3/7 as printed (S03-I; see DI-04)', 'S01!B4:F5; S03!L3:M7; S03!R3:S7; S03!C24:D37', 'Endpoint_pairwise; Survival_by_block')
EV = pd.DataFrame(E); EV.to_csv('evidence_index.csv', index=False)
pd.set_option('display.width', 300); pd.set_option('display.max_colwidth', 160); print(EV[['Ref','Claim','Value']].to_string())
