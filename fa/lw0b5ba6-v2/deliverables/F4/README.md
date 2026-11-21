# PSLN program: portfolio review package (analysis dated 1 November 2026)

| File | What it is |
|---|---|
| `PSLN_portfolio_proposal.pdf` | The proposal (21 pages). Page 1 is the recommendation. This is the version whose layout was checked. |
| `PSLN_portfolio_proposal.docx` | The same content, editable. Generated from the same source; its layout was not visually checked in Word. |
| `PSLN_portfolio_proposal.md` | The same content as Markdown (figures referenced from `figures/`). |
| `PSLN_analysis_tables.xlsx` | Supporting tables: evidence index (every headline number with source cells), data-integrity register, survival by block, pooled analyses, all descriptive and pairwise statistics, biomarker table, dose-response fits, duplicate-value scans, power calculations. Start with the `README` sheet. |
| `figures/` | Figures 1 to 6 and A1 as PNG (220 dpi). |
| `analysis_code/` | Python scripts that produce every table and figure from `psln_program_dataset.xlsx`. `run_all.sh` re-runs everything; `verify_citations.py` re-reads the workbook by the cell ranges cited in the proposal and recomputes the numbers (`verify_citations_log.txt` is the last run: all checks passed). `intermediate/` holds the tidy per-animal tables (each value with its cell address) and the printed logs. `report_build/` holds the document source and build scripts (paths inside them are specific to the machine where the document was built). |

## Conventions

- Cell references are `sheet!range` in `psln_program_dataset.xlsx`.
- `E1` to `E30` are entries in the evidence index (Appendix C of the proposal and the `Evidence_index` sheet).
- `DI-01` to `DI-19` are entries in the data-integrity register (Appendix A and the `Integrity_register` sheet).
- The source files are stamped 3 September 2026 (workbook) and 15 September 2026 (annotation).

## Re-running

```
cd analysis_code
PSLN_XLSX=/path/to/psln_program_dataset.xlsx PSLN_OUT=/path/to/output bash run_all.sh
```

Needs Python 3.11 with pandas, numpy, scipy, statsmodels, lifelines, matplotlib, openpyxl and xlsxwriter. Set `PY_STATS` and `PY_XL` to the interpreter(s) to use; the defaults call two conda environments that exist only on the machine where the analysis was run.
