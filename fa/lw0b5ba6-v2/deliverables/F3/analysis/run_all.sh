#!/usr/bin/env bash
# Regenerates every table, figure and the proposal from the two source files.
# Environments: 'chem' (openpyxl, xlsxwriter), 'core' (scipy, matplotlib), 'renv' (pandoc).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p /tmp/work/parsed /tmp/work/docx /tmp/outputs/figures
C="micromamba run -n chem python"; K="micromamba run -n core python"
$C 01_parse_workbook.py
$C 02_n_audit.py            > /tmp/work/parsed/log_02_n_audit.txt
$C 03_weight_vs_survival.py > /tmp/work/parsed/log_03_weight_vs_survival.txt
$C 04_duplicate_scan.py     > /tmp/work/parsed/log_04_duplicate_scan.txt
$C 04b_weight_trajectory_dups.py > /tmp/work/parsed/log_04b_weight_trajectory_dups.txt
$C 05_derived_value_checks.py    > /tmp/work/parsed/log_05_derived_value_checks.txt
$K 06_survival.py           > /tmp/work/parsed/log_06_survival.txt
$K 07_immunogenicity_moa.py > /tmp/work/parsed/log_07_immunogenicity_moa.txt
$K 08_safety_tolerability.py > /tmp/work/parsed/log_08_safety_tolerability.txt
$K 09_biomarkers_power.py   > /tmp/work/parsed/log_09_biomarkers_power.txt
for f in 10_fig1_survival.py 11_fig2_serology.py 12_fig3_restoration.py 13_fig4_moa.py 14_fig5_tolerability.py 15_fig6_timeline.py; do $K $f > /dev/null; done
$K build_report.py
micromamba run -n renv pandoc -o /tmp/work/docx/ref_default.docx --print-default-data-file reference.docx
python3 make_reference_docx.py
SOURCE_DATE_EPOCH=1793534400 micromamba run -n renv pandoc proposal.md -f markdown -t docx --reference-doc=/tmp/work/docx/reference.docx --columns=120 -o /tmp/work/docx/proposal_raw.docx
python3 postprocess_docx.py /tmp/work/docx/proposal_raw.docx /tmp/outputs/PSLN_portfolio_proposal.docx
$C 16_evidence_workbook.py
# independent cross-check of headline statistics in R
$K - <<'PY'
import json, csv
B = json.load(open('/tmp/work/parsed/parsed_blocks.json'))
ids = ['S03-I', 'S03-J', 'S06-A', 'S06-B', 'S06-C', 'S06-D', 'S06-E_r34', 'S06-F_r34', 'S06-G', 'S15-L', 'S15-N']
with open('/tmp/work/surv_long.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['block', 'group', 'day', 'event'])
    for b in ids:
        for g, a in B[b]['groups'].items():
            for x in a: w.writerow([b, g, x['day'] if x['day'] is not None else 21, x['event']])
PY
micromamba run -n renv Rscript crosscheck_in_R.R > /tmp/work/parsed/log_crosscheck_in_R.txt
$C spotcheck_direct_cells.py > /tmp/work/parsed/log_spotcheck_direct_cells.txt
mkdir -p logs && cp /tmp/work/parsed/log_*.txt logs/
echo "done"
