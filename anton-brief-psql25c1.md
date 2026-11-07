# Anton Task Brief — AMnESTI mucosal adjuvant, asset advancement
RLS short ID: psql25c1
RLS URL ID: task_4ce55343502b4d17b2182158ad6e4533
Campaign: camp_0589d1e96758477586df0e43dd8eeec1

Revision 2. Every figure in this brief was recomputed from the shipped workbook.
Changes from revision 1 are listed at the end under "What changed in revision 2".

## 1. THE PROMPT

### Scene
Asset is the adjuvant, not a vaccine. Indication is heterosubtypic influenza
protection in older adults. Decision is advance or not, at a committee meeting
with a GLP tox slot that releases on deferral.

### Deliverables and paths
/tmp/outputs/answer.md, recommendation on the first line, rest structured by the
model. Analysis artifacts under /tmp/outputs.

### As-of date
6 November 2026. Committee date of 20 November is a scene fact, not a record date.

### Out-of-scope
Study design, specification and interpretation of the mounted data. No bench
protocols.

### Prompt draft (257 words)

We have AMnESTI, a manganese-complexed pulmonary-surfactant-biomimetic liposomal
STING agonist, in preclinical development as a mucosal influenza vaccine adjuvant
for heterosubtypic protection in older adults.

Tell me whether we advance it, and what the next studies have to show. The
programme committee meets on 20 November and the GLP toxicology slot we are
holding releases if we do not commit at that meeting, so I need a decision, not a
deferral.

Everything we have is in /tmp/world/filesystem. It is a working directory rather
than a curated one, so some of it will not bear on the decision. All figures,
findings and conclusions must be grounded in those files rather than in outside
sources. Perform your analysis as of 6 November 2026.

Build me the proposal and lead with your recommendation on the first line
(/tmp/outputs/answer.md). Structure the rest as you see fit.

It has to be highly defensible. Every claim and every number needs explicit
reasoning, the file it came from and how it was reduced. Save any analysis you run
under /tmp/outputs.

The committee will want the effectors driving the protection, any biomarker of
efficacy worth carrying forward, and for each study you propose: endpoints,
populations, comparators, readouts and timing.

Tell me as well what you set aside and why, item by item, including anything in
there that does not bear on the decision.

Keep this at the level of study design, specification and interpretation of the
mounted data. No bench protocols.

### Prompt audit

No persona, no numbered steps, no tool names, no explained science, no answer
taxonomy. Load-bearing sources not named and the room described generically with
the not-all-relevant line. As-of date fixed and in the past. Both deliverable paths
named. Basis required per number. Set-aside section mandated, which is what makes
triage visible and what licenses the set-aside product in the golden. Scope line
present and forbids nothing the prompt requires. Mounted-only constraint explicit.
Under 600 words.

The set-aside sentence stops short of saying that any particular result is unsound,
so no trap is flagged. The institutional framing the refusal field note calls for is
carried by "in preclinical development" and "the programme committee"; that is the
addition that took an earlier panel from 0 of 16 completed to 7 of 16.

## 2. THE DATA ROOM

### Manifest
| File | Contents | States the world how |
|---|---|---|
| adz5242_data_file_s1.xlsx | 15 sheets, 101 per-animal data blocks | Shipped unmodified. 90 of 101 blocks do not name their measurand |
| trial_summary.md (to author) | Per-block annotation, methodology, formulation | Dry annotation only. See absence anchors |

No publication mounted. The MDAR reproducibility checklist that ships in the same
supplementary archive is not mounted either; it is filed under a different DOI from
the paper and is not part of this world.

Runs have retrieval; the three commitments are absent from the publication, so
retrieval does not win. The publication does hand over the Th1 claim, the protection
figures and the mechanism narrative, and it actively misleads on tolerability.

### Anchor table
| Anchor | Value | Block | Steps | Legible? |
|---|---|---|---|---|
| Heterosubtypic survival | cand 71.4-100%, comp 0-28.6%, sham 0%, across five independent configurations after collapsing 6G into 6E and setting 6J aside | 6A 85.7/14.3, 6C 71.4/0, 6E 100/28.6, 6H 71.4/0, 6I 71.4/14.3 | 1 | yes |
| Natural-death ceiling | unvaccinated unchallenged arm: 6H 85.7%, 6I 100%, 6J 57.1% | Fig.6 rows 34-68, fifth arm | 1 | yes |
| Early protection | 6C 71.4% at d3; 3J 100% at d2, censored at d21 | 6C, 3J | 1 | yes |
| Day-3 lung CD8, three convergent | NP+ 6.68/2.09; Ki-67 9.38/3.48; GZMB 5.69/2.99 | 5A, 5E, 5F | 1 | 5A merged hdr |
| Blockade chain | CBX 7.28->3.08; IFNAR 19.70->2.09, GM-CSF rescue 12.40; INCB 6.77->1.39 and 15.35->2.52; PTX lung 0.93x MLN 0.22x | S4E, 2K, 2L, 7F, 5D | 1 each, 4 sheets | yes |
| GM-CSF 36h | 8.74 vs 1.59 vs 1.21 | 2I | 1 | merged hdr |
| 72h residual | Ccl2 27.41, Ccl3 9.23, Tnf 8.44, Il6 7.19, Il10 4.16, Ifnb1 4.01, Ccl5 2.01; young comparator 0.11 to 101.59 on the same analytes | S2A block 2 | 3 | yes, header reads Log10 |
| Tolerability controls | S1J cand 99.8 vs comp+R848 90.7 (min 84.7, 4 of 5 animals); S3E cand 1.13-1.59 vs CT 2.68-5.50 | S1J, S3E | 1 | merged hdr |
| Dose plateau | 45.83 -> 50.23 (+9.6%) | S1B | 1 | merged hdr |
| Corrected subclass | H1N1: comp 0.578, cand 2.144, young 2.972. As printed: 2.972 / 0.578 / 2.144. H3N2 carries the same shift: 0.512 / 2.727 / 2.891 against printed 2.891 / 0.512 / 2.727 | 3B/3F + S8A-D | 3 | yes |
| Foreclosure for direction | subclass-sum/total-IgG 0.56/0.35/0.55 (H1N1) and 0.57/0.32/0.34 (H3N2) against 16.1x and 11.3x under the alternative | 3A/3E + S8A-D | 2 | yes |
| HAI | cand geo 367.6, arith 416.0; sham [10,10,10,0,0] arith 6.0 against a 1:10 floor | 3C | 2 | yes |
| 6E identical to 6G | 28 of 28 (time,event) pairs | Fig.6 | 2 | yes |
| Age-matched vs young | 19 of 19 paired endpoints below 1 against young (0.357-0.954) and above 1 against age-matched (2.31-20.70x), no exceptions. H1N1 IgG 18.1x / 0.62; H1N1 HAI 8.0x geometric / 0.76 | 13 humoral + 6 cellular, listed in the derivation notes | 2 | yes |

Legibility note on the 72h panel. It needs three transformations, but none is
invisible. The sheet header for the block reads `Fig. S2A 16h n=3 Log10`, so the
scale is stated in the workbook rather than in the annotation. The PBS arm means
exactly 1.00 after exponentiation in all fourteen analyte-blocks, which is a second
cue available without reading the header. Block identity resolves relationally:
block 1 Ifnb1 exponentiates to 36.3 against Fig. 1A at 16h (37.1), block 2 to 4.01
against Fig. 1A at 72h (4.43). Cite the header, not the companion document, when
writing this mode up.

### Fig. 6, full enumeration

| Block | Vaccine | Challenge | Day | Relation | cand | comp | sham |
|---|---|---|---|---|---|---|---|
| 6A | Aichi H3N2, 1 ug HA | PR8 H1N1, 5x mLD50 | 14 | heterosubtypic | 85.7% | 14.3% | 0% |
| 6C | Aichi H3N2, 1 ug HA | PR8 H1N1, 5x mLD50 | 3 | heterosubtypic | 71.4% | 0% | 0% |
| 6E | bivalent | rgH5N1, 5x mLD50 | 14 | heterosubtypic | 100% | 28.6% | 0% |
| 6G | bivalent | rgH5N1, 5x mLD50 | 3 | heterosubtypic | 100% | 28.6% | 0% |
| 6H | Aichi H3N2, 1 ug HA | PR8 H1N1, 5x mLD50 | 60 | heterosubtypic | 71.4% | 0% | 0% |
| 6I | bivalent | rgH5N1, 5x mLD50 | 60 | heterosubtypic | 71.4% | 14.3% | 0% |
| 6J | CA09 H1N1, 0.5 ug HA | Perth H3N2, 5x mLD50 | 60 | heterosubtypic | 57.1% | 0% | 0% |
| rows 69-70 cols G-L, labelled 6H | bivalent, 14-month mice, prior PR8 or saline | PR8 H1N1, 5x LD50 | not stated | within H1N1 | 85.7% / 85.7% | 0% / 57.1% | n/a |
| rows 69-70 cols M-R, labelled 6I | bivalent, 14-month mice, prior PR8 or saline | Perth H3N2, 5x LD50 | 14 | within H3N2 | 85.7% / 85.7% | 0% / 0% | n/a |

Two exclusions, both derivable from mounted facts.

6G collapses into 6E: all 28 (time, event) pairs are identical across all four arms,
so it is one experiment and not two.

6J cannot carry a protection estimate in either direction: its unvaccinated,
unchallenged arm lost 3 of 7 animals by day 10 (days 3, 7 and 10), giving 57.1%,
which is the same figure as its candidate arm. Background mortality and challenge
mortality are not separable inside that block. The same arm in the two
concurrently designed day-60 blocks ran at 85.7% and 100%.

The two blocks at rows 69-70 are within-subtype heterologous, not heterosubtypic:
the bivalent vaccine contains CA09 H1N1 and Aichi H3N2 and the challenges are PR8
H1N1 and Perth H3N2. They support the imprinting claim and not the configuration
count.

In 6H the achievable ceiling is 85.7% rather than 100%, so the day-60 result nets
to 71.4 of an available 85.7 against a sham of 0. In 6I the ceiling is 100%.

### Absence anchors (assert mechanically)
trial_summary.md must NOT contain:
- any fold-change, ratio, percentage, effect size or p-value
- "transient", "resolved", "returns to baseline", "sustained", or any judgment
  about the duration of the innate response
- "restored", "youth-like", "comparable to young", "reaches the levels of"
- that the young-comparator arm is a benchmark or reference FOR anything
- that the unvaccinated unchallenged arm is a control FOR anything, or that deaths
  in it are background
- that any assay is strain-specific, homologous-only, a correlate or a surrogate
- that any two blocks share data, duplicate, or are mislabelled
- that any challenge is homologous, heterologous or heterosubtypic
- that the ratio panel was computed from the subclass panels
- which readouts are peripherally accessible
- how many panels have or lack source data
- any causal claim, including the direction of the blockade results
- the source's figure titles

trial_summary.md MUST contain: per block the measurand, units and scale, timepoint,
stated n, group identities and replicate count. Per challenge block, vaccine
composition, challenge virus, challenge dose as stated, challenge day, mouse strain
and age, stated per block and not globally. Per immunoassay, the antigen used. For
the fifth arm of 6H, 6I and 6J, that those animals received no vaccine and no
challenge virus. Every intervention agent and its mechanism. Adjuvant identities
and the single composition difference. Stated statistical methods and summary
measures, including that the fig. S2A panels are normalised against untreated mice.
Dose per arm. That scRNA-seq was performed, on which cells, when. Plus mLD50
determination and formulation specifications as non-load-bearing noise.

Source inconsistencies reproduced verbatim and unremarked:
- both immunogen statements for 5A, the second inside an unclosed parenthesis; 5E
  and 5F read "vaccinated as in (B)" and (B) states no vaccination of its own
- the NP366-374 tetramer against the stated BALB/c strain
- the stated n values that disagree with their own observation counts: 3J header
  n=9 against arms of 10, 10 and 9 with a stated n of 10 in the source; 5A/5B
  header n=3 against 2 observations
- both fig. S2A headers reading 16h
- the sheet labelled Fig. S13 carrying fig. S14 panels
- Fig.6 rows 69-70 labelled 6H/6I carrying 6K/6L content
- the Fig. S3 block labelled S3C carrying S3E content
- Fig. 3J carrying three arms where the source legend names two, with a censoring
  day of 21 against 22 days of stated monitoring
- the rows-69-70 blocks stating the challenge dose as LD50 where every other
  challenge block states mLD50, and one of the two giving no challenge day

Do not carry into the annotation: the publication's own text states that the
day-60 experiment used the comparator-formulated vaccine and was fully protected,
which contradicts its own Fig. 6H comparator arm at 0 of 7. That is a publication
error, not a room fact.

Per-block strain matters. The rows-131-161 blocks of the sheet labelled Fig. S13
are aged C57BL/6 and Swiss Webster, not BALB/c. The NP366-374 restriction
inconsistency is determinate only where the strain is stated block by block.

### Required tooling
openpyxl or pandas with openpyxl. No merged-cell handling in default reads.
Confirmed present in sandbox.

## 3. THE GOLDEN RESPONSE

### Spec

First line:

> Advance AMnESTI into the GLP toxicology slot. The case is heterosubtypic survival
> in 20-month-old mice across five independent challenge configurations (71.4 to
> 100% AMnESTI against 0 to 28.6% for the same vaccine with the comparator adjuvant
> and 0% sham), and the next studies are powered on the day-3 lung CD8 readout
> against an age-matched comparator, not on any antibody titre.

Then, in the model's own structure:

- The protection case, with the event coding derived and the heterosubtypic set
  derived rather than asserted: 6G collapsed into 6E, 6J set aside on its own
  unvaccinated unchallenged arm, the rows-69-70 blocks classified as within-subtype,
  and the day-60 results netted against the ceiling that arm sets.
- Attribution to a non-antibody mechanism at d2-d3, with the three convergent day-3
  readouts and the innate alternative named but unresolved, plus the discriminating
  experiment.
- The effector chain, each step anchored to its blockade.
- GM-CSF at 36h as the antigen-independent PD marker, plus the accessibility gap.
- Tolerability bounded by both required checks, and the 72h state reported as
  unresolved rather than transient.
- What the package does not support.
- Two next studies with endpoints, populations, comparators, readouts and timing.
- The set-aside material, item by item with the reason, as the prompt now asks.

### Forcing chain (21 route-necessary legs)
1  indicator 1 is death                      joint distribution, 1 at d4-12, 0 only at d14
2  which blocks are heterosubtypic           annotation, classified by the solver
3  cand/comp differ only by Mn complex       annotation
4  the heterosubtypic set is derived         6G collapsed into 6E on 28 of 28; 6J set aside; rows 69-70 excluded as within-subtype
5  protection exists at d2-d3                6C, 3J
6  that protection is not antibody-mediated  timing + naive animals + external kinetics
7  two mechanisms remain live                S2A block 2 + d3 cellular
8  day-3 cellular readouts separate          5A, 5E, 5F
9  all immunoassays homologous-antigen       annotation
10 antigen-independence, five immunogens     3I, 6A, 6E, 3J, 2F + annotation
11 age-matched and young give opposite reads 19 blocks, unanimous
12 chain established by blockade             S4E, 2K, 2L, 7F, 5D
13 S2A block 2 is the 72h panel              Ifnb1 4.01 matches Fig.1A 72h; block 1 at 36.3 matches 16h
14 S2A is log10                              sheet header; PBS arm exponentiates to 1.00
15 all seven analytes unresolved at 72h      block 2 exponentiated
16 tolerability assays carry controls        S1J comp+R848, S3E cholera toxin
17 dose at plateau                           S1B
18 no accessible antigen-independent marker  enumeration by compartment
19 sequencing layer absent                   annotation says run, no data mounted
20 no non-influenza pathogen antigen         enumeration; OVA is a model protein
21 the fifth arm of 6H/6I/6J received no vaccine and no challenge, so any death in it is background  Fig.6 rows 34-68

Leg 21 binds unconditionally once a solver reads any day-60 block, which legs 4 and
11 both require.

Conditional legs, binding only if the solver uses the readout: 6E identical to 6G;
subclass panel inconsistent with direction forced; HAI sham estimate below assay
floor; Tfh:Tfr an algebraic transform.

### Named domain knowledge, marked as such in the golden
primary humoral kinetics; reciprocal dilution series, GMT convention, below-LOD
handling; NP366-374 H-2Db restriction against BALB/c H-2d; sustained type I IFN
antagonising IFN-gamma responsiveness and B cell responses; impaired inflammation
resolution in the aged airway; cyclic dinucleotide therapeutic window; influenza
licensure surrogates in older adults.

### Derivation notes

Survival from (time, event) pairs, percent censored at the block's own last day,
which is 14 everywhere except 3J, where it is 21.

Subclass ratio per animal then group mean, not ratio of group means. The H1N1 panel
is S8A over S8B and the H3N2 panel is S8C over S8D. Both ratio panels carry the same
cyclic column shift: what is printed under the three labels belongs to the arms one
position to the left.

Subclass sums against total IgG, which is what forecloses the direction. Correct
pairing gives 0.559, 0.346 and 0.551 for H1N1 against Fig. 3A, and 0.567, 0.319 and
0.337 for H3N2 against Fig. 3E. Under the alternative, that the shift sits in the
subclass panels rather than in the ratio panels, one arm's two subclasses sum to
16.1 times its own total IgG for H1N1 and 11.3 times for H3N2.

72h analytes as 10^mean(log10 replicates); the arithmetic reduction agrees within
10% and either is acceptable.

HAI as geometric mean; the sham arm requires a stated below-LOD convention. The
8.0x age-matched figure for HAI is geometric; the arithmetic reduction gives 8.67.

Age-matched comparisons pair arms within block. The 19 endpoints are: humoral 3A,
3C, 3D, 3E, 3G, 3H, S8A, S8B, S8C, S8D, S8H, S8I, S8J; cellular 5E, 5F, 5K, 5L, 5M,
5N. Report the unanimity rather than a mean. Mean ratios are sensitive to block
membership and to the reduction, and they are not the fact that carries the pillar.

72h panel, exponentiated, normalised to the PBS arm:

| Analyte | aged sham/PBS | aged comparator | aged candidate | young comparator |
|---|---|---|---|---|
| Ifnb1 | 1.00 | 3.40 | 4.01 | 1.39 |
| Il6 | 1.00 | 1.86 | 7.19 | 3.10 |
| Ccl2 | 1.00 | 5.23 | 27.41 | 101.59 |
| Ccl3 | 1.00 | 4.73 | 9.23 | 41.45 |
| Ccl5 | 1.00 | 1.21 | 2.01 | 0.55 |
| Tnf | 1.00 | 5.23 | 8.44 | 0.48 |
| Il10 | 1.00 | 4.18 | 4.16 | 0.11 |

The resolution claim is not that 72h inflammation is high. It is that at 72h the
aged candidate lung has not begun to resolve on the axis the young lung has already
resolved on, and that no arm carries a timepoint past 72h. Duration is unmeasured,
not measured and acceptable.

The gating study the golden proposes, in the five fields the prompt asks for:
endpoint, time to return of Ifnb1, Tnf, Il10 and Ccl5 to the untreated reference in
lung, with lung histopathology and body weight supporting; population, 20-month-old
animals at the strain and route of the mounted work; comparators, age-matched
adjuvant comparator and untreated age-matched, with the young arm as context rather
than as the acceptance criterion; readouts, the same seven-analyte panel on the
linear scale with the reduction stated; timing, extending past 72h until the
age-matched untreated reference is reached, since the mounted data fix 16h and 72h
only.

## 4. PRE-REGISTERED FAILURE MODES

### False-optimum map, tier 1
| Mode | Fails to check | Why it attracts | Refuting fact | Counterfactual |
|---|---|---|---|---|
| humoral-readout-as-asset-value | that every immunoassay is homologous-antigen, and that strain-specific titre is the antigen's property | 18.1x IgG and four-figure neut titres are the largest numbers in the package | annotation, antigen per assay | powers on the local cellular readout |
| resolution-inventoried-not-addressed | nothing; notes the 72h elevation and proposes no work | listing it feels like diligence | omission, not error | resolution kinetics becomes the gating study |
| log-scale-not-converted | the sheet header for the block | every value reads near 1 | header reads Log10; Ccl2 1.488 -> 27.41x; PBS arm would read 0 rather than 1 | finds all seven elevated |
| correlates-listed-not-chain-established | the four blockade experiments | DC and Treg shifts are easier to read than interventions across four sheets | S4E, 2K, 2L/7F, 5D | builds the chain, can then propose a PD marker |
| young-benchmark-as-sole-basis | the age-matched comparison | the package nominates the young arm | same endpoints invert, 19 of 19, 0.76 against 8.0x | recommends against standard of care |
| background-mortality-not-netted | that the day-60 blocks carry an arm receiving neither vaccine nor challenge, and that in 6J that arm lost 3 of 7 by day 10 | 6J reads as a sixth configuration at 57.1%, which either drags the headline range to 57-100% or gets dropped with no reason given | Fig.6 rows 34-68, fifth arm of 6J: events at days 3, 7 and 10 of 7 animals, against 1 of 7 in 6H and 0 of 7 in 6I | sets 6J aside on a stated mounted fact and reports 71.4-100% across five, or retains it and states that the two mortality sources are not separable |

### Tier 2 watch list
innate-alternative-not-considered; duplicated-blocks-treated-as-independent;
heterosubtypic-and-homologous-blocks-conflated;
within-subtype-challenge-counted-as-heterosubtypic;
central-estimate-below-assay-floor; derived-panel-unreconciled;
peripheral-surrogate-asserted; tolerability-asserted-without-assay-sensitivity;
non-resolution-omitted-from-tolerability; mechanism-imported-without-grounding;
coding-convention-not-established; algebraic-transform-treated-as-corroboration;
single-analyte-for-multi-analyte-claim; source-inconsistency-unflagged;
extensibility-claimed-without-non-influenza-data;
strain-specific-readouts-treated-as-asset-value

### Escape and foreclosure
| Escape | Local appeal | Foreclosing fact | Where |
|---|---|---|---|
| indicator 1 as alive | natural reading | 14-day study cannot record survivors dying at d4 | Fig.6, 3I/J |
| evaluate on homologous blocks | 3I 100%, 6K 85.7% are the cleanest numbers | those challenge viruses are in the vaccine | annotation |
| count 6K/6L toward the heterosubtypic set | the sheet labels them 6H and 6I | the bivalent vaccine contains both challenge subtypes | annotation, vaccine composition per block |
| report 6J as a sixth configuration at 57.1% | it is a labelled, independent, durable challenge block | its unvaccinated unchallenged arm is also 57.1%, against 85.7% and 100% in the two concurrent blocks | Fig.6 rows 34-68 |
| power on antibody titre | largest effects in the package | homologous-antigen only; titre is the antigen's property | annotation |
| early protection as antibody | antibody is the default mechanism | d2-d3 in naive animals, unadjuvanted arm 0-10% | 6C, 3J + external |
| cellular without addressing innate | d3 cellular data are positive | innate still running at 72h | S2A block 2 |
| transience from Ifnb1 or in log space | Ifnb1 is the headline analyte | 7 of 7 elevated; Ccl2 27.41x | S2A + units |
| 72h state is within the young range | young runs 101.59 on Ccl2 and 41.45 on Ccl3 against 27.41 and 9.23 | the direction inverts rather than the degree: the young arm is at or below its own untreated reference on Tnf 0.48, Il10 0.11, Ccl5 0.55 and Ifnb1 1.39 where the aged candidate arm is 8.44, 4.16, 2.01 and 4.01 | S2A block 2, all four arms |
| 6E and 6G as two experiments | differently labelled | 28 of 28 identical | Fig.6 |
| 69x HAI rise | arithmetic mean is the library default | implies sham titre 6.0 below a 1:10 floor | 3C |
| subclass ratio as printed | it is the panel built for it | one arm's subclass sum would exceed its own total IgG by 16.1x for H1N1 and 11.3x for H3N2 | 3B/3F, S8A-D, 3A/3E |
| import the mechanism narrative | retrieval supplies it | no sequencing data mounted | annotation + absence |
| young benchmark as sole basis | package nominates it | NONE in the room | - |

### Grader guidelines (ABC, brief)

A. Must be present and correct: a recommendation to advance, grounded in the
heterosubtypic challenge blocks rather than in any humoral readout; a
heterosubtypic set that is derived rather than asserted, with any block collapsed or
set aside on a stated mounted fact; a next-study comparator that is age-matched
rather than young; and resolution kinetics proposed as work, not inventoried as a
caveat. Each met only where the attempt's own cited numbers reproduce from the
mounted files by the route it states.

B. Penalise: powering a protection readout on antibody titre; reporting 72h analytes
unexponentiated; treating 6E and 6G as independent; reporting a protection range
that includes Fig. 6J without reference to its unvaccinated unchallenged arm;
counting the rows-69-70 blocks as heterosubtypic; citing the subclass ratio as
printed; asserting mechanism with no mounted citation; any central estimate below an
assay floor.

C. Neutral: number of studies; whether the innate alternative is resolved or left
open with a discriminating experiment; statistical method choice; whether the n
mismatches or sheet mislabels are noticed; retention of humoral readouts as a
regulatory bridge.

## 5. SUPPORTING

### Hidden basin
The package nominates the wrong benchmark for the decision it is being used to
make, and its largest effects are in the readouts that cannot carry its claim.

### Panel geometry
16 independent samples. No subagent fanout; correlated arms give sixteen versions
of one trajectory and a thin mode set.

### Known risks and open questions
1. The young-benchmark mode has no refuting fact in the room. Defence is that
   recognising differential benchmarks by age is competence, not a trick. If the
   panel shows nobody reaches it, the prompt is the lever.
2. The committee date and GLP slot are the only fabricated content. They exist to
   close the hedge, which the guidance asks for, but they are invented.
3. Resolved. The H-2Db restriction call holds: NP366-374 is the H-2Db-restricted
   epitope and the stated strain is BALB/c, H-2d. The BALB/c-dominant NP epitope is
   NP147-155 on H-2Kd. The restriction inconsistency is real, and it is determinate
   only where the annotation states strain per block, since some blocks in the
   workbook are C57BL/6.
4. Three products rest on annotation alone (legs 2, 3, 9). A thin or ambiguous
   annotation there breaks Pillars 1 and 3 rather than making them hard. Leg 14 no
   longer belongs on that list; the scale is stated in the workbook header.
5. S4B and S4C share 35 of 100 cells, the first two animals of every group at
   every timepoint. Suggestive of partial copy. Not determinate; no mode rests
   on it.
6. New. 6J's unvaccinated unchallenged arm is the only block where background
   mortality is high enough to matter, and the exclusion rests on comparing it to
   the same arm in 6H and 6I. If a reviewer disputes that the three blocks are
   comparable, the fallback is to retain 6J and report 57.1 to 100% with the
   non-separability stated. Either answer is defensible; silently dropping 6J is not,
   which is what makes the mode nameable.

### Build constraints
- Anchors carrying tier-1 modes must be legible under more than one extraction
  strategy. The 72h panel is verified: header, PBS-arm value and cross-block Ifnb1
  match all give the same reading.
- Absence anchors asserted mechanically, not checked by eye.
- The out-of-scope line forbids nothing the prompt requires: confirmed.
- Recompute the golden from the shipped data room after its last edit.
- Validate ceiling and floor: that a strong attempt working only from the room
  reaches the verdict, and that the obvious first pass does not.

### What changed in revision 2
- Fig. 6 fully enumerated. 6G collapsed into 6E, 6J set aside on its own
  unvaccinated unchallenged arm, rows 69-70 reclassified as within-subtype. Five
  configurations stand, now with a derivation behind them. New tier-1 mode
  `background-mortality-not-netted`, new forcing-chain leg 21, new escape rows, new
  anchor row for the natural-death ceiling, B list extended.
- Resolution pillar given the comparison it turns on. The escape "within the young
  range" is foreclosed on direction rather than degree, with the four-arm 72h table
  and the gating study specified to the prompt's five fields.
- Prompt extended by one sentence mandating the set-aside section, which licenses
  the set-aside product in the golden, plus the mounted-only clause. 233 to 257
  words.
- Age-matched anchor rewritten. The stated means do not reproduce by any reduction;
  replaced by unanimity across 19 named endpoints. The 8.0x HAI figure is geometric,
  and the arithmetic reduction gives 8.67.
- Added source inconsistencies for 3J, the rows-69-70 dose and day, and the 5A
  parenthetical chain to 5E/5F. Added the per-block strain requirement and two
  items to keep out of the annotation.
- Corrected where the log10 fact lives: the workbook header, not the companion
  document.
