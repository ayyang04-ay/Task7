"""15_workbook.py -- PSLN_analysis_workbook.xlsx: evidence register + every analysis table + tidy source data."""
import pandas as pd, numpy as np, importlib.util, sys
sys.path.insert(0, '/tmp/work/code')
spec = importlib.util.spec_from_file_location('content', '/tmp/work/code/14_content.py'); content = importlib.util.module_from_spec(spec); spec.loader.exec_module(content)
T = '/tmp/work/tables/'
SUM = content.SUM; CON = content.CON; SBG = content.SBG; STS = content.STS; SPL = content.SPL; MEC = content.MEC
GAP = content.GAP; DR = content.DR; CNS = content.CNS; RG = content.RG
S = pd.read_csv('/tmp/work/tidy/survival.csv'); C = pd.read_csv('/tmp/work/tidy/continuous.csv'); BW = pd.read_csv('/tmp/work/tidy/bodyweight.csv')
fp, fnum, con, center = content.fp, content.fnum, content.con, content.center

def cells_of(block, group=None, time=None):
    d = SUM[SUM.block == block]
    if group: d = d[d.group == group]
    if time is not None: d = d[d.time == str(time)]
    return '; '.join(d.cells.astype(str).unique()[:6])
def surv_cells(blocks, groups):
    d = S[S.block.isin(blocks) & S.group.isin(groups)]
    return '; '.join(f"{b}:{dd.cell.iloc[0]}..{dd.cell.iloc[-1]}" for (b, g), dd in d.groupby(['block', 'group']))
R = []
def reg(area, claim, value, blocks, cells, analysis, where):
    R.append(dict(area=area, claim=claim, value=value, source_blocks=blocks, source_cells=cells, analysis=analysis, used_in=where))
prim = ['S03-I', 'S03-J', 'S06-A', 'S06-B', 'S06-C', 'S06-E(d60)', 'S06-F(d60)', 'S06-G(d60)']
PR = content.PR
reg('Efficacy', 'Pooled survival, aged BALB/c, 8 experiments', 'PSLN-344 49/59 (83%); PSLN-212 7/59 (12%); Sham 1/59 (2%); young PSLN-212 49/49',
    ', '.join(prim), surv_cells(prim, ['PSLN-344', 'PSLN-212']), 'A5 survival_pooled', 'Sec 1, 2.1, Table 1, Fig 1')
reg('Efficacy', 'Stratified Cox HR, PSLN-344 vs PSLN-212', f"{PR.cox_HR:.3f} (95% CI {PR.HR_lo:.3f}-{PR.HR_hi:.3f}); p={PR.cox_p:.1e}", ', '.join(prim), 'see above', 'A5', 'Sec 1, 2.1, 8')
reg('Efficacy', 'Mantel-Haenszel risk difference in death', f"{100*PR.MH_RD_death:.1f} pp ({100*PR.RD_lo:.1f} to {100*PR.RD_hi:.1f})", ', '.join(prim), 'see above', 'A5', 'Table 1 note')
for pre, lab in [('Sens-1', 'drop S03-I'), ('Sens-2', 'drop S03-J'), ('Sens-4', 'add S15-L/N')]:
    r = SPL[SPL.analysis.str.startswith(pre)].iloc[0]
    reg('Efficacy (sensitivity)', f'Cox HR, {lab}', f"{r.cox_HR:.3f} ({r.HR_lo:.3f}-{r.HR_hi:.3f}); {r.surv_344} vs {r.surv_212}", r.blocks, '', 'A5', 'Sec 1, 3')
for pre in ['Challenge 14', 'Challenge 2-3', 'Heterosubtypic', 'Challenge 60', 'Middle-aged (14 mo) naive', 'Middle-aged (14 mo) imprinted']:
    r = SPL[SPL.analysis.str.startswith(pre)].iloc[0]
    reg('Efficacy (subgroup)', r.analysis, f"{r.surv_344} vs {r.surv_212}; HR {r.cox_HR:.3f}", r.blocks, '', 'A5', 'Sec 2.1, 8')
t = STS
reg('Efficacy', 'Day-60: PSLN-344 vs young; vs untreated background', '14/21 vs 21/21 (Fisher p=0.009); vs untreated 17/21 (p=0.48); untreated deaths 4/21',
    'S06-E(d60), S06-F(d60), S06-G(d60)', surv_cells(['S06-E(d60)', 'S06-F(d60)', 'S06-G(d60)'], ['PSLN-344', 'Untreated', 'PSLN-212(Y)']), 'A4 (Fisher on pooled counts)', 'Sec 2.1, 10')
reg('Efficacy', 'PSLN-212 vs Sham, pooled aged', '7/59 vs 1/59, Fisher p=0.061', ', '.join(prim), surv_cells(prim, ['PSLN-212', 'Sham']), 'A4', 'Sec 1, 8, 9')
reg('Efficacy', 'Young mice: all adjuvants protect', 'PSLN-212(Y) 8/8, 8/8, 8/8; PSLN-344(Y) 8/8, 8/8, 8/8, 7/7; CMP-204(Y) 7/7; Sham 0/8, 0/8, 0/7, 1/7',
    'S09-B, S09-D, S09-F, S13-E', surv_cells(['S09-B', 'S09-D', 'S09-F', 'S13-E'], ['PSLN-212(Y)', 'PSLN-344(Y)', 'CMP-204(Y)']), 'A4', 'Sec 1, 7, 9')
reg('Efficacy', 'Survivor weight nadir, PSLN-344 vs young', '87.3% (n=33) vs 89.8% (n=42); t-test p=0.0035', 'S15-A, S15-B, S15-C, S15-E, S15-F, S15-G', 'S15!A3..AC70', 'A9', 'Sec 2.1')
def regc(area, claim, block, contrast, time=None, meas=None, where='', extra=''):
    c = con(block, contrast, time, meas)
    a, b = contrast.split(' vs ')
    val = (f"{fnum(c.mean_a)} vs {fnum(c.mean_b)}; " + (f"GMR {c.est:.2f} ({c.lo:.2f}-{c.hi:.2f})" if c.effect == 'GMR' else f"diff {c.est:+.2f} ({c.lo:+.2f} to {c.hi:+.2f})")
           + f"; Tukey p={fp(c.tukey_p)}; Welch p={fp(c.welch_p)}; MW p={fp(c.mw_p)}" + extra)
    reg(area, f"{claim} [{contrast}]", val, block, f"{c.cells_a} / {c.cells_b}", 'A2 continuous_contrasts', where)
regc('Innate', 'Lung Ifnb1 16 h (fold)', 'S01-A', 'PSLN-344 vs PSLN-212', '16h', where='Sec 1, 2.2, 4, 5', extra=f"; young {fnum(center('S01-A','PSLN-212(Y)','16h'))}")
regc('Innate', 'Lung Ifnb1 16 h: CDN-1807 vs cGAMP in same vehicle', 'S01-A', 'PSLN-212 vs CMP-204', '16h', where='Sec 4, 9, 10')
regc('Innate', 'Lung Gm-csf 36 h (fold)', 'S02-F', 'PSLN-344 vs PSLN-212', '36h', where='Sec 2.2, 4, 5')
regc('Myeloid', 'Lung Ly6C+ monocytes d4 (%)', 'S01-D', 'PSLN-344 vs PSLN-212', '4', where='Sec 2.2, 4')
regc('DC', 'CCR7+ migratory DC (%)', 'S02-A', 'PSLN-344 vs PSLN-212', '72h', where='Sec 2.2, 4')
regc('DC', 'Antigen+ DC in MLN (%)', 'S02-C', 'PSLN-344 vs PSLN-212', '36h', where='Sec 2.2, 4')
regc('DC', 'OT-I priming by MLN DC (%)', 'S02-E', 'PSLN-344 vs PSLN-212', where='Sec 4')
regc('DC', 'MLN DC CD40+ (%)', 'S02-D CD40', 'PSLN-344 vs PSLN-212', 'd3', where='Sec 2.2')
regc('DC', 'MLN DC CD86+ (%)', 'S02-D CD86', 'PSLN-344 vs PSLN-212', 'd3', where='Sec 2.2')
regc('GC', 'ICOS-high Tfh d7 (%)', 'S04-A', 'PSLN-344 vs PSLN-212', 'd7', 'ICOS-high', where='Sec 2.2, 4, 5')
regc('GC', 'Tfr d7 (%)', 'S04-B Foxp3', 'PSLN-344 vs PSLN-212', 'd7', where='Sec 2.2, 4, 5')
regc('GC', 'GC B cells d7 (%)', 'S03-K', 'PSLN-344 vs PSLN-212', 'd7', where='Sec 2.2, 4')
for b, lab in [('S03-C', 'HAI anti-CA09 d14'), ('S03-G', 'HAI anti-Aichi d14'), ('S03-D', 'Neut anti-CA09 d14'), ('S03-H', 'Neut anti-Aichi d14'),
               ('S03-A', 'IgG anti-CA09 d14'), ('S03-E', 'IgG anti-Aichi d14'), ('S13-I', 'IgG anti-CA09 post-boost d28'), ('S13-J', 'IgG anti-Aichi post-boost d28')]:
    regc('Antibody', lab, b, 'PSLN-344 vs PSLN-212', where='Sec 2.2, 4, 5')
regc('Antibody', 'IgG2a/IgG1 anti-CA09 (recomputed from S13-A/B)', 'S13-A/B', 'PSLN-344 vs PSLN-212', where='Sec 2.2, 4')
regc('Antibody', 'IgG2a/IgG1 anti-Aichi (recomputed from S13-C/D)', 'S13-C/D', 'PSLN-344 vs PSLN-212', where='Sec 4')
for b, t_, lab in [('S05-D', 'd3', 'Lung Ki-67+ CD8'), ('S05-E', 'd3', 'Lung GZMB+ CD8'), ('S05-F', 'd14', 'IFN-g+ CD8 d14'), ('S05-G', 'd60', 'IFN-g+ CD8 d60'),
                   ('S05-H', 'd60', 'GZMB+ CD8 d60'), ('S05-I', 'd25', 'Lung TRM d25')]:
    regc('CD8', lab + ' (%)', b, 'PSLN-344 vs PSLN-212', t_, where='Sec 2.2, 4, 5')
regc('Myeloid', 'Lung CD206+ macrophages (%)', 'S11-E', 'PSLN-344 vs PSLN-212', where='Sec 4 (Fig 6)')
regc('Tolerance', 'Lung Treg d7 (%)', 'S04-D', 'PSLN-344 vs PSLN-212', 'd7', where='Fig 6')
g = GAP
reg('Age gap', 'Median share of age deficit closed (40 curated readouts)', f"{100*g.gap_closed.median():.1f}% (IQR {100*g.gap_closed.quantile(.25):.1f}-{100*g.gap_closed.quantile(.75):.1f}%); {int((g.gap_closed>=.5).sum())}/40 readouts >=50%",
    'see Age_gap_curated sheet', '', 'A3', 'Sec 1, 8, Fig 3')
for _, r in MEC.iterrows():
    reg('Mechanism', r.question, f"{fnum(r.mean_a)} vs {fnum(r.mean_b)} (ratio {r.ratio:.2f}); Student p={fp(r.student_p)}; MW p={fp(r.mw_p)}", r.block, f"{r.cells_a} / {r.cells_b}", 'A6 mechanism_tests', 'Sec 4, Table 4, D1')
for _, r in DR.iterrows():
    reg('Dose-response', f"S08-A Hill fit: {r.formulation}", f"top {r.top:.1f}; Emax {r.Emax:.1f} ({r.Emax_lo:.1f}-{r.Emax_hi:.1f}); ED50 {r.ED50:.1f} ug ({r.ED50_lo:.1f}-{r.ED50_hi:.1f}) {r.note if isinstance(r.note,str) else ''}", 'S08-A', 'S08!B3..M7', 'A7', 'Sec 4, 8, 9, Fig 5')
regc('CMC', 'Encapsulation efficiency (%)', 'S08-B', 'PSLN-344 vs PSLN-212', None, where='Sec 4, 3B')
for _, r in CNS.iterrows():
    if r.group in ('PSLN-344', 'CT'):
        reg('Safety', f"S10-A {r.measurand} 36 h, {r.group}", f"{r['mean']:.2f} +/- {r['sd']:.2f} vs PBS 1.00; Tukey p vs PBS={fp(r.tukey_p_vs_PBS)}", 'S10-A', r.cells, 'A8', 'Sec 5, 6 (3A), Fig 7')
for _, r in RG.iterrows():
    reg('Safety', f"S08-D weight nadir, {r.group}", f"{r.mean_nadir:.1f}% +/- {r.sd:.1f}; Tukey p vs vaccine={fp(r.tukey_p_vs_Vaccine)}; present at d10 {int(r.n_present_d10)}/5", 'S08-D', 'S08!B21..AE26', 'A8', 'Sec 1, 5, 9')
R848 = content.R848
for _, r in R848.iterrows():
    reg('Ruled out (R848)', f"{r.block} {r.measurand} {r.time}: {r.a} vs {r.b}", f"GM {r.gm_a:.1f} vs {r.gm_b:.1f}; GMR {r.GMR:.2f}; Tukey p={fp(r.tukey_p)}", r.block, '', 'A12 r848_contrasts', 'Sec 9')
reg('Safety watch', 'Aged PSLN-344 lung Il6 / Tnf at ~72 h (S09-A panel 2, mislabelled 16 h)', 'Il6 7.19x (young 3.10x); Tnf 8.44x (young 0.48x); n=3', 'S09-A panel 2', 'S09!AN4..AS4; S09!AN8..AS8', 'A2/A3', 'Sec 2.2, 10')
reg('Mechanism', 'Lung Ly6C+CCR2+ macrophages d5, PSLN-212 vs PSLN-344 (x10^5)', '19.03 vs 3.42; two-way ANOVA group x time interaction p=8.6e-05', 'S07-A', 'S07!B3..G7', 'A12 two_way_anova', 'Sec 4')
SS = content.SS
for _, r in SS.iterrows():
    reg('Planning', f"Sample size: {r.comparison}", f"n/arm = {r.n_per_arm} ({r.assumptions})", 'S03-C/G, S01-A, S03-A/E', '', 'A11', 'Sec 6')
reg('Integrity', 'Chance per-day identical-weight rate between animals of different blocks', '0.88% (4526/516317)', 'all body-weight blocks', '', 'A1 03b_bw_live_scan', 'Sec 3, App A')
REG = pd.DataFrame(R)

# study plan sheet from document blocks
plan = []
Bk = content.B
for i, b in enumerate(Bk):
    if b[0] == 'h3' and i+1 < len(Bk) and Bk[i+1][0] == 'table' and Bk[i+1][1].get('noheader'):
        for k, v in Bk[i+1][1]['rows']:
            plan.append(dict(study=b[1], item=k.strip('*'), detail=v.replace('**', '')))
PLAN = pd.DataFrame(plan)
gate_tbl = [b[1] for b in Bk if b[0] == 'table' and b[1].get('caption', '').startswith('Table 6')][0]
GATES = pd.DataFrame(gate_tbl['rows'], columns=gate_tbl['header'])

readme = pd.DataFrame({'PSLN analysis workbook (prepared 1 Nov 2026)': [
 'Source files: psln_program_dataset.xlsx (15 sheets) and psln_program_annotation.pdf.',
 'Citation convention: [Sxx-Y] = block as annotated; cell ranges are sheet!cell in the source workbook. [A#] = analysis ID below.',
 'A1 extraction + integrity scans (code 01, 02, 03, 03b, 04) -> Integrity_log, BW_duplicates',
 'A2 continuous endpoints: one-way ANOVA + Tukey (log10 for titres/fold-changes, linear for %); Welch t; exact Mann-Whitney (code 05) -> Continuous_summary, Continuous_contrasts',
 'A3 age-gap closure with bootstrap CI (code 05, 08) -> Age_gap_curated, Age_gap_all',
 'A4 per-block survival: Kaplan-Meier, log-rank, Fisher (code 06) -> Survival_by_group, Survival_tests',
 'A5 pooled survival: Cox stratified by experiment, Mantel-Haenszel (code 06) -> Survival_pooled',
 'A6 mechanistic interventions: Student t + Mann-Whitney (code 07) -> Mechanism_tests',
 'A7 S08-A Hill dose-response fits with bootstrap (code 07) -> Dose_response',
 'A8 safety: S10-A CNS (mean+/-SD, ANOVA+Tukey), S08-D reactogenicity nadir (code 07) -> CNS_S10A, Reactogenicity_S08D',
 'A9 body-weight vs survival reconciliation; survivor nadir (code 09) -> BW_vs_survival',
 'A10 regimen-level biomarker screen (code 10) -> Biomarker_screen',
 'A11 sample-size planning from observed variances (code 08) -> Sample_size',
 'A12 two-way ANOVA for time courses; R848 and other extra contrasts (code 13) -> Two_way_ANOVA, R848_contrasts',
 'Corrections applied: HAI values of 0 (below 1:10 LOD) set to 5; S03-B/F ratios replaced by ratios recomputed from S13-A..D; S06-D excluded (duplicate); S11-A/B, S07-C, S05-A/B excluded; one S03-J record without a day value censored at day 21.',
 'Tidy_* sheets hold every extracted value with its source cell so any number can be traced.']})

with pd.ExcelWriter('/tmp/outputs/PSLN_analysis_workbook.xlsx', engine='xlsxwriter') as xw:
    sheets = [('README', readme), ('Evidence_register', REG), ('Integrity_log', content.LOG), ('Gated_plan', GATES), ('Study_cards', PLAN),
              ('Survival_by_group', SBG), ('Survival_tests', STS), ('Survival_pooled', SPL),
              ('Continuous_summary', SUM), ('Continuous_contrasts', CON), ('Age_gap_curated', GAP), ('Age_gap_all', pd.read_csv(T+'age_gap_closure.csv')),
              ('Mechanism_tests', MEC), ('Dose_response', DR), ('CNS_S10A', CNS), ('Reactogenicity_S08D', RG),
              ('BW_vs_survival', pd.read_csv(T+'bodyweight_vs_survival.csv')), ('BW_duplicates', pd.read_csv('/tmp/work/tidy/bw_duplicate_trajectories.csv')),
              ('Biomarker_screen', content.BIO), ('Multiplicity_Holm', pd.read_csv(T+'multiplicity_holm.csv')), ('Sample_size', SS), ('Two_way_ANOVA', pd.read_csv(T+'two_way_anova.csv')), ('R848_contrasts', R848),
              ('Tidy_continuous', C), ('Tidy_survival', S), ('Tidy_bodyweight', BW)]
    for name, df in sheets:
        df.to_excel(xw, sheet_name=name, index=False)
        ws = xw.sheets[name]; wb = xw.book
        hdr = wb.add_format({'bold': True, 'bg_color': '#dbe5f1', 'text_wrap': True, 'valign': 'top', 'border': 1})
        wrap = wb.add_format({'text_wrap': True, 'valign': 'top'})
        for j, col in enumerate(df.columns):
            ws.write(0, j, str(col), hdr)
            maxlen = min(max([len(str(col))] + [len(str(x)) for x in df[col].head(200)]), 80)
            ws.set_column(j, j, max(8, maxlen*0.9 if maxlen < 30 else 45), wrap if maxlen >= 30 else None)
        ws.freeze_panes(1, 0)
print('register rows', len(REG), '| plan rows', len(PLAN))
