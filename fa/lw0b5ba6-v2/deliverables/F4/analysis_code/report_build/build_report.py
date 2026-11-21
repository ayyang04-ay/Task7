import pandas as pd, numpy as np, re
A = '/tmp/work/analysis/'
G = pd.read_csv(A+'surv_groups.csv'); SC = pd.read_csv(A+'scorecard.csv'); SC['time']=SC['time'].astype(str)
PO = pd.read_csv(A+'pooled_survival.csv'); WG = pd.read_csv(A+'wt_group_status.csv')
REG = pd.read_csv(A+'integrity_register.csv'); EV = pd.read_csv(A+'evidence_index.csv')

def md_table(header, rows, widths=None, align=None):
    n = len(header); widths = widths or [10]*n; align = align or ['l']*n
    def sep(w, a):
        d = '-'*max(3, w)
        return (':'+d[1:] if a=='l' else d[:-1]+':' if a=='r' else ':'+d[1:-1]+':')
    out = ['| ' + ' | '.join(header) + ' |', '|' + '|'.join(sep(w,a) for w,a in zip(widths, align)) + '|']
    for r in rows:
        out.append('| ' + ' | '.join(str(x).replace('|','/').replace('\n',' ') for x in r) + ' |')
    return '\n'.join(out)

def sg(block, group):
    r = G[(G.block==block)&(G.group==group)]
    if len(r)==0: return '–'
    r = r.iloc[0]; return f"{int(r.survivors)}/{int(r.n)}"

# ---------- Table 0 ----------
r = PO[PO.label.str.startswith('Aged BALB/c, single dose, excluding')].iloc[0]
def pc(g): 
    k,n = r[g].split('/'); return f"{r[g]} ({100*int(k)/int(n):.0f}%)"
T0 = md_table(['', 'Vaccine alone', 'Vaccine + PSLN-212', 'Vaccine + PSLN-344', 'Young benchmark (vaccine + PSLN-212)'],
  [['**Aged mice surviving lethal influenza challenge after one intranasal dose; seven experiments pooled**', pc('Sham'), pc('PSLN-212'), f"**{pc('PSLN-344')}**", pc('PSLN-212(Y)')]],
  widths=[40,12,14,14,20], align=['l','c','c','c','c'])

# ---------- Table 1 ----------
rect = {'S03-I':'S03!A16:F51','S06-A':'S06!A2:E30','S06-B':'S06!G2:K30','S06-C':'S06!M2:Q30','S06-D':'S06!A33:E61','S06-E':'S06!G33:L68','S06-F':'S06!M33:R68','S06-G':'S06!A70:F105'}
desc = {'S03-I':'Bivalent vaccine → matched H1N1 (CA09), day 14','S06-A':'H3N2 vaccine → H1N1 (PR8), day 14','S06-C':'Bivalent vaccine → H5N1 (rgH5N1), day 14','S06-B':'H3N2 vaccine → H1N1 (PR8), day 3',
        'S06-D':'Bivalent vaccine → H5N1 (rgH5N1), day 3','S06-E':'H3N2 vaccine → H1N1 (PR8), day 60','S06-F':'Bivalent vaccine → H5N1 (rgH5N1), day 60','S06-G':'H1N1 vaccine → H3N2 (Perth), day 60'}
note = {'S03-I':'Weight record: PSLN-212 3/7 (DI-04)','S06-A':'Table and weight record agree','S06-C':'Weight record: PSLN-212 1/7','S06-B':'Table and weight record agree',
        'S06-D':'Table is a copy of S06-C; weight record: PSLN-344 5/7, young 5/7 (DI-03). Not pooled','S06-E':'Weight record: PSLN-344 6/7, PSLN-212 1/7','S06-F':'Table and weight record agree','S06-G':'Weight record: PSLN-344 5/7'}
rows=[]
for b in ['S03-I','S06-A','S06-C','S06-B','S06-D','S06-E','S06-F','S06-G']:
    rows.append([b, desc[b], sg(b,'Sham'), sg(b,'PSLN-212'), f"**{sg(b,'PSLN-344')}**", sg(b,'PSLN-212(Y)'), rect[b], note[b]])
rw = PO[(PO.label=='Aged BALB/c, excl. S06-D')&(PO.source=='weights')].iloc[0]
rows.append(['**Pooled**', '**Seven experiments (S06-D excluded), survival tables**', f"**{r['Sham']}**", f"**{r['PSLN-212']}**", f"**{r['PSLN-344']}**", f"**{r['PSLN-212(Y)']}**", 'as above', f"PSLN-344 minus PSLN-212: +{r['PSLN-344 vs PSLN-212 MH_RD']:.0f} points (CI {r['PSLN-344 vs PSLN-212 MH_lo']:.0f} to {r['PSLN-344 vs PSLN-212 MH_hi']:.0f}); stratified log-rank p<0.0001"])
rows.append(['', 'Same seven, from body-weight records', rw['Sham'], rw['PSLN-212'], rw['PSLN-344'], rw['PSLN-212(Y)'], 'S13-F; S15-A, B, C, E, F, G', f"+{rw['PSLN-344 vs PSLN-212 MH_RD']:.0f} points (CI {rw['PSLN-344 vs PSLN-212 MH_lo']:.0f} to {rw['PSLN-344 vs PSLN-212 MH_hi']:.0f})"])
T1a = md_table(['Block','Vaccine → challenge virus, day of challenge','Vaccine alone','PSLN-212','PSLN-344','Young + PSLN-212','Source cells','Note'], rows, widths=[7,21,8,9,9,9,13,24], align=['l','l','c','c','c','c','l','l'])
rows=[]
rows.append(['S15-L', 'C57BL/6, 20 months; bivalent vaccine; challenge virus not stated', f"Vaccine alone {sg('S15-L','Sham')}; PSLN-212 {sg('S15-L','PSLN-212')}; **PSLN-344 {sg('S15-L','PSLN-344')}**; young + PSLN-212 {sg('S15-L','PSLN-212(Y)')}", 'S15!A102:E130'])
rows.append(['S15-N', 'Swiss Webster, 20 months; bivalent vaccine; challenge virus not stated', f"Vaccine alone {sg('S15-N','Sham')}; PSLN-212 {sg('S15-N','PSLN-212')}; **PSLN-344 {sg('S15-N','PSLN-344')}**; young + PSLN-212 {sg('S15-N','PSLN-212(Y)')}", 'S15!A133:E161'])
rows.append(['S15-H', 'Aged BALB/c; H5N1 (rgH5N1) challenge 3 days after dosing', f"Vaccine alone {sg('S15-H','3d Vaccine')}; PSLN-344 alone {sg('S15-H','3d PSLN-344')}; **vaccine + PSLN-344 {sg('S15-H','3d Vaccine+PSLN-344')}**", 'S15!A72:D93'])
rows.append(['S03-J', 'rgH5N1 vaccine; wild-type H5N1 challenge 2 days after dosing; followed to day 21; age not stated', f"**PSLN-344 9/9** (a tenth row has no day recorded); arms labeled PSLN-212 {sg('S03-J','PSLN-212')} and Sham {sg('S03-J','Sham')}", 'S03!G16:J46'])
rows.append(['S06 rows 71–98 (left)', 'BALB/c, 14 months at vaccination, with or without H1N1 infection 4 months earlier; H1N1 (PR8) challenge', f"No prior infection: PSLN-212 {sg('S06-E(r71)','Naïve+PSLN-212')}, **PSLN-344 {sg('S06-E(r71)','Naïve+PSLN-344')}**. Prior infection: PSLN-212 {sg('S06-E(r71)','Imprinting+PSLN-212')}, **PSLN-344 {sg('S06-E(r71)','Imprinting+PSLN-344')}**", 'S06!G70:K98'])
rows.append(['S06 rows 71–98 (right)', 'Same design; H3N2 (Perth) challenge at day 14', f"No prior infection: PSLN-212 {sg('S06-F(r71)','Naïve+PSLN-212')}, **PSLN-344 {sg('S06-F(r71)','Naïve+PSLN-344')}**. Prior infection: PSLN-212 {sg('S06-F(r71)','Imprinting+PSLN-212')}, **PSLN-344 {sg('S06-F(r71)','Imprinting+PSLN-344')}**", 'S06!M70:Q98'])
rows.append(['S09-B, S09-D, S09-F', 'Young BALB/c; mismatched-virus challenge at day 21, 21 and 180', f"Vaccine alone {sg('S09-B','Sham')}, {sg('S09-D','Sham')}, {sg('S09-F','Sham')}; PSLN-212 {sg('S09-B','PSLN-212Y')}, {sg('S09-D','PSLN-212Y')}, {sg('S09-F','PSLN-212Y')}; PSLN-344 {sg('S09-B','PSLN-344Y')}, {sg('S09-D','PSLN-344Y')}, {sg('S09-F','PSLN-344Y')}", 'S09!A11:D35; A38:D62; A65:D88'])
rows.append(['S13-E', 'Young BALB/c; matched H1N1 challenge at day 14', f"No vaccine {sg('S13-E','Naïve')}; vaccine alone {sg('S13-E','Sham')}; cGAMP liposome (CMP-204) {sg('S13-E','CMP-204(Y)')}; PSLN-344 {sg('S13-E','PSLN-344(Y)')}", 'S13!R2:V30'])
rows.append(['S03-I', 'Aged BALB/c; matched H1N1 challenge at day 14; cGAMP arm', f"cGAMP liposome (CMP-204) {sg('S03-I','CMP-204')} (see DI-04)", 'S03!C24:C30'])
T1b = md_table(['Block','Design','Survivors / n','Source cells'], rows, widths=[12,34,42,12])
T1 = "**Table 1a. Aged BALB/c, one dose: survivors / n at 14 days after challenge.**\n\n" + T1a + "\n\n**Table 1b. Other lethal-challenge experiments.**\n\n" + T1b

# ---------- Table 2 ----------
def f(x):
    if pd.isna(x): return '–'
    ax = abs(x)
    return f"{x:,.0f}" if ax>=100 else f"{x:.1f}" if ax>=10 else f"{x:.1f}" if ax>=1 else f"{x:.2f}"
def pf(p):
    if pd.isna(p): return '–'
    return '<0.001' if p<0.001 else f"{p:.3f}" if p<0.1 else f"{p:.2f}"
spec = [
 ('Lung Ifnb1 mRNA at 16 h, fold', 'S01-A', 'Ifnb1', '16h', 'S01!B3:F9'),
 ('Lung monocytes at day 4, %', 'S01-D', 'lung monocytes', '4', 'S01!B26:U26'),
 ('CCR7+ migratory dendritic cells in lung, 72 h, %', 'S02-A', 'lung CCR7', '72h', 'S02!A3:D7'),
 ('CD86+ dendritic cells in lymph node, day 3, %', 'S02-D CD86', 'CD86', 'd3', 'S02!F10:I14'),
 ('Germinal-center B cells, day 7, %', 'S03-K', 'MLN GC', 'd7', 'S03!L17:O21'),
 ('Follicular helper : follicular regulatory T-cell ratio, day 7', 'S04-B Tfh:Tfr', 'Tfh:Tfr', 'd7', 'S04!A15:D19'),
 ('Serum IgG to H1N1, day 14, titer', 'S03-A', 'serum IgG', 'd14', 'S03!A3:E7'),
 ('Hemagglutination inhibition, H1N1, day 14, titer', 'S03-C', 'HAI', 'd14', 'S03!K3:O7'),
 ('Hemagglutination inhibition, H3N2, day 14, titer', 'S03-G', 'HAI', 'd14', 'S03!K10:O14'),
 ('Neutralizing antibody, H1N1, day 14, titer', 'S03-D', 'neutralizing', 'd14', 'S03!Q3:U7'),
 ('Ki-67+ CD8 T cells in lung, day 3, %', 'S05-D', 'lung Ki67', 'd3', 'S05!A19:D23'),
 ('Interferon-γ+ CD8 T cells responding to H5N1, day 14, %', 'S05-F', 'MLN IFNg', 'd14', 'S05!A33:D37'),
 ('Interferon-γ+ CD8 T cells responding to H5N1, day 60, %', 'S05-G', 'MLN IFNg', 'd60', 'S05!A40:D44'),
 ('Lung-resident memory CD8 T cells, day 25, %', 'S05-I', 'lung CD8 TRM', 'd25', 'S05!A54:D58'),
]
rows=[]
for lab, blk, key, t, cells in spec:
    x = SC[(SC.block==blk)&(SC.analyte.str.contains(key, regex=False))&(SC.time==t)]
    assert len(x)==1, (blk,key,t,len(x)); x = x.iloc[0]
    fold = x['344v212_eff'] if x.stat=='GM' else x['PSLN-344']/x['PSLN-212']
    pct = 100*x['PSLN-344']/x['PSLN-212(Y)']
    rows.append([f"{lab} ({blk})", f(x['Sham']), f(x['PSLN-212']), f"**{f(x['PSLN-344'])}**", f(x['PSLN-212(Y)']), f"{fold:.1f}×", pf(x['344v212_pTukey']), f"{pct:.0f}%", cells])
# recomputed IgG2a:IgG1 row (values from audit_derived / Tukey on log ratio, see analysis)
rows.insert(10, ['IgG2a : IgG1 ratio, H1N1, day 14, recomputed from raw titers (S13-A ÷ S13-B)', '–', '0.54', '**1.85**', '2.50', '3.4×', '0.016', '74%', 'S13!A3:G7'])
T2 = "**Table 2. Key immune read-outs in aged animals (group mean; geometric mean for titers, mRNA and ratios). n=5 per group.**\n\n" + md_table(
  ['Read-out (block)','Vaccine alone','PSLN-212','PSLN-344','Young + PSLN-212','Ratio, 344 to 212','p (Tukey)','344 as % of young','Source cells'], rows, widths=[28,8,9,9,9,8,8,8,13], align=['l','c','c','c','c','c','c','c','l'])

# ---------- Table 3 (static) ----------
rows = [
 ['DI-01','IgG2a:IgG1 ratio blocks S03-B and S03-F','Column labels are rotated relative to the raw titers in S13-A to S13-D','As printed, PSLN-344 looks IgG1-skewed (0.54). Recomputed, it is IgG2a-skewed (1.85; 2.30 for H3N2) and PSLN-212 is the skewed one','Recomputed from raw titers'],
 ['DI-02','Second cytokine panel in S09-A','Labeled 16 h; its values are the 72-hour animals of S01-A (21 of 21 match)','Read as a replicate, it would hide that Tnf and Il6 are still raised in aged lung at 72 hours','Analyzed as 72 hours'],
 ['DI-03','Survival table S06-D','Identical row for row to S06-C, a different experiment','Day-3 H5N1 survival for PSLN-344 is 7/7 (table), 5/7 (weights) or 6/7 (independent run S15-H)','Excluded from pooled estimate'],
 ['DI-04','S03-I against its weight record S13-F','Table has all PSLN-212 animals dead by day 6; weights show all seven alive at day 8 and three recovering','PSLN-212 survival after matched-virus challenge is 0/7 or 3/7; the cGAMP against PSLN-212 ranking is unreliable','Reported as a range'],
 ['DI-05','Wild-type H5N1 study S03-J','Stated n of 9 with 10 rows; one row has no day; group names differ between table and weight record; age not stated','PSLN-344 result is firm; which comparator is which is not','Comparator identity flagged'],
 ['DI-07','Body-weight blocks on S15 and S09','Values shared between different experiments (S15-I and S15-C: 40 of 42 cells)','Weight curves are not independent confirmation; strain generalization is provisional','Used as cross-check only'],
 ['DI-08','Lung neutrophils S11-B','35 of 100 values identical to the alveolar-macrophage block S11-A','No usable neutrophil read-out','Excluded'],
 ['DI-16','"Untreated" groups at day 60','Not challenged; 4 of 21 died in 14 days','They measure background mortality in old animals and are not an efficacy comparator','Used as background only'],
]
T3 = "**Table 3. Integrity findings that change how a block should be read.**\n\n" + md_table(['ID','Where','What is wrong','Consequence','Handling'], rows, widths=[6,18,30,34,14])

# ---------- Table 4 (static biomarker panel; numbers from Endpoint_descriptives) ----------
rows = [
 ['Hours: target engagement', 'Lung Ifnb1 mRNA at 16 h (S01-A)', '37-fold vs 17-fold; no overlap between groups (5 vs 5); dose-dependent (S08-A)', 'Interferon-β and CXCL10 in nasal lining fluid; interferon-stimulated gene score in blood at 24 h', 'Proof of pharmacology; dose selection'],
 ['Hours: recruitment signals', 'Lung Ccl2 mRNA at 16 h (S09-A, n=3); Gm-csf mRNA at 16–36 h (S02-F)', 'Ccl2 590-fold vs 7.6-fold; Gm-csf 6.0- to 8.5-fold vs 1.4- to 1.6-fold', 'CCL2 and GM-CSF protein in nasal lining fluid', 'Widest dynamic range; most sensitive to the Mn2+ effect'],
 ['Days 3–7: cellular', 'Lung monocytes day 4 (S01-D); CCR7+ dendritic cells (S02-A); ICOS-high follicular helper T cells and germinal-center B cells day 7 (S04-A, S03-K)', '30.6% vs 16.7%; 30.7% vs 7.3%; 10.3% vs 3.8%; 6.5% vs 2.3%', 'Activated circulating follicular helper T cells and plasmablasts in blood at day 7', 'Early predictor of antibody response'],
 ['Days 14–28: antibody', 'Hemagglutination inhibition and neutralizing titers (S03-C, D, G, H); IgG2a:IgG1 ratio (S13-A to D)', 'Titers 368 vs 46 (H1N1) and 320 vs 35 (H3N2); neutralizing 3,840 vs 418; ratio 1.85 vs 0.54', 'Hemagglutination inhibition and microneutralization (the regulatory standard); nasal IgA, which we have never measured', 'Immunogenicity endpoint for matched strains'],
 ['Days 14–60: T cells', 'Interferon-γ+ CD8 T cells responding to H5N1 (S05-F, S05-G); lung-resident memory CD8 T cells (S05-I)', '6.4% vs 1.5% at day 14; 9.9% vs 3.0% at day 60; 4.0% vs 1.0%', 'Interferon-γ T-cell response in blood to conserved antigens (nucleoprotein, matrix) and to mismatched virus', 'Candidate correlate for mismatched-virus protection; unproven'],
 ['Safety', 'Lung Tnf and Il6 at 72 h (S09-A); body weight after dosing (S08-D); brain Tnf (S10-A)', 'Tnf 8.4-fold and Il6 7.2-fold at 72 h (young: 0.5 and 3.1); weight 96.7% at day 4; brain Tnf 1.6-fold', 'TNF and IL-6 in nasal fluid and serum; blood manganese; brain manganese by MRI; smell testing', 'Reactogenicity and manganese monitoring'],
]
T4 = "**Table 4. Biomarker panel. Values are aged animals given PSLN-344 vs PSLN-212.**\n\n" + md_table(['When and what for','Marker in our data (block)','PSLN-344 vs PSLN-212','Proposed measure in people','Use'], rows, widths=[13,25,24,22,16])

# ---------- Appendix A ----------
rows=[]
for _, x in REG.iterrows():
    rows.append([f"**{x['ID']}**", x['Severity'], x['Location (sheet!cells)'], f"{x['Issue']} *Evidence:* {x['Evidence']}", x['Effect on conclusions'], f"{x['How handled in this analysis']} *Lab action:* {x['Action for the lab']}"])
TA = md_table(['ID','Severity','Location','Issue and evidence','Effect on conclusions','Handling here; action for the lab'], rows, widths=[6,8,13,36,19,18])

# ---------- Appendix C ----------
rows=[]
for _, x in EV.iterrows():
    rows.append([x.Ref, x.Claim, x.Value, x.Source_cells, x.Analysis])
TC = md_table(['Ref','What','Value','Source cells','Analysis table or script'], rows, widths=[5,21,35,21,18])


# ---------- column widths for hand-written tables in the template ----------
def seprow(ws): return '|' + '|'.join(':' + '-'*(w-1) for w in ws) + '|'
fixes = [
 ('| | |\n|---|---|', '| Item | Specification |\n' + seprow([17, 83])),
 ('| Filter | Basis | Status |\n|---|---|---|', '| Filter | Basis | Status |\n' + seprow([32, 40, 28])),
 ('| Question | Criterion | Source |\n|---|---|---|', '| Question | Criterion | Source |\n' + seprow([28, 58, 14])),
 ('| Step | Population | Comparators | Endpoints and read-outs | Earliest timing |\n|---|---|---|---|---|', '| Step | Population | Comparators | Endpoints and read-outs | Earliest timing |\n' + seprow([19, 15, 17, 35, 14])),
 ('| Option | Decision | Reason and evidence |\n|---|---|---|', '| Option | Decision | Reason and evidence |\n' + seprow([27, 15, 58])),
 ('| Interpretation | Decision | Reason and evidence |\n|---|---|---|', '| Interpretation | Decision | Reason and evidence |\n' + seprow([30, 15, 55])),
 ('| Item | Reason |\n|---|---|', '| Item | Reason |\n' + seprow([45, 55])),
]

s = open('proposal_template.md').read()
for a, b in fixes:
    assert a in s, a
    s = s.replace(a, b)
for k, v in [('{{TABLE0}}',T0),('{{TABLE1}}',T1),('{{TABLE2}}',T2),('{{TABLE3}}',T3),('{{TABLE4}}',T4),('{{TABLEA}}',TA),('{{TABLEC}}',TC)]:
    assert k in s, k; s = s.replace(k, v)
open('proposal.md','w').write(s)
print('proposal.md written; words:', len(re.findall(r'\w+', s)))
print(T0); print(); print(T1a); print(); print(T2)
