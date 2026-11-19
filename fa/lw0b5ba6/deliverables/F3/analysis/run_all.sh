#!/usr/bin/env bash
# Reproduces every number, table and figure in the proposal from the two source files.
# Environments: "chem" has openpyxl (needed to read the workbook); "core" has lifelines/statsmodels.
# Source files are read from /tmp/world/filesystem; outputs are written to /tmp/outputs.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p logs
run() { env="$1"; shift; echo ">> $*"; micromamba run -n "$env" python "$@" > "logs/$(basename "$1" .py).log" 2>&1; }
run chem psln_blocks.py                                # parse workbook -> tidy_all_observations.csv (+ coverage check)
run chem audit_01_n_and_labels.py                      # stated n vs observed n
run chem audit_02_survival_vs_weight.py                # survival tables vs body-weight tables
run chem audit_03_duplicates.py                        # repeated values across blocks
run chem audit_03d_overlap_detail.py
run chem audit_04_derived_checks.py                    # derived blocks vs their sources
run core analysis_01_survival.py                       # survival, exact tests, pooled analyses
run core analysis_02_immunology.py                     # single-time-point blocks
run core audit_05_group_order_screen.py                # header-plausibility screen (needs analysis_02 output)
run core analysis_03_timecourses.py                    # time-course blocks
run core analysis_04_safety.py                         # tolerability blocks
run chem analysis_05_challenge_morbidity.py            # post-challenge weight, real observations only
run core analysis_06_dose_response.py                  # Emax fits
run core analysis_07_sensitivity_biomarkers_power.py   # sensitivity, biomarker separation, sample sizes
run core analysis_08_age_by_manganese.py               # age x formulation interaction
run core make_figures.py
run core make_moa_figure.py
run chem build_ledger.py                               # recompute every cited number from raw cells; stops on mismatch
run chem build_report.py                               # proposal (md, pdf) and evidence workbook (xlsx)
echo ">> verify_in_R.R"; Rscript verify_in_R.R > logs/verify_in_R.log 2>&1 || echo "   (R not available; skipped)"
echo "done"
