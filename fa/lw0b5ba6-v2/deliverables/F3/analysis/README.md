# Analysis behind the PSLN portfolio proposal

Everything in `PSLN_portfolio_proposal.docx`, `PSLN_evidence_tables.xlsx` and `figures/` is regenerated from the two
source files by `run_all.sh`.

Source files (read-only): `/tmp/world/filesystem/psln_program_dataset.xlsx`, `/tmp/world/filesystem/psln_program_annotation.pdf`.
Intermediate files are written to `/tmp/work/parsed`; outputs to `/tmp/outputs`. Paths are set at the top of each script.

| Script | What it does |
|---|---|
| `01_parse_workbook.py` | Reads every block of the workbook into `parsed_blocks.json`, keeping cell addresses. Checks that all 6,819 numeric cells are captured. Labels are taken as printed. |
| `02_n_audit.py` | Stated n against the number of values present, per block and group. |
| `03_weight_vs_survival.py` | Compares each survival table with its paired body-weight table (blank cells and carried-forward values are both treated as end of observation). |
| `04_duplicate_scan.py`, `04b_weight_trajectory_dups.py` | Look for number sequences that recur between blocks or groups. |
| `05_derived_value_checks.py` | Recomputes derived tables from raw tables (IgG2a:IgG1, Tfh:Tfr), checks scales (S09-A log10 vs S01-A linear), compares S01-B with S08-C and S11-A with S11-B. |
| `06_survival.py` | Survival per experiment, pooled and stratified tests, subsets, sensitivity analyses. |
| `07_immunogenicity_moa.py` | Titers (geometric means, ratios), cellular readouts, dose-response, intervention experiments, Holm adjustment. |
| `08_safety_tolerability.py` | Body weight after dosing, lung cytokines, brain transcripts, post-challenge weight in survivors. |
| `09_biomarkers_power.py` | Biomarker separation and gap-closed statistics; sample-size calculations. |
| `10_` to `15_` | Figures 1 to 6. |
| `facts.py` | Registry of every number quoted in the proposal, with source blocks, cells and method. |
| `integrity_log.py` | The 20 discrepancies: evidence, why each matters, handling, audit action. |
| `report_text.py`, `build_report.py` | Text of the proposal with `{{fact}}` placeholders; rendering to `proposal.md`. |
| `make_reference_docx.py`, `postprocess_docx.py` | Word styling and table widths. |
| `16_evidence_workbook.py` | Writes `PSLN_evidence_tables.xlsx`. |
| `spotcheck_direct_cells.py` | Reads headline cells straight from the workbook, without the parser, and prints the quoted summary numbers. |
| `crosscheck_in_R.R` | Recomputes the stratified log-rank statistic, the pooled Fisher test and one titer ratio in R as an independent check. |

`rebuild_doc.sh` re-renders the proposal and the evidence workbook after a text-only change, without recomputing statistics.

`logs/` holds the full printed output of scripts 02 to 09 and of the two cross-checks.

Environments: `chem` (openpyxl, xlsxwriter), `core` (numpy, scipy, matplotlib), `renv` (pandoc).
Random seed for the permutation tests: 20261101 (`06_survival.py`).
