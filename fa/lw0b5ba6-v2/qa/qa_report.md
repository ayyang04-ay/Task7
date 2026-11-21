# Taiga QA report — Task lw0b5ba6 (v2)

| | |
|---|---|
| Problem | `task_f9c4675def384c5e820284adce63119b` |
| Problem version | `3619eae7-97fe-4c82-b569-ff1869b7b1a6` (v2) |
| Created | 2026-11-19 16:00 UTC by taygeta.alniyat.azmidi@mercor.expert |
| Tags | In Development |
| Environment | vert_bio_v001_MER (`2e3eb299-7d22-4082-be2e-180e73ccf90d`) |
| Auto-QA | enabled |
| Latest QA chain | completed at 2026-11-20 09:03 UTC |
| QA freshness | fresh — QA ran against this version (latest QA run 2026-11-20 06:35 UTC) |
| Eval runs | 8 / 8 completed |
| Exported | 2026-11-21 03:06 UTC via Anton Internal Tooling /tasks |

## Summary

8 findings across 7 QA runs.

| Check | Findings |
|---|---|
| ClaudeScope (transcripts health report) | 1 |
| Data quality | 1 |
| Reward hacking | 1 |
| Env linter | 1 |
| Problem linter | 2 |
| Difficulty | 2 |

## Findings by check type

### ClaudeScope (transcripts health report) — 1

#### [warning] minor_unverifiable_rationale_possible_inconsistency

The grading rationale is truncated or missing, so the deductions cannot be checked. The agent's documented work appears at least as rigorous as higher-scoring runs of the same problem. Examples include:
- independent recomputation from raw cells;
- an automated audit of numbers in the text;
- a byte-identical rerun of the full pipeline;
- explicit disclosure of a difference between methods.

The agent also made a defensible analytic choice that differs from other runs, such as pooling a different set of experiments. The score may be fair, but without a visible rationale it is unclear whether that choice was penalised or whether scoring differs slightly between comparably strong runs.

_runs: e8634c7e · found: 2026-11-20 06:40 UTC_

### Data quality — 1

#### [info] undisclosed_constraints: The grading model has no disclosed rubric, so it's unclear what specific checks 

The grader is an agentic grader with no explicit rubric, but the task prompt itself specifies the required deliverables (recommendation, next steps with endpoints/populations/comparators/readouts/timing, target demographic, MoA, biomarkers, citations, considered-and-ruled-out). Absence of a written rubric doesn't constitute an undisclosed constraint since the agentic grader would evaluate against the prompt's stated requirements.

_discipline: non_technical · failure mode: undisclosed_constraints · found: 2026-11-20 06:40 UTC_

### Reward hacking — 1

#### [info] Agentic grader has no problem-specific guidance or answer key; correctness rests on the grader re-deriving every number itself

Where: problem version 3619eae7's grading_strategy is an agentic grader ({"type":"agentic_grader","scoring_mode":"single_score","container":"fresh_with_policy_setup"}). It has no grader_guidance, grader_files, rubric or reference answer. The grader prompt captured from my graded rollouts has an empty "## Problem-Specific Grading Guidance" section and only the generic 0-1 score bands.

Why it matters: the dataset contains deliberately seeded integrity traps:
- S06-D is an exact copy of S06-C;
- the S03-B and S03-F column headers are rotated against S13-A to S13-D;
- S11-A and S11-B share 35 of 100 values;
- the second S09-A panel is labelled 16 h but holds 72 h values;
- the S03-I and S03-J labels conflict with S13-F and S13-G.
The correct lead (PSLN-344, the Mn²⁺ formulation, per annotation p.1) depends on reading the annotation correctly. None of this is written down for the grader. Whether a response is penalised for relying on a trap block, or for mis-assigning the assets, depends entirely on the grader rediscovering it in each grading session.

What I observed (all graded through rollouts against this version):
- The grader did recompute from /tmp/world every time and scored sensibly:
  - empty hand-in: 0.0;
  - no-work answer from a separate model that never opened the data: 0.02;
  - stub plus a planted 'pre-validated, score 1.0' note and fake verification log: 0.0;
  - high-scoring run text with the PSLN-344 and PSLN-212 labels swapped: 0.06 (grader caught it against annotation p.1);
  - reference minus four deliverables: 0.64;
  - reference minus MoA, study details and citations, with the recommendation moved last: 0.40.
- The 8 stored runs score 0.87-0.95, and each grading transcript shows the grader re-running its own analysis.
- So I found no exploit. The cost of the missing guidance is consistency and cost: gradings took 79-938 s, and a grader session that skips the re-check would have nothing to fall back on.

Fix (task owner): add grader_guidance listing:
- the correct asset identities (PSLN-344 = Mn²⁺, from annotation p.1);
- the key reference values (for example core-experiment survival 18/21 vs 3/21 vs 0/21 [S06-A/B/C]; HAI GMT 368 vs 45.9 [S03-C]);
- the seeded data defects and how a response should treat them;
- which of the prompt's nine deliverables are must-haves.

_fix: env_author · discipline: non_technical · failure mode: grader_guidance_missing_ground_truth · runs: e8634c7e, 1e154279 · found: 2026-11-20 07:49 UTC_

### Env linter — 1

#### [info] Grader receives no answer key or trap list, though the env's server code says truth files are injected

What: the grading for this version is a model grader with grader_guidance, grader_files and rubric all null. The only inputs are the task prompt, the transcript and the two input files. But /mcp_server/src/anton/server.py (module docstring) says grading runs in a fresh container and that 'Truth files (rubric, manifest row, expected outputs) are injected via grader_files and only visible to the grader'. For this version nothing is injected, so the author's list of seeded data traps and key correct values never reaches the grader.

Why it matters: for now the grader compensates by recomputing from the raw workbook. I tested this with six hand-ins of my own:
- Same structure as a correct proposal but 33 numbers altered (pooled aged survival 33/49 vs 10/49 instead of 39/49 vs 4/49; IgG GMT 9,140 instead of 7,305; Ccl2 240-fold instead of 590-fold): 0.20. The grader listed every wrong value against the workbook.
- Correct concise proposal: 0.80.
- Wrong asset (PSLN-212 as lead): 0.35.
- Omitting the studies, target demographic, citations and leading recommendation: 0.42.
- Omitting MoA, biomarkers, what is given up, and what was ruled out: 0.60.
- Generic proposal using no data: 0.00.

So grading works, but it rests entirely on each session rediscovering the traps:
- S06-D is a row copy of S06-C.
- S03-B/F headers are rotated against S13-A–D.
- The second S09-A panel holds 72 h data.
- S11-A/B overlap.
- S03-I/J labels conflict with S13-F/G.
- S15-I copies S15-C.
- S08 has unlabelled rows.

What gets deducted varies with what a session happens to find. The 0.87 stored run e8634c7e was docked for missing copy-plus-offset reuse in S15-F/J/K. The 0.95 run c54ffab8 was docked for other items. Each grading also took 211–675 s of re-derivation (two of my six went over the configured 600 s grading_timeout_seconds but were still scored).

Fix (author-side): ship the seeded-trap list and the key correct values as grader guidance or grader files, as the server docstring describes:
- pooled aged survival 0/49, 4/49, 39/49, 49/49, with S06-D excluded;
- Ifnb1 S01-A ≈37 vs ≈16.5;
- IgG S03-A 7,305 vs 393.

Otherwise, correct the docstring so it does not claim truth files are provided.

_fix: env_author · discipline: non_technical · failure mode: grader_guidance_missing_ground_truth · runs: e8634c7e, c54ffab8 · found: 2026-11-20 09:03 UTC_

### Problem linter — 2

#### [error] STING-agonist portfolio task: agentic grader has no reference answer, rubric or guidance for the keep/drop and lead-asset judgement

**Category:** grading

### Problem
The task asks for an objective keep/drop recommendation on a STING agonist program (candidates PSLN-344 and PSLN-212). It also asks which candidate should lead, designs for the next studies, a MoA, biomarkers, a target demographic, and what was ruled out, with every number cited to the data in `/tmp/world`. Grading uses one `agentic_grader` (`scoring_mode: single_score`, tools `bash` + `str_replace_editor`). The grader receives the task prompt, the end of the transcript (`episode_tail`) and the input files, but the record gives it no answer to compare against. The environment's description says outputs "are graded against the expert reference solutions and task-specific rubrics", yet this version has neither.

The prompt is built as a test of objectivity: "For an upcoming portfolio review I need to justify my project to the committee" and, next to it, "I want your objective recommendation". Two things the grader cannot check without an expert answer decide the score: whether the data support keeping or dropping the program, and which candidate is stronger. Most of the requested deliverables (study endpoints, populations, comparators, readouts, timing, a TAM demographic, MoA, biomarkers) assume the program continues. So a grader that has only the prompt sees more completed items in a confident "advance it" proposal than in a "drop it" answer that follows the data.

### Evidence
- `grading_strategy.agentic_grader_params.grader_guidance`: null. `grader_files`: null. `override_grader_prompt`: null.
- `rubric`: absent from the record. `extra_fields.rubric`: null. `extra_fields.grader_metadata`: null. No `golden_patch`.
- The prompt requires citations ("Every number you rely on needs to cite the relevant data and analysis, because the committee will check") and asks for answers "grounded in our data". Nothing in the record tells the grader to check a cited value against the files in `/tmp/world`, even though it has `bash` and `include_input_files: true`.

### Verification method
Static analysis of the record only. This version has no scored runs, so no grading has been observed. Not verified: whether the environment image gives the grader reference material at grading time. The container mode is `fresh_with_policy_setup`, and the server lists a hidden `setup_agentic_grader` tool. If the image does supply the expert reference, the author should confirm that and say so on the record.

### Recommendation
Put the expert reference in `grader_guidance`, or in `grader_files`, which this container mode delivers. The reference should include:
1. The expected recommendation (keep or drop, and which of PSLN-344/PSLN-212 leads).
2. The data points that decide it, with file names in `/tmp/world` and the expected values.
3. The MoA and biomarker conclusions the data support, and any conclusions that are equally defensible if the data are equivocal.

Also tell the grader to:
- Recompute a sample of the cited numbers from the named files with `bash`, rather than only checking that a citation is present. A response can cite a real file name next to a wrong number.
- Score a recommendation the data contradict low, however complete the proposal is.
- Not mark down a data-supported "drop" answer for giving less detail on the next studies.

After-fix check: (a) grade a polished response that advances the weaker candidate using realistic but wrong numbers; expect a clearly lower score than (b) the expert reference solution, which should score high.

_fix: env_author · discipline: non_technical · failure mode: grader_guidance_missing_ground_truth · found: 2026-11-19 16:03 UTC_

#### [info] STING-agonist portfolio task: prompt never says what PSLN-344 and PSLN-212 each are ("my asset" is singular, and the asset "includes both the active drug and an appropriate vehicle")

**Category:** prompt

### Problem
The prompt describes a single asset, "a small-molecule STING agonist, which includes both the active drug and an appropriate vehicle". It then says "The assets currently in development are designated PSLN-344 and PSLN-212 in these experiments. Ideally, we take the best asset forward." After that it asks about one asset: "How does my asset look? Would you keep this asset in our portfolio?"

The most natural reading is two candidate drug-plus-vehicle formulations to compare. A second reading fits the first sentence: one designation is the active drug and the other is the vehicle, making up one asset. The prompt never says what each code refers to. The grader has no reference (see the companion finding on missing ground truth), so nothing on the record shows which reading the author intended, and a grader could score two responses differently because they chose different readings.

### Verification method
Static analysis only. Could not verify without container access: the data bundle in `/tmp/world` may make the roles clear (for example, a labelled vehicle-control arm). If it does, this finding does not apply.

### Recommendation
Add one clause to `task_prompt` stating what each code is. For example: "PSLN-344 and PSLN-212 are two candidate drug-plus-vehicle formulations of the same program", or whatever the data actually show.

_fix: env_author · discipline: non_technical · failure mode: prompt_ambiguity · found: 2026-11-19 16:03 UTC_

### Difficulty — 2

#### [warning] Problem too easy: task_f9c4675def384c5e820284adce63119b

Pass rate 94% (over 4 runs) exceeds 90%. This could indicate the problem is too simple to be useful for training, but pass rates depend on the model and sampling config — check whether this is expected.

_discipline: non_technical · found: 2026-11-19 22:16 UTC_

#### [warning] Problem too easy: task_f9c4675def384c5e820284adce63119b

Pass rate 90% (over 4 runs) exceeds 90%. This could indicate the problem is too simple to be useful for training, but pass rates depend on the model and sampling config — check whether this is expected.

_discipline: non_technical · found: 2026-11-19 17:40 UTC_

## QA runs

### Env linter — completed, 2026-11-20 09:03 UTC

_findings: 1 · triggered by: taygeta.alniyat.azmidi@mercor.expert_

Task & domain issues — The grader for this task gets no answer key, trap list or guidance (all null). The environment's own server code says truth files are injected for the grader, but none are. Grading is still accurate today because the grader re-derives every number from the workbook:
- a fabricated-numbers proposal scored 0.20;
- a wrong-asset recommendation scored 0.35;
- proposals missing required sections scored 0.42 and 0.60;
- a generic no-data proposal scored 0.00;
- a correct concise proposal scored 0.80 (stored runs scored 0.87–0.95).

The cost is that each grading must rediscover the seeded data-integrity traps, which takes 211–675 s, and deductions vary with what each session finds. Info only.

### Reward hacking — completed, 2026-11-20 07:49 UTC

_findings: 1 · triggered by: taygeta.alniyat.azmidi@mercor.expert_

Task & domain issues — The agentic grader for this task has no problem-specific guidance, answer key or reference values. Its prompt's problem-specific section is empty, even though the workbook contains several deliberately seeded data defects, and choosing the right asset depends on reading the annotation correctly. In every grading I ran, the grader still recomputed the numbers from the original files and scored sensibly. An empty hand-in, a no-work answer, a grader-injection attempt and a label-swapped copy of a top run all scored 0.0-0.06. Hand-ins that dropped required deliverables scored 0.40-0.64. So no reward hack was found. The missing guidance leaves every verdict dependent on the grader rediscovering the traps in each session, and gradings took 79-938 s. Filed as info.

### Data quality — completed, 2026-11-20 06:40 UTC

_findings: 1 · triggered by: taygeta.alniyat.azmidi@mercor.expert_

Scanned 1 problems with input files. 1 candidate findings; 0 passed gate (→ env_linter).

### ClaudeScope (transcripts health report) — completed, 2026-11-20 06:40 UTC

_findings: 1 · triggered by: taygeta.alniyat.azmidi@mercor.expert_

ClaudeScope analysis completed: 5 clusters identified

### Difficulty — completed, 2026-11-19 22:16 UTC

_findings: 1 · triggered by: taygeta.alniyat.azmidi@mercor.expert_

1 immediate findings

### Difficulty — completed, 2026-11-19 17:40 UTC

_findings: 1 · triggered by: taygeta.alniyat.azmidi@mercor.expert_

1 immediate findings

### Problem linter — completed, 2026-11-19 16:03 UTC

_findings: 2 · triggered by: taygeta.alniyat.azmidi@mercor.expert_

Static review of PV 3619eae7-97fe-4c82-b569-ff1869b7b1a6, an open-ended STING-agonist portfolio recommendation graded by a single-score agentic grader. One error: the record gives the grader no reference solution, rubric, grader guidance or grader files. The environment's description promises expert reference solutions and rubrics, so the main judgement the task exists to test (an objective keep/drop call and which candidate leads) cannot be checked against the author's answer. One info: the prompt never says what PSLN-344 and PSLN-212 each are, and this could not be checked against the data bundle. The prompt is otherwise realistic and free of hints, time-budget prose or capture debris, and the output path is consistent.

