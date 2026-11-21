"""Collect every supporting table into one Excel workbook (values only; all numbers are produced by the scripts named in each sheet)."""
import pandas as pd, os
T = '../tables/'
sheets = [
 ('Evidence ledger', 'T0_evidence_ledger.csv', 'Every number quoted in the proposal (used_in_proposal = True) plus all other numbers computed: value, workbook block, cell range, method, script. Produced by 10_numbers.py / 11_build_proposal.py.'),
 ('QC log', 'QC_log.csv', 'Data-integrity items Q1-Q15: finding, consequence, handling, action. 02e_qc_log.py.'),
 ('T1 survival by group', 'T1_survival_by_group.csv', 'Per experiment and group: n, deaths, survivors, survival % with exact 95% CI, death days. 03_survival.py.'),
 ('T2 survival pairwise', 'T2_survival_pairwise.csv', 'Pairwise log-rank (asymptotic and exact permutation) and Fisher exact tests within each experiment. 03_survival.py.'),
 ('T3 survival pooled', 'T3_survival_pooled.csv', 'Pooled survival, stratified log-rank and Mantel-Haenszel risk differences, as printed and for the core experiments. 03b_survival_pooled.py.'),
 ('T4 group summaries', 'T4_group_summaries.csv', 'Mean, SD, median, range (and geometric mean titre with 95% CI) for every non-survival block. 04_immunology_stats.py.'),
 ('T5 pairwise tests', 'T5_pairwise_tests.csv', 'Tukey HSD / Student t for every pair of groups in every block (log2 scale added for titres and fold-changes). 04_immunology_stats.py.'),
 ('T6 omnibus tests', 'T6_omnibus_tests.csv', 'One-way and two-way ANOVA per block. 04_immunology_stats.py.'),
 ('T7 restoration', 'T7_restoration_table.csv', 'Aged PSLN-212 and PSLN-344 as % of the young PSLN-212 response, fold differences and p-values. 04b_restoration.py.'),
 ('T8 dose-response', 'T8_dose_response_S08A.csv', 'Hill-model fits of lung Ifnb1 vs dose with bootstrap CIs. 05_dose_response.py.'),
 ('T9 tolerability', 'T9_tolerability_S08D.csv', 'Body-weight nadir after immunisation (no challenge). 06_safety.py.'),
 ('T10 lung cytokines', 'T10_lung_cytokines_S09A.csv', 'Lung transcripts (geometric mean fold) for both S09-A panels. 06_safety.py.'),
 ('T11 morbidity', 'T11_morbidity_bodyweight.csv', 'Maximum weight loss after challenge by experiment and group (supportive only; see QC Q5). 07_morbidity_and_factorial.py.'),
 ('T12 power', 'T12_power_survival.csv', 'Exact power of Fisher test for survival end-points at several group sizes. 08_power.py.'),
 ('T13 biomarkers', 'T13_biomarker_separation.csv', 'Candidate biomarkers: group means, ranges, overlap between aged PSLN-344 and PSLN-212, candidate cut-offs. 04c_biomarker_separation.py.'),
 ('QC survival vs weight', 'QC_survival_vs_bodyweight.csv', 'Deaths in each time-to-event block against animals leaving the paired body-weight record. 02b_qc_surv_bw.py.'),
 ('QC shared weights', 'QC_bodyweight_shared_values.csv', 'Body-weight group matrices that share identical values at the same animal/day positions. 02c_qc_duplicates.py.'),
 ('QC shared values', 'QC_shared_values_nonBW.csv', 'Order-insensitive scan for re-used values between groups of different non-weight blocks. 02d_qc_shared_values.py.'),
 ('Block index', '../data_tidy/psln_block_index.csv', 'Every block parsed: sheet, kind, stated n, observed n per group. 01_export_tidy.py.'),
]
out = T + 'PSLN_supporting_analysis.xlsx'
with pd.ExcelWriter(out, engine='xlsxwriter') as xw:
    wb = xw.book
    hdr = wb.add_format({'bold': True, 'bg_color': '#EDF2F7', 'border': 1, 'text_wrap': True, 'valign': 'top'})
    note = wb.add_format({'italic': True, 'font_color': '#444444', 'text_wrap': True, 'valign': 'top'})
    wrap = wb.add_format({'text_wrap': True, 'valign': 'top'})
    # contents sheet
    ws = wb.add_worksheet('Contents'); xw.sheets['Contents'] = ws
    ws.write_row(0, 0, ['Sheet', 'Content and producing script'], hdr); ws.set_column(0, 0, 26); ws.set_column(1, 1, 130, wrap)
    for i, (name, f, desc) in enumerate(sheets, start=1):
        ws.write_url(i, 0, f"internal:'{name}'!A1", string=name); ws.write(i, 1, desc, wrap)
    ws.write(len(sheets) + 2, 0, 'Source data'); ws.write(len(sheets) + 2, 1, 'psln_program_dataset.xlsx (last saved 3 Sep 2026) and psln_program_annotation.pdf (15 Sep 2026). Group labels are kept as printed in the workbook.', wrap)
    for name, f, desc in sheets:
        df = pd.read_csv(T + f)
        df.to_excel(xw, sheet_name=name, index=False, startrow=1)
        ws = xw.sheets[name]
        ws.merge_range(0, 0, 0, max(3, min(len(df.columns) - 1, 10)), desc, note); ws.set_row(0, 32)
        for j, c in enumerate(df.columns):
            ws.write(1, j, c, hdr)
            width = min(60, max(10, int(df[c].astype(str).str.len().quantile(0.9)) + 2, len(str(c)) + 2))
            ws.set_column(j, j, width, wrap if width >= 40 else None)
        ws.freeze_panes(2, 1); ws.autofilter(1, 0, 1 + len(df), len(df.columns) - 1)
print('written', out, os.path.getsize(out))
