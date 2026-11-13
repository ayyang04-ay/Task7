# psql25c1 — QA triage, export `qa_report_psql25c1_v2_f3a468ce`

Freshness: **fresh**. QA ran against problem version `f3a468ce`, the version both panel
jobs ran. Latest chain completed 2026-11-13 08:17 UTC; the two run jobs completed
2026-11-12 22:00 and 23:40 UTC, so **every QA job started after the panel finished** and
the ClaudeScope pass could see all sixteen runs. Nothing is STALE and nothing is held out.

Nine findings across seven jobs. Run UUIDs translated to panel labels throughout.

| # | Finding | Check | Runs | Type | Affects golden? | Action | Evidence |
|---|---|---|---|---|---|---|---|
| 1 | "Ground truth" framing against the seeded contradictions; 15–23 integrity findings per run exceed a real package | ClaudeScope, **error** | O4, O8, O7, O6, O5, O2 | Ambiguity / undisclosed constraint | No | **Writer's call, laid out below. Do not default to a rerun.** | QA text; the panel's own verdict split traces to this exact step |
| 2 | Fragmented conda envs: no openpyxl-plus-lifelines in any one env; no `file`, no `unzip`; `pip` missing in one run | ClaudeScope, warning | O4 | Tooling | No | Ignore. Task note in `error_modes.md` Phase 1f | QA text |
| 3 | Grader reasoning missing from stored metadata | ClaudeScope, warning | O2 | Technical | No | **Ignore, and record that the finding does not hold.** The grading record for O2 carries 5,038 characters of reasoning | Read directly from `grading/attempt_02_fe37920b.json` |
| 4 | No document renderer in the image: no LibreOffice, LaTeX, poppler, ghostscript, PyMuPDF or headless browser; `pdf2image` fails | ClaudeScope, warning | O3, O1, O5 | Tooling | No | Ignore. Task note. Every run shipped a PDF or DOCX it could not visually check | QA text |
| 5 | "The grader requires the recommendation be grounded specifically in heterosubtypic…" filed as an undisclosed constraint | Data quality, info | — | Self-resolving | No | No action. The finding's own body says grounding the call in challenge data is a standard inference the solver derives, not an undisclosed constraint | QA text |
| 6 | "Ground truth" wording against a grader that credits departing from the record; two graders acted on the ambiguity in opposite directions — O4's audit-led "no" was docked for not treating the data as ground truth, O1's audit-led "no/gated" was credited in full | Env linter, warning | O4, O1 | Prompt ambiguity **and** grader inconsistency | **No** | Same decision as #1. The grader half is addressable without touching the prompt: add one line saying whether a data-integrity audit is credited, neutral or penalised as the basis of the recommendation | QA text, plus both grading records |
| 7 | Grader section C names an "S10-A block holding S03-E content" that the workbook does not contain | Env linter, info | — | Grader / design-document error | **No** | **Confirmed, and fix it.** See below | Recomputed this session |
| 8 | Grader scores only the comparator of the five per-study attributes the prompt asks for | Problem linter, warning | — | Grader-only | No | Grader-only; no golden edit. Known and already in HANDOFF as prompt-elicitation drift | QA text |
| 9 | Three undefined clauses: the scope and tolerance of the number-reproduction rule, whether A6's "before" means order in the answer, whether A11 survives a different reading of the second S09-A timepoint | Problem linter, info | — | Grader-only | No | Grader-only. Worth noting that in practice all sixteen graders applied the reproduction rule to numbered figures only and none of them tripped on A6's "before" | QA text and all sixteen rationales |

---

## Finding 7, confirmed — and the limb of it that does not hold

**Confirmed.** `S10-A` in the shipped workbook holds `Ifnb1`, `Tnf` and `Isg15` for PBS,
Sham, PSLN-344 and CT, five observations per analyte. `S03-E` values appear only in their
own `S03` block at rows 10–14. There is no S10-A-holds-S03-E anomaly in this room.
The shipped annotation describes `S10-A` correctly as CNS transcripts at 36 h.

**Where the stale item lives, and what to change.**

| Location | Line | Change |
|---|---|---|
| `build/anton-brief-psql25c1.md` | 293, the workbook-defect list: "the S10 block labelled S10-A carrying S03-E content" | Delete the line. The grader's section C is sliced from this brief, so deleting it here is the whole fix; then `python3 -I make-artifacts.py` and `--check` |
| `task/grader-guidelines.txt` section C | the same phrase, generated | Regenerates from the brief. Do not hand-edit |
| `HANDOFF.md` §1 | "expect and do not treat as defects" list includes "the `S10-A` block holding `S03-E` content" | Delete that entry from the list |

**The golden needs no edit.** It never makes the claim: its only `S10-A` references are
the correct ones — "Other blocks do carry 36 h (S02-F, S02-C, S10-A)" and "Central nervous
system cytokines (S10-A) ran 1.13 to 1.59 for PSLN-344". So no mode and no counterfactual
in `error_modes.md` is touched, and nothing needs re-checking after the fix.

**Derivability check:** passes trivially. The fix removes an assertion rather than adding
a fact, so nothing is being patched over a gap in the room.

**The second limb of finding 7 does not hold.** QA adds, flagged as unverified, that "the
annotation describes S03-G as HAI after challenge with PSLN-212Y/Sham/PSLN-344Y, n=8"
against a workbook block of 5 groups at n=5. The shipped annotation entry for `S03-G`
reads: HAI against Aichi H3N2, day 14, stated n 5, observations per group 5, groups as
printed Sham, CMP-204, PSLN-212, PSLN-344, PSLN-212(Y). The workbook block at `S03!K8`
carries exactly those five groups with five observations each. Annotation and workbook
agree. No action.

---

## Findings 1 and 6 — the one decision that is the writer's

These are the same finding from two checks, and they are the live question on this task.
Both options are set out; neither is recommended here.

| | **Leave the prompt as it is** | **Reword the "ground truth" line** |
|---|---|---|
| What it costs | The declining runs' route — gate the recommendation on the audit — stays unresolvable by the prompt, and graders will keep splitting on it. One of two stored graders already docked a run for a penalty the guidance does not contain | A rerun. The current sixteen runs were produced against this wording |
| What it buys | Standing decision 1 is preserved intact: the data is authoritative for the decision and is not error-free, and the contradictions stay | Removes the contradiction QA files as an **error**, and makes the audit-versus-accept choice gradeable |
| Effect on the ledger | None. The integrity-audit candidate is already rejected as a task defect, so no mode rests on the wording | None directly, but the verdict split would probably collapse, and with it the clean divergence-point reading in the verdict map |
| What is addressable either way | **The grader half.** Adding one line to the guidance saying whether an integrity audit is credited, neutral or penalised as the basis of the recommendation removes the grader inconsistency without touching the prompt or needing a rerun | same |

**Claude's read, offered as a read and not a decision:** the grader-side line is worth
adding regardless, because it costs nothing and fixes the documented inconsistency. The
prompt reword is the expensive half and its only beneficiary is score comparability, which
is deprecated on this task. Nothing in the FA depends on it.
