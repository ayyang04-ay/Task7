# PSLN portfolio analysis: reproducible code

Input files (read-only): `/tmp/world/filesystem/psln_program_dataset.xlsx` and `psln_program_annotation.pdf`.
Intermediate files are written to `/tmp/work/`; deliverables go to `/tmp/outputs/`.
Environments: `chem` (openpyxl, xlsxwriter) and `core` (pandas, scipy, statsmodels, lifelines, matplotlib, reportlab).
Run each script with `micromamba run -n <env> python <script>`.

| Step | Script | Env | Purpose |
|---|---|---|---|
| 1 | parse.py | chem | Explicit cell-range map of all 108 blocks. Checks 535 header labels. Writes tidy.csv (6,120 values, each with its cell address) |
| 2 | coverage.py, coverage2.py | chem | Confirms every numeric cell is parsed data or a day/dose axis |
| 3 | integ_n.py | core | Stated vs observed n |
| 4 | integ_dup.py, integ_fp.py | core | Exact-duplicate scan; high-precision fractional fingerprints |
| 5 | integ_pos2.py | core | Body-weight positional concordance: exact and integer-shift matches vs chance (binomial, Bonferroni) |
| 6 | integ_pos3.py | core | Non-weight positional concordance (e.g. S11-A vs S11-B) |
| 7 | integ_surv.py, integ_mc.py | core | Identical survival vectors; Monte Carlo chance probability |
| 8 | integ_derived.py | core | Recomputes S03-B/F from S13 titres; S04-B Tfh:Tfr arithmetic |
| 9 | integ_sw.py | core | Survival vs paired body-weight concordance |
| 10 | integ_s09.py | core | S09-A panels vs S01-A 16 h / 72 h |
| 11 | survival.py | core | KM, log-rank, Fisher, pooled MH risk difference, CMH, stratified log-rank |
| 12 | moa_stats.py | core | Group summaries, Welch/Mann-Whitney/Holm, ANOVA + Tukey, restoration index |
| 13 | misc_stats.py | core | Emax dose-response, two-way ANOVA, reactogenicity |
| 14 | extra_stats.py | core | Hedges g, bootstrap CIs for risk differences, durability, power simulation |
| 15 | register.py | core | Integrity register (I-01..I-23) and evidence tiers |
| 16 | evidence.py | core | Evidence register (E1..E56), built directly from the analysis outputs |
| 17 | figures.py, fig7.py | core | Figures 1-7 |
| 18 | build_xlsx.py | chem | Evidence workbook |
| 19 | content.py + build_report.py | core | Proposal PDF and Markdown |
| 20 | spotcheck.py | chem | Independent re-computation of key numbers directly from the raw workbook |

Random seeds are fixed (bootstrap: 20261101; power and risk-difference bootstrap: 7; Monte Carlo: 1).
