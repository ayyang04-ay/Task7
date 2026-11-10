# AMnESTI: portfolio review position

Every figure below is a group mean recomputed from the workbook unless another
reduction is named. Survival percentages are the proportion of animals censored at
the block's final observation day. Comparisons between arms are log-rank
(Mantel-Cox), pairwise, unadjusted for multiplicity, which is the method the study
states. Statements marked **[external]** are field knowledge, not findings in this
package, and are flagged so the committee can tell the two apart.

---

## Recommendation

Advance it.

In all six configurations where aged animals were vaccinated and then challenged
with a virus of a different subtype, AMnESTI separated from the vaccine alone
(p = 0.0002 throughout) and from nanoSTING, which is the same liposome without the
manganese (p = 0.0009 to 0.0151). On survival the aged animals were not
distinguishable from young animals given nanoSTING in any configuration (p = 0.060
to 0.317). nanoSTING itself fails to separate from vaccine alone in three of the
six (p = 0.088, 0.111, 0.066), so the manganese is carrying the effect rather than
the liposome.

The asset is a correction of an age-specific priming deficit, not a general potency
increase. Within aged animals the adjuvant adds 1.65 to 24.35-fold across innate
and dendritic cell readouts. The identical comparison inside young animals adds
1.02 to 1.35-fold. That is the profile we want for a 65-plus indication, and it is
the single most defensible number set in the package because it is the only
comparison here that holds age and formulation apart.

Two things the package does not support, stated up front because the committee will
ask. It cannot tell us whether more antigen would do the same thing, and it cannot
link any immune measurement to any animal's outcome.

---

## The protection case

Nine challenge blocks sit on the S06 sheet. The set has to be derived before it
can be counted.

**S06-D is S06-C.** All 28 time-and-event pairs are identical across all four
arms. One experiment, entered twice, and counting both inflates the evidence.
Nothing in the room says which label owns the data, and the body-weight blocks for
the two challenge days are themselves distinct, so both experiments did run. The
choice to retain the day-14 reading and set aside the day-3 one is therefore
arbitrary; either could be the copy, and the day-3 rgH5N1 result should not be
leaned on separately.

**The two blocks at rows 69 to 70 are labelled S06-E and S06-F but hold the imprinting
experiment**, in 14-month-old animals given a bivalent vaccine containing both
CA09 H1N1 and Aichi H3N2 and then challenged with PR8 H1N1 or Perth H3N2. Those
challenges are within the subtypes the vaccine contains, so they belong to the
imprinting question, not to the cross-subtype count.

That leaves six.

| Block | Vaccine | Challenge | Day | AMnESTI | nanoSTING | sham | untreated |
|---|---|---|---|---|---|---|---|
| S06-A | Aichi H3N2 | PR8 H1N1 | 14 | 85.7% | 14.3% | 0% | - |
| S06-B | Aichi H3N2 | PR8 H1N1 | 3 | 71.4% | 0% | 0% | - |
| S06-C | bivalent | rgH5N1 | 14 | 100% | 28.6% | 0% | - |
| S06-E | Aichi H3N2 | PR8 H1N1 | 60 | 71.4% | 0% | 0% | 85.7% |
| S06-F | bivalent | rgH5N1 | 60 | 71.4% | 14.3% | 0% | 100% |
| S06-G | CA09 H1N1 | Perth H3N2 | 60 | 57.1% | 0% | 0% | 57.1% |

n = 7 per arm throughout. Reduction: proportion of rows censored at day 14.

| Comparison | S06-A | S06-B | S06-C | S06-E | S06-F | S06-G |
|---|---|---|---|---|---|---|
| AMnESTI vs sham | 0.0002 | 0.0002 | 0.0002 | 0.0002 | 0.0002 | 0.0002 |
| AMnESTI vs nanoSTING | 0.0083 | 0.0009 | 0.0068 | 0.0016 | 0.0094 | 0.0151 |
| AMnESTI vs young nanoSTING | 0.317 | 0.141 | identical | 0.141 | 0.141 | 0.060 |
| nanoSTING vs sham | 0.0267 | 0.088 | 0.0024 | 0.111 | 0.066 | 0.0063 |

**S06-G is not the weak end of a range.** The three day-60 blocks each carry an
arm of 20-month-old animals that received no vaccine and no virus. In S06-G that arm
lost 3 of 7 by day 10, giving 57.1%, which is the same figure as the AMnESTI arm
(p = 0.855). Every animal in that experiment that did not die of age survived the
infection. The same arm ran 6 of 7 in S06-E and 7 of 7 in S06-F, so S06-G drew a frailer
cohort. Reporting 57.1% as a protection rate without that arm misstates the result.

**Defence of the position.** With n = 7 per arm, a non-significant comparison is not
equivalence. Only S06-G is a tight match to its uninfected arm. In S06-E the AMnESTI arm
is one animal below it and in S06-F two below, and the test cannot resolve gaps that
small in either direction. The honest claim is "not distinguishable at this sample
size", and the next study is powered to do better.

Protection also appears at very short intervals. Challenge 3 days after a single
dose gives 71.4% against 0% for sham (S06-B). In a separate experiment where challenge
came 2 days after a single dose of rgH5N1 vaccine and animals were followed to day
21, AMnESTI was 10 of 10 censored, nanoSTING 3 of 10 and sham 1 of 10 (S03-J,
n = 10 per arm against a stated n of 9; one AMnESTI row carries an event code with
no day value and is counted as censored). At those intervals a vaccine-specific
antibody response has not yet formed **[external: primary humoral responses require
roughly one to two weeks]**, so whatever protects at day 2 or 3 is not antibody.

---

## What is driving the protection

The chain is established by intervention, not by correlation. Each step was removed
and the downstream readout fell.

**Uptake into the alveolar compartment.** Uptake of labelled liposome by alveolar
macrophages was 43.10% in wild-type animals and 12.65% in Sftpa1-/-Sftpd-/-
animals (S01-C, group means, n = 4). Carbenoxolone reduced recruited lung monocytes
from 7.28% to 3.08% (S11-C, group means, n = 5); the room gives the agent's route
and dose and not its mechanism, so read that step as gap-junction-dependent only on
**[external: carbenoxolone is a gap-junction blocker]**.

**Type I interferon.** In the adoptive transfer, monocyte-derived dendritic cells
were 19.70% from wild-type marrow and 2.09% from Ifnar-knockout marrow, and
recombinant GM-CSF brought the knockout arm back to 12.40% (S02-H, group means,
n = 5).

**GM-CSF.** Lung Gm-csf transcript at 36 hours was 8.74 for AMnESTI, 1.59 for
nanoSTING and 1.21 for sham, each relative to untreated animals (S02-F, group
means, n = 5).

**CCR2-dependent monocyte recruitment.** INCB3344 reduced lung GZMB+ CD8 T cells
from 6.77% to 1.39% (S02-I) and Ly6C+ macrophages from 15.35% to 2.52%, with
monocytes from 9.86% to 3.26% (S07-B). Group means, n = 5.

**Priming in the draining node.** Pertussis toxin left proliferating transferred
OT-I cells in lung at 0.93 of control (59.00% to 55.07%) while reducing them in the
mediastinal node to 0.22 of control (30.90% to 6.83%) (S05-C, group means,
n = 3).

Every one of those steps sits upstream of the adaptive response. The mechanism is
improved priming, not an effector function of the adjuvant itself.

**Where the chain stops.** No blockade experiment carries a challenge arm. INCB3344
cuts the lung cytotoxic CD8 population 4.9-fold and Ly6C+ macrophages 6.1-fold, and
no survival readout follows in either case, so the step from improved priming to
improved survival is inferred rather than shown.
That is the first thing the next study has to close.

**An alternative we cannot yet exclude.** Protection at day 3 is equally consistent
with a non-specific antiviral state left by STING activation. The day-3 cellular
readouts (NP-specific CD8 6.68% against 2.09%, Ki-67+ CD8 9.38% against 3.48%,
GZMB+ CD8 5.69% against 2.99%, all AMnESTI against nanoSTING, group means) are real
but sit inside the window where innate effects dominate **[external: primary CD8
responses to influenza in mice peak at days 7 to 10]**. The discriminating
experiment is in the next-studies section.

---

## What the adjuvant actually adds

The package compares aged animals given AMnESTI against young animals given
nanoSTING. That comparison changes two things at once. In six labelled blocks, seven panels, the workbook
also carries young animals given AMnESTI, which closes it.

| Readout | aged+nanoSTING | aged+AMnESTI | young+nanoSTING | young+AMnESTI |
|---|---|---|---|---|
| Ifnb1, 16 h (S01-A) | 16.64 | 37.11 | 37.60 | 50.70 |
| Ifnb1, 72 h (S01-A) | 3.43 | 4.43 | 1.59 | 3.13 |
| CD11b+ DC, d4 (S01-E) | 8.28 | 18.88 | 21.40 | 22.60 |
| cDC1, 72 h (S01-F) | 22.80 | 37.52 | 43.42 | 44.26 |
| cDC2, 72 h (S01-G) | 75.30 | 59.46 | 54.08 | 51.36 |
| Antigen-bearing DC in node (S02-C) | 1.77 | 7.09 | 9.39 | 11.12 |
| OT-I proliferation (S02-E) | 0.77 | 18.65 | 26.24 | 31.40 |

Group means, n = 5 throughout.

Adjuvant effect inside each cohort, AMnESTI over nanoSTING: aged 2.23, 2.28, 1.65,
4.01 and 24.35-fold on the five readouts the adjuvant raises, against 1.35, 1.06,
1.02, 1.18 and 1.20-fold in young animals. The cDC2 readout moves down in both,
0.79-fold aged and 0.95-fold young.

**Two headline numbers change.** Ifnb1 at 16 hours reads 0.99 of young on the
diagonal, which looks like a match. Holding formulation constant it is 0.73. And
the 72-hour residual reads 2.78 of young on the diagonal but 1.42 with formulation
held, because young animals given AMnESTI also fail to clear, 3.13 against 1.59 for
young animals given nanoSTING.

**The limit.** No humoral or cellular endpoint carries a young-plus-AMnESTI arm
*alongside* the aged and young-nanoSTING comparators, which is what a within-adjuvant
contrast needs. S02-I does carry a young-plus-AMnESTI arm, but only against its own
CCR2-blocked control, so it supports no age contrast. For everything downstream of
the dendritic cell compartment, age and formulation cannot be separated.

**Adaptive output is real but below young.** Across 18 endpoints with a young
comparator and a known direction, every one points the same way. Sixteen where more
is better fall below 1.0 (range 0.406 to 0.987) and two where more is worse sit
above it. The roster is fixed as follows, so that every count and mean below can be
rebuilt from the workbook:

| # | Endpoint | Block | Direction | ratio |
|---|---|---|---|---|
| 1 | Ifnb1, 16 h | S01-A | higher better | 0.987 |
| 2 | Ifnb1, 72 h | S01-A | **higher worse** | 2.785 |
| 3 | Ly6C+ monocytes, d4 | S01-D | higher better | 0.948 |
| 4 | Alveolar macrophages, d6 | S11-A | higher better | 0.661 |
| 5 | Serum IgG, H1N1 | S03-A | higher better | 0.618 |
| 6 | Serum IgG, H3N2 | S03-E | higher better | 0.406 |
| 7 | HAI, H1N1, geometric | S03-C | higher better | 0.758 |
| 8 | IgG2a:IgG1, corrected | S03-B + S13-A/B | higher better | 0.721 |
| 9 | Germinal centre B cells | S03-K | higher better | 0.666 |
| 10 | ICOS-high Tfh | S04-A | higher better | 0.752 |
| 11 | Tfr, d7 | S04-B | **higher worse** | 1.517 |
| 12 | NP+ CD8, lung, d3 | S05-A | higher better | 0.678 |
| 13 | NP+ CD8, lung, d7 | S05-A | higher better | 0.941 |
| 14 | Ki-67+ CD8, d3 | S05-D | higher better | 0.944 |
| 15 | GZMB+ CD8, d3 | S05-E | higher better | 0.592 |
| 16 | IFN-gamma+ CD8, cross-subtype restim, d14 | S05-F | higher better | 0.693 |
| 17 | IFN-gamma+ CD8, d60 | S05-G | higher better | 0.687 |
| 18 | Lung resident memory CD8 | S05-I | higher better | 0.656 |

Means of the per-endpoint ratios: humoral 0.654 over rows 5 to 10, cellular 0.741
over rows 12 to 18. Four endpoints are effectively matched: early interferon
induction (0.99), monocyte recruitment at day 4 (0.95), day-7 NP-specific CD8
(0.94) and CD8 proliferation (0.94).

The roster matters because the counts depend on it. Tfr at day 30 (S04-C) is the
same measurand as row 11, carries a young comparator, and sits at 1.893; MLN IgG in
B220+ cells (S13-H) sits at 0.954, above three of the four matched endpoints.
Neither is in the eighteen. Any count stated without the roster is unreconstructable
and should not be relied on.

Against the age-matched comparator the same endpoints invert. H1N1 serum IgG is
18.06-fold over nanoSTING (7891.6 against 437.0, group means) and 0.62 of young.
H1N1 HAI is 8.00-fold over nanoSTING by geometric mean (367.58 against 45.95) and
0.76 of young. Which comparator we pick decides whether this asset looks
transformative or disappointing, and for a 65-plus product the age-matched one is
the relevant one.

---

## Biomarkers, and what each could do in patients

**Antigen-specific CD8 and tissue-resident memory. Carry forward as the efficacy
marker.** These are accepted correlates of cross-subtype protection **[external]**,
so this package does not need to establish them. In the room they behave as the
mechanism predicts: lung resident memory at 0.656 of young, interferon-gamma
producing CD8 after cross-subtype restimulation at 0.693 at day 14 and 0.687 at day
60. The limit is access, not validity. The day-25 resident-memory readout is lung;
the day-14 and day-60 restimulation readouts are mediastinal lymph node. Both
compartments require tissue. In patients
the role is mechanistic and pharmacodynamic, read in a controlled human infection
study or from lavage in a dedicated cohort, not as a routine endpoint.

**Antigen-specific antibody. Carry forward as immunogenicity and the regulatory
bridge, not as the efficacy marker.** HAI at the conventional threshold is an
accepted correlate for matched strains **[external]**. It is peripherally
accessible and routine, which is its value. But every immunoassay in this package
was run against the antigens the vaccine contained, so none of them speaks to the
cross-subtype claim, and no accepted antibody surrogate exists for cross-subtype
protection **[external]**. Using titre as the efficacy readout would power the next
study on the one thing the asset is not claiming.

**Lung GM-CSF at 36 hours. Pharmacodynamic marker of adjuvant activity, preclinical
only.** It is antigen-independent, which makes it the cleanest readout of whether
the adjuvant engaged, and it separates cleanly (8.74 against 1.59 and 1.21). It is
also lung transcript, so there is no patient-accessible version of it. If we want a
clinical engagement marker we have to find one, and that is a gap rather than an
asset.

---

## Next studies

**Study 1. Close the priming-to-protection step and settle the mechanism.**
- *Establishes*: that the protection is monocyte and CD8-dependent rather than a
  non-specific antiviral state, and that the chain reaches survival.
- *Endpoints*: survival to day 14 after challenge, primary. Lung antigen-specific
  CD8 and resident memory, secondary.
- *Population*: 20-month-old animals, intranasal, as in the mounted work.
- *Comparators*: AMnESTI-adjuvanted vaccine with CCR2 blockade, with CD8 depletion,
  and with vehicle; plus sham. Adjuvant alone with no antigen is the arm that
  separates a non-specific antiviral state from a primed response.
- *Readouts*: survival curves by log-rank, with the cellular readouts on the same
  animals so the immune measure and the outcome are linked per animal, which
  nothing in the current package does.
- *Timing*: challenge at day 3 and at day 14 in parallel, since the two intervals
  test different mechanisms. Cellular sampling at day 7 to 10, not day 3.

**Study 2. Benchmark against the actual standard of care.**
- *Establishes*: whether the adjuvant beats more antigen, which is the comparison
  the committee and any payer will make. High-dose inactivated vaccine is licensed
  for 65-plus **[external]**, and HA content is never varied anywhere in this
  package, so we currently cannot answer it.
- *Endpoints*: survival after cross-subtype challenge, primary. Antigen-specific
  CD8, resident memory and serum antibody, secondary.
- *Population*: 20-month-old animals.
- *Comparators*: standard-dose vaccine with AMnESTI; high-dose antigen without
  adjuvant, dose-ranged; standard-dose with nanoSTING; sham.
- *Readouts*: survival by log-rank; immune endpoints on the same animals.
- *Timing*: single dose, challenge at day 14 and day 60 to cover durability.

**Study 3. Resolution kinetics, as the gating tolerability study.**
- *Establishes*: when the innate response returns to baseline, which the package
  does not measure. Both S09-A blocks are labelled 16h in the workbook and the
  annotation repeats that label for both, so the timepoint of the second is an
  inference, not a stated fact: exponentiated, its Ifnb1 values reproduce the 72 h
  column of S01-A (4.01 against 4.43) while the first block reproduces the 16 h
  column (36.3 against 37.1). On that basis all seven analytes sit above the
  untreated
  reference (Ccl2 27.41, Ccl3 9.23, Tnf 8.44, Il6 7.19, Il10 4.16, Ifnb1 4.01,
  Ccl5 2.01, each 10 to the power of the mean log10 of three replicates), and no
  arm carries a later timepoint. Young animals given AMnESTI also fail to clear, so
  this is a property of the formulation and not of the aged lung, which means it
  will not resolve itself in a younger population.
- *Endpoints*: time for Ifnb1, Tnf, Il10 and Ccl5 to return to the untreated
  reference. Lung histopathology and body weight, supporting.
- *Population*: 20-month-old animals, same strain and route.
- *Comparators*: age-matched nanoSTING and age-matched untreated. The young arm is
  context, not the acceptance criterion.
- *Readouts*: the same seven-analyte panel reported on a linear scale with the
  reduction stated.
- *Timing*: sampling beyond 72 hours until the untreated reference is reached. The
  analyte panel fixes only 16 and 72 hours, so the design has to run past both.
  Other blocks do carry 36 h (S02-F, S02-C, S10-A), but none carries an analyte
  timepoint later than 72 h.

---

## Considered and ruled out

**S06-D**, as a seventh configuration. Identical to S06-C in all 28 time-and-event
pairs.

**The two blocks at rows 69 to 70 of the S06 sheet**, as cross-subtype evidence.
Both challenge viruses fall inside the subtypes the bivalent vaccine contains.
Retained for the imprinting question, where both AMnESTI arms ran 85.7% whether or
not the animals had prior PR8 exposure.

**Antibody titre, as the readout to power the next study on.** Largest effects in
the package, but every assay used the vaccine's own antigens.

**The S03-B and S03-F subclass ratio panels, as printed.** Recomputed per animal
from the subclass data, the H1N1 ratio is 0.578 for nanoSTING, 2.144 for AMnESTI
and 2.972 for young, against 2.972, 0.578 and 2.144 as printed. The labels are
shifted by one position. The reading is forced rather than preferred: under the
printed assignment one arm's IgG2a plus IgG1 would have to exceed its own total IgG
by 16.1-fold for H1N1 and 11.3-fold for H3N2. Correctly paired the two subclasses
account for 0.559, 0.346 and 0.551 of total IgG. The same shift appears in both
panels.

**The arithmetic mean for HAI.** It gives an AMnESTI titre of 416.0 and a sham
titre of 6.0, and the lowest dilution tested was 1 in 10, so a central estimate of
6.0 is below the floor of the assay. Reduced as a geometric mean throughout.

**S05-A, as part of the day-3 mechanism case.** The source gives two different
immunisations for the same panel, ovalbumin in one statement and the bivalent
influenza vaccine in the other, and nothing resolves it. The day-3 case rests on
S05-D and S05-E, which are n = 5 and unambiguous. S05-I inherits the same
ambiguity.

**The single-cell layer.** Stated as performed on sorted CD45+ cells at days 5 and
7, with no data in the package. Nothing here rests on it.

**Extension beyond influenza.** No non-influenza pathogen antigen anywhere.
Ovalbumin is a model protein, not evidence of breadth.

**Tolerability, checked rather than assumed.** Both assays carry a positive control
that moved. Body weight at day 10 was 99.78% of baseline for AMnESTI against
90.65% for nanoSTING/R848, which is the arm that shows the assay can detect weight
loss, and that group had 4 of 5 animals remaining at day 10 with a minimum of
84.7%. Central nervous system cytokines ran 1.13 to 1.59 for AMnESTI against 2.68
to 5.50 for cholera toxin. Dosing sits at a plateau: 20 micrograms gives 45.83 and
40 micrograms gives 50.23, a 9.6% increase for twice the dose. The open question is
not acute tolerability but duration, which is Study 3.
