#!/usr/bin/env bash
# Regenerates every table, figure, number and the proposal itself from the workbook.
# Environments: "chem" (openpyxl), "core" (lifelines, scipy, statsmodels, matplotlib), "renv" (R survival), "genomics" (pandoc).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p ../tables ../figures ../data_tidy
C="micromamba run -n chem python"; K="micromamba run -n core python"
echo "== 1 parse workbook";            $C 00_coverage_check.py; $C 01_export_tidy.py > /dev/null
echo "== 2 data-integrity checks";     $C 02a_qc_derived.py > ../tables/QC_derived_blocks_report.txt; $C 02b_qc_surv_bw.py > /dev/null; $C 02c_qc_duplicates.py > ../tables/QC_duplicates_report.txt
                                       $K 02d_qc_shared_values.py > /dev/null; $K 02e_qc_log.py > /dev/null
echo "== 3 statistics";                $K 03_survival.py > /dev/null; $K 03b_survival_pooled.py > /dev/null
                                       micromamba run -n renv Rscript 03c_survival_crosscheck.R > ../tables/T2b_survival_crosscheck_R.txt
                                       $K 04_immunology_stats.py > /dev/null; $K 04b_restoration.py > /dev/null; $K 04c_biomarker_separation.py > /dev/null
                                       $K 05_dose_response.py > /dev/null; $K 06_safety.py > /dev/null; $K 07_morbidity_and_factorial.py > /dev/null; $K 08_power.py > /dev/null
echo "== 4 figures";                   for f in 09a_fig_survival 09b_fig_restoration 09c_fig_moa 09d_fig_pd_safety 09e_fig_qc 09f_fig_plan; do $K $f.py > /dev/null; done
echo "== 5 evidence ledger + text";    $K 10_numbers.py; $K 11_build_proposal.py
echo "== 6 render";                    micromamba run -n genomics pandoc -o /tmp/_pandoc_default_reference.docx --print-default-data-file reference.docx
                                       $K 12_make_reference_docx.py /tmp/_pandoc_default_reference.docx reference.docx; ./13_render.sh
echo "== 7 workbook + spot-check";     $C 14_supporting_workbook.py; $C 15_independent_spotcheck.py | tail -1
echo "done"
