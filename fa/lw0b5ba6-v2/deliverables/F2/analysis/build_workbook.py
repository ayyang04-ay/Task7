"""Evidence workbook: ledger, statistics, QC and tidy data in one xlsx."""
import pandas as pd, numpy as np, os
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from blocks import B, T, S, W
out = os.path.join(os.environ.get('PSLN_OUT', '/tmp/outputs'), 'PSLN_evidence_workbook.xlsx')
led = pd.read_csv('evidence_ledger_with_usage.csv')
led = led.rename(columns={'Value_as_cited':'Value as cited','Source_blocks':'Source blocks','Cited_in_proposal_section':'Cited in proposal (section)','Raw':'Raw value(s)'})
led = led[['ID','Cited in proposal (section)','Value as cited','Description','Source blocks','Cells','Method','Raw value(s)','Key']]
tidyB = pd.concat([d.assign(analyte=d['analyte'] if 'analyte' in d.columns else '') for d in B.values()])[['block','sheet','group','analyte','rep','value','cellref']]
def tcol(d): return [c for c in d.columns if c in ('day','time','dose_ug')][0]
tidyT = pd.concat([d.rename(columns={tcol(d):'time_or_dose'}).assign(axis=tcol(d)) for d in T.values()])[['block','sheet','group','axis','time_or_dose','rep','value','cellref']]
tidyS = pd.concat(S.values())[['block','sheet','group','day','event','cellref']]
tidyW = pd.concat(W.values())[['block','sheet','group','rep','day','value','cellref']]
readme = pd.DataFrame({'Sheet':['README','Ledger','Survival_by_group','Survival_pairwise','Survival_pooled','Restoration_vs_young','Contrasts_all','Descriptives','Timecourse_desc','Timecourse_pairwise','Timecourse_anova','Dose_response','Weight_after_dosing','Weight_after_challenge','QC_log','QC_survival_vs_weight','QC_duplicate_traces','Tidy_endpoints','Tidy_timecourses','Tidy_survival','Tidy_weights'],
 'Content':['This sheet. Source: psln_program_dataset.xlsx (last modified 2026-09-03) and psln_program_annotation.pdf (2026-09-15). All values computed by the scripts in the analysis folder; no value of the source workbook was altered.',
  'Evidence ledger: every number computed for the proposal, with source blocks, cell ranges and method. Column B shows the proposal section in which the number is first cited (blank = computed but not cited).',
  'Each survival block and group: n, deaths, survivors, exact 95% CI, death days, cell range.',
  'Within-block pairwise tests: log-rank (asymptotic and permutation) and Fisher exact.',
  'Pooled PSLN-344 vs PSLN-212 survival in aged mice: sets A-F (as printed, conservative, all strains, worst case), Mantel-Haenszel difference, CMH and stratified log-rank.',
  'Aged PSLN-344 and PSLN-212 as % of the young benchmark for every single-time-point block holding all three groups.',
  'Every pairwise contrast in every single-time-point block (both directions): means, geometric means, ratio, Welch CI and p, Tukey p, exact Mann-Whitney p.',
  'Descriptive statistics per block and group (single-time-point blocks).','Descriptive statistics per block, group and time (or dose).','Pairwise tests at each time point (Welch; Tukey within time point and across all cells).','Two-way ANOVA per time-course block.',
  'Hill fits of the Ifnb1 dose-response (S08-A).','Per-animal largest weight loss after dosing (S08-D).','Per-group largest weight loss after challenge (all weight blocks).',
  'Data-quality log (22 flags).','Survival block vs linked weight block: survivors implied by each.','Animal weight traces that recur in another block (>= 3 distinct identical values).',
  'Tidy data: single-time-point blocks, one row per value with its cell reference.','Tidy data: time-course and dose-response blocks.','Tidy data: time-to-event blocks (event 1 = death).','Tidy data: body-weight blocks.']})
sheets = [('README', readme), ('Ledger', led),
          ('Survival_by_group', pd.read_csv('stats_survival_groups.csv')), ('Survival_pairwise', pd.read_csv('stats_survival_pairwise.csv')), ('Survival_pooled', pd.read_csv('stats_survival_pooled.csv')),
          ('Restoration_vs_young', pd.read_csv('restoration_index.csv')), ('Contrasts_all', pd.read_csv('stats_contrasts_all.csv')), ('Descriptives', pd.read_csv('desc_endpoint_blocks.csv')),
          ('Timecourse_desc', pd.read_csv('desc_timecourse_blocks.csv')), ('Timecourse_pairwise', pd.read_csv('stats_timecourse_pairwise.csv')), ('Timecourse_anova', pd.read_csv('stats_timecourse_anova.csv')),
          ('Dose_response', pd.read_csv('dose_response_S08A.csv')), ('Weight_after_dosing', pd.read_csv('safety_S08D_nadir.csv')), ('Weight_after_challenge', pd.read_csv('bw_challenge_nadir.csv')),
          ('QC_log', pd.read_csv('qc_log.csv')), ('QC_survival_vs_weight', pd.read_csv('qc_tte_vs_bodyweight.csv')), ('QC_duplicate_traces', pd.read_csv('qc_duplicate_trajectories_nonflat.csv')),
          ('Tidy_endpoints', tidyB), ('Tidy_timecourses', tidyT), ('Tidy_survival', tidyS), ('Tidy_weights', tidyW)]
with pd.ExcelWriter(out, engine='openpyxl') as xw:
    for name, df in sheets:
        df.to_excel(xw, sheet_name=name, index=False)
        ws = xw.sheets[name]
        for c in ws[1]:
            c.font = Font(bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor='12324F'); c.alignment = Alignment(vertical='top', wrap_text=True)
        ws.freeze_panes = 'A2'
        for i, col in enumerate(df.columns, 1):
            mx = max([len(str(col))] + [len(str(v)) for v in df[col].head(300)])
            ws.column_dimensions[get_column_letter(i)].width = min(max(9, mx + 2), 70)
        if name in ('README','Ledger','QC_log'):
            for row in ws.iter_rows(min_row=2):
                for c in row: c.alignment = Alignment(vertical='top', wrap_text=True)
print('wrote', out, [(n, len(d)) for n, d in sheets])
