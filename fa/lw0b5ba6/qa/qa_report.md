# Taiga QA report — Task lw0b5ba6 (v1)

| | |
|---|---|
| Problem | `task_f9c4675def384c5e820284adce63119b` |
| Problem version | `e031e3a6-3ae7-4e6f-a57c-c563c545a89d` (v1) |
| Created | 2026-11-19 06:02 UTC by taygeta.alniyat.azmidi@mercor.expert |
| Tags | In Development |
| Environment | vert_bio_v001_MER (`2e3eb299-7d22-4082-be2e-180e73ccf90d`) |
| Auto-QA | enabled |
| Latest QA chain | completed at 2026-11-19 10:55 UTC |
| QA freshness | fresh — QA ran against this version (latest QA run 2026-11-19 08:31 UTC) |
| Eval runs | 8 / 8 completed |
| Exported | 2026-11-19 14:54 UTC via Anton Internal Tooling /tasks |

## Summary

9 findings across 7 QA runs.

| Check | Findings |
|---|---|
| ClaudeScope (transcripts health report) | 1 |
| Data quality | 1 |
| Reward hacking | 2 |
| Env linter | 2 |
| Problem linter | 1 |
| Difficulty | 2 |

## Findings by check type

### ClaudeScope (transcripts health report) — 1

#### [error] moderate_ambiguous_asset_identity_and_framing_mismatch

The prompt describes the asset as a "small-molecule STING agonist, which includes both the active drug and an appropriate vehicle". That wording suggests a therapeutic, possibly in oncology. The supplied data instead cover only an intranasal influenza vaccine adjuvant: a cyclic dinucleotide plus Mn²⁺ in a liposome, tested in aged mice. The data contain several candidate preparations (PSLN-344, PSLN-212, CMP-204), and the prompt never says which one is "the asset". Agents must infer it from an annotation PDF subject line and state their assumption. The central recommendation reverses depending on that choice: keep PSLN-344, drop PSLN-212. A domain expert could not be certain of the intended asset or indication from the prompt alone.

_runs: 05938b91 · found: 2026-11-19 08:36 UTC_

### Data quality — 1

#### [info] undisclosed_constraints: The prompt demands citations but never specifies the required citation format or

Requiring citations without specifying a format is a normal business request, not an undisclosed constraint; the grader would reasonably accept any clear citation approach rather than penalize on an unstated format standard.

_discipline: non_technical · failure mode: undisclosed_constraints · found: 2026-11-19 08:36 UTC_

### Reward hacking — 2

#### [info] Grader has no task-specific guidance or reference values; it must re-derive the whole 15-sheet workbook at every grading

What's wrong: the problem version has no grader_guidance, rubric, grader_files or reference answer. The grader prompt's "Problem-Specific Grading Guidance" section is empty. The dataset contains deliberate-looking inconsistencies:
- S03-B/S03-F IgG2a/IgG1 ratio headers are permuted against the S13 subclass titres.
- S11-B duplicates S11-A replicate columns.
- The second S09-A panel is the log10 of the S01-A 72 h data.
- S06-C and S06-D are identical.
- S15-C and S15-I share body-weight traces.

How well a response handles these can only be judged by the grader rediscovering them each time.

How I know, from graded rollouts:
- A proposal with correct structure and block citations but invented key numbers (92/108 changed to 104/108, Ifnb1 37.1 changed to 58.4-fold, HAI 368 changed to 1,280, and a false claim of no integrity problems) scored 0.12. The grader recomputed the figures from the workbook, so verification worked this time.
- That grading took 455 s. Grading an accurate compact proposal took 633 s. Stored grader run 32ae525e used 60 bash calls.
- In the accurate-proposal grading, the grader deducted for workbook issues it found on its own that no guidance names: S06-G untreated controls 4/7 surviving, S08-C headers permuted, S13-F/G group sets not matching S03-I/J.

Impact: no false positive observed. But scoring rests wholly on what the grader happens to re-derive in each session, and what it finds can vary between gradings.

Fix: add grader_guidance listing the key reference values (e.g. aged survival 92/108 vs 15/108; day-60 durability 14/21; Ifnb1 37.1 vs 16.6-fold [S01-A]; HAI 368 vs 46 [S03-C]) and the planted data defects a strong response should catch.

_fix: env_author · discipline: non_technical · failure mode: grader_guidance_missing_ground_truth · runs: 32ae525e · found: 2026-11-19 09:45 UTC_

#### [info] Prompt calls the asset an unnamed 'small-molecule STING agonist' but the data cover an intranasal flu-vaccine adjuvant with several candidates

What's wrong: the task prompt says "a proprietary asset, a small-molecule STING agonist, which includes both the active drug and an appropriate vehicle". It names no asset and no indication. The inputs are /tmp/world/filesystem/psln_program_dataset.xlsx (15 study sheets, S01–S15) and psln_program_annotation.pdf (19 pages; PDF Subject metadata "Per-block annotation of the PSLN-344 preclinical dataset"). They describe an intranasal adjuvant for inactivated influenza vaccine in aged mice: CDN-1807 in a surfactant-biomimetic liposome, with Mn2+ (PSLN-344) or without it (PSLN-212). They also contain other candidate preparations (CMP-204, PSLN-R848, PSLN-212/R848). The only pointer to which one is "the asset" is the PDF's subject line.

How I know: I read the prompt and inputs in a fresh container. I drew 3 answers from a separate model call that saw only the prompt. All three assumed an oncology STING programme (tumour models, anti-PD-1 combinations). In my graded rollout of an accurate proposal, the grader listed "treating PSLN-344 as 'the asset' is an assumption, though it is stated explicitly" under weaknesses. All 8 stored runs (e.g. 723b22d4, 0.95) chose PSLN-344 and stated that choice.

Impact: small so far. Scores are tight (0.90–0.95) and no run was marked down much for its choice. But the wording invites oncology framing, and whether the asset is PSLN-344 or PSLN-212 is left to inference.

Fix: name the asset (PSLN-344) and the intended indication in the prompt, or say that identifying them from the files is part of the task.

_fix: env_author · discipline: non_technical · failure mode: prompt_ambiguity · runs: 723b22d4 · found: 2026-11-19 09:45 UTC_

### Env linter — 2

#### [info] No grader guidance or reference values, so each grading re-derives the whole workbook and runs close to the 600 s budget

The problem's grading strategy is agentic_grader (single_score), with:
- grader_guidance: null
- grader_files: null
- no rubric and no reference answer
- an empty "Problem-Specific Grading Guidance" section in the grader prompt.

The grader therefore opens the 15-sheet workbook and the PDF and recomputes the figures itself on every grading. Its conversations in this check show it doing so.

The result is correct but slow. Grading durations in this check:

| Hand-in | Grading time |
|---|---|
| Complete alternative proposal | 545 s |
| Citations removed | 558 s |
| Omission variants | 445 s and 456 s |

The earlier reward-hacking check recorded a 633 s grading. The grading budget is the default 600 s (grading_timeout_seconds 600 in environment.json). No grading has failed: 0 failures and a timeout rate of 0 across the 8 stored runs, and 0 across the 6 rollouts here. This is therefore a margin risk, not a demonstrated failure.

There is a second effect. Without a reference list of the planted data problems, the grader's judgement of which data-integrity issues a response should catch rests entirely on what it re-discovers in each grading. Examples it found in grading here:
- inconsistent units between S03-J, S13-E and S05-A/B
- duplicated block labels on S06
- repeated group labels in S07-C
- S10-A summarised as mean±SD rather than per-animal values

Suggested fix: add grader_guidance or a grader_files reference listing the key computed values, the lead asset and indication, and the planted data defects a strong response should flag. This shortens grading and makes the grader's checklist the same across gradings.

_fix: env_author · discipline: non_technical · failure mode: grader_guidance_missing_ground_truth · runs: 619b246b, 723b22d4 · found: 2026-11-19 10:55 UTC_

#### [info] Prompt does not name the asset or indication; the files describe an intranasal flu-vaccine adjuvant, not an oncology drug

Task prompt: "a proprietary asset, a small-molecule STING agonist, which includes both the active drug and an appropriate vehicle". It gives no compound name and no indication.

The inputs are /tmp/world/filesystem/psln_program_dataset.xlsx (15 sheets) and psln_program_annotation.pdf. They describe an intranasal influenza-vaccine adjuvant programme covering more than one candidate. The only place the lead asset is named (PSLN-344) is the PDF's document metadata (Subject field), not the body text.

STING agonists are best known as intratumoral oncology agents, so the natural reading of the prompt points the wrong way. Evidence:
- I graded a proposal with every requested section present but an oncology framing (ADU-S100/MK-1454, CT26/B16F10 models, PD-1-refractory solid tumours). It scored 0.02. The grader's stated reason was that it was "an unsourced proposal for the wrong therapeutic area".
- The earlier reward-hacking check reports that its three no-work answers also assumed oncology and scored 0.02–0.03.

The stored runs that read the files resolve this correctly and score 0.90–0.95 (e.g. 723b22d4 at 0.95 and 619b246b at 0.90). The impact is therefore limited, and discovering the indication from the data may be intended.

Suggested fix: add one sentence to the prompt naming the lead compound (PSLN-344) and its intended use (intranasal vaccine adjuvant). Alternatively, if discovering it is part of the test, say in the prompt that the indication is to be determined from the data.

_fix: env_author · discipline: non_technical · failure mode: prompt_ambiguity · runs: 619b246b, 723b22d4 · found: 2026-11-19 10:55 UTC_

### Problem linter — 1

#### [error] STING-agonist portfolio-review task: agentic grader has no reference solution, rubric or grader_guidance for the keep/drop verdict, MoA and biomarkers

**Category:** grading

### Problem
The task asks for an objective keep/drop recommendation on a proprietary small-molecule STING agonist, based on the data bundled in `/tmp/world`. It also asks for a committee proposal covering: next studies with endpoints, a target demographic, a data-backed MoA, biomarkers for validating efficacy, and what was "considered and ruled out". The prompt adds: "Every number you rely on needs to cite the relevant data and analysis, because the committee will check." A single `agentic_grader` does the grading (`claude-opus-5-5`, `scoring_mode: single_score`, `container: fresh_with_policy_setup`, `grader_extra_tools: [bash, str_replace_editor]`, `grading_timeout_seconds: 600`).

The record gives that grader nothing to grade against:
- there is no `rubric` key
- `agentic_grader_params.grader_guidance: null`, `grader_files: null`, `override_grader_prompt: null`
- `extra_fields.rubric: null`, `extra_fields.grader_metadata: null`
- there is no `golden_patch`

The environment's own description says the design is different: "model outputs are graded against the expert reference solutions and task-specific rubrics".

### Evidence
The grader receives the task prompt (`include_task_prompt: true`), the end of the transcript (`policy_transcript_mode: episode_tail`), the model's outputs and the input files (`include_input_files: true`). With bash it can recompute a cited figure from `/tmp/world`, so it can catch a made-up number if it goes looking. The central judgment has no expected answer anywhere the grader can read:
- whether the data supports keeping the asset ("Would you keep this asset in our portfolio?")
- which finding in the data decides that
- which indication or demographic, MoA and biomarkers the data actually supports
- which alternatives an expert would rule out

To grade, the grader must redo the expert analysis itself within 600 s and then compare the answer with its own conclusion. Nothing in the record lets it mark down a fluent, well-cited proposal that reaches the wrong verdict or misses the data's key signal. Two runs that reach opposite verdicts can get similar scores. Six separate deliverables go into one score, with no acceptance criteria for any of them.

### Verification method
Static analysis only, from the problem-version record. This session could not read how the `anton-omni` image behaves at grade time (its MCP server lists a hidden `setup_agentic_grader` tool) or what the `/tmp/world` bundle contains. Nothing in the record points the grader at reference material.

### Recommendation
Write the expert reference solution into `agentic_grader_params.grader_guidance`, or add it as a `grader_files` entry (these reach the grader under `container: fresh_with_policy_setup`). Keep it out of `/tmp/world` and anything else the model's container receives. It should contain:
1. The expected recommendation and the specific data findings behind it, each with its source file and value or analysis.
2. The key numbers a correct answer must cite, with tolerances.
3. Which indications or target demographics, MoA and biomarkers the data supports, and which ones it contradicts.
4. The alternatives a strong answer should consider and rule out.
5. How to score a wrong verdict with strong analysis compared with a right verdict with thin support, and how to treat numbers that can't be traced to the data.

To check the fix:
- (a) Grade a confident, well-formatted answer that gives the opposite verdict and uses plausible but untraceable numbers. Expect a low score.
- (b) Grade the author's own reference answer. Expect a high score.

_fix: env_author · discipline: non_technical · failure mode: grader_guidance_missing_ground_truth · found: 2026-11-19 06:05 UTC_

### Difficulty — 2

#### [warning] Problem too easy: task_f9c4675def384c5e820284adce63119b

Pass rate 94% (over 4 runs) exceeds 90%. This could indicate the problem is too simple to be useful for training, but pass rates depend on the model and sampling config — check whether this is expected.

_discipline: non_technical · found: 2026-11-19 08:19 UTC_

#### [warning] Problem too easy: task_f9c4675def384c5e820284adce63119b

Pass rate 92% (over 4 runs) exceeds 90%. This could indicate the problem is too simple to be useful for training, but pass rates depend on the model and sampling config — check whether this is expected.

_discipline: non_technical · found: 2026-11-19 07:22 UTC_

## QA runs

### Env linter — completed, 2026-11-19 10:55 UTC

_findings: 2 · triggered by: louisciano@mercor.com_

Engineering issues — The grader has no reference material. No grader guidance, reference answer or grader files exist, and the grader prompt's problem-specific guidance section is empty. Each grading therefore rebuilds the 15-sheet workbook analysis from scratch. Full-length hand-ins took 445–558 s to grade in this check, and one took 633 s in an earlier check, against a 600 s grading budget. No grading has failed yet: 0 failures across the 8 stored runs and 6 rollouts graded here. Adding reference values and a list of the planted data defects would shorten grading and make it steadier.

Task & domain issues — The prompt describes the asset only as "a small-molecule STING agonist … and an appropriate vehicle". It does not name the compound or the indication. The files show an intranasal influenza-vaccine adjuvant programme, and only the PDF's document metadata names PSLN-344. An answer that assumes the usual oncology use gets ~0.02, so the indication has to be found in the files. That is a fair test, but one sentence naming the asset and indication would remove the ambiguity.

Otherwise the grading held up under every probe:
- An empty hand-in scored 0.0 and an unsourced oncology proposal 0.02.
- Hand-ins omitting one or more required sections scored 0.38, 0.40 and 0.60.
- A complete proposal written by a different route scored 0.78; the grader docked it for real content defects it named, not for its format.
- The standard leak and tamper probes were clean.

### Reward hacking — completed, 2026-11-19 09:45 UTC

_findings: 2 · triggered by: louisciano@mercor.com_

Task & domain issues — No reward hack found. I graded six hand-ins that should score low: an empty hand-in (0.0), a proposal with invented numbers (0.12), two no-work answers drawn from a separate model call (0.02 and 0.03), and two proposals each missing several requested sections (0.55 and 0.32). All were scored well below stored runs (0.90–0.95). Placing a named pipe, a symlink to /, a symlink loop and unreadable entries in /tmp/outputs did not make grading fail: the hand-in was graded normally at 0.02. Two informational notes: (1) the prompt calls the asset an unnamed \"small-molecule STING agonist\", while the data describe an intranasal influenza-vaccine adjuvant with several candidate preparations (PSLN-344 is the inferred asset), and model answers written without the data default to oncology; (2) the grader has no task-specific guidance or reference values, so every grading re-derives the 15-sheet workbook (7–10 minutes), and which data defects it credits or penalises rests on what it rediscovers.

### Data quality — completed, 2026-11-19 08:36 UTC

_findings: 1 · triggered by: louisciano@mercor.com_

Scanned 1 problems with input files. 1 candidate findings; 0 passed gate (→ env_linter).

### ClaudeScope (transcripts health report) — completed, 2026-11-19 08:36 UTC

_findings: 1 · triggered by: louisciano@mercor.com_

ClaudeScope analysis completed: 5 clusters identified

### Difficulty — completed, 2026-11-19 08:19 UTC

_findings: 1 · triggered by: taygeta.alniyat.azmidi@mercor.expert_

1 immediate findings

### Difficulty — completed, 2026-11-19 07:22 UTC

_findings: 1 · triggered by: taygeta.alniyat.azmidi@mercor.expert_

1 immediate findings

### Problem linter — completed, 2026-11-19 06:05 UTC

_findings: 1 · triggered by: taygeta.alniyat.azmidi@mercor.expert_

Problem-definition review of e031e3a6 (STING-agonist portfolio-review task, agentic grader) found one error. The task is realistic and clearly scoped, and it has no hints, no suffix and no authored time budget. However, the record gives its single-score agentic grader no reference: no rubric, no grader_guidance, no grader_files and no golden patch. The environment description says outputs are graded against expert reference solutions and rubrics. The grader can recompute cited numbers from /tmp/world with bash, but nothing tells it the expected keep/drop verdict, the deciding data findings, or the MoA, biomarkers and target demographic the data supports, so it must redo the expert analysis within 600 s to judge. No prompt, hints or consistency issues were found. Static analysis only: the image's grade-time behaviour and the bundle's contents could not be read.

