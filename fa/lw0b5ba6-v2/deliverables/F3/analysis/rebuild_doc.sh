#!/usr/bin/env bash
# Fast path: re-render the proposal and the evidence workbook after a text-only change (no statistics are recomputed).
set -euo pipefail
cd "$(dirname "$0")"
micromamba run -n core python build_report.py
python3 make_reference_docx.py > /dev/null
SOURCE_DATE_EPOCH=1793534400 micromamba run -n renv pandoc proposal.md -f markdown -t docx --reference-doc=/tmp/work/docx/reference.docx --columns=120 -o /tmp/work/docx/proposal_raw.docx
python3 postprocess_docx.py /tmp/work/docx/proposal_raw.docx /tmp/outputs/PSLN_portfolio_proposal.docx
micromamba run -n chem python 16_evidence_workbook.py
