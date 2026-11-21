#!/usr/bin/env bash
# Reproduce every table and figure from the raw workbook. Usage: bash run_all.sh
set -euo pipefail
cd "$(dirname "$0")"
L=logs; mkdir -p $L tidy snippets
mm() { micromamba run -n "$@"; }
echo "[1] extract blocks with cell provenance";        mm singlecell python parse.py        > $L/01_parse.log
echo "[2] integrity checks";                           mm singlecell python audit.py        > $L/02_audit.log
mm singlecell python fingerprint.py  > $L/02b_fingerprint.log
mm singlecell python bw_recycle.py   > $L/02c_bw_recycle.log
mm singlecell python tte_bw_check.py > $L/02d_tte_bw.log
mm singlecell python crosscheck.py   > $L/02e_crosscheck.log
mm singlecell python fp_breakdown.py > $L/02f_fp_breakdown.log
mm singlecell python qa_independent.py > $L/02g_qa_independent.log
echo "[3] head-to-head statistics";                    mm core python h2h.py                > $L/03_h2h.log 2>&1
echo "[4] survival";                                   mm core python survival.py           > $L/04_survival.log
mm core python newcombe.py > $L/04b_newcombe.log
mm renv Rscript strat.R    > $L/04c_strat_R.log
echo "[5] MoA, restoration, biomarkers, power";        mm core python moa.py > $L/05_moa.log
mm core python restoration.py  > $L/05b_restoration.log
mm core python biomarkers.py   > $L/05c_biomarkers.log
mm core python power.py        > $L/05d_power.log
mm core python extra_checks.py > $L/05e_extra.log
echo "[6] integrity register + tables";                mm core python integrity_register.py > $L/06_register.log
mm core python build_tables.py > $L/06b_tables.log
mm core python facts.py > $L/06c_facts.log
echo "[7] figures";                                    mm core python figures.py > $L/07_figs.log
mm core python fig5.py >> $L/07_figs.log

echo "[8] render proposal + package";                  mm core python render.py
mm genomics pandoc /tmp/outputs/PSLN_portfolio_proposal.md -o /tmp/outputs/PSLN_portfolio_proposal.docx --toc --toc-depth=2 --resource-path=/tmp/outputs
mm genomics pandoc /tmp/outputs/PSLN_portfolio_proposal.md -o /tmp/outputs/PSLN_portfolio_proposal.html --standalone --embed-resources --toc --toc-depth=2 --css=style.css --resource-path=/tmp/outputs
echo "all done"
