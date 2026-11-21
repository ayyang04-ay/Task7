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

---

# MoA and biomarker clustering

Coverage: each run's MoA and biomarker sections read directly. Screens re-run with two or
more spellings where a figure is involved, and every zero-hit row was checked by reading
the surrounding text. Two of my own screens gave false signals and are corrected below.

## MoA: two clusters, and they follow the model

**Cluster A. Tabulated chain with a per-link evidence-type column.** O1 O2 O3 O4. Opus-only,
all four.

| Run | Column that labels evidence strength | Example value |
|---|---|---|
| O1 | Table 4 titled "Interventional (causal) evidence", columns Intervention, Readout, Control, Change, p, Block | "Test: carbenoxolone vs saline (PSLN-344) ... 7.3 -> 3.1, -58%, 0.0041, S11-C" |
| O2 | Table 4 "Mechanism claims and the strength of the supporting evidence"; figure legend reads "Dashed boxes = correlative or inferred steps that need confirmation" | seven-step chain |
| O3 | "Type of evidence" | "Causal (genetic)" |
| O4 | "Evidence type; confidence" | "Genetic KO; moderate" |

**Cluster B. Prose chain, no per-link evidence-type column.** F1 F2 F3 F4. Fable-only, all four.

| Run | Opening | Block citation at the link |
|---|---|---|
| F1 | "In one paragraph" plus Figure 5 | no |
| F2 | prose plus "Source blocks for every number are in Table 7" | in an appendix table |
| F3 | "In short:" plus Figure 4 | partly inline, e.g. S07-A, S04-D |
| F4 | "Mechanism in one paragraph." | no |

All eight present the same chain: surfactant-dependent uptake, STING sensing with Mn2+
raising the ceiling, IFN and GM-CSF, CCR2 monocyte recruitment, moDC conversion, node
migration, Tfh and GC, CD8 effector and memory. The clusters differ in presentation and in
where the intervention blocks are cited, not in the chain's content.

Intervention-block citation density, as a screen over the whole proposal:

| | O1 | O2 | O3 | O4 | F1 | F2 | F3 | F4 |
|---|---|---|---|---|---|---|---|---|
| carbenoxolone / CBX | 3 | 1 | 3 | 1 | 1 | 4 | 2 | 0 |
| IFNAR | 6 | 12 | 7 | 3 | 0 | 3 | 1 | 0 |
| S11-C | 2 | 2 | 1 | 1 | 1 | 3 | 5 | 0 |
| S02-H | 4 | 7 | 1 | 1 | 1 | 4 | 7 | 1 |
| S05-C | 4 | 4 | 1 | 0 | 1 | 5 | 9 | 1 |

F4 carries the IFNAR and GM-CSF rescue step in prose ("a step that needs the interferon
receptor and is rescued by GM-CSF") without naming IFNAR or the block. F1 likewise carries
CCR2 and the GM-CSF dependency in prose without block citations at those links.

Golden, last: two sections, "What is driving the protection" and "What the adjuvant actually
adds". It states the chain and names the blockade experiments. It carries no evidence-type
column.

## Biomarkers

**Correction to my own screen.** A pattern keyed to the golden's vocabulary (peripherally
accessible, bronchoscopy, lavage, invasive) returned 0 for O2 O3 O4 and 1 for O1, which was
a false signal. Reading the sections shows all four Opus runs handle human measurability
explicitly:

| Run | How it handles human measurability |
|---|---|
| O1 | "For human use, each needs an accessible matrix: nasal lining fluid, nasal brushings or blood"; column "Human-measurable analogue" |
| O2 | one of three stated selection criteria, "whether it can be measured in people"; column "Human analogue" |
| O3 | column "Proposed human / large-animal measure", naming nasosorption |
| O4 | one of three stated criteria, "whether the same measurement can be taken in people"; column "Human sampling" |

So all eight separate what can be measured in people from what cannot. The approach is
shared; the vocabulary differs.

**Tiering.** All eight tier the markers by time or by role. O1, O2, O3 and O4 use an explicit
Tier column (PD / target engagement, mechanism, adaptive output). F2 and F4 fold biomarkers
into the MoA section. F1 and F3 give a separate section.

**The per-animal limit.** O2 and O4 state that the immune and survival readouts come from
different animals, so no readout is yet a correlate of protection:

- O2: "Biomarkers and survival come from different animals, so these are regimen-level
  markers, not validated individual correlates of protection."
- O4: "Our immunology and survival readouts come from *different animals*, so no readout can
  yet be called a correlate of protection."

The golden states the same limit, in its next-studies section: readouts should be taken "on
the same animals so the immune measure and the outcome are linked per animal, which nothing
in the current package does."

**Antibody role.** A screen for antibody being assigned to immunogenicity or a regulatory
bridge rather than to cross-subtype efficacy returned 0 across all eight. The pattern was
keyed to the golden's wording and is not reliable; the surrounding text has not yet been
read run by run. Not resolved. HAI is named 4 to 85 times depending on the run (F4 4, O4 15,
F1 21, O3 25, F2 27, O1 30, O2 35, F3 85).

## Young-benchmark screen

Reported as positions only. What it means is the writer's call.

The restoration claim on Ifnb1 at 16 h compares an aged PSLN-344 value of about 36.9 to a
young reference. S01-A holds young PSLN-212 at 37.60 and young PSLN-344 at 50.70.

| Run | Restoration figure stated | References a young PSLN-344 arm anywhere | Cites 50.70 | Where |
|---|---|---|---|---|
| O1 | 0.98 / 0.99, 10 occurrences | 6, all to survival blocks S09-B/D/F | no | §5 Table 5 row "Ifnb1 (lung) ... 36.9 ... Young PSLN-212 37.5" |
| O2 | 1 occurrence | 5, incl. S15-M / S09-E weight comparison | no | §4 Table 4 |
| O3 | "equal to young (S01-A)" | **0** | no | §3 step 2, "Ifnb1 at 16 h is 36.9x vs 16.5x, equal to young (S01-A)" |
| O4 | "matches young level (restoration 0.98)" | 1, to S13-E survival | no | §5 Tier A row |
| F1 | "Mn2+ brings it to 99%" | **0** | no | §5, "In old lungs given PSLN-212 this burst is 44% of the young response; Mn2+ brings it to 99%" |
| F2 | 2 occurrences | 2 | **3** | §4.1 and the S02-I row |
| F3 | 0 | 6, incl. S09-F survival | no | §4 |
| F4 | 1 occurrence | 2, incl. the d180 recovery comparison | no | §3 |

No run uses a "formulation held constant" or "within-formulation" phrasing. **F2 is the only
run citing 50.70.** O3 and F1 state the restoration claim and reference no young PSLN-344 arm
at any point in the deliverable.

**Correction to my own screen.** O1's single "0.73" hit is an effect-size value in an S13-C
table row, not a formulation-held ratio. No run cites 0.732.

Golden, last: "Ifnb1 at 16 hours reads 0.99 of young on the diagonal, which looks like a
match. Holding formulation constant it is 0.73." The golden also tabulates young PSLN-344 at
50.70 against aged PSLN-344 at 37.11 in its seven-panel table.

---

# Antibody role: the row left unresolved, now closed

Coverage: all eight biomarker sections read line by line for antibody content. The earlier
screen was keyed to the golden's wording and returned 0 across the panel; that result is
withdrawn. Screened again on HAI, IgG, antibody, neutralis/neutraliz, titre/titer, and the
matched text read.

## Clusters

**Cluster 1. Antibody assigned to immunogenicity or a regulatory role.** O2 O4 F1 F2.

| Run | Label it gives antibody | Where |
|---|---|---|
| O4 | "HAI and microneutralisation (homologous strains)" with the role "Registrational immunogenicity"; separately labels cross-reactive T cells "**The correlate for heterosubtypic protection**, since HAI does not cross subtypes" | §5 tiers C and D |
| O2 | "Primary immunogenicity endpoint (licensu[re])" | §5 Table 5, Humoral row |
| F2 | "**Accepted regulatory surrogate.** Not sufficient here" | §4 Table 7, HAI row |
| F1 | "HAI titre (standard immunogenicity endpoint)" | §6 table, right-hand column |

**Cluster 2. Antibody placed in an efficacy-surrogate tier.** O1 O3. Opus-only.

| Run | Tier label | Carries the HAI-threshold observation in the same section |
|---|---|---|
| O1 | "T3 efficacy surrogate (d14-28)" for HAI CA09, HAI Aichi, Neut CA09, IgG2a CA09 | no |
| O3 | "**3. Efficacy surrogate (d14-28)**" for HAI, neutralisation, IgG2a/IgG1 | yes |

**Cluster 3. Antibody as a time-ordered tier without a role label.** F4, and F3 whose antibody
discussion sits in the evidence section rather than the biomarker section.

## The HAI-threshold observation

Three runs derive from the room that the conventional HAI threshold does not discriminate in
this package. One Opus, two Fable.

| Run | Quoted | Where |
|---|---|---|
| O3 | "At group level, HAI >=1:40 was **not** protective in aged mice. All 5/5 PSLN-212 mice had HAI >=40, yet 0/7 survived 10x LD50 CA09 (S03-C vs S03-I; note S03-I is tier C)" | §4 |
| F2 | "Not sufficient here: all 5/5 aged PSLN-212 animals had HAI >= 40 to H1N1, yet 0/7 (survival block) or 3/7 (weight block) survived matched challenge" | §4 Table 7 |
| F3 | "The usual HAI threshold of 1:40 does not discriminate here. 5/5 aged PSLN-212 animals reached 40 against H1N1 [S03-C], yet that regimen protected 0/7 against the matched virus [S03-I] (or 3/7 on the other ...)" | §4 |

O1, O2, O4, F1 and F4 carry no occurrence of the threshold figure.

F2 and F3 both note the survival-block and weight-block discrepancy inline, 0/7 against 3/7.
O3 marks S03-I as tier C.

**Golden, last.** The golden carries no occurrence of 1:40, >=40 or seroprotection. Its single
threshold statement runs the other way, as external knowledge: "HAI at the conventional
threshold is an accepted correlate for matched strains **[external]**." Its position on
antibody is role-based: "Carry forward as immunogenicity and the regulatory bridge, not as
the efficacy marker", on the grounds that "every antibody assay in this package was run
against the antigens the vaccine contained, so none of them speaks to the cross-subtype
claim, and no accepted antibody surrogate exists for cross-subtype protection **[external]**."

Both can hold at once: the golden's claim is about accepted practice for matched strains, and
the three runs' claim is about whether the threshold separates protected from unprotected
arms inside this package. Set out as two statements, with no verdict between them.

## Cross-model groupings on this decision point

| Grouping | Runs | Model split | Differs from the golden |
|---|---|---|---|
| Antibody in an efficacy-surrogate tier | O1 O3 | Opus-only | Golden assigns antibody to immunogenicity and the regulatory bridge, "not as the efficacy marker" |
| HAI threshold shown not to discriminate, from the room | O3 F2 F3 | mixed, 1 Opus and 2 Fable | Golden makes no such observation |
| Antibody separated from the heterosubtypic question in terms | O4 | Opus, unique in model | Matches the golden's reasoning, including that HAI does not cross subtypes |

O3 appears in two of the three groupings: it labels the tier "Efficacy surrogate" and makes
the threshold observation in the same section.
