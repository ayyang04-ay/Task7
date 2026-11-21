#!/bin/bash
# Regenerates every table, figure, number and document from the source workbook.
# Usage: PSLN_XLSX=/path/to/psln_program_dataset.xlsx PSLN_OUT=/path/to/output bash run_all.sh
# Needs Python 3.11 with pandas, scipy, statsmodels, matplotlib, openpyxl, reportlab (here: micromamba env "chem") and R with survival (env "renv").
set -e
cd "$(dirname "$0")"
PY="micromamba run -n chem python"
$PY desc.py > /dev/null
$PY desc_time.py > /dev/null
$PY stats_key_contrasts.py > /dev/null
$PY stats_survival.py > /dev/null
$PY stats_pooled_survival.py > /dev/null
$PY stats_timecourse.py > /dev/null
$PY dose_response.py > /dev/null
$PY safety_bw.py > /dev/null
$PY bw_challenge.py > /dev/null
$PY restoration.py > /dev/null
$PY qc_tte_vs_bw.py > /dev/null
$PY qc_duplicate_traces.py > /dev/null
$PY qc_log.py > qc_log_output.txt
$PY qc_derived.py > qc_derived_output.txt              # IgG2a/IgG1 and Tfh:Tfr recomputation, S01-B vs S08-C
$PY qc_s09a.py > qc_s09a_output.txt                    # S09-A panels vs S01-A (16 h / 72 h)
$PY qc_tte_dups.py > qc_tte_dups_output.txt            # identical survival columns
$PY qc_neardups.py > qc_neardups_output.txt            # near-duplicate blocks (S11-A vs S11-B)
$PY export_tte.py
micromamba run -n renv Rscript check_lr.R            # cross-check of log-rank / Cox results
$PY ledger_numbers.py
$PY verify_ledger.py                                   # re-derives simple ledger entries straight from the quoted cell ranges
for f in fig1_survival fig2_restoration fig3_moa fig4_safety fig5_pd fig6_gantt; do $PY $f.py; done
$PY build_report.py
$PY build_workbook.py
