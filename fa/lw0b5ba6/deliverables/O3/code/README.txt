PSLN portfolio analysis - reproducibility package
=================================================
Inputs : /tmp/world/filesystem/psln_program_dataset.xlsx, psln_program_annotation.pdf
Outputs: /tmp/outputs (proposal DOCX/PDF, PSLN_analysis_tables.xlsx, figures/)
Run    : copy these scripts to /tmp/work and execute ./run_all.sh  (conda envs: chem for Python, genomics for pandoc)

Order and purpose
  parse.py               every workbook block -> tidy tables with source cell (continuous / survival / weights)
  audit1.py, audit2.py   duplicate-value screens; derived-block checks (S03-B/F vs S13, Tfh:Tfr vs Foxp3, S09-A vs S01-A)
  audit3.py              survival vs paired body-weight reconciliation
  audit4.py, audit5.py   identical survival vectors / weight rows; cross-block weight-trajectory recycling
  audit_s11.py           S11-A vs S11-B animal-level identity
  analysis_cont.py       group summaries, ANOVA + Tukey, Welch/Student, exact Mann-Whitney, Hedges g (all continuous blocks)
  analysis_surv.py       per-experiment Kaplan-Meier, log-rank, Fisher
  analysis_pool.py       pooled aged survival (MH risk difference, CMH, stratified log-rank) under 4 integrity scenarios
  analysis_safety.py     post-vaccination weight nadir (S08-D), CNS transcripts (S10-A)
  analysis_biomarkers.py biomarker separation (AUC, Hedges g, % of young), arm-level concordance, dose-response fits
  analysis_extra.py      key endpoint ratios; payload comparison; encapsulation efficiency
  analysis_twoway.py     two-way ANOVA (group x time)
  analysis_mech.py       perturbation experiments (CCR2, IFNAR, GM-CSF, PTX, CBX, SP-A/D)
  exp_table.py           aged-experiment survival table with integrity flags
  integrity_table.py     the 17 integrity findings
  power.py               exact Fisher and t-test sample sizes for Gate 1
  figures.py             Figures 1-7
  citation_index.py      recomputes every headline number with its source block/sheet
  build_workbook.py      PSLN_analysis_tables.xlsx
  build_report.py        proposal.md -> DOCX (pandoc) and PDF (reportlab)
