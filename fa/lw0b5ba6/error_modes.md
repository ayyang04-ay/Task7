# lw0b5ba6 — error mode ledger

Task `task_f9c4675def384c5e820284adce63119b`, problem version `3619eae7`. Panel: Opus job
`70ccbec0`, Fable job `8de89bb3`, 4 attempts each, 2026-11-19. **Trajectory-only mode** —
the version carries no grader guidance, files or rubric, so no mode rests on a score.

Supersedes `fa/psql25c1/error_modes.md`, whose run labels are retired. The mode definition,
counterfactual figures, four-arm block list and 72 h contrasts carry over; labels,
prevalence and exemplars do not.

Run map, parse manifest, verdict map and reading coverage: `submittability.md`.

| Version | Change |
|---|---|
| v1 2026-11-22 | First ledger on the 2026-11-19 exports. Two modes ship; two held, three absent, two inverted. |

---

## Mode 1 — the age claim is measured against a different formulation (16 h)

| Field | Content |
|---|---|
| Short name | Age and adjuvant varied together wherever the aged response is measured against a young one |
| Class | Analytical |
| Runs | O1 O2 O3 O4 F1 F2 F3 F4 |
| Not checked | that the aged-versus-young contrast changes the formulation as well as the age, in the six blocks carrying a young arm on the Mn formulation |
| Description | `S01-A` (`S01` rows 3–10, cols B–F), lung *Ifnb1* 16 h, fold over untreated, n=5: aged+212 **16.64**, aged+344 **37.11**, young+212 **37.60**, young+344 **50.70** (geometric means 16.5 / 36.9 / 37.5 / 50.2). Every run builds a restoration, age-gap-closed or "% of young" figure on the **young+212** denominator and reports the aged response returned to the young level — 0.98, 98%, 100%, "fully restored", "restored 100%" |
| Counterfactual | Formulation held: 37.11 / 50.70 = **0.732**. The uncontaminated reading is the within-cohort increment, available in all six four-arm blocks: `S01-A` aged ×2.23 / young ×1.35; `S01-E` ×2.28 / ×1.06; `S01-F` ×1.65 / ×1.02; `S02-C` ×4.01 / ×1.18; `S02-E` ×24.35 / ×1.20 |
| Four-arm blocks in the room | `S01-A`, `S01-E`, `S01-F`, `S01-G`, `S02-C`, `S02-E` |
| Shape | Encountered-then-unapplied in all 8 — raw values `S01!B10:F10` (60.02, 52.51, 46.93, 54.02, 40.04) read by every run. Established-then-unwritten in six (table below) |
| Exemplar | none — all 8 carry it |
| Consequence | Mechanism step and biomarker rationale in all 8, both prompt-mandated. Biomarker ranking in O4 `:286`. **Removes the golden's age-specificity pillar in all 8** (below). Reaches no gate, stop rule, verdict or asset selection |
| Graded? | n/a |

**Positions**

| Run | Where |
|---|---|
| O1 | `:48` table, `:212` claim 2, `:264` biomarker rationale, `:713` appendix; RI defined at `:9` |
| O2 | `:14`, `:84` table, `:104` definition, `:400`, `:473` method |
| O3 | `:66` table "Restored 100%", `:372` definition |
| O4 | `:244` step 2, `:275` biomarker tier, `:507` definition |
| F1 | `:99` table, `:194` step 3, `:225` biomarker row |
| F2 | `:178`, `:404` E515, `:646` definition |
| F3 | `:161` table, `:1715` definition |
| F4 | `:89` table "98%", `:105` "fully restored" |

**Had the controlling value and did not use it**

| Run | What it held | Where |
|---|---|---|
| O3 | ran a block headed "Young: does Mn add anything?" giving GM 37.5 → 50.2 (1.34x), Welch p=0.0092; deliverable never prints 50.2 | transcript blk136 |
| F4 | own stats table carries `Y212 37.5`, `Y344 50.2` **and** a computed `344vY 0.98`; ships only the 0.98 | transcript blk90 |
| O1 | "37.5 → 50.2, +34%, p=0.009" in the deliverable itself | `:288` |
| F2 | 50.7 with cell range `S01!B10:F10` as ledger entry E099; computes 1.3x p=0.009 | `:484`, `:178` |
| F3 | 50.2 with cell range as row 120; prints 37.5 / 50.2 side by side | `:1365`, `:179` |
| O4 | "50.7 vs 37.6" noted in reasoning | transcript blk75 |
| F1 | tool output printed "young: PSLN-212(Y) 37.6, PSLN-344(Y) 50.7" three times | transcript blk88 |

**Two runs reason about the benchmark and still use it.** F3 `:721` lists "Pooling the young
benchmark with aged animals as if it were an age-matched control" among things it rules out.
F2 `:342` lists "Restores the aged response to young" under claims it does not think the data
support, on CD40/CD86 grounds — contesting the conclusion without correcting the comparison.

**Defensibility — both sides, writer's call.** *For:* a restoration index against young on the
current regimen is conventional; six runs state the denominator in a methods line. *Against:*
the claim made is about age ("returns the aged response to the young level", "fully
restored"), which requires the formulation held; the controlling arm is in the same block,
all 8 read its raw values, six computed the contrast.

---

## Mode 2 — the same denominator on the 72 h panel, where it inflates the risk

| Field | Content |
|---|---|
| Short name | Reactogenicity read against the young Mn-free arm |
| Class | Analytical |
| Runs | O1 O3 O4 |
| Not checked | that the age-matched Mn-free arm carries the same 72 h tail |
| Description | `S09-A` panel 2 (`S09` cols X–AS rows 3–9, printed 16 h, holds 72 h). Reported as Tnf "8.4x vs young 0.5x" (O1 `:267`), "whereas young animals have resolved (0.5x, 0.1x)" (O3 `:107`), "2.9x the young PSLN-212 level" (O4 `:226`). This is the one reading in the package that argues against the asset |
| Counterfactual | Against the age-matched Mn-free arm: Tnf ×1.62 (p=0.052), Il10 ×1.00 (p=0.991), Ifnb1 ×1.18 (p=0.665); `S01-A` n=5 Ifnb1 ×1.29 (p=0.2619). Aged+212 carries Tnf 5.2 and Il10 4.2. Only Il6 separates, ×3.85 p=0.026. Two analytes reverse: young+212 Ccl2 101.59 and Ccl3 41.45 against aged+344's 27.41 and 9.23 |
| Exemplar | **F4** `:125` holds age constant outright ("PSLN-212 also resolved slowly in aged lung, Tnf 5.2-fold at 72 hours"); **F3** `:171` `:187` reports the aged Mn-free column alongside; **F2** `:190` reports both |
| Consequence | How the asset's only safety signal reads. Not the verdict |
| Graded? | n/a |

Stronger than Mode 1 on defensibility: three runs held the formulation constant on the
identical panel, so the room does not force the error.

---

## Held — not dropped; the writer decides

| # | Candidate | Runs | Bar failed |
|---|---|---|---|
| 3 | O1 states both readings of the 72 h panel: correct age-matched contrast with its interval at `:774` (Tnf ×1.62, 0.99–2.62, p=0.052), young-denominator version in the recommendation body at `:92` `:267` | O1 | Prevalence — one run. Could fold into Mode 2 as a shape |
| 4 | "In young animals manganese adds nothing" (`:166`) used to exclude adults under 50 and children from the TAM (`:300`) | F2 | Defensibility, on the run's own figure: `:178` reports the contrast as "p = 0.009 Welch, **0.63 after Tukey**". Golden uses uncorrected Welch (p = 0.014). Both methods defensible |

## Absent

| Candidate | Finding |
|---|---|
| Matched-subtype blocks pooled into a cross-subtype claim | Not observed. No Fable run uses cross-subtype vocabulary; Opus runs that do name the blocks individually |
| Proposing an adjuvant-alone or antigen-free arm the room already settles | Not observed, second consecutive panel. All 8 cite `S15-H`. Pre-registered, so readable as an absence rather than an oversight |
| Over-applying a duplication finding to the whole 72 h panel | Not observed. All 8 cite `S06-D`; all 8 use the panel |
| Antibody offered as the cross-subtype correlate | **0 of 8.** Every apparent hit is HAI as a matched-strain non-inferiority endpoint beside a separate cross-protection endpoint (O2 `:294`, O4 `:341`, F1 `:335`), or an explicit statement that antibody to the mismatched virus was never measured (F2 `:255` `:276`, F4 `:157`) |

## Inverted — runs right, golden short. Not modes; belongs in the correct-approach section

| Finding | Runs |
|---|---|
| The conventional HAI threshold does not discriminate inside this package. `S03!M3:M7` = 40, 80, 40, 40, 40, all at or above it, against PSLN-212 survival 0/7 in `S03-I` (3/7 on the weight block). Golden has **zero** occurrences across nine spellings of the threshold | O1 `:273` O3 F1 `:245` F2 F3 F4 `:177` `:358` — 3 Opus, 3 Fable. **O1 is the most careful**: notes the titres and survival come from different animals, flags `S03-I`'s integrity problem, proposes ≥1:160 with counts, and designs a study measuring both in the same animals |
| Antibody filed in an "efficacy surrogate" tier against the golden's "not as the efficacy marker" | O1, O3. Label-versus-substance: both carry the discriminating observation in the same section, so defensible |

## Golden-part coverage

| Golden part | Present in | Caused by a mode? |
|---|---|---|
| Age-specificity as the **magnitude** of the priming gain, not its existence (`:54`–`:69`) | **0 of 8** | **Yes — Mode 1.** The wrong denominator replaces a magnitude claim with a binary restoration claim. Four runs assert the opposite of the golden's warning that the data will not support "the asset does nothing in young animals": O2 `:16`, F2 `:166`, F3 `:655` `:698`. O1 `:288` is closest and defensible |
| No per-animal immune-to-outcome link | 8 of 8 — F1 `:219`, F2 `:261`, F3 `:256` state it in their own words | — |
| Antibody not the cross-subtype correlate | 8 of 8 | — |
| Antigen dose unanswerable, HA content never varied | 0 of 8 | No. All 8 engage high-dose comparators in another form; prompt asks for no inventory of unanswerable questions. Calibration, as at 0 of 16 in the retired panel |
| HAI threshold non-discriminating | 6 of 8, golden lacks it | No. Golden gap |

**One run contradicts the golden.** O4 `:276` proposes nasal GM-CSF as the human sampling
route; the golden calls GM-CSF a lung transcript with no patient-accessible version, "a gap,
not an asset". F1 `:239` sides with the golden. External knowledge decides it, not the room.
Unresolved.

## Calibration — not FA material

No mode bears on the verdict. All 8 reached the golden's call (keep, PSLN-344 leads,
PSLN-212 stops, gated) on every decision the prompt asks for. The verdict is over-determined:
+71 points from the `S06` series, a path carrying no trap. The retired panel recorded the
same. The advance/decline split that panel showed has collapsed — all 8 now gate.

## Correction log

| Claim | Status |
|---|---|
| Mode 1 carried into a human PD go criterion in O1, O2, O4 | **Withdrawn.** O2's gate `:266` uses the within-aged ratio 2.23, the correct contrast; O4 `:275` is a ranking row; O1 has no such criterion. The criterion cited belongs to the retired panel's O1 `:370` |
| Golden's per-animal-linkage statement missing from F1, F2, F3 | **Withdrawn.** Pattern artefact from a tight probe; all three state it. Loosening found 8 of 8 |

## Epistemic labels

[computed] all `S01-A` and `S09-A` arm means, ratios and the `S03-C` titres, recomputed from
`data-room/psln_program_dataset.xlsx` this session. [transcript] every position above, read in
the run's own deliverable or transcript. [inference] that the biomarker rationale inherits the
confound — stated by the runs themselves at O1 `:264`, O4 `:275`, F2 `:267`, not inferred.
p-values are the runs' own or the retired ledger's hand-computed figures; no scipy in this
container.

**Retype, do not transcribe.** Paste is disabled in Studio and an overlap check runs before
submission.
