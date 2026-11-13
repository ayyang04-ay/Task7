# psql25c1 — calibration notes, 16-run panel

Panel-level observations that are **not FA material**. Keep out of the FA unless a
reviewer asks for panel context.

## Items that discriminate nothing

| Item | What happened | Read |
|---|---|---|
| **A5 / B4** (age-versus-adjuvant confound) | Fails in all sixteen runs | The task's one reliable trap. It is also the only item that both models fail without exception, so it is carrying the whole discrimination load. Worth knowing before the trap is ever softened |
| **A8** (the antigen-dose comparison named as unanswerable) | Not met or only partly met in all sixteen | **Discriminates nothing, and the requirement is weaker than the item implies.** Independently confirmed: the room holds each antigen at exactly one dose (0.5 µg HA CA09, 1 µg Aichi) and zero runs name the fixed dose as unanswerable. But the prompt does not ask for an inventory of unanswerable questions, and ten runs proposed a licensed high-dose comparator, which is the commercially relevant form of the question. The item is a grading-document requirement with no prompt or room basis, which is why it is a calibration note and not a mode |
| **B1, B2, B5, B6, B8, B9, B10** | Fired nowhere | Seven of the ten pre-registered penalties are inert on this panel. B2 in particular: every run found the mislabelled 72 h panel and exponentiated the log10 scale correctly, so the scale trap is solved by both models every time |
| **B7** (treating `S06-C` and `S06-D` as independent) | Fired nowhere as written | Every run found the 28-of-28 identity and excluded `S06-D` from its primary estimate. Two runs (F6, F7) use `S06-D` inside a day-3 pool while disclosing the identity in the same table |
| **A11 / B3** (resolution kinetics proposed as work) | Failed by O2, O4, O6, O7 on the grader's reading | **Looked discriminating and dissolved on the probe.** The item asks for a dedicated resolution study on a three-animal single-timepoint panel in which the candidate does not separate from the age-matched parent on five of seven analytes. Three of the four "failing" runs carried the finding into a safety or PD plan anyway. The item as written penalises a defensible prioritisation call, so it does not discriminate reasoning — it discriminates study-plan formatting. Worth rewording or retiring. Full evidence in `probe_notes.md` |
| **A13** (the limit that no blockade experiment carries a challenge endpoint) | Met wherever a rationale resolves it; unresolved in ten rationales | Not screenable from the deliverables by pattern: the phrasing varies too widely for a reproducible count, and that alone disqualified it as a mode |

## The pre-registration paid off

The fourth candidate registered at the foot of `fa/error_modes.md` — proposing an
adjuvant-alone or antigen-free arm that `S15-H` already settles — was looked for in this
panel and is **absent**. Fifteen runs cite `S15-H` by block label and retire the
non-specific-antiviral alternative on it; the sixteenth cites the same experiment by its
own evidence ID. Where an adjuvant-alone arm is proposed it is for attribution or
tolerability, which B10's own wording exempts.

This is the value of registering a shape before the batch runs: the result is
interpretable as an absence rather than as an oversight. Keep the practice.

## The model split, and why it is not a finding

Every Fable run advanced the asset, gated. Four of the eight Opus runs declined. The split
traces to one step: whether the data-integrity findings **gate** the recommendation or sit
beside it. Each declining run is an Opus run that gates on the audit.

This is a task-design axis, not a capability difference and not a failure mode. The prompt
tells the solver the data "serves as ground truth" while the room carries the
contradictions, so both routes are defensible; the QA chain files the contradiction as an
environment **error**; and the env-linter finding shows two graders acting on the ambiguity
in opposite directions. Any claim that one model "audits more" rather than "gates on the
audit it also ran" is unsupportable from this panel — every run in both arms produced a
long integrity register.

## Difficulty

The submit gate (mean score at or below 0.55) is **not cleared**: Fable 0.670, Opus 0.681.
Under standing decision 3 that gate is deprecated and the operative gate is at least one
failure mode shared by at least two runs, which is met several times over. Recorded here
only so that a reviewer reading the job metadata is not surprised by the red gate.

Two environment gaps every run worked around, both filed by ClaudeScope and neither a
mode: no single conda env carries openpyxl and lifelines together and `file`/`unzip` are
absent, so every run built a multi-env pipeline; and the image has no document renderer at
all, so no run could visually check the PDF or DOCX it shipped. The second is worth
flagging to whoever owns the image — sixteen of sixteen runs produced a document they were
unable to inspect.

## The 72 h panel is the task's best feature and the grader does not use it

The probe turned up something worth keeping for task design rather than for the FA. The
72 h panel is where the confound bites hardest, because there the young-parent denominator
inflates the *risk* rather than the benefit, and two runs in this very panel (F4, F8) got
it right while six did not. That is the cleanest discrimination anywhere in the package —
and B4's wording reaches it only incidentally, through "an age-gap, restoration or
age-gap-closure metric". A reactogenicity figure quoted as "2.85× the young level" is not
obviously a restoration metric, so a grader could miss it. If the grader is touched again,
B4 is worth widening from *metrics* to *any aged-versus-young figure in a block carrying a
young-plus-candidate arm*, which is what the FA mode actually covers.

## One thing to watch in the next batch

Mode 1 is now observed in twenty-four of twenty-four trajectories across two panels and two
identifier generations. That is a very reliable trap, which is good for the task and a
reason to be careful: a trap this reliable is usually a trap the room makes hard to avoid.
The counter-evidence is that one fresh agent in an earlier session did avoid it, and that
the avoiding comparison is printed in the same block. If a future panel fails it 16 of 16
again, it is worth asking whether the room's layout — the young-candidate arm sitting in
the last two columns of the block, absent from most other blocks — is doing more of the
work than the reasoning is.
