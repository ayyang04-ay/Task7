#!/usr/bin/env bash
# Reproduce every table, figure and document from the two source files.
# Requires the micromamba envs present on the analysis machine: chem (openpyxl/xlsxwriter), core (lifelines/statsmodels/reportlab), genomics (pandoc/pypdf).
# Source files expected at /tmp/world/filesystem/; intermediate files go to /tmp/work/{tidy,tables}; deliverables to /tmp/outputs.
set -euo pipefail
CODE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p /tmp/work/tidy /tmp/work/tables /tmp/outputs/figures /tmp/work/code
cp "$CODE"/*.py /tmp/work/code/
cd /tmp/work
mm() { micromamba run -n "$@"; }
mm chem python code/01_extract.py                 # A1 tidy extraction with cell addresses
mm chem python code/02_qc_scan.py > tables/qc_scan_output.txt
mm chem python code/03_bw_trajectory_scan.py > tables/bw_trajectory_scan_output.txt
mm chem python code/03b_bw_live_scan.py > tables/bw_live_scan_output.txt
mm core python code/04_issue_log.py               # integrity log
mm core python code/05_continuous_stats.py        # A2, A3
mm core python code/06_survival.py                # A4, A5
mm core python code/07_mechanism_safety_dose.py   # A6, A7, A8
mm core python code/08_gap_power.py               # A3 curated, A11
mm core python code/09_bodyweight.py              # A9
mm core python code/10_biomarkers.py              # A10
mm core python code/13_extra_contrasts.py         # A12
mm core python code/11_figures.py                 # Figs 1-5, 7
mm core python code/12_fig_moa_integrity.py       # Figs 6, 8
mm core python - << 'PY'                          # Holm multiplicity table (A2/A3)
import pandas as pd
from statsmodels.stats.multitest import multipletests
G=pd.read_csv('tables/age_gap_curated.csv'); G['time']=G['time'].astype(str)
K=pd.read_csv('tables/continuous_contrasts.csv'); K['time']=K['time'].astype(str)
rows=[]
for _,g in G.iterrows():
    k=K[(K.block==g.block)&(K.time==g.time)&(K.contrast=='PSLN-344 vs PSLN-212')]
    if g.block=='S04-A': k=k[k.measurand.str.contains('ICOS-high')]
    if g.block.startswith('S09-A'): k=k[k.measurand.str.contains(g.readout.split()[1])]
    k=k.iloc[0]; rows.append(dict(readout=g.readout,block=g.block,welch_p=k.welch_p,tukey_p=k.tukey_p,mw_p=k.mw_p))
R=pd.DataFrame(rows)
for c in ['welch_p','tukey_p']: R[c+'_holm']=multipletests(R[c].fillna(1),method='holm')[1]
R.to_csv('tables/multiplicity_holm.csv',index=False)
PY
mm core python code/14_content.py                 # PDF + Markdown
micromamba run -n genomics pandoc /tmp/outputs/PSLN_portfolio_proposal.md -o /tmp/outputs/PSLN_portfolio_proposal.docx --resource-path=/tmp/outputs
mm chem python code/15_workbook.py                # Excel workbook (evidence register)
mm chem python code/16_independent_check.py       # raw-cell recomputation + alternative Cox
mm core python code/17_text_audit.py              # document-number audit
