# lw0b5ba6 — FA writer handoff

Bare facts arranged under the Studio form's fields. **Nothing here is a sentence for the
form.** Paste is disabled and an AI-writing check runs before submission; the way to pass it
is to write the sentences yourself from these facts, not to rework supplied prose.

Source: `error_modes.md` (ledger), `submittability.md` (manifest, run map, verdict map).
A correction made in the ledger propagates by rewriting one cell here.

## Field shapes — from review feedback on another task, 2026-11-22

Four rules that cost a round trip there. Apply them before writing, not after.

| Field | Must hold | Must not hold |
|---|---|---|
| `failure_mode_type` | A general category. Applies to tasks other than this one | Run labels, assay names, block IDs, a consequence clause, or a restatement of `failure_mode` |
| `failure_mode` | The specific behaviour, phrased as a test a reader can apply yes/no to a **new** trajectory | A description of what the data room lacks. A bundle of separate defects |
| `rollouts[].description` | What that one attempt did, and where | Anything the attempt did well. Any run not visibly showing the stated behaviour |

Two further rules from the same review and from the output rules:

- **Every cited attempt must visibly show the stated behaviour.** An attempt whose entry
  explains why it avoided the problem gets the citation struck.
- **No praise inside a failure item.** "Which is reasonable", "the conclusion is right",
  "correct approach" get the item rejected. Anything a run did well goes in the
  should-have-done field.
- No scores. No k-of-n ratios. Name the runs.

---

# Entry 1

## `failure_mode_type` — category to denote

An analytical comparison that varies two factors at once where the room contains the arm
holding the second fixed. No runs, no blocks, no consequence.

## `failure_mode` — the test

Applies yes/no to a new trajectory: does the response report an age-related restoration,
age-gap-closure or percent-of-young figure whose denominator is young animals on the
comparator formulation, while the same block carries young animals on the asset formulation.

## `What did the model do wrong` — facts

Block: `S01-A`, sheet `S01` rows 3–10, cols B–F. Lung *Ifnb1* at 16 h, fold over untreated,
n=5 per arm.

| Arm | Arithmetic mean | Geometric mean | Cells |
|---|---|---|---|
| aged + PSLN-212 | 16.64 | 16.5 | `S01!B5:F5` |
| aged + PSLN-344 | 37.11 | 36.9 | `S01!B8:F8` |
| young + PSLN-212 | 37.60 | 37.5 | `S01!B9:F9` |
| young + PSLN-344 | **50.70** | **50.2** | `S01!B10:F10` |

Reported figure across the panel: 0.98, 98%, 100%, "fully restored", "restored 100%",
"returns the aged response to the young level". Denominator in every case is young+PSLN-212.

Four-arm blocks in the room — the only ones where age varies with formulation fixed:
`S01-A`, `S01-E`, `S01-F`, `S01-G`, `S02-C`, `S02-E`.

Raw per-animal values of the controlling arm, read by all eight: 60.02, 52.51, 46.93, 54.02,
40.04.

## `rollouts[].description` — eight boxes

Per-attempt. Position column is the deliverable line unless marked transcript.

| Attempt | What it did | Where |
|---|---|---|
| Opus 1 | Defines the index on young+PSLN-212 at `:9`; reports 0.98 at `:48`, `:212`, `:264`, `:713`. **Also prints the controlling contrast in the same document — "37.5 → 50.2, +34%, p=0.009"** — and leaves 0.98 unchanged | `:9` `:48` `:212` `:264` `:288` `:713` |
| Opus 2 | Defines age-gap closure on young+PSLN-212 at `:104` and `:473`; extends the same denominator to 40 readouts; reports 98% at `:84` and `:400` | `:84` `:104` `:400` `:473` |
| Opus 3 | Reports "Restored 100%" at `:66`; defines the index on young+PSLN-212 at `:372`. **Ran a probe headed "Young: does Mn add anything?" giving GM 37.5 → 50.2, 1.34x, Welch p=0.0092, and the deliverable never prints 50.2** | `:66` `:372`; transcript blk136 |
| Opus 4 | Defines the index on young+PSLN-212 at `:507`; reports 0.98 at `:244` and carries it into the biomarker tier at `:275`. Noted "50.7 vs 37.6" in reasoning | `:244` `:275` `:507`; transcript blk75 |
| Fable 1 | Uses 37.6 as the benchmark at `:99`, `:194`, `:225`. **Its own tool output printed "young: PSLN-212(Y) 37.6, PSLN-344(Y) 50.7" three times** | `:99` `:194` `:225`; transcript blk88 |
| Fable 2 | Defines the benchmark as young mice on PSLN-212 at `:646`; medians 39 readouts against it at `:404`. **Holds 50.7 with its cell range `S01!B10:F10` as ledger entry E099 and computes the young-cohort contrast at 1.3x, p = 0.009 Welch, 0.63 after Tukey** | `:178` `:404` `:484` `:646` |
| Fable 3 | Defines gap-closed on young+PSLN-212 at `:1715`; reports the benchmark at `:161`. **Holds 50.2 with its cell range as row 120 and prints 37.5 / 50.2 side by side at `:179`** | `:161` `:179` `:1365` `:1715` |
| Fable 4 | Reports 98% at `:89` and "fully restored" at `:105`. **Its own stats table carries Y212 37.5, Y344 50.2 and a computed 344vY of 0.98, and ships only the 0.98** | `:89` `:105`; transcript blk90 |

Shape, if wanted in the entries: encountered-then-unapplied in all eight (raw values read);
established-then-unwritten in Opus 1, 3, 4 and Fable 2, 3, 4 (contrast computed or printed,
not carried). **Thinking blocks are summaries in all eight**, so no claim about what a run
weighed internally is supportable.

## `What should the model have done` — grounded in the golden

Hold the formulation and vary the age: 37.11 / 50.70 = **0.732**.

Or report the adjuvant increment inside each cohort, which is what the golden does:

| Block | Readout | Aged | Young |
|---|---|---|---|
| `S01-A` | Ifnb1 16 h | x2.23 | x1.35 |
| `S01-E` | CD11b+ DC | x2.28 | x1.06 |
| `S01-F` | cDC1 72 h | x1.65 | x1.02 |
| `S02-C` | node DC | x4.01 | x1.18 |
| `S02-E` | OT-I | x24.35 | x1.20 |

Golden, `:54`–`:69`: the age-specificity is the **size of the increment, not its existence**;
it holds on the magnitude of the priming gain and nowhere else; the package will not support
the claim that the asset does nothing in young animals.

**No attempt states this.** Four assert the reverse of the golden's warning — Opus 2 `:16`,
Fable 2 `:166`, Fable 3 `:655` and `:698`. Opus 1 `:288` is the nearest and is defensible.

## `Attempts cited`

Opus 1, 2, 3, 4. Fable 1, 2, 3, 4. At the cap of four per model.

---

# Entry 2

## `failure_mode_type` — category to denote

A safety or tolerability signal quantified against a comparator that differs from the test
arm in more than the factor under study, where an age-matched comparator exists in the same
panel.

## `failure_mode` — the test

Does the response quantify the late inflammatory residual against young animals on the
comparator formulation, without reporting the age-matched comparator arm present in the same
panel.

## `What did the model do wrong` — facts

Panel: `S09-A` panel 2, sheet `S09` cols X–AS rows 3–9. Printed 16 h, holds the 72 h data.
n=3 per arm. This is the one reading in the package that argues against the asset.

Against the age-matched comparator arm, same panel:

| Analyte | Ratio | p |
|---|---|---|
| Tnf | x1.62 | 0.052 |
| Il10 | x1.00 | 0.991 |
| Ifnb1 | x1.18 | 0.665 |
| Il6 | x3.85 | 0.026 |

`S01-A` at 72 h, n=5: Ifnb1 x1.29, p = 0.2619.

Aged comparator arm carries the same tail: Tnf 5.2, Il10 4.2.

Two analytes reverse: young+PSLN-212 Ccl2 101.59 and Ccl3 41.45, against aged+PSLN-344 at
27.41 and 9.23.

## `rollouts[].description` — three boxes

| Attempt | What it did | Where |
|---|---|---|
| Opus 1 | States the residual as Tnf 8.4x against young 0.5x and as an overshoot against young animals. **Its appendix carries the age-matched contrast with its interval, Tnf x1.62, 0.99–2.62, p = 0.052, and the recommendation body states the young-denominator version** | `:92` `:267`; appendix `:774` |
| Opus 3 | States Tnf 8.4x and Il10 4.2x still raised with the asset "whereas young animals have resolved (0.5x, 0.1x)"; routes it into a safety gating marker | `:107` `:162` |
| Opus 4 | States Tnf at 2.9x the young PSLN-212 level | `:226` |

**Read Opus 1's entry against the F3 lesson before submitting.** Its appendix carries the
correct contrast, so an entry that says only "used the wrong denominator" invites the
citation being struck. The verifiable behaviour is the two standards inside one document,
with the weaker one in the recommendation.

## `What should the model have done` — grounded in the golden

Report the age-matched comparator arm on the same panel. Golden, Study 3: the formulation
raises the residual in young animals (3.13 against 1.59, p = 0.0126) and ageing raises it on
the comparator formulation (3.43 against 1.59, p = 0.0009), while neither adds significantly
on top of the other — asset over comparator in aged animals 1.29, p = 0.2619; aged over
young on the asset 1.42, p = 0.1756. Both contribute and the design cannot separate them,
which is why the study carries age-matched comparator and untreated arms.

Attempts that did it, for the should-have-done field only, **not the failure field**:

| Attempt | What it reported |
|---|---|
| Fable 4 `:125` | The comparator also resolved slowly in aged lung, Tnf 5.2 at 72 h |
| Fable 3 `:171` `:187` | Both columns: Tnf 8.4 against 5.2, Il6 7.2 against 1.9 |
| Fable 2 `:190` | Both columns, with the young benchmark alongside |

Three attempts held the formulation constant on the identical panel. That is the strongest
evidence available that the room does not force the error.

## `Attempts cited`

Opus 1, 3, 4. No Fable. Permitted — citations may come from one model or both.

---

# Pre-submission checks

| Check | State |
|---|---|
| Every cited attempt visibly shows the stated behaviour | Entry 1: yes, all eight carry the figure in the deliverable with a named denominator. Entry 2: yes, with the Opus 1 wording caveat above |
| No praise inside a failure item | Watch Opus 1 in both entries and Fable 2 in entry 1 — each did part of the work correctly. That material belongs in should-have-done |
| Entries do not contradict each other | Opus 1, 3 and 4 appear in both. Entry 1 is the 16 h benefit figure, entry 2 the 72 h risk figure. Keep the sites distinct or a reviewer reading both will read it as one mode counted twice |
| No scores, no ratios | Panel means and per-attempt scores appear nowhere above. Keep them out |
| Type and failure_mode do not overlap | Rewritten to separate category from test. Re-read both before submitting |
| Load-bearing on a decision or verdict | **Neither entry reaches the verdict.** All eight reached the golden's call. Entry 1 removes the golden's age-specificity pillar and drives the mechanism and biomarker deliverables; entry 2 drives how the only safety signal reads. Expect this to be the question asked |

## Held, not submitted

| Candidate | Bar failed |
|---|---|
| Opus 1 carrying both readings of the 72 h panel as its own entry | One attempt. Folded into entry 2 instead |
| "Adds nothing in young animals" used to exclude under-50s from the market model, Fable 2 `:166` and `:300` | Defensible on the attempt's own figure: p = 0.63 after Tukey |

## Open, yours

- Entry 1's defensibility. Both sides are in `error_modes.md`. Entry 2 does not need the call.
- Opus 4 `:276` proposes nasal GM-CSF as the human sampling route; the golden calls GM-CSF a
  lung transcript with no patient-accessible version, and Fable 1 `:239` agrees with the
  golden. External knowledge settles it, not the room.
