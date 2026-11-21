# PSLN program: portfolio-review package (data as of 1 Nov 2026)

**Recommendation:** keep the program. Take **PSLN-344** forward as the single lead and stop **PSLN-212**. Fund in gates: Gate 0 (data verification, a hard stop) → Gate 1 (confirmatory and attribution study) → Gates 2–3 (benchmark, durability, Mn/CNS safety, CMC/device) → IND.

| File | What it is |
|---|---|
| `PSLN_portfolio_proposal.pdf` | Committee proposal (20 pp). Recommendation first, then evidence, data-integrity findings, MoA, biomarkers, gated study plan, target demographic, what we give up, what was ruled out, risks, and appendices. |
| `PSLN_portfolio_proposal.docx` / `.md` | Editable versions with the same content. |
| `PSLN_analysis_workbook.xlsx` | Evidence register (every headline number with source block, cell range and analysis ID), integrity log, study plan, all statistical tables, and tidy source data with cell addresses. |
| `figures/` | Fig 1 survival overview; Fig 2 Kaplan–Meier; Fig 3 age-gap closure; Fig 4 immunogenicity; Fig 5 dose–response; Fig 6 MoA schematic; Fig 7 safety; Fig 8 data-integrity exhibits. |
| `supporting/` | Raw outputs of the duplication scans and the integrity log (CSV). |
| `code/` | Full pipeline (`run_all.sh`). Regenerates every number, figure and document from the two source files; includes a raw-cell recomputation check (16) and a document-number audit (17). |

Citation convention used throughout: `[Sxx-Y]` = block in `psln_program_dataset.xlsx` as annotated in `psln_program_annotation.pdf`; `[A#]` = analysis ID (Appendix A of the proposal; README sheet of the workbook).
