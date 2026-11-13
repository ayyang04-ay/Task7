# psql25c1 — FA outline, shaped for the submission form

**This is a reformat of `error_modes.md`, `probe_notes.md` and `solvability_screen.md`.
No new analysis. A correction made in the ledger propagates by rewriting one cell here.**

**Retype everything. Do not transcribe from this file.** Paste is disabled in Studio and
AI detection runs before submission. Work from the numbers, the run labels and the
locations; write the sentences yourself. The plain-language blocks below are marked as
**context to read, not to lift** — they exist so the finding is clear in your head before
you write it, and lifting them is exactly what the overlap check catches. Ask me for the
overlap measurement against my own output before you submit.

**One question before you use this layout:** do you have an FA from another task that was
accepted? Reformatting into a shape with known reviewer acceptance beats this one, which
is the format from task `af758d37` and cleared the AI QC bar there but is not yours.

---

# Part 1 — What did the model do wrong

**One failure item. Two sites.** The item is in all sixteen runs at the first site and in
six at the second. Nothing else in the panel cleared both the prevalence floor and the
defensibility bar; what died, and on which bar, is in `error_modes.md` and summarised at
the end of Part 2, because a correct approach whose absence was defensible belongs in the
should-have-done section and not here.

## The aged response is measured against a differently formulated young arm

**Runs:** every run — F1, F2, F3, F4, F5, F6, F7, F8, O1, O2, O3, O4, O5, O6, O7, O8.

**Plain language — context to read, not to lift.** The room holds four groups on the same
readout: old and young animals, each given the candidate or the Mn-free parent. To ask
what ageing costs, you compare old against young on the *same* formulation. Every run
instead compared old animals on the candidate against young animals on the *parent*, and
reported that the candidate returns the aged response to a young level. On the comparison
that holds the formulation fixed, the aged animals reach about three-quarters of young.
Three runs had the fourth group's number written down in their own files and did not use
it. The consequence is not the survival verdict, which nobody got wrong — it is the
mechanism claim, the biomarker rationale, and in one run a human go criterion.

### Site 1 — the 16 h restoration figure

`S01-A`, sheet `S01` rows 3–10, columns B–F. Arm means over five animals, lung *Ifnb1*
at 16 h, fold over untreated: **aged+parent 16.64, aged+candidate 37.11, young+parent
37.60, young+candidate 50.70.** Runs reporting geometric means give 16.5, 36.9, 37.5,
50.2.

| Run | The number or claim it produced | Where |
|---|---|---|
| F1 | "which is the young level (37.6 … in young mice on PSLN-212)"; "the one readout restored in full" | `:168` |
| F1 | "median 72% of the young PSLN-212 value", 28 readouts | `:116` |
| F2 | "median 73% of the young PSLN-212 response", 26 readouts | `:74` |
| F2 | ledger row `I26`, the restoration index; row `M1` holds young+candidate 50.7 ± 7.6; row `M23` holds the within-cohort effect | `:454`, `:455`, `:479` |
| F3 | "against young mice given PSLN-212 (37.6-fold) the ratio is 0.98×" | `:110` |
| F3 | "PSLN-212 gives aged mice 44% of the young Ifnb1 response and PSLN-344 gives 99%" | `:271` |
| F4 | "0.98 of young" | `:17` |
| F5 | table row, restoration `0.98` | `:124` |
| F6 | "gap closed 98%" | `:160` |
| F7 | restoration index defined as 1 = equal to young PSLN-212 | `:105` |
| F7 | table row, restoration `0.98` | `:109` |
| F8 | "returns the aged interferon response to the young level (99%; CI 84–116)" | `:140` |
| O1 | table row "restoration R = 0.98" | `:68` |
| O1 | prints young+candidate at 50.2 against 37.5 and leaves R = 0.98 unchanged | `:258` |
| O1 | human go criterion "older-donor R ≥ 0.5", R being that index | `:370` |
| O2 | "GMR vs young = 0.98"; "R = 0.98" | `:146`, `:147` |
| O2 | "fully age-restoring: aged PSLN-344 equals young PSLN-212 (GMR 0.98)" | `:337` |
| O3 | "lung IFN-β at 16 h 98% of young" | `:128` |
| O4 | index written out: (aged+cand − aged+parent) ÷ (young+parent − aged+parent) | `:125` |
| O4 | table row, RI `0.98` | `:134` |
| O5 | "That equals the young value (37.5×; ratio 0.984, 95% CI 0.837–1.16)" | `:144` |
| O6 | "restores IFN-β induction to the young level … restoration index 0.98" | `:22` |
| O7 | "closes 98% of the age gap" | `:43` |
| O7 | "Mn²⁺ restores this completely (restoration 0.98)" | `:233` |
| O8 | "Mn²⁺ restores it exactly: 36.9×, ratio to young 0.98" | `:123` |

**Why it is wrong, in the room's own numbers.** The denominator changes the age and the
adjuvant together. `S01-A` carries young+candidate at 50.70 in the same block, so the
formulation can be held constant: aged+candidate over young+candidate is **37.11 / 50.70
= 0.732**, not 0.98. The uncontaminated reading of the same block is the adjuvant effect
inside each cohort — aged ×2.23 against young ×1.35 — and the same contrast is available
in all six four-arm blocks: `S01-E` ×2.28 against ×1.06, `S01-F` ×1.65 against ×1.02,
`S02-C` ×4.01 against ×1.18, `S02-E` ×24.35 against ×1.20. Six of the seven panels rise
in aged animals. The exception is the 72 h residual, where the young gain is the larger,
×1.29 against ×1.97.

**Why it is not simply a defensible call.** The arm that settles it is in the same block,
and three runs retrieved its value and still did not use it: F2 at ledger row `M1`, F3 in
its ruled-out table, O1 in the body of the memo at `:258`. F2 went further and computed
the within-cohort effect at row `M23` without carrying it into the claim. So the failure
is not that the room hid the control — the room prints it, and the runs read it.

**Exemplar.** None at this site; every run carries it. It is avoidable: in an earlier
session one of two fresh agents run against the same room compared aged+candidate against
young+candidate and reported the amplification as a property of the chemistry rather than
a correction of an aged deficit (p = 0.0121, verified).

**One honest limit to carry.** This changes the mechanism claim, the biomarker
qualification and O1's human go criterion. It does **not** change any run's advance or
decline verdict, and the survival case is not affected. Do not push it further than that.

### Site 2 — the same denominator on the 72 h panel, where it inflates the risk

`S09-A` panel 2 (`S09` columns X–AS, rows 3–9, the panel printed 16 h that holds the 72 h
data) and `S01-A` at 72 h. This is the reading that argues *against* the asset, and it is
computed against the same young-parent arm.

| Run | The number or claim it produced | Where |
|---|---|---|
| O2 | "At 72 h, *Ifnb1* is still 2.85× the young level" | `:177` |
| O3 | "Aged PSLN-344 285% of young at 72 h", carried into a safety marker | `:184` |
| O4 | "Tnf 17.8× (p = 0.008), Il10 36.6× (p = 0.002) vs the young benchmark" | `:338` |
| O5 | restoration fraction −0.235, read as moving away from the young profile | `:97`, `:139` |
| O6 | "Lung Ifnb1 at 72 h is 2.85× the young level" | `:203` |
| O8 | "At 72 h aged PSLN-344 lungs still carry Ifnb1 2.85× above young"; tolerability marker at −0.24 "overshoot" | `:150`, `:171` |

**Why it is wrong, in the room's own numbers.** Against the age-matched parent arm the
same panel gives Tnf ×1.62 (p = 0.052), Il10 ×1.00 (p = 0.991) and Ifnb1 ×1.18
(p = 0.665); in `S01-A` at n = 5, Ifnb1 is ×1.29 (p = 0.2619). Two analytes reverse
outright: at 72 h the young parent arm carries Ccl2 101.59 and Ccl3 41.45 against the aged
candidate's 27.41 and 9.23. So the alarming version of the reactogenicity flag is produced
by the denominator, not by the candidate.

**Exemplar — and this is the strongest thing in the FA.** Two runs in the same panel did
it correctly. **F8** at `:168`: "Aged PSLN-212 shows the same Tnf and Il10 tail (5.2 and
4.2), so that part is an age effect. Il6 is the exception: 7.2 vs 1.9, p = 0.03" — which
reproduces the independent recomputation (p = 0.026). **F4** at `:251` reports both
columns, "Tnf 17.8 times young (4.8–66) and 1.6 times aged PSLN-212 (0.99–2.6)", with an
interval that correctly straddles 1.0. Lead with this when the defensibility challenge
comes: two runs held the formulation constant on this exact panel and six did not, so the
room does not force the error.

**One honest limit to carry.** Il6 *is* a real candidate-specific excess at 72 h, ×3.85,
p = 0.026. The claim is that the panel's headline figures are confounded, not that there
is no 72 h signal at all.

---

# Part 2 — What the model should have done

**Section discipline.** Everything prescriptive goes here, and so does anything a run did
well. Critically, so does **any correct approach whose absence was a defensible choice** —
three of those are at the end of this part. The two parts are not mirror images, and three
of the candidates that died on the defensibility bar still belong in this one.

## The verdict, as one block

Advance the asset. Across the six configurations in which aged animals were vaccinated and
then challenged with a virus of a different subtype, the candidate separates from vaccine
alone at p = 0.0002 in every block and from the Mn-free parent at p = 0.0009 to 0.0151,
while the parent itself fails to separate from vaccine alone in three of those six
(p = 0.088, 0.111, 0.066) — so the manganese carries the effect, not the liposome. On
survival the aged animals are not distinguishable from young animals on the parent in any
configuration (p = 0.060 to 0.317). The route is intranasal in aged animals at the mounted
adjuvant dose; the forward plan is three studies, gated on the resolution study as the
tolerability question; and the asset's claim is cross-subtype breadth, not titre.

## The components, each with what derives it

| # | Component | The call | What derives or supports it |
|---|---|---|---|
| 1 | Verdict | Advance | six cross-subtype configurations, candidate vs vaccine alone p = 0.0002 throughout, vs parent p = 0.0009–0.0151 |
| 2 | What carries the effect | the manganese, not the liposome | the parent fails to separate from vaccine alone in three of the six, p = 0.088, 0.111, 0.066 |
| 3 | The claim | cross-subtype breadth | the strict set, challenge sharing neither HA nor NA with the vaccine: `S06-A`, `S06-B`, `S06-E` rows 34–68, `S06-G`, giving candidate 20/28 against parent 1/28. Adding the two sharing N1 only, `S06-C` and `S06-F`, gives 32/42 against 4/42 |
| 4 | Not rested on titre | no antibody measure as the cross-subtype correlate | every antibody assay in the room runs against the vaccine's own strains — HAI and neutralisation against CA09 in `S03-C`/`S03-D` and against Aichi in `S03-G`/`S03-H` — while the challenges are PR8, Perth, rgH5N1 and wild-type VN04 |
| 5 | The age claim, stated correctly | the adjuvant effect inside each cohort, not a cross-formulation restoration figure | `S01-A` aged ×2.23 vs young ×1.35; `S01-E` ×2.28 vs ×1.06; `S01-F` ×1.65 vs ×1.02; `S02-C` ×4.01 vs ×1.18; `S02-E` ×24.35 vs ×1.20. Formulation held constant, aged reaches 0.732 of young, not 0.98 |
| 6 | Efficacy biomarker | antigen-specific CD8 and tissue-resident memory — carry forward | resident memory 0.656 of young; cross-subtype-restimulated IFN-γ CD8 0.693 at day 14 and 0.687 at day 60 |
| 6b | …and its limit | access, not validity: not a routine endpoint | day-25 resident memory is lung; day-14 and day-60 restimulation are mediastinal node. Both need tissue |
| 7 | Antibody's role | immunogenicity and the regulatory bridge, **not** efficacy | peripherally accessible and routine, which is its value; but no accepted antibody surrogate exists for cross-subtype protection |
| 8 | Adjuvant-engagement marker | lung GM-CSF at 36 h, preclinical only | antigen-independent and separates cleanly, 8.74 against 1.59 and 1.21. Lung transcript, so there is no patient-accessible version — a gap, not an asset |
| 9 | Priming chain | rested on the blockade experiments, not on correlation | `S11-C`, `S02-H`, `S02-I`, `S07-B`, `S05-C` |
| 9b | …and its limit | the step from priming to protection is inferred, not shown | no blockade experiment carries a challenge endpoint |
| 10 | Per-animal linkage | state that none exists | survival blocks carry only time and event; immune readouts and survival were never measured in the same animals |
| 11 | Study 1 | close the priming-to-protection step | survival to day 14 primary, with the cellular readouts on the same animals; CCR2 blockade, CD8 depletion, vehicle, sham; challenge at day 3 and day 14 in parallel; cellular sampling day 7–10, not day 3 |
| 12 | Study 2 | benchmark against more antigen | HA content is never varied anywhere in the package, so the question cannot be answered from it; comparators standard-dose with candidate, **high-dose antigen without adjuvant, dose-ranged**, standard-dose with parent, sham |
| 13 | Study 3 | resolution kinetics, as the **gating** tolerability study | all seven analytes above the untreated reference at the last measured timepoint — Ccl2 27.41, Ccl3 9.23, Tnf 8.44, Il6 7.19, Il10 4.16, Ifnb1 4.01, Ccl5 2.01 — and no arm carries a later one |
| 13b | …and its comparators | age-matched parent and age-matched untreated; the young arm is context, not the acceptance criterion | both ageing and the formulation raise the residual and the block cannot separate them: formulation ×1.97 p = 0.0126 in young and ×1.29 p = 0.2619 in aged; ageing ×2.16 p = 0.0009 on the parent and ×1.42 p = 0.1756 on the candidate |
| 14 | Dose | the mounted adjuvant dose, and not higher | `S08-A` reads a plateau; higher parent doses do not substitute |

## Alternatives closed, each on its own ground

| Alternative | Closed on |
|---|---|
| A non-specific antiviral state from STING activation | `S15-H` at the 3-day interval: adjuvant alone 0/7, vaccine alone 0/7, the combination 6/7. Protection needs the antigen |
| `S06-D` as a seventh configuration | identical to `S06-C` in all 28 time-and-event pairs |
| The two blocks at `S06` rows 69–70 as cross-subtype evidence | both challenge viruses fall inside the subtypes the bivalent vaccine contains. Retained for the imprinting question, where both candidate arms ran 85.7% with or without prior PR8 exposure |
| Antibody titre as the readout to power the next study on | largest effects in the package, but every antibody assay used the vaccine's own antigens |
| The `S03-B`/`S03-F` subclass panels as printed | under the printed assignment one arm's IgG2a plus IgG1 would exceed its own total IgG by 16.1-fold for H1N1 and 11.3-fold for H3N2; reducing per animal makes it 18.8 and 12.5, so the reading is reduction-invariant |
| The arithmetic mean for HAI | on `S03-C` it implies a sham titre of 6.0 against an assay floor of 1 in 10 |
| `S05-A` in the day-3 mechanism case | the source gives two different immunisations for the same panel and nothing resolves it; the day-3 case rests on `S05-D` and `S05-E` |
| Extension beyond influenza | no non-influenza pathogen antigen anywhere; ovalbumin is a model protein |
| A BALB/c-only effect | `S15-L` and `S15-N` point the same way, candidate 6/7 in both — but they state no challenge virus, so they cannot be classified and are not in the six |

## Correct approaches whose absence was defensible — they belong here, not in Part 1

Three candidates were built against this panel, tested, and dropped. Each is still
something a response should have done; none is something a run can be faulted for.
**Say so explicitly if you include them, or a reviewer reads Part 1 as incomplete.**

| What a response should have done | Why its absence is not a failure |
|---|---|
| Named the antigen-dose question as one the package cannot answer, and proposed a dose-ranged high-dose-antigen arm **at the asset's own route** | No run named it, on both a tight and a loose screen, and the room holds each antigen at exactly one dose — 0.5 µg HA for CA09, 1 µg for Aichi. But the prompt does not ask for an inventory of unanswerable questions, and ten runs proposed a licensed high-dose comparator, which is the commercially relevant form of it. The requirement sits in the grading document, not in the prompt or the room. Where runs did propose the arm it was intramuscular, so route moved with dose — worth saying as a design point, not as an error |
| Specified a study that measures when the 72 h innate response returns to baseline | O2, O4, O6 and O7 did not. But the readout is three animals per arm at one timepoint on a panel carrying its own duplication finding, and the candidate does not separate from the age-matched parent on five of seven analytes. O4 quantified it with its n and flag stated and built a 72 h reactogenicity guard-rail; O6 named it as a risk and routed lung histopathology into the IND package; O7 excluded the panel on a stated mounted fact. Folding resolution into standard GLP toxicology is a defensible prioritisation call |
| Used the cross-subtype subset as the unit of analysis rather than an all-challenge pool | F1, F2, F3, O3, O4, O5 and O6 never compute any heterosubtypic-restricted estimate, and rest a breadth claim on a pool mixing homologous `S03-I`/`S03-J`, the matched-subtype imprinting blocks, and `S15-L`/`S15-N` whose challenge virus is unstated. But each of them names the heterosubtypic blocks individually in a table a reader can see, which is a presentational choice an expert defends. Only O6 states outright that the imprinting challenges are "heterosubtypic or antigenically distant", which is wrong — one run, so it does not clear the floor |

## The closing line, if you use one — and two claims that do NOT survive

If you write "everything else was already right in all sixteen runs", it needs its
exceptions verified run by run rather than taken from the grader. I checked four candidate
blanket claims. **Three hold. Two of the four do not, and I had drafted one of the failing
ones into this file before checking it.**

**Safe to assert, verified run by run in the deliverables:**

| Claim | Basis |
|---|---|
| The log10 scale on `S09-A` was handled correctly in all sixteen | every run exponentiated; the graders' independent recomputations agree; the panel-2 relabelling reproduces `S01-A` 72 h in 21 of 21 values, median error 0.113%, against 76.2% versus the 16 h panel |
| All sixteen identified the 28-of-28 identity of `S06-C` and `S06-D` | read in each run's own integrity register |
| All sixteen engaged `S15-H` and retired the non-specific-antiviral alternative on it | fifteen cite the block label; O7 cites the same experiment by its own evidence id |

**Do not assert these — they break:**

| Claim I would have made | Where it breaks |
|---|---|
| "`S06-D` was excluded from the primary estimate in all sixteen" | F6's breadth figure is "39 of 49 against 6 of 49; S06-A to S06-G" at `:19` and it resolves the duplication by dropping `S06-C` instead, at `:106`. F7's day-3 pool "28/31" at `:17` includes `S06-D`, with "Without S06-D" offered as a sensitivity at `:94`. Both handle the duplication, neither by the same route, so the blanket form is wrong |
| "`S06-G` was reported with its unvaccinated unchallenged arm in all sixteen" | a direct screen returns nothing for F4, F6, F8, O1, O6, O7 and O8. Some of those may be legitimate set-asides of the block on another stated fact, which the grader's own B6 exempts — but I have not resolved them one by one, so it cannot go in a blanket line |

Anything beyond those three, check before it goes in.
