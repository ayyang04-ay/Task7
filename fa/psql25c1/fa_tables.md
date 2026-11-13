# psql25c1 — the two form questions, as tables

Strip-down of `fa_outline.md` for typing straight into the form. Cells are clipped on
purpose: a cell that reads as a finished sentence gets pasted, and pasted prose is what
the overlap check catches. **Retype.**

## Q1 — What did the model do wrong

**Item: the aged response is measured against a differently formulated young arm.**
Runs: F1, F2, F3, F4, F5, F6, F7, F8, O1, O2, O3, O4, O5, O6, O7, O8.

| Fact | Value |
|---|---|
| Block | `S01-A`, `S01` rows 3–10 cols B–F; lung *Ifnb1* 16 h, fold over untreated |
| aged + parent | 16.64 (GM 16.5) |
| aged + candidate | 37.11 (GM 36.9) |
| young + parent | 37.60 (GM 37.5) |
| young + candidate | **50.70 (GM 50.2)** |
| What the panel reported | aged/young = 0.98, "restored to the young level", "99%", "closes 98% of the age gap" |
| Formulation held constant | 37.11 / 50.70 = **0.732** |
| The clean contrast in the same block | adjuvant effect within cohort: aged ×2.23, young ×1.35 |
| Same contrast, other four-arm blocks | `S01-E` ×2.28/×1.06; `S01-F` ×1.65/×1.02; `S02-C` ×4.01/×1.18; `S02-E` ×24.35/×1.20 |
| Four-arm blocks in the room | `S01-A`, `S01-E`, `S01-F`, `S01-G`, `S02-C`, `S02-E` |
| Had the controlling value and did not use it | F2 `:455` ledger row `M1`; F3 ruled-out table; O1 `:258` |
| Computed the clean contrast and did not carry it | F2 `:479` ledger row `M23` |
| Carried the confounded index into a human go criterion | O1 `:370` |
| Exemplar at this site | none — all sixteen carry it |

**Second site — the same denominator at 72 h, inflating the risk.** Runs: O2, O3, O4, O5, O6, O8.

| Fact | Value |
|---|---|
| Panel | `S09-A` panel 2, `S09` cols X–AS rows 3–9 (printed 16 h, holds 72 h); plus `S01-A` 72 h |
| What the panel reported | "2.85× the young level", "285% of young", "Tnf 17.8× / Il10 36.6× vs the young benchmark", restoration fraction −0.235 / −0.24 |
| Against the age-matched parent | Tnf ×1.62 p = 0.052; Il10 ×1.00 p = 0.991; Ifnb1 ×1.18 p = 0.665; `S01-A` n=5 Ifnb1 ×1.29 p = 0.2619 |
| Two analytes reverse | young parent Ccl2 101.59 and Ccl3 41.45 vs aged candidate 27.41 and 9.23 |
| Real candidate-specific excess | Il6 only, ×3.85 p = 0.026 |
| **Exemplars** | **F8 `:168`** states the Tnf/Il10 tail is an age effect because the aged parent shows the same, isolating Il6 at p = 0.03. **F4 `:251`** reports both columns, Tnf ×17.8 vs young and ×1.6 vs aged parent (0.99–2.6) |

## Q2 — What should the model have done

See `fa_outline.md` Part 2 for the components table and the closed alternatives. The three
items that belong here **because** they failed the defensibility bar:

| Should have done | Not a failure because |
|---|---|
| Named the antigen-dose question as unanswerable and proposed a dose-ranged high-antigen arm at the asset's own route | the prompt does not ask for an inventory of unanswerable questions; ten runs proposed the licensed high-dose comparator, which is its commercial form |
| Specified when the 72 h response returns to baseline | n = 3, one timepoint, panel carries its own duplication flag, no separation from the age-matched parent on five of seven analytes; O4 built a 72 h guard-rail anyway |
| Used the cross-subtype subset as the unit of analysis | seven runs rest a breadth claim on an all-challenge pool but name the heterosubtypic blocks individually in a table; only O6 miscalls the imprinting blocks cross-subtype, and one run does not clear the floor |

## Counterfactual figures the writer will need

| Quantity | Value |
|---|---|
| Strict cross-subtype set, `S06-A`/`S06-B`/`S06-E`(34–68)/`S06-G` | candidate 20/28, parent 1/28 |
| Plus the N1-sharing blocks `S06-C`, `S06-F` | candidate 32/42, parent 4/42 |
| 72 h analytes above untreated, aged candidate | Ccl2 27.41, Ccl3 9.23, Tnf 8.44, Il6 7.19, Il10 4.16, Ifnb1 4.01, Ccl5 2.01 |
| 72 h four-way, `S01-A` | formulation in young ×1.97 p = 0.0126; in aged ×1.29 p = 0.2619; ageing on parent ×2.16 p = 0.0009; on candidate ×1.42 p = 0.1756 |
| Antigen doses in the whole room | 0.5 µg HA CA09, 1 µg HA Aichi. Never varied |
