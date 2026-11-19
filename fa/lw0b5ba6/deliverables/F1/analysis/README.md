# Analysis behind the PSLN-344 portfolio proposal

Everything in the proposal is computed from `psln_program_dataset.xlsx` by the scripts in this folder.
`bash run_all.sh` rebuilds all tables, figures, the Word and PDF documents and the evidence workbook.
Set `PSLN_XLSX=/path/to/psln_program_dataset.xlsx` if the workbook is not at its original location.

| Script | What it does | Output |
|---|---|---|
| `paths.py` | folder locations | |
| `psln_blocks.py` | hand-checked map of all 102 data blocks to their cell ranges; every number keeps its cell reference | T0 |
| `stats_util.py` | exact confidence intervals, log-rank (asymptotic, exact, stratified), Mantel-Haenszel, Tukey, Welch, exact power | |
| `a01_counts.py` | observations per block and group, as found | T1 |
| `a02_surv_vs_weight.py` | each survival table against the deaths implied by its paired weight block | T2 |
| `a03_duplicates.py`, `a03c_trace_reuse.py` | identical vectors, identical survival tables, re-used weight traces | T3, T3c, T3d, T3e |
| `a04_crosschecks.py` | recomputation checks between linked blocks (ratio blocks, cytokine panels, dye uptake) | T4 |
| `a05_survival.py` | survival per experiment; log-rank and Fisher tests | T5, T6 |
| `a06_survival_pooled.py` | pooled and stratified survival; sensitivity sets; durability; background mortality | T7, T8 |
| `a06c_cox.R` | stratified Cox model; check of the log-rank code against R `survival` | T7b, T6b |
| `a07_point_stats.py` | means, geometric means, ANOVA with Tukey, Welch, exact Mann-Whitney for every read-out | T9, T10 |
| `a08_restoration.py` | restoration index with bootstrap interval; biomarker separation | T11 |
| `a09_weights.py` | lowest body weight per animal; tolerability after dosing | T12, T13 |
| `a10_dose_response.py` | Hill fit of the interferon dose-response | T14 |
| `a11_timecourse_anova.py` | two-way ANOVA of the time-course blocks | T15 |
| `a12_power.py` | exact power and sample sizes for the proposed studies | T16 |
| `evidence.py` | defines every number quoted in the proposal, with its cells and analysis | T18 |
| `defects.py` | register of record defects D1-D16 | T17 |
| `figures.py` | figures 1-9 | `../figures/` |
| `proposal_template.md` | text of the proposal with evidence placeholders | |
| `make_reference.py`, `build_report.py`, `build_pdf.py`, `build_workbook.py` | render the Word document, the PDF and the evidence workbook | `../` |

Conventions
- Group names are used as printed in the workbook. "Sham" (empty liposome with vaccine) is called "vehicle" in the proposal.
- In time-to-event blocks a flag of 1 is read as death and 0 as alive at the end of observation.
- Where the analysis departs from a printed label (defects D4 and D6) the departure is made in the analysis scripts and stated in the proposal, never by editing the data.
- Random seeds are fixed (bootstrap intervals), so results are reproducible.
