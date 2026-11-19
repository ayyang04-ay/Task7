#!/usr/bin/env bash
# Reproduces every table, figure and the PDF from the two source files.
# Requires the micromamba envs 'singlecell' (pandas/openpyxl/scipy/statsmodels) and 'core' (lifelines/matplotlib/reportlab).
# Scripts read /tmp/world/filesystem/psln_program_dataset.xlsx and write intermediates to /tmp/work, outputs to /tmp/outputs.
set -euo pipefail
mkdir -p /tmp/work /tmp/outputs/figures
cp "$(dirname "$0")"/*.py /tmp/work/
cd /tmp/work
S="micromamba run -n singlecell python"; C="micromamba run -n core python"
$S parse_blocks.py                 # tidy.csv, survival.csv, bodyweight.csv (every value with its source cell)
$S audit_dups.py  > audit_dups.log  # cross-block duplicate screens
$S audit_s11.py   > audit_s11.log   # S11-A vs S11-B position-matched identity
$S audit_bw.py    > audit_bw.log    # body-weight value reuse
$S audit_concord.py > audit_concord.log   # survival vs body-weight concordance -> concordance.csv
$S audit_labels.py  > audit_labels.log    # S03-B/F rotation, Tfh:Tfr derivation, S09-A timepoint
$S analysis_continuous.py > continuous.log  # continuous_results.csv
$S analysis_mech.py > mech.log; $S save_mech.py   # mech_results.csv
$S analysis_surv.py > surv.log                    # surv_summary.csv, surv_pairwise.csv
$C xcheck_lifelines.py                            # verifies log-rank against lifelines
$S analysis_pooled.py > pooled.log                # pooled_survival.csv
$S analysis_time.py > time.log
$S robustness.py > robustness.log
$S save_bwdup.py; $S findings_register.py > /dev/null
$C fig_effects.py > /dev/null; $C fig2_fix.py > /dev/null; $C fig_surv.py; $C fig_integrity.py; $C fig_moa.py; $C fig_safety.py
$S claims_index.py > claims.log
$S build_workbook.py
$C render_pdf.py
echo "done"
