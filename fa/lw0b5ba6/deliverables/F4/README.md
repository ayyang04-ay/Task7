# PSLN-344 portfolio review — contents

| File | What it is |
|---|---|
| `PSLN-344_portfolio_proposal.pdf` | The proposal for the committee (13 pages: recommendation, next studies and endpoints, scorecard, target demographic, mechanism, biomarkers, what we give up, what was ruled out, data-integrity log) |
| `PSLN-344_portfolio_proposal.md` / `.html` | Same content in Markdown and as a single self-contained web page |
| `figures/` | The six figures used in the proposal |
| `analysis/run_all.sh` | Rebuilds everything from `psln_program_dataset.xlsx` (scripts `01`–`14`, about 7 minutes) |
| `analysis/parsed/` | Every numeric workbook cell in long format with its cell address |
| `analysis/logs/` | Printed output of each analysis step, including the full data-integrity evidence (`log_03_integrity.txt`) |
| `analysis/tables/` | All analysis tables (`T00`–`T11`); `T10_numbers_cited.csv` maps each number in the proposal to its source block and analysis |
| `analysis/proposal_template.md` | Text of the proposal with placeholders; numbers are filled in by `11_build_proposal.py`, not typed |

## How to check a number

1. Find it in `analysis/tables/T10_numbers_cited.csv` (columns: value, source block, analysis table).
2. Open the named table; `T02` and `T05` carry the workbook cell range for every group.
3. `analysis/12_independent_check.py` re-derives 32 headline numbers directly from workbook cells, without using the parsed files.

## Table index

| Table | Content |
|---|---|
| `T00` | Inventory of every block: groups, observations, stated n |
| `T01a`–`T01h` | Evidence behind each data-integrity finding (Appendix A of the proposal) |
| `T02`, `T03` | Survival by group; pairwise contrasts (log-rank, exact permutation, Fisher) |
| `T04`, `T04b`, `T04c` | Pooled survival (stratified by experiment), day-60 and attrition analyses, worst-case sensitivity |
| `T05`, `T06` | Descriptives and contrasts for every immune, qPCR and formulation block |
| `T07` (two files) | Aged-mouse responses as a percentage of the young benchmark |
| `T08a`–`T08e` | Post-dose body weight, lung cytokines, CNS transcripts, dose-response |
| `T09a`–`T09c` | Post-challenge weight loss in survivors; PSLN-344 vs PSLN-212 in young mice (immune read-outs; post-challenge weight) |
| `T10` | Register of numbers quoted in the proposal |
| `T11` | Sample-size calculations for the proposed replication study |

## Environment

Python via micromamba: `chem` (openpyxl, markdown) and `core` (pandas, scipy, statsmodels, lifelines, matplotlib, PySide6).
