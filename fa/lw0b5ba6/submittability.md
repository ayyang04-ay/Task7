# lw0b5ba6 — submittability verdict

Task `task_f9c4675def384c5e820284adce63119b`, problem version `3619eae7` (versionNumber 2).
Panel: Opus job `70ccbec0`, Fable job `8de89bb3`, both 2026-11-19. Exports read from
`ayyang04-ay/fa-data@b924f84`.

Migrated from `psql25c1` (`task_4ce55343502b4d17b2182158ad6e4533`). Writer confirms the
ID change is the migration and the task is essentially the same. Two things did change and
both matter below: the prompt gained a sentence, and **the grading document did not come
across**.

**Mode: trajectory-only.** The problem version carries `grader_guidance: null`,
`grader_files: null`, no rubric and no reference answer. The 8 runs were scored by a
default agentic grader with an empty problem-specific section. Scores are uninformative
and are not used to rank runs or choose reading order. The prior ledger's A/B item mapping
(A5, B4) does not apply to this panel.

---

## 1. Verdict

**Submittable after golden edits, with one QA Error to action on the task record first.**
Nothing requires a prompt or data room edit and nothing requires a rerun.

## 2. Checks

| Check | Result | Reason |
|---|---|---|
| QA fixability | **your call** | One `error`: the problem version gives the grader no reference answer, rubric or guidance. Fix is to attach the documents that already exist in the repo; it is a record fix, not a prompt or room edit. Blocks submission until actioned or rebutted, does not block the FA |
| Golden derivability | pass, edit needed | The prompt now asks which of the two assets leads. The golden states a single-asset advance. The selection answer is derivable from the room; see §4 |
| At least one candidate | pass | Mode 1 clears every mechanical bar in all 8 runs, with the controlling value read in all 8. Defensibility is the writer's call; both sides in §3 |

## 3. Candidate modes

| # | Mode | Class | Runs | What happened | Why it is a mistake | Where visible | Status |
|---|---|---|---|---|---|---|---|
| 1 | Age claim measured against a differently formulated young arm (16 h site) | Analytical | O1 O2 O3 O4 F1 F2 F3 F4 | Each run built a restoration, age-gap-closed or "% of young" figure whose denominator is young animals on the **Mn-free** asset, and reported that the Mn asset returns the aged response to the young level — 0.98, 98%, 100%, "fully restored" | The same block carries young animals on the **Mn** asset. Holding the formulation constant the aged response is 0.732 of young, not 0.98. Prompt: "objective and defensible", "grounded in our data"; every run built the MoA section the claim sits in | O1 `:48` `:212` `:264` `:713`; O2 `:14` `:84` `:104` `:400` `:473`; O3 `:66` `:372`; O4 `:244` `:275` `:507`; F1 `:99` `:194` `:225`; F2 `:178` `:404` `:646`; F3 `:161` `:1715`; F4 `:89` `:105` | confirmed present |
| 2 | Same denominator on the 72 h panel, where it inflates the asset's risk | Analytical | O1 O3 O4 | The reactogenicity read — the one finding that argues against the asset — is also taken against the young Mn-free arm: Tnf "8.4x vs young 0.5x", "2.9x the young level", "overshoot" | Against the age-matched Mn-free arm the same panel gives Tnf x1.62 (p=0.052) and Il10 x1.00 (p=0.991); the aged Mn-free arm shows the same tail at 5.2 and 4.2. Only Il6 separates (x3.85, p=0.026) | O1 `:92` `:267`; O3 `:107`; O4 `:226` | confirmed present |
| 3 | O1 states both readings of the 72 h panel and ships the confounded one | Reasoning (self-contradiction) | O1 | O1's appendix carries the age-matched contrast with its interval, Tnf x1.62 (0.99-2.62) p=0.052. The body states the young-denominator version as the reactogenicity flag | Same run, two standards, the weaker one in the recommendation | O1 `:774` against `:92` and `:267` | held — single run, below the floor of 2 |
| 4 | Matched-subtype blocks pooled into a cross-subtype claim | Synthesis | — | Watch-list item carried from the prior ledger. No Fable run uses cross-subtype vocabulary at all; the Opus runs that do name the blocks individually | — | — | not observed |
| 5 | Proposing an arm the room already settles (adjuvant alone / antigen free) | Synthesis | — | Pre-registered before the prior panel and absent again. All 8 cite `S15-H` | — | — | not observed |
| 6 | Over-applying a duplication finding to the whole 72 h panel | Retrieval | — | Watch-list item from the prior ledger's single-run finding. Not seen; all 8 cite `S06-D` and all 8 use the 72 h panel | — | — | not observed |

### Mode 1 — what changed since the prior panel

Stronger, not weaker. In the retired 16-run panel 3 runs held the controlling value. Here
**all 8 read the young+Mn arm's per-animal values** (60.02, 52.51, 46.93, 54.02, 40.04 —
`S01!B10:F10`), and 6 of 8 computed or printed the young-cohort contrast and then did not
use it:

| Run | What it had | Where |
|---|---|---|
| O1 | "37.5 -> 50.2, +34%, p=0.009" in its own deliverable, RI 0.98 unchanged | `:288` |
| O3 | ran a block headed "Young: does Mn add anything?" giving GM 37.5 -> 50.2 (1.34x), Welch p=0.0092; deliverable never prints 50.2 and reports "Restored 100%" | transcript blk136; `:66` |
| O4 | noted "50.7 vs 37.6" in reasoning; deliverable defines the index on the young Mn-free arm | transcript blk75; `:507` |
| F1 | tool output printed "young: PSLN-212(Y) 37.6, PSLN-344(Y) 50.7" three times | transcript blk88 |
| F2 | holds 50.7 with its cell range as ledger entry E099 and computes 1.3x, p=0.009; benchmarks 39 readouts on the young Mn-free arm | `:484` `:178` `:404` |
| F3 | holds 50.2 with its cell range as row 120 and prints 37.5 / 50.2 side by side | `:1365` `:179` |
| F4 | its own stats table carries columns Y212 = 37.5 and Y344 = 50.2 **and** a computed 344vY = 0.98; ships only the 0.98 | transcript blk90; `:89` |

Two runs reason about the benchmark's status and still use it. F3 lists, among things it
rules out, "Pooling the young benchmark with aged animals as if it were an age-matched
control. It is a benchmark for what a full response looks like, nothing more" (`:721`).
F2 lists "Restores the aged response to young" under claims it does not think the data
support, on the ground that CD40/CD86 reach only 29% and 38% (`:342`) — contesting the
conclusion without correcting the comparison.

### Defensibility, both sides — the writer's call

**For defensible.** A restoration index against young animals on the current regimen is a
conventional construction: it asks how much of the age deficit the new agent closes
relative to what young people get today. Six runs state the denominator explicitly in a
methods line, so nothing is hidden. Several also report the young-cohort effect elsewhere,
so the package as a whole contains both readings.

**Against defensible.** The claim actually made is about age — "returns the aged response
to the young level", "fully restored", "restored 100%" — and that claim requires the
formulation held constant. The controlling arm is in the same block, all 8 read its raw
values, and 6 computed the contrast. It is the stated mechanism step and the stated
biomarker qualification in all 8, both prompt-mandated deliverables: mechanism at O2 `:171`,
O4 `:244`, F2 `:250`, F1 `:194`; biomarker rationale at O1 `:264`, O4 `:275`, F2 `:267`.
O4 `:286` also uses the restoration indices to rank biomarker candidates against the
survival index of 0.80 and rejects CD40/CD86 and GZMB on that basis.

**What it does not reach — correction, 2026-11-21.** An earlier version of this section said
the confounded figure was carried into a proposed human PD go criterion in O1, O2 and O4.
**Withdrawn.** It reaches no go/no-go, gate, stop rule, acceptance criterion, verdict or
asset selection in this panel. O2's gate at `:266` uses "Ifnb1 ratio >= 2", the within-aged
ratio of 2.23, which is the correct contrast; O4 `:275` is a ranking row, not a gate; O1 has
no such criterion. The criterion cited ("older-donor R >= 0.5") belongs to the **retired**
panel's O1 at `:370` and was carried across — the error the superseded banners exist to
prevent. The pillar the mode does corrupt is component 5 of the golden's components list,
the age claim stated correctly, which is what justifies the 65-plus indication.

### Exemplars

At the 16 h site, none — all 8 carry it. At the 72 h site there are clean ones, which is
the strongest evidence the room does not force the error: **F4** `:125` states "PSLN-212
also resolved slowly in aged lung (Tnf 5.2-fold at 72 hours)", holding age constant;
**F3** `:171` `:187` reports the aged Mn-free column alongside ("Tnf 8.4 versus 5.2-fold,
Il6 7.2 versus 1.9-fold"); **F2** `:190` reports both columns.

## 4. Golden edits required

**Corrected 2026-11-21.** The first version of this section listed one golden edit. There
are three. Edits 2 and 3 are pre-existing gaps against prompt asks the repo's own
`task/prompt.txt` already carried, not consequences of the migration.

| # | Location | Change | Why |
|---|---|---|---|
| 1 | `task/golden-response.md:14`, `## Recommendation` | State the selection: PSLN-344 leads, PSLN-212 stops as a development candidate and continues as the Mn-free comparator | The prompt says "The assets currently in development are designated PSLN-344 and PSLN-212 in these experiments. Ideally, we take the best asset forward." The golden says only "Advance it." and treats PSLN-212 purely as a mechanistic comparator. A sentence, not new analysis: the evidence is in the same section (PSLN-212 fails to separate from vaccine alone in three of the six, p = 0.088, 0.111, 0.066). All 8 runs answered it explicitly |
| 2 | `task/golden-response.md`, new section | Add the target demographic: primary segment, sub-segments, exclusions, and the inputs market research must supply | The prompt asks for "a target demographic so that our market research team can check the TAM". The golden has no such section — only incidental "65-plus" at `:56` and `:346`. The segment is derivable from the room; sizing inputs are external and go in marked `[external]`, the convention already used at `:346` |
| 3 | `task/golden-response.md`, new section | Add what dropping gives up, and why | The prompt asks "If I drop this I have to be able to tell the committee exactly what we are giving up and why". Absent: no match for "giving up", "give up", "if we drop" or "forgo". Derivable with no new analysis; it is the protection case restated as a loss |
| — | `task/prompt.txt` | Replace with the shipped text, `006aa3ff6c6b`, 252 words | Not a golden edit. The repo carries `bf4e427cdf08`, 231 words; the deployed prompt is one revision ahead |
| — | `build/anton-brief-psql25c1.md:293` and `HANDOFF.md` §1 | Delete the stale "S10-A block holding S03-E content" entry, regenerate | Not a golden edit. Carried over from the prior QA triage, confirmed stale, not yet actioned |

**No golden edit is needed for either confirmed mode**, verified against the golden text
this session. `:48`–`:69` give young+Mn at 50.70 with p = 0.012 against aged+Mn and
p = 0.014 against young+Mn-free, the within-cohort increments (1.65 to 24.35-fold aged
against 1.02 to 1.35-fold young), and the statement that this "is the only comparison here
that holds age and formulation apart". Study 3 covers the 72 h site including the reversal
(formulation x1.97 p = 0.0126 in young against x1.29 p = 0.2619 in aged). So the FA's
counterfactual for both modes is already grounded in the golden.

**`audit-golden.py` cannot catch edits 2 and 3.** It checks figures and correspondence —
253 checks, `CORRESPONDENCE` 120/120, golden still hashing to `4a91dfde8b74` as HANDOFF
records — and carries no section-coverage assertion, so it passes clean with two
prompt-mandated deliverables absent. Closing that needs an assertion over required
headings, not more figure checks.

## 5. Held QA items

| Finding | Severity | Held because |
|---|---|---|
| Grader has no answer key or trap list, though the environment's server code says truth files are injected | info | Same root cause as the Error in §2. Env linter's own probes show the grader still recomputes from the workbook |
| Agentic grader has no problem-specific guidance; correctness rests on it re-deriving every number | info | Same root cause. Reward-hacking probes found no hack: empty hand-in, no-work answer, grader-injection attempt and a label-swapped copy all scored 0.0–0.06 |
| No disclosed rubric, so unclear what checks apply | info | The finding's own body resolves it: the prompt specifies the deliverables |
| Grading rationale truncated or missing for one run | warning | Affects O2 (`e8634c7e`). Not an FA input in trajectory-only mode |
| "Problem too easy": pass rate 90% and 94% over 4 runs | warning x2 | Score-based. Under current guidance there is no score to clear and the operative gate is a modal failure, which is met |
| Prompt never says what PSLN-344 and PSLN-212 each are | info | **Rebuttable with evidence.** The finding states it could not be checked against the bundle. The annotation does define them, and all 8 runs identified PSLN-344 as the Mn-containing formulation and PSLN-212 as Mn-free: O1 `:9`, O3 `:9`, F2 `:243` |

Reported without explanation, per the parse manifest: the ClaudeScope job records
`findingCount: 5` against one exported item, so four clusters are not in the export. No
explanation is available from the files. The same gap appeared in the prior panel.

## 6. Deferred

- Attach `task/grader-guidelines.txt` and the golden to problem version `3619eae7`, then
  re-evaluate. Needed before submission; not needed for the FA.
- Widen the grader's restoration-metric penalty from metrics to any aged-versus-young
  figure in a block carrying a young+Mn arm. On this panel the grader scored 0.98 as
  correct, which it arithmetically is, so the item as written does not reach Mode 1.
- Reconcile the `fa/psql25c1/` headers to the new task ID, or supersede them with this
  directory.

---

## Parse manifest

| Row | State | Detail |
|---|---|---|
| Run export located | PASS | `fa-data@b924f84`; sha256 prefixes `47d7c4c1` (Opus), `9af69dd2` (Fable), `10a70b6b` (QA) |
| Export complete | PASS | Both `job_info.json` carry `export_selection` included `outputs`, `transcripts`, `grading`; excluded `task_files`, `grader_files`. One job per model, not complementary halves |
| Clusters present | PASS | No `_ERROR.txt`. `task_files` excluded by selection, not by failure |
| Run map | PASS | Below |
| Run count and status | PASS | 8 runs, 4 per model, all `completed`, 0 refused, no T&S block |
| QA report | PASS | Fresh. Latest chain completed 2026-11-20 09:03 UTC; runs completed 2026-11-19 17:40 and 22:15 UTC, so every QA job started after the panel finished. 8 items across 7 jobs: 1 error, 3 warnings, 4 info |
| Golden | PASS, edit needed | `task/golden-response.md` in the repo; answers the prior prompt. See §4 |
| Data room | PASS | Not in the export. Verified against `data-room/psln_program_dataset.xlsx` by recomputation: `S01!B3:F10` gives 16.64 / 37.11 / 37.60 / 50.70, matching the runs' own values. The bundle snapshot changed (`snap_823264f5…v2` to `snap_52076e09…v3`), consistent with a re-upload of the same files |
| Grading document | **FAIL, waived** | None attached to the version. Drives trajectory-only mode |
| Stats availability | FAIL, waived | No scipy in this container. Nothing above needs a test beyond counts, ratios and recomputed means; p-values quoted are the runs' own or the prior ledger's hand-computed figures |
| Thinking channel | PASS, limiting | All 8 `thinking_summary_status: ready`, so blocks are summaries. **No claim about what a run weighed internally is supportable**, which rules out the raised-then-abandoned shape. Encountered-then-unapplied and established-then-unwritten remain available from tool calls and deliverables |
| Deliverable present | PASS | `outputs/` in both exports, 36 to 81 files per run, primary proposal 40 to 217 KB |

### Run map

| Label | Model | Attempt | Short hash | Run UUID |
|---|---|---|---|---|
| Opus O1 | claude-opus-5-5 | 1 | `f295b831` | f295b831-668f-4e1b-984f-3888910db113 |
| Opus O2 | claude-opus-5-5 | 2 | `e8634c7e` | e8634c7e-5f50-4b4f-bd8c-f53e7b630120 |
| Opus O3 | claude-opus-5-5 | 3 | `978e3829` | 978e3829-863d-4c89-b175-553d29d32858 |
| Opus O4 | claude-opus-5-5 | 4 | `e7837212` | e7837212-0398-4997-a07b-e82ee253b47e |
| Fable F1 | claude-fable-5-2 | 1 | `1e154279` | 1e154279-96d3-4a5d-a970-bcb6857d4e8c |
| Fable F2 | claude-fable-5-2 | 2 | `355880fe` | 355880fe-b171-4da8-8f84-388d6d60b21e |
| Fable F3 | claude-fable-5-2 | 3 | `f644c65d` | f644c65d-aa74-45f2-9b62-35144f1a254d |
| Fable F4 | claude-fable-5-2 | 4 | `c54ffab8` | c54ffab8-8cc5-4b3e-b115-1ffe622d9ddd |

### Verdict map

| Run | Keep or drop | Which asset leads | PSLN-212 | Gated? |
|---|---|---|---|---|
| O1 | keep | PSLN-344 | stop, retain as Mn-free control | yes, Gates A and B |
| O2 | keep | PSLN-344 | stop now | yes, tranches |
| O3 | keep | PSLN-344 | stop, retain as comparator and fallback | yes, two gates |
| O4 | keep | PSLN-344 | discontinue as candidate | yes, three gates |
| F1 | keep | PSLN-344 | stop as lead, Mn-free reference arm | yes, next gate only |
| F2 | keep | PSLN-344 | stop, Mn-free comparator | yes, Gate 1 |
| F3 | keep | PSLN-344 | stop active development, comparator | yes, three conditions |
| F4 | keep | PSLN-344 | stop for the population, comparator | yes |

**Unanimous on every decision the prompt asks for.** The advance/decline split that the
prior panel showed, which traced to whether the integrity findings gate the recommendation,
has collapsed: all 8 now gate. So the verdict map yields no divergence-point candidate and
the method-based screen carries the FA, as it did before. A unanimous verdict can still
hide a shared mode, and Mode 1 is that mode.

### Reading coverage

| What | Which runs |
|---|---|
| Primary deliverable read in the sections bearing on each candidate | all 8 |
| Searched for Mode 1 and Mode 2, two or more patterns of differing looseness, numeric probes in two or more spellings | all 8 |
| Transcript element census | all 8 |
| Raw-cell probe for the controlling arm | all 8 |
| Grader rationale read | none — trajectory-only mode; no mode rests on one |

Numeric probes were run in both spellings: `37.5`/`37.6`/`37.60`, `50.7`/`50.70`/`50.2`,
`0.98`/`0.987`/`99%`, plus the raw per-animal values `60.02`/`52.51`/`46.93`/`54.02`/`40.04`.
The raw-value probe is what established that all 8 read the arm; the summary-value probes
alone would have put 4 runs in "not retrieved".

### Epistemic labels

[computed] `S01-A` arm means and all ratios in §3 and §4, recomputed from
`data-room/psln_program_dataset.xlsx` this session. [transcript] every position cited above,
read in the run's own deliverable or transcript. [inference] that the confounded figure is
load-bearing where it enters a proposed human go criterion — stated by O1, O2 and O4
themselves, not inferred.


---

## Addendum, 2026-11-21 — a third candidate, built and failed

The golden states the package "will not support the claim that the asset does nothing in
young animals". Six runs make a version of that claim. F2 `:166` makes the unscoped
version, "In young animals manganese adds nothing", in the same bullet that lists
interferon-beta 50.7-fold against 37.6-fold, and F2 `:300` then excludes adults under 50
and children from the TAM on it, which would make it load-bearing on the demographic
deliverable.

**Failed on defensibility, on the run's own statistic.** F2 `:178` reports that contrast as
"1.3x; p = 0.009 Welch, 0.63 after Tukey". On its own multiplicity-corrected figure the
difference is not significant, so "adds nothing" is defensible. The golden uses uncorrected
Welch (p = 0.014 for young+Mn against young+Mn-free); both methods are defensible. Every
other instance is scoped to survival, where young animals sit at a ceiling of 24/24 against
24/24: F3 `:655` `:698`, O1 `:492`, O2 `:16`, F4 `:112`. F3 `:278` states the careful form.

Held with its evidence rather than dropped, so it is not re-raised as new.

## Addendum — calibration note, not FA material

No mode in this panel bears on the verdict. The verdict is over-determined: the survival
effect is +71 points, it comes from the S06 series, and that path carries no trap, so a run
can state the age claim wrongly and still land the recommendation. All 8 did. The retired
panel recorded the same thing. If a verdict-bearing mode is required, this task does not
have one and more screening will not find it.
