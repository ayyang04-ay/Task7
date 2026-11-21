import pandas as pd, numpy as np
import os
out = os.path.join(os.environ.get('PSLN_OUT', '/tmp/outputs'), 'PSLN_analysis_tables.xlsx')
def rd(f): return pd.read_csv(f)
sheets = []
readme = pd.DataFrame({'Item':[
 'Purpose','Source data','Data cut','Conventions','Conventions','Conventions','Conventions','Conventions','Statistics','Statistics','Statistics','Statistics','Reproducibility',
 'Sheet: Evidence_index','Sheet: Integrity_register','Sheet: Survival_by_block','Sheet: Survival_pairwise','Sheet: Survival_pooled','Sheet: Survival_vs_weights','Sheet: Weight_status','Sheet: Endpoint_descriptives','Sheet: Endpoint_pairwise','Sheet: Endpoint_anova','Sheet: Scorecard','Sheet: Biomarkers','Sheet: Dose_response','Sheet: N_mismatch','Sheet: Dup_weights / Dup_quant / Dup_survival','Sheet: Power'],
 'Description':[
 'Supporting tables for "PSLN program: portfolio recommendation and proposal for next steps". Every number in the proposal traces to a row here and, through the cell references, to the source workbook.',
 'psln_program_dataset.xlsx (15 sheets, S01–S15) and psln_program_annotation.pdf (19 pages).',
 'Workbook last modified 2026-09-03; annotation created 2026-09-15 (file metadata). Analysis run 2026-11-01.',
 'Cell references are sheet!range in the source workbook. "S06-E(r71)" and "S06-F(r71)" are the second blocks carrying the labels S06-E and S06-F (rows 71–98; prior-infection study).',
 'Groups: Sham = vaccine + empty liposome; PSLN-212 = CDN-1807 liposome; PSLN-344 = CDN-1807 + Mn2+ liposome; (Y) = young (7–8 weeks); no suffix = aged (≥20 months) unless the annotation says otherwise; CMP-204 = cGAMP liposome; Untreated = aged, no vaccine, no adjuvant, NO challenge.',
 'Titers and mRNA fold-changes are summarized as geometric means and tested on the log10 scale; percentages on the linear scale. HAI "0" (below the 1:10 starting dilution) is set to 5. S09-A is stored as log10 and back-transformed; its second panel (columns X–AS) is analyzed as 72 h (see Integrity_register DI-02).',
 'IgG2a:IgG1 ratios are recomputed from S13-A–D; the S03-B/S03-F blocks are mislabeled (DI-01).',
 'Time-to-event: event 1 = death/humane endpoint, 0 = alive at end of observation. The S03-J PSLN-344 row without a day value is excluded (n=9).',
 'Continuous endpoints: one-way ANOVA with Tukey HSD (the method stated in the annotation), plus Welch t-test and exact Mann–Whitney as robustness checks; two-way ANOVA for time courses (stats_misc.py).',
 'Survival: Kaplan–Meier, log-rank and Fisher exact per block; pooled analysis = exact (Clopper–Pearson) CI on pooled proportions, Mantel–Haenszel risk difference stratified by experiment, stratified log-rank.',
 'Body-weight records: an animal is treated as removed when its cells go blank, or when a trailing run of identical values reaches the last day (run ≥3, or run of 2 at ≤90 % of baseline) — i.e. last observation carried forward.',
 'No adjustment for multiplicity across blocks; group sizes are 3–10, single experiments, with no randomization or blinding information in the annotation. P-values are descriptive.',
 'Python scripts in analysis_code/: parse_blocks.py → quant_long.csv, surv_long.csv, wt_long.csv; stats_quant.py; stats_surv.py; pooled_surv.py; wt_status.py; audit_*.py; dose_response.py; morbidity.py; biomarkers.py; power.py; fig*.py.',
 'Headline numbers used in the proposal, with source cells and the analysis table they come from.',
 'Nineteen data-integrity findings: location, evidence, effect on conclusions, handling, action.',
 'Survivors/n, exact 95 % CI, median survival and death days for every group in every time-to-event block.',
 'All pairwise log-rank and Fisher tests within each block.',
 'Pooled analyses (base case, sensitivity, by challenge interval, by strain).',
 'Time-to-event table vs survivors implied by the paired body-weight block, group by group.',
 'Per-group status derived from body-weight records (alive at end, removed, last live day, nadir).',
 'n, mean, SD, median, geometric mean and source cells for every group in every continuous block.',
 'All pairwise comparisons (effect, 95 % CI, Tukey, Welch, Mann–Whitney).',
 'One-way ANOVA and Kruskal–Wallis per block.',
 'One row per endpoint: Sham, CMP-204, PSLN-212, PSLN-344, young; PSLN-344 vs PSLN-212; PSLN-344 vs young.',
 'Effect sizes PSLN-344 vs PSLN-212 and response as % of the young benchmark.',
 'Hill fits to the Ifnb1 dose-response (S08-A).',
 'Blocks where the stated n differs from the rows present.',
 'Duplicate-value scans across blocks.',
 'Sample-size calculations used in the study proposals.']})
sheets.append(('README', readme))
sheets.append(('Evidence_index', rd('evidence_index.csv')))
sheets.append(('Integrity_register', rd('integrity_register.csv')))
sg = rd('surv_groups.csv'); sg['median_days'] = sg['median_days'].replace(np.inf, 'not reached')
sheets.append(('Survival_by_block', sg.round(2)))
sheets.append(('Survival_pairwise', rd('surv_pairs.csv')))
sheets.append(('Survival_pooled', rd('pooled_survival.csv')))
sheets.append(('Survival_vs_weights', rd('surv_vs_weights.csv')))
sheets.append(('Weight_status', rd('wt_group_status.csv')))
sheets.append(('Endpoint_descriptives', rd('desc_stats.csv')))
sheets.append(('Endpoint_pairwise', rd('pairwise_stats.csv')))
sheets.append(('Endpoint_anova', rd('anova_stats.csv')))
sheets.append(('Scorecard', rd('scorecard.csv')))
sheets.append(('Biomarkers', rd('biomarker_table.csv')))
sheets.append(('Dose_response', rd('dose_response_fit.csv')))
sheets.append(('N_mismatch', rd('audit_n_mismatch.csv')))
sheets.append(('Dup_weights', rd('audit_dups_weights.csv')))
sheets.append(('Dup_quant', rd('audit_dups_quant.csv')))
sheets.append(('Dup_survival', rd('audit_dups_surv.csv')))
pw = pd.DataFrame([
 ('Survival, two-sided Fisher exact, alpha 0.05, 80% vs 10%', 'n per arm for ≥80% power', 10), ('Survival, 80% vs 20%', 'n per arm for ≥80% power', 12), ('Survival, 80% vs 30%', 'n per arm for ≥80% power', 18),
 ('Survival, 80% vs 20%, n=12', 'power', 0.81), ('Survival, 80% vs 30%, n=12', 'power', 0.61), ('Survival, 80% vs 30%, n=15', 'power', 0.68),
 ('GMT, 2-fold difference, log10 SD 0.25 (observed within-group SD 0.14–0.37)', 'n per arm for 80% power', 12), ('GMT, 2-fold difference, log10 SD 0.30', 'n per arm for 80% power', 17), ('GMT, 4-fold difference, log10 SD 0.30', 'n per arm for 80% power', 6),
 ('Maximum weight loss, 4-point difference, SD 3.7 points', 'n per arm for 80% power', 15), ('Maximum weight loss, 5-point difference, SD 3.7 points', 'n per arm for 80% power', 10),
 ('Zero events in n=49: one-sided 95% upper bound on event rate', 'percent', 6), ('Zero events in n=7', 'percent', 35), ('Zero events in n=5', 'percent', 45)], columns=['Scenario','Quantity','Value'])
sheets.append(('Power', pw))
with pd.ExcelWriter(out, engine='xlsxwriter') as xw:
    wb = xw.book
    hdr = wb.add_format({'bold': True, 'bg_color': '#1F5FA8', 'font_color': 'white', 'text_wrap': True, 'valign': 'top', 'border': 1})
    wrap = wb.add_format({'text_wrap': True, 'valign': 'top'})
    for name, df in sheets:
        df.to_excel(xw, sheet_name=name, index=False)
        ws = xw.sheets[name]
        for j, col in enumerate(df.columns):
            ws.write(0, j, col, hdr)
            mx = max([len(str(col))] + [len(str(v)) for v in df[col].head(300)])
            w = min(max(10, mx + 2), 70 if name in ('README','Evidence_index','Integrity_register') else 42)
            ws.set_column(j, j, w, wrap if (name in ('README','Evidence_index','Integrity_register')) else None)
        ws.freeze_panes(1, 1 if name not in ('README',) else 0)
        if len(df) > 0: ws.autofilter(0, 0, len(df), len(df.columns)-1)
print('written', out)
