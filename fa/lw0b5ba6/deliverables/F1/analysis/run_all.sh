#!/usr/bin/env bash
# Rebuilds every table, figure and document from psln_program_dataset.xlsx.
# Usage:  bash run_all.sh            (from the analysis folder)
# Needs:  Python >= 3.11 with pandas, numpy, scipy, statsmodels, matplotlib, openpyxl, reportlab, pillow;
#         R with the 'survival' package; pandoc >= 3.
# In the original environment these are the micromamba environments 'chem' (Python), 'renv' (R) and 'genomics' (pandoc).
set -euo pipefail
cd "$(dirname "$0")"
PY=${PY:-"micromamba run -n chem python"}
RS=${RS:-"micromamba run -n renv Rscript"}

$PY psln_blocks.py            # T0  every observation with its cell reference; coverage check of all numeric cells
$PY a01_counts.py > /dev/null # T1  observation counts per block and group
$PY a02_surv_vs_weight.py > /dev/null   # T2  survival tables vs weight-implied deaths
$PY a03_duplicates.py > /dev/null       # T3  identical vectors / identical survival tables
$PY a03c_trace_reuse.py > /dev/null     # T3c re-used body-weight traces
$PY a04_crosschecks.py > /dev/null      # T4  recomputation checks between linked blocks
$PY a05_survival.py > /dev/null         # T5, T6  survival per experiment, log-rank and Fisher tests
$PY a06_survival_pooled.py > /dev/null  # T7, T8  pooled and stratified survival, durability, background mortality
$RS a06c_cox.R                          # T7b stratified Cox model; T6b check of the log-rank code against R
$PY a07_point_stats.py > /dev/null      # T9, T10 group summaries and pairwise contrasts
$PY a08_restoration.py > /dev/null      # T11 restoration index and biomarker separation
$PY a09_weights.py > /dev/null          # T12, T13 body-weight analyses
$PY a10_dose_response.py > /dev/null    # T14 dose-response fit
$PY a11_timecourse_anova.py > /dev/null # T15 two-way ANOVA of time courses
$PY a12_power.py > /dev/null            # T16 power and sample size
$PY figures.py                          # figures 1-9
$PY make_reference.py                   # Word styles
$PY build_report.py                     # evidence tags, generated tables, Word document; T17, T18
$PY build_pdf.py                        # PDF copy of the proposal
$PY build_workbook.py                   # evidence workbook
rm -rf __pycache__ build/default-reference.docx
echo "done"
