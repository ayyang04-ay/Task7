# psql25c1 — Phase 2 probe notes

## Probe 1 (2026-11-13) — Mode 2's defensibility, full 72 h context

**Asked for:** the full 72 h context, to test whether "the residual innate elevation was
left out of the forward view" survives the defensibility bar.

**Result: it does not. Mode 2 is retracted.** Two independent reasons, either of which
would be enough. The evidence is below so the retraction can be checked rather than taken.

---

### 1. The 72 h signal is not candidate-specific on the comparison that holds age constant

`S09-A` panel 2 (the panel printed 16 h that holds the 72 h data), n = 3 per arm,
geometric mean fold over untreated. Welch t on the log10 values as stored, computed by
hand — no scipy in this container.

| Analyte | aged candidate | aged parent | young parent | candidate ÷ aged parent | p | candidate ÷ young parent | p |
|---|---|---|---|---|---|---|---|
| Ifnb1 | 4.01 | 3.40 | 1.39 | 1.18 | 0.665 | 2.87 | 0.109 |
| Il6 | 7.19 | 1.86 | 3.10 | **3.85** | **0.026** | 2.32 | 0.085 |
| Ccl2 | 27.41 | 5.23 | 101.59 | **5.24** | **0.010** | **0.27** | **0.011** |
| Ccl3 | 9.23 | 4.73 | 41.45 | 1.95 | 0.076 | **0.22** | **0.011** |
| Ccl5 | 2.01 | 1.21 | 0.55 | 1.66 | 0.082 | 3.68 | 0.076 |
| Tnf | 8.44 | 5.23 | 0.48 | 1.62 | 0.052 | **17.76** | **0.008** |
| Il10 | 4.16 | 4.18 | 0.11 | **1.00** | **0.991** | **36.59** | **0.002** |

And the n = 5 block, `S01-A` Ifnb1 at 72 h, arm means over five animals:
sham 0.996, aged parent 3.432, aged candidate 4.428, young parent 1.590, young
candidate 3.128. Candidate against aged parent: ratio 1.29, **p = 0.262**. Candidate
against young parent: 2.78, p = 0.017. Candidate against young candidate: 1.42, p = 0.176.

Three things follow.

- **Against the age-matched parent the candidate is indistinguishable at 72 h on Ifnb1
  (both blocks), Il10 (1.00×, p = 0.991), and borderline on Tnf, Ccl3 and Ccl5.** Only
  Il6 is a clean candidate-specific excess. So "the manganese leaves a prolonged
  inflammatory tail" is not what the room shows; the tail is a property of the aged lung
  on this liposome platform.
- **On two analytes the young animals are the high ones.** Ccl2 101.59 and Ccl3 41.45 in
  young parent against 27.41 and 9.23 in aged candidate. The sentence "the young profile
  has resolved and the aged has not" is true for Tnf, Il10, Ccl5 and Ifnb1 and false for
  Ccl2 and Ccl3.
- **The dramatic figures the panel quotes are Mode 1's confound again.** Tnf 17.8×,
  Il10 36.6×, Ifnb1 2.85× / "285 % of young" are all candidate-over-**young-parent**.
  The age-matched versions are 1.62×, 1.00× and 1.18–1.29×.

**Consequence for my own ledger wording, which was overclaiming.** The retracted Mode 2
counterfactual read "Seven analytes sit above the untreated reference at the last measured
timepoint." That is true and nearly vacuous: so does the aged parent arm, and on two
analytes the young arm is several-fold higher. A reviewer would have asked for the
age-matched column, and the age-matched column is what dissolves the mode.

### 2. Each of the four runs either used the panel and proposed work on it, or set it aside on a stated mounted fact

Read in full, not screened.

| Run | What it actually did |
|---|---|
| O4 | **Identified, quantified, caveated and designed around it.** Integrity item Q11 scopes the duplication to the Ifnb1 row and says the panel "is used only for the other cytokines, relabelled 72 h". §7 tabulates Tnf 17.8× p = 0.008 and Il10 36.6× p = 0.002 with the n = 3 and the Q23 flag stated. §Biomarker proposes "the same panel, extended to 72 h, serves as a reactogenicity guard-rail", and the §7 conclusion names "a possible prolonged inflammatory tail in aged lungs … the evidence is n = 3 per group from a panel with its own integrity flag, so it needs re-measurement, but it should not be ignored". That is the work the counterfactual asked for |
| O6 | Quantified it correctly, **including the age-matched reading** (Tnf 8.4× against young 0.5×), named "a prolonged inflammatory tail in aged lung" in its risk list, put the `S09-A` qPCR run files inside the Gate 0 audit scope, and routed lung histopathology into the IND-enabling package. No dedicated resolution time-course, but the risk is carried, not dropped |
| O2 | Flagged it as a reactogenicity concern for a frail population, correctly, and its safety study's "must establish" includes tolerable repeat-dose inflammation. It calls the tail "transient: back to about 4× by 72 h" — a fall from 36× to 4× is defensibly transient |
| O7 | **My characterisation of this run was wrong.** It did not fail to retrieve the panel. Integrity item I09 reads: "S09-A panel 2, labelled 16 h, is the 72-h data. Its 'PBS' group holds the 'Sham' values. S09-A re-presents S01-A — relabelled; not counted as independent." Its `code/` directory touches `S09`. It retrieved the panel, diagnosed the mislabel correctly, and excluded it on a stated mounted fact. Under the grader's own A4, placement on a stated mounted fact is legitimate |

**The defence an expert gives, stated at full strength.** The 72 h readout is three animals
per arm at a single timepoint, on a panel carrying its own duplication finding, in which
the candidate does not separate from the age-matched comparator on five of seven analytes.
Folding resolution into the standard GLP toxicology and PD package — which all four runs
did in some form — is a defensible prioritisation call, not an omission. I cannot refute
that, and under the FA bar a choice a careful expert defends is not a failure mode however
many runs share it.

**Where this leaves HANDOFF standing decision 12.** SD12 is not wrong on the regulatory
point: the asset cannot file without resolution data. But the FA claim has to be that a
run made a *mistake*, and SD12 rested on a single ratio — "the candidate's 4.43 against
the predecessor's 3.43, only 1.29-fold". The probe adds the p-value for that ratio
(**0.262**) and shows the pattern holds across the whole seven-analyte panel, plus the
Ccl2/Ccl3 reversal. That is new evidence, not a re-litigation, and it is the kind of
evidence SD12 said it wanted to be judged on. **Recommendation: retire Mode 2.** The
decision is the writer's; nothing else in the FA depends on it.

---

### What survives, and it is worth more than the mode was

**The 72 h panel becomes a second site for Mode 1, and a better one than the 16 h site.**
At 16 h the confound inflates the asset's *benefit*. At 72 h the same denominator inflates
the asset's *risk*: the one number in the package that argues against advancing — the
reactogenicity flag — is also computed against the young parent arm. Six runs carry the
72 h form: O2 ("Ifnb1 still 2.85× the young level"), O3 ("285 % of young at 72 h",
"TNF 2.92× vs young PSLN-212", carried into a safety marker), O4 (Tnf 17.8×, Il10 36.6×
"vs the young benchmark"), O5 (restoration fraction −0.235, read as moving away from the
young profile), O6 ("Ifnb1 at 72 h is 2.85× the young level"), O8 ("2.85× above young",
and a tolerability marker at −0.24 "overshoot").

**And the exemplars are clean, which is what the 16 h site lacks.** F8 writes: "Aged
PSLN-212 shows the same Tnf and Il10 tail (5.2 and 4.2), so that part is an age effect.
Il6 is the exception: 7.2 vs 1.9, p = 0.03." That is the age-matched reading, and its
p = 0.03 reproduces my 0.026. F4 gives both columns: "Tnf 17.8 times young (4.8–66) and
1.6 times aged PSLN-212 (0.99–2.6)", a confidence interval that correctly straddles 1.0,
consistent with my p = 0.052. So at the 72 h site the mode has two runs that got it right
and six that did not, inside the same panel. That is the strongest evidence in the whole
FA that the confound is a choice rather than a property of the room.

### A single-run finding, recorded and not shipped

O7's exclusion over-applies its own duplication finding. Verified this session: the
duplication holds for **the Ifnb1 row only** — panel 2's seven arms de-logged match
`S01-A` 72 h as printed in 21 of 21 values, median error 0.113 %, maximum 0.405 %, against
a median error of 76.2 % versus the 16 h panel. The other six analytes at 72 h — Il6,
Ccl2, Ccl3, Ccl5, Tnf, Il10 — appear **nowhere** in `S01` (0 of 21 values each). So
discarding the panel discards six analytes with no other source in the room, and O7 then
asserts "No tolerability signal in mice at the dose that works." O4 drew the line
correctly on the same finding. This is one run, so it does not clear the prevalence floor
and is not a mode. Screen the next batch for it.
