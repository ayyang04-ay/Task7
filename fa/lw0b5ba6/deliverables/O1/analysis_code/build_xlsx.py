import pandas as pd, numpy as np
W = '/tmp/work/'
sheets = [
 ('README', None),
 ('Evidence_register', 'evidence_register.csv'),
 ('Integrity_register', 'integrity_register.csv'),
 ('Evidence_tiers', 'evidence_tiers.csv'),
 ('Survival_by_group', 'surv_summary.csv'),
 ('Survival_experiments', 'surv_meta.csv'),
 ('Survival_contrasts', 'surv_contrasts.csv'),
 ('Survival_pooled', 'surv_pooled.csv'),
 ('Group_summaries', 'summary_stats.csv'),
 ('Key_contrasts', 'contrasts.csv'),
 ('Tukey_HSD', 'tukey.csv'),
 ('Restoration_index', 'restoration_index.csv'),
 ('Hedges_g', 'hedges_g.csv'),
 ('Dose_response_S08A', 'dose_response.csv'),
 ('Reactogenicity_S08D', 'reactogenicity.csv'),
 ('TwoWay_ANOVA', 'twoway_anova.csv'),
 ('n_check', 'n_check.csv'),
 ('Weight_copy_significant', 'weight_copy_sig.csv'),
 ('Weight_copy_all_pairs', 'weight_copy_all.csv'),
 ('NonWeight_copy_tests', 'nonweight_copy.csv'),
 ('Fingerprints_weights', 'fingerprints.csv'),
 ('Surv_weight_concordance', 'surv_weight_concordance.csv'),
 ('Header_checks', 'header_checks.csv'),
 ('Tidy_data', 'tidy.csv'),
]
readme = pd.DataFrame({'Sheet':[s for s,_ in sheets], 'Contents':[
 'This sheet',
 'E1-E56: every number used in the proposal, with blocks, workbook cells, method and evidence tier',
 'I-01-I-23: data-integrity findings with cell-level evidence and decision impact',
 'Evidence tier (A usable / B caveat / C excluded / D derived) for all 108 blocks, with register reference',
 'Per experiment x group: n, deaths, survival %, Wilson 95% CI, KM median, cell range',
 'Experiment descriptors (animals, vaccine, challenge, timing, flags) from the annotation',
 'Pairwise log-rank and Fisher exact tests per experiment',
 'Pooled analyses: Mantel-Haenszel risk difference, CMH test, stratified log-rank (all 9 aged four-arm experiments; Tier-A-only sensitivity; by timing; other strains)',
 'Per block x group (x time/analyte): n, mean, SD, median, geometric mean (log-scale blocks) with 95% CI, cell range',
 'Key pairwise contrasts per block: effect (ratio of geometric means or difference), Welch p, Mann-Whitney p, Holm-adjusted p within block',
 'One-way ANOVA + Tukey HSD per block (stated method), on analysis scale',
 'Restoration index (aged PSLN-344 vs aged PSLN-212 relative to young PSLN-212) with bootstrap 95% CI',
 "Hedges' g, PSLN-344 vs PSLN-212 (aged), Tier A/B readouts",
 'Emax fit to S08-A Ifnb1 dose-response',
 'Per-animal weight nadir after vaccination (no challenge), S08-D',
 'Two-way ANOVA (group x time) for time-course blocks',
 'Stated n vs observed n per block and group',
 'Body-weight block-group pairs with same-animal duplication beyond chance (Bonferroni)',
 'All body-weight block-group pair tests (exact and integer-shift matches)',
 'Non-weight block pairs: same-position matches vs chance',
 'High-precision fractional-part fingerprints shared across block-groups',
 'Survival block vs paired body-weight block: n and death counts',
 '535 automated checks that every group label in the parser matches the workbook header cell',
 'All 6,120 parsed values with block, group, age, time, event, measurand, unit and exact workbook cell',
]})
with pd.ExcelWriter('/tmp/outputs/PSLN_evidence_workbook.xlsx', engine='xlsxwriter') as xw:
    wb = xw.book
    hdr = wb.add_format({'bold':True,'bg_color':'#0b2e59','font_color':'white','text_wrap':True,'valign':'top','border':1})
    wrap = wb.add_format({'text_wrap':True,'valign':'top'})
    for name, f in sheets:
        df = readme if f is None else pd.read_csv(W+f)
        df.to_excel(xw, sheet_name=name, index=False)
        ws = xw.sheets[name]
        for j,col in enumerate(df.columns):
            ws.write(0, j, col, hdr)
            q = df[col].astype(str).str.len().quantile(0.9) if len(df) else 10
            q = 10 if pd.isna(q) else int(q)
            width = min(60, max(10, q, len(str(col))+2))
            ws.set_column(j, j, width, wrap if width>=40 else None)
        ws.freeze_panes(1, 0)
        if len(df): ws.autofilter(0, 0, len(df), len(df.columns)-1)
print('xlsx written')
