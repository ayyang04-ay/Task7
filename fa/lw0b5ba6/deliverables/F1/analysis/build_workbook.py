"""build_workbook.py -- collects the evidence ledger, the defect register and the analysis tables into one Excel file."""
import pandas as pd, os
from paths import TABLES as T, OUT
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Alignment, PatternFill

SHEETS = [  # (sheet name, file, description)
 ('E_ledger', 'T18_evidence_ledger.csv', 'Every [E#] tag in the proposal: statement, workbook cells, analysis'),
 ('D_defects', 'T17_record_defects.csv', 'Register of record defects D1-D16'),
 ('T0_observations', 'T0_tidy_all_observations.csv', 'All 6,120 observations read from the workbook, one per row, with cell reference'),
 ('T1_counts', 'T1_observation_counts.csv', 'Observations per block and group as found'),
 ('T2_surv_vs_weight', 'T2_survival_vs_weight_crosscheck.csv', 'Deaths per survival table vs deaths implied by the paired weight block'),
 ('T3_identical_vectors', 'T3_identical_vectors.csv', 'Identical value vectors in different groups or blocks'),
 ('T3c_reused_traces', 'T3c_reused_weight_traces.csv', 'Body-weight traces shared between blocks (>= 5 identical values)'),
 ('T3e_identical_survival', 'T3e_identical_survival.csv', 'Identical time-to-event vectors in different blocks'),
 ('T4_label_checks', 'T4_label_crosschecks.csv', 'Recomputation checks: ratio blocks vs subclass titres; S09-A vs S01-A'),
 ('T5_survival_by_block', 'T5_survival_by_block.csv', 'Survivors, exact CI and days of death for every time-to-event block'),
 ('T6_survival_contrasts', 'T6_survival_contrasts.csv', 'Log-rank (asymptotic, exact) and Fisher tests within each experiment'),
 ('T6b_logrank_R_check', 'T6b_logrank_R_check.csv', 'Python log-rank statistic vs R survival::survdiff'),
 ('T7_survival_pooled', 'T7_survival_pooled.csv', 'Pooled and stratified survival analyses with sensitivity sets'),
 ('T7b_cox', 'T7b_stratified_cox.csv', 'Stratified Cox hazard ratios (R)'),
 ('T8_durability', 'T8_durability_background.csv', 'Day-14 vs day-60 survival and background mortality'),
 ('T9_group_summaries', 'T9_group_summaries.csv', 'Mean, SD, geometric mean per block, read-out and group'),
 ('T10_contrasts', 'T10_pairwise_contrasts.csv', 'All pairwise contrasts: Welch, exact Mann-Whitney, Tukey'),
 ('T11_restoration', 'T11_restoration_and_biomarker_triage.csv', 'Restoration index and biomarker separation for 40 read-outs'),
 ('T12_weight_nadir', 'T12_weight_nadir_by_group.csv', 'Lowest body weight per group in every weight block'),
 ('T12c_nadir_contrasts', 'T12c_weight_nadir_contrasts.csv', 'Weight-nadir contrasts, PSLN-344 vs comparators'),
 ('T13_tolerability', 'T13_tolerability_S08D.csv', 'Body weight after dosing without challenge (S08-D)'),
 ('T14_dose_response', 'T14_dose_response_fit.csv', 'Hill-model fit of the interferon dose-response (S08-A)'),
 ('T14b_dose_means', 'T14b_dose_response_means.csv', 'Mean interferon response per dose'),
 ('T15_two_way_anova', 'T15_timecourse_two_way_anova.csv', 'Two-way ANOVA for time-course blocks'),
 ('T16_power', 'T16_power_sample_size.csv', 'Exact power and sample-size calculations'),
]
path = OUT + 'PSLN-344_evidence_workbook.xlsx'
with pd.ExcelWriter(path, engine='openpyxl') as xw:
    readme = pd.DataFrame([dict(sheet=s, content=d) for s, f, d in SHEETS if os.path.exists(T + f)])
    readme.to_excel(xw, sheet_name='README', index=False, startrow=4)
    ws = xw.sheets['README']
    ws['A1'] = 'PSLN-344 evidence workbook'; ws['A1'].font = Font(bold=True, size=13)
    ws['A2'] = 'Companion to PSLN-344_portfolio_proposal. Source data: psln_program_dataset.xlsx and psln_program_annotation.pdf. Built by analysis/run_all.sh on the data as of 1 November 2026.'
    ws['A3'] = 'Cell references are given as Sheet!Range of the source workbook. Group names are as printed in the source workbook ("Sham" = vehicle + vaccine).'
    for s, f, d in SHEETS:
        if not os.path.exists(T + f): print('missing', f); continue
        df = pd.read_csv(T + f)
        df.to_excel(xw, sheet_name=s[:31], index=False)
    for ws in xw.book.worksheets:
        hdr_row = 5 if ws.title == 'README' else 1
        for c in ws[hdr_row]:
            c.font = Font(bold=True); c.fill = PatternFill('solid', fgColor='E8EEF4'); c.alignment = Alignment(wrap_text=True, vertical='top')
        ws.freeze_panes = ws.cell(row=hdr_row + 1, column=1)
        for i, col in enumerate(ws.iter_cols(min_row=hdr_row, max_row=min(ws.max_row, 300)), start=1):
            width = max(len(str(c.value)) if c.value is not None else 0 for c in col)
            ws.column_dimensions[get_column_letter(i)].width = max(8, min(70, width + 2))
        if ws.title in ('E_ledger', 'D_defects'):
            for row in ws.iter_rows(min_row=2):
                for c in row: c.alignment = Alignment(wrap_text=True, vertical='top')
print('workbook written:', path)
