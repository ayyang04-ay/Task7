import pandas as pd, numpy as np
T = '/tmp/work/tidy'
out = '/tmp/outputs/PSLN_analysis_tables.xlsx'
readme = pd.DataFrame({'item': [
 'Purpose', 'Source data', 'Data cut', 'How to verify a number', 'Scales', 'Tests', 'Survival pooling', 'Integrity scenarios',
 'Group labels', 'Excluded blocks', 'Reproduce'],
 'description': [
 'Supporting tables for the PSLN portfolio proposal. Every number in the proposal can be traced to a sheet here, and every data value to its workbook cell.',
 'psln_program_dataset.xlsx (15 sheets) and psln_program_annotation.pdf (block definitions).',
 'Complete as of 1 November 2026 (as provided).',
 'Start at Citation_index: each headline number in the proposal is recomputed there from the analysis tables, with its source block and sheet. Tidy_* sheets list every raw value with its source cell (column "cell").',
 'Antibody titres analysed on log2 (HI values of 0 below the 1:10 limit of detection set to 5); qPCR fold-changes on log10; S09-A already log10; percentages/counts linear.',
 'One-way ANOVA + Tukey HSD across all groups in a block (stated method); Welch and Student t for pre-specified contrasts; exact Mann-Whitney U (robustness); Hedges g; two-way ANOVA for time courses; Kaplan-Meier/log-rank and Fisher exact per experiment.',
 'Mantel-Haenszel risk difference, Cochran-Mantel-Haenszel test and log-rank stratified by experiment across the 11 aged-mouse challenge experiments.',
 'As recorded; excluding 7 integrity-flagged experiments; deaths inferred from paired weight records; worst case for PSLN-344 (max deaths for PSLN-344, min for comparators).',
 'Sham = vaccine + empty liposome (vehicle). Vaccine/PBS = no liposome. (Y) = young (7-8 wk). Printed labels retained in column group_printed of Tidy sheets.',
 'S07-C (duplicate group labels), S08 rows 89-101 (unlabelled), S11-A/B (shared values) excluded from inference; S03-B/F replaced by ratios recomputed from S13-A-D; S09-A and S04-B Tfh:Tfr treated as derived.',
 'Run code/parse.py then analysis_*.py, audit*.py, figures.py, build_workbook.py, build_report.py (see code/README.txt).']})
sheets = [('README', readme),
          ('Citation_index', pd.read_csv(f'{T}/citation_index.csv')),
          ('Integrity_findings', pd.read_csv(f'{T}/integrity_findings.csv')),
          ('Flagged_experiments', pd.read_csv(f'{T}/flagged_experiments.csv')),
          ('Aged_survival_by_experiment', pd.read_csv(f'{T}/aged_experiment_table.csv')),
          ('Pooled_survival_scenarios', pd.read_csv(f'{T}/pooled_survival.csv')),
          ('Survival_all_arms', pd.read_csv(f'{T}/summary_survival.csv')),
          ('Survival_pairwise', pd.read_csv(f'{T}/pairwise_survival.csv')),
          ('Key_endpoints_ratios', pd.read_csv(f'{T}/key_endpoints_ratios.csv')),
          ('Forest_344_vs_212', pd.read_csv(f'{T}/forest_344_vs_212.csv')),
          ('Continuous_summary', pd.read_csv(f'{T}/summary_continuous.csv')),
          ('Continuous_contrasts', pd.read_csv(f'{T}/contrasts_continuous.csv')),
          ('Biomarker_candidates', pd.read_csv(f'{T}/biomarker_candidates.csv')),
          ('Mechanistic_tests', pd.read_csv(f'{T}/mechanistic_tests.csv')),
          ('Safety_S08D_nadir', pd.read_csv(f'{T}/safety_S08D_nadir.csv')),
          ('Dose_response_fits', pd.read_csv(f'{T}/dose_response_fits.csv')),
          ('Twoway_ANOVA', pd.read_csv(f'{T}/twoway_anova.csv')),
          ('Sample_size', pd.read_csv(f'{T}/sample_size.csv')),
          ('Survival_vs_weight', pd.read_csv(f'{T}/audit_survival_vs_weight.csv')),
          ('Weight_recycling_pairs', pd.read_csv(f'{T}/audit_weight_recycling.csv')),
          ('Audit_S11A_vs_S11B', pd.read_csv(f'{T}/audit_s11.csv')),
          ('Tidy_continuous', pd.read_csv(f'{T}/continuous.csv')),
          ('Tidy_survival', pd.read_csv(f'{T}/survival.csv')),
          ('Tidy_weights', pd.read_csv(f'{T}/weights.csv'))]
with pd.ExcelWriter(out, engine='xlsxwriter') as xw:
    wb = xw.book
    hdr = wb.add_format({'bold': True, 'bg_color': '#1f4e79', 'font_color': 'white', 'text_wrap': True, 'valign': 'top', 'border': 1})
    wrap = wb.add_format({'text_wrap': True, 'valign': 'top'})
    for name, df in sheets:
        df = df.copy()
        for c in df.columns:
            if df[c].dtype == object:
                df[c] = df[c].astype(str).replace('nan', '')
        df.to_excel(xw, sheet_name=name[:31], index=False)
        ws = xw.sheets[name[:31]]
        for j, c in enumerate(df.columns):
            ws.write(0, j, c, hdr)
            width = min(60, max(10, int(df[c].astype(str).str.len().quantile(0.9)) + 2 if len(df) else 12, len(str(c)) + 2))
            ws.set_column(j, j, width, wrap if width >= 40 else None)
        ws.freeze_panes(1, 0)
        ws.autofilter(0, 0, max(len(df), 1), len(df.columns) - 1)
print('written', out, [n for n, _ in sheets])
