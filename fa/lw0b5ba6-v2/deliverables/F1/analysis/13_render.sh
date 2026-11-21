#!/usr/bin/env bash
# Render the proposal (Markdown -> Word and self-contained HTML).  Needs pandoc (conda env "genomics").
set -euo pipefail
cd "$(dirname "$0")/.."
PANDOC="micromamba run -n genomics pandoc"
$PANDOC PSLN_portfolio_proposal.md -f markdown+pipe_tables+implicit_figures --reference-doc=analysis/reference.docx --resource-path=. -o PSLN_portfolio_proposal.docx
micromamba run -n core python analysis/13b_fix_docx_tables.py PSLN_portfolio_proposal.docx
$PANDOC PSLN_portfolio_proposal.md -f markdown+pipe_tables+implicit_figures -s --embed-resources --resource-path=. -c analysis/proposal.css \
        --metadata pagetitle="PSLN program: portfolio recommendation" -o PSLN_portfolio_proposal.html
# PDF: printed from the HTML by the headless Chromium bundled with kaleido 0.2.1 (see analysis/pdf/make_pdf.py)
micromamba run -n genomics python analysis/pdf/make_pdf.py PSLN_portfolio_proposal.html PSLN_portfolio_proposal.pdf 2>&1 | grep -v "deprecated\|upgrade Kaleido" > analysis/pdf/pdf_page_report.txt || true
head -1 analysis/pdf/pdf_page_report.txt
echo rendered
