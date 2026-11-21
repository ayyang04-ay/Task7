# Explore log — lw0b5ba6 v2 panel

Descriptive only. Nothing here is labelled a failure mode; that call is the writer's.

## Panel

8 runs, problem version 3619eae7 (v2), prompt 006aa3ff6c6b which normalises to the same
text as `task/prompt.txt` (e75574f8f69a). Labels from `job_info.json` and `all_runs.csv`.

| Label | Model | Attempt | Short | Score |
|---|---|---|---|---|
| O1 | claude-opus-5-5 | 1 | `f295b831` | 0.93 |
| O2 | claude-opus-5-5 | 2 | `e8634c7e` | 0.87 |
| O3 | claude-opus-5-5 | 3 | `978e3829` | 0.90 |
| O4 | claude-opus-5-5 | 4 | `e7837212` | 0.92 |
| F1 | claude-fable-5-2 | 1 | `1e154279` | 0.95 |
| F2 | claude-fable-5-2 | 2 | `355880fe` | 0.94 |
| F3 | claude-fable-5-2 | 3 | `f644c65d` | 0.90 |
| F4 | claude-fable-5-2 | 4 | `c54ffab8` | 0.95 |

## Reading coverage

Each run's proposal read by section extraction and pattern search, not end to end.
Transcripts not yet read. Grader records read for the retired panel only. Counts below are
screens over the proposal text; where a count is zero the surrounding text was read to
check for the same content under another term.

## Decision points, from the revision 7 prompt

Deliverable components: verdict; asset selection; asset assessment; next studies and what
each must establish; the five per-study attributes (endpoints, populations, comparators,
readouts, timing); target demographic for the TAM check; MoA from the data; biomarkers;
what is forfeited on a drop; considered and ruled out.

Constraints: recommendation placed first; per-number provenance; objective stance;
grounded in the supplied data; as-of date.

Revision 7 changed two of these against the retired panel: the per-study ask now carries
all five attributes, and asset selection became an explicit ask rather than an inference.

## Divergence table

| Decision point | Approach | Runs | Model split | Unique in model | Golden | Matches golden? | Where |
|---|---|---|---|---|---|---|---|
| Verdict | Keep the programme, gated, no IND commitment released now, kill criteria fixed in advance | O1 O2 O3 O4 F1 F2 F3 F4 | mixed, all 8 | none | "Advance it." No gate structure and no conditions | Same direction by a different route: every run conditions the keep, the golden does not | each run §1 Recommendation |
| Asset selection | PSLN-344 as sole lead; PSLN-212 stopped as a candidate and retained as the Mn-free comparator | O1 O2 O3 O4 F1 F2 F3 F4 | mixed, all 8 | none | Treats PSLN-344 as the asset and PSLN-212 as the parent comparator; never frames a selection and never states 212 stops | Yes on which asset; the golden holds no position on retiring 212 | O1 §1; O4 §2 "Which asset? PSLN-344 vs PSLN-212"; F3 §3 "PSLN-344 or PSLN-212" |
| Asset selection, alternatives | No run selected PSLN-212; no run split the recommendation by population | — | — | — | — | — | pattern search for a population split returns 0 of 8 |
| Asset framing | States the data show an adjuvant rather than a stand-alone STING drug | O4 F1 F2 F3 F4 | all 4 Fable plus O4 | O4, the only Opus run taking it | Refers to "the adjuvant" 16 times and carries a section "What the adjuvant actually adds"; never uses stand-alone language because it never adopts the drug framing | Aligns with the golden's framing | F2 §1 "The data do not describe a stand-alone STING-agonist drug. They describe a vaccine adjuvant"; F3 §1 "The data do not support a stand-alone STING drug" |
| Asset framing | Does not address the prompt's stand-alone-drug description | O1 O2 O3 | Opus-only | — | as above | Leaves the prompt's framing unexamined where the golden works from the adjuvant framing | O1, O2, O3 §1 and §2 |
| Five per-study attributes | Uses "readout" as a named per-study item, 10 to 22 occurrences | O1 O2 O3 O4 F3 | mixed | F3, the only Fable run taking it | Golden's next-study entries carry the labels Establishes, Endpoints, Population, Comparators, Readouts, Timing | Yes | O2 §6; O3 §6; F3 §6 |
| Five per-study attributes | No occurrence of "readout" anywhere; per-study detail carried under other column names | F1 F2 F4 | Fable-only, 3 of 4 | — | as above | Four of the five attributes are named; Readouts is not a distinct item | F1 §8 table columns are Study, Question it must answer, Population, Comparators, Primary endpoint, Timing; F2 §2 Gates table is Gate, When, Question, Passed if, If not |
| Target demographic | Segmented demographic section present | O1 O2 O3 O4 F1 F2 F3 F4 | mixed, all 8 | none | No demographic or segment section. "65-plus" asserted three times, derived nowhere | All 8 carry content the golden does not | O1 §6; O2 §7; O3 §5; O4 §7; F1 §7; F2 §5; F3 §5; F4 §4 |
| Target demographic | Does not use the term TAM although the section is present | F3 F4 | Fable-only | — | — | — | F3 §5 "Target population, for the market-research check"; F4 §4 "Target demographic for the market-size check" |
| Data integrity | A register or dedicated section, not asked for by the prompt | O1 O2 O3 O4 F1 F2 F3 F4 | mixed, all 8 | none | No integrity content: zero occurrences of integrity, defect, duplicate, contradict, mislabel or rotated | All 8 carry content the golden does not | O1 §3 and App. A; O2 §3 and App. B; O3 §2.5 and App. A; O4 §2.5; F1 §10; F2 App. A; F3 §9; F4 §2.5 |
| Forfeited on a drop | Dedicated section or subsection | O1 O2 O3 O4 F1 F2 F3 F4 | mixed, all 8 | none | No drop-branch content: zero occurrences of give up, giving up or forfeit | All 8 carry content the golden does not | O1 §8; O2 §8; O3 in §1; O4 §1.4; F1 §4; F2 §6; F3 §7; F4 §6 |
| Considered and ruled out | Dedicated section | O1 O2 O3 O4 F1 F2 F3 F4 | mixed, all 8 | none | "Considered and ruled out" section present | Yes | each run's own section |
| Recommendation placed first | §1 is the recommendation | O1 O2 O3 O4 F1 F2 F3 F4 | mixed, all 8 | none | "Recommendation" is the golden's first section | Yes | each run §1 |

## Patterns the skill asks to surface

**All runs differ from the golden.** Four decision points where inter-run comparison sees
no divergence because every run shares the approach, and the approach differs from the
golden.

| Decision point | What all 8 do | What the golden does |
|---|---|---|
| Verdict | condition the keep on gates with pre-set kill criteria | "Advance it.", unconditional |
| Data integrity | carry a register, unprompted | carries none |
| Forfeited on a drop | dedicated section | carries none |
| Target demographic | segmented section with sizing guidance | asserts 65-plus three times, derives it nowhere |

**Same verdict, different route.** All 8 reach the golden's direction on the asset and keep
the programme, by a route the golden does not take: every run routes the decision through
a data-integrity gate first.

**Cross-model pairs.** The asset-framing split is the closest to the pattern the client
prefers, though it is 5 against 3 rather than a pair: O4 is the only Opus run stating the
adjuvant reframe, which all 4 Fable runs state. The inverse grouping, O1 O2 O3, is
Opus-only.

**Deliverable vs own transcript.** Not assessed. Transcripts not yet read.

## Not yet covered

MoA and biomarker approaches are not yet clustered. Provenance, objectivity, grounding and
as-of-date handling are not yet assessed. No numeric recomputation against the workbook
has been run for this panel.
