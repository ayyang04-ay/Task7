# psql25c1 — error mode ledger

**Identifiers in this file have been renamed twice since the panel ran.** The 8-run
batch below saw the source programme's published compound names; those became
`AVB-101` in rename 2 and `PSLN-212` in rename 3. Quoted trajectory text has been
updated to the current identifier so it matches the shipped room, so a quotation here
is not verbatim at the compound name. The analysis a solver does is unchanged. See
HANDOFF section 7 for both mappings and section 9 on why a new batch supersedes these
trajectory IDs.

Panel: 8 runs, job 91694a59. Mode: graded, but per 2026-11 guidance the grading
document is context only; no mode below rests on it and runs are not ranked by score.

**Reading coverage.** Attempts 03 and 04 read end to end (deliverable rebuilt from
transcript file operations; `outputs/` is excluded from this export). All 8 searched
for each candidate mode with multiple patterns of differing looseness and differing
numeric spellings. Every count below was confirmed by reading the matched text.

**Thinking channel.** All 8 carry `thinking_summary: {status: ok}`, so the blocks are
summaries, not raw reasoning. 58 to 94 of 59 to 96 blocks per run hold text. No claim
about what a run weighed internally is supportable, which rules out the
raised-then-abandoned shape for this panel.

---

## Mode 1 — age and adjuvant confounded in the restoration metric

| Field | Content |
|---|---|
| Class | measurement not corrected for a known covariate |
| Trajectory IDs | a006995a, 16a5e37f, 5c73bcfd, 10d15660, 1bbadcbf, 53d28969, d4235306, b359fc9d |
| Not checked | that the aged-versus-young contrast varies the adjuvant as well as the age, in blocks that carry a young arm on the candidate adjuvant |
| Shape | encountered then unapplied |

**Description in the task's own numbers and files.** S01-A, S01-E, S01-F, S01-G, S02-C and S02-E each
carry four arms: aged+PSLN-212, aged+PSLN-344, young+PSLN-212 and young+PSLN-344. Every
run built a quantitative age-gap-closure or restoration metric whose denominator is the
young+PSLN-212 arm, so the numerator differs from the denominator in both age and
adjuvant. Every run referenced the young+PSLN-344 arm (100 or more references each) and
pulled its values, 50.70 at 16 h and 3.13 at 72 h in S01-A.

**Where it is visible.**
- 5c73bcfd, elements 366 and 440: states the convention outright, that "Young" always
  means the animals given the Mn-free parent liposome. Its own ledger row M23 is the
  within-adjuvant comparison and is not cited in the deliverable. Element 375 carries the
  resulting claim, aged IFN-beta reaching the young level at 36.9 against 37.5.
- 10d15660, element 161: defines age-gap closure as (PSLN-344 − PSLN-212) divided by
  (PSLN-212(Y) − PSLN-212). The mode is in the metric definition, not the prose; a
  prose-only screen returns zero for this run.
- 16a5e37f, element 366 row L22: computes the age-by-formulation interaction, 1.66 with
  CI 1.33 to 2.08, from all four cells. Element 347 then states that ageing cuts the
  response to 44 percent of young and Mn brings it back to 99 percent.
- a006995a, 1bbadcbf, 53d28969, d4235306, b359fc9d: same denominator, confirmed by
  reading each run's metric definition.

**Counterfactual.** Holding the adjuvant constant, aged over young is 0.732 at 16 h, not
the 0.987 the cross-adjuvant contrast gives. At 72 h the young+PSLN-344 arm is itself 3.13
against 1.59 for young+PSLN-212, so most of the persistence attributed to the aged lung
is a property of the formulation. The within-age adjuvant effect, 2.23-fold in aged
animals against 1.35-fold in young, is available in the same block and is not confounded.

**Consequence.** Changes the mechanism claim, the biomarker rationale and, in several
runs, the safety reasoning about persistence.

---

## Mode 2 — mislabelled 72 h panel identified, then no resolution work proposed

| Field | Content |
|---|---|
| Class | finding recorded as a caveat where the prompt asks for work |
| Trajectory IDs | a006995a, 16a5e37f, 5c73bcfd, 10d15660, d4235306, b359fc9d |
| Not checked | when the innate response returns to baseline, given no timepoint past 72 h exists anywhere in the package |

**Description.** All 8 runs identified that the second S09-A block holds the 72 h data
despite its 16 h header, and exponentiated the log10 values correctly. The prompt asks
what the next studies have to establish. These six runs record the 72 h elevation as a
reactogenicity or persistence caveat and propose no study of its resolution.

**Where it is visible.** Each run's next-studies section; the 72 h material appears in the
caveat or safety text rather than in any study specification.

**Excluded from the count.** 1bbadcbf and 53d28969 carry resolution-gate language, a
day-7 or day-28 criterion, so the omission is not clean for those two.

**Counterfactual.** Seven analytes sit above the untreated reference at the last measured
timepoint, Ccl2 27.41, Ccl3 9.23, Tnf 8.44, Il6 7.19, Il10 4.16, Ifnb1 4.01, Ccl5 2.01,
and no arm carries a later one. The study that establishes the return to baseline is
specifiable from that alone.

**Consequence.** Leaves the gating tolerability question unaddressed in the forward view.

---

## Rejected candidate — integrity audit drives the recommendation

Present in b359fc9d, 16a5e37f, 53d28969, 10d15660, d4235306, a006995a, so it clears the
prevalence floor comfortably. **It fails the defensibility bar and must not ship as a
mode.** The workbook does contain the contradictions the runs found; each run verified
them; a careful expert who found an identical duplicate survival table, reused weight
trajectories and rotated subclass labels would raise them. The prompt's instruction to
treat the data as ground truth is what puts the run in an unresolvable position, and the
QA chain records this as an environment Error against all 8 runs rather than a model
failure.

This is a task defect, not FA material.

---

## Pre-registered candidate for the next batch — not yet observed

**Proposing an experiment the data room already contains.**

Registered here before the next panel runs so it cannot be read back into the
transcripts after the fact. **No count, no trajectory IDs: this has not been looked
for yet.** The 8-run panel above was analysed before S15-H was identified, so its
transcripts were never screened for this shape and the ledger above must not be read
as evidence either way.

| Field | Content |
|---|---|
| Class | forward-looking recommendation duplicating an experiment already in the data |
| Shape | gap asserted where the room closes it |
| Screen on | the next-studies section, for an adjuvant-alone or no-antigen arm |

**What the data says.** S15-H carries, at the 3-day interval, adjuvant alone,
vaccine alone and the combination. Adjuvant alone kills every animal, 0 of 7, with
deaths on days 5, 5, 6, 6, 6, 7 and 8. Vaccine alone also loses all 7. The
combination gives 6 of 7, a single death on day 12. A non-specific antiviral state
left by STING activation protects nobody, so the alternative is excluded by the
mounted data.

**The error shape.** A solver reads the day-3 cellular readouts, correctly notes they
sit inside the window where innate effects dominate, concludes the mechanism is
unresolved, and specifies an adjuvant-alone arm to settle it. Every step of that
reasoning is sound except the conclusion, which the room already answers. The cost
is a study arm spent on a closed question.

**Why it is worth screening for.** It is method-based and reproducible: either the
response proposes an antigen-free or adjuvant-only arm, or it does not. It does not
require reading intent, which is what rules out the raised-then-abandoned shape for
this panel.

**What would disqualify it.** A solver that cites S15-H and still proposes the arm
for a different reason, such as powering or a different interval, has not made this
error. A solver that leaves the mechanism open without proposing the arm is a weaker
and separate case; do not fold the two together. If it fails the two-trajectory floor
in the next batch, drop it rather than stretching the definition.

---

## Refinement to mode 1, from a post-repair solvability run

Two fresh agents were run against the repaired data room with no access to the
answers. One of them did **not** commit mode 1, which matters twice over: it confirms
the mode is avoidable rather than forced by the data room's layout, and it shows the
screen as written would have misclassified it.

That run compared aged+PSLN-344 against **young+PSLN-344**, holding formulation constant
and varying age, and reported "the amplification is also present in young animals
(PSLN-344(Y) 50.7 vs PSLN-344 aged 37.1, p = 0.012), i.e. it is a property of the
chemistry, not a correction of an aged deficit." Verified: p = 0.0121.

That is a clean comparison. It is a different clean comparison from the golden's,
which holds age constant and varies formulation, but it is not the confounded one.

**Screening rule, tightened.** Mode 1 is the use of a denominator that varies age and
adjuvant together, i.e. a metric built on aged+PSLN-344 over young+PSLN-212. A run
that compares aged+PSLN-344 against young+PSLN-344 has held formulation constant and has
**not** committed mode 1, even though it is comparing across age. Check the denominator
of the metric, not whether the word "young" appears. Two of the eight trajectories in
the ledger above were identified from a metric definition rather than from prose, so
this distinction decides counts.

**Consequence for the golden, not for the mode.** The run's substantive point was
correct and the golden was wrong: it had claimed the asset is "a correction of an
age-specific priming deficit, not a general potency increase". PSLN-344 raises Ifnb1
significantly in young animals too (50.70 against 37.60, p = 0.014). What is
age-specific is the size of the increment. The golden has been corrected. A solver
making the same observation is right and must not be marked down for it.
