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

## 1. START HERE — the one thing blocking the re-run

Everything mechanical is done and verified. **What has not happened is any independent
read of the renamed files.**

The last change was a 194-replacement rename across the workbook, the annotation, the
golden and two scripts, plus eight annotation edits and six golden edits. Every check
run against it since is mechanical: string counts, audits, correspondence, provenance
greps. All green. But:

- the earlier solvability check passed against the **pre-rename** files
- the leakage red-team read the **pre-rename** files
- the same class of bulk rename corrupted 73 identifiers the first time it ran
- a red-team found a published-compound-name leak in files that had already passed
  four of my own provenance sweeps

My own verification has twice been insufficient on exactly this kind of change.
**Re-run the sweep before shipping.** Four agents:

1. **Leakage red-team.** Isolated sandbox, only the two shipped data-room files plus
   `task/prompt.txt`. No repo access, no web. Brief it adversarially — to *disprove*
   the claim that the files are an internal dump. Point it at zip internals, PDF
   object-level metadata and XMP, font names, prose register, and whether the original
   figure-panel scheme is recoverable. **Tell it explicitly to search for published
   compound, product and reagent names**, which is the check every earlier sweep of
   mine lacked and the reason this branch exists. Make the enumeration a named
   deliverable: every compound, product, reagent, catalogue and protocol identifier in
   both files, with a verdict per identifier on whether it resolves to a real published
   entity and to what. The sandbox has no web, so that enumeration is parametric
   knowledge only and a real-but-obscure name can pass it — **run a separate web pass
   over the returned list, outside the sandbox.** That is how rename 3's `AVB-101`
   collision was found, and no earlier sweep would have caught it.
   Also give it the annotation's `as printed` register as an explicit target: section 6
   records the user's decision to keep it and the reasoning, and the open question is
   whether an independent read calls it a pointer at a *publication* or merely at an
   internal upstream source.
2. **Solvability, two agents.** Isolated, prompt plus the two files only, no answer
   key. Ask for a full analysis plus an exhaustive derivation log marking every
   question DERIVED / BLOCKED / AMBIGUOUS. Write the grading checklist *before* the
   reports land.
3. **References.** Repo access. Recompute every cited number. Tell it
   `build/audit-golden.py` is **not** authority — same author as the golden, so they
   can share a mistake.

A leg counts as solvable if at least one agent derives it. An agent reaching a
different conclusion from the golden is not a failure; only an underivable leg is.

Expect and do not treat as defects: the workbook's internal contradictions, both
`S09-A` headers reading 16h, `S06-D` duplicating `S06-C`, `S15-L`/`S15-N` carrying no
stated challenge virus, the unlabelled region at `S08` rows 89–101, no timepoint past
72 h, no HA dose-ranging, no per-animal link between an immune measure and an outcome.

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
python3 -I rename-assets.py --check   # dry-run the rename rules and the never-touch guard
```

The first two must be green before any upload. No scipy, no lifelines — log-rank is
Mantel-Cox inline, t-tests via an inline incomplete beta.

---

## 4. The five shipped artifacts

| Upload as | File | Bytes | sha256 |
|---|---|---|---|
| Prompt | `task/prompt.txt` | 1,187 | `cfc0f29bde3c` |
| Grader guidelines | `task/grader-guidelines.txt` | 3,717 | `4b166be59225` |
| Data room | `data-room/adjuvant_program_dataset.xlsx` | 56,787 | `f293502992c7` |
| Data room | `data-room/trial_summary.pdf` | 59,695 | `842e9dcdf179` |
| Reviewer golden (either) | `task/golden-response.txt` | 23,800 | `9ba947f20db4` |
| Reviewer golden (either) | `task/golden-response.pdf` | 41,361 | `43865c1c27e4` |

Prompt is 201 words, grader 576. Check each paste against `build/paste-checks.txt`,
which carries word count, character count, hash prefix and required last line. The
line-break property is the one a diff will not show you: confirm in the form that each
paragraph is still a single unbroken line, and that the grader's C list is present at
the bottom.

**Never upload a `.md`.** `task/golden-response.md` is the authored source;
`make-artifacts.py` generates `.txt` and `.pdf` with content verified identical, and
one of those goes in the form. The project guideline banning `.md` is not scoped to the
data room, so neither is this.

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
7. **No `.md` anywhere in the upload.**
8. Assume the solver image has the packages it needs.
9. **Generic and non-proprietary items carry no leak exposure and stay.**
    **CORRECTION, rename 4:** this decision's premise is wrong about one item.
    `ADU-S100` is not generic — it is a named clinical-stage asset, the CDN STING
    agonist ML RR-S2 CDA, Aduro Biotech, licensed to Novartis as MIW815, Phase 1,
    dropped from the portfolio in 2019. The user's decision to keep it still stands and
    is defensible on different grounds: it is the field's standard published tool CDN,
    real preclinical programmes name their tool compounds, and an invented CDN name
    would make the room less realistic while touching forcing-chain leg 3. But the
    exposure it carries is not zero, and it is not the string — it is the fingerprint.
    ADU-S100 plus manganese coordination polymer plus pulmonary-surfactant-biomimetic
    liposome plus aged mice plus heterosubtypic influenza locates the paper with no
    compound name at all. Renaming the asset does not close that. BEI
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
12. **Any workbook edit is zip-level, sheet entries only.** Never an openpyxl
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

**Two findings it got right that are still open.** The annotation PDF is stamped
2026-03-07 while the workbook it describes is stamped 2026-09-03, so the annotation
predates its subject by six months — one epoch constant in `make-annotation-pdf.py`. And
the room's *structure* is a figure set: the publisher original's sheets are literally
`Fig.1` … `Fig.7`, `Fig. S1`, `S2`, `S3`, `S4`, `S7`, `S8`, `S12`, `S13`. Rename 1
flattened seven main and eight supplementary figures into a contiguous `S01`–`S15`,
erasing both the main/supplement split and the gaps. The red-team reconstructed the seam
without ever seeing that file: its `S06` survival ↔ `S15` weight pairing is
`Fig.6` ↔ `Fig. S13`. No rename fixes this; it is the shape of a supplementary data
file, which standing rule 1 makes the room.

**The lesson from rename 4, which is not the same as rename 1's or 2's.** The red-team
that found Leak 2 classified `AMnESTI` as "INVENTED — contrived backronym with Mn
embedded." Exactly wrong, and instructively so: it *is* a contrived backronym, because
the authors contrived it. An isolated red-team has no web access, so its identifier
enumeration is parametric knowledge only and systematically cannot catch a real name it
does not happen to know. **Always run a web pass over the enumeration it returns,
outside the sandbox, in extended search mode.** Standard mode returned nothing for
`AMnESTI`; extended mode returned the paper as the first result. That difference is what
the whole branch turned on.

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
- **Golden vs grader:** all 8 A items met with quoted passages, 0 of 9 B penalties
  tripped, no double-classification, no placement or ordering requirement, every A item
  traceable to something the prompt asks.
- **Golden arithmetic:** an independent agent recomputed ~180 numeric claims and
  **every one reproduced exactly** — all 24 log-rank p-values, every survival count,
  geometric and arithmetic means, per-animal ratios, `10^mean(log10)` values and Welch
  p-values. No number in the golden is wrong.
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

**Blind spot now closed:** `audit-golden.py` previously checked no survival percentage
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
