#!/usr/bin/env python
"""
Step 14 - Assemble the proposal (Markdown -> DOCX via pandoc) and the evidence ledger.
Every number in the text is looked up from the analysis outputs through report_numbers.py; the same
variables feed the ledger, so text and ledger cannot drift apart.
"""
import sys, os, re, json, subprocess, textwrap
sys.path.insert(0, "/tmp/outputs/analysis")
import numpy as np, pandas as pd
from scipy import stats
from report_numbers import *
import integrity_log as IL

SRC = "/tmp/outputs/analysis/report_src"; os.makedirs(SRC, exist_ok=True)
LEDGER = []
def led(section, statement, value, source, output, method=""):
    LEDGER.append(dict(id=f"L{len(LEDGER)+1:03d}", section=section, statement=statement, value=value, workbook_source=source, analysis_output=output, method=method))

def pct(k, n): return f"{100*k/n:.0f}%"
def frac(t): return f"{t[0]}/{t[1]}"
def f1(v): return f"{v:.1f}"
def f0(v): return f"{v:.0f}"
def f2(v): return f"{v:.2f}"
def fx(v): return f"{v:.1f}" if v < 10 else f"{v:.0f}"
def th(v): return f"{v:,.0f}"

# =====================================================================================================
# NUMBERS
# =====================================================================================================
# ---- pooled survival
pT2 = pool("TTE", "PSLN-212"); pTs = pool("TTE", "Sham"); pW2 = pool("WORST", "PSLN-212"); pWs = pool("WORST", "Sham")
sNF2 = sens("excluding every experiment", "PSLN-212"); sNFs = sens("excluding every experiment", "Sham"); sXD = sens("excluding S06-D", "PSLN-212")
OUT_POOL = "stats/survival_pooled.csv (script 05)"; OUT_SENS = "stats/survival_sensitivity.csv (script 08)"; OUT_ARM = "stats/survival_by_arm.csv (script 04)"
SRC_POOL = "status columns of S03-I, S03-J, S06-A to S06-G, S06-E and S06-F second blocks, S15-L, S15-N (and S15-H for the sham comparison)"
led("1", "Pooled survival, aged animals, vaccine + PSLN-344 vs vaccine + PSLN-212 (15 head-to-head comparisons in 13 experiment blocks)",
    f"{pT2.psln344} ({pT2.psln344_pct:.0f}%, 95% CI {pT2.psln344_ci}) vs {pT2.comparator_surv} ({pT2.comparator_pct:.0f}%, 95% CI {pT2.comparator_ci})", SRC_POOL, OUT_POOL,
    f"Cochran-Mantel-Haenszel stratified by experiment, chi2 = {pT2.cmh_chi2:.0f}, p < 1e-20; Mantel-Haenszel risk difference {pT2.mh_risk_diff_pct:.0f} points; exact (Clopper-Pearson) CIs")
led("1", "Pooled survival, vaccine + PSLN-344 vs vaccine + empty liposome or vaccine alone (12 comparisons)",
    f"{pTs.psln344} ({pTs.psln344_pct:.0f}%) vs {pTs.comparator_surv} ({pTs.comparator_pct:.0f}%)", SRC_POOL, OUT_POOL, f"CMH chi2 = {pTs.cmh_chi2:.0f}, p < 1e-20")
led("1", "Same, worst reading of the workbook (lower of survival-block and weight-block count for PSLN-344, higher for each comparator)",
    f"{pW2.psln344} ({pW2.psln344_pct:.0f}%) vs {pW2.comparator_surv} ({pW2.comparator_pct:.0f}%) for PSLN-212; {pWs.psln344} vs {pWs.comparator_surv} for sham", SRC_POOL + "; paired weight blocks S13-F, S13-G, S15-A to S15-O",
    OUT_POOL + "; stats/survival_reconciliation.csv", f"CMH p < 1e-20 for both")
led("1", "Same, after removing every experiment with an integrity flag (kept: S06-A, S06-B, S06-F, S15-N, S06-E and S06-F second blocks)",
    f"{sNF2.psln344} ({sNF2.psln344_pct:.0f}%) vs {sNF2.comparator_surv} ({sNF2.comparator_pct:.0f}%) for PSLN-212; {sNFs.psln344} vs {sNFs.comparator_surv} for sham", "as above, subset", OUT_SENS, f"CMH p = {sNF2.cmh_p:.1e} and {sNFs.cmh_p:.1e}")
k20_344 = sumk(["S03-I", "S03-J", "S06-A", "S06-B", "S06-C", "S06-D", "S06-E", "S06-F", "S06-G", "S15-L", "S15-N"], "PSLN-344")
k20_212 = sumk(["S03-I", "S03-J", "S06-A", "S06-B", "S06-C", "S06-D", "S06-E", "S06-F", "S06-G", "S15-L", "S15-N"], "PSLN-212")
led("1", "Subset of animals aged 20 months or more (11 experiment blocks)", f"{frac(k20_344)} vs {frac(k20_212)}", "S03-I, S03-J, S06-A to S06-G, S15-L, S15-N", OUT_ARM, "sum of arms")
# ---- breadth
hom = arm("S03-I", "PSLN-344"); het14 = sumk(["S06-A", "S06-C"], "PSLN-344"); het14_212 = sumk(["S06-A", "S06-C"], "PSLN-212")
early = (sum(arm(b, g)[0] for b, g in [("S03-J", "PSLN-344"), ("S06-B", "PSLN-344"), ("S06-D", "PSLN-344"), ("S15-H", "3d Vaccine+PSLN-344")]), sum(arm(b, g)[1] for b, g in [("S03-J", "PSLN-344"), ("S06-B", "PSLN-344"), ("S06-D", "PSLN-344"), ("S15-H", "3d Vaccine+PSLN-344")]))
early_sham = (sum(arm(b, g)[0] for b, g in [("S03-J", "Sham"), ("S06-B", "Sham"), ("S06-D", "Sham"), ("S15-H", "3d Vaccine")]), 31)
h5 = arm("S03-J", "PSLN-344"); h5s = arm("S03-J", "Sham"); h5p = arm("S03-J", "PSLN-212")
strain = sumk(["S15-L", "S15-N"], "PSLN-344"); strain212 = sumk(["S15-L", "S15-N"], "PSLN-212")
imp344 = (sum(arm(b, g)[0] for b in ["S06-E(2) imprinting/PR8", "S06-F(2) imprinting/Perth"] for g in ["Naive+PSLN-344", "Imprinting+PSLN-344"]), 28)
imp212 = (sum(arm(b, g)[0] for b in ["S06-E(2) imprinting/PR8", "S06-F(2) imprinting/Perth"] for g in ["Naive+PSLN-212", "Imprinting+PSLN-212"]), 28)
naive14_344 = (sum(arm(b, "Naive+PSLN-344")[0] for b in ["S06-E(2) imprinting/PR8", "S06-F(2) imprinting/Perth"]), 14)
naive14_212 = (sum(arm(b, "Naive+PSLN-212")[0] for b in ["S06-E(2) imprinting/PR8", "S06-F(2) imprinting/Perth"]), 14)
impr_344 = (sum(arm(b, "Imprinting+PSLN-344")[0] for b in ["S06-E(2) imprinting/PR8", "S06-F(2) imprinting/Perth"]), 14)
impr_212 = (sum(arm(b, "Imprinting+PSLN-212")[0] for b in ["S06-E(2) imprinting/PR8", "S06-F(2) imprinting/Perth"]), 14)
d60_344 = sumk(["S06-E", "S06-F", "S06-G"], "PSLN-344"); d60_212 = sumk(["S06-E", "S06-F", "S06-G"], "PSLN-212"); d60_sham = sumk(["S06-E", "S06-F", "S06-G"], "Sham")
d60_y = sumk(["S06-E", "S06-F", "S06-G"], "PSLN-212(Y)"); d60_unt = sumk(["S06-E", "S06-F", "S06-G"], "Untreated")
d14_344 = sumk(["S03-I", "S06-A", "S06-C"], "PSLN-344")
p_d14_d60 = stats.fisher_exact([[d14_344[0], d14_344[1] - d14_344[0]], [d60_344[0], d60_344[1] - d60_344[0]]])[1]
p_d60_unt = stats.fisher_exact([[d60_344[0], d60_344[1] - d60_344[0]], [d60_unt[0], d60_unt[1] - d60_unt[0]]])[1]
alone = arm("S15-H", "3d PSLN-344"); vacalone = arm("S15-H", "3d Vaccine"); combo = arm("S15-H", "3d Vaccine+PSLN-344")
young = {b: (arm(b, "PSLN-344Y"), arm(b, "PSLN-212Y"), arm(b, "Sham")) for b in ["S09-B", "S09-D", "S09-F"]}
cmp_surv = arm("S03-I", "CMP-204")
led("1", "Matched-strain (homologous) challenge, day 14, PSLN-344", frac(hom), armcells("S03-I", "PSLN-344"), OUT_ARM, f"vs Sham {frac(arm('S03-I','Sham'))}: exact log-rank p = {fp(sp('S03-I','Sham','PSLN-344'))}")
led("1", "Cross-subtype (heterosubtypic) challenge at day 14, PSLN-344 vs PSLN-212", f"{frac(het14)} vs {frac(het14_212)}", f"S06-A {armcells('S06-A','PSLN-344')}; S06-C {armcells('S06-C','PSLN-344')}", OUT_ARM, "sum of two experiments")
led("1", "Challenge 2 to 3 days after a single dose, PSLN-344 (vs sham or vaccine alone)", f"{frac(early)} vs {frac(early_sham)}", "S03-J, S06-B, S06-D, S15-H", OUT_ARM + "; stats/sensitivity_power.txt", "sum of four experiments")
led("1", "Wild-type H5N1 challenge 2 days after one dose: PSLN-344 vs the two comparator arms as labelled (Sham, PSLN-212)", f"{frac(h5)} vs {frac(h5s)} and {frac(h5p)}", "S03!H17:J46 (days in G17:G46; G46 empty)", OUT_ARM,
    f"exact log-rank p = {fp(sp('S03-J','Sham','PSLN-344'))} and {fp(sp('S03-J','PSLN-212','PSLN-344'))}; see integrity item D-07")
led("1", "Other mouse strains (aged C57BL/6 and Swiss Webster), PSLN-344 vs PSLN-212", f"{frac(strain)} vs {frac(strain212)}", "S15!B103:E130; S15!B134:E161", OUT_ARM, "sum of two experiments; challenge virus not stated; see D-08, D-15")
led("1", "14-month animals with or without prior PR8 infection, PSLN-344 vs PSLN-212", f"{frac(imp344)} vs {frac(imp212)}", "S06!H71:K98; S06!N71:Q98", OUT_ARM, "sum of four arms each")
led("3", "14-month animals without prior infection: PSLN-344 vs PSLN-212", f"{frac(naive14_344)} vs {frac(naive14_212)}", "S06!H71:H77, J85:J91, N71:N77, P85:P91", OUT_ARM, "sum of two experiments")
led("3", "14-month animals with prior PR8 infection: PSLN-344 vs PSLN-212", f"{frac(impr_344)} vs {frac(impr_212)}", "S06!I78:I84, K92:K98, O78:O84, Q92:Q98", OUT_ARM, "sum of two experiments")
led("1", "Adjuvant without vaccine, vaccine without adjuvant, and both, challenged on day 3", f"{frac(alone)}, {frac(vacalone)}, {frac(combo)}", "S15!B73:D93", OUT_ARM, f"exact log-rank, both vs alone p = {fp(sp('S15-H','3d PSLN-344','3d Vaccine+PSLN-344'))}")
led("1", "Young animals, three challenge models (S09-B and S09-D challenged 21 days after the dose, S09-F 180 days after): PSLN-344 vs PSLN-212 (vs sham)", "; ".join(f"{b}: {frac(v[0])} vs {frac(v[1])} ({frac(v[2])})" for b, v in young.items()), "S09!B12:D35; S09!B39:D62; S09!B66:D88", OUT_ARM, "counts")
led("1", "Day-60 challenge: PSLN-344, PSLN-212, sham, young PSLN-212, untreated-unchallenged", f"{frac(d60_344)} ({pct(*d60_344)}), {frac(d60_212)}, {frac(d60_sham)}, {frac(d60_y)}, {frac(d60_unt)}", "S06!H34:L68; S06!N34:R68; S06!B71:F105", OUT_ARM + "; stats/sensitivity_power.txt", "sum of S06-E, S06-F, S06-G")
led("1", "Day-14 challenge (S03-I, S06-A, S06-C) vs day-60 challenge, PSLN-344", f"{frac(d14_344)} vs {frac(d60_344)}", "as above", "stats/sensitivity_power.txt (script 08)", f"Fisher exact p = {p_d14_d60:.3f}")
led("6", "Day-60 challenged PSLN-344 vs untreated-unchallenged animals", f"{frac(d60_344)} vs {frac(d60_unt)}", "as above", "stats/sensitivity_power.txt", f"Fisher exact p = {p_d60_unt:.2f}")
d14m = sumk(["S06-A", "S06-C"], "PSLN-344"); d60m = sumk(["S06-E", "S06-F"], "PSLN-344")
p_matched = stats.fisher_exact([[d14m[0], d14m[1] - d14m[0]], [d60m[0], d60m[1] - d60m[0]]])[1]
led("6", "Durability restricted to the two models run at both intervals (S06-A and S06-C at day 14; S06-E and S06-F at day 60), PSLN-344", f"{frac(d14m)} vs {frac(d60m)}", "S06!D17:D23, P17:P23 vs S06!J48:J54, P48:P54", "stats/sensitivity_power.txt (script 08, part b)", f"Fisher exact p = {p_matched:.2f}")
# weight at death (script 08, part c)
WD_344 = [79.8, 85.3, 83.9, 80.3, 77.5]; WD_UNT = [94.5, 96.6, 95.0, 95.7]
Dst = pd.read_csv("/tmp/outputs/analysis/integrity/D_bodyweight_animal_status.csv"); bwt = pd.read_csv("/tmp/outputs/analysis/tidy/bodyweight.csv")
def lastw(group):
    q = Dst[Dst.block.isin(["S15-E", "S15-F", "S15-G"]) & (Dst.status != "complete") & (Dst.group == group)]
    out = []
    for _, r in q.iterrows():
        v = bwt[(bwt.block == r.block) & (bwt.animal == r.animal) & (bwt.day == r.last_real_day)]["value"].iloc[0]; out.append(float(v))
    return out
wd344, wdunt = lastw("PSLN-344"), lastw("Untreated"); assert sorted(wd344) == sorted(WD_344) and sorted(wdunt) == sorted(WD_UNT)
p_wd = stats.mannwhitneyu(wd344, wdunt, method="exact").pvalue
led("1", "Last recorded body weight of animals that died: PSLN-344 after day-60 challenge vs untreated-unchallenged", f"{min(wd344):.1f} to {max(wd344):.1f}% of starting weight, i.e. a loss of {100-max(wd344):.0f} to {100-min(wd344)+1e-9:.0f}% (mean {np.mean(wd344):.1f}%, n = {len(wd344)}) vs {min(wdunt):.1f} to {max(wdunt):.1f}% (mean {np.mean(wdunt):.1f}%, n = {len(wdunt)})",
    "S15!W47, W56, Z56, W69, Z69 vs S15!AE45, AD65, AE67, AF68", "stats/sensitivity_power.txt (script 08, part c)", f"exact Mann-Whitney p = {p_wd:.3f}")
# ---- innate
B = "S01-A"; i344 = m(B, "PSLN-344", "Ifnb1 16h", "16h"); i212 = m(B, "PSLN-212", "Ifnb1 16h", "16h"); iy = m(B, "PSLN-212(Y)", "Ifnb1 16h", "16h"); i344y = m(B, "PSLN-344(Y)", "Ifnb1 16h", "16h"); icmp = m(B, "CMP-204", "Ifnb1 16h", "16h")
ir848 = m(B, "PSLN-R848", "Ifnb1 16h", "16h"); icombo = m(B, "PSLN-212/R848", "Ifnb1 16h", "16h")
OUT_C = "stats/continuous_summary.csv, continuous_pairwise.csv (script 03)"
led("1", "Lung Ifnb1 at 16 h, fold vs untreated: PSLN-344 aged, PSLN-212 aged, PSLN-212 young", f"{f1(i344)}, {f1(i212)}, {f1(iy)} (ratio {i344/i212:.1f}; aged as % of young: {100*i344/iy:.0f}% and {100*i212/iy:.0f}%)",
    f"{cells(B,'PSLN-344','Ifnb1 16h','16h')}; {cells(B,'PSLN-212','Ifnb1 16h','16h')}; {cells(B,'PSLN-212(Y)','Ifnb1 16h','16h')}", OUT_C,
    f"n = 5; Welch on log10 p = {fp(pw(B,'PSLN-212','PSLN-344','Ifnb1 16h','16h',True))}; exact Mann-Whitney p = {fp(pmw(B,'PSLN-212','PSLN-344','Ifnb1 16h','16h'))}; Tukey p = {fp(ptk(B,'PSLN-212','PSLN-344','Ifnb1 16h','16h'))}; PSLN-344 vs young p = {fp(pw(B,'PSLN-344','PSLN-212(Y)','Ifnb1 16h','16h',True))}")
g16_344, g16_212, g16_sh = m("S02-F", "PSLN-344", "", "16h"), m("S02-F", "PSLN-212", "", "16h"), m("S02-F", "Sham", "", "16h")
g36_344, g36_212 = m("S02-F", "PSLN-344", "", "36h"), m("S02-F", "PSLN-212", "", "36h")
led("1", "Lung Gm-csf, fold vs untreated, 16 h and 36 h: PSLN-344 vs PSLN-212 (sham at 16 h)", f"16 h: {f1(g16_344)} vs {f1(g16_212)} ({g16_344/g16_212:.1f}x; sham {f1(g16_sh)}); 36 h: {f1(g36_344)} vs {f1(g36_212)} ({g36_344/g36_212:.1f}x)",
    "S02!B17:P19", OUT_C, f"n = 5; Welch on log10 p = {fp(pw('S02-F','PSLN-344','PSLN-212','','16h',True))} and {fp(pw('S02-F','PSLN-344','PSLN-212','','36h',True))}; PSLN-212 vs sham at 16 h p = {fp(pw('S02-F','PSLN-212','Sham','','16h',True))}")
ch = CHAIN[CHAIN.stage != "Protection"]; n_ch = len(ch); n60 = int((ch.aged344_pct_young >= 60).sum()); lo_ch = ch.sort_values("aged344_pct_young").head(2)
led("1", f"Immune readouts (of {n_ch}) in which aged PSLN-344 reaches at least 60% of the young benchmark", f"{n60} of {n_ch}; range {ch.aged344_pct_young.min():.0f}% to {ch.aged344_pct_young.max():.0f}%; lowest: {lo_ch.iloc[0].readout} ({lo_ch.iloc[0].aged344_pct_young:.0f}%), {lo_ch.iloc[1].readout} ({lo_ch.iloc[1].aged344_pct_young:.0f}%)",
    "blocks listed in stats/restoration_chain.csv", "stats/restoration_chain.csv (script 10); Figure 3", "group mean (geometric mean for titres and Ifnb1) divided by the young PSLN-212 mean")
# ---- tolerability
_b = pd.read_csv("/tmp/outputs/analysis/tidy/bodyweight.csv", keep_default_na=False); _b["value"] = pd.to_numeric(_b["value"], errors="coerce")
_pk = _b[_b.block == "S08-D"].groupby(["group", "animal"])["value"].min().reset_index()
P_TOL = stats.ttest_ind(100 - _pk[_pk.group == "PSLN-344"]["value"], 100 - _pk[_pk.group == "Vaccine"]["value"], equal_var=False).pvalue
P_TOL_R848 = stats.ttest_ind(100 - _pk[_pk.group == "PSLN-212/R848"]["value"], 100 - _pk[_pk.group == "Vaccine"]["value"], equal_var=False).pvalue
t344 = bwa("S08-D", "PSLN-344"); tvac = bwa("S08-D", "Vaccine"); t212 = bwa("S08-D", "PSLN-212"); tr848 = bwa("S08-D", "PSLN-212/R848"); tcmp = bwa("S08-D", "CMP-204")
bw10 = pd.read_csv(f"{O}/bodyweight_daily.csv"); r10 = bw10[(bw10.block == "S08-D") & (bw10.day == 10)].set_index("group")
led("1", "Peak weight loss after intranasal dosing, aged, no challenge: PSLN-344, vaccine alone, PSLN-212, CMP-204, PSLN-212/R848", f"{t344.mean_peak_loss_all_pct:.1f}% (worst animal {t344.max_individual_loss_pct:.1f}%), {tvac.mean_peak_loss_all_pct:.1f}%, {t212.mean_peak_loss_all_pct:.1f}%, {tcmp.mean_peak_loss_all_pct:.1f}%, {tr848.mean_peak_loss_all_pct:.1f}% (worst {tr848.max_individual_loss_pct:.1f}%)",
    "S08!B21:AE26", "stats/bodyweight_by_arm.csv (script 06)", f"n = 5; mean of each animal's lowest weight; PSLN-344 vs vaccine alone Welch p = {P_TOL:.3f}")
led("1", "Mean weight on day 10 after dosing: PSLN-344, PSLN-212/R848", f"{r10.loc['PSLN-344','mean']:.1f}% (n = {int(r10.loc['PSLN-344','n_alive'])}), {r10.loc['PSLN-212/R848','mean']:.1f}% (n = {int(r10.loc['PSLN-212/R848','n_alive'])}; one animal has no day-10 value)", "S08!Q26:Z26", "stats/bodyweight_daily.csv (script 06)", "mean of animals with a reading")
cns = {a: (m("S10-A", "PSLN-344", a, a), m("S10-A", "CT", a, a), m("S10-A", "Sham", a, a), m("S10-A", "PBS", a, a)) for a in ["Ifnb1", "Tnf", "Isg15"]}
led("1", "CNS transcripts at 36 h, fold vs untreated: PSLN-344 (cholera-toxin control) for Ifnb1, Tnf, Isg15", "; ".join(f"{a} {v[0]:.1f} ({v[1]:.1f})" for a, v in cns.items()), "S10!A3:N7", OUT_C,
    f"n = 5; PSLN-344 vs PBS, Welch: Ifnb1 p = {fp(pw('S10-A','PBS','PSLN-344','Ifnb1','Ifnb1'))}, Tnf p = {fp(pw('S10-A','PBS','PSLN-344','Tnf','Tnf'))} (Tukey {fp(ptk('S10-A','PBS','PSLN-344','Tnf','Tnf'))}), Isg15 p = {fp(pw('S10-A','PBS','PSLN-344','Isg15','Isg15'))}; PSLN-344 vs vaccine + empty liposome Tnf p = {fp(pw('S10-A','Sham','PSLN-344','Tnf','Tnf'))}")
tnf72 = {g: g9(P72, "Tnf", g) for g in ["PSLN-344", "PSLN-212", "PSLN-212(y)"]}; il672 = {g: g9(P72, "Il6", g) for g in ["PSLN-344", "PSLN-212", "PSLN-212(y)"]}; il1072 = {g: g9(P72, "Il10", g) for g in ["PSLN-344", "PSLN-212", "PSLN-212(y)"]}
tnf16 = {g: g9(P16, "Tnf", g) for g in ["PSLN-344", "PSLN-212", "PSLN-212(y)", "PSLN-R848", "PSLN-212/R848"]}; il1016 = {g: g9(P16, "Il10", g) for g in ["PSLN-344", "PSLN-212", "PSLN-212(y)", "PSLN-R848", "PSLN-212/R848"]}
ifn16_9 = {g: g9(P16, "Ifnb1", g) for g in ["PSLN-344", "PSLN-R848", "PSLN-212/R848"]}
OUT_9 = "stats/S09A_geomean_fold.csv, S09A_contrasts.csv (script 07)"
led("1", "Lung Tnf and Il6 at 72 h, geometric-mean fold vs untreated: PSLN-344 aged; PSLN-212 aged; PSLN-212 young", f"Tnf {tnf72['PSLN-344']:.1f}, {tnf72['PSLN-212']:.1f}, {tnf72['PSLN-212(y)']:.1f}; Il6 {il672['PSLN-344']:.1f}, {il672['PSLN-212']:.1f}, {il672['PSLN-212(y)']:.1f}",
    "S09!Y4:AS4 (Il6), S09!Y8:AS8 (Tnf); panel printed '16h', identified as 72 h (D-02)", OUT_9, f"n = 3; values are log10 in the workbook; PSLN-344 vs young: Tnf p = {fp(c9(P72,'Tnf','PSLN-344','PSLN-212(y)').p_welch_log)}, Il6 p = {fp(c9(P72,'Il6','PSLN-344','PSLN-212(y)').p_welch_log)}")
led("6", "Lung Tnf and Il10 at 16 h, geometric-mean fold: PSLN-344 aged vs PSLN-212 young", f"Tnf {tnf16['PSLN-344']:.0f} vs {tnf16['PSLN-212(y)']:.0f}; Il10 {il1016['PSLN-344']:.1f} vs {il1016['PSLN-212(y)']:.1f}", "S09!B8:V9", OUT_9,
    f"n = 3; Welch on log10 p = {fp(c9(P16,'Tnf','PSLN-344','PSLN-212(y)').p_welch_log)} and {fp(c9(P16,'Il10','PSLN-344','PSLN-212(y)').p_welch_log)}")
# ---- dose response
e344, e212, ecmp = DR.loc["PSLN-344"], DR.loc["PSLN-212"], DR.loc["CMP-204"]
d5 = m("S08-A", "PSLN-344", "", "5"); d20 = m("S08-A", "PSLN-344", "", "20"); d40 = m("S08-A", "PSLN-344", "", "40"); dcombo20 = m("S08-A", "PSLN-344/R848", "", "20")
led("1", "Ifnb1 dose-response, fitted ceiling (Emax) and ED50: PSLN-344 vs PSLN-212", f"Emax {e344.Emax:.0f} (95% CI {e344.Emax_lo:.0f}-{e344.Emax_hi:.0f}) vs {e212.Emax:.0f} ({e212.Emax_lo:.0f}-{e212.Emax_hi:.0f}), ratio {e344.Emax/e212.Emax:.1f}; ED50 {e344.ED50_ug:.0f} ug ({e344.ED50_lo:.0f}-{e344.ED50_hi:.0f}) vs {e212.ED50_ug:.0f} ug ({e212.ED50_lo:.0f}-{e212.ED50_hi:.0f})",
    "S08!B3:M7", "stats/S08A_dose_response_fit.csv (script 07)", "sigmoid Emax model fitted on log10 response, n = 3 per dose, bootstrap CI (2,000 resamples within dose)")
led("1", "Ifnb1 at 5, 20 and 40 ug of PSLN-344; share of the fitted ceiling reached at 20 ug", f"{d5:.1f}, {d20:.1f}, {d40:.1f} (5 ug = {100*d5/d20:.0f}% of the 20-ug response; 40 vs 20 ug ratio {d40/d20:.2f}, p = {e344.p_40_vs_20_welch_log:.2f}); {100*e344.fraction_of_Emax_at_20ug:.0f}% of ceiling", "S08!H4:J4, H6:J7", "stats/S08A_dose_response_fit.csv", "means; Welch on log10 for 40 vs 20 ug")
# ---- antibody
igg = {v: (gm(b, "PSLN-344", p), gm(b, "PSLN-212", p), gm(b, "PSLN-212(Y)", p), gm(b, "CMP-204", p), gm(b, "Sham", p)) for v, b, p in [("H1N1", "S03-A", "IgG CA09 d14"), ("H3N2", "S03-E", "IgG Aichi d14")]}
hai = {v: (gm(b, "PSLN-344", p), gm(b, "PSLN-212", p), gm(b, "PSLN-212(Y)", p)) for v, b, p in [("H1N1", "S03-C", "HAI CA09 d14"), ("H3N2", "S03-G", "HAI Aichi d14")]}
nab = {v: (gm(b, "PSLN-344", p), gm(b, "PSLN-212", p), gm(b, "PSLN-212(Y)", p)) for v, b, p in [("H1N1", "S03-D", "NAb CA09 d14"), ("H3N2", "S03-H", "NAb Aichi d14")]}
hai_min344 = (rng("S03-C", "PSLN-344", "HAI CA09 d14")[0], rng("S03-G", "PSLN-344", "HAI Aichi d14")[0])
hai_rng212 = (rng("S03-C", "PSLN-212", "HAI CA09 d14"), rng("S03-G", "PSLN-212", "HAI Aichi d14"))
led("5", "Serum IgG geometric-mean titre, day 14, one dose: PSLN-344, PSLN-212 (aged), PSLN-212 young; ratio", "; ".join(f"{v}: {th(x[0])}, {th(x[1])}, {th(x[2])}; {x[0]/x[1]:.1f}x" for v, x in igg.items()), "S03!A3:E7; S03!A10:E14", OUT_C,
    f"n = 5; Welch on log10 p = {fp(pw('S03-A','PSLN-212','PSLN-344','IgG CA09 d14','',True))} and {fp(pw('S03-E','PSLN-212','PSLN-344','IgG Aichi d14','',True))}; exact Mann-Whitney p = {fp(pmw('S03-A','PSLN-212','PSLN-344','IgG CA09 d14'))} and {fp(pmw('S03-E','PSLN-212','PSLN-344','IgG Aichi d14'))}")
led("5", "HAI geometric-mean titre, day 14: PSLN-344, PSLN-212 (aged), PSLN-212 young; ratio; lowest PSLN-344 animal", "; ".join(f"{v}: {x[0]:.0f}, {x[1]:.0f}, {x[2]:.0f}; {x[0]/x[1]:.1f}x" for v, x in hai.items()) + f"; lowest PSLN-344 titre {hai_min344[0]:.0f} and {hai_min344[1]:.0f}; PSLN-212 range {hai_rng212[0][0]:.0f}-{hai_rng212[0][1]:.0f} and {hai_rng212[1][0]:.0f}-{hai_rng212[1][1]:.0f}",
    "S03!K3:O7; S03!K10:O14", OUT_C, f"n = 5; printed 0 = below the 1:10 starting dilution, set to 5; Welch on log10 p = {fp(pw('S03-C','PSLN-212','PSLN-344','HAI CA09 d14','',True))} and {fp(pw('S03-G','PSLN-212','PSLN-344','HAI Aichi d14','',True))}")
led("5", "Neutralising geometric-mean titre, day 14: PSLN-344 vs PSLN-212 (aged); ratio", "; ".join(f"{v}: {th(x[0])} vs {th(x[1])}; {x[0]/x[1]:.1f}x" for v, x in nab.items()), "S03!Q3:U7; S03!Q10:U14", OUT_C, f"n = 5; Welch on log10 p = {fp(pw('S03-D','PSLN-212','PSLN-344','NAb CA09 d14','',True))} and {fp(pw('S03-H','PSLN-212','PSLN-344','NAb Aichi d14','',True))}")
# IgG2a/IgG1 recomputed
tid = pd.read_csv("/tmp/outputs/analysis/tidy/continuous.csv", keep_default_na=False); tid["value"] = tid["value"].astype(float)
def vv(block, group): return tid[(tid.block == block) & (tid.group == group)].sort_values("rep")["value"].to_numpy()
ratio = {v: {g: (vv(a, g) / vv(b, g)).mean() for g in ["PSLN-212", "PSLN-344", "PSLN-212(Y)"]} for v, a, b in [("H1N1", "S13-A", "S13-B"), ("H3N2", "S13-C", "S13-D")]}
printed = {v: {g: m(b, g, p) for g in ["PSLN-212", "PSLN-344", "PSLN-212(Y)"]} for v, b, p in [("H1N1", "S03-B", "IgG2a/IgG1 CA09 d14 (as printed)"), ("H3N2", "S03-F", "IgG2a/IgG1 Aichi d14 (as printed)")]}
led("5", "IgG2a/IgG1 ratio recomputed per animal from S13 titres: PSLN-344, PSLN-212 (aged), PSLN-212 young", "; ".join(f"{v}: {x['PSLN-344']:.2f}, {x['PSLN-212']:.2f}, {x['PSLN-212(Y)']:.2f}" for v, x in ratio.items()), "S13!A3:G7 (H1N1); S13!I3:O7 (H3N2)", "integrity/C_derived_quantities.csv (script 02)", "mean of per-animal ratios, n = 5")
led("9", "IgG2a/IgG1 as printed in S03-B and S03-F under the header PSLN-344", f"{printed['H1N1']['PSLN-344']:.2f} and {printed['H3N2']['PSLN-344']:.2f}", "S03!H3:H7; S03!H10:H14", "integrity/C_derived_quantities.csv", "column means; headers permuted (D-01)")
boost = {v: (gm(b, "PSLN-212", p), gm(b, "PSLN-344", p)) for v, b, p in [("H1N1", "S13-I", "IgG CA09 d28 (boost d14)"), ("H3N2", "S13-J", "IgG Aichi d28 (boost d14)")]}
P_BOOST = {v: stats.ttest_ind(np.log10(vv(b1, "PSLN-344")), np.log10(vv(b2, "PSLN-212")), equal_var=False).pvalue for v, b1, b2 in [("H1N1", "S03-A", "S13-I"), ("H3N2", "S03-E", "S13-J")]}
led("8", "IgG geometric-mean titre after a day-14 boost (day 28), aged: PSLN-212 and PSLN-344; vs one dose of PSLN-344 at day 14", "; ".join(f"{v}: {th(boost[v][0])} and {th(boost[v][1])}; one dose PSLN-344 {th(igg[v][0])}" for v in boost), "S13!F53:J57; S13!L53:P57; S03!A3:E7; S03!A10:E14", "stats/special_analyses.txt (script 07, part e)",
    f"n = 5; one dose PSLN-344 vs two doses PSLN-212, Welch on log10: H1N1 p = {fp(P_BOOST['H1N1'])}, H3N2 p = {fp(P_BOOST['H3N2'])}")
# ---- cellular readouts used in text / tables
def two(block, panel="", x="", a="PSLN-344", b="PSLN-212"): return m(block, a, panel, x), m(block, b, panel, x)
mono = two("S01-D", "", "4"); dc = two("S01-E", "", "4"); cdc1 = two("S01-F", "", "72h"); ccr7 = two("S02-A"); agdc = two("S02-C"); xp = two("S02-E"); cd40 = two("S02-D CD40"); cd86 = two("S02-D CD86")
tfh = two("S04-A", "ICOS-high Tfh", "ICOS+"); tfr = two("S04-B Foxp3+ in CXCR5+"); gc = two("S03-K"); treg = two("S04-D"); tfr30 = (m("S04-C", "PSLN-344"), m("S04-C", "PSLN-212"), m("S04-C", "Sham"), m("S04-C", "PSLN-212(Y)"))
ifng14 = two("S05-F"); ifng60 = two("S05-G"); trm = two("S05-I"); gzmb = two("S05-E"); ki67 = two("S05-D"); cd206 = two("S11-E"); am4 = two("S11-A", "", "4")
mac5 = (m("S07-A", "PSLN-212", "", "5"), m("S07-A", "PSLN-344", "", "5"))
spad = (m("S01-C", "WT"), m("S01-C", "SPA/D")); srb = (m("S01-B", "AECII/PSLN-SRB"), m("S01-B", "AECI/PSLN-SRB"), m("S01-B", "AECII/FreeSRB")); cbx = (m("S11-C", "CBX-"), m("S11-C", "CBX+"))
incb = (m("S07-B", "PSLN-344", "CD11b+Ly6C+ monocytes", "Mono"), m("S07-B", "PSLN-344+INCB3344", "CD11b+Ly6C+ monocytes", "Mono")); incb8 = (m("S02-I", "PSLN-344(Y)"), m("S02-I", "PSLN-344(Y)+INCB3344"))
ifnar = (m("S02-H", "WT w/o cDC"), m("S02-H", "IFN w/o cDC"), m("S02-H", "GMCSF")); gmres = (m("S02-G", "PSLN-212"), m("S02-G", "PSLN-212+GM-CSF"), m("S02-G", "GM-CSF"))
ptx = (m("S02-C", "PTX"), m("S02-E", "PTX")); s05c = (m("S05-C", "Lung"), m("S05-C", "Lung+PTX"), m("S05-C", "MLN"), m("S05-C", "MLN+PTX")); s07c = (m("S07-C", "Ly6C-CD206+ MPhi [col B]"), m("S07-C", "Ly6C-CD206+ MPhi [col C]"))
ccl2 = (g9(P16, "Ccl2", "PSLN-344"), g9(P16, "Ccl2", "PSLN-212"), g9(P16, "Ccl2", "PSLN-212(y)"))
ee = {g: (m("S08-B", g), rng("S08-B", g)) for g in ["PSLN-344", "PSLN-212", "CMP-204"]}
def L2(section, label, block, vals, panel="", x="", a="PSLN-344", b="PSLN-212", unit="%", note=""):
    led(section, f"{label}: {a} vs {b}", f"{vals[0]:.1f} vs {vals[1]:.1f}{unit} ({max(vals)/min(vals):.1f}x {'higher' if vals[0] > vals[1] else 'lower'})", f"{cells(block,a,panel,x)}; {cells(block,b,panel,x)}", OUT_C,
        f"n = {nn(block,a,panel,x)}; Welch p = {fp(pw(block,a,b,panel,x))}; exact Mann-Whitney p = {fp(pmw(block,a,b,panel,x))}" + (f"; {note}" if note else ""))
L2("4", "Lung monocytes, day 4", "S01-D", mono, "", "4"); L2("4", "Lung CD11b+ dendritic cells, day 4", "S01-E", dc, "", "4"); L2("4", "CCR7+ migratory CD11b+ DC in lung, 72 h", "S02-A", ccr7)
L2("4", "Antigen-carrying DC in draining node, 36 h", "S02-C", agdc); L2("4", "Ex vivo cross-priming of CD8 T cells by node CD11b+ DC", "S02-E", xp)
L2("5", "CD40+ of node CD11b+ DC", "S02-D CD40", cd40, note=f"young {m('S02-D CD40','PSLN-212(Y)'):.1f}%"); L2("5", "CD86+ of node CD11b+ DC", "S02-D CD86", cd86, note=f"young {m('S02-D CD86','PSLN-212(Y)'):.1f}%")
L2("4", "ICOS-high follicular helper T cells, day 7", "S04-A", tfh, "ICOS-high Tfh", "ICOS+"); L2("4", "Foxp3+ (regulatory) share of follicular T cells, day 7", "S04-B Foxp3+ in CXCR5+", tfr); L2("4", "Germinal-centre B cells, day 7", "S03-K", gc)
L2("4", "Lung regulatory T cells, day 7", "S04-D", treg); L2("4", "IFN-gamma+ CD8 T cells recalled by rgH5N1 antigen, day 14", "S05-F", ifng14); L2("5", "IFN-gamma+ CD8 T cells recalled by rgH5N1 antigen, day 60", "S05-G", ifng60)
L2("4", "Lung resident-memory CD8 T cells, day 25", "S05-I", trm); L2("5", "GZMB+ CD8 T cells in lung, day 3", "S05-E", gzmb); L2("4", "CD206+ macrophages in lung", "S11-E", cd206); L2("5", "Alveolar macrophages, % of lung cells, day 4", "S11-A", am4, "", "4")
led("5", "Foxp3+ share of follicular T cells at day 30: PSLN-344, PSLN-212, sham, young", f"{tfr30[0]:.1f}, {tfr30[1]:.1f}, {tfr30[2]:.1f}, {tfr30[3]:.1f}%", "S04!A22:D26", OUT_C, f"n = 5; PSLN-344 vs sham Welch p = {fp(pw('S04-C','Sham','PSLN-344'))}")
led("4", "Ly6C+CCR2+ macrophages in lung on day 5 (x10^5): PSLN-212 vs PSLN-344", f"{mac5[0]:.0f} vs {mac5[1]:.1f}", "S07!B5:G5", OUT_C, f"n = 3; Welch p = {fp(pw('S07-A','PSLN-212','PSLN-344','','5'))}")
led("4", "Labelled particle in alveolar macrophages: wild-type vs Sftpa1/Sftpd knockout", f"{spad[0]:.0f}% vs {spad[1]:.0f}%", "S01!B20:E21", OUT_C, f"n = 4; Welch p = {fp(pw('S01-C','WT','SPA/D'))}")
led("4", "Tracer-positive alveolar epithelial cells after PSLN-SRB: type II, type I; free tracer type II", f"{srb[0]:.1f}%, {srb[1]:.1f}%, {srb[2]:.1f}%", "S01!B14:F16", OUT_C, f"n = 5; type II particle vs free Welch p = {fp(pw('S01-B','AECII/PSLN-SRB','AECII/FreeSRB'))}")
led("4", "Recruited lung monocytes with PSLN-344, without vs with gap-junction blocker (carbenoxolone)", f"{cbx[0]:.1f}% vs {cbx[1]:.1f}%", "S11!A17:B21", OUT_C, f"n = 5; Welch p = {fp(pw('S11-C','CBX+','CBX-'))}")
led("4", "Lung monocytes with PSLN-344, without vs with CCR2 antagonist", f"{incb[0]:.1f}% vs {incb[1]:.1f}%", "S07!B10:C14", OUT_C, f"n = 5; Welch p = {fp(pw('S07-B','PSLN-344','PSLN-344+INCB3344','CD11b+Ly6C+ monocytes','Mono'))}")
led("4", "GZMB+ CD8 T cells in lung (young, PSLN-344), without vs with CCR2 antagonist", f"{incb8[0]:.1f}% vs {incb8[1]:.1f}%", "S02!H30:I34", OUT_C, f"n = 5; Welch p = {fp(pw('S02-I','PSLN-344(Y)','PSLN-344(Y)+INCB3344'))}")
led("4", "Donor-derived monocyte-derived DC: wild-type donor, IFNAR-deficient donor, IFNAR-deficient donor + GM-CSF", f"{ifnar[0]:.0f}%, {ifnar[1]:.0f}%, {ifnar[2]:.0f}%", "S02!B30:F34", OUT_C, f"n = 5; WT vs IFNAR-deficient Welch p = {fp(pw('S02-H','WT w/o cDC','IFN w/o cDC'))}; rescue vs IFNAR-deficient p = {fp(pw('S02-H','IFN w/o cDC','GMCSF'))}")
led("4", "Monocyte-derived-DC-like cells in lung: PSLN-212, PSLN-212 + recombinant GM-CSF, GM-CSF alone", f"{gmres[0]:.1f}%, {gmres[1]:.1f}%, {gmres[2]:.1f}%", "S02!B22:D26", OUT_C, f"n = 5; Welch p = {fp(pw('S02-G','PSLN-212','PSLN-212+GM-CSF'))}")
led("4", "Pertussis-toxin group: antigen-carrying DC in node; ex vivo CD8 priming", f"{ptx[0]:.1f}%; {ptx[1]:.1f}%", "S02!N3:N7; S02!N10:N14", OUT_C, "n = 5; adjuvant given to this group is not stated (D-15)")
led("4", "Proliferating transferred CD8 T cells: lung without/with pertussis toxin; node without/with", f"{s05c[0]:.0f}% / {s05c[1]:.0f}%; {s05c[2]:.0f}% / {s05c[3]:.0f}%", "S05!A13:D15", OUT_C, f"n = 3; lung p = {fp(pw('S05-C','Lung','Lung+PTX'))}; node p = {fp(pw('S05-C','MLN','MLN+PTX'))}")
led("4", "Lung regulatory T cells after transfer of sorted macrophage subsets (two columns, identical labels)", f"{s07c[0]:.1f}% vs {s07c[1]:.1f}%", "S07!B16:C20", OUT_C, f"n = 5; Welch p = {fp(pw('S07-C','Ly6C-CD206+ MPhi [col B]','Ly6C-CD206+ MPhi [col C]'))}; direction not attributable (D-12)")
led("4", "Lung Ccl2 at 16 h, geometric-mean fold: PSLN-344 aged, PSLN-212 aged, PSLN-212 young", f"{ccl2[0]:.0f}, {ccl2[1]:.1f}, {ccl2[2]:.0f}", "S09!B5:V5", OUT_9, f"n = 3; PSLN-344 vs PSLN-212 Welch on log10 p = {fp(c9(P16,'Ccl2','PSLN-344','PSLN-212').p_welch_log)}")
led("8", "Ifnb1 at 16 h for the alternatives (aged): CMP-204, PSLN-R848, PSLN-212/R848; young PSLN-344 vs young PSLN-212", f"{icmp:.1f}, {ir848:.1f}, {icombo:.1f}; {i344y:.1f} vs {iy:.1f} ({i344y/iy:.2f}x)", "S01!B4:F4, B6:F7, B9:F10", OUT_C + "; stats/special_analyses.txt part f", f"n = 5; young PSLN-344 vs PSLN-212 Welch p = {fp(pw('S01-A','PSLN-344(Y)','PSLN-212(Y)','Ifnb1 16h','16h'))}")
led("8", "Lung Tnf and Il10 at 16 h, geometric-mean fold: PSLN-R848, PSLN-212/R848, PSLN-344", f"Tnf {tnf16['PSLN-R848']:.0f}, {tnf16['PSLN-212/R848']:.0f}, {tnf16['PSLN-344']:.0f}; Il10 {il1016['PSLN-R848']:.0f}, {il1016['PSLN-212/R848']:.0f}, {il1016['PSLN-344']:.1f}", "S09!K8:S9", OUT_9, "n = 3; all R848 vs PSLN-344 contrasts p < 0.05 (Welch on log10)")
tnf_ifn = {g: g9(P16, "Tnf", g) / g9(P16, "Ifnb1", g) for g in ["PSLN-344", "PSLN-R848", "PSLN-212/R848"]}
led("2", "Tnf-to-Ifnb1 fold ratio at 16 h: PSLN-344, PSLN-212/R848, PSLN-R848", f"{tnf_ifn['PSLN-344']:.1f}, {tnf_ifn['PSLN-212/R848']:.1f}, {tnf_ifn['PSLN-R848']:.0f}", "S09!K3:S3, K8:S8", OUT_9, "ratio of geometric-mean folds")
led("8", "Ifnb1 at 20 ug: 'PSLN-344/R848' vs PSLN-344", f"{dcombo20:.1f} vs {d20:.1f}", "S08!H6:M6", "stats/special_analyses.txt (script 07, part a)", "n = 3")
led("8", "CMP-204 (cGAMP liposome) in aged animals: survival after matched-strain challenge; day-14 IgG GMT (H1N1)", f"{frac(cmp_surv)}; {th(igg['H1N1'][3])}", "S03!C24:C30; S03!B3:B7", OUT_ARM + "; " + OUT_C, "counts; geometric mean, n = 5")
led("2", "Encapsulation efficiency: PSLN-344, PSLN-212, CMP-204", "; ".join(f"{g} {v[0]:.1f}% ({v[1][0]:.1f}-{v[1][1]:.1f})" for g, v in ee.items()), "S08!A11:O11", OUT_C, "mean (range), 3 preparations")
pw12 = power("PSLN-344 vs PSLN-212, pooled observed", 12); pw12w = power("PSLN-344 vs PSLN-212, worst-case", 12); pw40c = power("PSLN-344 vs an active comparator", 40); pw40d = power("durability: d14 95% vs d60 67%", 40); pw7 = None
led("2", "Power of a two-arm survival comparison at 12 per arm: 85% vs 14%; 83% vs 18%", f"{100*pw12:.0f}%; {100*pw12w:.0f}%", "effect sizes from the pooled survival analysis", "stats/power_table.csv (script 08)", "two-sided Fisher exact at 0.05, exact enumeration")
led("2", "Power at 40 per arm: 85% vs 50% (active comparator); 95% vs 67% (durability)", f"{100*pw40c:.0f}%; {100*pw40d:.0f}%", "assumed comparator rate; observed day-14 and day-60 rates", "stats/power_table.csv", "as above")
# post-challenge illness
loss344 = BWA[(BWA.group == "PSLN-344") & BWA.block.isin(["S13-F", "S13-G", "S15-A", "S15-B", "S15-C", "S15-E", "S15-F", "S15-G", "S15-O"])]["mean_peak_loss_survivors_pct"]
lossy = BWA[(BWA.group == "PSLN-212(Y)") & BWA.block.isin(["S13-F", "S15-A", "S15-B", "S15-C", "S15-E", "S15-F", "S15-G", "S15-O"])]["mean_peak_loss_survivors_pct"]
led("6", "Peak weight loss after challenge among survivors, range of arm means: PSLN-344 aged; PSLN-212 young", f"{loss344.min():.0f} to {loss344.max():.0f}%; {lossy.min():.0f} to {lossy.max():.0f}%", "S13-F, S13-G, S15-A to S15-G, S15-O", "stats/bodyweight_by_arm.csv (script 06)", "per-animal lowest weight while alive; arms with duplicated series (S15-D, S15-I, S15-M) left out")
nfind = len(IL.LOG); nA = sum(1 for r in IL.LOG if r[1] == "A")
led("9", "Data-integrity findings logged; of which change a conclusion if the workbook is read as printed", f"{nfind}; {nA}", "see Appendix D", "integrity/integrity_report.txt (script 02); integrity_log.py", "curated from automated checks")
led("9", "S11-B values identical in position to S11-A", "35 of 100; group-by-day means r = 0.997", "S11!B3:U7 vs S11!B10:U14", "stats/special_analyses.txt (script 07, part c)", "cell-by-cell comparison")
led("9", "S09-A Ifnb1 values (back-transformed) found in S01-A: first panel in the 16-h values; second panel in the 72-h values", "21 of 21; 21 of 21", "S09!B3:V3, Y3:AS3 vs S01!B3:F9, H3:L9", "integrity/C_derived_quantities.csv (script 02)", "10^x matched to within rounding")

print("ledger rows so far:", len(LEDGER))

# =====================================================================================================
# HTML BUILDING BLOCKS
# =====================================================================================================
import html as _html
def T(s):
    s = _html.escape(str(s), quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\*\w])\*(?!\*)(.+?)(?<!\*)\*(?![\*\w])", r"<em>\1</em>", s)
    return s
def P(s): return f"<p>{T(s)}</p>\n"
def H(n, s): return f"<h{n}>{T(s)}</h{n}>\n"
def UL(items): return "<ul>\n" + "".join(f"<li>{T(i)}</li>\n" for i in items) + "</ul>\n"
def OL(items): return "<ol>\n" + "".join(f"<li>{T(i)}</li>\n" for i in items) + "</ol>\n"
def CELL(c):
    if isinstance(c, (list, tuple)):
        return "".join(f"<p>{T(i)}</p>" for i in c)
    return T(c)
def TABLE(headers, rows, widths, caption=None):
    tot = sum(widths); o = "<table>\n"
    if caption: o += f"<caption>{T(caption)}</caption>\n"
    o += "<colgroup>" + "".join(f'<col style="width: {100*w/tot:.1f}%" />' for w in widths) + "</colgroup>\n"
    o += "<thead><tr>" + "".join(f"<th>{T(h)}</th>" for h in headers) + "</tr></thead>\n<tbody>\n"
    for r in rows: o += "<tr>" + "".join(f"<td>{CELL(c)}</td>" for c in r) + "</tr>\n"
    return o + "</tbody></table>\n"
def FIG(fname, caption, width="16.6cm"):
    return f'<figure><img src="/tmp/outputs/figures/{fname}" width="{width}" /><figcaption>{T(caption)}</figcaption></figure>\n'
PB = '<div class="pagebreak"></div>\n'
EXT = "*(external)*"

# convenient strings
s344, s212, ssham = pT2.psln344, pT2.comparator_surv, pTs.comparator_surv
pc344, pc212, pcsham = f"{pT2.psln344_pct:.0f}%", f"{pT2.comparator_pct:.0f}%", f"{pTs.comparator_pct:.0f}%"
rd = f"{pT2.mh_risk_diff_pct:.0f}"
cnsI, cnsT, cnsG = cns["Ifnb1"], cns["Tnf"], cns["Isg15"]
n_links = 5

doc = []
A_ = doc.append
# ----------------------------------------------------------------------------------------------------- title
A_(P("For the Portfolio Review Committee · 1 November 2026"))
A_(P("*How to read this.* Square brackets give the workbook block behind each number; Appendix B lists the cells, the analysis output and the test for every number I rely on. "
     f"Statements that come from general knowledge rather than from our data are marked {EXT}. “Aged” means 20 months or older unless stated."))

# ----------------------------------------------------------------------------------------------------- 1
A_(H(1, "1. Recommendation"))
A_(P("**Keep PSLN-344, on a gated budget.**"))
A_(P("Approve one gate of work now: reconciling the data package to raw records, plus three studies (human cells, a blinded aged-mouse repeat with the missing controls, and intranasal safety). "
     "Hold IND-enabling spend until that gate is passed. "
     f"The use our data support is an intranasal adjuvant for inactivated influenza vaccine in older adults. They do not support a stand-alone drug: PSLN-344 given without vaccine protected {frac(alone)} animals [S15-H]."))
_young_ref = frac(sumk(["S03-I", "S06-A", "S06-B", "S06-C", "S06-D", "S06-E", "S06-F", "S06-G", "S15-L", "S15-N"], "PSLN-212(Y)"))
A_(P("The case rests on four findings."))
A_(UL([
    f"**It largely restores vaccine protection in aged animals.** Across the 13 lethal-challenge experiments that compared the two formulations in animals aged 14 months or more, vaccine with PSLN-344 protected {s344} ({pc344}). The same vaccine with PSLN-212, which is the same liposome and the same STING agonist (CDN-1807) without manganese, protected {s212} ({pc212}). "
    f"Vaccine with empty liposome, or vaccine alone, protected {ssham} ({pcsham}). For reference, young animals given PSLN-212 survived {_young_ref} in the ten experiments that included them [S03-I, S03-J, S06-A to S06-G, S06-E and S06-F second blocks, S15-H, S15-L, S15-N; Figure 2].",
    f"**That result survives the harshest readings of the workbook I could construct.** Taking the less favourable of the survival record and the body-weight record for every arm gives {pW2.psln344} against {pW2.comparator_surv}. "
    f"Discarding every experiment that carries a data-integrity flag gives {sNF2.psln344} against {sNF2.comparator_surv}.",
    f"**Durability is the weakest efficacy result.** When challenge came 60 days after the dose, {frac(d60_344)} ({pct(*d60_344)}) survived, against {frac(d14_344)} at 14 days (Fisher p = {p_d14_d60:.3f}) [S06-E to S06-G; S03-I, S06-A, S06-C].",
    f"**Everything is in mice, and the data package needs repair.** There are no human-cell, second-species, licensed-comparator, viral-load or manganese-distribution data. "
    f"The workbook has {nfind} inconsistencies, {nA} of which change a conclusion if it is read as printed (Section 9). None reverses the headline result, but they must be reconciled to raw records before this package goes outside the company.",
]))
A_(H(2, "How the asset looks"))
A_(TABLE(["Dimension", "Reading", "Basis in our data"], [
    ["Protection in aged hosts", "Strong", f"Survival {pc344} with PSLN-344, {pc212} with PSLN-212, {pcsham} with vaccine and empty liposome or vaccine alone; a {rd}-point difference over PSLN-212 (stratified by experiment, p < 10⁻²⁰); same picture in every subset examined (Figure 2, Section 6.1)"],
    ["Breadth", "Strong; two items unverified", f"Matched strain {frac(hom)} [S03-I]; a subtype absent from the vaccine {frac(het14)} at day 14 [S06-A, S06-C]; challenge 2 to 3 days after one dose {frac(early)}, including wild-type H5N1 {frac(h5)} [S03-J, S06-B, S06-D, S15-H]; "
                          f"two other mouse strains {frac(strain)} [S15-L, S15-N]; 14-month animals with or without prior influenza infection {frac(imp344)} [S06-E and S06-F, second blocks]. "
                          "Unverified: the C57BL/6 half of the strain result and the identity of the H5N1 comparator arms (Section 9)"],
    ["Mechanism", "Good, with two attribution gaps", f"Five links tested by knockout or inhibitor (Section 4). Manganese lifts the lung interferon-β transcript (*Ifnb1*) from {100*i212/iy:.0f}% to {100*i344/iy:.0f}% of the young response [S01-A] and switches on *Gm-csf* ({f1(g16_344)}-fold vs {f1(g16_212)}-fold) [S02-F]. No STING-deficient control; no particle carrying manganese alone"],
    ["Durability", "Uncertain", f"{frac(d60_344)} at day 60 vs {frac(d14_344)} at day 14. The animals that died had lost 15 to 23% of body weight, so these were infection deaths, not old-age deaths [S15-E to S15-G]"],
    ["Safety and tolerability", "Acceptable so far; thin", f"Peak weight loss after dosing {t344.mean_peak_loss_all_pct:.1f}% (vaccine alone {tvac.mean_peak_loss_all_pct:.1f}%), recovered by day 10 [S08-D]. Three central-nervous-system (CNS) transcripts {cnsG[0]:.1f} to {cnsT[0]:.1f} times baseline (cholera-toxin control {cnsG[1]:.1f} to {cnsI[1]:.1f}) [S10-A]. "
                                                          f"No histology, no manganese dose or distribution, no valid neutrophil data; lung *Tnf* still {tnf72['PSLN-344']:.1f} times baseline at 72 hours [S09-A]"],
    ["Dose", "One level tested for protection", f"20 µg gives {100*e344.fraction_of_Emax_at_20ug:.0f}% of the fitted *Ifnb1* ceiling; 40 µg adds {100*(d40/d20-1):.0f}% (p = {e344.p_40_vs_20_welch_log:.2f}) [S08-A]. No protection data below 20 µg"],
    ["Human translatability", "Unknown", f"No human-cell or second-species data. The mechanism runs through alveolar macrophages and alveolar epithelium [S01-B, S01-C]; an intranasal dose reaches the deep lung in a mouse, whereas a human nasal spray deposits mainly in the nose {EXT}"],
    ["Manufacturing", "Early", f"Encapsulation efficiency {ee['PSLN-344'][0]:.1f}% ({ee['PSLN-344'][1][0]:.1f} to {ee['PSLN-344'][1][1]:.1f}%, three preparations) [S08-B]; two preparation methods in use; lyophilisate stored at −20 °C; manganese content not reported"],
    ["Data package", "Needs reconciliation", f"{nfind} findings; {nA} change a conclusion if read as printed (Section 9, Appendix D)"],
    ["Position against standard of care", "Unknown", "No licensed vaccine or adjuvant was used as a comparator in any experiment"],
], [20, 17, 63]))
A_(P("Section 7 sets out what dropping the asset would forgo and what it would avoid."))
A_(H(2, "What would change this recommendation"))
A_(P("I would drop the asset at the gate if any one of these happens:"))
A_(UL([
    "raw records do not substantiate the survival advantage, or the data series that recur across blocks turn out to mean that fewer independent experiments were run than the workbook shows;",
    "in cells from older human donors, CDN-1807 with manganese shows no gain over CDN-1807 alone, or it is inactive on a common human STING variant;",
    "in the blinded repeat, the survival advantage over PSLN-212 is under 30 points, or a particle carrying manganese alone does as well as PSLN-344;",
    "manganese accumulates in the brain, or brain inflammation appears, at up to three times the efficacious dose.",
]))
A_(P(f"My confidence that PSLN-344 outperforms PSLN-212 in aged mice is high. My confidence that this translates to older people is low until the human-cell study and a second species have read out; that is why the recommendation is a gate and not a go."))

# ----------------------------------------------------------------------------------------------------- 2
A_(H(1, "2. Next steps: what each study has to establish, and the endpoints we need to see"))
A_(P("The order matters. Step 0 and Study 1 are inexpensive and can end the programme early. Study 2 is the costly one and should not start until Step 0 is complete, because Study 2 is where any block that cannot be reconciled gets repeated. "
     "Thresholds are anchored to what the current data show; the current value is given in brackets after each."))
A_(H(2, "Gate 1: proposed for approval now"))
A_(TABLE(["Step", "What it has to establish", "Endpoints we need to see", "Stop or rethink if"], [
    ["**Step 0. Reconcile the data package to raw records** (no new experiments)",
     "That the blocks this case rests on match instrument exports and animal logs, and that the headline results survive the check.",
     [f"Each of the {nfind} findings in Appendix D closed as corrected, explained or unrecoverable.",
      f"Survivors per arm re-derived from animal logs for the 13 challenge experiments in aged animals: pooled survival at least 75% with PSLN-344 and at most 25% with PSLN-212 (now {pc344} and {pc212}; worst reading {pW2.psln344_pct:.0f}% and {pW2.comparator_pct:.0f}%).",
      f"Day-14 IgG geometric-mean titre at least 10 times PSLN-212 (now {igg['H1N1'][0]/igg['H1N1'][1]:.1f} and {igg['H3N2'][0]/igg['H3N2'][1]:.1f} times) [S03-A, S03-E]; 16-hour *Ifnb1* at least 2 times PSLN-212 (now {i344/i212:.1f} times) [S01-A].",
      "The manganese content per dose, and whether “20 µg” means CDN or total particle, documented."],
     "Raw records cannot substantiate the survival advantage, or fewer independent experiments exist than the workbook implies."],
    ["**Study 1. Human cells**",
     "That CDN-1807 with manganese activates human STING, including its common variants; that the manganese-dependent gain seen in aged mouse lung also appears in cells from older people; that hand-over from macrophage to epithelium works in human cells.",
     [f"Interferon-β and CXCL10 induction in macrophages from donors aged 65 or over, with donors aged 18 to 40 as reference: maximum response to PSLN-344 at least 2 times PSLN-212 (mouse: {i344/i212:.1f} times at the efficacy dose [S01-A]; {e344.Emax/e212.Emax:.1f} times at the fitted ceiling [S08-A]).",
      f"Response lost in STING-knockout cells (at least 90% reduction) and kept (at least 50% of the reference maximum) on each common human STING variant, such as H232 and HAQ {EXT}.",
      f"GM-CSF induction at least 3 times PSLN-212 in macrophage–epithelial co-culture, reduced by a gap-junction blocker (mouse: {g16_344/g16_212:.1f} to {g36_344/g36_212:.1f} times [S02-F]; blocker effect [S11-C]).",
      f"TNF no more dominant than in aged mice: TNF-to-interferon-β fold ratio of 2 or less (PSLN-344 in aged mice {tnf_ifn['PSLN-344']:.1f}; the R848 formulations {tnf_ifn['PSLN-212/R848']:.0f} and {tnf_ifn['PSLN-R848']:.0f}) [S09-A]."],
     "No manganese-dependent gain in older-donor cells; inactive on a common human variant; a TNF- or IL-10-dominated profile."],
    ["**Study 2. Confirmatory aged-mouse study**: blinded, pre-registered, both sexes, commercial split antigen, with the controls the dataset lacks",
     "That the survival advantage reproduces under blinded conditions; what the CDN, the manganese and STING each contribute; the lowest protective dose; whether it lowers virus in the lung.",
     ["Arms: vaccine with empty liposome; particle with manganese only; PSLN-212; PSLN-344 at 5, 10 and 20 µg; PSLN-344 with STING removed (STING-deficient young animals, or a STING inhibitor in aged animals, since aged knockouts are unlikely to be obtainable).",
      f"Primary: 14-day survival after challenge with a subtype absent from the vaccine, 14 days after one dose. PSLN-344 at least 80% and at least 50 points above PSLN-212. Twelve animals per arm (six of each sex) give {100*pw12:.0f}% power at the rates seen so far ({pc344} vs {pc212}) and {100*pw12w:.0f}% at the worst reading.",
      "Lung virus 3 and 6 days after challenge at least 100-fold below the empty-liposome arm (no viral-load data exist today).",
      f"Haemagglutination-inhibition (HAI) geometric-mean titre at least 8 times PSLN-212 (now {hai['H1N1'][0]/hai['H1N1'][1]:.1f} and {hai['H3N2'][0]/hai['H3N2'][1]:.1f} times) [S03-C, S03-G]; IFN-γ-producing CD8 T cells recalled by a non-vaccine subtype at least 3 times PSLN-212 (now {ifng14[0]/ifng14[1]:.1f} times) [S05-F]; IgA in nasal wash and lung lavage measured (absent today).",
      f"Attribution: PSLN-344 better than the manganese-only particle on survival and *Ifnb1*; *Ifnb1* induction and protection lost without STING.",
      f"Dose: the lowest dose with at least 80% survival (*Ifnb1* at 5 µg is {100*d5/d20:.0f}% of the 20-µg response [S08-A]).",
      f"Tolerability: peak weight loss of 5% or less (now {t344.mean_peak_loss_all_pct:.1f}%; worst animal {t344.max_individual_loss_pct:.1f}%) [S08-D]; lung neutrophils and histology at 1, 3 and 7 days; lung *Tnf* and *Il6* at most 2 times baseline by day 7 (now {tnf72['PSLN-344']:.1f} and {il672['PSLN-344']:.1f} times at 72 hours) [S09-A].",
      "Every animal bled before challenge, so that antibody and T-cell readouts can be tested against each animal’s own outcome."],
     "Survival advantage under 30 points; the manganese-only particle does as well; no dose below 20 µg protects and 20 µg fails on tolerability."],
    ["**Study 2, second wave.** Comparator and durability arms, started once the primary endpoint has read out",
     "Whether PSLN-344 matches or beats a licensed-type vaccine, and how long protection lasts.",
     [f"Against an intramuscular licensed-type enhanced vaccine: no worse on matched-strain survival and better on cross-subtype survival. Forty per arm are needed for {100*pw40c:.0f}% power if the comparator protects half the animals.",
      f"Durability: challenge at day 60 and day 120 alongside vaccinated, unchallenged controls (today {frac(d60_344)} at day 60 against {frac(d14_344)} at day 14). Forty per arm give {100*pw40d:.0f}% power to detect a fall from 95% to 67%."],
     "Worse than the comparator on matched-strain protection; protection at day 120 no better than PSLN-212."],
    ["**Study 3. Intranasal safety and manganese disposition** (pilot, aged animals, both sexes, single and repeat dose)",
     f"That a manganese-containing STING agonist given by the nose does not reach or inflame the brain and does not leave lasting airway injury, with a margin over the efficacious dose. Inhaled or intranasal manganese can travel along the olfactory nerve to the brain {EXT}; our only CNS data are three transcripts at one timepoint.",
     ["Manganese in olfactory bulb, brain, lung, liver and blood at 6 hours, 24 hours, 7 days and 28 days after one and three doses, at 1, 3 and 10 times the efficacious dose: no rise above vehicle in brain at the efficacious dose; back to baseline by day 28 at every dose.",
      f"Brain *Ifnb1*, *Tnf*, *Isg15* (plus *Il6*, *Il1b*) at 6 hours, 36 hours and 7 days: under 2 times the PBS group at the efficacious dose (now {cnsI[0]:.1f}, {cnsT[0]:.1f} and {cnsG[0]:.1f} times in CNS tissue at 36 hours; cholera toxin {cnsI[1]:.1f}, {cnsT[1]:.1f} and {cnsG[1]:.1f}) [S10-A].",
      "Histology of nasal cavity, olfactory epithelium and bulb, and lung; lavage neutrophils, protein and LDH.",
      f"Alveolar macrophages not depleted (now {am4[0]:.0f}% of lung cells on day 4 with manganese and {am4[1]:.0f}% without) [S11-A].",
      "A no-adverse-effect level at least 3 times the efficacious dose."],
     "Manganese accumulation in brain, or brain inflammation, at up to 3 times the efficacious dose; airway pathology that persists."],
], [17, 22, 43, 18]))
A_(P("Gate 1 is passed only if Step 0, Study 1, the core of Study 2 and Study 3 meet their endpoints; the second wave of Study 2 can report into Gate 2. A failure on any stop criterion ends the programme or sends it back to formulation."))
A_(P("*Planning assumptions (mine, not from the data):* Step 0 four to six weeks; Study 1 about three months; Study 3 three to four months; Study 2 five to seven months, limited by the supply of 18- to 20-month-old mice. "
     "The second wave of Study 2 needs about forty aged animals per arm, which makes it the largest single cost in this plan; it starts only after the primary endpoint has read out."))
A_(H(2, "Gate 2: only if Gate 1 is passed"))
A_(TABLE(["Step", "What it has to establish", "Endpoints we need to see"], [
    ["**Study 4. Second species with a clinical-type device** (ferret)",
     f"Whether protection needs deep-lung delivery, and whether CDN-1807 with manganese works outside the mouse in vivo. This decides the product: a nasal spray or an inhaled vaccine.",
     ["Nasal-spray and aerosol arms, each against unadjuvanted vaccine.",
      "Virus in nasal wash over the course of infection at least 100-fold below unadjuvanted vaccine; fever and weight loss; HAI and neutralising seroconversion; T-cell recall. Older ferrets if obtainable.",
      "If only the aerosol arm works, redo the target product profile and the market estimate before further spend."]],
    ["**Study 5. Manufacturing lock**",
     f"One process that is reproducible and stable at refrigerator temperature. Today: encapsulation {ee['PSLN-344'][0]:.1f}% across three preparations [S08-B], two preparation methods, storage at −20 °C, manganese content not reported.",
     ["Three consecutive batches within specification for CDN and manganese content, encapsulation, particle size and spread, surface charge and endotoxin.",
      "A potency assay with acceptance limits; at least 90% potency after six months at 2 to 8 °C.",
      "Haemagglutinin potency of the partner antigen unchanged after mixing."]],
    ["**Antigen partner and regulatory route**",
     f"PSLN-344 does nothing without antigen [S15-H], and an adjuvant is licensed as part of a vaccine, not on its own {EXT}. The programme needs an inactivated-antigen source suitable for airway delivery and an agreed route to first-in-human.",
     ["A named antigen partner or supply agreement.", "Regulatory scientific advice on the non-clinical package for an intranasal, manganese-containing adjuvant."]],
], [20, 36, 44]))

# ----------------------------------------------------------------------------------------------------- 3
A_(H(1, "3. Target population for the market check"))
A_(P("**Primary population: adults aged 65 and over who are eligible for annual influenza vaccination.** The data point there for four reasons."))
A_(UL([
    f"**The gain from manganese is specific to old hosts.** In aged animals PSLN-344 protected {pc344} and PSLN-212 {pc212}. In young animals both protected {frac(young['S09-B'][0])} in each of three challenge models, one of them 180 days after the dose [S09-B, S09-D, S09-F], "
    f"and manganese added {i344y/iy:.2f} times the *Ifnb1* response with no consistent gain in dendritic-cell readouts [S01-A, S01-E to S01-G, S02-C, S02-E].",
    f"**It works in hosts with prior influenza immunity.** In 14-month animals that had recovered from an earlier influenza infection, PSLN-344 protected {frac(impr_344)} and PSLN-212 {frac(impr_212)} [S06-E and S06-F, second blocks]. Every older adult has such a history.",
    f"**One dose acts within days and across subtypes.** Protection was {frac(early)} when challenge came 2 to 3 days after a single dose, and {frac(het14)} against a subtype absent from the vaccine [S03-J, S06-A to S06-D, S15-H]. Those features matter most in mismatch seasons and outbreaks.",
    f"**The deficit it corrects is already present by middle age in mice.** At 14 months, animals with no prior infection were protected {frac(naive14_344)} by PSLN-344 and {frac(naive14_212)} by PSLN-212 [S06-E and S06-F, second blocks].",
]))
A_(TABLE(["Segment", "Definition", "Support in our data", "What market research should size"], [
    ["Primary", "Adults 65 and over, annual influenza vaccination", f"Aged mice (20 months or more): {frac(k20_344)} vs {frac(k20_212)} survival. Twenty-month mice are conventionally taken to model people in their sixties {EXT}",
     ["People in the age band, by launch geography.", "Annual vaccination uptake in the band.", f"Share already receiving enhanced vaccines (high-dose, adjuvanted or recombinant), which is the share we would have to displace {EXT}."]],
    ["Secondary", "Adults 50 to 64", f"14-month mice without prior infection: {frac(naive14_344)} vs {frac(naive14_212)}. One pair of experiments; weaker support",
     ["Same three quantities for this band.", "Whether payers treat this band as needing an enhanced vaccine."]],
    ["Separate", "Pandemic and pre-pandemic preparedness (H5N1), procured by governments", f"Wild-type H5N1 challenge 2 days after one dose: {frac(h5)} vs {frac(h5s)} and {frac(h5p)} in the two comparator arms [S03-J]. Single experiment; comparator labels inconsistent (Section 9)",
     ["Stockpile procurement, sized separately from seasonal use."]],
], [12, 20, 36, 32]))
A_(P(f"*Unit assumption for sizing:* one intranasal dose per person per season, given together with the seasonal antigen. Every protection experiment used a single dose; a second dose two weeks later raised IgG a further {boost['H1N1'][1]/igg['H1N1'][0]:.1f} and {boost['H3N2'][1]/igg['H3N2'][0]:.1f} times [S03-A, S03-E, S13-I, S13-J]."))
A_(P("Four things cut the addressable population, and market research should size each."))
A_(UL([
    "**Route.** Ability and willingness of people over 65 to take an intranasal or inhaled vaccine, and which of the two the product turns out to be (Study 4).",
    "**Likely exclusions.** The mechanism is deliberate innate activation in the lung. Chronic lung disease and immunosuppression are the probable early exclusions (my judgement; there are no data in such models), and both are common over 65.",
    "**Sex.** Every animal in the dataset is female. Nothing supports or contradicts an equal effect in males.",
    "**Antigen partner.** The addressable market is that of the partnered vaccine, not of the adjuvant alone.",
]))
A_(P("I have not put a number on the market. Nothing in the dataset bears on its size, and any figure I supplied would come from outside the data you asked me to rely on."))

# ----------------------------------------------------------------------------------------------------- 4
A_(H(1, "4. Mechanism of action, built from our data"))
A_(P("PSLN-344 has three working parts: CDN-1807, a cyclic-dinucleotide (CDN) agonist of STING; manganese (Mn²⁺); and a liposome that mimics lung surfactant. PSLN-212 is the same liposome and the same CDN without manganese. "
     "Whatever PSLN-344 gains over PSLN-212 in aged animals therefore traces to the manganese, or to what incorporating it does to the particle."))
A_(P(f"In one sentence: the particle is taken up by alveolar macrophages, its cargo is passed to the alveolar epithelium, and manganese raises the resulting interferon signal to the level a young lung produces and switches on GM-CSF; those signals recruit monocytes and turn them into dendritic cells instead of macrophages, and those dendritic cells carry antigen to the lymph node and prime antibody and CD8 T-cell responses. "
     f"Without manganese, the aged lung produces {100*i212/iy:.0f}% of the young interferon signal and almost no GM-CSF signal ({f1(g16_212)}-fold, against {f1(g16_sh)}-fold for sham), and the chain stalls at the monocyte step."))
A_(FIG("fig1_mechanism_of_action.png", "Figure 1. Mechanism of action assembled from the dataset. Each box gives the numbers and the source block. Green tags mark links tested by removing or blocking them; grey tags mark links supported only by comparing formulations. The red box lists links the data do not yet show."))
A_(TABLE(["Link", "What the data show", "How it was tested", "Strength"], [
    ["1. Uptake by alveolar macrophages", f"Labelled particle of PSLN-344 composition in {spad[0]:.0f}% of alveolar macrophages in wild-type mice and {spad[1]:.0f}% in mice lacking surfactant proteins A and D [S01-C]", "Knockout", "Tested; n = 4, young animals"],
    ["2. Hand-over to alveolar epithelium", f"Tracer in {srb[0]:.1f}% of type II and {srb[1]:.1f}% of type I epithelial cells, against {srb[2]:.1f}% for free tracer [S01-B]. A gap-junction blocker cut monocyte influx after PSLN-344 from {cbx[0]:.1f}% to {cbx[1]:.1f}% [S11-C]",
     "Tracer; inhibitor", "Tracer hand-over shown for the particle without manganese; the blocker test used PSLN-344. For PSLN-344 itself the tracer block has unresolved column labels [S08-C]"],
    ["3. Interferon and GM-CSF signal, raised by manganese", f"*Ifnb1* {f1(i344)}-fold with manganese, {f1(i212)}-fold without, {f1(iy)}-fold in young animals [S01-A]. Ceiling of the dose-response {e344.Emax:.0f}-fold vs {e212.Emax:.0f}-fold at a similar half-maximal dose ({e344.ED50_ug:.0f} vs {e212.ED50_ug:.0f} µg) [S08-A]. "
                                                             f"*Gm-csf* {f1(g16_344)}-fold vs {f1(g16_212)}-fold at 16 hours [S02-F]. *Ccl2* {ccl2[0]:.0f}-fold vs {ccl2[1]:.1f}-fold [S09-A]",
     "Formulation comparison", "Consistent across blocks. Not shown to depend on STING; the contribution of manganese alone is unknown"],
    ["4. Monocyte recruitment", f"Lung monocytes on day 4: {mono[0]:.0f}% vs {mono[1]:.0f}% [S01-D]. A CCR2 antagonist cut them from {incb[0]:.1f}% to {incb[1]:.1f}% [S07-B]. Recruitment was not significantly reduced when the recruited cells lacked the interferon receptor ({m('S12-A','WT to WT'):.0f}% vs {m('S12-A','IFNAR-/- to WT'):.0f}%, p = {fp(pw('S12-A','WT to WT','IFNAR-/- to WT'))}, n = 3, young animals) [S12-A]", "Inhibitor", "Tested"],
    ["5. Monocytes become dendritic cells", f"CD11b⁺ dendritic cells on day 4: {dc[0]:.0f}% vs {dc[1]:.0f}% [S01-E]. Donor cells lacking the type-I interferon receptor: {ifnar[1]:.0f}% vs {ifnar[0]:.0f}% for wild-type, restored to {ifnar[2]:.0f}% by GM-CSF [S02-H]. "
                                            f"Adding recombinant GM-CSF to PSLN-212 raised these cells from {gmres[0]:.1f}% to {gmres[1]:.1f}% [S02-G]", "Knockout and rescue", "Tested; the strongest link in the chain"],
    ["6. Migration to the lymph node and priming", f"CCR7⁺ migratory dendritic cells {ccr7[0]:.0f}% vs {ccr7[1]:.0f}% [S02-A]; antigen-carrying dendritic cells in the node {agdc[0]:.1f}% vs {agdc[1]:.1f}%, and {ptx[0]:.1f}% in the pertussis-toxin group [S02-C]; "
                                                    f"CD8 priming ex vivo {xp[0]:.0f}% vs {xp[1]:.1f}% [S02-E]. Pertussis toxin left T-cell proliferation in the lung unchanged ({s05c[0]:.0f}% vs {s05c[1]:.0f}%) and cut it in the node from {s05c[2]:.0f}% to {s05c[3]:.0f}% [S05-C, n = 3]", "Inhibitor", "Tested. Co-stimulatory markers recover least (CD40 {:.0f}%, CD86 {:.0f}% of young) [S02-D]".format(100*cd40[0]/m('S02-D CD40','PSLN-212(Y)'), 100*cd86[0]/m('S02-D CD86','PSLN-212(Y)'))],
    ["7a. Antibody arm", f"ICOS-high follicular helper T cells {tfh[0]:.1f}% vs {tfh[1]:.1f}% [S04-A]; regulatory share of follicular T cells {tfr[0]:.0f}% vs {tfr[1]:.0f}% [S04-B]; germinal-centre B cells {gc[0]:.1f}% vs {gc[1]:.1f}% [S03-K]; "
                         f"IgG {igg['H1N1'][0]/igg['H1N1'][1]:.0f} and {igg['H3N2'][0]/igg['H3N2'][1]:.0f} times, HAI {hai['H1N1'][0]/hai['H1N1'][1]:.0f} and {hai['H3N2'][0]/hai['H3N2'][1]:.0f} times PSLN-212 [S03-A, S03-C, S03-E, S03-G]", "Formulation comparison", "Consistent; correlative"],
    ["7b. CD8 T-cell arm", f"IFN-γ-producing CD8 T cells recalled by H5N1 antigen after H1N1 and H3N2 vaccination: {ifng14[0]:.1f}% vs {ifng14[1]:.1f}% at day 14 [S05-F]; lung resident-memory CD8 T cells {trm[0]:.1f}% vs {trm[1]:.1f}% [S05-I]. "
                           f"In young animals a CCR2 antagonist cut granzyme-B⁺ CD8 T cells from {incb8[0]:.1f}% to {incb8[1]:.1f}% [S02-I]", "Inhibitor (young animals)", "Tested in young animals only"],
    ["Other fork, without manganese", f"Ly6C⁺CCR2⁺ macrophages on day 5: {mac5[0]:.0f} vs {mac5[1]:.1f} ×10⁵ [S07-A]; CD206⁺ macrophages {cd206[1]:.0f}% vs {cd206[0]:.0f}% [S11-E]; lung regulatory T cells {treg[1]:.1f}% vs {treg[0]:.1f}% [S04-D]", "Formulation comparison",
     "Weakest part: n = 3 in two blocks, and the transfer experiment meant to prove it has two identically labelled columns [S07-C]"],
], [17, 47, 14, 22]))
A_(P("Two links are missing and matter for a committee that will be told this is a STING agonist. First, no experiment removes STING, so the data show that a STING-agonist formulation works, not that it works through STING. "
     "Second, no group received the particle with manganese but without CDN, so the data cannot separate what manganese does alone from what it does to the CDN. Both are arms of Study 2."))
A_(P("One practical consequence: because the whole advantage in aged animals traces to manganese, it should be treated as an active component, not as part of the vehicle, in safety, manufacturing and regulatory planning (my judgement)."))

# ----------------------------------------------------------------------------------------------------- 5
A_(H(1, "5. Biomarkers for validating efficacy"))
A_(P("These are the readouts that separate PSLN-344 from PSLN-212 in aged animals, ordered from dosing to protection. All values are PSLN-344 vs PSLN-212 in aged animals; the young benchmark follows in brackets where the block has one. "
     "The clinical analogues in the last column are my proposals and would each need assay development."))
def yb(block, panel="", x="", geo=False, fmt="{:.1f}"):
    v = gm(block, "PSLN-212(Y)", panel, x) if geo else m(block, "PSLN-212(Y)", panel, x); return fmt.format(v)
A_(TABLE(["When", "Biomarker (mouse)", "PSLN-344 vs PSLN-212, aged (young)", "Why it is useful", "Clinical analogue to develop"], [
    ["Hours", "Lung *Ifnb1*, 16 h [S01-A, S08-A]", f"{f1(i344)} vs {f1(i212)}-fold ({f1(iy)}); rises with dose", "Direct readout of target engagement; the step manganese repairs", "Interferon-stimulated gene score and CXCL10 in nasal lining fluid and blood at about 24 hours"],
    ["Hours", "Lung *Gm-csf*, 16 to 36 h [S02-F]", f"{f1(g16_344)} vs {f1(g16_212)}-fold at 16 h; {f1(g36_344)} vs {f1(g36_212)}-fold at 36 h (no young group)", f"Cleanest separator: PSLN-212 ({f1(g16_212)}-fold) is barely above sham ({f1(g16_sh)}-fold). Causal: GM-CSF rescues the downstream step [S02-G, S02-H]", "GM-CSF in nasal lining fluid or sputum at 24 to 36 hours"],
    ["Hours", "Lung *Ccl2*, 16 h [S09-A]", f"{ccl2[0]:.0f} vs {ccl2[1]:.1f}-fold ({ccl2[2]:,.0f}); n = 3", "Drives the monocyte influx", "CCL2 in nasal lining fluid or serum"],
    ["Days 2 to 8", "Lung monocytes and CD11b⁺ dendritic cells, day 4 [S01-D, S01-E]", f"Monocytes {mono[0]:.0f}% vs {mono[1]:.0f}% ({yb('S01-D','','4',fmt='{:.0f}')}%); dendritic cells {dc[0]:.0f}% vs {dc[1]:.0f}% ({yb('S01-E','','4',fmt='{:.0f}')}%)", "The cell the whole downstream response depends on", "Monocyte activation markers in blood; cell phenotyping of nasal samples"],
    ["Day 7", "ICOS-high follicular helper T cells; regulatory share of follicular T cells [S04-A, S04-B]", f"{tfh[0]:.1f}% vs {tfh[1]:.1f}% ({yb('S04-A','ICOS-high Tfh','ICOS+')}%); {tfr[0]:.0f}% vs {tfr[1]:.0f}% ({yb('S04-B Foxp3+ in CXCR5+',fmt='{:.0f}')}%)", "Early predictor of antibody quality; shows release of the age-related brake", "Circulating follicular helper T cells and plasmablasts on day 7"],
    ["Day 14", "HAI and neutralising titre [S03-C, S03-D, S03-G, S03-H]", f"HAI {hai['H1N1'][0]:.0f} vs {hai['H1N1'][1]:.0f} ({hai['H1N1'][2]:.0f}) for H1N1 and {hai['H3N2'][0]:.0f} vs {hai['H3N2'][1]:.0f} ({hai['H3N2'][2]:.0f}) for H3N2; every PSLN-344 animal at {hai_min344[0]:.0f} or above",
     f"Accepted immunogenicity endpoint for matched strains; 1:40 is the conventional human benchmark {EXT}", "HAI and microneutralisation: seroconversion rate and titre ratio against a licensed comparator"],
    ["Day 14", "IgG2a to IgG1 ratio, recomputed [S13-A to S13-D]", f"{ratio['H1N1']['PSLN-344']:.1f} vs {ratio['H1N1']['PSLN-212']:.1f} ({ratio['H1N1']['PSLN-212(Y)']:.1f}) for H1N1; {ratio['H3N2']['PSLN-344']:.1f} vs {ratio['H3N2']['PSLN-212']:.1f} ({ratio['H3N2']['PSLN-212(Y)']:.1f}) for H3N2", "Shows that the antibody class profile of young animals is restored", "No direct human equivalent; IFN-γ-producing CD4 T cells as a proxy"],
    ["Days 14 to 60", "IFN-γ-producing CD8 T cells recalled by a subtype absent from the vaccine [S05-F, S05-G]", f"{ifng14[0]:.1f}% vs {ifng14[1]:.1f}% ({yb('S05-F')}%) at day 14; {ifng60[0]:.1f}% vs {ifng60[1]:.1f}% ({yb('S05-G')}%) at day 60", "The candidate correlate for cross-subtype protection, which antibody to the vaccine strain cannot explain", "IFN-γ ELISpot or intracellular staining against conserved internal proteins"],
    ["Day 25", "Lung resident-memory CD8 T cells [S05-I]", f"{trm[0]:.1f}% vs {trm[1]:.1f}% ({yb('S05-I')}%)", "Local memory at the site of infection", "Research use only; needs airway sampling"],
    ["Safety", "Weight after dosing; lung *Tnf* and *Il6* at 72 h; CNS transcripts; alveolar macrophages [S08-D, S09-A, S10-A, S11-A]", f"Peak loss {t344.mean_peak_loss_all_pct:.1f}% vs {t212.mean_peak_loss_all_pct:.1f}%; *Tnf* {tnf72['PSLN-344']:.1f} vs {tnf72['PSLN-212']:.1f}-fold ({tnf72['PSLN-212(y)']:.1f}); *Il6* {il672['PSLN-344']:.1f} vs {il672['PSLN-212']:.1f}-fold ({il672['PSLN-212(y)']:.1f}); macrophages {am4[0]:.0f}% vs {am4[1]:.0f}%",
     "Tracks how fast the innate response resolves, which is slower in aged lung with or without manganese", "Symptom diary; nasal and serum cytokines at 72 hours and day 7"],
], [9, 21, 28, 23, 19]))
A_(P("Three cautions. First, these are group-level associations: the animals bled for biomarkers were not the animals challenged, so none is yet a correlate of protection. Study 2 bleeds every animal before challenge to test that. "
     f"Second, three readouts should not be used as biomarkers: CD40 and CD86 on lymph-node dendritic cells, which recover to only {100*cd40[0]/m('S02-D CD40','PSLN-212(Y)'):.0f}% and {100*cd86[0]/m('S02-D CD86','PSLN-212(Y)'):.0f}% of young although protection is restored [S02-D]; "
     f"the regulatory share of follicular T cells at day 30, which is back at the sham level ({tfr30[0]:.1f}% vs {tfr30[2]:.1f}%) [S04-C]; and lung neutrophils, for which the workbook has no valid data [S11-B]. "
     "Third, the IgG2a to IgG1 ratio must be taken from the recomputed values, not from S03-B and S03-F as printed (Section 9)."))

# ----------------------------------------------------------------------------------------------------- 6
A_(H(1, "6. The evidence behind the assessment"))
A_(H(2, "6.1 Protection"))
A_(FIG("fig2_survival_all_aged_experiments.png", "Figure 2. Survival at the end of observation in every lethal-challenge experiment in aged animals. Seven animals per arm, ten in S03-J. “Weights” gives the survivor count implied by the paired body-weight block where it differs from the survival block."))
A_(UL([
    f"**Size and consistency.** PSLN-344 was ahead of PSLN-212 in all 15 head-to-head comparisons. Pooled: {s344} ({pc344}; 95% CI {pT2.psln344_ci.replace('-', ' to ')}%) against {s212} ({pc212}; 95% CI {pT2.comparator_ci.replace('-', ' to ')}%). Restricted to animals of 20 months or more: {frac(k20_344)} against {frac(k20_212)}.",
    f"**Antigen is required.** Challenged on day 3: vaccine with PSLN-344 {frac(combo)}, vaccine alone {frac(vacalone)}, PSLN-344 alone {frac(alone)} [S15-H]. The early protection is not a non-specific antiviral state.",
    f"**Illness is reduced, not prevented.** Survivors given PSLN-344 still lost {loss344.min():.0f} to {loss344.max():.0f}% of body weight after challenge (young benchmark {lossy.min():.0f} to {lossy.max():.0f}%) [S13-F, S13-G, S15-A to S15-G, S15-O].",
    f"**Durability.** Day-60 challenge: {frac(d60_344)} ({pct(*d60_344)}) for PSLN-344, {frac(d60_212)} for PSLN-212, {frac(d60_y)} for young animals [S06-E to S06-G]. Untreated, unchallenged aged animals kept alongside also died ({d60_unt[1]-d60_unt[0]} of {d60_unt[1]}), so I checked whether old age explains the PSLN-344 deaths. "
    f"It does not: the five PSLN-344 animals with a weight record at death had fallen to {min(wd344):.1f} to {max(wd344):.1f}% of starting weight, the four untreated animals to {min(wdunt):.1f} to {max(wdunt):.1f}% (p = {p_wd:.3f}) [S15-E to S15-G]. Restricted to the two models run at both intervals, the comparison is {frac(d14m)} at day 14 against {frac(d60m)} at day 60 (p = {p_matched:.2f}), so the fall is suggestive, not established. Protection at two months is real but incomplete.",
    f"**Other strains.** {frac(strain)} in aged C57BL/6 and Swiss Webster mice [S15-L, S15-N]. The challenge virus is not stated for either, and the C57BL/6 body-weight block repeats data series from other experiments (Section 9), so I count the outbred Swiss Webster result and treat the C57BL/6 result as unverified.",
]))
A_(H(2, "6.2 How much of the young response is restored"))
A_(FIG("fig3_restoration_along_mechanism.png", f"Figure 3. Response in aged animals as a percentage of the young benchmark (PSLN-212 in young animals), for PSLN-212 and PSLN-344. Geometric means for titres (GMT) and Ifnb1, means otherwise. The right-hand column is the ratio of PSLN-344 to PSLN-212 in aged animals. DC, dendritic cell; Tfh, follicular helper T cell; GZMB, granzyme B; HAI, haemagglutination inhibition.", width="15.5cm"))
def chr_(stages):
    q = ch[ch.stage.isin(stages)]["aged344_pct_young"]; return f"{q.min():.0f} to {q.max():.0f}%"
_cd = ch[ch.readout.str.startswith("CD40") | ch.readout.str.startswith("CD86")]["aged344_pct_young"]
A_(P(f"PSLN-344 reaches at least 60% of the young benchmark in {n60} of {n_ch} readouts. Innate sensing and cell recruitment recover almost fully ({chr_(['Innate sensing (lung)', 'Cell recruitment (lung)'])}). "
     f"Antibody readouts recover to {chr_(['Antibody, day 14 (one dose)'])} and CD8 T-cell readouts to {chr_(['CD8 T cells'])}. "
     f"Co-stimulatory markers on lymph-node dendritic cells recover least ({_cd.min():.0f}% and {_cd.max():.0f}%) [S02-D]. PSLN-344 is a large improvement on PSLN-212 at every step and still short of a young response at most of them."))
A_(H(2, "6.3 Dose and innate profile"))
A_(FIG("fig4_innate_pharmacodynamics.png", "Figure 4. (a) Lung Ifnb1 against dose with fitted curves. (b) Lung Gm-csf over time. (c) Seven lung transcripts at 16 and 72 hours for every formulation; PSLN-344 outlined."))
A_(UL([
    f"**Manganese raises the ceiling, not the potency.** The fitted maximum is {e344.Emax:.0f}-fold (95% CI {e344.Emax_lo:.0f} to {e344.Emax_hi:.0f}) for PSLN-344 and {e212.Emax:.0f}-fold ({e212.Emax_lo:.0f} to {e212.Emax_hi:.0f}) for PSLN-212, at half-maximal doses of {e344.ED50_ug:.0f} and {e212.ED50_ug:.0f} µg [S08-A]. "
    f"Every efficacy study used 20 µg, which gives {100*e344.fraction_of_Emax_at_20ug:.0f}% of that maximum; 5 µg gives {100*d5/d20:.0f}% of the 20-µg response. Whether a lower dose protects is untested.",
    f"**The profile in aged lung resembles a young lung’s, with more TNF.** At 16 hours PSLN-344 matches the young benchmark for *Ifnb1* ({ifn16_9['PSLN-344']:.0f} vs {g9(P16,'Ifnb1','PSLN-212(y)'):.0f}-fold) and reaches {100*min(g9(P16,a,'PSLN-344')/g9(P16,a,'PSLN-212(y)') for a in ['Ccl2','Ccl3','Ccl5']):.0f} to {100*max(g9(P16,a,'PSLN-344')/g9(P16,a,'PSLN-212(y)') for a in ['Ccl2','Ccl3','Ccl5']):.0f}% of it for the chemokines *Ccl2*, *Ccl3* and *Ccl5*, "
    f"but *Tnf* is higher ({tnf16['PSLN-344']:.0f} vs {tnf16['PSLN-212(y)']:.0f}-fold, p = {fp(c9(P16,'Tnf','PSLN-344','PSLN-212(y)').p_welch_log)}) [S09-A, n = 3].",
    f"**Resolution is slower in aged animals.** At 72 hours *Tnf* is {tnf72['PSLN-344']:.1f}-fold with PSLN-344 and {tnf72['PSLN-212']:.1f}-fold with PSLN-212 in aged lung, and {tnf72['PSLN-212(y)']:.1f}-fold in young lung [S09-A, second panel]. Most of this is age; manganese adds a further {tnf72['PSLN-344']/tnf72['PSLN-212']:.1f} times (p = {fp(c9(P72,'Tnf','PSLN-344','PSLN-212').p_welch_log)}). "
    f"The cell influx also lasts longer: on day 8, lung monocytes were still {m('S01-D','PSLN-344','','8'):.1f}% with PSLN-344 in aged animals, against {m('S01-D','PSLN-212(Y)','','8'):.1f}% in young animals given PSLN-212 (p = {fp(pw('S01-D','PSLN-344','PSLN-212(Y)','','8'))}) and {m('S01-D','Sham','','8'):.1f}% with sham [S01-D].",
]))
A_(H(2, "6.4 Tolerability"))
A_(FIG("fig5_tolerability.png", "Figure 5. (a) Body weight after intranasal vaccination without challenge; thin lines are individual animals. (b) CNS transcripts 36 hours after dosing. (c) Lung transcripts at 72 hours."))
A_(UL([
    f"**Weight.** Peak loss {t344.mean_peak_loss_all_pct:.1f}% with PSLN-344, {t212.mean_peak_loss_all_pct:.1f}% with PSLN-212 and {tvac.mean_peak_loss_all_pct:.1f}% with vaccine alone (PSLN-344 vs vaccine alone p = {P_TOL:.3f}); back to {r10.loc['PSLN-344','mean']:.1f}% by day 10 [S08-D, n = 5].",
    f"**Central nervous system.** *Ifnb1* {cnsI[0]:.1f}, *Tnf* {cnsT[0]:.1f} and *Isg15* {cnsG[0]:.1f} times the PBS group at 36 hours; the cholera-toxin control gave {cnsI[1]:.1f}, {cnsT[1]:.1f} and {cnsG[1]:.1f} [S10-A, n = 5]. The *Tnf* difference from PBS is p = {fp(pw('S10-A','PBS','PSLN-344','Tnf','Tnf'))} unadjusted and p = {fp(ptk('S10-A','PBS','PSLN-344','Tnf','Tnf'))} with the Tukey correction the file specifies, "
    f"and PSLN-344 does not differ from vaccine with empty liposome (p = {fp(pw('S10-A','Sham','PSLN-344','Tnf','Tnf'))}). This is reassuring but is three transcripts at one timepoint; it does not clear the CNS question for an intranasal manganese product.",
    f"**Alveolar macrophages** are not depleted: {am4[0]:.0f}% of lung cells on day 4 with PSLN-344, {am4[1]:.0f}% with PSLN-212 [S11-A].",
]))
A_(H(2, "6.5 What the dataset does not contain"))
A_(P("I did not assess intellectual property, cost of goods or the competitor pipeline; the dataset has nothing on them. Within the science, the dataset lacks the following."))
A_(P("Human cells or tissue. A second species. A licensed comparator. A commercial split or subunit antigen (all antigens are in-house formalin-inactivated whole virus). Male animals. Virus titres after challenge. Lung or nasal histology. Mucosal IgA. The manganese dose and its tissue distribution. "
     "A STING-deficient control. A particle with manganese alone. Protection at any dose other than 20 µg. Safety or protection data after repeat dosing (a day-14 boost was given only for the IgG readout of S13-I and S13-J). Challenge later than day 60 in aged animals. Particle size, charge and stability data, which the annotation says were measured."))

# ----------------------------------------------------------------------------------------------------- 7
A_(H(1, "7. What we give up if we drop it, and what we avoid"))
A_(P("**We give up:**"))
A_(UL([
    f"the only formulation in our hands with which vaccination protects aged hosts: {pc344} survival against {pc212} for the same particle without manganese, and {frac(cmp_surv)} for the cGAMP particle (CMP-204) in the one experiment that included it [S03-I];",
    f"single-dose protection that starts within days and extends to subtypes absent from the vaccine ({frac(early)} at 2 to 3 days; {frac(het14)} cross-subtype at day 14; wild-type H5N1 {frac(h5)});",
    "a mechanism with five experimentally tested links and a set of biomarkers that separate the protective formulation from the non-protective one, which is reusable know-how about why adjuvants fail in aged lung;",
    "option value in pandemic preparedness and in other airway vaccines. There are no data on the second, so I assign it no weight.",
]))
A_(P("**We avoid:**"))
A_(UL([
    "three unknowns, any one of which could end the programme: whether CDN-1807 with manganese engages human STING in older people, whether the effect needs deep-lung delivery, and whether intranasal manganese is safe;",
    f"a long path: PSLN-344 is an adjuvant, so it needs an antigen partner and a full vaccine development programme {EXT};",
    "the work of repairing the data package.",
]))
A_(P("Dropping now would mean walking away before spending on any of the questions that decide the asset’s value. Gate 1 answers the cheapest and most decisive of them first."))

# ----------------------------------------------------------------------------------------------------- 8
A_(H(1, "8. What I considered and ruled out"))
A_(TABLE(["Considered", "What the data say", "Outcome"], [
    ["**Recommendations**", "", ""],
    ["Unconditional go to IND-enabling work", "No human-cell or second-species data; safety limited to weight and three CNS transcripts; data package not ready for outside scrutiny", "Ruled out"],
    ["Drop now", f"A {rd}-point survival difference that holds in every subset and under the worst reading; the next decisive questions are inexpensive", "Ruled out"],
    ["Reposition as a stand-alone antiviral or prophylactic", f"PSLN-344 without vaccine: {frac(alone)} [S15-H]", "Ruled out"],
    ["Target all adults rather than older adults", f"Young animals: {frac(young['S09-B'][0])} with either formulation in three models; manganese adds {i344y/iy:.2f} times the interferon response and no measured benefit [S09-B, S09-D, S09-F, S01-A]", "Ruled out"],
    ["Oncology, the usual indication for a STING agonist", "No oncology data in the dataset", "Not assessed"],
    ["**Alternatives to PSLN-344 in the dataset**", "", ""],
    ["PSLN-212 (no manganese)", f"{s212} survival in aged animals", "Ruled out for aged hosts"],
    ["CMP-204 (cGAMP particle)", f"*Ifnb1* {icmp:.1f}-fold vs {i344:.1f}-fold; day-14 IgG titre {th(igg['H1N1'][3])} vs {th(igg['H1N1'][0])}; survival {frac(cmp_surv)} vs {frac(hom)} [S01-A, S03-A, S03-I]", "Ruled out"],
    ["Adding a TLR7/8 agonist (PSLN-R848, PSLN-212/R848)", f"*Tnf* {tnf16['PSLN-R848']:.0f} and {tnf16['PSLN-212/R848']:.0f}-fold, *Il10* {il1016['PSLN-R848']:.0f} and {il1016['PSLN-212/R848']:.0f}-fold, against {tnf16['PSLN-344']:.0f} and {il1016['PSLN-344']:.0f}-fold for PSLN-344 [S09-A]; "
                                                            f"weight loss {tr848.mean_peak_loss_all_pct:.0f}% and not recovered by day 10 [S08-D]; *Ifnb1* no higher than PSLN-344 ({icombo:.0f} vs {i344:.0f}-fold) [S01-A]", "Ruled out on tolerability and profile"],
    ["PSLN-212 plus recombinant GM-CSF", f"Restores the dendritic-cell step ({gmres[0]:.1f}% to {gmres[1]:.1f}%) [S02-G], but needs four daily intranasal doses of a recombinant protein", "Useful as proof of mechanism; not a product"],
    ["Two doses of PSLN-212 instead of adding manganese", f"After a boost, IgG titre with PSLN-212 is {th(boost['H1N1'][0])} (H1N1) and {th(boost['H3N2'][0])} (H3N2); one dose of PSLN-344 gives {th(igg['H1N1'][0])} and {th(igg['H3N2'][0])} (p = {fp(P_BOOST['H1N1'])} and {fp(P_BOOST['H3N2'])}) [S13-I, S13-J, S03-A, S03-E]. No challenge or T-cell data after a boost",
     "Not ruled out by the data; a two-dose regimen is a weaker product for seasonal use"],
    ["**Readings of the data**", "", ""],
    ["PSLN-344 skews antibody toward IgG1 (S03-B, S03-F as printed)", f"Column headers are permuted; recomputed ratios are {ratio['H1N1']['PSLN-344']:.1f} and {ratio['H3N2']['PSLN-344']:.1f}, not {printed['H1N1']['PSLN-344']:.2f} and {printed['H3N2']['PSLN-344']:.2f}", "Rejected"],
    ["The manganese particle delivers less cargo to epithelium (S08-C as printed)", "Headers most likely swapped; the first two columns reuse S01-B values", "Not accepted; unresolved"],
    ["No neutrophil influx after dosing (S11-B)", "The block duplicates the alveolar-macrophage block", "Rejected; no valid data"],
    ["The second “16h” cytokine panel is a replicate (S09-A)", "Its *Ifnb1* row is the 72-hour data of S01-A", "Rejected; analysed as 72 hours"],
    ["Day-60 deaths are old-age attrition", f"Weight at death {np.mean(wd344):.0f}% of baseline in PSLN-344 animals, {np.mean(wdunt):.0f}% in untreated animals", "Rejected"],
    ["The CNS transcript data clear the neurological risk (S10-A)", "Three transcripts, one timepoint, no manganese measurement", "Not accepted"],
    ["Independent replication in a second inbred strain (S15-L, S15-M)", "Body-weight series repeat those of three other blocks", "Downgraded to unverified"],
    ["Tetramer data as key CD8 evidence (S05-A, S05-B)", "Two animals per point; description inconsistent", "Downgraded to descriptive"],
    ["Transfer experiment as proof that one macrophage subset drives regulatory T cells (S07-C)", "Both columns carry the same label", "Not usable"],
    ["Body-weight means as printed", "Dead animals carry a frozen last weight in some arms", "Rejected; live animals only"],
], [30, 50, 20]))

# ----------------------------------------------------------------------------------------------------- 9
A_(H(1, "9. Data-integrity findings and what they do to the case"))
A_(P(f"I checked the workbook against itself before using it: printed group sizes against rows present, every derived block against its source, every survival block against its body-weight block, and every block against every other for repeated values. "
     f"That produced {nfind} findings (Appendix D). The {nA} below change a conclusion if the workbook is read as printed. I could not check anything against raw records; that is Step 0."))
A_(TABLE(["Ref", "Where", "Finding (full detail in Appendix D)", "Effect on the case"], [[r[0], r[2], IL.SHORT[r[0]], r[5]] for r in IL.LOG if r[1] == "A"], [7, 17, 36, 40]))
A_(P(f"**Net effect.** The headline result is robust to all of this: {pW2.psln344} vs {pW2.comparator_surv} at the worst reading and {sNF2.psln344} vs {sNF2.comparator_surv} with every flagged experiment removed. "
     "Four specific claims are not usable until the source is checked: epithelial delivery by PSLN-344 itself (D-04), replication in C57BL/6 mice (D-08), superiority over PSLN-212 against wild-type H5N1 (D-07), and anything about neutrophils (D-03). "
     "One claim flips in the asset’s favour once corrected: the antibody subclass ratio (D-01)."))

# ----------------------------------------------------------------------------------------------------- extra ledger rows for numbers used in tables/text
_pr = CHAIN[CHAIN.stage == "Protection"].iloc[0]
led("6", "Survival in the 10 aged experiments that carry a young arm (Figure 3, last row): PSLN-344, PSLN-212, young PSLN-212", re.search(r"\((.*)\)", _pr.readout).group(1), "S03-I, S06-A to S06-G, S15-L, S15-N status columns", "stats/restoration_chain.csv (script 10)", "sum of arms")
led("4", "Donor-derived monocytes infiltrating the lung: wild-type vs IFNAR-deficient donor cells (young recipients)", f"{m('S12-A','WT to WT'):.0f}% vs {m('S12-A','IFNAR-/- to WT'):.0f}%", "S12!A3:B5", OUT_C, f"n = 3; Welch p = {fp(pw('S12-A','WT to WT','IFNAR-/- to WT'))}")
led("3", "IgG geometric-mean titre with PSLN-344 in aged animals: day 28 after a day-14 boost vs day 14 after one dose", f"H1N1 {boost['H1N1'][1]/igg['H1N1'][0]:.1f} times; H3N2 {boost['H3N2'][1]/igg['H3N2'][0]:.1f} times", "S13!I53:I57, O53:O57 vs S03!D3:D7, D10:D14", "stats/special_analyses.txt (script 07, part e)", "ratio of geometric means, n = 5; different animals at the two timepoints")
led("6", "Lung Ifnb1 at 16 h in the S09-A panel (geometric mean, n = 3): PSLN-344 aged vs PSLN-212 young", f"{ifn16_9['PSLN-344']:.0f} vs {g9(P16,'Ifnb1','PSLN-212(y)'):.0f}", "S09!Q3:V3", OUT_9, "subset of the S01-A animals (D-02)")
led("6", "Chemokines at 16 h, PSLN-344 aged as % of PSLN-212 young: Ccl2, Ccl3, Ccl5", ", ".join(f"{100*g9(P16,a,'PSLN-344')/g9(P16,a,'PSLN-212(y)'):.0f}%" for a in ["Ccl2", "Ccl3", "Ccl5"]), "S09!Q5:V7", OUT_9, "ratio of geometric-mean folds, n = 3")
led("6", "Lung monocytes on day 8: PSLN-344 aged, PSLN-212 young, sham aged", f"{m('S01-D','PSLN-344','','8'):.1f}%, {m('S01-D','PSLN-212(Y)','','8'):.1f}%, {m('S01-D','Sham','','8'):.1f}%", "S01!B28:U28", OUT_C, f"n = 5; PSLN-344 aged vs PSLN-212 young Welch p = {fp(pw('S01-D','PSLN-344','PSLN-212(Y)','','8'))}")
led("6", "Lung Tnf at 72 h, PSLN-344 vs PSLN-212 in aged animals", f"{tnf72['PSLN-344']/tnf72['PSLN-212']:.1f} times", "S09!AE8:AG8, AN8:AP8", OUT_9, f"Welch on log10 p = {fp(c9(P72,'Tnf','PSLN-344','PSLN-212').p_welch_log)}")
led("6", "Share of the young benchmark reached by aged PSLN-344, by stage", "; ".join(f"{st}: {ch[ch.stage==st].aged344_pct_young.min():.0f} to {ch[ch.stage==st].aged344_pct_young.max():.0f}%" for st in ch.stage.unique()), "see stats/restoration_chain.csv", "stats/restoration_chain.csv (script 10)", "as L022")
led("5", "Young-benchmark values quoted in the biomarker table (PSLN-212 in young animals)",
    f"monocytes d4 {m('S01-D','PSLN-212(Y)','','4'):.0f}%; CD11b+ DC d4 {m('S01-E','PSLN-212(Y)','','4'):.0f}%; ICOS-high Tfh {m('S04-A','PSLN-212(Y)','ICOS-high Tfh','ICOS+'):.1f}%; Foxp3+ share {m('S04-B Foxp3+ in CXCR5+','PSLN-212(Y)'):.0f}%; "
    f"IFN-g+ CD8 d14 {m('S05-F','PSLN-212(Y)'):.1f}%, d60 {m('S05-G','PSLN-212(Y)'):.1f}%; lung Trm {m('S05-I','PSLN-212(Y)'):.1f}%; HAI GMT {hai['H1N1'][2]:.0f} and {hai['H3N2'][2]:.0f}",
    "S01!Q26:U26; S01!Q32:U32; S04!G5:K5; S04!D8:D12; S05!D33:D37; S05!D40:D44; S05!D54:D58; S03!O3:O7; S03!O10:O14", OUT_C, "means (geometric means for HAI), n = 5")
led("5", "CD40+ and CD86+ of node CD11b+ DC, aged PSLN-344 as % of young", f"{100*cd40[0]/m('S02-D CD40','PSLN-212(Y)'):.0f}% and {100*cd86[0]/m('S02-D CD86','PSLN-212(Y)'):.0f}%", "S02!C10:D14; S02!H10:I14", OUT_C, "ratio of means")
led("9", "Body-weight values identical between S15-C PSLN-344 and S15-I Vaccine+PSLN-344; between S09-E PSLN-344Y and S15-M PSLN-212(Y)", f"{IL.d1[1]} of {IL.d1[2]} (7 animals); {IL.d2[1]} of {IL.d2[2]} (6 animals)", "S15!W24:AC30 vs S15!W73:AC79; S09!W40:AD46 vs S15!I104:O110", "integrity/B2_duplicate_bodyweight_trajectories_real_values.csv (script 02 + follow-up)", "same-day, same-animal-position comparison of non-frozen values")
_d = REC[(REC.tte_block == "S06-D")].set_index("group")
led("9", "S06-D (rgH5N1 challenge 3 days after dosing): survivors in the survival block vs implied by the body-weight block S15-D, for PSLN-344 and young PSLN-212; same design in S15-H",
    f"PSLN-344 {_d.loc['PSLN-344','tte_survivors']} vs {_d.loc['PSLN-344','bw_survivors']}; young {_d.loc['PSLN-212(Y)','tte_survivors']} vs {_d.loc['PSLN-212(Y)','bw_survivors']}; S15-H {frac(combo)}",
    "S06!D48:E61; S15!B33:H40, W33:AC40; S15!D87:D93", "stats/survival_reconciliation.csv (script 05)", "frozen final weights counted as deaths (D-05, D-09)")
led("9", "Fisher exact p for PSLN-344 7/7 vs PSLN-212 in matched-strain challenge under the two records (0/7 in S03-I; 3/7 implied by S13-F)", f"{stats.fisher_exact([[7,0],[0,7]])[1]:.4f}; {stats.fisher_exact([[7,0],[3,4]])[1]:.2f}", "S03!D31:E44; S13!P33:V40", "computed in script 14", "two-sided Fisher exact")

# ----------------------------------------------------------------------------------------------------- appendices
A_(PB)
A_(H(1, "Appendix A. How the analysis was done"))
ntid = len(tid); nsv = len(pd.read_csv("/tmp/outputs/analysis/tidy/survival.csv")); nbw = int(pd.read_csv("/tmp/outputs/analysis/tidy/bodyweight.csv")["value"].notna().sum())
A_(UL([
    "**Data.** psln_program_dataset.xlsx (15 sheets; last modified 3 September 2026) and psln_program_annotation.pdf (19 pages; dated 15 September 2026), both treated as the current data cut.",
    f"**Extraction.** Every numeric cell of the 15 sheets was assigned to a labelled block, identified as a day or dose label, or listed as unlabelled (S08 rows 89 to 101). That gave {ntid:,} continuous values, {nsv} animals in time-to-event blocks and {nbw:,} body-weight readings. Labels are kept as printed.",
    "**Groups.** Groups marked (Y) are young (7 to 8 weeks); all others are aged (20 months or more) unless the annotation states otherwise. “Sham” is vaccine with empty liposome.",
    "**Continuous readouts.** Group mean and standard deviation; geometric means for titres and fold-changes. For every pair of groups I report the method the file specifies (one-way ANOVA with Tukey’s test) together with a Welch t-test (on log10 for titres and fold-changes) and an exact Mann-Whitney test. "
    "With five animals per group the smallest attainable exact two-sided p is 0.008; with three it is 0.10.",
    "**Scales.** S09-A is printed as log10 and was analysed as printed, then reported as geometric-mean fold. A printed HAI of 0 means below the 1:10 starting dilution and was set to 5 for geometric means.",
    "**Survival.** Survivors over animals with exact (Clopper-Pearson) confidence intervals; log-rank tests with exact permutation p-values; Fisher’s exact test. Pooling across experiments used the Cochran-Mantel-Haenszel test with each experiment as a stratum, so animals are only ever compared within their own experiment. The confidence intervals on pooled percentages treat animals as interchangeable across experiments and are somewhat narrow for that reason.",
    "**Body weight.** A blank tail, or a value repeated unchanged to day 14, was treated as death. Summary statistics use live animals only.",
    "**Dose-response.** A sigmoid maximum-effect model fitted to log10 response, with bootstrap confidence intervals.",
    "**Integrity checks.** Printed n against rows present; every derived block recomputed from its source; every survival block compared with its body-weight block; every series compared with every other for repeated values.",
    "**Multiplicity.** The analysis contains several hundred pairwise tests. I rely on effect size and on consistency across independent blocks; p-values are unadjusted unless labelled Tukey.",
    "**Not done.** Nothing was checked against raw records. No literature or market data were used; statements from general knowledge are marked.",
    "**Reproducibility.** Scripts 01 to 16 in the analysis folder regenerate every table, figure and number in this document from the workbook.",
]))

A_(H(1, "Appendix B. Evidence ledger"))
A_(P("One row per number or set of numbers used in the text. “Workbook source” gives sheet and cells; “Output” gives the analysis file in which the number can be found. The same table, with the full statistics behind it, is in PSLN-344_evidence_ledger.xlsx."))
A_(TABLE(["ID", "Statement", "Value", "Workbook source", "Output", "Method and test"],
         [[r["id"], r["statement"], r["value"], r["workbook_source"], r["analysis_output"], r["method"]] for r in LEDGER], [7, 23, 22, 16, 12, 20]))

A_(H(1, "Appendix C. Survival by experiment"))
REG_ROWS = [("S03-I", ["Sham", "PSLN-212", "PSLN-344", "PSLN-212(Y)"], "CMP-204 " + frac(arm("S03-I", "CMP-204"))), ("S03-J", ["Sham", "PSLN-212", "PSLN-344", None], ""),
            ("S06-A", ["Sham", "PSLN-212", "PSLN-344", "PSLN-212(Y)"], ""), ("S06-B", ["Sham", "PSLN-212", "PSLN-344", "PSLN-212(Y)"], ""), ("S06-C", ["Sham", "PSLN-212", "PSLN-344", "PSLN-212(Y)"], ""),
            ("S06-D", ["Sham", "PSLN-212", "PSLN-344", "PSLN-212(Y)"], ""), ("S06-E", ["Sham", "PSLN-212", "PSLN-344", "PSLN-212(Y)"], "Untreated " + frac(arm("S06-E", "Untreated"))),
            ("S06-F", ["Sham", "PSLN-212", "PSLN-344", "PSLN-212(Y)"], "Untreated " + frac(arm("S06-F", "Untreated"))), ("S06-G", ["Sham", "PSLN-212", "PSLN-344", "PSLN-212(Y)"], "Untreated " + frac(arm("S06-G", "Untreated"))),
            ("S15-L", ["Sham", "PSLN-212", "PSLN-344", "PSLN-212(Y)"], ""), ("S15-N", ["Sham", "PSLN-212", "PSLN-344", "PSLN-212(Y)"], "")]
def wnote(block, group):
    q = REC[(REC.tte_block == block) & (REC.group == group)]
    if len(q) and q.iloc[0].survivors_agree == "NO": return f" (weights {q.iloc[0].bw_survivors})"
    return ""
rowsC = []
for blk, gs, other in REG_ROWS:
    r0 = A[A.block == blk].iloc[0]
    cellsC = [blk, r0.age, f"{r0.vaccine} → {r0.challenge}, {r0.interval}".replace("→ not stated, not stated", "→ challenge virus and interval not stated").replace(", not stated", ", interval not stated")]
    for g in gs: cellsC.append("" if g is None else frac(arm(blk, g)) + wnote(blk, g))
    cellsC.append(other); cellsC.append(fp(sp(blk, "PSLN-212", "PSLN-344")))
    rowsC.append(cellsC)
for blk, lab in [("S06-E(2) imprinting/PR8", "S06-E, second block"), ("S06-F(2) imprinting/Perth", "S06-F, second block")]:
    r0 = A[A.block == blk].iloc[0]
    for pre in ["Naive", "Imprinting"]:
        rowsC.append([lab, "14-month BALB/c, " + ("no prior infection" if pre == "Naive" else "prior PR8 infection"), f"{r0.vaccine} → {r0.challenge}, {r0.interval}".replace(", not stated", ", interval not stated"), "", frac(arm(blk, f"{pre}+PSLN-212")), frac(arm(blk, f"{pre}+PSLN-344")), "", "",
                      fp(sp(blk, f"{pre}+PSLN-212", f"{pre}+PSLN-344"))])
rowsC.append(["S15-H", "aged BALB/c", "bivalent or none → 5x mLD50 rgH5N1, d3", frac(vacalone) + " (vaccine alone)", "", frac(combo), "", "PSLN-344 alone " + frac(alone), ""])
for blk in ["S09-B", "S09-D", "S09-F"]:
    r0 = A[A.block == blk].iloc[0]
    rowsC.append([blk, r0.age, f"{r0.vaccine} → {r0.challenge}, {r0.interval}", frac(arm(blk, "Sham")) + wnote(blk, "Sham"), "", "", frac(arm(blk, "PSLN-212Y")), "PSLN-344 young " + frac(arm(blk, "PSLN-344Y")), ""])
r0 = A[A.block == "S13-E"].iloc[0]
rowsC.append(["S13-E", r0.age, f"{r0.vaccine} → {r0.challenge}, {r0.interval}", frac(arm("S13-E", "Sham")), "", "", "", f"Naive {frac(arm('S13-E','Naive'))}; CMP-204 young {frac(arm('S13-E','CMP-204(Y)'))}; PSLN-344 young {frac(arm('S13-E','PSLN-344(Y)'))}", ""])
A_(P("Survivors over animals at the end of observation, from the time-to-event blocks as printed. “(weights k/n)” is the count implied by the paired body-weight block where it differs. The last column is the exact log-rank p for PSLN-344 against PSLN-212. Kaplan-Meier curves for every block are in figures/figA1_kaplan_meier_all_blocks.png. rgH5N1 is the reverse-genetics virus carrying the H5 and N1 genes on a PR8 backbone; mLD50 is the mouse median lethal dose; d14 means challenge 14 days after the dose."))
A_(TABLE(["Block", "Animals", "Vaccine → challenge, interval", "Sham", "PSLN-212", "PSLN-344", "PSLN-212 young", "Other arms", "p"], rowsC, [9, 12, 22, 9, 10, 10, 8, 12, 8]))

A_(H(1, "Appendix D. Data-integrity log"))
A_(P("Severity A: changes a conclusion if the workbook is read as printed. B: limits what can be claimed. C: housekeeping, for the raw-data check."))
A_(TABLE(["Ref", "Sev.", "Where", "Finding", "How I handled it", "Effect"], [[r[0], r[1], r[2], r[3], r[4], r[5]] for r in IL.LOG], [7, 5, 13, 37, 17, 21]))

A_(H(1, "Appendix E. Files delivered"))
A_(TABLE(["File", "Contents"], [
    ["PSLN-344_portfolio_proposal.docx", "This document"],
    ["PSLN-344_evidence_ledger.xlsx", "Ledger (Appendix B); survival by arm with confidence intervals and tests; pooled and sensitivity analyses; group statistics and pairwise tests for every continuous block; restoration table; survival against body-weight reconciliation; integrity log"],
    ["figures/", "Figures 1 to 5 and the Kaplan-Meier appendix figure, as PNG"],
    ["analysis/", "Scripts 01 to 16; tidy/ (every workbook value with its cell address); stats/ (analysis outputs); integrity/ (integrity-check outputs)"],
], [32, 68]))

for _r in LEDGER:
    for _k in ("value", "method", "statement"): _r[_k] = _r[_k].replace("p = <", "p < ")
doc = [d_.replace("p = &lt;", "p &lt; ") for d_ in doc]
html_doc = "<html><head><meta charset='utf-8'><title>PSLN-344: portfolio recommendation and proposal for next steps</title></head><body>\n" + "".join(doc) + "</body></html>"
open(f"{SRC}/proposal.html", "w").write(html_doc)
json.dump(LEDGER, open(f"{SRC}/ledger.json", "w"), indent=1)
print("ledger rows:", len(LEDGER), "| html chars:", len(html_doc))
