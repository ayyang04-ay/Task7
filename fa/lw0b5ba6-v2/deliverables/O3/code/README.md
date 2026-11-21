# Analysis code for the PSLN-344 portfolio proposal

Input: `/tmp/world/filesystem/psln_program_dataset.xlsx` (path set in `load.py`).

Environments used: `mm chem` (openpyxl; parsing) and `mm core` (scipy/statsmodels/lifelines/matplotlib; statistics and figures).

Run order:
1. `mm chem python -c "from load import *; DF.to_csv('/tmp/work/tidy_values.csv',index=False); SV.to_csv('/tmp/work/tidy_survival.csv',index=False)"`
   * `load.py` parses every block with its sheet and cell address.
   * `loadcsv.py` reloads the tidy CSVs.
2. Integrity checks: `integ1.py` … `integ9.py`.
   * Derived-quantity checks: Tfh:Tfr and IgG2a/IgG1.
   * Cross-experiment duplication and the chance baseline.
   * Survival vs body-weight reconciliation.
   * Duplicated survival blocks.
   * Timepoint and label checks for S09-A and S08-C.
3. Statistics:
   * `stats_h2h.py`: 43-readout head-to-head → `h2h_344_vs_212.csv` → T1.
   * `stats_surv.py`: per-study and pooled survival → T2/T3.
   * `stats_moa.py` and `t5.py`: causal MoA experiments → T5.
   * `stats_panel.py`: S09-A panel → T4.
   * `stats_safety_dose.py`: S08-A/B/D and S10-A.
   * `stats_power.py`: sample sizes.
4. Tables and register: `tables.py`, `register.py`.
5. Figures: `fig1_forest.py`, `fig2_survival.py`, `fig3_integrity.py` (→ Fig5), `fig4_moa.py` (→ Fig3), `fig5_dose_safety.py` (→ Fig4), `fig6_biomarkers.py`.

Notes:
* Intermediate files go to `/tmp/work/`.
* Random seeds are fixed for the power simulations.
* S03-J has one PSLN-344 row with no time value (cell G46 blank, J46 = 0). It is treated as censored at the end of follow-up (21 d).
* HAI <1:10 is set to 5.
