# psql25c1 — solvability screen run against the 16-run panel

Per HANDOFF standing decision 13 and `fa/solvability-checklist.md`. **The checklist was
committed 2026-11-12 19:38 (`3165311`); the panel jobs were created 20:17 and 20:17 the
same day.** It predates the evidence by 39 minutes, so it is valid as written.

**Pass rule, unchanged: a leg is solvable if at least one run derives it. A run
disagreeing with the golden is not a failure; only an underivable leg is.**

## Verdict

**The room is solvable as shipped. No route-necessary leg is blocked by the room, so the
batch is FA material and not evidence for a rebuild. No prompt or data-room change is
indicated, and therefore no rerun.**

One leg returns AMBIGUOUS and resolves to a **golden** defect rather than a room defect.
That is a no-rerun fix. Details below.

## Panel provenance, verified before the screen

| Check | Result |
|---|---|
| Prompt served vs `task/prompt.txt` | **Identical in content.** 1,195 against 1,187 characters, the difference being four blank lines separating paragraphs in the `.md` rendering. Diff over non-blank lines: identical |
| Grader guidance served vs `task/grader-guidelines.txt` | **Byte-identical**, sha256 prefix `ab841822cb24`, both jobs |
| Data room mounted | Both jobs mounted the **same** bundle snapshot, `snap_823264f5d03b4b87907bb4d7329e7817.v2`. The bytes are not in the export (`task_files` excluded), so identity with the repo room is established behaviourally rather than by hash: every cell-level figure the runs cite reproduces from the repo workbook, and the graders — which had bash access to the mounted files — recomputed independently and agreed |
| Problem version | `f3a468ce` for both jobs and for the QA export |

So both models saw the same prompt, the same grader and the same room.

## Legs screened

Screened with two or more patterns of differing looseness, every hit confirmed by reading
the matched text. "Runs deriving it" names runs where the derivation is in the deliverable.

| Leg | Claim | Verdict | Derived by |
|---|---|---|---|
| 1 | indicator 1 means death | DERIVED | F1, F2, F5, F8, O1 |
| 2 | which blocks are heterosubtypic, with strain-to-subtype reasoning | **DERIVED** | F3, F4, F7, F8, O2, O5, O7, O8 and others; O8 and O2 give the strict no-shared-HA-or-NA set explicitly |
| 3 | candidate and comparator differ only by the Mn complex | **DERIVED** | F3, F6, O2, O5, O6, O8 state the single composition difference from the annotation's Materials section |
| 4 | the heterosubtypic set derived, not asserted | DERIVED | O1, O2, O7, O8 |
| 5 | `S06-G` read against its own ceiling | DERIVED | every run cites the fifth arm |
| 6 | the fifth arm of `S06-E/F/G` got neither vaccine nor challenge | **DERIVED** | all sixteen, from the annotation |
| 7 | protection exists at day 2–3 | DERIVED | all sixteen |
| 8 | early protection is not antibody-mediated | DERIVED | F1–F8, O1–O8 via `S15-H` and timing |
| 9 | the aged/young diagonal varies two things | DERIVED | F2 (ledger row `M1` and `M2` carry `PSLN-344(Y)` with SD and cell refs), F3, O1 ("Mn still raises young Ifnb1, 50.2 vs 37.5") |
| 10 | the within-age adjuvant effect is the clean comparison | DERIVED | nearly all; F2 row `M23` computes it in all five four-arm blocks with an interaction p |
| 11 | endpoint direction before pooling | DERIVED | F1, O1, O4, O5, O8 |
| 12 | age-matched and young give opposite reads | DERIVED | F8 states it outright for the 72 h tail |
| 13 | all immunoassays are homologous-antigen | **DERIVED** | F3, F4, F5, F8, O5, O7, O8 |
| 14 | antigen-independence across immunogens | DERIVED | all sixteen enumerate more than one |
| 15 | the effector chain established by blockade | DERIVED | F1, F2, F3, O1, O4, O5, O6 |
| 16 | second `S09-A` block is the 72 h panel | DERIVED | all sixteen |
| 17 | `S09-A` is log10 | DERIVED | all sixteen exponentiate correctly |
| 18 | all seven analytes unresolved at 72 h | DERIVED | F4, F7 and O5 report the full seven-analyte set |
| 19 | non-resolution is a formulation property | **AMBIGUOUS — see below** | none |
| 20 | tolerability assays carry controls | DERIVED | F8, O4, O7 name the positive control |
| 21 | dose at plateau | DERIVED | all sixteen read `S08-A` |
| 22 | no accessible antigen-independent marker | DERIVED | F1, F6, F7, O1, O3, O7, O8 separate peripheral from lung-local |
| 23 | no per-animal immune-to-outcome linkage | DERIVED | F7, O1, O3, O4, O6 state the absence |

**The four highest-stakes rows pass.** Legs 2, 3, 6 and 13 rest on the annotation alone and
were the rows most exposed to rename 3's 188 annotation substitutions. All four are derived
by multiple runs across both models. **The annotation survived the renames**, which is the
question standing decision 13 wanted the panel to answer.

## Leg 19 — AMBIGUOUS, and it is the golden that is wrong, not the room

**The leg as declared:** "non-resolution is a formulation property", basis young+candidate
3.13 against young+comparator 1.59, DERIVED if the run "makes the within-young comparison".

**No run makes it.** F2 prints all four `S01-A` 72 h arms in ledger row `M2` — sham 1.00,
aged parent 3.43, aged candidate 4.43, young parent 1.59, young candidate 3.13, with SDs and
cell references — and computes Tukey p for candidate against aged parent (0.42) and against
young parent (2.2e-05), but **not** young candidate against young parent. Every other run
that engages the residual frames it as aged candidate against young parent. O5 reaches the
**opposite** conclusion: "This is an ageing feature that Mn²⁺ does not correct."

**This resolves to a golden defect, for three reasons, in order of weight.**

1. **The leg's target claim is not true, so the room cannot be blamed for not yielding it.**
   `S01-A` Ifnb1 at 72 h, n = 5 per arm, Welch t computed by hand:

   | Contrast | Ratio | p |
   |---|---|---|
   | formulation effect in **young** (344Y / 212Y) | 1.97 | **0.0126** |
   | formulation effect in **aged** (344 / 212) | 1.29 | 0.2619 |
   | age effect on the **parent** (212 / 212Y) | 2.16 | **0.0009** |
   | age effect on the **candidate** (344 / 344Y) | 1.42 | 0.1756 |
   | young candidate vs untreated | 3.14 | **0.0041** |
   | aged parent vs untreated | 3.45 | **<0.0001** |

   Both ageing and the formulation raise the residual, each significantly in the arm where
   the other is absent, and neither adds significantly on top of the other. "A property of
   the formulation **and not of the aged lung**" is not supportable: the aged lung on the
   Mn-free parent already fails to clear, at 3.45× untreated, which is higher than young
   animals on the candidate.
2. **The facts are legible and were retrieved.** F2 holds all four arms. The comparison is
   one subtraction away from a table it built. That is the checklist's "never needed it for
   the route they took", not "tried and could not" — which is the distinction the checklist
   says decides room-versus-mode, and it decides against a room defect.
3. **The pass rule covers the disagreement.** O5's reading is a disagreement with the
   golden, not a failure, and the checklist records that twice already a solvability agent
   has been right and the golden wrong. O5 is right about the datum the golden's clause
   ignores.

### Golden revision, supplied for the writer's go — not applied

| | |
|---|---|
| Location | `task/golden-response.md`, Study 3 "Resolution kinetics, as the gating tolerability study", the *Establishes* bullet, final sentence |
| Original | "Young animals given PSLN-344 also fail to clear, so this is a property of the formulation and not of the aged lung, which means it will not resolve itself in a younger population." |
| Words changed | Keep the first clause and the conclusion; replace the exclusive attribution in the middle with the four contrasts and the limit |
| Replacement | "Young animals given PSLN-344 also fail to clear, 3.13 against 0.996 untreated (p = 0.0041), so it will not resolve itself in a younger population. The attribution goes no further than that, and the block does not let it: the formulation raises the residual in young animals (3.13 against 1.59, p = 0.0126) and ageing raises it on the parent formulation (3.43 against 1.59, p = 0.0009), while neither adds significantly on top of the other (candidate over parent in aged animals 1.29, p = 0.2619; aged over young on the candidate 1.42, p = 0.1756). Both contribute, and the design cannot separate them further — which is itself why the resolution study has to carry age-matched parent and untreated arms." |
| Why | The clause as written is contradicted by the aged parent arm in the same block. Every figure in the replacement is computed from `S01!H3:L10` |
| Derivability | Passes. Uses only the four 72 h arm means already in the room; adds no fact the runs could not reach |
| Ledger effect | **None on Mode 1 or its counterfactual.** It removes a golden claim that was a milder version of the mode Mode 1 describes, on the same block, which is worth knowing: the golden read a two-variable design on one diagonal too |
| Also update | Brief leg 19 in `build/anton-brief-psql25c1.md` section 3, and leg 19 in `fa/solvability-checklist.md`, to the non-exclusive claim |
| Regeneration | `python3 -I make-artifacts.py` then `--check` (the `.txt` and `.pdf` copies are generated), and add the four new figures to `audit-golden.py`'s claimed set so `CORRESPONDENCE` stays provable. **Not done — awaiting go** |
