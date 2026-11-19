#!/usr/bin/env bash
# Regenerates every table, figure and document from the workbook.
# Scripts 04, 05, 08, 09 need lifelines (env `core`); the rest need openpyxl (env `chem`); pandoc comes from env `genomics`.
set -euo pipefail
cd "$(dirname "$0")"
C="micromamba run -n chem python"; K="micromamba run -n core python"
$C 01_extract_blocks.py
$C 02_integrity_checks.py > /dev/null
$C 02b_bodyweight_duplicates.py > integrity/B2_summary.txt
$C 03_continuous_stats.py
$K 04_survival_stats.py > stats/survival_stats_stdout.txt
$K 05_survival_pooled.py > /dev/null
$C 06_bodyweight_stats.py > stats/bodyweight_stats_stdout.txt
$C 07_special_analyses.py > /dev/null
$K 08_sensitivity_power.py > /dev/null
$K 09_fig2_survival.py
$C 10_fig3_restoration.py > /dev/null
$C 11_fig1_moa.py
$C 12_fig4_fig5.py
$C 13_figA1_km.py
$C 14_build_report.py
$C 15_make_docx.py
$C 16_build_xlsx.py
echo "all done"
