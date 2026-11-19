Batch lw0b5ba6 — task_f9c4675def384c5e820284adce63119b, 8 runs, 2026-11-19

Run map, from job_info.json and all_runs.json. Not constructed.

  Label  Model              Attempt  Short      Score  Job
  O1     claude-opus-5-5    1        3ac7375f   0.93   291ac55a
  O2     claude-opus-5-5    2        9e317553   0.93   291ac55a
  O3     claude-opus-5-5    3        619b246b   0.90   291ac55a
  O4     claude-opus-5-5    4        e5c8a16c   0.91   291ac55a
  F1     claude-fable-5-2   1        32ae525e   0.94   3d83f32b
  F2     claude-fable-5-2   2        723b22d4   0.95   3d83f32b
  F3     claude-fable-5-2   3        05938b91   0.91   3d83f32b
  F4     claude-fable-5-2   4        1341e698   0.94   3d83f32b

Environment vert_bio_v001_MER. Problem version e031e3a6 (v1), tag "In Development",
grading agentic_grader / single_score. All 8 completed, 0 failed.

Layout

  deliverables/<label>/   each run's own output files, text only: proposal markdown,
                          analysis code, CSV and JSON tables, READMEs
  grading/<label>_<hash>.json   the grader record per run, including its rationale
  meta/<job>/             job_info.json, all_runs.json, all_runs.csv,
                          input_files_manifest.json, grading_config.json, task_prompt.md
  qa/                     the v1 Taiga QA export, unpacked: qa_report.md, qa_items.json,
                          qa_jobs.json, qa_status.json, problem_version.json

Not unpacked here, to avoid duplicating 128 MB that the archives already hold.
Both live in fa/exports/lw0b5ba6/:

  transcripts/      8 files, 86.43 MB. The per-run transcripts.
  output binaries   77 files, 41.43 MB. PDF, DOCX, XLSX, HTML, PNG.

The prompt these runs answered

  meta/<job>/task_prompt.md is sha256 42129eee4c00, 225 words. It is NOT the copy in
  task/prompt.txt (bf4e427cdf08, 231 words). The substantive difference is the
  per-study ask: as run it requests endpoints only, where the repo copy requests
  endpoints, populations, comparators, readouts and timing.
