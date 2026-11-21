# PSLN program review: what is in this folder

Start with **`PSLN_portfolio_proposal.pdf`**. The same document is provided as `.docx` (for editing), as a self-contained `.html`, and as `.md` source.
Section 1 is the recommendation and stands alone; sections 2–10 are the supporting case.

| Path | What it is |
|---|---|
| `PSLN_portfolio_proposal.pdf` / `.docx` / `.html` / `.md` | The proposal: recommendation, evidence, what we give up, mechanism, biomarkers, target demographic, next studies, options ruled out, data-integrity findings |
| `tables/T0_evidence_ledger.csv` | Every number quoted in the proposal, with workbook block, cell range, method and producing script (`used_in_proposal = True`) |
| `tables/PSLN_supporting_analysis.xlsx` | All supporting tables (T1–T13, QC log and QC checks, block index) in one workbook |
| `tables/QC_log.csv` | The 15 data-integrity items with full wording and the action needed from the data owners |
| `figures/` | Figures 1–8 as used in the proposal, drawn at printed size |
| `data_tidy/` | The workbook re-exported as one tidy table (6,107 observations) plus an index of blocks with stated and observed group sizes |
| `analysis/` | Scripts. `run_all.sh` regenerates every table, figure, number and the proposal from the workbook |

## How the numbers are tied to the data

1. `analysis/psln_blocks.py` maps each block of `psln_program_dataset.xlsx` to explicit cell ranges; `00_coverage_check.py` confirms that every numeric cell is accounted for (26 cells in an unlabelled region of sheet S08 are excluded).
2. Statistics follow the methods stated in the annotation (ANOVA with Tukey's test, Student's t, log-rank), with exact tests added for the small survival groups. Log-rank results were reproduced in R.
3. `10_numbers.py` computes every number that appears in the text and writes it to the evidence ledger; `11_build_proposal.py` fills the text from that ledger and fails if a number is missing.
4. `15_independent_spotcheck.py` recomputes 36 headline numbers directly from workbook cell addresses, bypassing the pipeline; all 36 agree.

## Limits

- The workbook and its annotation are the only sources. No external data were used for any number.
- Group labels were kept as printed. Where blocks contradict each other (section 10 of the proposal) both readings are reported and the affected blocks are kept out of the headline figures.
- Study designs, gate criteria, timings and animal numbers in section 8 are planning proposals, not results. No cost data were available, so no budget is given.
- The `.html` and the `.pdf` were rendered with a headless Chromium. `analysis/pdf/pdf_page_report.txt` lists what landed on each PDF page, and the rendered layout was inspected on screen for the opening page, every figure and a sample of the tables. The `.docx` comes from the same source through pandoc, with explicit table widths, but could not be opened in Word in this environment; check its layout once before circulating.
