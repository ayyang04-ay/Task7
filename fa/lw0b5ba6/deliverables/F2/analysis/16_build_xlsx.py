#!/usr/bin/env python
"""Step 16 - evidence workbook: the ledger plus every analysis table behind it."""
import sys, json
sys.path.insert(0, "/tmp/outputs/analysis")
import pandas as pd, numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import integrity_log as IL
O = "/tmp/outputs/analysis/stats"; SRC = "/tmp/outputs/analysis/report_src"
OUT = "/tmp/outputs/PSLN-344_evidence_ledger.xlsx"
wb = Workbook()
HEAD = PatternFill("solid", fgColor="0B3954"); HF = Font(bold=True, color="FFFFFF", name="Calibri", size=10); BF = Font(name="Calibri", size=10)
thin = Side(style="thin", color="C8CED6"); BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
def add_sheet(title, df, widths=None, wrap=(), note=None, numfmt=None):
    ws = wb.create_sheet(title[:31]); r0 = 1
    if note:
        ws.cell(1, 1, note).font = Font(italic=True, name="Calibri", size=10); ws.row_dimensions[1].height = 30
        ws.cell(1, 1).alignment = Alignment(wrap_text=True, vertical="top"); ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=max(2, min(len(df.columns), 8))); r0 = 2
    for j, c in enumerate(df.columns, 1):
        cell = ws.cell(r0, j, str(c)); cell.fill = HEAD; cell.font = HF; cell.alignment = Alignment(wrap_text=True, vertical="center"); cell.border = BORDER
    for i, row in enumerate(df.itertuples(index=False), r0 + 1):
        for j, v in enumerate(row, 1):
            if isinstance(v, (np.floating, float)):
                v = None if (v != v) else float(v)
            elif isinstance(v, (np.integer,)): v = int(v)
            elif isinstance(v, (np.bool_,)): v = bool(v)
            cell = ws.cell(i, j, v); cell.font = BF; cell.border = BORDER
            col = df.columns[j - 1]
            cell.alignment = Alignment(wrap_text=col in wrap, vertical="top")
            if isinstance(v, float):
                if numfmt and col in numfmt: cell.number_format = numfmt[col]
                elif col.startswith("p_") or col.endswith("_p") or "anova" in col: cell.number_format = "0.0000"
                else: cell.number_format = "0.###"
    for j, c in enumerate(df.columns, 1):
        w = (widths or {}).get(c)
        if w is None:
            mx = max([len(str(c))] + [len(str(x)) for x in df.iloc[:200, j - 1].tolist()]); w = min(max(9, mx + 2), 42)
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = ws.cell(r0 + 1, 1); ws.auto_filter.ref = f"A{r0}:{get_column_letter(len(df.columns))}{r0 + len(df)}"
    return ws

# README
ws = wb.active; ws.title = "README"
lines = [("PSLN-344 evidence workbook", True), ("Companion to PSLN-344_portfolio_proposal.docx. Every value is computed by the scripts in analysis/ from psln_program_dataset.xlsx; nothing here is typed by hand.", False), ("", False),
         ("Sheet", True), ("Ledger - one row per number (or set of numbers) used in the proposal: statement, value, workbook cells, analysis output, method and test. IDs match Appendix B.", False),
         ("Survival by arm - survivors, n, exact 95% CI, median survival and death days for every arm of every time-to-event block, with the design facts from the annotation.", False),
         ("Survival pairwise - log-rank (asymptotic and exact permutation) and Fisher exact p for every pair of arms within a block.", False),
         ("Pooled survival - PSLN-344 vs PSLN-212 and vs sham in aged animals under three readings of the workbook (TTE = time-to-event blocks as printed; BW = body-weight-implied; WORST = least favourable to PSLN-344), plus subset sensitivity analyses.", False),
         ("Survival vs weights - survivor count in each survival block against the count implied by its paired body-weight block.", False),
         ("Group statistics - n, mean, SD, median, range, geometric mean and cell range for every group of every continuous block.", False),
         ("Pairwise tests - every pair of groups in every continuous block: ratio, Hedges g, Welch t, Student t, exact Mann-Whitney, ANOVA + Tukey (raw and log10 where applicable).", False),
         ("Restoration - aged PSLN-212 and PSLN-344 as % of the young benchmark for the 25 readouts of Figure 3, plus pooled survival.", False),
         ("Dose-response - sigmoid Emax fits of S08-A.  S09-A fold - geometric-mean fold for both panels of S09-A.", False),
         ("Body weight by arm - per-arm peak weight loss with dead animals handled explicitly.", False),
         ("Power - exact power of two-arm survival comparisons at the effect sizes observed.", False),
         ("Integrity log - the 24 data-integrity findings (Appendix D).", False), ("", False),
         ("Conventions", True), ("Block labels are as printed in the workbook; the second blocks labelled S06-E and S06-F are shown as 'S06-E(2) imprinting/PR8' and 'S06-F(2) imprinting/Perth'.", False),
         ("Groups marked (Y), Y or (y) are young; all others aged. p-values are unadjusted unless the column name says Tukey.", False),
         ("S09-A values are log10 in the source workbook and are kept on that scale in 'Group statistics'; geo_mean there is the fold-change.", False)]
for i, (t, b) in enumerate(lines, 1):
    c = ws.cell(i, 1, t); c.font = Font(bold=b, name="Calibri", size=12 if i == 1 else 10); c.alignment = Alignment(wrap_text=True, vertical="top")
ws.column_dimensions["A"].width = 150

L = pd.DataFrame(json.load(open(f"{SRC}/ledger.json")))
L = L.rename(columns={"id": "ID", "section": "Proposal section", "statement": "Statement", "value": "Value", "workbook_source": "Workbook source (sheet!cells)", "analysis_output": "Analysis output", "method": "Method and test"})
add_sheet("Ledger", L, widths={"ID": 7, "Proposal section": 9, "Statement": 60, "Value": 55, "Workbook source (sheet!cells)": 42, "Analysis output": 36, "Method and test": 60}, wrap=set(L.columns))
A = pd.read_csv(f"{O}/survival_by_arm.csv", keep_default_na=False)
for c in ["survival_pct", "ci95_lo", "ci95_hi", "median_survival_d"]: A[c] = pd.to_numeric(A[c], errors="coerce").replace([np.inf], np.nan)
add_sheet("Survival by arm", A, wrap={"age", "vaccine", "challenge", "match"}, widths={"age": 26, "vaccine": 26, "challenge": 30, "match": 22, "death_days": 22}, numfmt={"survival_pct": "0.0", "ci95_lo": "0.0", "ci95_hi": "0.0"},
          note="median_survival_d is blank where more than half the arm survived. One PSLN-344 row in S03-J has a status but no day (n_missing_time = 1).")
SP = pd.read_csv(f"{O}/survival_pairwise.csv"); add_sheet("Survival pairwise", SP)
P1 = pd.read_csv(f"{O}/survival_pooled.csv"); P1.insert(0, "analysis", "three readings, all aged experiments")
P2 = pd.read_csv(f"{O}/survival_sensitivity.csv").rename(columns={"subset": "reading", "strata": "n_strata", "psln344_ci95": "psln344_ci", "comparator_ci95": "comparator_ci"}); P2.insert(0, "analysis", "subsets, time-to-event blocks as printed")
PP = pd.concat([P1, P2], ignore_index=True)[["analysis", "reading", "comparator", "n_strata", "psln344", "psln344_pct", "psln344_ci", "comparator_surv", "comparator_pct", "comparator_ci", "cmh_chi2", "cmh_p", "mh_risk_diff_pct"]]
add_sheet("Pooled survival", PP, widths={"analysis": 34, "reading": 48, "comparator": 28}, numfmt={"cmh_p": "0.0E+00", "psln344_pct": "0.0", "comparator_pct": "0.0", "cmh_chi2": "0.0", "mh_risk_diff_pct": "0.0"},
          note="Cochran-Mantel-Haenszel test with each experiment as a stratum. CIs are exact (Clopper-Pearson), in %.")
add_sheet("Survival vs weights", pd.read_csv(f"{O}/survival_reconciliation.csv", keep_default_na=False), widths={"tte_death_days": 22, "bw_last_real_day_of_nonsurvivors": 30},
          note="bw_survivors = animals with a real (non-blank, non-frozen) weight on the last day. death_timing_compatible = every death day falls within 2 days after the last real weight.")
S = pd.read_csv(f"{O}/continuous_summary.csv", keep_default_na=False)
for c in ["mean", "sd", "sem", "median", "min", "max", "geo_mean"]: S[c] = pd.to_numeric(S[c], errors="coerce")
add_sheet("Group statistics", S, widths={"panel": 34, "scale_note": 44, "cells": 18})
PW = pd.read_csv(f"{O}/continuous_pairwise.csv", keep_default_na=False)
for c in [c for c in PW.columns if c not in ("block", "panel", "x", "group_a", "group_b", "no_overlap")]: PW[c] = pd.to_numeric(PW[c], errors="coerce")
add_sheet("Pairwise tests", PW, widths={"panel": 30})
add_sheet("Restoration", pd.read_csv(f"{O}/restoration_chain.csv"), widths={"readout": 46, "stage": 28})
add_sheet("Dose-response", pd.read_csv(f"{O}/S08A_dose_response_fit.csv"), note="Sigmoid Emax model fitted to log10(Ifnb1 fold) vs dose, S08-A; 95% limits from 2,000 bootstrap resamples within dose.")
add_sheet("S09-A fold", pd.read_csv(f"{O}/S09A_geomean_fold.csv"), note="Geometric-mean fold vs untreated (10^mean of printed log10 values). Panel 2 is printed '16h' in the workbook and identified as 72 h (integrity item D-02).")
add_sheet("Body weight by arm", pd.read_csv(f"{O}/bodyweight_by_arm.csv"), note="Losses are % of day-0 weight. Dead animals (blank or frozen tails) are excluded from the day they stop having real readings.")
add_sheet("Power", pd.read_csv(f"{O}/power_table.csv"), widths={"scenario": 56})
IG = pd.DataFrame(IL.LOG, columns=["Ref", "Severity", "Where", "Finding", "How handled", "Effect on the case"])
add_sheet("Integrity log", IG, widths={"Ref": 7, "Severity": 9, "Where": 30, "Finding": 90, "How handled": 45, "Effect on the case": 60}, wrap=set(IG.columns),
          note="Severity A: changes a conclusion if the workbook is read as printed. B: limits what can be claimed. C: housekeeping for the raw-data check.")
wb.save(OUT); print("written", OUT, [w.title for w in wb.worksheets])
