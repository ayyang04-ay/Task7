#!/usr/bin/env bash
# Reproduce every table, figure and document. Requires the conda envs "chem" (python, pandas, scipy, statsmodels, matplotlib,
# openpyxl, xlsxwriter, reportlab, mpmath) and "genomics" (pandoc). Input files are read from /tmp/world/filesystem.
set -euo pipefail
cd "$(dirname "$0")"
R="micromamba run -n chem python"
mkdir -p /tmp/work/tidy /tmp/outputs/figures
$R parse.py > logs_parse.txt
for s in audit1 audit2 audit3 audit4 audit5 audit_s11 analysis_cont analysis_surv analysis_pool analysis_safety analysis_biomarkers \
         analysis_extra analysis_twoway analysis_mech exp_table integrity_table power figures citation_index build_workbook; do
  echo "== $s"; $R $s.py > logs_$s.txt 2>&1
done
$R build_report.py
echo done
