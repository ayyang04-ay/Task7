# psql25c1 — error mode ledger, 16-run panel (v1, 2026-11-13)

Supersedes `fa/error_modes.md`, which analysed the 8-run batch `job_91694a59` against
the pre-rename-3 identifiers. Nothing in that file's trajectory IDs carries over.
The old file stays in place because HANDOFF §8 cites its Mode 1 tightening as the
source of the grader's B4 wording.

| Version | Change |
|---|---|
| v1 2026-11-13 | First ledger built on the two 2026-11-12 exports. Three modes ship; four candidates dropped with reasons. |

---

## Phase 0 — parse manifest

| Row | State | Detail |
|---|---|---|
| Run export located | PASS | `fa/exports/Anton_…_job_121a8283_2026-11-12.zip` and `…_job_af49afff_2026-11-12.zip`. sha256 prefixes `8e5abed6` and `f8230a9f`, matching HANDOFF §10 |
| Export complete | PASS | Both `job_info.json` carry the same `export_selection`: included `outputs`, `transcripts`, `grading`; excluded `task_files`, `grader_files`. Different jobs, not complementary halves — one job per model |
| Clusters present | PASS (with limit) | No `_ERROR.txt`. `task_files` and `grader_files` were not exported, so the data room as the runs saw it is reconstructed from the repo working tree, which `verify-rename.py` ties to v2. Both jobs ran against problem version `f3a468ce`, the version in the repo |
| Run map | PASS | Below. Attempt numbers are the export's own `attempt_NN`, not constructed |
| Run count and status | PASS | 16 runs, 8 per model. All `completed`, none refused, none truncated. No Trust & Safety voids |
| QA report | PASS | `qa_report_psql25c1_v2_f3a468ce.zip`, freshness row reads **fresh**, same problem version. Nothing STALE. Model coverage taken from the run map, not from QA |
| Golden | PASS | `task/golden-response.md`, the version `make-artifacts.py --check` and `audit-golden.py` both pass against |
| Data room | PASS | `audit-golden.py` re-run this session from `build/`: 246 checks, 0 mismatches, exit 0. `CORRESPONDENCE` 115/115 |
| Grading document | PASS | `task/grader-guidelines.txt`, 13 A items and 10 B items. **Graded mode, context only** — no mode below rests on it and no run is ranked by score |
| Stats availability | FAIL, waived | No scipy in this container. Nothing in this ledger needs a test beyond exact counts and ratios computed by hand |
| Thinking channel | PASS, limiting | All 16 carry `thinking_summary_status: ready`, so blocks are **summaries, not raw reasoning**. Text-bearing blocks per run: 51 to 87 of 61 to 130. **No claim about what a run weighed internally is supportable, which rules out the raised-then-abandoned shape for this panel before Phase 1.** Encountered-then-unapplied and established-then-unwritten remain available, from tool calls and deliverables |
| Deliverable present | PASS | `outputs/` is in both exports. Every run shipped a primary memo in Markdown, 36 to 100 KB, plus ledgers, figures and in most cases .docx/.pdf/.html twins |

### Two things to report rather than explain

1. **ClaudeScope gap.** `qa_jobs.json` records the ClaudeScope run as `itemCount: 4`, `findingCount: 8`, summary "8 clusters identified". Four clusters are not in the export. No explanation is available from the files.
2. **One ClaudeScope finding is contradicted by the export it describes.** `minor_grader_reasoning_truncated_in_metadata` says run `fe37920b` has no stored grader reasoning. The grading record for that run carries 5,038 characters of reasoning. Either the finding is wrong or the export was re-generated after it.

### Run map

| Label | Model | Attempt | Short hash | Job |
|---|---|---|---|---|
| Fable F1 | claude-fable-5-2 | 1 | `5e31f7bc` | 121a8283 |
| Fable F2 | claude-fable-5-2 | 2 | `58e064d2` | 121a8283 |
| Fable F3 | claude-fable-5-2 | 3 | `d2d19615` | 121a8283 |
| Fable F4 | claude-fable-5-2 | 4 | `fb6c88e7` | 121a8283 |
| Fable F5 | claude-fable-5-2 | 5 | `4a746b06` | 121a8283 |
| Fable F6 | claude-fable-5-2 | 6 | `bef8406c` | 121a8283 |
| Fable F7 | claude-fable-5-2 | 7 | `bd81877b` | 121a8283 |
| Fable F8 | claude-fable-5-2 | 8 | `6312fe94` | 121a8283 |
| Opus O1 | claude-opus-5-5 | 1 | `5701d39b` | af49afff |
| Opus O2 | claude-opus-5-5 | 2 | `fe37920b` | af49afff |
| Opus O3 | claude-opus-5-5 | 3 | `42462321` | af49afff |
| Opus O4 | claude-opus-5-5 | 4 | `3e85dbd2` | af49afff |
| Opus O5 | claude-opus-5-5 | 5 | `dcee42be` | af49afff |
| Opus O6 | claude-opus-5-5 | 6 | `cd72221b` | af49afff |
| Opus O7 | claude-opus-5-5 | 7 | `caffc26d` | af49afff |
| Opus O8 | claude-opus-5-5 | 8 | `a078ba5e` | af49afff |

### Reading coverage

| What | Which runs |
|---|---|
| Primary deliverable read in full | Opus O1 (`5701d39b`), Fable F1 (`5e31f7bc`), Opus O7 (`caffc26d`) |
| Deliverable read in the sections bearing on each candidate | all 16 |
| Searched for every candidate mode, two or more patterns of differing looseness, numeric probes in two or more spellings | all 16 |
| Grader rationale read in full | all 16 — as a candidate screen only. Every mode below was confirmed in the run's own deliverable before it entered the ledger |
| Transcript element census run | all 16 (`fa/transcript-extract.py`, retargeted) |

Numeric probes were run in both spellings throughout: `37.5`/`37.6`/`37.60`, `50.7`/`50.70`/`50.2`
(geometric mean), `0.98`/`0.987`/`99 %`, `20/28`/`20 of 28`, `32/42`/`32 of 42`. The
geometric-mean spelling matters: most runs report S01-A as geometric means, so an
arithmetic-mean-only probe misses them.

---

## Phase 1a2 — verdict map

| Run | Advance? | Decision rests on | Heterosubtypic set computed? | 72 h residual carried into the plan? |
|---|---|---|---|---|
| F1 | advance, gated | efficacy, challenge blocks | no | yes |
| F2 | advance, gated | efficacy, challenge blocks | no | yes |
| F3 | advance, conditional | efficacy, challenge blocks | no | yes |
| F4 | advance, one gate at a time | efficacy, challenge blocks | N1-inclusive only | yes |
| F5 | advance, conditional | efficacy, challenge blocks | mis-specified set | yes |
| F6 | advance, conditional | efficacy, challenge blocks | yes | yes |
| F7 | advance, conditional | efficacy, challenge blocks | yes | yes |
| F8 | advance, conditional | efficacy, challenge blocks | yes | yes |
| O1 | **no**, verify-or-terminate gate | integrity audit | yes | yes |
| O2 | **no**, confirm-or-kill | integrity audit | yes | **no** |
| O3 | advance, conditional | efficacy, with integrity caveat | no | yes |
| O4 | **no**, hold behind audit | integrity audit | no | **no** |
| O5 | **no**, do not advance now | integrity audit | no | yes |
| O6 | advance, conditional | efficacy, with integrity caveat | no | **no** |
| O7 | advance, gated | efficacy | yes | **no** |
| O8 | advance, confirm-and-de-risk | efficacy | yes | yes |

**The verdict is not the finding.** The advance/decline split traces to one earlier step:
whether the data-integrity findings gate the recommendation or sit beside it. Every
declining run is an Opus run that gates on the audit. That step is **not** a failure mode —
the prompt tells the solver the data "serves as ground truth" while the room contains the
contradictions, so both sides are defensible and the QA chain records the contradiction as
an environment Error. It is the same candidate the 8-run ledger rejected. It stays rejected.
See `calibration.md`.

---

## Phase 1c — coverage screen (block citations in the primary deliverable)

Screen only. Non-citation is not non-use; each apparent non-use below was checked against
the run's text before it was recorded.

| Block | Runs citing it | Note |
|---|---|---|
| S01-G | F4, O3, O5 | four-arm block |
| S01-F | F2, F4, F5, O3, O5 | four-arm block |
| S01-E | F1, F2, F3, F4, F5, O3 | four-arm block |
| S13-C | F2, F5, O2, O3 | |
| S15-B | F1, F2, F4, F5 | |
| S15-K | F1, F4, F5, O3 | |
| S03-L | F1, F4, O3, O5, O6 | |
| S05-E | F2, F3, F4, F5, O3, O5 | |
| S01-A | all 16 | four-arm block |
| S02-C / S02-E | 12 / 13 | four-arm blocks |

**The finding this screen produced.** The six blocks that carry all four arms — the only
blocks in the room where age can be varied with the adjuvant held constant — are
`S01-A, S01-E, S01-F, S01-G, S02-C, S02-E` (`audit-golden.py` asserts exactly these six).
S01-A is cited by every run; the three S01 blocks that would let the age claim be tested
are among the least-cited blocks in the whole room. That is Mode 1 seen from the other side.

---

## Phase 1d — the ledger

Ordered by prevalence first, consequence second. Prevalence was counted only to clear the
floor of two and is then dropped: the Runs cell names the runs, with no count and no ratio.

**Two modes ship.** A third candidate was built, tested and failed the floor; it is kept
below the ledger with its evidence rather than stretched to fit. Four further candidates
were dropped and are listed after it with reasons.

### Mode 1 — the age claim is measured against a different formulation

| Field | Content |
|---|---|
| Short name | Age and adjuvant varied together in the restoration metric |
| Class | Analytical — a comparison not corrected for a known covariate the room controls |
| Runs | F1, F2, F3, F4, F5, F6, F7, F8, O1, O2, O3, O4, O5, O6, O7, O8 |
| Not checked | that the aged-versus-young contrast changes the adjuvant as well as the age, in the six blocks that carry a young arm on the candidate formulation |
| Shape | encountered then unapplied in F2, F3 and O1, which hold the controlling value and do not use it; not retrieved in the rest |
| Graded? | A5 and B4, counted once by the grader |

**Description, in the task's own numbers and files.** `S01-A` (sheet `S01`, rows 3–10,
columns B–F) carries four arms on lung *Ifnb1* at 16 h, fold over untreated: aged+PSLN-212
16.64, aged+PSLN-344 37.11, young+PSLN-212 37.60, young+PSLN-344 50.70 (arithmetic means
of five animals; runs reporting geometric means give 16.5, 36.9, 37.5, 50.2). Every run
builds a restoration, age-gap or age-gap-closure figure whose denominator is the
**young+PSLN-212** arm, and reports that the candidate returns the aged response to the
young level — 0.98, 0.987, "98 % of the age gap", "99 %", "restored in full", "fully
age-restoring". The same denominator is then carried into the biomarker rationale, and in
several runs into a human go criterion. The block itself carries young+PSLN-344 at 50.70.
With the formulation held constant the aged response is **0.732** of young, not 0.98.
The same denominator appears on the 72 h panel of the same block, where the run reports
aged+PSLN-344 at 2.85× to 2.92× young, and the formulation-held ratio is 1.37×.

**Where it is visible.**

| Run | Position |
|---|---|
| F1 | memo §5 and the Table 2 restoration column; the 28-readout median "% of young" and Figure 3 right panel |
| F2 | memo §2.3; evidence-ledger row `I26` (the restoration index) while row `M1` of the same ledger holds young+PSLN-344 at 50.7, and row `M23` holds the within-cohort adjuvant effect it does not use |
| F3 | memo §2.3 numbered claim 2 and §2.4 Table 2 "344 as % of young"; the young+PSLN-344 value appears only in the ruled-out table, on the young-adult indication row |
| F4 | memo claim 4 in the executive summary, "0.98 of young"; the restoration-index table and Figure 3 |
| F5 | memo Table 2, restoration column; the summary claim that the aged lung "under-responds and manganese corrects it" |
| F6 | memo bullet 2 of the summary; the mechanism table row "Mn → interferon-β"; the biomarker table, "gap closed 98 %" |
| F7 | memo Table, innate row: 16.6 / 37.1 / 37.6 with restoration 0.98 |
| F8 | memo §mechanism, "returns the aged interferon response to the young level (99 %; CI 84–116)"; Figure 3's 24-readout spread |
| O1 | memo §1 bullet, §Table "restoration R = 0.98", §mechanism and the Study 3b human go criterion. **Also §mechanism bullet: "Mn still raises young Ifnb1 (50.2 vs 37.5-fold)" — the controlling value is in the deliverable and the restoration figure is unchanged** |
| O2 | memo §immunology, "GMR vs young = 0.98", "R = 0.98", and the biomarker claim "fully age-restoring: aged PSLN-344 equals young PSLN-212" |
| O3 | memo "What Figure 2 shows" — IFN-β at 16 h "98 % of young", monocyte recruitment 95 %, migratory DC 88 %; and the 72 h safety-marker row at "285 % of young" |
| O4 | memo "What does Mn restore?" and the Table restoration column; the index is written out as (aged344 − aged212) ÷ (young212 − aged212) |
| O5 | memo Table restoration column (0.980) and §4, "That equals the young value (37.5×; ratio 0.984, CI 0.837–1.16)" |
| O6 | memo §1 bullet 3, "restores IFN-β induction to the young level … restoration index 0.98 [I194]"; the biomarker table row |
| O7 | memo §1 bullets, "aged lungs make only 44 % of the young early IFN-β response … closes 98 % of the age gap"; the mechanism table; the biomarker table, "0.98, over-restored" |
| O8 | memo evidence row 8, "equal to young (37.5×; ratio 0.98)"; §mechanism, "Mn restores it exactly"; the biomarker table |

**Counterfactual.** Hold the formulation constant and vary the age: in `S01-A` at 16 h
aged+PSLN-344 over young+PSLN-344 is 37.11 / 50.70 = **0.732**. The comparison the room
supports without a confound is the adjuvant effect within each cohort, available in the
same six blocks: `S01-A` 16 h aged ×2.23 against young ×1.35; `S01-E` CD11b⁺ DC aged ×2.28
against young ×1.06; `S01-F` cDC1 72 h aged ×1.65 against young ×1.02; `S02-C` node DC
aged ×4.01 against young ×1.18; `S02-E` OT-I aged ×24.35 against young ×1.20. Six of the
seven panels rise in aged animals; the exception is the 72 h residual, where the young
gain is the larger (aged ×1.29, young ×1.97). A run that reports the adjuvant effect in
each cohort has the age-specificity claim without the confound.

**Exemplar.** None in this panel: every run carries the mode. The mode is nonetheless
avoidable — one of two fresh agents run against the repaired room in an earlier session
compared aged+PSLN-344 against young+PSLN-344 and reported the amplification as a property
of the chemistry rather than a correction of an aged deficit (recorded in
`fa/error_modes.md`; p = 0.0121 verified).

**Consequence.** Changes the mechanism claim, the biomarker rationale and, in O1, a
proposed human go criterion. It does not change any run's advance/decline verdict.

**Evidence.** [computed] all five S01-A arm means recomputed from `S01!B3:F10` this
session; `audit-golden.py` reproduces the within-cohort ratios (246 checks, 0 mismatches).
[transcript] the positions above, each read in the run's own deliverable.
[inference] that the biomarker rationale inherits the confound — stated by the runs
themselves, not inferred, in O2, O6, O7 and O8, where the restoration figure is the
biomarker's stated qualification.

**Plain-language restatement.** The room has four groups: old and young animals, each on
the new formulation and on the old one. To ask what ageing costs, compare old and young on
the same formulation. Every run instead compared old animals on the new formulation with
young animals on the old one, and reported that the new formulation brings old animals back
to a young response. On the comparison that holds the formulation fixed, old animals reach
about three-quarters of young. Three runs had the fourth group's number written down in
their own files and did not use it.

---

### Mode 2 — the last measured timepoint's residual is not carried into the safety plan

| Field | Content |
|---|---|
| Short name | Residual innate elevation at the last measured timepoint left out of the forward view |
| Class | Adjudication — conclusion-action gap |
| Runs | O2, O4, O6, O7 |
| Not checked | when the innate response returns to baseline, given that no timepoint beyond 72 h exists anywhere in the package |
| Shape | established then unwritten in O2, O4 and O6; not retrieved in O7 |
| Graded? | A11, with B3 for O2, O4 and O6 |

**Description, in the task's own numbers and files.** The second `S09-A` panel (sheet
`S09`, columns X–AS, rows 3–9) is headed 16 h and holds the 72 h data; every run in the
panel identified that and exponentiated the log10 scale correctly. In the aged
candidate arm at that timepoint, fold over untreated: Ccl2 27.41, Ccl3 9.23, Tnf 8.44,
Il6 7.19, Il10 4.16, Ifnb1 4.01, Ccl5 2.01. The young parent arm has resolved on two of
these — Tnf 0.48, Il10 0.11. No arm anywhere in the room carries a later timepoint.
O2 logs the elevation as a "reactogenicity flag" and calls it transient; O4 proposes only
re-measurement and extending a panel to 72 h; O6 lists it as a clinical risk and a
next-generation target. **O7 never retrieves the 72 h panel at all** — it cites `S09-A`
once, has no reference to a 72 h timepoint anywhere in the memo, and asserts "No
tolerability signal in mice at the dose that works." None of the four specifies a study
that measures when the response returns to baseline.

**Where it is visible.** Each run's next-studies section and its safety study: O2's S4
intranasal-Mn study, whose "must establish" is CNS Mn and repeat-dose tolerance; O4's
Study 6, scoped to olfactory, CNS and local toxicity; O6's IND-enabling row, scoped to
nasal, olfactory and CNS histopathology; O7's S3b GLP toxicology, in rat and a second
species for an Mn NOAEL. In all four the aged lung's own time-course is absent from the
endpoint list.

**Counterfactual.** Seven analytes sit above the untreated reference at the last measured
timepoint and no arm carries a later one, so the study that establishes the return to
baseline is fully specifiable from the room: the same analytes in aged lung at the
efficacious dose, sampled past 72 h, with a resolution criterion. F1, F2, F3, F4, F5, F6,
F7, F8, O1, O3, O5 and O8 all specified it, so it is not a stretch.

**Exemplar.** O1 — Study 4 samples cytokines at 6, 24 and 72 h with lung histopathology
at days 3, 7 and 28 and a go criterion of aged-lung inflammation resolved by day 7.
O8 carries the same as gate G3.

**Consequence.** Leaves the gating tolerability question out of the forward view. In O7 it
also leaves a positive safety claim standing against a contrary datum in the room that the
run never retrieved.

**Evidence.** [computed] all seven exponentiated values recomputed from `S09!AN3:AP9` and
the young parent arm from `S09!AQ3:AS9` this session. [transcript] positions above.

**Defensibility challenge, already raised and resolved — administrative note, not mode
text.** An independent rubric audit argued that inventorying resolution kinetics as a
caveat is defensible. The writer resolved it in favour of keeping the mode: the asset
cannot reach IND without the data, so a forward view that does not specify it leaves the
programme unable to file. HANDOFF standing decision 12 carries the full reasoning and the
sharpest counter-argument. One thing this panel adds in the mode's favour: most of the
panel proposed the work, named run by run in the counterfactual above, so the omission is
a choice rather than a property of the room. One thing it adds against: at 72 h the aged **parent** arm is at Tnf 5.23 and Il10
4.18, so non-resolution is substantially a platform property rather than something the
manganese introduces. That does not rescue the omission — the asset still needs its own
resolution data — but it is what a reviewer will raise.

---

### Candidate that does not clear the bar — matched-subtype blocks inside a pooled breadth estimate

**Not a mode. Recorded with its evidence so it is not re-raised as new, and so the writer
can see exactly where it died.**

| Field | Content |
|---|---|
| Short name | Matched-subtype challenges pooled into the estimate a cross-subtype claim rests on |
| Class | Synthesis, if it held |
| Clears the prevalence floor? | **No.** One run commits it unambiguously |

**The fact, verified.** The annotation's `S06-E` and `S06-F` entries for rows 71 to 105
state that those animals were immunised with the **bivalent** vaccine — CA09 H1N1 and
Aichi H3N2 — and challenged with PR8 H1N1 and Perth H3N2 respectively. Both challenge
subtypes are in the vaccine, so neither block is a cross-subtype challenge. The grader's
section C makes counting them toward the heterosubtypic set explicitly non-neutral.

**The one clear instance.** O6, memo §breadth: "The 3-day study (S15-H) and both
imprinting challenges are also heterosubtypic or antigenically distant", in the same
bullet that correctly sorts the ten aged experiments into six heterosubtypic, two
homologous and two with no stated challenge. The following bullet then asserts that in
"the heterosubtypic pairings" antibody to the vaccine HA cannot inhibit the challenge
virus, and the ruled-out table uses the imprinting study among the grounds for retiring
antibody as the mechanism. For the imprinting blocks that reasoning does not hold: the
vaccine contains both challenge HAs.

**Why no second run joins it.**

| Run | What it actually does | Verdict |
|---|---|---|
| F4 | Its primary versus-parent estimate is labelled "14 strata (10 experiments + 4 imprinting strata)", 84/100 against 13/101, and one executive-summary sentence joins that +71 figure to "across subtypes" language. But F4's dedicated Breadth section names the strict set — `S06-A`, `S06-B`, `S06-E`(1), `S06-G` — correctly, and F4 separately reports the six-block no-conflict set at 32/42 against 4/42 | Arguable, not clear. An expert defends a pooled all-strata effect estimate sitting beside a correctly scoped breadth section |
| F3 | Memo labels the imprinting blocks correctly (`H1N1+H3N2 → PR8 H1N1`, `H1N1+H3N2 → Perth H3N2`). The mislabel is in a supporting CSV only | Artefact, not the deliverable's claim |
| F5 | Memo labels them correctly, then reports a "mismatched-subtype" restriction of 56/70 — a denominator far larger than the 28 animals in the strict set, so the restricted set is mis-specified | A different error: a mis-specified set, not matched blocks counted as cross-subtype. Do not fold the two together |
| F1, F2, O3, O4, O5 | Rest a breadth claim on an all-challenge pool while naming the heterosubtypic blocks individually in a table | Presentational, and defensible. Widening the mode here would be pinged |

**The counterfactual, computed, kept because it is useful whatever happens to the
candidate.** The blocks whose challenge shares neither HA nor NA with the vaccine are
`S06-A`, `S06-B`, `S06-E` (rows 34–68) and `S06-G`: candidate 20/28 against parent 1/28.
Adding the two that share N1 only, `S06-C` and `S06-F`, gives 32/42 against 4/42. Both
still support advancing, so even if the candidate had held, it would change the strength
and specificity of the breadth claim and not any verdict. [computed] from the `S06` status
columns this session.

**What would revive it.** A second run that counts a matched-subtype block as
cross-subtype in its own deliverable, not in a supporting file. Screen the next batch for
exactly that sentence; do not relax it to "pooled an all-challenge estimate", which is the
version that eight runs here would satisfy and that an expert defends.

---

## Dropped candidates, with the reason

| Candidate | Where it came from | Why it is not in the ledger |
|---|---|---|
| **Proposing an adjuvant-alone or antigen-free arm the room already settles** | Pre-registered at the foot of `fa/error_modes.md` before this panel ran | **Not observed.** Fifteen of sixteen runs cite `S15-H` and retire the non-specific-antiviral alternative on it; O7 cites the same experiment by its own ledger ID. Where an adjuvant-alone arm is proposed (O4, O8) it is for attribution or tolerability, which the grader's own B10 wording exempts. The pre-registration worked: the shape was looked for and is absent |
| **The antigen-dose question never named as unanswerable** | A8; flagged by fourteen of the sixteen grader rationales | **Requirement basis fails.** Independently confirmed: the room holds each antigen at one dose throughout (0.5 µg HA for CA09, 1 µg for Aichi, nothing else), and zero of sixteen runs name the fixed antigen dose as a question the package cannot answer, on both a tight and a loose screen. But the prompt does not ask for an inventory of unanswerable questions, and an expert who proposes a licensed high-dose comparator as a standard-of-care benchmark has addressed the commercially relevant form of it. The requirement lives in the grading document. Goes to `calibration.md` |
| **Treating `S06-C` and `S06-D` as independent experiments** | B7 | **Not observed as a mode.** Every run identifies the 28-of-28 identity and excludes `S06-D` from its primary estimate. F6 and F7 do use `S06-D` inside a day-3 pool, but both disclose the identity in the same table, which an expert defends |
| **Reporting `S09-A` on a linear scale** | B2 | **Not observed.** Every run exponentiated correctly; the graders' own recomputations agree |
| **Integrity audit drives the recommendation** | Carried over from the 8-run ledger; it is the divergence point of this panel's verdict split | **Still a task defect, not FA material.** Same reasoning as before: the contradictions are real, each declining run verified them, and the prompt's "ground truth" wording is what puts the run in an unresolvable position. The QA chain records it as an environment Error, and the env_linter finding shows two graders acting on the ambiguity in opposite directions |

---

## Phase 1e — item matrix (internal only; nothing here reaches the FA)

Built from the grader rationales, which are a screen. Cells read from the rationale text,
not parsed from prose. `·` means the rationale does not resolve the item either way.

| Run | A3/A4 set | A5 | A8 | A11 | A13 | B4 | B3 | other B fired |
|---|---|---|---|---|---|---|---|---|
| F1 | partial | not met | mostly | met | met | fired | — | none |
| F2 | missed | missed | weak | met | met | fired | — | none |
| F3 | partial | not met | weak | met | met | fired | — | none |
| F4 | not met | not met | partial | met | · | fired | — | none |
| F5 | wrong set | not met | not stated | met | · | fired | — | none |
| F6 | partial | not met | partial | met | · | fired | — | B7 partial |
| F7 | met/mostly | not met | not met | met | · | fired | not fired | none |
| F8 | met | not met | weak | met | · | fired | — | B7 partial |
| O1 | met | missed | partial | met | met | fired | not fired | none |
| O2 | met | missed | met | **not met** | · | fired | **fired** | none |
| O3 | mostly | · | met | met | · | fired | — | none |
| O4 | not met | not met | not met | **not met** | · | fired | — | none |
| O5 | partial | not met | not framed | met | · | fired | not fired | none |
| O6 | partial | fails | weak | **fails** | · | fired | **fired** | none |
| O7 | met | not met | partial | **not met** | · | fired | n/a | none |
| O8 | met | · | not named | met | · | fired | — | none |

Summary: **A5 and B4 are the only items the whole panel fails.** A11 discriminates four
runs. A8 is failed or only partly met by every run, so it discriminates nothing — see
`calibration.md`. B1, B2, B5, B6, B8, B9 and B10 fired nowhere.

---

## Phase 1f — per-trajectory profile

| Run | Modes carried | Unique to it | Poor exemplar? |
|---|---|---|---|
| F1 | 1 | — | no; a clean exemplar for Mode 1's "% of young" form |
| F2 | 1 | — | **best exemplar for Mode 1's encountered-then-unapplied shape**: the controlling value is row `M1` of its own ledger and the within-cohort effect is row `M23`, neither used |
| F3 | 1 | labels the imprinting blocks correctly in the memo and mislabels them in a supporting CSV | no |
| F4 | 1 | pools four matched-subtype strata into its primary versus-parent estimate | no |
| F5 | 1 | a "mismatched-subtype" restricted set at 56/70, far larger than the 28 animals in the strict set | no |
| F6 | 1 | — | no |
| F7 | 1 | — | no |
| F8 | 1 | — | no |
| O1 | 1 | — | **best exemplar for Mode 1 overall**: the memo prints young+PSLN-344 at 50.2 and keeps R = 0.98, and carries the same benchmark into a human go criterion |
| O2 | 1, 2 | — | no |
| O3 | 1 | — | no |
| O4 | 1, 2 | — | no |
| O5 | 1 | — | no |
| O6 | 1, 2 | the one clear instance of the matched-subtype candidate below the ledger | no |
| O7 | 1, 2 | — | **best exemplar for Mode 2's not-retrieved shape**: no 72 h reference anywhere, and a positive tolerability claim |
| O8 | 1 | — | no; the cleanest statement of the heterosubtypic counterfactual, 20/28 against 1/28 and 32/42 against 4/42 |

**Tooling friction is not a mode and is not in the ledger.** ClaudeScope records two
environment gaps that every run worked around: no openpyxl-plus-lifelines in any single
conda env and no `file`/`unzip` CLI, and no document renderer at all, so no run could
visually check its own PDF or DOCX. Both cost time, neither caused a failure above.
Recorded here and in `qa_triage.md` as task notes.
