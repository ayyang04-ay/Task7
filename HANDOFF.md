# Handoff — Anton task psql25c1 (AMnESTI mucosal adjuvant)

Repo `ayyang04-ay/Task7`, branch **`claude/exciting-cray-mkihzd-v2`**, HEAD `e5f8226`,
working tree clean, all work pushed. Develop and push here.

**Do not build on `claude/exciting-cray-mkihzd`.** That is the pre-rename history and
it shipped a leak. v2 exists because of it.

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
   mine lacked and the reason this branch exists.
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

**Source material** is Gao et al., Sci Immunol 2026;11(123):eadz5242. Its
supplementary data file is the data room. The publication is NOT mounted and must stay
unmounted. Licence was checked by the user against the AAAS policy page and cleared —
do not reopen it.

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
```

The first two must be green before any upload. No scipy, no lifelines — log-rank is
Mantel-Cox inline, t-tests via an inline incomplete beta.

---

## 4. The five shipped artifacts

| Upload as | File | Bytes | sha256 |
|---|---|---|---|
| Prompt | `task/prompt.txt` | 1,185 | `ad26031a9b9c` |
| Grader guidelines | `task/grader-guidelines.txt` | 3,716 | `59c80b9d1fd8` |
| Data room | `data-room/amnesti_preclinical_dataset.xlsx` | 56,830 | `f52687b64766` |
| Data room | `data-room/trial_summary.pdf` | 59,731 | `1652d1d66813` |
| Reviewer golden (either) | `task/golden-response.txt` | 23,738 | `7a2f4645020d` |
| Reviewer golden (either) | `task/golden-response.pdf` | 41,453 | `5170d5435bad` |

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
9. **Generic and non-proprietary items carry no leak exposure and stay.** BEI
   catalogue numbers (`NR-3177`, `NR-348`, `NR-41803`, `FR-201`), every strain name,
   `ADU-S100`, `R848`, the lipid names, `INCB3344`, `Clodrosome`, carbenoxolone,
   `OT-I`, `Sftpa1-/-Sftpd-/-`. Strain names are additionally load-bearing: the subtype
   classification is derived from them.
10. **No reagent glosses.** Mechanism explanations for common reagents were removed;
    `Carbenoxolone (CBX)` keeps its parenthetical on the user's instruction.

---

## 6. What remains

**Blocking:** the sweep in §1. Nothing else.

**Then:** resubmit, re-run the panel, write the FA.

**Two open user calls, both offered and neither answered:**

- **The annotation's "as printed" / "as found" register.** Every entry is framed as a
  third party transcribing an external artifact. The red-team read that as a provenance
  tell and is right that it is one. I had argued for keeping it because both
  solvability agents quoted those phrases back as useful signals about which fields are
  the workbook's own claims — but that was weak evidence for a *leak* question, since
  those agents were not looking for leaks, and **I withdrew the recommendation.**
  Rewriting the framing across 102 entries is a substantial edit nobody has authorised.
  Ask first.
- **`AUP-0417`.** The animal-protocol identifier. The original was a real searchable
  number from the source publication's methods and is gone. This replacement was
  invented in-session; it resolves to nothing and is not a leak. The red-team ranked it
  its top finding on the false premise that it points at a real registry — it does not,
  and it could not have known that. Its weaker point stands: the `AUP-####` format
  reads academic rather than corporate, which fights the "our asset" framing. Cosmetic
  realism only. Options offered: a corporate-style ID, keep as is, or drop the number.

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
`Naïve+AVB-101`. The rename script lives in the session scratchpad only, not the repo.

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
w=openpyxl.load_workbook('data-room/amnesti_preclinical_dataset.xlsx',data_only=True)
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
