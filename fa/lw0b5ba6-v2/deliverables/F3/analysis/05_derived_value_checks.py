"""05_derived_value_checks.py
Recompute every derived block from the raw block it should come from, and test scale/label concordance
between blocks that report the same measurand.
"""
import json, itertools, math
import numpy as np
B = json.load(open('/tmp/work/parsed/parsed_blocks.json'))
g = lambda bid: B[bid]['groups']

print("=" * 100)
print("CHECK 1. IgG2a/IgG1 quotient blocks (S03-B, S03-F) vs per-animal quotient of raw subclass titres (S13-A/B, S13-C/D)")
for ratio_blk, num, den, virus in [('S03-B', 'S13-A', 'S13-B', 'CA09 H1N1'), ('S03-F', 'S13-C', 'S13-D', 'Aichi H3N2')]:
    print(f"\n  {ratio_blk} ({virus}) vs {num}/{den}")
    raw = {k: [a / b for a, b in zip(g(num)[k], g(den)[k])] for k in B[num]['order']}
    for lab in B[ratio_blk]['order']:
        printed = g(ratio_blk)[lab]
        match = [k for k, v in raw.items() if np.allclose(v, printed, rtol=1e-4)]
        print(f"     column printed as {lab:<12} = {np.round(printed, 3).tolist()}  -> equals raw quotient of group: {match}")
    print("     raw per-animal quotients, labelled by the raw blocks:")
    for k, v in raw.items():
        print(f"        {k:<12} {np.round(v, 3).tolist()}   geometric mean {np.exp(np.mean(np.log(v))):.2f}")
    # which labelling agrees with total IgG rank order?
tot = {k: np.exp(np.mean(np.log(v))) for k, v in g('S03-A').items()}
print("\n  Cross-check against total IgG (S03-A, CA09): GMT", {k: round(v) for k, v in tot.items()})
print("  IgG2a+IgG1 sum by raw-block label (S13-A + S13-B):", {k: [round(a + b) for a, b in zip(g('S13-A')[k], g('S13-B')[k])] for k in B['S13-A']['order']})

print("\n" + "=" * 100)
print("CHECK 2. S04-B 'Tfh:Tfr' quotient vs (100 - Foxp3%)/Foxp3% from S04-B Foxp3 block")
for lab in B['S04-B_TfhTfr']['order']:
    fx = np.array(g('S04-B_Foxp3')[lab]); pr = np.array(g('S04-B_TfhTfr')[lab])
    print(f"   {lab:<12} printed {np.round(pr, 3).tolist()}  recomputed {np.round((100 - fx) / fx, 3).tolist()}  match={np.allclose(pr, (100 - fx) / fx, rtol=1e-4)}")
print("   NOTE: annotation defines the quotient as Tfh% / Tfr%; S04-A Tfh% (ICOS-lo + ICOS-hi) over S04-B Foxp3% would be:")
for lab in B['S04-B_TfhTfr']['order']:
    tfh = np.array(g('S04-A_ICOSlo')[lab]) + np.array(g('S04-A_ICOShi')[lab])
    print(f"   {lab:<12} Tfh total% {np.round(tfh, 2).tolist()}  /Foxp3% -> {np.round(tfh / np.array(g('S04-B_Foxp3')[lab]), 3).tolist()}")

print("\n" + "=" * 100)
print("CHECK 3. Ifnb1: S01-A (linear fold) vs S09-A (log10 fold); which S01-A timepoint does each S09-A panel match?")
m = {'PBS': 'Sham', 'CMP-204': 'CMP-204', 'PSLN-212': 'PSLN-212', 'PSLN-R848': 'PSLN-R848', 'PSLN-212/R848': 'PSLN-212/R848', 'PSLN-344': 'PSLN-344', 'PSLN-212(y)': 'PSLN-212(Y)'}
print(f"   {'group':<15}{'S01-A 16h GM':>13}{'S01-A 72h GM':>13}{'S09-A p1 10^mean':>18}{'S09-A p2 10^mean':>18}")
d16 = []; d72 = []
for k9, k1 in m.items():
    a16 = np.exp(np.mean(np.log(g('S01-A_16h')[k1]))); a72 = np.exp(np.mean(np.log(g('S01-A_72h')[k1])))
    p1 = 10 ** np.mean(g('S09-A_panel1')[k9]['Ifnb1']); p2 = 10 ** np.mean(g('S09-A_panel2')[k9]['Ifnb1'])
    print(f"   {k9:<15}{a16:>13.2f}{a72:>13.2f}{p1:>18.2f}{p2:>18.2f}")
    d16.append((math.log10(a16), math.log10(a72), math.log10(p1), math.log10(p2)))
d = np.array(d16)
print(f"   RMS log10 difference: panel1 vs 16h = {np.sqrt(np.mean((d[:,2]-d[:,0])**2)):.3f}; panel1 vs 72h = {np.sqrt(np.mean((d[:,2]-d[:,1])**2)):.3f}")
print(f"                         panel2 vs 16h = {np.sqrt(np.mean((d[:,3]-d[:,0])**2)):.3f}; panel2 vs 72h = {np.sqrt(np.mean((d[:,3]-d[:,1])**2)):.3f}")
print("   both panels carry the printed label:", B['S09-A_panel1']['printed_label'], '|', B['S09-A_panel2']['printed_label'])

print("\n" + "=" * 100)
print("CHECK 4. SRB uptake: S01-B vs S08-C (same measurand, PSLN-SRB arm should agree)")
for k, v in g('S01-B').items(): print(f"   S01-B  {k:<22} {v}  mean {np.mean(v):.2f}")
for k, v in g('S08-C').items(): print(f"   S08-C  {k:<22} {v}  mean {np.mean(v):.2f}")

print("\n" + "=" * 100)
print("CHECK 5. S11-A (alveolar macrophages) vs S11-B (neutrophils): identical replicate values")
tot = same = 0
for grp in B['S11-A']['order']:
    for t in B['S11-A']['times']:
        a = g('S11-A')[grp][t]; b = g('S11-B')[grp][t]
        eq = [i for i in range(5) if a[i] == b[i]]
        tot += 5; same += len(eq)
        print(f"   {grp:<12} day {t}: identical replicate positions {eq}   A={a}  B={b}")
print(f"   -> {same}/{tot} cells identical between the two blocks; replicate #1 identical in "
      f"{sum(g('S11-A')[grp][t][0]==g('S11-B')[grp][t][0] for grp in B['S11-A']['order'] for t in B['S11-A']['times'])}/20 group-timepoints, replicate #2 in "
      f"{sum(g('S11-A')[grp][t][1]==g('S11-B')[grp][t][1] for grp in B['S11-A']['order'] for t in B['S11-A']['times'])}/20")

print("\n" + "=" * 100)
print("CHECK 6. HAI values below the stated lowest dilution (1:10)")
for bid in ['S03-C', 'S03-G']:
    for k, v in g(bid).items():
        lo = [x for x in v if x < 10]
        if lo: print(f"   {bid} {k}: {v}  -> {len(lo)} value(s) < 10 (printed as {lo})")
print("   other titre blocks with floor-like values:")
for bid in ['S13-I', 'S13-J', 'S03-A', 'S03-E']:
    for k, v in g(bid).items():
        if min(v) <= 10: print(f"   {bid} {k}: {v}")

print("\n" + "=" * 100)
print("CHECK 7. S08 unlabelled region rows 89-101")
print("  ", B['S08-orphan_r89-101']['cells_raw'])
