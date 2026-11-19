#!/usr/bin/env bash
# Rebuilds every table, figure and document from the workbook.  Usage:  bash run_all.sh
# Needs the micromamba environments "chem" (openpyxl, markdown) and "core" (pandas, scipy, statsmodels, lifelines, matplotlib, PySide6).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p parsed tables logs build ../figures
micromamba run -n chem python 01_parse_workbook.py          # workbook  -> parsed/*.csv (every numeric cell accounted for)
micromamba run -n core python 02_block_inventory.py > logs/log_02_inventory.txt
micromamba run -n core python 03_integrity_checks.py > logs/log_03_integrity.txt
micromamba run -n core python 04_survival.py > logs/log_04_survival.txt
micromamba run -n core python 05_endpoints.py > logs/log_05_endpoints.txt
micromamba run -n core python 05b_curated_restoration.py > logs/log_05b_restoration.txt
micromamba run -n core python 06_safety_dose.py > logs/log_06_safety_dose.txt
micromamba run -n core python 06b_morbidity_young.py > logs/log_06b_morbidity_young.txt
micromamba run -n core python 07_power.py > logs/log_07_power.txt
micromamba run -n core python 08_figures.py
micromamba run -n core python 09_moa_figure.py
micromamba run -n core python 10_numbers.py > logs/log_10_numbers.txt   # register of every number quoted in the proposal
micromamba run -n core python 11_build_proposal.py           # proposal_template.md + register -> ../PSLN-344_portfolio_proposal.md
micromamba run -n chem python 12_independent_check.py | tee logs/log_12_independent_check.txt   # headline numbers re-derived straight from workbook cells
micromamba run -n chem python 13_build_html.py               # -> ../PSLN-344_portfolio_proposal.html
micromamba run -n core python 14_build_pdf.py                # -> ../PSLN-344_portfolio_proposal.pdf (+ build/preview/page_XX.png)
