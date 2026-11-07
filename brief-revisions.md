# Anton Task Brief psql25c1 — revisions to sections 2, 3, 4, 1

Every number below was recomputed from `adz5242_data_file_s1.xlsx` in this session.
Legend facts are from the unmounted publication (Gao et al., Sci Immunol 2026, adz5242)
and its supplementary materials, which stay out of the room and feed `trial_summary.md`.

---

## 1. The protection anchor: two exclusions, both derivable

### What Fig. 6 actually contains

| Block | Vaccine | Challenge | Challenge day | Relation to vaccine | AMnESTI | comparator | sham |
|---|---|---|---|---|---|---|---|
| 6A | Aichi H3N2, 1 µg HA | PR8 H1N1, 5x mLD50 | 14 | heterosubtypic | 85.7% | 14.3% | 0% |
| 6C | Aichi H3N2, 1 µg HA | PR8 H1N1, 5x mLD50 | 3 | heterosubtypic | 71.4% | 0% | 0% |
| 6E | bivalent | rgH5N1, 5x mLD50 | 14 | heterosubtypic | 100% | 28.6% | 0% |
| 6G | bivalent | rgH5N1, 5x mLD50 | 3 | heterosubtypic | 100% | 28.6% | 0% |
| 6H | Aichi H3N2, 1 µg HA | PR8 H1N1, 5x mLD50 | 60 | heterosubtypic | 71.4% | 0% | 0% |
| 6I | bivalent | rgH5N1, 5x mLD50 | 60 | heterosubtypic | 71.4% | 14.3% | 0% |
| 6J | CA09 H1N1, 0.5 µg HA | Perth H3N2, 5x mLD50 | 60 | heterosubtypic | 57.1% | 0% | 0% |
| rows 69-70, cols G-L (labelled 6H, content 6K) | bivalent, 14-month mice, prior PR8 or saline | PR8 H1N1, 5x LD50 | not stated | within H1N1 | 85.7% naive, 85.7% imprinted | 0% / 57.1% | n/a |
| rows 69-70, cols M-R (labelled 6I, content 6L) | bivalent, 14-month mice, prior PR8 or saline | Perth H3N2, 5x LD50 | 14 | within H3N2 | 85.7% naive, 85.7% imprinted | 0% / 0% | n/a |

Natural-death arm (20-month-old, no vaccine, no challenge), present in 6H, 6I and 6J only:

| Block | n | deaths | days | survival |
|---|---|---|---|---|
| 6H | 7 | 1 | 4 | 85.7% |
| 6I | 7 | 0 | — | 100% |
| 6J | 7 | 3 | 3, 7, 10 | 57.1% |

### The two exclusions

**6G collapses into 6E.** All 28 (time, event) pairs are identical across all four arms.
One experiment, not two.

**6J cannot carry a protection estimate in either direction.** Its untreated,
unchallenged arm lost 3 of 7 animals by day 10, giving 57.1%, which is the same figure
as its AMnESTI arm. Background mortality and challenge mortality are not separable
inside that block. The same arm in the two concurrently designed day-60 blocks ran at
85.7% (6H) and 100% (6I), so 6J is the outlier rather than the rule.

Five independent heterosubtypic configurations remain: 6A, 6C, 6E, 6H, 6I.
AMnESTI 71.4 to 100%, age-matched comparator 0 to 28.6%, sham 0% in all five.

**Net the day-60 blocks against the ceiling.** In 6H the achievable ceiling is 85.7%,
not 100%, so AMnESTI recovers 71.4 of an available 85.7 against a sham of 0.
In 6I the ceiling is 100%.

**6K and 6L are not heterosubtypic.** The bivalent vaccine contains CA09 H1N1 and
Aichi H3N2; the challenges are PR8 H1N1 and Perth H3N2. Both are within-subtype
heterologous. They support the imprinting claim, not the heterosubtypic count.

### Replacement anchor-table row

| Anchor | Value | Block | Steps | Legible? |
|---|---|---|---|---|
| Heterosubtypic survival | cand 71.4-100%, comp 0-28.6%, sham 0%, over five independent configurations after collapsing 6G into 6E and setting 6J aside | 6A 85.7/14.3, 6C 71.4/0, 6E 100/28.6, 6H 71.4/0, 6I 71.4/14.3 | 1 | yes |
| Natural-death ceiling | 6H 85.7%, 6I 100%, 6J 57.1% in the unvaccinated unchallenged arm | Fig.6 rows 34-68, fifth arm | 1 | yes |

### Replacement golden first line

> Advance AMnESTI into the GLP toxicology slot. The case is heterosubtypic survival in
> 20-month-old mice across five independent challenge configurations (71.4 to 100%
> AMnESTI against 0 to 28.6% for the same vaccine with the comparator adjuvant and 0%
> sham), and the next studies are powered on the day-3 lung CD8 readout against an
> age-matched comparator, not on any antibody titre.

### New tier-1 mode

| Mode | Fails to check | Why it attracts | Refuting fact | Counterfactual |
|---|---|---|---|---|
| background-mortality-not-netted | that the day-60 blocks carry an arm receiving neither vaccine nor challenge, and that in 6J that arm lost 3 of 7 by day 10 | 6J reads as a sixth configuration at 57.1%, which either drags the headline range down to 57-100% or gets dropped silently | Fig.6 rows 34-68, fifth arm of 6J: events at days 3, 7 and 10 of 7 animals, against 1 of 7 in 6H and 0 of 7 in 6I | sets 6J aside on a stated mounted fact and reports 71.4-100% across five; or retains it and states that the two mortality sources are not separable |

### New tier-2 watch item

`within-subtype-challenge-counted-as-heterosubtypic`: counting the rows-69-70 blocks,
or 3I, toward the heterosubtypic configuration count.

### Forcing chain, amended legs

- **4** (was: heterosubtypic protection, 5 blocks) now reads: the heterosubtypic set is
  *derived*. 6G collapsed into 6E on 28 of 28 identical pairs; 6J set aside on its own
  natural-death arm; rows 69-70 excluded as within-subtype. Route-necessary.
- **New leg 21**: the fifth arm of 6H, 6I and 6J received neither vaccine nor challenge,
  so any death in it is background. Route-necessary for any solver that reads 6J.

### Grader, amended

- **A** add: the heterosubtypic set is derived rather than asserted, with any block
  collapsed or set aside on a stated mounted fact.
- **B** add: reporting a protection range that includes Fig. 6J without reference to its
  unvaccinated unchallenged arm; counting the rows-69-70 blocks as heterosubtypic.

---

## 2. The resolution pillar: name the comparison

72h panel, fig. S2A block 2, 10^mean(log10 of 3 replicates), normalised to the PBS arm:

| Analyte | aged sham/PBS | aged comparator | aged AMnESTI | young comparator |
|---|---|---|---|---|
| Ifnb1 | 1.00 | 3.40 | 4.01 | 1.39 |
| Il6 | 1.00 | 1.86 | 7.19 | 3.10 |
| Ccl2 | 1.00 | 5.23 | 27.41 | 101.59 |
| Ccl3 | 1.00 | 4.73 | 9.23 | 41.45 |
| Ccl5 | 1.00 | 1.21 | 2.01 | 0.55 |
| Tnf | 1.00 | 5.23 | 8.44 | 0.48 |
| Il10 | 1.00 | 4.18 | 4.16 | 0.11 |

### The escape the brief leaves open

A solver can say, defensibly, that the 72h profile sits inside the young benchmark's
range: young runs 101.59 on Ccl2 and 41.45 on Ccl3 against AMnESTI's 27.41 and 9.23.
That is a careful expert defending the choice, which is the FA bar failing.

### What forecloses it

The direction inverts rather than the degree. On four of the seven analytes the young
arm at 72h is at or below its own untreated reference (Tnf 0.48, Il10 0.11, Ccl5 0.55,
Ifnb1 1.39) while AMnESTI in the aged lung is at 8.44, 4.16, 2.01 and 4.01. The young
lung has cleared the type I IFN and TNF axis and retains chemokine; the aged AMnESTI
lung has cleared nothing. All seven analytes are above the untreated reference, and
none is below the age-matched comparator. That is a different state, not a milder one.

### Pillar as it should read

The claim is not that 72h inflammation is high. It is that at 72h the aged AMnESTI lung
has not begun to resolve on the axis the young lung has already resolved on, and the
package contains no timepoint past 72h on any arm. Duration of the innate response is
therefore unmeasured, not measured and acceptable.

Gating study, in the form the prompt asks for:

- **Endpoint**: time to return of Ifnb1, Tnf, Il10 and Ccl5 to the untreated reference
  in lung, with lung histopathology and body weight as supporting endpoints.
- **Population**: 20-month-old animals, the same strain and route as the mounted work.
- **Comparators**: age-matched adjuvant comparator and untreated age-matched, with the
  young arm retained as context rather than as the acceptance criterion.
- **Readouts**: the same seven-analyte panel, reported on the linear scale with the
  reduction stated.
- **Timing**: extends past 72h until the age-matched untreated reference is reached;
  the mounted data fix 16h and 72h only, so the sampling has to run beyond both.

### Annotation consequences

`trial_summary.md` must state, per fig. S2A block: the analyte names, the units and
scale, the timepoint, n=3, the group identities, and that values are normalised against
untreated mice. It must not say "transient", "resolved", "returns to baseline",
"sustained", or anything about duration, and must not say the young arm is a benchmark.

Note for the mode write-up: `log-scale-not-converted` is refuted by the sheet header
itself, which reads `Fig. S2A 16h n=3 Log10`, not by the annotation. The PBS arm means
exactly 1.00 after exponentiation in all 14 analyte-blocks, which is a second cue
available without reading the header. Cite the header, not the companion document.

---

## 3. Prompt: add the set-aside ask

The golden spec carries "the set-aside material" as a product. The draft prompt never
asks for it, which makes it unrequested analysis in the golden. One sentence fixes both
that and the missing exclusions heading.

### Revised draft (257 words)

> We have AMnESTI, a manganese-complexed pulmonary-surfactant-biomimetic liposomal STING
> agonist, in preclinical development as a mucosal influenza vaccine adjuvant for
> heterosubtypic protection in older adults.
>
> Tell me whether we advance it, and what the next studies have to show. The programme
> committee meets on 20 November and the GLP toxicology slot we are holding releases if
> we do not commit at that meeting, so I need a decision, not a deferral.
>
> Everything we have is in /tmp/world/filesystem. It is a working directory rather than a
> curated one, so some of it will not bear on the decision. All figures, findings and
> conclusions must be grounded in those files rather than in outside sources. Perform
> your analysis as of 6 November 2026.
>
> Build me the proposal and lead with your recommendation on the first line
> (/tmp/outputs/answer.md). Structure the rest as you see fit.
>
> It has to be highly defensible. Every claim and every number needs explicit reasoning,
> the file it came from and how it was reduced. Save any analysis you run under
> /tmp/outputs.
>
> The committee will want the effectors driving the protection, any biomarker of efficacy
> worth carrying forward, and for each study you propose: endpoints, populations,
> comparators, readouts and timing.
>
> Tell me as well what you set aside and why, item by item, including anything in there
> that does not bear on the decision.
>
> Keep this at the level of study design, specification and interpretation of the mounted
> data. No bench protocols.

Changes: "rather than in outside sources" closes the mounted-only line; the set-aside
paragraph mandates the exclusions heading. The wording stops short of saying that any
particular result is unsound, so no trap is flagged.

Audit against the prompt-craft checklist: no persona, no numbered steps, no tool names,
no explained science, no answer taxonomy, load-bearing sources unnamed, as-of date fixed
and past, deliverable paths named, basis required per number, exclusions mandated, scope
line present and forbidding nothing the prompt requires, under 600 words. The
institutional framing that the refusal field note calls for is carried by "in
preclinical development" and "the programme committee", which is the thing that took an
earlier panel from 0 of 16 to 7 of 16.

---

## 4. The age-matched anchor: replace the means

The means in the brief do not reproduce. Across the 13 humoral and 6 cellular paired
endpoints, the mean AMnESTI/young ratio computes to 0.561 humoral and 0.718 cellular on
arithmetic group means, and 0.542 humoral on geometric means. Neither route gives 0.65
and 0.74.

The two named endpoints do reproduce exactly, and the reduction matters for one of them:

- **18.1x**: H1N1 serum IgG, Fig. 3A, arithmetic group means, 7891.6 / 437.0 = 18.06.
- **8.0x**: H1N1 HAI, Fig. 3C, geometric group means, 367.58 / 45.95 = 8.00.
  The arithmetic reduction gives 8.67 instead.

### What to use instead

Unanimity, which is stronger than a mean and reproduces by either route:

> Across 19 paired endpoints, every one reads below 1 against the young arm (range 0.357
> to 0.954) and above 1 against the age-matched arm (range 2.31x to 20.70x). There are no
> exceptions in either direction. The same two endpoints that read 0.62 and 0.76 against
> the young arm read 18.1x and 8.0x against the age-matched arm.

Blocks: humoral 3A, 3C, 3D, 3E, 3G, 3H, S8A, S8B, S8C, S8D, S8H, S8I, S8J;
cellular 5E, 5F, 5K, 5L, 5M, 5N.

### Replacement anchor-table row

| Anchor | Value | Block | Steps | Legible? |
|---|---|---|---|---|
| Age-matched vs young | 19 of 19 paired endpoints below 1 against young (0.357-0.954) and above 1 against age-matched (2.31-20.70x); H1N1 IgG 18.1x / 0.62, H1N1 HAI 8.0x geometric / 0.76 | 13 humoral + 6 cellular, listed above | 2 | yes |

`young-benchmark-as-sole-basis` keeps its force. The refuting fact is the unanimity, not
a mean, and it is the same fact under any reduction the solver picks.

---

## Items for the companion document, found while checking

Source inconsistencies to reproduce verbatim and unremarked, in addition to those
already listed:

- Fig. 3J carries three arms in the workbook (sham, comparator, candidate); the source
  legend names two. Its censoring day is 21, not 14, and the legend states 22 days of
  monitoring against a stated n of 10 and a sheet header of n=9 over arms of 10, 10 and 9.
- The 6K legend gives the challenge day as "d.p.i." with no number. 6K and 6L state the
  challenge dose as 5x LD50 where every other challenge block states mLD50.
- Fig. 5A's two immunogen statements are both in the legend, the second inside an
  unclosed parenthesis. 5E and 5F read "vaccinated as in (B)", and (B) states no
  vaccination of its own, so their immunogen resolves only through 5A's parenthetical.

Do not carry into the annotation: the publication's own text states that the day-60
experiment used the comparator-formulated vaccine and was fully protected, which
contradicts Fig. 6H's comparator arm at 0 of 7. That is a publication error, not a room
fact. The MDAR checklist shipped in the supplement zip is filed under a different DOI
from the paper; it is not part of the room.

Blocks whose arms the annotation must label per block rather than globally: the
rows-131-161 blocks of the sheet labelled Fig. S13 are aged C57BL/6 and Swiss Webster,
not BALB/c. The NP366-374 restriction inconsistency is determinate only where the strain
is stated per block.
