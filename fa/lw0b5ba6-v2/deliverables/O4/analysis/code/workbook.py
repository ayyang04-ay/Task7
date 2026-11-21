import pandas as pd, numpy as np, re
from openpyxl.utils import column_index_from_string as ci, get_column_letter as gl
vals = pd.read_csv('values_corrected.csv'); surv = pd.read_csv('survival.csv'); bw = pd.read_csv('bw.csv')
def rng(cells):
    rc = []
    for c in cells:
        sh, co = c.split('!'); m = re.match(r'([A-Z]+)(\d+)', co); rc.append((sh, ci(m.group(1)), int(m.group(2))))
    sh = rc[0][0]; c0 = min(x[1] for x in rc); c1 = max(x[1] for x in rc); r0 = min(x[2] for x in rc); r1 = max(x[2] for x in rc)
    return f"{sh}!{gl(c0)}{r0}:{gl(c1)}{r1}"
rows=[]
for b,d in vals.groupby('block', sort=False):
    rows.append(dict(block=b, type='continuous', cell_range=rng(d.cell), groups='; '.join(dict.fromkeys(d.group)), unit=d.unit.iloc[0], timepoints='; '.join(map(str,dict.fromkeys(d.time.astype(str)))), n_values=len(d)))
for b,d in surv.groupby('block', sort=False):
    rows.append(dict(block=b, type='survival (day, event)', cell_range=rng(list(d.cell_event)+list(d.cell_day.dropna())), groups='; '.join(dict.fromkeys(d.group)), unit='days; 1=death 0=censored', timepoints='', n_values=len(d)))
for b,d in bw.groupby('block', sort=False):
    rows.append(dict(block=b, type='body weight (% day 0)', cell_range=rng(d.cell), groups='; '.join(dict.fromkeys(d.group)), unit='% of day-0 weight', timepoints='days '+','.join(map(lambda x: str(int(x)), sorted(d.day.unique()))), n_values=int(d.value.notna().sum())))
src = pd.DataFrame(rows)
src.to_csv('/tmp/outputs/analysis/Source_map.csv', index=False)
readme = pd.DataFrame({'item':[
 'Purpose','Source files','How to trace a number','Corrections applied before analysis','Exclusions','Statistical methods','Tables','Reproduce'],
 'description':[
 'Supporting analyses for the PSLN-344 portfolio-review proposal (1 Nov 2026). Every number in the proposal cites a workbook block (e.g., S06-A), an analysis table (T1-T15) and/or an audit finding (A1-A17).',
 'psln_program_dataset.xlsx (last modified 3 Sep 2026) and psln_program_annotation.pdf (15 Sep 2026).',
 'Source_map gives the cell range of every block. Data_values / Data_survival / Data_bodyweight hold each per-animal value with its exact sheet!cell address.',
 '(1) S03-B and S03-F group labels rotated back to match raw subclass titres in S13-A..D (A6). (2) HAI values of 0 (below the 1:10 lowest dilution) set to 5 for log analysis. (3) S09-A second block treated as 72 h (A7). (4) S03-J animal with blank day (S03!G46, event 0) censored at day 21.',
 'S06-D (exact duplicate of S06-C; A1) removed from pooled sets B-D. S11-A and S11-B (A2), S05-A/B (A10), S07-C (A11), S13-F/G as corroboration (A5) and S08 rows 89-101 (A15) not interpreted. Body-weight blocks not used as endpoints (A3, A8).',
 'Log-rank (validated against lifelines 0.30.3), stratified log-rank, Mantel-Haenszel risk difference (Sato/Greenland-Robins variance), Fisher exact, Newcombe CIs; one-way ANOVA with Tukey HSD (the annotation\'s stated method) and Welch t with 95% CI on log10 scale for titres/fold-changes and linear scale for percentages; Hill/Emax fits; percentile bootstrap (4,000 resamples) for restoration indices; exact power for Fisher tests.',
 'T1 survival by group; T2 pairwise survival tests; T3 pooled survival and sensitivity sets; T4 immunology contrasts; T5 S09-A timepoint check; T6 lung cytokines 16 h; T7 CNS transcripts; T8 post-vaccination body weight; T9 mechanism perturbations; T10 dose-response; T11 restoration index; T12 power; T13 survival vs body-weight concordance; T14 body-weight shared fractional parts; T15 S11-A vs S11-B positions; A audit log.',
 'Python scripts in analysis/code (parse.py first, then survstats.py, pooled.py, immuno.py, safety.py, moa.py, extra.py, power.py, concord.py, bwforensic.py, audit.py, figs.py).']})
tabs = [('README',readme),('A_audit_log','A_data_integrity_audit_log.csv'),('Source_map',src),
        ('T1_survival_by_group','T1_survival_by_group.csv'),('T2_survival_pairwise','T2_survival_pairwise_tests.csv'),('T3_pooled_survival','T3_pooled_survival.csv'),
        ('T4_immunology','T4_immunology_contrasts.csv'),('T5_S09A_timepoint','T5_S09A_timepoint_check.csv'),('T6_lung_cytokines_16h','T6_lung_cytokines_16h.csv'),
        ('T7_CNS','T7_CNS_transcripts.csv'),('T8_postvacc_weight','T8_postvaccination_bodyweight.csv'),('T9_mechanism','T9_mechanism_perturbations.csv'),
        ('T10_dose_response','T10_dose_response.csv'),('T11_restoration_index','T11_restoration_index.csv'),('T12_power','T12_power_survival.csv'),
        ('T13_surv_vs_bw','/tmp/work/concordance.csv'),('T14_bw_shared_decimals','T14_bodyweight_shared_fractional_parts.csv'),('T15_S11A_vs_S11B','T15_S11A_vs_S11B_positions.csv'),
        ('Data_values',vals),('Data_survival',surv),('Data_bodyweight',bw)]
with pd.ExcelWriter('/tmp/outputs/PSLN_analysis_workbook.xlsx', engine='xlsxwriter') as xw:
    wb = xw.book; wrap = wb.add_format({'text_wrap':True,'valign':'top'}); hdr = wb.add_format({'bold':True,'bg_color':'#DDEBF7','text_wrap':True,'valign':'top','border':1})
    for name, t in tabs:
        df = t if isinstance(t, pd.DataFrame) else pd.read_csv(t if t.startswith('/') else '/tmp/outputs/analysis/'+t)
        df.to_excel(xw, sheet_name=name[:31], index=False)
        ws = xw.sheets[name[:31]]
        for j,c in enumerate(df.columns):
            width = min(60, max(10, int(df[c].astype(str).str.len().quantile(0.9) if len(df) else 10), len(str(c))+2))
            ws.set_column(j, j, width, wrap if width>=40 else None)
            ws.write(0, j, c, hdr)
        ws.freeze_panes(1,0)
print('workbook written'); print(src.head(8).to_string())
