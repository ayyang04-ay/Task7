# psql25c1 — task defects and proposed fixes

Ordered by whether they must be settled before anything else, then by whether the fix
forces a fresh batch of runs.

---

## 0. Settle first, because everything else is moot if it goes the wrong way

### D0. Source licence is unresolved and the evidence points away from CC BY 4.0

The data room is the supplementary data file of Gao et al., Sci Immunol 2026;11(123):eadz5242,
doi 10.1126/sciimmunol.adz5242.

- Science Immunology is an AAAS subscription title. Science Advances is the open-access
  journal in that family.
- The manuscript copy in hand is an HHS Public Access author manuscript deposited in PMC.
  That deposit is made under the NIH Public Access Policy, which grants PMC a licence to
  archive and display. It is not a CC BY 4.0 grant and it does not carry redistribution
  rights for the supplementary data file.
- Searching the full manuscript text for "creative commons", "CC BY", "open access",
  "licence", "license", "copyright", "reuse" and "permission" returns nothing.

**I cannot confirm CC BY 4.0 and I am not able to confirm it from what is available here.**
Verify on the publisher's article page before any other work. If it is CC BY-NC or
CC BY-NC-ND, or all rights reserved, the data room cannot be used and the task needs a
different source, which makes every fix below irrelevant.

---

## 1. Blockers

### D1. Submit gate not cleared

`job_info.json` carries a gate this environment enforces:

```
max_avg_score 0.55
rule  ships only if the model does NOT solve it — mean score must be at or below max_avg_score
mean_score 0.57
clears_gate false
```

Mean 0.57 against a ceiling of 0.55. I previously told the writer there was no score bar,
on the strength of the scoping guidance. That guidance is not what this environment
applies. Correcting that: there is a gate, and the task is 0.02 over it.

Note the interaction with D2. Removing the integrity tangle may raise scores by letting
runs spend their effort on the intended analysis, so fixing D2 alone could push the mean
further over. The confound and resolution material is where the difficulty actually lives,
and both modes already fire panel-wide, so the lever is to make those load-bearing rather
than to add new traps.

### D2. Ground-truth framing contradicts the seeded defects — QA Error, all 8 runs

The prompt says the data serve as ground truth. The workbook carries roughly a dozen
internal contradictions, and the annotation preserves every one of them unremarked.
Individually each is a plausible publishing error. Collectively they read as fabrication.

All 8 runs audited the data. Six made the audit the primary driver of the recommendation,
which routes around the analysis the task was built to test.

This one is mine. Standing rule 3 says to reproduce source inconsistencies verbatim and
unremarked, and I applied it to every inconsistency I found rather than asking how many
the room could carry before their combined weight became the story.

**Options, in order of preference.**

1. **Drop the ground-truth sentence from the prompt.** One line out, no data-room change.
   The tension disappears because nothing asserts the data are clean. Runs may still
   audit, but the prompt no longer contradicts what they find.
2. **Thin the inconsistency set.** Keep the ones a forcing-chain leg needs: the S06-C/S06-D
   identity (leg 4), the S09-A 16 h header (leg 16), the S03-B/S03-F label rotation, and the
   stated-n mismatches. Repair the rest in the shipped workbook: the reused weight
   trajectories, the shared S11-A/S11-B cells, the survival-versus-weight conflicts, the
   deaths in unchallenged controls. Those four carry no leg and are what tip the set from
   sloppy into suspicious.
3. Both. My recommendation, because 1 alone leaves a dozen contradictions in a file the
   runs will still audit, and 2 alone leaves the prompt asserting something about data
   that still has defects in it.

Either option forces a fresh batch.

### D3. The data room identifies its published source, confirmed in-transcript

Worse than the leak described in the other submission's feedback, because one vector here
is inside the file rather than in its name.

| Vector | Evidence |
|---|---|
| Filename `amnesti_preclinical_dataset.xlsx` is the DOI suffix | all 8 runs cite the filename; b359fc9d element 166 reasons from it that the file is "the supplementary file from a published paper" |
| Sheet names are the article's figure-panel names | `Fig.1`, `Fig. 2` … `Fig. S13`, visible in `docProps/app.xml` |
| **Embedded author metadata** | `dc:creator` and `cp:lastModifiedBy` are both `Gao, Shilin,PhD`, the paper's first author. Read by 16a5e37f and 5c73bcfd via openpyxl DocumentProperties at element 187 |
| Timestamps | created 2026-07-01, modified 2026-09-11, matching the publication timeline |

**Fixes.**

- Rename the workbook to something internal. `amnesti_adjuvant_dataset.xlsx` or similar.
  No DOI fragment, no `data_file_s1`.
- **Strip `docProps/core.xml`.** Clear creator, lastModifiedBy, created and modified. This
  is the one that names a real researcher inside a file presented as internal.
- Rename the sheets. `S01` through `S15`, or names drawn from the assay rather than the
  figure. This is the expensive one: the annotation, the golden, the grader, the brief and
  both audit scripts all address blocks by figure label, so all of them need the same
  rename applied consistently.
- Reword the annotation's block identifiers to match.

Forces a fresh batch.

---

## 2. Non-blocking, worth doing in the same pass

### D4. Grader has no criterion for the prompt's ruled-out deliverable

QA warning. The prompt asks what was considered and ruled out; section A does not check
it. Either add an A item or accept that the ask is supporting material, which is what the
brief's own prompt-versus-modes pass already concluded.

### D5. Grader constraints not disclosed by the prompt

QA warning. The grader penalises offering antibody as the cross-subtype correlate and
requires separating peripherally accessible biomarkers from the rest. The prompt asks only
whether a biomarker of efficacy is worth carrying forward. Judgement call: the constraints
follow from the data room rather than needing to be stated, but the warning is fair and
cheap to answer by softening the A wording.

### D6. No document-rendering toolchain in the environment

QA warning, all runs affected, none blocked. Runs asked for committee-ready documents
could not produce a PDF the normal way and hand-rolled renderers. The prompt no longer
names an output format, so this costs effort rather than correctness. Worth reporting to
the environment owner rather than fixing here.

---

## 3. What not to change

The two panel-wide error modes are intact and well evidenced. The confound mode fires in
all 8 runs and the resolution mode in 6. Neither depends on the inconsistency set, the
filename or the sheet names, so the fixes above do not cost the FA its material.
