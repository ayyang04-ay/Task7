Reproducing the PSLN-344 analyses
=================================
Environment: Python 3.11 with pandas, numpy, scipy, statsmodels, matplotlib, openpyxl, xlsxwriter
(lifelines 0.30.3 only for xval.py, the log-rank cross-check).
Input: /tmp/world/filesystem/psln_program_dataset.xlsx (path is set at the top of parse.py).
Run from one working directory (intermediate CSVs are written there; tables go to /tmp/outputs/analysis):

 1. parse.py        - extracts every block with sheet!cell provenance -> values.csv, survival.csv, bw.csv
 2. ncheck.py       - stated vs observed n (audit A9)
 3. dupscan.py      - whole-block and value-level duplicate scan (A1)
 4. posdup.py       - positional duplication + permutation null, S11-A vs S11-B (A2)
 5. bwforensic.py   - shared high-precision fractional parts in body weights (A3)
 6. concord.py      - survival vs body-weight concordance -> concordance.csv (A4, T13)
 7. survstats.py    - per-experiment survival and pairwise tests (T1, T2)
 8. xval.py         - cross-validation of log-rank against lifelines
 9. pooled.py       - pooled Mantel-Haenszel / stratified log-rank + sensitivity sets (T3)
10. immuno.py       - immunology contrasts, label correction of S03-B/F, HAI LLOQ handling (T4) -> values_corrected.csv
11. safety.py       - S09-A timepoint check, lung cytokines, CNS, post-vaccination weight (T5-T8)
12. moa.py          - mechanism perturbations and dose-response (T9, T10)
13. extra.py        - comparator (cGAMP/R848) numbers and bootstrap restoration indices (T11)
14. young.py, reuse.py, check2.py, showbw.py - supporting checks quoted in the report
15. power.py        - exact Fisher power and immunogenicity sample sizes (T12)
16. audit.py        - audit log + forensic tables (A log, T14, T15)
17. figs.py, moafig.py - figures 1-6
18. workbook.py     - assembles PSLN_analysis_workbook.xlsx
