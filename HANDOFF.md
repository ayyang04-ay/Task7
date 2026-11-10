# Handoff — Anton task psql25c1 (AMnESTI mucosal adjuvant)

Written at the end of a long session. A new session starts here.

Repo `ayyang04-ay/Task7`, branch `claude/exciting-cray-mkihzd`, all work pushed.
RLS short ID `psql25c1`, task `task_4ce55343502b4d17b2182158ad6e4533`, campaign
`camp_0589d1e96758477586df0e43dd8eeec1`.

---

## 1. What this is

An Anton eval task (Mercor, preclinical drug R&D). A solver gets a prompt and a
data room and has to recommend whether to advance an adjuvant. The deliverable
that matters is the **failure analysis**, written by hand by the user in Studio,
on what the panel of solver runs got wrong. Build artifacts exist to produce
transcripts, not to score well.

Read `/root/.claude/skills/.../anton-scope2/SKILL.md` and its `references/` before
making design decisions. Read `anton-fa` before touching the FA.

**Source material** is Gao et al., Sci Immunol 2026;11(123):eadz5242. Its
supplementary data file is the data room. The publication is NOT mounted and must
stay unmounted. Licence was checked by the user against the AAAS policy page and
cleared; do not reopen it.

## 2. Repo layout

```
data-room/   what the solver sees: amnesti_preclinical_dataset.xlsx, trial_summary.pdf
task/        uploaded to Studio: prompt.txt, grader-guidelines.txt, golden-response.md
build/       sources, generators, audits. NOT uploaded.
fa/          failure-analysis working files
HANDOFF.md   this file
```

`build/make-artifacts.py` regenerates prompt.txt and grader-guidelines.txt from the
brief and rebuilds the annotation PDF. `--check` fails on drift.
`build/audit-golden.py` recomputes every figure in the golden against the workbook.
`build/audit-registry.py` prints the full verified value set.
Run both from `build/` with `python3 -I`. No scipy or lifelines; log-rank is
Mantel-Cox implemented inline.

## 3. Standing decisions — do not re-litigate

The user settled all of these. Re-opening them wasted time once already.

1. **"Ground truth" means the data is the authoritative source for the decision, not
   that it is error-free.** The workbook's internal contradictions are a flawed real
   dataset and they STAY. Do not repair them. Standing rule 3 covers this.
2. **QA findings are overridable unless Critical.** The task priority is the FA, so
   QA matters even less. Do not spend effort on QA rebuttals.
3. **Scoring is deprecated.** The old 0.55 mean gate does not apply. The gate is
   **at least one failure mode shared by at least two runs.** That is already met.
4. **The grader is a skeleton** to help prep the FA. It does not need to be airtight.
5. **No out-of-scope line in the prompt**, no not-all-relevant line, no world-fact
   constraint on deferral. All deliberate.
6. **All 101 blocks annotated; non-load-bearing noise kept as is.**
7. **No `.md` file in the data room.** Annotation ships as PDF.
8. Assume the solver image has the packages it needs.

## 4. State of the four artifacts

| | Status |
|---|---|
| Prompt | Done. 201 words, flat text, all four 7-Nov deprecations absent. Unchanged by any repair below |
| Data room | Done. Corruption reverted, hyperlinks stripped, bullet glyph fixed, drift check now covers the PDF |
| Golden | Done. 5.5 to 5.10 all applied; `audit-golden.py` green including new checks on the six-readout claim and on S15-H |
| Grader | Done as a skeleton. Re-checked against the rewritten golden: the only mention of the innate alternative is in the neutral C list, which permits either position, so nothing trips |

**Everything in section 5 below is now done.** It is kept as the record of what was
wrong and what the fix was, because the FA write-up needs it and because 5.11 is
still the user's call. One item is new and open: see 5.12.

## 5. Work that was outstanding — all done except 5.11 and 5.12

### WAS BLOCKING, NOW FIXED

**5.1 — 73 corrupted strings, 27 of them in the shipped PDF.**
A bulk rename of block labels used bare panel tokens as plain substring
replacements, which fired inside unrelated identifiers:

| Was | Became | Rule that fired |
|---|---|---|
| `H5N1` | `HS05-I1` | `5N` -> `S05-I` |
| `Ly6C` | `LyS06-B` | `6C` -> `S06-B` |
| `Ly6G` | `LyS06-D` | `6G` -> `S06-D` |
| `H-2Db` | `H-S02-Cb` | `2D` -> `S02-C` |
| `H-2Kd` | `H-S02-Hd` | `2K` -> `S02-H` |

In `build/annotation-source.md`, `task/golden-response.md`,
`build/anton-brief-psql25c1.md`, `build/audit-golden.py` line 87, and the shipped
`data-room/trial_summary.pdf`.

**This breaks forcing-chain leg 2.** The annotation now reads "rgVN04 HS05-I1
comprises the H5 and N1 genes of A/Vietnam/1203/2004". A solver classifies which
challenges are heterosubtypic by reading the challenge virus subtype out of that
sentence. Mangled, the classification is not derivable. `Ly6C` and `Ly6G` define
the monocyte and neutrophil gates.

**The workbook itself is clean.** It still carries the correct identifiers (4
occurrences, 0 corrupted). So the annotation now contradicts the workbook it
describes: `S07` header reads `CD11b+Ly6C+ Monocytes` while the annotation calls
that block `CD11b+LyS06-B+CD11c-LyS06-D-`. A solver reading both shipped files sees
a direct disagreement between them.

Fix: revert all five strings in the four text files, then
`cd build && python3 -I make-artifacts.py` to rebuild the PDF. Do not touch the
workbook.

Verification, before and after:

```bash
cd /home/user/Task7
for s in HS05-I1 LyS06-B LyS06-D H-S02-Cb H-S02-Hd; do
  printf '%-10s ann:%s gold:%s brief:%s\n' "$s" \
    "$(grep -c "$s" build/annotation-source.md)" \
    "$(grep -c "$s" task/golden-response.md)" \
    "$(grep -c "$s" build/anton-brief-psql25c1.md)"
done
python3 -I -c "from pdfminer.high_level import extract_text as e; t=e('data-room/trial_summary.pdf'); print({s:t.count(s) for s in ('HS05-I1','LyS06-B','LyS06-D')})"
```

Current counts: annotation 15/7/1, golden 3/2/0, brief 4/1/0 plus 2 `H-S02-Cb` and
1 `H-S02-Hd`, PDF 16/10/1. All must reach zero. `audit-golden.py` line 87 also
carries a `LyS06-B` dict key.

**5.2 — 20 hyperlink artefacts in the workbook name the pre-rename compound.**
`xl/worksheets/sheet13.xml` and `sheet15.xml` plus their `_rels` carry
`display="NanoSTING@Mn"` and `Target="mailto:NanoSTING@Mn"` on ten cells whose
visible value is `AMnESTI`. They came with the publisher's file, not from this
build, but they are residual provenance in a file presented as internal. An
adversarial agent found them with no external lookup and called them a smoking gun.

Fix: strip every `<hyperlinks>` block and the `mailto:` rels from all worksheet
parts. Also normalise `docProps/app.xml`, which still reads
`Openpyxl 3.1.5`, and give created/modified a plausible spread rather than an
identical timestamp.

**5.3 — The replacement rule set is unsafe to re-run.**
`build/replacements.json` holds 505 rules of which 125 are bare panel tokens.
Delete those 125 or gate them on a `Fig` prefix. As it stands, anyone re-running it
repeats 5.1.

**5.4 — `make-artifacts.py --check` does not cover the annotation PDF.**
It only diffs prompt.txt and grader-guidelines.txt against the brief. That is how a
shipped data-room file carried 27 corruptions through a green drift check. Extend it.

**5.5 — The golden asserts a gap the data room closes.**
It says day-3 protection is "equally consistent with a non-specific antiviral state
left by STING activation", and Study 1 names "adjuvant alone with no antigen" as the
arm that would settle it.

That arm is already in the room. **S15-H**: adjuvant alone at the 3-day interval,
**0 of 7 survive** (deaths days 5,5,6,6,6,7,8); vaccine alone 0 of 7; vaccine plus
adjuvant 6 of 7 (single death day 12). Antigen and adjuvant are both required and a
non-specific antiviral state protects nobody. The golden never cites S15-H.

Fix: cite S15-H, withdraw the unexcluded-alternative framing, drop that Study 1 arm.
This is the most consequential defect; two independent agents found it.

**5.6 — "The five readouts the adjuvant raises" is six, and both headline ranges
are wrong.** Ifnb1 at 72 h is also raised: 1.29x aged, 1.97x young, both computable
from the golden's own four-arm table. The recommendation states aged 1.65 to 24.35
and young 1.02 to 1.35. A reader recomputing finds 1.29 below the aged floor and
1.97 above the young ceiling.

### WAS NON-BLOCKING, NOW FIXED

**5.7** The 0.99 Ifnb1-16h ratio is debunked as a false match in one paragraph and
then counted as one of four matched endpoints in another, and the count of four
depends on including it.

**5.8** The closing tolerability paragraph cites no block for any figure, in the one
place the golden breaks the prompt's own citation rule. Figures are correct
(S08-D day 10, S10-A, S08-A).

**5.9** `S15-L` and `S15-N` are aged, vaccinated, challenged blocks whose challenge
virus is not stated. The golden never mentions them, under an unqualified "all six
configurations". They do not change the answer: candidate 6/7 in both.

**5.10** Build-file residuals: `6K`/`6L` at brief line 290; `SS03-E` at brief 129,
291, 423; lowercase `fig.` prefixes at brief 276, 289; `S3` registry keys at
`audit-registry.py` 74, 76 which print the old scheme in script output. Two stale
assertions in `audit-golden.py` lines 43 and 106 that no longer match the golden.

**5.12 — OPEN, new. The grader treats a now-wrong answer as neutral.**
The C list calls it neutral "whether the innate alternative is resolved or left open
with a discriminating experiment". That was right when the golden thought the
alternative was open. It is not right now: S15-H settles it from the mounted data, so
a solver who leaves it open and spends a study arm on an adjuvant-alone group has
made an error, not a defensible choice. Two options, and the user picks:
either move it to a B penalty, or leave it neutral on the grounds that the grader is
a skeleton and the FA is where this gets written up. It is pre-registered as an FA
candidate either way, at the foot of `fa/error_modes.md`, with no count attached
because the existing panel was never screened for it.

**5.11 — User's call, not yet made.** The annotation carries an external academic
IACUC protocol number (`2008N000173`) and is worded in the register of third-party
annotation ("the stated n as printed in the workbook", "both are given as found",
"Groups as printed"). Both were flagged as provenance tells. Recommendation offered
and not yet accepted: drop the IACUC number, keep the BEI Resources catalogue
numbers since buying reference strains is ordinary industry practice, and reword the
"as printed"/"as found" framing while keeping the stated-n and observation-count
fields.

## 6. Verified good, do not redo

- Workbook metadata: `dc:creator`, `cp:lastModifiedBy` and the `x15ac:absPath`
  carrying the author's username and local path are all stripped. Package-wide
  sweep for author names, institutions and path fragments returns clean.
- Rename integrity: all 101 blocks have an annotation entry and vice versa; the
  mapping is complete and injective; the three deliberate label collisions survive
  (two duplicated pairs at S06 rows 69-70, the twin S09-A blocks both reading 16h);
  sheet names are opaque; both audit scripts run with no out-of-range access.
- Grader against golden: every A item satisfied with a quoted passage, no B penalty
  tripped, no item double-classified, no placement or ordering requirement, every A
  item traceable to something the prompt asks.
- Data room solvability: an agent given only the two files and the prompt, with no
  access to the answers, independently rebuilt the survival table, the subtype
  classification, the four-arm age/formulation comparison, the S09-A timepoint
  identification and the full blockade chain. It did this before the 5.1 corruption
  was introduced; the corruption is now reverted to the same strings it read, so the
  verdict holds again. **Still worth one fresh run before resubmitting**, because the
  bullet-glyph fix changed the PDF's extracted text and no solvability check has seen
  the current file.
- Corruption repair, verified three ways: zero occurrences of all five bad strings in
  every source file and in the shipped PDF; the reverted identifiers present at the
  expected counts; and `make-artifacts.py --check` extended to the PDF and confirmed
  to catch a deliberately reintroduced corruption before being run clean.

## 7. FA status — the gate is met

Three modes, all clearing the floor of two trajectories. Ledger in
`fa/error_modes.md`, defect analysis in `fa/task-defects-and-fixes.md`.

| Mode | Trajectories |
|---|---|
| Age and adjuvant confounded in the restoration metric | all 8 |
| Provenance audit substituted for the efficacy judgement | b359fc9d, 16a5e37f, 53d28969, 10d15660, d4235306, a006995a |
| Mislabelled 72 h panel identified, then no resolution work | a006995a, 16a5e37f, 5c73bcfd, 10d15660, d4235306, b359fc9d |

Notes the FA needs:
- Thinking blocks are summaries, not raw, so no claim about internal weighing is
  supportable. That rules out the raised-then-abandoned shape for this panel.
- Modes 1 and 3 are conditional on the solver electing to aggregate or to compare.
  Absence from a transcript is not evidence of correct handling; check whether the
  solver attempted the step at all before counting either way.
- A fourth candidate, the integrity audit driving the recommendation, was rejected
  then readmitted as mode 2 after the user corrected the reading of "ground truth".
- **These trajectory IDs come from the batch that ran against the old labels.** The
  analysis a solver does is unchanged by the rename, so the modes should reproduce,
  but a new batch supersedes these IDs.

## 7a. Not in the repo — the user must re-upload

A new session will not have these. They lived in the previous session's uploads and
scratchpad.

| Needed for | What to re-upload |
|---|---|
| FA, any transcript work | `Anton_4ce55343502b4d17b2182158ad6e4533_job_91694a59_2026-11-09.zip` |
| QA cross-reference, if ever wanted | `qa_report_psql25c1_v1_84eb8cc6.zip` |
| Verifying or re-authoring any annotation entry against its source legend | `nihms-2207669.pdf` and `NIHMS2207669-supplement-supplemental_materials.docx` |
| Design decisions | `anton-scope2_1.zip`, the newer of the two skill drops |

The source publication PDF is only needed to check annotation entries against the
figure legends they were written from. It must never be mounted in the data room.

`build/pre-edit-workbook-backup.xlsx` is the workbook as the publisher shipped it,
before the metadata strip and the rename. Kept so any integrity claim can be
re-checked. It is not uploaded to Studio.

## 8. Transcripts and QA

Run export and QA report are in the session scratchpad, not the repo:
`/tmp/claude-0/-home-user-Task7/3f93e5f0-693c-509b-b7f2-541df7a6a49c/scratchpad/runs/`
and `.../scratchpad/qa/`. A new session will not have these. The user has the
originals and can re-upload. `fa/transcript-extract.py` parses the Taiga export
format: thinking text lives in the element's `data` field under
`contexts[].conversation.data[].contents[]`, not in `thinking` or `text`.

## 9. What is left

1. Ask the user on 5.11 (the IACUC number and the "as printed" register) and 5.12
   (whether the innate alternative moves from the grader's neutral list to a penalty).
2. One fresh solvability run against the current data room, since the bullet-glyph
   fix changed the PDF's extracted text.
3. Resubmit, re-run the panel, then write the FA.

Before any resubmission, from `build/`: `python3 -I make-artifacts.py --check` must
report no drift and `python3 -I audit-golden.py` must report no failures. Both are
green as of this handoff.
