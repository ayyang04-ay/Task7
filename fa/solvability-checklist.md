# psql25c1 — solvability grading checklist

**Written and committed before any solvability report exists.** The point of
pre-registering it is that a checklist written after the reports land is fitted to
them. Check the git log: if this file's commit is not earlier than the reports, it is
worthless and should be rewritten from the brief alone.

Scope: the two independent solvability agents run against the shipped room on
`claude/exciting-cray-mkihzd-v3` after rename 3. Each gets `task/prompt.txt` plus the
two data-room files and no answer key, and returns a full analysis plus a derivation log
marking every question DERIVED / BLOCKED / AMBIGUOUS.

---

## The pass rule

**A leg counts as solvable if at least one agent derives it.**

**An agent reaching a different conclusion from the golden is not a failure.** Only an
underivable leg is. Twice already a solvability agent has been right and the golden
wrong — the age-specificity claim and the `S15-H` seventh configuration were both
corrected on an agent's objection. A disagreement is a finding to adjudicate against
the mounted data, not a mark against the agent.

**A leg BLOCKED by both agents is the stop condition.** It means the room is not
solvable as shipped and nothing gets resubmitted until it is fixed.

Three verdicts, and they are not equally informative:

| Verdict | Means | Action |
|---|---|---|
| DERIVED | reached from mounted facts, with the basis stated | leg passes |
| BLOCKED | the agent judges no mounted fact supports it | if both agents, STOP; if one, record which fact the other used |
| AMBIGUOUS | mounted facts admit more than one reading | check against the exclusions below before treating it as a defect |

---

## Route-necessary legs

All 23 from `build/anton-brief-psql25c1.md` section 3. Every correct route must
establish each of these whatever method it uses, so a leg no agent can reach is a
broken room rather than a hard one.

| # | Claim the agent must reach | Mounted basis | What counts as DERIVED |
|---|---|---|---|
| 1 | indicator 1 means death, not survival | joint distribution: 1 at d2-12, 0 only at a block's last day | states the coding and the evidence for it, not just the convention |
| 2 | which blocks are heterosubtypic | annotation, classified by the solver | names the set and the strain-to-subtype reasoning behind it |
| 3 | candidate and comparator differ only by the Mn complex | annotation, Materials | states the single composition difference |
| 4 | the heterosubtypic set is derived, not asserted | `S06-D` collapses into `S06-C` on 28 of 28; rows 69-70 excluded as within-subtype | each block retained, collapsed or set aside on a stated fact |
| 5 | `S06-G` read against its own ceiling | `S06` rows 34-68, fifth arm, 3 events against 1 and 0 concurrent | cites the fifth arm; retaining or setting aside are both fine |
| 6 | the fifth arm of `S06-E/F/G` got neither vaccine nor challenge | annotation | states it from the annotation, not inferred from the numbers alone |
| 7 | protection exists at d2-d3 | `S06-B`, `S03-J` | locates the early separation |
| 8 | that early protection is not antibody-mediated | timing, naive animals, external kinetics | names the timing argument |
| 9 | the aged/young diagonal varies two things | `S01-A` rows 9 and 10 carry both young arms | identifies the fourth arm |
| 10 | the within-age adjuvant effect is the clean comparison | `S01-A`, `S01-E`, `S01-F`, `S01-G`, `S02-C`, `S02-E` | computes within-age, or explicitly holds formulation constant instead |
| 11 | endpoint direction established before pooling | 18-endpoint set; 2 invert | states direction per endpoint, or declines to pool and says why |
| 12 | age-matched and young give opposite reads | 18 endpoints, unanimous | reports the unanimity or the per-endpoint set |
| 13 | all immunoassays are homologous-antigen | annotation, antigen per assay | states it from the annotation |
| 14 | antigen-independence across five immunogens | `S03-I`, `S06-A`, `S06-C`, `S03-J`, `S02-E` + annotation | enumerates more than one immunogen |
| 15 | the effector chain established by blockade | `S11-C`, `S02-H`, `S02-I`, `S07-B`, `S05-C` | reaches the blockade experiments, not correlation alone |
| 16 | second `S09-A` block is the 72h panel | Ifnb1 4.01 against `S01-A` 72h; block 1 at 36.3 against 16h | identifies the mislabel and says how |
| 17 | `S09-A` is log10 | sheet header; PBS arm exponentiates to 1.00 | exponentiates, by either route |
| 18 | all seven analytes unresolved at 72h | block 2 exponentiated | reports all seven, not one |
| 19 | non-resolution is a formulation property | young+candidate 3.13 against young+comparator 1.59 | makes the within-young comparison |
| 20 | tolerability assays carry controls | `S08-D` comparator+R848, `S03-E` cholera toxin | names a positive control |
| 21 | dose at plateau | `S08-A` | reads the dose-response |
| 22 | no accessible antigen-independent marker | enumeration by compartment | separates peripherally accessible from lung-local |
| 23 | no per-animal immune-to-outcome linkage exists | survival blocks carry only time and event | states the absence |

### Legs resting on the annotation alone — the highest-stakes rows

**Legs 2, 3, 6 and 13.** Known risk 4 in the brief: a thin or ambiguous annotation here
breaks the protection and carry-forward pillars rather than making them hard. These are
also the legs most exposed to rename 3, because the rename touched 188 strings in the
annotation. **A BLOCKED or AMBIGUOUS verdict on any of these four is the most serious
result this sweep can return and is treated as blocking even from one agent.**

### Conditional legs

Bind only if the agent uses the readout. BLOCKED here is not a failure unless the agent
used the readout and still could not establish the leg.

- `S06-C` identical to `S06-D`
- the subclass panel inconsistent with the direction forced
- the HAI sham estimate below assay floor
- Tfh:Tfr an algebraic transform

---

## Pre-declared exclusions

AMBIGUOUS or adverse comment on any of these is **expected and is not a defect**.
Declared here so it cannot be decided after reading a report.

From HANDOFF section 1: the workbook's internal contradictions generally; both `S09-A`
headers reading 16h; `S06-D` duplicating `S06-C`; `S15-L` and `S15-N` carrying no stated
challenge virus; the unlabelled region at `S08` rows 89-101; no timepoint past 72h; no
HA dose-ranging; no per-animal link between an immune measure and an outcome.

Also: the stated-n values that disagree with their own observation counts; the `S10-A`
block holding `S03-E` content; the `S06` sheet's two printed labels that each appear
twice; the `NP366-374` tetramer against the stated BALB/c strain; the GM-CSF route
inconsistency; the OVA ug/ul inconsistency.

**And specifically, known risk 8:** `S05-A`'s immunogen is irreducibly ambiguous and the
ambiguity reaches endpoints 12, 13 and 18. Nothing in the source resolves it, so no
agent can. An agent naming that ambiguity is **correct**, and the brief records that
this is variance rather than difficulty and must not carry a failure mode.

**Correct observations that must not be marked down**, per HANDOFF section 9: that the
adjuvant also raises the young response, and that `S15-H` is a seventh favourable
configuration. Both corrected the golden.

---

## What this sweep is not for

- **Not scoring.** Standing decision 3: the mean-score gate is deprecated.
- **Not reference auditing.** A numeric disagreement between an agent and the golden
  routes to the reference auditor, which recomputes independently and does not treat
  `build/audit-golden.py` as authority. Do not resolve a number from a solvability
  report alone.
- **Not a panel.** Two subagents spawned from one parent context share conditioning and
  are not independent samples in the sense panel geometry requires. This is a ceiling
  test — is the leg derivable at all — and agreement between the two is not evidence
  about prevalence. Nothing in the FA may rest on it.

## Recording

For each leg: verdict per agent, the mounted fact each cited, and whether it matches the
basis column above. A leg DERIVED from a *different* mounted fact than the brief
predicts is a pass and worth noting — it means the anchor is legible under more than one
extraction strategy, which is what the brief's build constraints ask for.
