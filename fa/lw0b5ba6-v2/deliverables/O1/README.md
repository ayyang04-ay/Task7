# PSLN portfolio review: deliverables

**Start here:** `PSLN_portfolio_proposal.docx` (editable). The same content is in `PSLN_portfolio_proposal.html` (self-contained; print to PDF from a browser) and `PSLN_portfolio_proposal.md`.

## What is where

| Path | Contents |
|---|---|
| `PSLN_portfolio_proposal.*` | The committee proposal. Recommendation first, then comparison, data integrity, MoA, biomarkers, target demographic, gated next steps, what we give up if we drop, what was ruled out, methods, appendices |
| `figures/` | Fig 1 survival forest plot; Fig 2 Kaplan–Meier grid; Fig 3 immune-cascade effects and restoration index; Fig 4 Ifnb1 dose–response; Fig 5 MoA schematic |
| `analysis/evidence_ledger.csv` | **Every number quoted in the proposal text**: value, meaning, source block(s)/cells, analysis script. Column `used_in_proposal_text` marks the 158 quoted facts |
| `analysis/tidy/` | Every observation extracted from the workbook, with its cell reference (`values.csv` scalar endpoints, `tte.csv` survival, `bw.csv` body weight, `s08_unlabeled.csv`) |
| `analysis/h2h_endpoints.csv` | PSLN-344 vs PSLN-212 for every endpoint: effect, 95% CI, Welch p, exact Mann–Whitney p, BH q, restoration index; exclusions with reasons |
| `analysis/survival_*.csv` | Survival by group, pairwise tests, pooled analyses (sets A–F), leave-one-out |
| `analysis/integrity_register.csv` | 22 data-integrity findings (4 critical, 8 major, 10 minor) with cells, impact, handling, remediation |
| `analysis/bw_vs_tte.csv` | Reconciliation of each survival block with its body-weight block |
| `analysis/audit_logs/` | Raw outputs of every check and analysis step |
| `code/` | Full pipeline; `run_all.sh` regenerates everything from the workbook in about 2 minutes |

## How a committee member can check a number

1. Find the number in `analysis/evidence_ledger.csv`. It gives the source block (e.g. S03-C) and, for survival, the cells.
2. Open the workbook at that block. `analysis/tidy/*.csv` maps every value to its exact cell (e.g. `S03!N3`).
3. Re-run `code/run_all.sh` to reproduce the analysis.
