# Anton Task Brief — PSLN-344 mucosal adjuvant, asset advancement
RLS short ID: psql25c1
RLS URL ID: task_4ce55343502b4d17b2182158ad6e4533
Campaign: camp_0589d1e96758477586df0e43dd8eeec1
Studio: https://studio.mercor.com/annotator/tasks/task_4ce55343502b4d17b2182158ad6e4533/?campaignId=camp_0589d1e96758477586df0e43dd8eeec1

Revision 3. Every figure was recomputed from the shipped workbook in session.
Legend and design facts come from the unmounted publication (Gao et al., Sci
Immunol 2026, adz5242) and its supplementary materials, which stay out of the room
and feed adjuvant_program_annotation.pdf. Change log at the end.

---

## 1. THE PROMPT

### Scene
Asset is the adjuvant, not a vaccine. Stated indication is IAV vaccine development
in older adults. Decision is advance or not, for a portfolio review at which every
asset has to be justified. No dates anywhere, and no fabricated content.

### What the answer must carry
Asked as questions, not headings. No output object is named; the reply is the
deliverable. In the solver's own words: whether to advance; the case for that call,
with as much support and defence as the data allows; the file and the reduction
behind every number relied on; what is driving the protection; whether a biomarker
of efficacy is worth carrying forward, whether it could go into patients and in
what role; what the next studies have to establish, each with endpoints,
populations, comparators, readouts and timing; and what was considered and ruled
out.

### Out-of-scope
None stated in the prompt as shipped. See item 3 of the audit below.

### Prompt draft (203 words), flat text as pasted

PSLN-344 is our manganese-complexed pulmonary-surfactant-biomimetic liposomal STING agonist. It has been in preclinical development as an adjuvant for IAV vaccine development in older adults. For an upcoming portfolio review I need to justify every asset to the committee.

All of our data on PSLN-344 is dumped here. All analysis and recommendations should be grounded in our data, which serves as ground truth.

I want your recommendation: do we advance this adjuvant? Regardless of yes or no, I need a strong defensible case to present, so build out the position with as much support and defense as the data allows. Every number you rely on needs to cite the relevant data and state how you reduced it, because the committee will check them.

And either way I need the forward view, because if I drop this I have to be able to say what we are dropping and why. What is actually driving the protection? Is there a biomarker of efficacy worth carrying forward, could it go into patients, and in what role? What would the next studies have to establish, and for each one, what are the endpoints, populations, comparators, readouts and timing?

Tell me what you considered and ruled out.

### Prompt audit

Passes: no persona; terse brief, situation then ask then stop; no numbered steps,
tool names, cautions or hints; load-bearing sources not named; spoken by the person
who owns the decision; no decision rule stated; no answer set printed; the solver
constructs the verdict in its own words with no format prescribed; what was ruled
out is asked as a question rather than mandated as a heading; reporting conventions
mounted rather than stated; the asks are imperative and concrete; the
wrong-but-attractive conclusion is expressible; 203 words; flat text.

Deprecations confirmed absent: no as-of date or analysis cut-off; no output file,
path, directory or named artifact; no no-web or no-search line; no request for
saved analysis artifacts; no mandated output headings or prescribed section order.

Provenance holds, one notch softer than before. "All analysis and recommendations
should be grounded in our data" is on its own the weak phrasing the guidance names
as insufficient, but the prompt also asks each number to cite the relevant data and
state how it was reduced. The reduction clause is the load-bearing half: it is what
makes a figure recomputable rather than merely attributed. Dropping the earlier
file-level wording removes a pointer but not the guard. With saved artifacts
deprecated this is the only remaining defence against invented figures, so it must
not be cut back to the grounding sentence alone.

Three checklist items this version drops. Recorded so the choice is on the record
rather than silent.

1. No not-all-of-it-is-relevant line. The room is deliberately noisy by design and
   the guidance asks for that line where it is. Without it a solver may treat every
   block as load-bearing, and the ruled-out question loses the ground it stands on.
2. No constraint on deferral as a world fact. "Regardless of yes or no, I need a
   strong defensible case" makes both branches cost work, which is how the
   delivered house-style prompt closes the hedge, so this may be sufficient alone.
3. No out-of-scope line. The project boundary is that design, specification and
   interpretation are in scope and bench-executable procedure is not. The prompt
   asks for next studies with readouts and timing and sets no boundary.

Prompt versus predicted modes, both directions. Every tier-1 mode below is fairly
elicited: the advance question forces the protection set and the comparator choice;
"what is actually driving the protection" forces the blockade chain and the
innate-versus-adaptive call; "is there a biomarker worth carrying forward, could it
go into patients" forces the accessibility and antigen-specificity work; "endpoints,
populations, comparators, readouts and timing" forces the comparator and the
sampling timepoint. The ruled-out question has the weakest forced core, resting on
the duplicated block and the S05-A ambiguity; it stays because the scene wants it
but it is not counted as a product.

The indication line reads IAV vaccine development rather than heterosubtypic
protection. That removes a steer: the earlier wording named the conclusion the
protection pillar is supposed to reach.

---

## 2. THE DATA ROOM

### Manifest
| File | Contents | States the world how |
|---|---|---|
| adjuvant_program_dataset.xlsx | 15 sheets, 101 per-animal data blocks | Shipped unmodified. 90 of 101 blocks do not name their measurand |
| adjuvant_program_annotation.pdf (to author, ships as PDF) | Per-block annotation, methodology, formulation | Dry annotation only. See absence anchors. Markdown is no longer permitted in the room; the workbook stays .xlsx |

No publication mounted. The MDAR reproducibility checklist shipped in the same
supplementary archive is not mounted either; it is filed under a different DOI from
the paper.

Runs have retrieval; the commitments are absent from the publication, so retrieval
does not win. The publication hands over the Th1 claim, the protection figures and
the mechanism narrative, and it actively misleads on tolerability and on the
age-versus-formulation comparison.

### Anchor table
| Anchor | Value | Block | Steps | Legible? |
|---|---|---|---|---|
| Heterosubtypic survival | cand 57.1-100%, comp 0-28.6%, sham 0% across six configurations after collapsing S06-D into S06-C; cand separates from sham at p=0.0002 and from the comparator at p=0.0009 to 0.0151 in all six | S06-A, S06-B, S06-C, S06-E, S06-F, S06-G | 2 | yes |
| Natural-death ceiling | unvaccinated unchallenged arm S06-E 85.7%, S06-F 100%, S06-G 57.1%; in S06-G the candidate arm and that arm are both 4 of 7, p=0.855 | S06 rows 34-68, fifth arm | 2 | yes |
| Survival reaches young | cand vs young comparator not significant in any configuration (p=0.060 to 0.317, identical in S06-C) | S06 | 2 | yes |
| Within-age adjuvant effect | aged 1.65x to 24.35x, young 1.02x to 1.35x, across six blocks, seven panels, carrying the full 2x2 | S01-A, S01-E, S01-F, S01-G, S02-C, S02-E | 2 | yes |
| Age/formulation 2x2 | Ifnb1 16h: diagonal 0.99, formulation held 0.73. Ifnb1 72h: diagonal 2.78, formulation held 1.42, and young+cand 3.13 against young+comp 1.59 | S01-A rows 5, 8, 9, 10 | 2 | yes |
| Early protection | S06-B 71.4% challenged at d3; S03-J 100% challenged at d2, censored at d21 | S06-B, S03-J | 1 | yes |
| Day-3 lung CD8 | NP+ 6.68/2.09; Ki-67 9.38/3.48; GZMB 5.69/2.99 | S05-A, S05-D, S05-E | 1 | S05-A merged hdr |
| Blockade chain | CBX 7.28->3.08; IFNAR 19.70->2.09 with GM-CSF rescue 12.40; INCB 6.77->1.39 and 15.35->2.52; PTX lung 0.93x MLN 0.22x | S11-C, S02-H, S02-I, S07-B, S05-C | 1 each, 4 sheets | yes |
| Delivery depends on surfactant protein | WT 43.10 vs Sftpa1-/-Sftpd-/- 12.66 | S01-C | 1 | yes |
| GM-CSF 36h | 8.74 vs 1.59 vs 1.21 | S02-F | 1 | merged hdr, no young arm |
| 72h residual | Ccl2 27.41, Ccl3 9.23, Tnf 8.44, Il6 7.19, Il10 4.16, Ifnb1 4.01, Ccl5 2.01; young comparator 0.11 to 101.59 on the same analytes | S09-A block 2 | 3 | yes, header reads Log10 |
| Tolerability controls | S08-D cand 99.78 vs comp+R848 90.65 (min 84.7, 4 of 5 animals); S03-E cand 1.13-1.59 vs CT 2.68-5.50 | S08-D, S03-E | 1 | merged hdr |
| Dose plateau | 45.83 -> 50.23 (+9.6%) | S08-A | 1 | merged hdr |
| Corrected subclass | H1N1 comp 0.578, cand 2.144, young 2.972 against printed 2.972 / 0.578 / 2.144. H3N2 carries the same cyclic shift: 0.512 / 2.727 / 2.891 against printed 2.891 / 0.512 / 2.727 | S03-B/S03-F + S13-A-D | 3 | yes |
| Foreclosure for direction | subclass-sum/total-IgG 0.56/0.35/0.55 (H1N1) and 0.57/0.32/0.34 (H3N2) against 16.1x and 11.3x under the alternative | S03-A/S03-E + S13-A-D | 2 | yes |
| HAI | cand geo 367.6, arith 416.0; sham [10,10,10,0,0] arith 6.0 against a 1:10 floor | S03-C | 2 | yes |
| S06-C identical to S06-D | 28 of 28 (time,event) pairs | S06 | 2 | yes |
| Age-matched vs young, 18 endpoints | 18 of 18 directionally interpretable endpoints point the same way: 16 higher-is-better below 1.0 (0.406 to 0.987) and 2 higher-is-worse above it (Ifnb1 72h 2.78, Tfr 1.52). Same two endpoints read 18.1x and 8.0x against the age-matched arm | listed in derivation notes | 3 | yes |

### S06, full enumeration

| Block | Vaccine | Challenge | Day | Relation | cand | comp | sham | uninfected |
|---|---|---|---|---|---|---|---|---|
| S06-A | Aichi H3N2, 1 ug HA | PR8 H1N1, 5x mLD50 | 14 | heterosubtypic | 85.7% | 14.3% | 0% | — |
| S06-B | Aichi H3N2, 1 ug HA | PR8 H1N1, 5x mLD50 | 3 | heterosubtypic | 71.4% | 0% | 0% | — |
| S06-C | bivalent | rgH5N1, 5x mLD50 | 14 | heterosubtypic | 100% | 28.6% | 0% | — |
| S06-D | bivalent | rgH5N1, 5x mLD50 | 3 | heterosubtypic | 100% | 28.6% | 0% | — |
| S06-E | Aichi H3N2, 1 ug HA | PR8 H1N1, 5x mLD50 | 60 | heterosubtypic | 71.4% | 0% | 0% | 85.7% |
| S06-F | bivalent | rgH5N1, 5x mLD50 | 60 | heterosubtypic | 71.4% | 14.3% | 0% | 100% |
| S06-G | CA09 H1N1, 0.5 ug HA | Perth H3N2, 5x mLD50 | 60 | heterosubtypic | 57.1% | 0% | 0% | 57.1% |
| rows 69-70 cols G-L, labelled S06-E | bivalent, 14-month mice, prior PR8 or saline | PR8 H1N1, 5x LD50 | not stated | within H1N1 | 85.7% / 85.7% | 0% / 57.1% | n/a | — |
| rows 69-70 cols M-R, labelled S06-F | bivalent, 14-month mice, prior PR8 or saline | Perth H3N2, 5x LD50 | 14 | within H3N2 | 85.7% / 85.7% | 0% / 0% | n/a | — |

Log-rank, Mantel-Cox, pairwise, n=7 per arm, no multiplicity correction:

| Comparison | S06-A | S06-B | S06-C | S06-E | S06-F | S06-G |
|---|---|---|---|---|---|---|
| cand vs sham | 0.0002 | 0.0002 | 0.0002 | 0.0002 | 0.0002 | 0.0002 |
| cand vs comparator | 0.0083 | 0.0009 | 0.0068 | 0.0016 | 0.0094 | 0.0151 |
| cand vs young comparator | 0.317 | 0.141 | identical | 0.141 | 0.141 | 0.060 |
| cand vs uninfected | — | — | — | 0.594 | 0.141 | 0.855 |

The comparator adjuvant fails to separate from sham in S06-B (p=0.088), S06-E (p=0.111)
and S06-F (p=0.066).

One collapse and one retention, both derivable.

S06-D collapses into S06-C: all 28 (time, event) pairs are identical across all four
arms, so it is one experiment entered twice.

S06-G is retained and read against its own ceiling. Its unvaccinated, unchallenged arm
lost 3 of 7 animals by day 10 (days 3, 7 and 10), giving 57.1%, the same figure as
its candidate arm, p=0.855. The 57.1% is therefore not a weak protection result:
every animal in that experiment that did not die of age survived the infection. The
same arm ran 6 of 7 in S06-E and 7 of 7 in S06-F, so S06-G drew a frailer cohort. Dropping
the block is also defensible; reporting 57.1% as the weak end of a range without
reference to that arm is not.

With n=7 per arm, failure to detect a difference is not equivalence. Only S06-G is a
tight match. In S06-E the candidate arm is one animal below the uninfected arm and in
S06-F two below, and n=7 cannot resolve gaps that small in either direction. Word it
as not distinguishable at this sample size.

The two blocks at rows 69-70 are within-subtype heterologous, not heterosubtypic:
the bivalent vaccine contains CA09 H1N1 and Aichi H3N2 and the challenges are PR8
H1N1 and Perth H3N2. They support the imprinting claim and not the configuration
count.

### The age-versus-formulation 2x2

The workbook carries a young-plus-candidate arm in seven blocks that the source
never uses. Where it exists the confound closes.

| Readout | aged+comp | aged+cand | young+comp | young+cand | diagonal | formulation held |
|---|---|---|---|---|---|---|
| Ifnb1 16h (S01-A) | 16.64 | 37.11 | 37.60 | 50.70 | 0.987 | 0.732 |
| Ifnb1 72h (S01-A) | 3.43 | 4.43 | 1.59 | 3.13 | 2.785 | 1.416 |
| CD11b+ DC d4 (S01-E) | 8.28 | 18.88 | 21.40 | 22.60 | 0.882 | 0.835 |
| cDC1 72h (S01-F) | 22.80 | 37.52 | 43.42 | 44.26 | 0.864 | 0.848 |
| cDC2 72h (S01-G) | 75.30 | 59.46 | 54.08 | 51.36 | 1.099 | 1.158 |
| Antigen-bearing DC in MLN (S02-C) | 1.77 | 7.09 | 9.39 | 11.12 | 0.755 | 0.638 |
| OT-I proliferation (S02-E) | 0.77 | 18.65 | 26.24 | 31.40 | 0.711 | 0.594 |

Within-age adjuvant effect, candidate over comparator inside each cohort:

| Readout | aged | young |
|---|---|---|
| Ifnb1 16h | 2.23x | 1.35x |
| CD11b+ DC d4 | 2.28x | 1.06x |
| cDC1 72h | 1.65x | 1.02x |
| Antigen-bearing DC in MLN | 4.01x | 1.18x |
| OT-I proliferation | 24.35x | 1.20x |

Three consequences.

The 0.99 on Ifnb1 at 16h is an artifact of the diagonal. Hold formulation constant
and it is 0.73. The apparent match came from comparing the candidate against the
weaker product, not from the aged lung catching up.

Failure to resolve at 72h is a property of the formulation, not of the aged lung.
Young animals given the candidate sit at 3.13 against 1.59 for young animals given
the comparator, a 1.97x effect inside the young cohort. The diagonal reading of
2.78 halves to 1.42 once formulation is held constant.

The within-age comparison is the only one in the package free of the confound, and
it is the strongest thing in the package: the candidate adds 1.65 to 24x in aged
animals and 1.02 to 1.20x in young ones. That is the profile an adjuvant for the
elderly should have, and the source never states it.

Hard limit: no humoral or cellular endpoint carries the young-plus-candidate arm.
Of the 18 endpoints in the age-matched anchor, only Ifnb1 at 16h and at 72h can be
deconfounded. Both keep their sign under either reading.

### The two comparator gaps

No antigen dose-response exists anywhere in the room. HA content is 0.5 ug for CA09
H1N1 and 1 ug for Aichi H3N2 and is never varied within a strain. The room
therefore cannot separate an adjuvant effect from the effect of more antigen. That
is not a technical caveat: high-dose inactivated vaccine is the licensed standard of
care in 65+, so it is the comparator this asset is actually judged against. A
high-dose arm is the primary comparator for the next efficacy study, with the
age-matched predecessor adjuvant alongside it.

No blockade experiment carries a challenge arm. INCB3344 reduces lung GZMB+ CD8
from 6.77 to 1.39 (S02-I) and Ly6C+ macrophages from 15.35 to 2.52 (S07-B), and no
survival readout follows either. The causal chain is established
up to the immune readouts and assumed from there to protection.

### Absence anchors (assert mechanically)
adjuvant_program_annotation.pdf must NOT contain:
- any fold-change, ratio, percentage, effect size or p-value
- "transient", "resolved", "returns to baseline", "sustained", or any judgment
  about the duration of the innate response
- "restored", "youth-like", "comparable to young", "reaches the levels of"
- that the young-comparator arm is a benchmark or reference FOR anything
- that the unvaccinated unchallenged arm is a control FOR anything, or that deaths
  in it are background
- that any readout is higher-is-better or higher-is-worse, or what any readout
  indicates
- that any assay is strain-specific, homologous-only, a correlate or a surrogate
- that any two blocks share data, duplicate, or are mislabelled
- that any challenge is homologous, heterologous or heterosubtypic
- that the ratio panel was computed from the subclass panels
- which readouts are peripherally accessible
- how many panels have or lack source data
- any causal claim, including the direction of the blockade results
- the source's figure titles

adjuvant_program_annotation.pdf MUST contain: per block the measurand, units and scale, timepoint,
stated n, group identities and replicate count. Per block, the route of
administration and the dose for every agent given. Per challenge block, vaccine
composition including HA content, challenge virus, challenge dose as stated,
challenge day, mouse strain and age, stated per block and not globally. Per
immunoassay, the antigen used. For the fifth arm of S06-E, S06-F and S06-G, that those
animals received no vaccine and no challenge virus. Every intervention agent, named as the
source names it, with route and dose. Target is given only where it is part of the
compound's standard identifier, as in "CCR2 antagonist INCB3344". No mechanistic
gloss for established reagents: a working record names them and does not explain
them. Adjuvant identities and the single composition difference. Stated
statistical methods and summary measures, including that the S09-A panels are
normalised against untreated mice. That scRNA-seq was performed, on which cells,
when. Plus mLD50 determination and formulation specifications as non-load-bearing
noise.

Source inconsistencies reproduced verbatim and unremarked:
- both immunogen statements for S05-A, the second inside an unclosed parenthesis; S05-D,
  S05-E, S05-F, S05-G and S05-H read "vaccinated as in (B)" and (B) states no vaccination of
  its own; S05-I reads "vaccinated as in (A)"
- the NP366-374 tetramer against the stated BALB/c strain
- the stated n values that disagree with their own observation counts: S03-J header
  n=9 against arms of 10, 10 and 10; S05-A/S05-B
  header n=3 against 2 observations
- both S09-A headers reading 16h
- S06 rows 69-70 reusing the printed labels S06-E and S06-F for different content,
  so each label appears twice (the correspondence is in label-mapping.tsv)
- the S10 block labelled S10-A carrying S03-E content
- S03-J carrying three arms where the source legend names two, with a censoring
  day of 21 against 22 days of stated monitoring
- the rows-69-70 blocks stating the challenge dose as LD50 where every other
  challenge block states mLD50, and one of the two giving no challenge day
- GM-CSF administered intranasally in one experiment and intratracheally in another
- the OVA dose given as 30 ug in the legend and 30 ul in the methods

Do not carry into the annotation: the publication's own text states that the
day-60 experiment used the comparator-formulated vaccine and was fully protected,
which contradicts its own S06-E comparator arm at 0 of 7. That is a publication
error, not a room fact.

Per-block strain matters. The rows-131-161 blocks of the sheet labelled S15
are aged C57BL/6 and Swiss Webster, not BALB/c. The NP366-374 restriction
inconsistency is determinate only where the strain is stated block by block.

### Required tooling
openpyxl or pandas with openpyxl. No merged-cell handling in default reads. A
survival or log-rank implementation; lifelines is the obvious one. Confirm it
imports in the task image as the model user before launch: the sandbox is offline
and a missing package forces every attempt to hand-roll Mantel-Cox.

---

## 3. THE GOLDEN RESPONSE

### Spec

The recommendation is to advance, stated in the golden's own words. No position in
the answer is prescribed for it and none may be required by the grader: placement
and ordering requirements are prohibited, and with output headings deprecated any
such requirement is necessarily one the prompt did not set. The golden may open
with it, and does:

> (Illustrative only. The shipped golden is task/golden-response.md and has moved on
> from this wording; do not treat the block below as its current text.)
>
> Advance PSLN-344. In all six heterosubtypic challenge configurations it separated
> from the vaccine alone (p = 0.0002) and from the chemically matched predecessor
> adjuvant (p = 0.0009 to 0.0151) in 20-month-old mice, and on survival it was not
> distinguishable from young animals. The effect is a correction of an age-specific
> priming deficit: within the aged cohort the adjuvant adds 1.65 to 24-fold on
> innate and dendritic cell readouts, where the same comparison in young animals
> adds 1.02 to 1.20-fold. Next studies sample the adaptive compartment at day 7 to
> 10 against high-dose standard of care and the age-matched predecessor adjuvant.

### The spine, in eight steps

The golden's structure follows the reasoning the verdict actually rests on. Each
step is a conclusion in its own right, which is what the Stage 2 independent-causes
test now asks to be counted.

1. **Route and delivery.** Single intranasal dose with the vaccine. Uptake depends
   on surfactant protein A/D (S01-C, 43.10 in WT against 12.66 in the double
   knockout) and on gap-junction transfer into alveolar epithelial cells (CBX 7.28
   to 3.08). The asset is airway-specific by construction, which is why the safety
   package is nose, olfactory bulb and CNS against cholera toxin rather than
   systemic toxicology.
2. **It corrects an age-specific deficit rather than adding generic potency.** The
   within-age adjuvant effect, aged 1.65 to 24.35x against young 1.02 to 1.35x. The
   only comparison in the package free of the age/formulation confound.
3. **The mechanism is priming, not effector function.** Alveolar epithelial
   delivery, then type I interferon (IFNAR-/- 19.70 to 2.09, rescued to 12.40 by
   GM-CSF), then GM-CSF at 36h (8.74 against 1.59 and 1.21), then CCR2-dependent
   monocyte recruitment (6.77 to 1.39; 15.35 to 2.52), then monocyte-derived DCs,
   then priming in the draining node (PTX: MLN 0.22x, lung 0.93x). Every step sits
   upstream of the adaptive response.
4. **Adaptive output is elicited but sub-young.** Humoral 0.41 to 0.76 of the young
   arm, cellular 0.59 to 0.94, and 18 of 18 directionally interpretable endpoints
   point the same way. Real responses, causally downstream of step 3.
5. **Protection reaches young even though magnitude does not.** The clinical
   endpoint matches the young arm in every configuration while every immunological
   magnitude endpoint falls short of it. The markers do not have to match young;
   they have to clear a protective threshold.
6. **Timing.** Mouse primary CD8 responses to influenza peak at days 7 to 10, so
   the day-3 readouts sit inside the innate window. Adaptive sampling in the next
   study goes at day 7 to 10, not day 3.
7. **Carry-forward, and the three markers split three ways.** Marked as named
   domain knowledge. Antigen-specific CD8 and tissue-resident memory are accepted
   correlates of heterosubtypic protection and are carried forward on that basis;
   nothing in this package needs to demonstrate it. Their limit is access, not
   validity: in mice they are lung-local, so the clinical role is mechanistic and
   pharmacodynamic, read in challenge or lavage studies rather than as a routine
   endpoint. Antigen-specific antibody is an accepted correlate for matched strains
   only, and every immunoassay mounted here is homologous-antigen, so for the
   heterosubtypic indication it is unestablished and has to be tested. Its role is
   peripheral accessibility and the regulatory bridge, not the efficacy correlate.
   GM-CSF at 36h is the antigen-independent pharmacodynamic marker of adjuvant
   activity and carries the same lung-local access problem.
8. **The 72h non-resolution is a formulation property, not an ageing one.** Young
   animals given the candidate also fail to resolve, 3.13 against 1.59. A
   toxicology and CMC question rather than an efficacy one, and the gating study.

### What the package does not support

- Antibody as a correlate of heterosubtypic protection. Accepted for matched
  strains, unestablished across subtypes, and every immunoassay mounted is
  homologous-antigen. No block pairs a per-animal immune measurement with that
  animal's outcome, so nothing here can close that gap either. This does not apply
  to the cellular markers, which are carried on accepted grounds.
- Comparison against the relevant standard of care. High-dose inactivated vaccine
  is what this asset competes with in 65+, and HA content is never varied within a
  strain anywhere in the room, so no arm speaks to it.
- The step from improved priming to protection. No blockade experiment has a
  challenge arm.
- Any age-versus-formulation claim on an adaptive endpoint. The young-plus-candidate
  arm exists only on innate and dendritic cell readouts.
- Extension beyond influenza. No non-influenza pathogen antigen is mounted; OVA is
  a model protein.

### Forcing chain (23 route-necessary legs)

| # | Claim established | Mounted evidence |
|---|---|---|
| 1 | indicator 1 is death | joint distribution, 1 at d2-12, 0 only at the block's last day |
| 2 | which blocks are heterosubtypic | annotation, classified by the solver |
| 3 | cand and comp differ only by the Mn complex | annotation |
| 4 | the heterosubtypic set is derived | S06-D collapsed into S06-C on 28 of 28; rows 69-70 excluded as within-subtype |
| 5 | S06-G is read against its own ceiling | S06 rows 34-68, fifth arm, 3 events against 1 and 0 in the concurrent blocks |
| 6 | the fifth arm of S06-E/S06-F/S06-G received no vaccine and no challenge | annotation |
| 7 | protection exists at d2-d3 | S06-B, S03-J |
| 8 | that protection is not antibody-mediated | timing, naive animals, external kinetics |
| 9 | the aged/young diagonal varies two things | S01-A rows 9 and 10 carry both young arms |
| 10 | the within-age adjuvant effect is the clean comparison | S01-A, S01-E, S01-F, S01-G, S02-C, S02-E |
| 11 | endpoint direction must be established before pooling | 18-endpoint set; 2 endpoints invert |
| 12 | age-matched and young give opposite reads | 18 endpoints, unanimous |
| 13 | all immunoassays are homologous-antigen | annotation |
| 14 | antigen-independence, five immunogens | S03-I, S06-A, S06-C, S03-J, S02-E + annotation |
| 15 | chain established by blockade | S11-C, S02-H, S02-I, S07-B, S05-C |
| 16 | S09-A block 2 is the 72h panel | Ifnb1 4.01 against S01-A 72h; block 1 at 36.3 against 16h |
| 17 | S09-A is log10 | sheet header; PBS arm exponentiates to 1.00 |
| 18 | all seven analytes unresolved at 72h | block 2 exponentiated |
| 19 | non-resolution is a formulation property | young+cand 3.13 against young+comp 1.59 |
| 20 | tolerability assays carry controls | S08-D comp+R848, S03-E cholera toxin |
| 21 | dose at plateau | S08-A |
| 22 | no accessible antigen-independent marker | enumeration by compartment |
| 23 | no per-animal immune-to-outcome linkage exists | survival blocks carry only time and event |

Conditional legs, binding only if the solver uses the readout: S06-C identical to S06-D;
subclass panel inconsistent with the direction forced; HAI sham estimate below
assay floor; Tfh:Tfr an algebraic transform.

### Named domain knowledge, marked as such in the golden
Antigen-specific antibody (HAI at the conventional threshold) as an accepted
correlate of protection for matched influenza strains, and antigen-specific CD8 and
tissue-resident memory as accepted mechanistic correlates of heterosubtypic
protection; the absence of an agreed regulatory surrogate for heterosubtypic
protection. Primary humoral kinetics. Mouse primary CD8 kinetics, peak days 7 to 10
by epitope and tissue. Reciprocal dilution series, GMT convention, below-LOD
handling. NP366-374 H-2Db restriction against BALB/c H-2d. Sustained type I IFN
antagonising IFN-gamma responsiveness and B cell responses. Impaired inflammation
resolution in the aged airway. Cyclic dinucleotide therapeutic window. High-dose
inactivated vaccine as licensed standard of care in 65+. Influenza licensure
surrogates in older adults.

### Derivation notes

Survival from (time, event) pairs, percent censored at the block's own last day,
which is 14 everywhere except S03-J, where it is 21. Log-rank is Mantel-Cox, pairwise,
unadjusted for multiplicity, as in the source.

Subclass ratio per animal then group mean, not ratio of group means. H1N1 is S13-A
over S13-B, H3N2 is S13-C over S13-D. Both ratio panels carry the same cyclic column
shift: what is printed under the three labels belongs to the arms one position to
the left. Subclass sums against total IgG forecloses the direction: correct pairing
gives 0.559, 0.346, 0.551 for H1N1 against S03-A and 0.567, 0.319, 0.337 for H3N2
against S03-E, where the alternative requires one arm's two subclasses to sum to
16.1 times its own total IgG for H1N1 and 11.3 times for H3N2.

72h analytes as 10^mean(log10 replicates); the arithmetic reduction agrees within
10% and either is acceptable.

HAI as geometric mean; the sham arm requires a stated below-LOD convention. The
8.0x age-matched figure for HAI is geometric; arithmetic gives 8.67.

The 18 endpoints, aged candidate over young comparator, with direction:

| # | Endpoint | Figure | Direction | cand | young | ratio |
|---|---|---|---|---|---|---|
| 1 | Ifnb1 16h | S01-A | higher better | 37.11 | 37.60 | 0.987 |
| 2 | Ifnb1 72h | S01-A | **higher worse** | 4.43 | 1.59 | 2.785 |
| 3 | Ly6C+ monocytes d4 | S01-D | higher better | 30.56 | 32.22 | 0.948 |
| 4 | Alveolar macrophages d6 | S11-A | higher better | 31.00 | 46.88 | 0.661 |
| 5 | Total IgG H1N1 | S03-A | higher better | 7891.60 | 12775.00 | 0.618 |
| 6 | Total IgG H3N2 | S03-E | higher better | 6386.80 | 15722.40 | 0.406 |
| 7 | HAI H1N1, geometric | S03-C | higher better | 367.58 | 485.03 | 0.758 |
| 8 | IgG2a:IgG1, corrected | S03-B + S13-A/B | higher better | 2.14 | 2.97 | 0.721 |
| 9 | GC B cells | S03-K | higher better | 6.54 | 9.82 | 0.666 |
| 10 | ICOS-high Tfh | S04-A | higher better | 10.26 | 13.63 | 0.752 |
| 11 | Tfr | S04-B | **higher worse** | 10.80 | 7.12 | 1.517 |
| 12 | NP+ CD8 lung d3 | S05-A | higher better | 6.68 | 9.85 | 0.678 |
| 13 | NP+ CD8 lung d7 | S05-A | higher better | 14.25 | 15.15 | 0.941 |
| 14 | Ki-67+ CD8 d3 | S05-D | higher better | 9.38 | 9.94 | 0.944 |
| 15 | GZMB+ CD8 d3 | S05-E | higher better | 5.69 | 9.61 | 0.592 |
| 16 | IFN-gamma+ CD8, H5N1 restim d14 | S05-F | higher better | 6.36 | 9.18 | 0.693 |
| 17 | IFN-gamma+ CD8 d60 | S05-G | higher better | 9.86 | 14.36 | 0.687 |
| 18 | Lung TRM CD8 | S05-I | higher better | 3.96 | 6.04 | 0.656 |

All 18 point the same way: the candidate does not reach the young comparator.
Sixteen higher-is-better endpoints below 1.0 and two higher-is-worse endpoints
above it. Report the unanimity rather than a class mean: class means are sensitive
to membership and reduction and are not the fact that carries the pillar. Where a
mean is wanted, humoral rows 5 to 10 give 0.654 and cellular rows 12 to 18 give
0.741, both as a mean of per-endpoint ratios.

Rows 1, 3, 13 and 14 are effectively matched at 0.99, 0.95, 0.94 and 0.94. Name
them rather than folding them into a range: the candidate matches young on early
interferon induction, monocyte recruitment, day-7 NP-specific CD8 and CD8
proliferation, and falls short elsewhere.

GM-CSF at 36h is excluded from the 18. S02-F has only aged sham, aged comparator
and aged candidate arms, so 8.74 is a fold-change over untreated and not a ratio
against anything.

Rows 1 and 2 are the only two that can be deconfounded, and both keep their sign:
0.987 to 0.732 and 2.785 to 1.416.

---

## 4. PRE-REGISTERED FAILURE MODES

### False-optimum map, tier 1

| Mode | Fails to check | Why it attracts | Refuting fact | Counterfactual |
|---|---|---|---|---|
| confound-not-separated | that the aged-versus-young comparison varies adjuvant as well as age, where the young-plus-candidate arm sits in the same block | the source frames everything on the diagonal and the fourth arm is unlabelled in the narrative | S01-A rows 9 and 10; the 2x2 in five further blocks | reports the within-age adjuvant effect and notes that 0.99 on Ifnb1 becomes 0.73 |
| humoral-readout-carries-heterosubtypic-claim | that every mounted immunoassay is homologous-antigen | 18.1x IgG and four-figure neutralising titres are the largest numbers in the package | annotation, antigen per assay | carries the humoral data as immunogenicity and rests the heterosubtypic claim on the challenge and cellular data |
| resolution-not-addressed | the 72h panel at all, or its scale, or that it is unresolved, or proposes no work on it | listing it feels like diligence; every value reads near 1 unexponentiated | sheet header reads Log10; PBS arm exponentiates to 1.00; Ccl2 1.488 to 27.41x | finds all seven elevated and makes resolution kinetics the gating study |
| direction-not-established-before-pooling | that two of the 18 endpoints invert | every other endpoint reduces to lower-means-worse | Ifnb1 72h at 2.78 and Tfr at 1.52 are the candidate doing worse, not better | establishes each readout's direction, then reports 18 of 18 pointing one way |
| background-mortality-not-netted | that S06-E, S06-F and S06-G carry an arm receiving neither vaccine nor challenge | S06-G reads as the weak end of a range at 57.1% | S06 rows 34-68, fifth arm of S06-G: 3 of 7 dead by day 10, p=0.855 against the candidate arm | reports S06-G at its own ceiling, or sets it aside on that fact |
| correlates-listed-not-chain-established | the four blockade experiments | DC and Treg shifts are easier to read than interventions across four sheets | S11-C, S02-H, S02-I/S07-B, S05-C | builds the chain, and can then propose a PD marker |
| young-benchmark-as-acceptance-criterion | the age-matched comparison | the package nominates the young arm | the same endpoints invert, 0.76 against 8.0x; survival reaches young while magnitude does not | compares against high-dose standard of care in the aged population and does not require matching young to advance |

**Expected prevalence, highest to lowest.** All seven stay in the map and in the
grader's B list. The order is a prior for the FA, so that prevalence can be ranked
against it rather than discovered from scratch.

1. confound-not-separated. The source frames every age comparison on the diagonal,
   so a solver following the data's own framing lands here by default. As with mode
   7, absence is not evidence the confound was handled: a trajectory that never
   makes an aged-versus-young comparison gives a second annotator nothing to
   observe, so the FA should confirm the comparison was attempted before counting
   it either way.
2. resolution-not-addressed. Three chances to fail: find the second S09-A block,
   exponentiate it, then propose work rather than record a caveat.
3. background-mortality-not-netted. Requires noticing a fifth arm that exists in
   only three of the nine challenge blocks.
4. humoral-readout-carries-heterosubtypic-claim. The largest numbers in the package
   pull hard in this direction.
5. young-benchmark-as-acceptance-criterion. The package nominates the young arm, so
   taking it as the bar is the path of least resistance.
6. correlates-listed-not-chain-established. The blockade data are findable but sit
   across four sheets.
7. direction-not-established-before-pooling. Lowest, and for a structural reason
   rather than a confidence one: it can only fire if the solver chooses to
   aggregate the endpoint set at all. A solver that reports endpoints individually
   never faces the question. **Absence of this mode in a transcript is therefore
   not evidence that direction was handled correctly**, and the FA should check
   whether aggregation was attempted before counting it either way.

### Tier 2 watch list
innate-alternative-not-considered; early-readout-treated-as-adaptive;
adjuvant-effect-not-separated-from-antigen-dose;
priming-to-protection-step-assumed;
antibody-treated-as-heterosubtypic-correlate; standard-of-care-comparator-omitted;
duplicated-blocks-treated-as-independent;
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
| indicator 1 as alive | natural reading | a 14-day study cannot record survivors dying at d4 | S06, S03-I/J |
| evaluate on homologous blocks | S03-I 100% is the cleanest number | those challenge viruses are in the vaccine | annotation |
| count rows 69-70 toward the heterosubtypic set | the sheet labels them S06-E and S06-F | the bivalent vaccine contains both challenge subtypes | annotation |
| report S06-G as the weak end of a range | it is a labelled, independent, durable challenge block | its unvaccinated unchallenged arm is also 57.1%, against 85.7% and 100% in the two concurrent blocks | S06 rows 34-68 |
| read aged-vs-young as an ageing effect | the source frames it that way throughout | the same block carries a young-plus-candidate arm | S01-A rows 9 and 10; S01-E, S01-F, S01-G, S02-C, S02-E |
| pool all endpoints on sign alone | 16 of 18 run the same way | Ifnb1 72h and Tfr invert; pooling them cancels the signal | 18-endpoint set |
| power on antibody titre | largest effects in the package | homologous-antigen only; titre is the antigen's property | annotation |
| early protection as antibody | antibody is the default mechanism | d2-d3 in naive animals, unadjuvanted arm 0-10% | S06-B, S03-J + external |
| cellular without addressing innate | d3 cellular data are positive | innate still running at 72h, and d3 is inside the innate window | S09-A block 2 + external kinetics |
| transience from Ifnb1 or in log space | Ifnb1 is the headline analyte | 7 of 7 elevated; Ccl2 27.41x | S09-A + units |
| 72h state is within the young range | young runs 101.59 on Ccl2 and 41.45 on Ccl3 against 27.41 and 9.23 | the direction inverts rather than the degree: young is at or below its untreated reference on Tnf 0.48, Il10 0.11, Ccl5 0.55 and Ifnb1 1.39 where the aged candidate is 8.44, 4.16, 2.01 and 4.01 | S09-A block 2, all four arms |
| 72h non-resolution as an aged-lung property | the asset is an ageing asset | young animals given the candidate also fail to resolve | S01-A rows 9 and 10 |
| S06-C and S06-D as two experiments | differently labelled | 28 of 28 identical | S06 |
| 69x HAI rise | arithmetic mean is the library default | implies a sham titre of 6.0, below a 1:10 floor | S03-C |
| subclass ratio as printed | it is the panel built for it | one arm's subclass sum would exceed its own total IgG by 16.1x for H1N1 and 11.3x for H3N2 | S03-B/S03-F, S13-A-D, S03-A/S03-E |
| import the mechanism narrative | retrieval supplies it | no sequencing data mounted | annotation + absence |
| young benchmark as sole basis | package nominates it | NONE in the room | - |

### Grader guidelines (ABC skeleton)

Re-audited against the golden after its last edit, per the build constraint. Two A
items were added at that pass: the golden makes high-dose standard of care the
primary comparator for the efficacy study, which the earlier wording did not
capture and which an age-matched-only requirement does not discriminate; and the
prompt asks directly whether a biomarker could go into patients and in what role,
which A did not check at all.

Derived mechanically from the forcing chain and the expected-to-fire tier. Not
polished, not exhaustive. B carries only the tier-1 modes, each phrased as
something a reader can see the model do or skip, so B doubles as the FA lookup.
Nothing here requires content to appear in any particular place or order: placement
and ordering count as structure, and with output headings deprecated any placement
requirement would be one the prompt did not set. Written flat for pasting.

### Grader framing

You are grading a response to a portfolio-review request on PSLN-344, a manganese-complexed pulmonary-surfactant-biomimetic liposomal STING agonist developed as an adjuvant for influenza A vaccines in older adults. The solver had the study's per-animal data workbook and a per-block annotation, and was asked whether to advance the asset, what is driving the protection, whether a biomarker is worth carrying forward and could go into patients, what the next studies must establish, and what was ruled out. Grade content for presence and correctness only. Do not grade where in the answer anything sits or in what order it appears. Sections A and B overlap deliberately: A lists what a correct route must establish and B lists the errors expected to occur, so the same passage can bear on an item in each. Where it does, credit or penalise it once and not both; a response is never both credited under A and penalised under B for one and the same passage.

A. Must be present and correct: thirteen separately scored items, so that a response satisfying one half of a requirement and failing the other is not credited for both. (1) a recommendation on whether to advance; (2) that recommendation grounded in the heterosubtypic challenge blocks rather than in any humoral readout; (3) a heterosubtypic set that is derived rather than asserted; (4) every block placed in or out of that set on a stated mounted fact, whether collapsed, retained or set aside; (5) recognition that the aged-versus-young comparison varies adjuvant as well as age wherever both young arms exist in the same block; (6) the direction of each endpoint established before any pooling or averaging; (7) a next-study comparator set that is age-matched rather than young; (8) the antigen-dose comparison the package cannot answer, named as something the next studies must establish; (9) a biomarker answer that separates what is peripherally accessible from what is not; (10) no antibody measure offered as the cross-subtype efficacy correlate; (11) resolution kinetics proposed as work rather than inventoried as a caveat; (12) the priming chain rested on the blockade experiments rather than on correlation; (13) the limit stated that none of those blockade experiments carries a challenge endpoint, so the step from priming to protection is inferred rather than shown. Each item is met only where the attempt's own cited numbers reproduce from the mounted files by the route it states, so that the model is shown to have made the right call over the appropriate data.

B. Penalise, as ten separately identified items, which double as the lookup for the pre-registered failure modes: (1) powering a protection readout on antibody titre, or resting the heterosubtypic claim on assays run against the vaccine's own antigens; (2) reporting the S09-A analyte values as linear without exponentiating the log10 scale its own sheet header states, which is an error about scale and does not depend on which timepoint the second block is taken to be; (3) identifying the elevation at the later timepoint and proposing no work on its resolution; (4) building an age-gap, restoration or age-gap-closure metric whose denominator varies adjuvant as well as age, meaning aged-plus-candidate over young-plus-predecessor, in a block that also carries a young-plus-candidate arm which would have held formulation constant, where it is the denominator that matters and not whether the word young appears; an aged-versus-young comparison that does hold formulation constant is a clean comparison and is not this penalty; (5) pooling endpoints of opposite stated direction without reorienting them, so that the higher-is-worse endpoints offset the rest instead of adding to it; (6) reporting S06-G without reference to its unvaccinated unchallenged arm, except where the response sets the block aside on another stated mounted fact; (7) treating S06-C and S06-D as independent experiments; (8) listing the DC and Treg shifts as the mechanism, and nominating them as the mechanism, without reaching the blockade experiments; (9) declining to advance, or materially discounting the asset, solely because the aged arm falls below the young arm on immunological magnitude; (10) proposing an adjuvant-alone or antigen-free arm at the short challenge interval, in order to discriminate a non-specific antiviral state from primed immunity, without engaging S15-H, which already carries that arm at that interval and settles it. Proposing the arm at a later interval, or for tolerability, pharmacodynamic or formulation reasons, is not this penalty.

C. Neutral: number of studies proposed; whether the response raises the non-specific-antiviral-state alternative at all, and if it does, whether it retires it on S15-H or on the day-7-to-10 timing of a primary CD8 response; statistical method choice; whether the stated-n mismatches are noticed, or the block-label defects that carry no identity consequence, meaning the S10-A block holding S03-E content and the two printed labels that each appear twice on the S06 sheet, read as labels, meaning that noticing or not noticing the duplication is neutral; this does not extend to where the rows-69-70 blocks belong, and counting them toward the heterosubtypic set is not neutral but a failure of A items 3 and 4, since the vaccine in those blocks contains both challenge subtypes; this does not extend to the S06-C and S06-D data identity, which B covers; retention of humoral readouts as a regulatory bridge or as immunogenicity; whether S06-G is retained at its ceiling or set aside on that same fact; route, units, layout, length, and where in the answer anything sits.

---

## 5. SUPPORTING

### Hidden basin
The package nominates a comparison that varies two things at once, and its largest
effects are in readouts that cannot carry the claim it is being used to make.

### Verdict and pillars, one line each
- Advance, on heterosubtypic survival in six configurations against both sham and
  the chemically matched predecessor.
- The asset's value is the adjuvant effect within the aged cohort, not any
  aged-versus-young ratio.
- The mechanism is priming, established step by step by blockade, and it stops
  short of protection.
- Adaptive output is elicited but does not reach young on any of 18 endpoints,
  which is not disqualifying because survival does.
- The innate response has not resolved at 72h, and that is a property of the
  formulation rather than of the aged lung.

### Panel geometry
16 independent samples. No subagent fanout; correlated arms give sixteen versions
of one trajectory and a thin mode set.

### Known risks and open questions
1. The young-benchmark mode has no refuting fact in the room. The defence is that
   recognising differential benchmarks by age is competence, not a trick. The
   confound finding partly supersedes it: the stronger version of the same point is
   that the comparison varies two things, and that one does have a mounted refuting
   fact.
2. Resolved. The prompt carries no fabricated content. The committee date and the
   GLP slot are gone and the hedge is closed by requiring a defensible case either
   way. The cost is that deferral is no longer expensive as a fact about the world.
3. Resolved. The H-2Db restriction call holds: NP366-374 is the H-2Db-restricted
   epitope and the stated strain is BALB/c, H-2d. The BALB/c-dominant NP epitope is
   NP147-155 on H-2Kd. Determinate only where the annotation states strain per block.
4. Three products rest on annotation alone (legs 2, 3, 13). A thin or ambiguous
   annotation there breaks the protection and carry-forward pillars rather than
   making them hard. Leg 17 is no longer on that list; the scale is in the workbook
   header.
5. S11-A and S11-B share 35 of 100 cells, the first two animals of every group at every
   timepoint. Suggestive of partial copy. Not determinate; no mode rests on it.
6. The S06-G retention rests on the three day-60 blocks being comparable. If a reviewer
   treats 3 of 7 against 1 of 7 as within noise, the fallback is to set S06-G aside on
   the same fact. Both readings are in the C list; silence is in B.
7. The direction-adjudication mode rests on external knowledge: that residual
   interferon at 72h and a higher suppressive Tfr frequency are both bad. The first
   is consistent with the task's own tolerability pillar. The second is the softer
   call and is the leg a reviewer will press.
8. New. S05-A's immunogen is irreducibly ambiguous and the ambiguity reaches
   three of the cellular endpoints (rows 12, 13 and 18, since S05-I reads "as in (A)").
   Nothing in the source resolves it, so a solver cannot resolve it either. The
   day-3 cellular case therefore rests on S05-D and S05-E, and S05-A is cited with the
   ambiguity named. This is variance, not difficulty, and must not carry a mode.

### Build constraints
- Anchors carrying tier-1 modes must be legible under more than one extraction
  strategy. The 72h panel is verified: header, PBS-arm value and cross-block Ifnb1
  match all give the same reading. The 2x2 is verified: the fourth arm is a labelled
  column in the same block as the other three.
- Absence anchors asserted mechanically, not checked by eye. The two new ones are
  that no readout is described as higher-better or higher-worse, and that the
  unvaccinated unchallenged arm is never said to be a control for anything.
- The golden is recomputed from the shipped data room after its last edit, and every
  A item is re-read against the golden after any change to it.
- Confirm a log-rank implementation imports in the task image as the model user.
- Validate ceiling and floor: that a strong attempt working only from the room
  reaches the verdict, and that the obvious first pass does not.

### What changed after revision 3

- Cellular correlates decoupled from the demonstration requirement. Antigen-specific
  CD8 and TRM are accepted correlates of heterosubtypic protection and are carried
  on that basis; the no-linkage fact about the room applies only to antibody, where
  the cross-subtype correlate is genuinely unestablished.
- High-dose inactivated vaccine named as the primary comparator for the next
  efficacy study, since it is the licensed standard of care in 65+ and therefore
  what the asset is judged against.

### What changed in revision 3
- S06-G retained and read against its own ceiling, with the full log-rank table.
  The headline is no longer a survival range but separation from sham and from the
  chemically matched comparator in all six configurations, plus no detectable
  difference from young on survival.
- The age/formulation confound written in as a data-room section, two anchor rows
  and a tier-1 mode. The within-age adjuvant effect becomes the lead argument and
  the first line of the golden.
- The endpoint set fixed at 18, with direction stated per endpoint, the unanimity
  claim replacing the class means, and direction-adjudication added as forcing-chain
  leg 11 and a tier-1 mode.
- The eight-step spine written in as the golden's structure.
- The resolution pillar reframed: non-resolution is a formulation property, shown
  inside the young cohort, not an aged-lung property. log-scale-not-converted
  collapsed into resolution-not-addressed, since both reach the same conclusion.
- Readout timing added: day 7 to 10 for adaptive sampling, with mouse CD8 kinetics
  as named domain knowledge.
- Correlates handled on field-established grounds as named domain knowledge, with
  the narrower room-specific constraint kept: the mounted immunoassays are all
  homologous-antigen, and no block links a per-animal immune measurement to that
  animal's outcome.
- Two comparator gaps added: no antigen dose-response anywhere, and no blockade
  experiment with a challenge arm.
- Route of administration added to the annotation must-contain list, with the
  GM-CSF route inconsistency and the OVA ug/ul inconsistency added to the
  reproduce-verbatim list.
