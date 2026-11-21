"""08_safety_tolerability.py
Everything in the workbook that bears on tolerability / safety of the adjuvant itself:
  S08-D  body weight after immunisation (no challenge)
  S09-A  lung cytokine mRNA (log10) - panel 1 (16 h) and panel 2 (printed 16 h; matches the 72 h Ifnb1 data of S01-A)
  S10-A  CNS transcripts 36 h
  S11    lung cell infiltrates
  post-challenge body weight among animals still under observation (carried-forward values removed)
"""
import json, math
import numpy as np
from scipy import stats
B = json.load(open('/tmp/work/parsed/parsed_blocks.json'))
OUT = {}
def welch(a, b):
    t, p = stats.ttest_ind(a, b, equal_var=False); return float(np.mean(a) - np.mean(b)), float(p)

print("=" * 110); print("S08-D body weight after immunisation (aged unless (Y); % of day 0), mean [min] per day"); print("=" * 110)
b = B['S08-D']; OUT['S08-D'] = {}
for g in b['order']:
    rows = {t: [x for x in v if x is not None] for t, v in b['groups'][g].items()}
    print(f"   {g:<14}" + '  '.join(f"d{t}: {np.mean(v):5.1f} [{min(v):5.1f}] n={len(v)}" for t, v in rows.items()))
    nad_t = min(rows, key=lambda t: np.mean(rows[t]))
    per_animal_nadir = [min(b['groups'][g][t][i] for t in b['times'] if b['groups'][g][t][i] is not None) for i in range(5)]
    OUT['S08-D'][g] = dict(mean_by_day={t: float(np.mean(v)) for t, v in rows.items()}, n_by_day={t: len(v) for t, v in rows.items()},
                           nadir_day=nad_t, nadir_mean=float(np.mean(rows[nad_t])), per_animal_nadir=per_animal_nadir,
                           d10_mean=float(np.mean(rows['10'])), animals_below_95=int(sum(1 for x in per_animal_nadir if x < 95)), animals_below_90=int(sum(1 for x in per_animal_nadir if x < 90)))
    print(f"   {'':<14}group nadir day {nad_t}: {np.mean(rows[nad_t]):.1f}%; per-animal nadirs {per_animal_nadir}; animals <95%: {OUT['S08-D'][g]['animals_below_95']}/5, <90%: {OUT['S08-D'][g]['animals_below_90']}/5")
for t in ['4', '6', '8', '10']:
    d, p = welch(b['groups']['PSLN-344'][t], b['groups']['Vaccine'][t]); d2, p2 = welch(b['groups']['PSLN-344'][t], b['groups']['PSLN-212'][t])
    d3, p3 = welch([x for x in b['groups']['PSLN-212/R848'][t] if x is not None], b['groups']['Vaccine'][t])
    print(f"   day {t}: PSLN-344 minus vaccine-alone {d:+.1f} pts (p={p:.2g}); minus PSLN-212 {d2:+.1f} (p={p2:.2g}); PSLN-212/R848 minus vaccine-alone {d3:+.1f} (p={p3:.2g})")
    OUT['S08-D'][f'd{t}_344_minus_vaccine'] = (d, p); OUT['S08-D'][f'd{t}_344_minus_212'] = (d2, p2); OUT['S08-D'][f'd{t}_R848combo_minus_vaccine'] = (d3, p3)

print("\n" + "=" * 110); print("S09-A lung cytokine mRNA: fold vs untreated = 10^(mean log10), n=3"); print("=" * 110)
for pid, lab in [('S09-A_panel1', 'panel 1 (columns A-U, printed 16 h; matches S01-A 16 h)'), ('S09-A_panel2', 'panel 2 (columns X-AS, printed 16 h; Ifnb1 matches S01-A 72 h)')]:
    b = B[pid]; OUT[pid] = {}
    print(f" {lab}")
    print(f"   {'analyte':<8}" + ''.join(f"{g:>15}" for g in b['order']))
    for an in b['analytes']:
        vals = {g: 10 ** float(np.mean(b['groups'][g][an])) for g in b['order']}
        OUT[pid][an] = vals
        print(f"   {an:<8}" + ''.join(f"{vals[g]:>15.1f}" for g in b['order']))
print(" ratios of interest (fold PSLN-344 aged / fold comparator), Welch on log10 values:")
for pid in ['S09-A_panel1', 'S09-A_panel2']:
    b = B[pid]
    for an in b['analytes']:
        outs = []
        for comp in ['PSLN-212', 'PSLN-212(y)', 'PSLN-212/R848']:
            a = b['groups']['PSLN-344'][an]; c = b['groups'][comp][an]
            d, p = welch(a, c); outs.append(f"vs {comp}: x{10**d:.2f} (p={p:.2g})")
            OUT[pid][f'{an}::344/{comp}'] = (10 ** d, p)
        print(f"   {pid[-6:]} {an:<6} " + ' | '.join(outs))

print("\n" + "=" * 110); print("S10-A CNS transcripts 36 h after intranasal vaccine +/- adjuvant (fold, linear; mean ± SD, n=5)"); print("=" * 110)
for an in ['Ifnb1', 'Tnf', 'Isg15']:
    g = B[f'S10-A_{an}']['groups']; OUT[f'S10-A_{an}'] = {}
    line = f"   {an:<6} " + ' | '.join(f"{k}: {np.mean(v):.2f}±{np.std(v, ddof=1):.2f}" for k, v in g.items())
    d, p = welch(np.log(g['PSLN-344']), np.log(g['PBS'])); d2, p2 = welch(np.log(g['PSLN-344']), np.log(g['Sham'])); d3, p3 = welch(np.log(g['CT']), np.log(g['PBS']))
    # upper bound of 95% CI of ratio 344/PBS
    a, c = np.log(g['PSLN-344']), np.log(g['PBS'])
    va, vc = a.var(ddof=1) / 5, c.var(ddof=1) / 5; df = (va + vc) ** 2 / (va ** 2 / 4 + vc ** 2 / 4); se = math.sqrt(va + vc)
    lo, hi = math.exp(d - stats.t.ppf(.975, df) * se), math.exp(d + stats.t.ppf(.975, df) * se)
    print(line + f"\n          PSLN-344/PBS = {math.exp(d):.2f} [95% CI {lo:.2f}-{hi:.2f}] p={p:.2g}; PSLN-344/Sham = {math.exp(d2):.2f} p={p2:.2g}; CT/PBS = {math.exp(d3):.2f} p={p3:.2g}")
    OUT[f'S10-A_{an}'] = dict(means={k: float(np.mean(v)) for k, v in g.items()}, r344_pbs=(math.exp(d), lo, hi, p), r344_sham=(math.exp(d2), p2), rCT_pbs=(math.exp(d3), p3))

print("\n" + "=" * 110); print("Post-challenge body weight among animals still under observation (carried-forward tails and blanks removed)"); print("=" * 110)
def live_series(b, g):
    times = b['times']; n = len(b['groups'][g][times[0]]); out = []
    for i in range(n):
        s = [b['groups'][g][t][i] for t in times]
        present = [j for j, v in enumerate(s) if v is not None]; last = present[-1]
        run = 1
        while last - run >= 0 and s[last - run] is not None and s[last - run] == s[last]: run += 1
        dead = (last < len(s) - 1) or run >= 3 or (run == 2 and s[last] < 90)
        cut = last - run + 1 if (run >= 2 and dead and last == len(s) - 1) else last
        out.append(dict(series=s[:cut + 1], dead=dead, nadir=min(s[:cut + 1]), final=s[cut] if not dead else None))
    return out
rows = []
for bid in ['S13-F', 'S15-A', 'S15-B', 'S15-C', 'S15-D', 'S15-E', 'S15-F', 'S15-G', 'S15-M', 'S15-O', 'S15-I', 'S15-J', 'S15-K', 'S09-C', 'S09-E', 'S09-G', 'S13-G']:
    b = B[bid]
    for g in b['order']:
        ls = live_series(b, g); surv = [x for x in ls if not x['dead']]
        if surv:
            nad = [x['nadir'] for x in surv]; fin = [x['final'] for x in surv]
            rows.append((bid, g, len(surv), len(ls), float(np.mean(nad)), float(min(nad)), float(np.mean(fin))))
print(f"   {'block':<7}{'group':<24}{'survivors (weight block)':>26}{'mean nadir %':>14}{'worst nadir %':>15}{'mean d14 %':>12}")
for r in rows:
    print(f"   {r[0]:<7}{r[1]:<24}{str(r[2])+'/'+str(r[3]):>26}{r[4]:>14.1f}{r[5]:>15.1f}{r[6]:>12.1f}")
OUT['post_challenge_weight_survivors'] = rows
# aggregate: aged PSLN-344 survivors vs young PSLN-212(Y) survivors in the standard blocks
std = ['S13-F', 'S15-A', 'S15-B', 'S15-C', 'S15-D', 'S15-E', 'S15-F', 'S15-G', 'S15-M', 'S15-O']
for g in ['PSLN-344', 'PSLN-212(Y)', 'PSLN-212']:
    sel = [r for r in rows if r[0] in std and r[1] == g]
    n = sum(r[2] for r in sel); m = sum(r[4] * r[2] for r in sel) / n
    print(f"   survivors pooled over {len(sel)} aged-design blocks, {g:<12}: n={n}, mean individual nadir {m:.1f}% of d0 (mean loss {100-m:.1f}%)")
    OUT[f'pooled_nadir_{g}'] = dict(n=n, mean_nadir=m)
json.dump(OUT, open('/tmp/work/parsed/safety_results.json', 'w'), indent=1, default=float)
