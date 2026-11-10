# Anton task psql25c1 — PSLN-344 mucosal adjuvant

RLS short ID `psql25c1` · task `task_4ce55343502b4d17b2182158ad6e4533` · campaign
`camp_0589d1e96758477586df0e43dd8eeec1`

[Open in Studio](https://studio.mercor.com/annotator/tasks/task_4ce55343502b4d17b2182158ad6e4533/?campaignId=camp_0589d1e96758477586df0e43dd8eeec1)

## What ships

| Upload as | File |
|---|---|
| Data room | `data-room/adjuvant_program_dataset.xlsx` |
| Data room | `data-room/trial_summary.pdf` |
| Prompt | `task/prompt.txt` |
| Grader guidelines | `task/grader-guidelines.txt` |
| Reviewer Facing Golden Response | `task/golden-response.txt`, or `.pdf` if the field takes a file |

Nothing in `build/` is uploaded. **No `.md` file is uploaded anywhere**, data room or
otherwise. `task/golden-response.md` is the authored source; `make-artifacts.py`
generates `.txt` and `.pdf` copies with identical content, and one of those is what
goes into the form.

Before uploading, check each pasted field against `build/paste-checks.txt`, which
carries the word count, character count, hash prefix and required last line for
the prompt and the grader. The line-break property is the one a diff will not show
you, so confirm in the form that each paragraph is still a single unbroken line.

## What generates what

`build/anton-brief-psql25c1.md` is the design document and the single source for
the prompt and the grader. `build/annotation-source.md` is the single source for
the annotation PDF. The shipped copies are generated and are never edited by hand.

```
python3 -I make-artifacts.py          # regenerate all shipped artifacts
python3 -I make-artifacts.py --check  # fail if any shipped copy has drifted
```

Run the check before any upload. It exists because the prompt and the grader
appear both in the brief and as standalone files, and a copy edited in one place
and not the other is the failure this repo is arranged to prevent.

## Verifying the golden

```
python3 -I audit-golden.py     # recompute every figure in the golden, diff against the document
python3 -I audit-registry.py   # print the full verified value set, for tracing any figure to source
```

Both read the shipped workbook and run on the standard library alone. Log-rank is
Mantel-Cox implemented inline, so neither needs lifelines or scipy. The build
constraint requires the golden to be recomputed after the data room's last edit;
`audit-golden.py` is how that is done.

## Layout

```
data-room/   what the solver sees
task/        what is uploaded to Studio alongside the data room
build/       sources, generators and verification. Not uploaded.
```
