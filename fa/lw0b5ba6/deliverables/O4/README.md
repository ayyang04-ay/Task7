# PSLN-344 portfolio review: deliverables (data cut 1 Nov 2026)

**Bottom line:** Do not advance on the current package. Keep PSLN-344 only as a frozen asset behind two gates: a 3-month forensic data audit, then an independent confirmatory aged-mouse study run alongside Mn/CNS safety and CMC work. Termination is the default if either gate fails. If the choice today were strictly advance or drop, drop.

| File | What it is |
|---|---|
| `PSLN-344_Portfolio_Proposal.pdf` | Committee document (14 pp.): recommendation, gated next steps with endpoints, evidence, integrity findings, MoA, biomarkers, target demographic, options ruled out, methods, appendices |
| `PSLN-344_Portfolio_Proposal.md` | Same content in Markdown |
| `PSLN-344_evidence_ledger.xlsx` | Every quoted number → claim ID → workbook cells → analysis output (27 sheets, including per-animal tidy data with cell references) |
| `figures/` | Figures 1–7 (PNG) |
| `analysis/` | All Python scripts and intermediate CSVs (run order in proposal Appendix B; env `chem`) |

To trace a number: find the claim ID in the proposal (e.g. `E12c`), look it up in the ledger's **Claims** sheet, then use the listed cells or ledger sheet.
