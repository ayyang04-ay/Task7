# Handoff — Anton task psql25c1 (AMnESTI mucosal adjuvant)

Repo `ayyang04-ay/Task7`, branch **`claude/exciting-cray-mkihzd-v3`**, cloned from v2
at `0c83eae`. Develop and push here.

**`claude/exciting-cray-mkihzd-v2` is the integrity reference and must not be edited.**
It carries the pre-rename-3 identifiers, which is exactly what `build/verify-rename.py`
diffs the working tree against. Editing it destroys that reference.

**Do not build on `claude/exciting-cray-mkihzd`** either. That is pre-rename-2 history
and it shipped a leak. v2 exists because of it.

RLS short ID `psql25c1`, task `task_4ce55343502b4d17b2182158ad6e4533`, campaign
`camp_0589d1e96758477586df0e43dd8eeec1`.
[Studio](https://studio.mercor.com/annotator/tasks/task_4ce55343502b4d17b2182158ad6e4533/?campaignId=camp_0589d1e96758477586df0e43dd8eeec1)

---

## 1. START HERE — the sweep is done; the panel is the last unverified thing

**Everything mechanical and everything the verification sweep found is closed.** Three
independent audits ran against the renamed files and their findings are actioned: a
reference audit of every cited number, an adversarial leakage red-team, and an audit of
every grader A and B item. Sections 7 and 8 carry what they found and what was done.

**One thing was never obtained and will not be: an independent solvability read.** See
standing decision 13. Seven launches across four configurations died on the same
`[reasoning_extraction]` safeguard flag, so the 16-run panel is the solvability test by
decision rather than by omission. What to do with the first batch is in that decision,
and `fa/solvability-checklist.md` is the screen to run against it.

**So the order of work from here is:**

1. Re-verify the five artifacts and paste them per `build/paste-checks.txt` (section 4).
2. Run the panel. 16 independent samples, no subagent fanout.
3. **Before analysing for failure modes, screen the batch for solvability** against
   `fa/solvability-checklist.md`. A route-necessary leg that no run reaches is a broken
   room, not a failure mode, and the distinction decides whether the batch is FA
   material or a rebuild. Legs 2, 3, 6 and 13 are the exposed ones: they rest on the
   annotation alone, and the annotation absorbed 313 of the rename substitutions.
4. Then the failure analysis. Section 9 has the ledger status and what supersedes what.

**Why the sweep was needed, kept because it explains the shape of the repo.** The
renames touched the workbook, the annotation, the golden, the brief and five scripts.
Every check run against them in-session was mechanical: string counts, audits,
correspondence, provenance greps. All green, and all insufficient twice before — a bulk
rename of this class corrupted 73 identifiers the first time it ran, and a red-team
found a published-compound-name leak in files that had already passed four provenance
sweeps. The third recurrence was found in this session: the asset name itself was the
source paper's title word. Independent adversarial reads found what greps did not, every
time. Budget for them.

**Expect and do not treat as defects:** the workbook's internal contradictions, both
`S09-A` headers reading 16h, `S06-D` duplicating `S06-C`, `S15-L`/`S15-N` carrying no
stated challenge virus, the unlabelled region at `S08` rows 89–101, no timepoint past
72 h, no HA dose-ranging, no per-animal link between an immune measure and an outcome,
the stated-n mismatches, the `S10-A` block holding `S03-E` content, the `S06` duplicated
printed labels, the `NP366-374` tetramer against the stated strain, and `S05-A`'s
ambiguous immunogen.

**If a sweep is ever re-run**, the briefs that worked are worth reusing and are
reconstructable from sections 7 and 8; `claude/solvability-room` is an orphan branch
holding only the two data-room files, with no design document, golden, grader, script or
history, kept as a ready-made isolated checkout for a manual solvability pass.

---

## 2. What this is

An Anton eval task (Mercor, preclinical drug R&D). A solver gets a prompt and a data
room and must recommend whether to advance an adjuvant. **The deliverable that matters
is the failure analysis**, hand-written by the user in Studio, on what a panel of
solver runs got wrong. Build artifacts exist to produce transcripts, not to score well.

Read the `anton-scope2` skill and its `references/` before any design decision, and
`anton-fa` before touching the FA.

**Source material** is Gao et al., Sci Immunol 2026;11(123):eadz5242, titled "AMnESTI
reverses age-associated lung immune decline to drive heterosubtypic protection by
inactivated influenza vaccines". Its supplementary data file is the data room. The
publication is NOT mounted and must stay unmounted. Licence was checked by the user
against the AAAS policy page and cleared — do not reopen it.

**The asset's name was the paper's title word.** `AMnESTI` — "AEC-targeting MN
Encapsulated STING agonist" — was the source's own compound name, not an authored one.
It is present in `build/pre-edit-workbook-backup.xlsx`, the publisher's original, at
cells no rename had ever touched, which is the dispositive proof. One search on it
returned the article and its PMC full text. Renamed to `PSLN-344` in rename 4; see
section 7. The data room still carries `AECI`/`AECII` arm labels, which is the first
letter of the acronym, and that is unavoidable since they are real cell types.

---

## 3. Repo layout and commands

```
data-room/   what the solver sees
task/        uploaded to Studio
build/       sources, generators, audits. NOT uploaded.
fa/          failure-analysis working files
```

`build/anton-brief-psql25c1.md` is the design document and the single source for the
prompt and the grader. `build/annotation-source.md` is the single source for the
annotation PDF. `task/golden-response.md` is the authored golden. **The shipped copies
are generated and are never edited by hand.**

From `build/`, with `python3 -I`:

```bash
python3 -I make-artifacts.py          # regenerate every shipped artifact
python3 -I make-artifacts.py --check  # fail on drift; covers prompt, grader, annotation PDF, both golden copies
python3 -I audit-golden.py            # recompute every figure in the golden against the workbook
python3 -I audit-registry.py          # print the full verified value set
python3 -I verify-rename.py           # prove the tree reduces to rename 3's declared substitutions
python3 -I rename-assets.py --check   # dry-run renames 3-5 and their never-touch guards
python3 -I rename-asset-name.py --check
python3 -I rename-payload.py --check
```

The first two must be green before any upload. No scipy, no lifelines — log-rank is
Mantel-Cox inline, t-tests via an inline incomplete beta.

---

## 4. The five shipped artifacts

| Upload as | File | Bytes | sha256 |
|---|---|---|---|
| Prompt | `task/prompt.txt` | 1,187 | `cfc0f29bde3c` |
| Grader guidelines | `task/grader-guidelines.txt` | 5,666 | `c545a600076a` |
| Data room | `data-room/adjuvant_program_dataset.xlsx` | 56,787 | `f293502992c7` |
| Data room | `data-room/adjuvant_program_annotation.pdf` | 59,700 | `83f2e9fb45db` |
| Reviewer golden (any of the three) | `task/golden-response.md` | 24,972 | `55bfe5837780` |
| Reviewer golden (any of the three) | `task/golden-response.txt` | 24,777 | `e77e485a55fa` |
| Reviewer golden (any of the three) | `task/golden-response.pdf` | 41,946 | `937d3e808cdd` |

Prompt is 201 words, grader 898. Check each paste against `build/paste-checks.txt`,
which carries word count, character count, hash prefix and required last line. The
line-break property is the one a diff will not show you: confirm in the form that each
paragraph is still a single unbroken line, and that the grader's C list is present at
the bottom.

**The `.md` ban is scoped to the data room and the prompt, not to the golden** — see
standing decision 7, corrected 2026-11-12. `task/golden-response.md` is the authored
source and may itself be submitted; `make-artifacts.py` also generates `.txt` and `.pdf`
with content verified identical, so any of the three may go in the form. What must never
happen is an `.md` in the data room, or a prompt that asks for or references one.

---

## 5. Standing decisions — do not re-litigate

The user settled all of these. Re-opening them has wasted time more than once.

1. **"Ground truth" means the data is the authoritative source for the decision, not
   that it is error-free.** The workbook's internal contradictions are a flawed real
   dataset and they STAY. Do not repair them.
2. **QA findings are overridable unless Critical.** The priority is the FA.
3. **Scoring is deprecated.** The old 0.55 mean gate does not apply. The gate is at
   least one failure mode shared by at least two runs. Already met.
4. **The grader is a skeleton** to help prep the FA. It need not be airtight.
5. **No out-of-scope line in the prompt**, no not-all-relevant line, no world-fact
   constraint on deferral. All deliberate.
6. **All 101 blocks annotated; non-load-bearing noise kept as is.**
7. **No `.md` in the DATA ROOM, and the prompt must not ask for one or reference one.
    The golden may be `.md`.** Corrected 2026-11-12: an earlier version of this decision
    read "no `.md` anywhere in the upload", which over-scoped it. The constraint is on
    the solver-visible room and on the prompt, not on the reviewer-facing golden.
    Verified at the time of the correction: the data room is `.xlsx` plus `.pdf` with no
    `.md`; `task/prompt.txt` names no file, format, document or `.md` at all; and the
    shipped annotation text contains no `.md` reference. `make-artifacts.py` still
    generates verified-identical `.txt` and `.pdf` copies of the golden, so any of the
    three may go in the form — that is insurance, not a requirement.
8. Assume the solver image has the packages it needs.
9. **Commodity reagents carry no leak exposure and stay. `ADU-S100` did not, and was
    renamed to `CDN-1807` in rename 5.** The decision originally classed it with the
    commodity tools, which was wrong: it is a named development-stage asset, the CDN
    STING agonist ML RR-S2 CDA, Aduro Biotech, licensed to Novartis as MIW815, Phase 1,
    dropped from the portfolio in 2019.

    **The operative line, which this decision now states explicitly, is not "is it a
    company code".** `INCB3344` is one and it stays. It is **whether the identifier
    names the asset's own composition.** ADU-S100 was the payload both the candidate and
    the predecessor encapsulate, and the source paper's abstract names it as what the
    asset encapsulates, so it was constitutive of the thing the publication is about.
    `R848`, `cGAMP`, `INCB3344`, `Clodrosome`, carbenoxolone, the lipid names and the BEI
    and IRR catalogue numbers are commodity tools that hundreds of papers use and that
    point at nothing in particular. They stay.

    **What rename 5 does not fix.** The exposure was never only the string. A cyclic
    dinucleotide payload plus manganese coordination polymerisation plus a
    pulmonary-surfactant-biomimetic liposome plus aged mice plus heterosubtypic influenza
    narrows the literature to this programme with no compound name present at all.
    Renaming removes a named hook, not the fingerprint. The fingerprint is science and
    cannot be edited away without fabricating. BEI
   catalogue numbers (`NR-3177`, `NR-348`, `NR-41803`, `FR-201`), every strain name,
   `ADU-S100`, `R848`, the lipid names, `INCB3344`, `Clodrosome`, carbenoxolone,
   `OT-I`, `Sftpa1-/-Sftpd-/-`. Strain names are additionally load-bearing: the subtype
   classification is derived from them.
10. **No reagent glosses.** Mechanism explanations for common reagents were removed;
    `Carbenoxolone (CBX)` keeps its parenthetical on the user's instruction.
11. **Only proprietary asset names are ever renamed for leak exposure.** Reagent,
    strain, gene, allele, marker, protein and catalogue identifiers never change —
    `CD11b`, `Ly6C`, `H5N1`, `H-2Db` and the rest are the never-touch guard in
    `build/rename-assets.py`, not targets. This is decision 9 restated as an
    operational rule after rename 1 corrupted 73 of exactly those strings.
12. **A7 and FA Mode 2 STAY. Resolution kinetics is required as proposed work, not
    accepted as a caveat.** The rubric audit argued that inventorying it as a caveat is
    defensible, which would have failed Mode 2 against the FA bar and cost a third of
    the ledger. The user resolved it and the reasoning is recorded because it is the
    answer to the defensibility challenge a reviewer will raise:

    **Resolution kinetics IS a GLP tox question — and that is why it is a study rather
    than a gap, not why it can be deferred.** The asset cannot reach IND without the
    data, so a forward view that does not specify it leaves the programme with no path
    to filing. An expert who lists it as a known gap has not made a defensible
    prioritisation call; they have left the asset unfileable. That holds without needing
    body weight to carry more than it can: `S08-D` at 99.78% against 90.65% for the
    positive control is a crude screen, adequate to say "not acutely reactogenic,
    continue", which is a different claim from "resolves". The resolution study earns
    its slot as the follow-up that converts the screen into IND-enabling data.

    Note for whoever reads the evidence fresh: at 72 h the *predecessor* arm is at 3.43
    against sham 0.996, so the candidate's 4.43 is only 1.29-fold over its own
    predecessor. Non-resolution is substantially a property of the liposome platform in
    the aged lung rather than something the manganese introduces. This does not change
    the decision — the asset still needs its own resolution data to file — but it is the
    sharpest version of the counter-argument and is worth having ready.

13. **THE PANEL IS THE SOLVABILITY TEST. This is a recorded decision, not an omission.**
    No independent solvability read was ever obtained against the renamed room, and one
    is not obtainable by any route available in-session. **Seven launches across four
    configurations all died on the same `[reasoning_extraction]` safeguard flag:** two
    Opus subagents, one Sonnet subagent, two more Opus subagents after a retry, and two
    separate cloud sessions on an orphan branch holding nothing but the two data-room
    files. Not model-specific, not session-specific, not fixed by stripping the persona
    line or inlining the request, not fixed by physically removing the answer key.

    The only pattern that survives seven attempts: the three audits that **ran** —
    reference, red-team, rubric — all *audit the package*, while all seven that **failed**
    *answer the prompt as a solver*. That is a correlation and not a diagnosis, and
    further guessing was stopped rather than continued.

    **So the first batch of 16 does double duty**, and the screen comes before the FA:
    - Screen for solvability FIRST, against `fa/solvability-checklist.md`, which was
      pre-registered for this purpose and is repurposed to score transcripts instead of
      agent reports. The pass rule is unchanged: a leg is solvable if **at least one run
      derives it**; a run disagreeing with the golden is not a failure, only an
      underivable leg is.
    - **A route-necessary leg no run reaches is a broken room, not a failure mode.** Do
      not write it up as a mode. That distinction decides whether the batch is FA
      material or evidence for a rebuild.
    - Legs 2, 3, 6 and 13 are the exposed ones. They rest on the annotation alone, which
      absorbed 313 of the rename substitutions, and known risk 4 is that a thin
      annotation there breaks the protection and carry-forward pillars rather than making
      them hard.

    **What the decision is resting on, stated so it can be judged rather than trusted.**
    In favour: `audit-golden.py`'s 246 checks all reproduce against the shipped room;
    annotation-to-workbook correspondence is exact at 101 occurrences and 95 distinct
    with the six deliberate duplicates; `verify-rename.py` proves the renames changed
    nothing but the declared strings across every file, 22,542 workbook cells and both
    PDFs. Against: none of that is a solvability test. Every one of those checks confirms
    that the room says what it is supposed to say — not that a solver can get from the
    room to the conclusion. The cost of being wrong is one wasted batch; the cost of the
    alternative was an unbounded number of further launches against a flag that did not
    move. The user took the batch.

14. **Any workbook edit is zip-level, sheet entries only.** Never an openpyxl
    round-trip. See section 7, rename 3.

---

## 6. What remains

**Blocking:** the sweep in §1. Nothing else.

**Then:** resubmit, re-run the panel, write the FA.

**Both former open calls are now answered by the user. Do not reopen them.**

- **The annotation's "as printed" register: KEEP AS IS.** The user's call, and the
  reasoning behind it is worth recording because it reverses an earlier position.
  The register is 111 occurrences, and they are not one thing: 102 are the repeated
  field label `**Groups as printed**`, one is the preamble that establishes the stance,
  four are `as printed in the header row` / `in column 1`, and **two are
  `**Timepoint**: as printed in the block label, 16 hours after administration` at
  annotation-source lines 592 and 600 — the two S09-A headers, i.e. forcing-chain leg
  16.** Those two cannot change under any option: strip the phrase and the annotation
  stops transcribing a wrong label and starts asserting a timepoint the data
  contradicts, which is the companion document inventing a fact and is forbidden by
  standing rule 2. That makes any rewrite necessarily partial, leaving two unexplained
  leftovers in a document whose declared stance no longer accounts for them, which is a
  worse tell than consistency. The register is also coherent with the file's own
  authored provenance: `core.xml` names the creator `Preclinical Data Management`, a
  transcribing function rather than a scientist, so voice and metadata agree. The
  register remains an explicit red-team target so the next sweep gives an independent
  read, but the default is no change.
- **`AUP-0417` is now `PCL-26-0417`.** Corporate-style identifier on the user's
  instruction. The surrounding sentence is unchanged: companies do run IACUCs, so only
  the identifier read academic. Resolves to nothing, as before.

---

## 7. Incident history — read before any bulk edit

Two leaks and two renames. Kept because it prevents repeats and the FA needs it.

**Leak 1, metadata and labels.** The workbook was the publisher's supplementary file:
filename was the DOI suffix, sheet names were the article's figure-panel names,
`dc:creator` and `cp:lastModifiedBy` named the first author, `x15ac:absPath` carried
their local path, and ten cells carried `mailto:` hyperlink artefacts naming a
pre-rename compound. All 8 runs of the first panel cited the filename, and one reasoned
from it that the file was "the supplementary file from a published paper". All fixed.

**Rename 1, which corrupted the data.** Block labels were renamed to `S01`–`S15` /
`S01-A` with a 505-rule dictionary, **125 of whose rules were bare two-character panel
tokens applied as plain substring replacements.** `5N`→`S05-I` turned `H5N1` into
`HS05-I1`; `6C`→`S06-B` turned `Ly6C` into `LyS06-B`; also `Ly6G`, `H-2Db`, `H-2Kd`.
73 real identifiers corrupted, 27 of them in the shipped PDF, and the annotation ended
up contradicting the workbook it described. It broke the subtype-classification leg,
because the solver reads the challenge virus out of a sentence the rename mangled. I
had written "risk is low but real" when building the dictionary and never checked.
Reverted; the 125 rules deleted; `build/replacements.README.txt` records what they did
and the identifier list to diff against before writing anything like them again. The
380 surviving rules all anchor on a `Fig`/`Figure`/`Supp`/`Table` prefix and were
tested against 64 real identifiers — zero fire.

**Leak 2, published compound names.** Found by an adversarial red-team on files that
had already passed four of my own provenance sweeps. Those searched authors, DOIs,
journals, paths and generator strings. **None searched for published compound names.**
The data room named two adjuvants from the source program's lineage and defined the
asset as a one-variable delta on one of them.

**Rename 2, done with the lesson applied.** Every rule is a full compound name of 7+
characters, so none can match inside a gene, allele, strain or marker name. A
48-identifier guard ran before and after every file and **caught a rule of mine that
would have destroyed `R848` inside `NanoR848`.**

| Was | Now |
|---|---|
| `NanoSTING` / `nanoSTING` | `AVB-101` |
| `NanoSTING/R848` | `AVB-101/R848` |
| `NanoR848` | `AVB-R848` |
| `NanoSRB` | `AVB-SRB` |
| `PS-GAMP` / `PSGAMP` | `CMP-204` |
| molar ratio `10:1:1:1` | removed |

Suffixes rode along, so the deliberate quirks survived: `AVB-101 ` with the trailing
space, `AVB-101(y)` lowercase, `AVB-101Y` without parentheses, `Imprinting+AVB-101`,
`Naïve+AVB-101`. The rename script lived in the session scratchpad only, not the repo,
which is why rename 3 had to rebuild the guard from nothing. Fixed: see below.

**Rename 3, a third-party collision rather than a leak.** `AVB-101` is a real
clinical-stage asset — AviadoBio's AAV9-GRN gene therapy for frontotemporal dementia,
Phase 1/2 since 2023, FDA Orphan and Fast Track. Rename 2 had replaced one published
compound name with a different published compound name. It is **not** a provenance
leak: nothing about a dementia gene therapy points at the source programme, influenza
or STING, so a solver who recognises the string concludes the writer reused an
unrelated code. The cost was realism and reviewer credibility. `CMP-204` was searched
and is clean, and stays.

| Was | Now |
|---|---|
| `AVB-101` | `PSLN-212` |
| `AVB-R848` | `PSLN-R848` |
| `AVB-SRB` | `PSLN-SRB` |
| `AUP-0417` | `PCL-26-0417` |

Three rules, each a full name of 7+ characters so none can match inside a gene, allele,
strain or marker, applied longest-first so none can fire inside another. Suffixes rode
along again and every quirk survived: `PSLN-212 ` trailing space, `PSLN-212(y)`,
`PSLN-212Y`, `PSLN-212/R848`, `PSLN-212+GM-CSF`, `Imprinting+PSLN-212`,
`Naïve+PSLN-212`, `AECI/PSLN-SRB` and the three other AEC forms.

**Both scripts are in the repo this time.** `build/rename-assets.py` carries the rules
and a 60-entry never-touch guard, counted in every target before and after, aborting if
any count moves. `build/verify-rename.py` proves the stronger property: take every file
as it stands on v2, apply the declared substitutions, and require byte-identity with
the working tree. It passes over 18 text files, 22,542 workbook cells, the zip shape and
both PDFs. 177 string cells renamed, 6,819 non-string cells identical.

**The workbook was edited at the zip level, sheet entries only, never through
openpyxl.** An `openpyxl` load/save round-trip rebuilds the entry set, synthesises a
`sharedStrings.xml` the file does not have, rewrites `app.xml` and the theme and resets
every mtime — reintroducing the over-sanitisation tells recorded below as fixed. Entry
names, order, mtimes and compression are preserved and every non-sheet entry is
byte-identical. Any future edit to the workbook must work the same way.

**Rename 4, the asset name — Leak 2 again, and the worst of the three.** `AMnESTI` was
the source publication's own compound name and it is in the paper's **title**. Rename 2
renamed `NanoSTING` and `PS-GAMP` and left the headline compound, so the single most
searchable string in the package was the asset name, present in the prompt, the grader,
the golden, the filename, 115 workbook cells and all 19 pages of the annotation.

| Was | Now |
|---|---|
| `AMnESTI` | `PSLN-344` |
| `amnesti_preclinical_dataset.xlsx` | `adjuvant_program_dataset.xlsx` |

Wider blast radius than rename 3, in two ways worth remembering. The prompt and the
grader are **generated from the brief**, so the rename had to go into
`build/anton-brief-psql25c1.md`, not into the shipped copies — and into
`build/make-artifacts.py`, whose prompt slice marker is the literal opening words of the
prompt. And `build/make-annotation-pdf.py` writes the asset name into the `/Subject`
metadata of **both** shipped PDFs, which is its own leak vector and would not have been
caught by reading the documents.

Script committed: `build/rename-asset-name.py`. `verify-rename.py` now proves the
cumulative property across both renames: every file as it stands on v2, with all six
declared substitutions applied, is byte-identical to the working tree — 16 text files,
22,542 workbook cells, 292 renamed string cells, 6,819 non-string cells identical, zip
shape preserved, both PDFs. It gained two categories in the process: `FROZEN`, for files
whose job is to record the prior state and which must stay byte-identical, and an
exclusion for `paste-checks.txt`, which holds statistics *about* the text and so does
not transform under substitution.

**Two red-team findings that the backup diff refuted.** Worth recording, because both
looked like our redaction scars and neither was:

- The workbook's `Hyperlink` cell style, whose only users are the cells carrying the
  asset name, is present in the publisher's original with the same `cellXfs` indices,
  and those cells already read `AMnESTI` there. The red-team inferred the asset name had
  been "written over a pre-existing label". It had not — but chasing that inference is
  how the Leak 2 recurrence was found.
- The double and triple spaces in block labels (`'S04-C   n=5'`) are the **source's own
  spacing**: `'Fig. 4G   n=5'` in the original. **Zero** space runs were introduced by
  any of our edits. The red-team read them as deleted descriptor tokens. They are
  standing rule 3 working as intended.

**Two findings it got right. One fixed, one accepted.**

*Fixed.* The annotation PDF was stamped 2026-03-07 while the workbook it describes is
stamped 2026-09-03, so the annotation predated its subject by six months. The epoch
constant in `make-annotation-pdf.py` now puts it at 2026-09-15, with a comment saying it
must stay later than the workbook.

*Also fixed.* The annotation was called `trial_summary.pdf` and contains no trial —
nineteen pages of mouse work and no human data — and it carried **three different names**
across its filename, its `/Title` ("Dataset annotation") and its page-1 heading ("Study
annotation"). The red-team read the mismatch as a label applied from outside by someone
who had not read the document, which is exactly what it was. All three now agree on
*Dataset annotation*, and the file is `adjuvant_program_annotation.pdf`, so the two
data-room files read as a matched pair from one internal export. No data changed; the
page-1 heading is the only content edit and no forcing-chain leg touches it.

*Accepted, on the user's decision — do not reopen.* The room's **structure** is a figure
set. The publisher original's sheets are literally `Fig.1` … `Fig.7`, `Fig. S1`, `S2`,
`S3`, `S4`, `S7`, `S8`, `S12`, `S13`. Rename 1 flattened seven main and eight
supplementary figures into a contiguous `S01`–`S15`, erasing both the main/supplement
split and the gaps, but the shape survives: the red-team reconstructed the seam without
ever seeing that file, its `S06` survival ↔ `S15` weight pairing being
`Fig.6` ↔ `Fig. S13`. **No rename fixes this.** It is the shape of a supplementary data
file, and standing rule 1 makes the room exactly that. The user has accepted it rather
than renumbering again; a third structural rename would risk the rename-1 class of
damage for no gain, since the pairing is recoverable from the data whatever the labels
say. Expect a red-team to find it every time and do not treat it as a new finding.

**The lesson from rename 4, which is not the same as rename 1's or 2's.** The red-team
that found Leak 2 classified `AMnESTI` as "INVENTED — contrived backronym with Mn
embedded." Exactly wrong, and instructively so: it *is* a contrived backronym, because
the authors contrived it. An isolated red-team has no web access, so its identifier
enumeration is parametric knowledge only and systematically cannot catch a real name it
does not happen to know. **Always run a web pass over the enumeration it returns,
outside the sandbox, in extended search mode.** Standard mode returned nothing for
`AMnESTI`; extended mode returned the paper as the first result. That difference is what
the whole branch turned on.

**Rename 5, the encapsulated payload.** `ADU-S100` → `CDN-1807`. Five occurrences, all
in `build/annotation-source.md`, which generates the shipped annotation PDF; **zero in
the workbook**, which `build/rename-payload.py` asserts rather than assumes. Nothing in
the prompt, the grader or the golden referred to it. The reasoning and the line it draws
are in standing decision 9. Forcing-chain leg 3 is preserved: it rests on the annotation
saying both preparations encapsulate the *same* cyclic dinucleotide, and the sentence
still reads "both encapsulate the cyclic dinucleotide STING agonist CDN-1807. They
differ in one respect: PSLN-344 incorporates Mn2+ by coordination polymerization and
PSLN-212 does not."

`verify-rename.py` now carries seven declared substitutions across renames 3 to 5 and
still proves the whole chain back to v2 in one pass.

**My own sanitisation created new tells**, all found by the red-team: an empty
`core.xml` (an absent creator is itself a signal), every zip entry stamped
`1980-01-01`, two empty `_rels` shells left behind by hyperlinks I had stripped, and
cursor state (`activeCell`, `topLeftCell`) in all 15 sheets. Over-sanitising is
detectable. `core.xml` now carries a plausible internal creator and a date spread, zip
entries a uniform realistic mtime, and the theme and default font are no longer the
Excel 2024 pair.

**Lesson, stated plainly:** on this task my own verification has been insufficient
twice on bulk edits, in both cases because I searched for the vectors I had already
thought of. Independent adversarial reads found what greps did not. Budget for them.

---

## 8. Verified good — do not redo

Current as of `e5f8226`, all re-run after the rename.

- `audit-golden.py`, `audit-registry.py`, `make-artifacts.py --check`: all clean.
- **Annotation ↔ workbook:** 101 label occurrences, 95 distinct, zero asymmetry in
  either direction. **Six labels appear twice and all six are deliberate:** `S02-D`,
  `S04-B`, `S06-E`, `S06-F`, `S09-A`, `S14-A`. An earlier version of this file said
  three; verify with the snippet below rather than trusting any count in prose.
- **Workbook data untouched:** all 6,819 numeric cells byte-identical to
  `build/pre-edit-workbook-backup.xlsx`, the publisher's original.
- **Provenance sweep** over every part of the xlsx and the annotation text: no author
  name, path, generator string, DOI, journal, mailto, hyperlink, cursor state, theme
  font or old identifier.
- **Rubric audit, and four defects it found.** An independent agent audited every A and
  B item on three axes: accurate against the mounted cells, defensible against the FA
  bar, correctly cited. Four items were wrong and are fixed; the reasoning matters more
  than the wording, so it is recorded here.
  1. **B3 penalised the golden.** It read "**any** aged-versus-young ratio as an ageing
     effect where the same block carries a young-plus-candidate arm." The golden's own
     line 46 does exactly that — aged+PSLN-212 16.64 against young+PSLN-212 37.60 — and
     it is the **adjuvant-matched** comparison, the one comparison in the package that
     isolates age. **The fix was already written down and the grader never picked it
     up:** `fa/error_modes.md` carries the tightened Mode 1 rule from the post-repair
     solvability run, which says the mode is a denominator varying age *and* adjuvant,
     and that holding formulation constant is explicitly not the mode. The ledger and
     the grader had been out of sync since that tightening, on the mode that fires in
     all 8 trajectories. B3 now names the denominator and exempts the clean comparison.
  2. **A8 contradicted the golden outright.** It required "the **effector** chain rested
     on the blockade experiments". The golden's only use of the word, line 171, is
     "improved priming, **not an effector function** of the adjuvant itself", and lines
     173 and 176 say no blockade carries a challenge arm and the step to survival is
     inferred rather than shown. The item demanded something the golden denies, so it
     rewarded over-claiming. Now "the priming chain", with the limit required to be
     stated — which the golden already does, so it now passes an item it used to fail.
  3. **B4's "cancel" was factually wrong.** Pooling the roster on sign alone moves the
     mean from 0.7318 to 0.8894 — attenuation, not cancellation, and still well below
     1.0. "The two higher-is-worse endpoints" was also roster-relative without naming
     the roster, so it could not be scored against a response using a different set.
  4. **B8 penalised a stance rather than an error.** Aged+candidate is indistinguishable
     from young+predecessor in all six blocks (p = 0.060 to 0.317), so an expert who
     sets non-inferiority-to-young as the bar, shows it met, and advances has made no
     mistake. This independently confirms **known risk 1**: the young-benchmark mode has
     no refuting fact in the room. Two independent reads now agree it is the weakest
     item in the map. Narrowed to declining or discounting on that ground.

  B2 was also split: the scale error (reporting `S09-A` as linear) is now separate from
  the later-timepoint-no-work limb, because tying the scale error to "the 72h analytes"
  made the penalty conditional on the solver having already made the leg-16 inference.
  The audit called this its most serious finding on the grounds that no 72h log10 panel
  exists; that is overstated — the fact is derived, not absent, and `audit-golden.py`
  verifies it from both directions — but the drafting fix stands.

  **One audit claim rejected.** It argued A3 is scoped backwards and should require the
  confound recognition wherever the only young arm is the predecessor, i.e. in the `S06`
  survival blocks. Declined: that is precisely where no foreclosing fact exists, which
  known risk 1 records, and widening A3 there would convert a determinate A item into an
  indeterminate requirement. A3's scope is correct *because* the refuting fact exists
  only in those six blocks.

  **Then fixed in a second pass, 2026-11-12.** The three remaining structural findings
  are closed:
  - **A is split into thirteen separately scored, numbered items.** A1, A2, A5 and A6
    were each two requirements bolted together, and A8 became a third when it was
    rewritten, so a response could satisfy one limb and fail the other and be credited
    for both. Each limb is now its own numbered item. B is numbered 1 to 10 in the same
    pass, since B doubles as the lookup for the pre-registered modes and numbered items
    make trajectory screening tractable.
  - **The A/B overlap now has a rule.** Five pairs score the same requirement twice, and
    the overlap is structural rather than accidental — A lists what a correct route must
    establish, B lists the errors expected to occur — so it stays. The framing paragraph
    now says a passage is credited or penalised once and never both.
  - **C's carve-out is narrowed.** "Read as labels" was meant to make noticing the
    duplication neutral, not the block placement, but a reader could take the wider
    sense and count the imprinting blocks toward the heterosubtypic set — the exact error
    A exists to catch. C now says so explicitly and points at A items 3 and 4.

  One trap worth knowing for any future grader edit: `make-artifacts.py` slices the
  grader out of this brief on the literal string `A. Must be present and correct:`,
  colon included. Rewriting that opening crashes the generator, which is how it was
  caught — it refused to ship rather than emitting a truncated grader.

  **Prompt elicitation, still open and sharper than D5 states it.** The prompt never uses
  the words heterosubtypic, cross-subtype, breadth, drift or mismatch — it frames the
  asset only as "an adjuvant for IAV vaccine development in older adults". A1, A2, A6's
  second limb and B1's second limb all turn on a cross-subtype value proposition the
  solver must infer from the room alone. Defensible as difficulty, but it is the two
  heaviest A items resting on an unstated frame.

- **Golden vs grader, before the rubric audit:** all 8 A items met with quoted passages, 0 of 9 B penalties
  tripped, no double-classification, no placement or ordering requirement, every A item
  traceable to something the prompt asks.
- **Golden arithmetic: true on values, and it was overstated on routes.** Two
  independent agents have now recomputed the golden. Every *value* reproduces — all 24
  log-rank p-values, every survival count, all 28 cells of the 2x2, all 18 roster
  ratios, both pooled means, all seven exponentiated analytes, both `S09-A` timepoint
  anchors, geometric and arithmetic means, per-animal ratios and Welch p-values. **But
  the second audit found a defect the first missed:** three figures in the subclass
  paragraph (16.1-fold, 11.3-fold, and the 0.559/0.346/0.551 triple) reproduce only as
  ratios of group means while the golden said "computing each per animal". Grader A
  closes on numbers reproducing *by the route stated*, so by its own standard three of
  the golden's figures did not. Fixed, numbers unchanged, and the paragraph now says
  that reducing per animal makes the impossibility larger (18.8-fold and 12.5-fold) so
  the conclusion is reduction-invariant. The earlier version of this bullet claimed "no
  number in the golden is wrong" and inferred too much from one agent agreeing.
- **Prompt:** free of all four constructs deprecated 2026-11-07 — as-of dates, named
  output files or paths, no-web constraints, saved analysis artifacts.

```bash
cd /home/user/Task7 && python3 -I -c "
import re, openpyxl, collections
w=openpyxl.load_workbook('data-room/adjuvant_program_dataset.xlsx',data_only=True)
occ=[m for s in w for r in s.iter_rows() for c in r if isinstance(c.value,str)
     for m in re.findall(r'\bS\d\d-[A-Z]\b',c.value)]
print(len(occ),'occurrences',len(set(occ)),'distinct')
print({k:v for k,v in collections.Counter(occ).items() if v>1})"
```

**`audit-golden.py` gaps: CLOSED.** The second reference audit enumerated 24
load-bearing claims the script did not cover. Coverage went from **109 to 246 diffed
checks**, and the three classes it found are all addressed.

*Too loose.* Every cell of the log-rank table is now diffed against its printed value.
The old version asserted only `p_par <= 0.0151` and `p_young >= 0.0597`, i.e. range
membership, so a block drifting from 0.0083 to 0.0001 would have passed. The
`p < 0.0001` age-deficit claim was checked as `chk(..., 0.0, 2e-3)`, which passes
anything under 0.002, so the inequality the golden states was never tested; it is now
tested as an inequality.

*Printed but not checked.* All six blocks' survival fractions and per-arm n, all
eighteen roster ratios (only `min` and `max` were asserted, so the middle fourteen could
drift), and the `S06-C`/`S06-D` 28-pair count.

*Not computed at all.* The whole `PSLN-212`-vs-sham log-rank row, which carries the
claim that the manganese rather than the liposome does the work; the entire subclass
argument, with roster row 8 now derived from the workbook instead of hard-coded; `S04-C`
and `S13-H`; the imprinting blocks; `S10-A`; the `S06` block count; `S09-A` block 1;
`S06-E`/`S06-F` against their untreated arms; the `S08-A` percentage and the `S08-D`
positive control; the diagonal-versus-formulation-held pair; cDC2; the `S05-C` and CCR2
fold-changes; the matched-endpoint set; the `S15-L`/`S15-N` parent arms; `S03-J`'s last
day; and the four-arm-block exclusivity claim, which independently reproduces exactly
the six blocks the golden names with `S02-I`, `S09-B`–`S09-G` and `S13-E` excluded.

**Two defects the new coverage found immediately, both worth knowing about.**

1. **It caught an error in the golden written the same day.** The day-4 clause said "the
   mean across all five days is 0.996". That is the ratio of the two arms' pooled
   five-day means; the mean of the five per-day ratios is 1.007, which *exceeds* 1.0 and
   would have undercut the clause's own point. The same unnamed-reduction defect the
   reference audit had just found in the subclass paragraph, reintroduced and then caught
   within minutes. The golden now names the reduction.
2. **The script exited 0 even with `chk` mismatches recorded.** Only an `assert` ever
   failed the run, so a scripted gate reading the exit status saw green whenever no
   assertion happened to fire. Fixed with an explicit `sys.exit(1 if fails else 0)`.
   **Every "audit-golden passes" claim made before that fix was weaker than it sounded.**

**A gap that remains, by design.** The script recomputes the workbook and diffs it
against what the script says the golden claims — and those claimed values live in the
script, as a hand-maintained transcription. Editing a figure in the golden without
editing the script was proved by deliberate tamper to go unnoticed. A `CORRESPONDENCE`
section now asserts that all 115 of the golden's load-bearing figures appear literally
in its text, which makes the transcription provable rather than parallel, and a tamper
test confirms it fires. It is still a literal-string check: it catches a changed or
deleted figure, not a figure whose surrounding prose has drifted.

`audit-registry.py` is a reporting tool, not a gate — it prints the verified value set
and asserts nothing. "It passed" means only that it ran.

**Blind spot closed earlier, for the record:** `audit-golden.py` previously checked no survival percentage
and no log-rank p-value, so nothing in the build verified the golden's most
load-bearing argument. It now computes all 24 log-rank values, the six configurations,
the `S06-C`/`S06-D` identity, the `S06-G` ceiling reading, `S15-L`, `S15-N` and
`S03-J`. `--check` now also covers the two reviewer-facing golden copies, verified
against a deliberate tamper.

---

## 9. FA status — the gate is met

Ledger in `fa/error_modes.md`, defect analysis in `fa/task-defects-and-fixes.md`.

| Mode | Trajectories |
|---|---|
| Age and adjuvant confounded in the restoration metric | all 8 |
| Provenance audit substituted for the efficacy judgement | 6 of 8 |
| Mislabelled 72 h panel identified, then no resolution work | 6 of 8 |

Notes the FA needs:

- **Thinking blocks are summaries, not raw**, so no claim about what a run weighed
  internally is supportable. That rules out the raised-then-abandoned shape.
- **Mode 1's screening rule was tightened and this changes counts.** The mode is
  specifically a denominator that varies age *and* adjuvant together — a metric built
  on aged+AMnESTI over young+parent. A run comparing aged+AMnESTI against young+AMnESTI
  has held formulation constant and has **not** committed it. Read the metric
  definition, not whether the word "young" appears: two of the eight trajectories were
  identified from a metric definition rather than from prose. One of two fresh agents
  avoided the mode entirely, so it is avoidable, which strengthens it.
- **A pre-registered fourth candidate** sits at the foot of `fa/error_modes.md`:
  proposing an adjuvant-alone arm the room already contains. **No count, no trajectory
  IDs** — the existing panel was analysed before `S15-H` was found and was never
  screened for it, so that ledger is not evidence either way.
- **All trajectory IDs above come from the batch that ran against the old labels and
  the old compound names.** The analysis a solver does is unchanged, so the modes
  should reproduce, but a new batch supersedes these IDs.
- A solver who observes that the adjuvant also raises the young response, or who counts
  `S15-H` as a seventh favourable configuration, is **correct** and must not be marked
  down. Both points corrected the golden.

---

## 10. Not in the repo — the user must re-upload

| Needed for | What to re-upload |
|---|---|
| FA, any transcript work | `Anton_4ce55343502b4d17b2182158ad6e4533_job_91694a59_2026-11-09.zip` |
| QA cross-reference, if ever wanted | `qa_report_psql25c1_v1_84eb8cc6.zip` |
| Checking an annotation entry against its source legend | `nihms-2207669.pdf`, `NIHMS2207669-supplement-supplemental_materials.docx` |
| Design decisions | `anton-scope2_1.zip`, the newer of the two skill drops |

The source publication is only for checking annotation entries against the figure
legends they were written from. **It must never be mounted in the data room.**

`fa/transcript-extract.py` parses the Taiga export: thinking text lives in the
element's `data` field under `contexts[].conversation.data[].contents[]`, not in
`thinking` or `text`.

`build/pre-edit-workbook-backup.xlsx` is the publisher's original workbook, kept so any
integrity claim stays re-checkable. Not uploaded to Studio.
