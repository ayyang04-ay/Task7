# Reproducing the analysis

`bash run_all.sh` runs every step in order:

1. extraction;
2. integrity checks;
3. statistics;
4. survival analysis, including the R cross-check;
5. MoA, biomarker and power analyses;
6. tables and evidence ledger;
7. figures;
8. rendering of the MD, DOCX and HTML outputs.

## Paths and environments

**Paths** are fixed at the top of each script:

- input workbook: `/tmp/world/filesystem/psln_program_dataset.xlsx`;
- working directory: `/tmp/work` (scripts and `run_all.sh` must be placed there);
- outputs: `/tmp/outputs`.

Edit these paths to relocate.

**Environments** (micromamba):

- `singlecell`: openpyxl extraction and audit;
- `core`: pandas, scipy, statsmodels, lifelines, matplotlib;
- `renv`: R 4.3 + survival 3.8-3, for the stratified log-rank and Cox cross-check;
- `genomics`: pandoc 3.12.

## Key scripts

| Script | Purpose |
|---|---|
| `parse.py` | Block-by-block extraction with cell provenance; coordinates cross-checked against the annotation PDF |
| `audit.py`, `fingerprint.py`, `fp_breakdown.py`, `bw_recycle.py`, `tte_bw_check.py`, `crosscheck.py`, `extra_checks.py`, `qa_independent.py` | Integrity checks and independent re-derivation of headline numbers |
| `h2h.py` | Head-to-head statistics (log2 for titres/qPCR; Welch + exact MW; BH-FDR; restoration index) |
| `survival.py`, `newcombe.py`, `strat.R` | Per-experiment and pooled survival; sensitivity sets; R cross-check |
| `moa.py`, `restoration.py`, `biomarkers.py`, `power.py` | Interventional MoA contrasts, dose–response, restoration by layer, biomarker table, sample sizes |
| `integrity_register.py`, `build_tables.py`, `facts.py`, `render.py` | Register, tables, evidence ledger; template rendering (fails if any quoted number lacks a ledger entry) |
