Batch lw0b5ba6-v2 — task_f9c4675def384c5e820284adce63119b, problem version v2, 8 runs

THIS IS THE LIVE PANEL. It answered revision 7 of the prompt, which is what
task/prompt.txt currently holds. The earlier batch in fa/lw0b5ba6/ answered a
different and now-retired prompt.

  as-run task_prompt.md   006aa3ff6c6b raw, 252 words
  task/prompt.txt         e75574f8f69a, 252 words
  identical after normalising the Studio form's blank-line padding: YES
  (both normalise to a66d62de41a1)

Run map, from job_info.json and all_runs.csv. Not constructed.

  Label  Model              Attempt  Short      Score  Job
  O1     claude-opus-5-5    1        f295b831   0.93   70ccbec0
  O2     claude-opus-5-5    2        e8634c7e   0.87   70ccbec0
  O3     claude-opus-5-5    3        978e3829   0.90   70ccbec0
  O4     claude-opus-5-5    4        e7837212   0.92   70ccbec0
  F1     claude-fable-5-2   1        1e154279   0.95   8de89bb3
  F2     claude-fable-5-2   2        355880fe   0.94   8de89bb3
  F3     claude-fable-5-2   3        f644c65d   0.90   8de89bb3
  F4     claude-fable-5-2   4        c54ffab8   0.95   8de89bb3

  Opus mean 0.905, Fable mean 0.935, panel mean 0.920.
  For comparison, the retired panel ran 0.926.

Problem version 3619eae7 (v2), created 2026-11-19 16:00 UTC, tag "In Development",
environment vert_bio_v001_MER, grading agentic_grader / single_score.
Jobs created 16:00 UTC; Opus completed 17:40, Fable 22:15. All 8 completed, 0 failed.

Layout matches fa/lw0b5ba6/: deliverables/<label>/, grading/<label>_<hash>, meta/<job>/, qa/.

Not unpacked here, to avoid duplicating what the archives already hold. Both live in
fa/exports/lw0b5ba6-v2/: the 8 transcripts and the output binaries (PDF, DOCX, XLSX,
HTML, PNG).

QA v2 in qa/qa_report.md — 8 findings across 7 runs. The v1 asset-identity error is
GONE: naming PSLN-344 and PSLN-212 closed it. What remains is the grader-reference
error, carried over from v1, plus a new info-level prompt finding that the prompt does
not say what each of the two codes IS, and that "my asset" is singular beside two
designations.
