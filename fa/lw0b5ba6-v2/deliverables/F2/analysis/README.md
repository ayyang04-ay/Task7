# PSLN portfolio analysis: scripts and intermediate results

Everything in the proposal (PDF/Markdown), the figures and the evidence workbook is regenerated from the source
workbook by `run_all.sh`. No number in the proposal is typed by hand: the text is assembled in `build_report.py`
from values registered in `ledger_numbers.py`.

    PSLN_XLSX=/path/to/psln_program_dataset.xlsx PSLN_OUT=/path/to/output bash run_all.sh

Runtime is about 7 minutes; the permutation log-rank tests dominate (exact enumeration up to 20,000 arrangements,
otherwise 20,000 seeded random permutations).

Requirements: Python 3.11 with pandas, numpy, scipy, statsmodels, matplotlib, openpyxl, reportlab; R with the
`survival` package (used only as an independent cross-check of the log-rank tests and for the stratified Cox model).
`run_all.sh` calls them through micromamba environments named `chem` and `renv`; edit the two lines at the top
of the script if your environments are named differently.

| Step | Script | What it does | Output |
|---|---|---|---|
| Parse | `blocks.py` | Reads every block of the workbook by explicit cell coordinates into tidy tables (B = single time point, T = time course / dose, S = time to event, W = body weight). Reports how many numeric cells were captured. | (library) |
| Describe | `desc.py`, `desc_time.py` | n, mean, SD, geometric mean per block and group | `desc_*.csv` |
| Contrasts | `statlib.py`, `stats_key_contrasts.py` | Every pairwise contrast in every single-time-point block: Welch test and CI, one-way ANOVA + Tukey, exact Mann-Whitney | `stats_contrasts_all.csv` |
| Time courses | `stats_timecourse.py` | Two-way ANOVA + Tukey, Welch per time point | `stats_timecourse_*.csv` |
| Survival | `stats_survival.py`, `stats_pooled_survival.py`, `export_tte.py`, `check_lr.R` | Per-block survival, log-rank (asymptotic, permutation), Fisher; pooled sets A-F (Mantel-Haenszel, CMH, stratified log-rank); R cross-check and stratified Cox | `stats_survival_*.csv`, `r_logrank_check.csv`, `cox_hr.csv` |
| Dose-response | `dose_response.py` | Hill fits for S08-A | `dose_response_S08A.csv` |
| Tolerability | `safety_bw.py`, `bw_challenge.py` | Weight loss after dosing (S08-D) and after challenge | `safety_S08D_nadir.csv`, `bw_challenge_nadir.csv` |
| Young benchmark | `restoration.py` | Aged PSLN-344 and PSLN-212 as % of young benchmark, block by block | `restoration_index.csv` |
| Data quality | `qc_tte_vs_bw.py`, `qc_duplicate_traces.py`, `qc_tte_dups.py`, `qc_derived.py`, `qc_s09a.py`, `qc_neardups.py`, `qc_log.py` | Survival block vs weight block; recycled weight traces; identical survival columns; derived-quantity checks (IgG2a/IgG1, Tfh:Tfr); S09-A vs S01-A; near-duplicate blocks; the 22-flag log | `qc_*.csv` |
| Ledger | `ledger_numbers.py`, `verify_ledger.py` | Registers every number used in the text with source blocks, cells and method; `verify_ledger.py` re-reads the quoted cell ranges straight from the workbook (without `blocks.py`) and recomputes the simple entries | `evidence_ledger*.csv` |
| Figures | `figstyle.py`, `fig1_survival.py` ... `fig6_gantt.py` | Six figures | `figures/*.png` |
| Documents | `docengine.py`, `build_report.py`, `build_workbook.py` | Proposal (PDF + Markdown) and evidence workbook | `PSLN_portfolio_proposal.*`, `PSLN_evidence_workbook.xlsx` |

Conventions: time-to-event status 1 = death, 0 = alive at end of observation. Titres and fold-change transcripts
are analysed on log10; HAI values of 0 (below the lowest dilution, 1:10) are set to 5. Block names are the
workbook's; the second blocks labelled S06-E / S06-F (rows 69-98) are called S06-E2 / S06-F2, and the two panels
labelled "S09-A 16h" are called left (columns B-V) and right (columns Y-AS; identified as the 72 h time point).
