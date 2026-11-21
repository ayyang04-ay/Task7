#!/usr/bin/env bash
# Re-runs the whole analysis from the source workbook.
#   PSLN_XLSX  path to psln_program_dataset.xlsx   (default: /tmp/world/filesystem/psln_program_dataset.xlsx)
#   PSLN_OUT   where figures/ and PSLN_analysis_tables.xlsx are written (default: /tmp/outputs)
#   PY_STATS   python with pandas, numpy, scipy, statsmodels, lifelines, matplotlib   (default: micromamba env "core")
#   PY_XL      python with pandas, openpyxl, xlsxwriter                                (default: micromamba env "chem")
set -e
cd "$(dirname "$0")"
PY_STATS=${PY_STATS:-"micromamba run -n core python"}
PY_XL=${PY_XL:-"micromamba run -n chem python"}
$PY_XL parse_blocks.py > parse_log.txt            # workbook -> quant_long.csv, surv_long.csv, wt_long.csv (every value keeps its cell address)
$PY_STATS stats_quant.py > /dev/null              # descriptives, ANOVA + Tukey, Welch, Mann-Whitney
$PY_STATS scorecard.py > scorecard_print.txt
$PY_STATS stats_surv.py > surv_print.txt          # Kaplan-Meier, log-rank, Fisher per block
$PY_STATS wt_status.py > /dev/null 2>&1           # survival implied by body-weight records
$PY_STATS pooled_surv.py > pooled_print.txt 2>&1  # pooled and stratified analyses; table-vs-weights concordance
$PY_XL audit_n.py > audit_n_print.txt             # stated n vs rows present
$PY_XL audit_dups.py > audit_dups_print.txt       # repeated values across blocks
$PY_XL audit_derived.py > audit_derived_print.txt # derived quantities vs raw inputs (IgG2a:IgG1, S09-A vs S01-A, ...)
$PY_STATS stats_misc.py > stats_misc_print.txt    # S10-A, S08-D, two-way ANOVA for time courses
$PY_STATS dose_response.py > dose_print.txt
$PY_STATS morbidity.py > morbidity_print.txt
$PY_STATS biomarkers.py > biomarkers_print.txt
$PY_STATS power.py > power_print.txt
$PY_STATS integrity_register.py > /dev/null
$PY_STATS evidence_index.py > /dev/null
for f in fig1_survival fig2_km fig3_restoration fig4_dose_safety fig5_moa fig6_integrity fig7_timeline; do $PY_STATS $f.py > /dev/null; done
$PY_XL build_xlsx.py
echo ALL_OK
