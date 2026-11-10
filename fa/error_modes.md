# psql25c1 — error mode ledger

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
carry four arms: aged+nanoSTING, aged+AMnESTI, young+nanoSTING and young+AMnESTI. Every
run built a quantitative age-gap-closure or restoration metric whose denominator is the
young+nanoSTING arm, so the numerator differs from the denominator in both age and
adjuvant. Every run referenced the young+AMnESTI arm (100 or more references each) and
pulled its values, 50.70 at 16 h and 3.13 at 72 h in S01-A.

**Where it is visible.**
- 5c73bcfd, elements 366 and 440: states the convention outright, that "Young" always
  means the animals given the Mn-free parent liposome. Its own ledger row M23 is the
  within-adjuvant comparison and is not cited in the deliverable. Element 375 carries the
  resulting claim, aged IFN-beta reaching the young level at 36.9 against 37.5.
- 10d15660, element 161: defines age-gap closure as (AMnESTI − NanoSTING) divided by
  (NanoSTING(Y) − NanoSTING). The mode is in the metric definition, not the prose; a
  prose-only screen returns zero for this run.
- 16a5e37f, element 366 row L22: computes the age-by-formulation interaction, 1.66 with
  CI 1.33 to 2.08, from all four cells. Element 347 then states that ageing cuts the
  response to 44 percent of young and Mn brings it back to 99 percent.
- a006995a, 1bbadcbf, 53d28969, d4235306, b359fc9d: same denominator, confirmed by
  reading each run's metric definition.

**Counterfactual.** Holding the adjuvant constant, aged over young is 0.732 at 16 h, not
the 0.987 the cross-adjuvant contrast gives. At 72 h the young+AMnESTI arm is itself 3.13
against 1.59 for young+nanoSTING, so most of the persistence attributed to the aged lung
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
