# PSLN-344 portfolio review: what is in this folder

| File | What it is |
|---|---|
| `PSLN-344_portfolio_proposal.pdf` | The proposal for the committee. Recommendation on page 1; then evidence, what we give up, next studies with endpoints and stop rules, target demographic, mechanism, biomarkers, what was considered and ruled out, data-quality register, limits. Appendices: evidence ledger, survival by experiment, methods. |
| `PSLN-344_portfolio_proposal.md` | The same text in Markdown, for editing. |
| `PSLN-344_evidence_ledger.xlsx` | Sheet `Ledger`: every `[L..]` / `[Q..]` reference in the proposal, with the statement, the workbook cells it is computed from, and the analysis output and method. Other sheets: the full result tables behind the proposal (survival, immunology, time-courses, safety, dose-response, power, and the data-quality audits). |
| `figures/` | The six figures in the proposal, plus `supp_onset_and_durability.png`. |
| `analysis/` | Scripts, intermediate tables and logs. `run_all.sh` rebuilds everything from the two source files. |

## How to check a number

1. Find its reference in the proposal, for example `[L10]`.
2. Open the `Ledger` sheet (or Appendix A). The row gives the cells in `psln_program_dataset.xlsx` (`sheet!range`) and the analysis file that produced the value.
3. `analysis/build_ledger.py` recomputes each ledger value directly from those cells and stops if it disagrees with the analysis output.

## How the analysis is organised

- `psln_blocks.py` declares every data block of the workbook with explicit cell ranges and checks that every non-empty cell is accounted for. Output: `tidy_all_observations.csv`, 6,120 observations, one row each with its cell address.
- `audit_01` to `audit_05` check the file against itself: stated n against rows present; survival tables against the body-weight tables for the same animals; repeated values; derived blocks against their sources; and a screen of group order in every block that has aged and young comparators.
- `analysis_01` to `analysis_08` produce the results: survival (exact tests, pooled analyses), single-time-point immunology, time-courses, tolerability, post-challenge weight, dose-response, sensitivity / biomarker separation / sample sizes, and the age-by-manganese interaction.
- `verify_in_R.R` recomputes a sample of the statistics (log-rank, Cochran-Mantel-Haenszel, exact intervals, Fisher, Welch, ANOVA interaction, Tukey) in R as an independent check; its output is in `logs/verify_in_R.log` and matches the Python results.
- `build_ledger.py` and `build_report.py` assemble the ledger, the proposal and the evidence workbook. `report_content.py` holds the proposal text; every number in it is read from the ledger.

## Conventions used

- "Aged" = 20 months or older; "young" = 7 to 8 weeks; "Sham" = vaccine with empty liposome.
- Experiment E05 (block S06-C) is excluded from all pooled figures because its survival table is identical to E06 (S06-D).
- qPCR fold-changes and antibody titres are summarised as geometric means; flow-cytometry percentages as arithmetic means.
- Body-weight tables are decoded so that animals that have left a study (blank cells, or a constant value carried forward) are not averaged as if alive.
- Statements labelled "outside our data" in the proposal are general knowledge, not derived from the two files, and were not verified here.
