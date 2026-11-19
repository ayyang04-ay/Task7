# Anton_f9c4675def384c5e820284adce63119b_job_291ac55a_2026-11-19

- **Task ID**: `task_f9c4675def384c5e820284adce63119b`
- **Taiga job**: `291ac55a-9ab4-48e0-8c2d-e44bf3bb99e7` — `Studio - task_f9c4675def384c5e820284adce63119b`
- **Status**: `completed`
- **Environment**: vert_bio_v001_MER (`2e3eb299-7d22-4082-be2e-180e73ccf90d`)
- **Model**: claude-opus-5-5
- **Created**: 2026-11-19T06:02:18.668494Z
- **Grader**: agentic_grader (claude-opus-5-5)
- **Attempts**: 4 completed / 4 total — 4 scored
- **Score**: mean **0.918** over 4 SCORED attempt(s)  ·  0 refused (Trust & Safety)  ·  4 of 4 rollouts reached the model
- **Pass counts**: pass@0.8 4/4  ·  pass@0.5 4/4
- **Submit gate (Avg Score Under 55%)**: **NOT CLEARED** — mean 0.918 > 0.55. The model solved this task too often; it needs to be made harder before it ships.

## How to read the score

Anton grading is **agentic**: an external grader container reads the run's
transcript against the writer's grading guidance and returns ONE normalized
score in `[0,1]`. There is no partial-credit arithmetic to re-derive by hand —
the number is the grader's judgement, and its reasoning is in the grading record.

**The submit gate is inverted.** A task ships only if the model does **NOT**
solve it: the bar is *Avg Score Under 55%*
(mean ≤ 0.55). A HIGH mean is a FAILING task, not a good one —
it means the model handled the problem and the task needs to be made harder.

A Trust & Safety refusal is a third outcome, neither a pass nor a fail. The
classifier blocks the turn before the model answers, so the rollout produces no
function call and no work: it is a void. Refused attempts appear as `T&S` in the
table below, carry `refused: true` in `all_runs.json` / `all_runs.csv`, and are
excluded from the mean and from every pass count.

## Export selection

Included clusters: outputs, transcripts, grading. **Excluded** (not in this export): task_files, grader_files.

Only the selected clusters are present in this bundle (the always-on metadata —
README, job_info, all_runs, task_prompt, grading_config, and the manifests — is
always included; the manifests keep the gs:// references for excluded clusters).

## Layout (selected clusters only)

```
Anton_f9c4675def384c5e820284adce63119b_job_291ac55a_2026-11-19/
├── README.md                   this file
├── job_info.json               job metadata + score stats + submit-gate verdict
├── all_runs.json               per-attempt summary (score, refused, status, file pointers)
├── all_runs.csv                same, flat — one row per attempt, one sub_* column per subscore
├── task_prompt.md              the task prompt the model received
├── grading_config.json         grader type/model + grader guidance + rubric (input grader info)
├── input_files_manifest.json   task_files/ summary + original gs:// references
├── output_files_manifest.json  per-run outputs/ summary + original gs:// references
├── grader_files_manifest.json  grader_files/ summary + original gs:// references
├── task_files/                 the task data room the model saw at /tmp/world
│                               (extracted from its bundle)
├── grader_files/               the writer's GRADING artifacts (grader-only, NOT
│                               model-facing): golden / reference solution, answer
│                               key & answer spec, grading prompt / spec, verifier
│                               script, and ground-truth values
├── outputs/                    per-attempt model output files (the out_dir),
│                               one folder per attempt: outputs/attempt_NN_<run>/
├── grading/                    full grading record per attempt (score, subscores,
│                               rubric evaluations, the grader's own transcript)
└── transcripts/                Taiga Conversation JSON — ALL 4 attempts
```

## Per-attempt scores

`T&S` = the rollout was blocked by the client's Trust & Safety classifier: void,
not zero.

| att | run | status | score |
| :-: | :-- | :-- | --: |
| 01 | `3ac7375f` | completed | 0.93 |
| 02 | `9e317553` | completed | 0.93 |
| 03 | `619b246b` | completed | 0.90 |
| 04 | `e5c8a16c` | completed | 0.91 |

## Notes

- Anton grading is **agentic** (`agentic_grader`): a single
  normalized score in `[0,1]` with the grader's reasoning. The full record per attempt is
  in `grading/attempt_NN_*.json` (subscores, `metadata.rubric_evaluations`, and
  `metadata.grading_transcript` — the grader's own run). Refused attempts have no record.
- Raw file BYTES are now included. task_files/ holds the input data room the writer submitted (mounted at /tmp/world for the model); the read-only tool mounts (/opt/weights, /opt/refdbs) are listed but never downloaded. outputs/attempt_NN_*/ holds each run's produced files (the out_dir). The original gs:// references are still listed for provenance. Transcripts (all attempts) and the full grading record (incl. the grader's own transcript and rubric evaluations) are also included.
- grader_files/ holds the writer-authored grading artifacts the grader sees but the model never does — the golden / reference solution, answer key & answer spec, the grading prompt / spec, the verifier script (checker.py / grader.py / verify.py), and ground-truth values. Pulled from the problem version's grader volume (mounted at /tmp/grader_files for the grader). Reuse these to re-derive and audit each run.
