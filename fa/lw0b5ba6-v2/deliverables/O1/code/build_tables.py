"""Generate markdown tables for the proposal directly from analysis outputs (no hand transcription)."""
import pandas as pd, numpy as np, os
os.makedirs('/tmp/work/snippets', exist_ok=True)
H = pd.read_csv('/tmp/work/h2h.csv'); R = pd.read_csv('/tmp/work/restoration_index.csv')
S = pd.read_csv('/tmp/work/survival_by_group.csv'); P = pd.read_csv('/tmp/work/survival_pooled.csv')
PO = pd.read_csv('/tmp/work/survival_pooled_arms.csv'); M = pd.read_csv('/tmp/work/moa_contrasts.csv')
BM = pd.read_csv('/tmp/work/biomarker_table.csv'); IR = pd.read_csv('/tmp/work/integrity_register.csv')
RX = pd.read_csv('/tmp/work/reactogenicity_s08d.csv')

def fq(q):
    return '<0.001' if q < 0.001 else f'{q:.3f}'
def fnum(x, kind):
    if pd.isna(x): return '-'
    if kind == 'titre': return f'{x:,.0f}'
    if kind == 'fold': return f'{x:.1f}'
    return f'{x:.1f}'

# ---------- 1. headline evidence table ----------
rows = [('Lung Ifnb1 at 16 h (fold vs untreated)', 'S01-A', 'Ifnb1', '16h', 'fold'),
        ('Lung Gm-csf at 36 h (fold)', 'S02-F', 'Gm-csf (lung)', '36h', 'fold'),
        ('Lung monocytes, day 4 (%)', 'S01-D', 'Lung monocytes', 'd4', 'pct'),
        ('CCR7+ migratory CD11b+ DC, 72 h (%)', 'S02-A', 'CCR7+ migratory CD11b+ DC (lung)', '72h', 'pct'),
        ('Antigen+ DC in MLN, 36 h (%)', 'S02-C', 'MLN AF647-OVA+ DC', '36h', 'pct'),
        ('OT-I CD8 priming by MLN DC (%)', 'S02-E', 'OT-I proliferation (DC co-culture)', '72h+3d', 'pct'),
        ('CD86+ of MLN CD11b+ DC, day 3 (%)', 'S02-D CD86', 'CD86+ of MLN CD11b+ DC', 'd3', 'pct'),
        ('ICOS-hi Tfh, day 7 (%)', 'S04-A', 'Tfh ICOS-hi', 'd7', 'pct'),
        ('Tfr (Foxp3+ of CXCR5+ICOShi), day 7 (%) - lower is better', 'S04-B Foxp3', 'Tfr (Foxp3+ of CXCR5+ICOShi)', 'd7', 'pct'),
        ('Germinal-centre B cells, day 7 (%)', 'S03-K', 'MLN GC B cells', 'd7', 'pct'),
        ('Serum IgG anti-CA09 H1N1, day 14 (GMT)', 'S03-A', 'IgG CA09 H1N1', 'd14', 'titre'),
        ('HAI anti-CA09 H1N1, day 14 (GMT)', 'S03-C', 'HAI CA09 H1N1', 'd14', 'titre'),
        ('HAI anti-Aichi H3N2, day 14 (GMT)', 'S03-G', 'HAI Aichi H3N2', 'd14', 'titre'),
        ('Neutralising Ab anti-CA09 H1N1, day 14 (GMT)', 'S03-D', 'Neut CA09 H1N1', 'd14', 'titre'),
        ('IgG anti-CA09 after boost, day 28 (GMT)', 'S13-I', 'IgG CA09 H1N1 post-boost', 'd28', 'titre'),
        ('IFN-g+ CD8 (rgH5N1 restim), day 14 (%)', 'S05-F', 'MLN IFNg+ CD8 (rgH5N1 restim)', 'd14', 'pct'),
        ('IFN-g+ CD8 (rgH5N1 restim), day 60 (%)', 'S05-G', 'MLN IFNg+ CD8 (rgH5N1 restim)', 'd60', 'pct'),
        ('Lung resident-memory CD8, day 25 (%)', 'S05-I', 'Lung TRM CD8', 'd25', 'pct')]
out = ['| Endpoint (aged mice unless stated) | Sham | PSLN-212 | **PSLN-344** | Young PSLN-212 | PSLN-344 vs PSLN-212 (95% CI) | FDR q | Gap closed (RI) | Source |',
       '|---|---|---|---|---|---|---|---|---|']
for lab, blk, an, t, kind in rows:
    h = H[(H.block == blk) & (H.analyte == an) & (H.time == t)].iloc[0]
    if h.scale == 'linear %':
        eff = f'{h.est:+.1f} pp ({h.lo:+.1f} to {h.hi:+.1f})'
    else:
        eff = f'{h.est:.1f}x ({h.lo:.1f}-{h.hi:.1f})'
    r = R[(R.block == blk) & (R.analyte == an)]
    ri = f'{r.RI.iloc[0]:.2f}' if len(r) else '-'
    out.append(f'| {lab} | {fnum(h.summarySham, kind)} | {fnum(h.summary212, kind)} | **{fnum(h.summary344, kind)}** | {fnum(h.summaryY, kind)} | {eff} | {fq(h.q_BH)} | {ri} | {blk} |')
# survival + safety rows
po = PO.set_index('group')
out.append(f"| **Survival after lethal challenge, pooled aged arms (10 experiments)** | {po.loc['Sham','survivors']}/{po.loc['Sham','n']} ({po.loc['Sham','pct']:.0f}%) | {po.loc['PSLN-212','survivors']}/{po.loc['PSLN-212','n']} ({po.loc['PSLN-212','pct']:.0f}%) | **{po.loc['PSLN-344','survivors']}/{po.loc['PSLN-344','n']} ({po.loc['PSLN-344','pct']:.0f}%)** | {po.loc['PSLN-212(Y)','survivors']}/{po.loc['PSLN-212(Y)','n']} ({po.loc['PSLN-212(Y)','pct']:.0f}%) | see Table 2 | - | 0.83 | S03-I/J, S06-A-G (excl. D), S15-L/N |")
rx = RX.set_index('group')
out.append(f"| Post-vaccination weight nadir, no challenge (% of day 0) | {rx.loc['Vaccine','mean_nadir']:.1f} (vaccine only) | {rx.loc['PSLN-212','mean_nadir']:.1f} | **{rx.loc['PSLN-344','mean_nadir']:.1f}** | {rx.loc['PSLN-212(Y)','mean_nadir']:.1f} | -0.6 pp (p=0.56) | - | - | S08-D |")
open('/tmp/work/snippets/t1_headline.md', 'w').write('\n'.join(out))

# ---------- 2. survival per experiment ----------
pw = pd.read_csv('/tmp/work/survival_pairwise.csv')
exp = [('S03-I', 'Aged BALB/c; bivalent vaccine, homologous CA09 H1N1 10x LD50 at d14', 'PSLN-344', 'PSLN-212'),
       ('S03-J', 'BALB/c (aged by convention); rgH5N1 vaccine, wild-type VN04 H5N1 at d2', 'PSLN-344', 'PSLN-212'),
       ('S06-A', 'Aged; Aichi H3N2 vaccine -> PR8 H1N1 at d14 (heterosubtypic)', 'PSLN-344', 'PSLN-212'),
       ('S06-B', 'Aged; Aichi H3N2 vaccine -> PR8 H1N1 at d3 (rapid)', 'PSLN-344', 'PSLN-212'),
       ('S06-C', 'Aged; bivalent -> rgH5N1 at d14', 'PSLN-344', 'PSLN-212'),
       ('S06-D', 'Aged; bivalent -> rgH5N1 at d3 - EXCLUDED (identical to S06-C)', 'PSLN-344', 'PSLN-212'),
       ('S06-E', 'Aged; Aichi H3N2 vaccine -> PR8 H1N1 at d60 (durability)', 'PSLN-344', 'PSLN-212'),
       ('S06-F', 'Aged; bivalent -> rgH5N1 at d60', 'PSLN-344', 'PSLN-212'),
       ('S06-G', 'Aged; CA09 H1N1 vaccine -> Perth H3N2 at d60', 'PSLN-344', 'PSLN-212'),
       ('S06-E[imprint]', '14-month naive; bivalent -> PR8 H1N1', 'Naive+PSLN-344', 'Naive+PSLN-212'),
       ('S06-E[imprint]', '14-month PR8-imprinted; bivalent -> PR8 H1N1', 'Imprinting+PSLN-344', 'Imprinting+PSLN-212'),
       ('S06-F[imprint]', '14-month naive; bivalent -> Perth H3N2 at d14', 'Naive+PSLN-344', 'Naive+PSLN-212'),
       ('S06-F[imprint]', '14-month PR8-imprinted; bivalent -> Perth H3N2 at d14', 'Imprinting+PSLN-344', 'Imprinting+PSLN-212'),
       ('S15-L', 'Aged C57BL/6 (challenge not stated; body weight recycled)', 'PSLN-344', 'PSLN-212'),
       ('S15-N', 'Aged Swiss Webster (challenge not stated; body weight recycled)', 'PSLN-344', 'PSLN-212')]
out = ['| Block | Design | Sham | PSLN-212 | PSLN-344 | Young PSLN-212 | Log-rank p (344 vs 212) | Fisher p |', '|---|---|---|---|---|---|---|---|']
for blk, des, a, b in exp:
    s = S[S.block == blk].set_index('group')
    f = lambda g: f"{int(s.loc[g, 'survivors'])}/{int(s.loc[g, 'n'])}" if g in s.index else '-'
    pr = pw[(pw.block == blk) & (pw.A == a) & (pw.B == b)].iloc[0]
    out.append(f"| {blk} | {des} | {f('Sham')} | {f(b)} | **{f(a)}** | {f('PSLN-212(Y)')} | {pr.p_logrank:.4f} | {pr.p_fisher:.4f} |")
for blk, des in [('S09-B', 'Young; Aichi H3N2 vaccine -> PR8 at d21'), ('S09-D', 'Young; CA09 vaccine -> Perth H3N2 at d21'),
                 ('S09-F', 'Young; bivalent -> rgH5N1 at d180'), ('S13-E', 'Young; bivalent -> CA09 10x LD50 at d14')]:
    s = S[S.block == blk].set_index('group')
    f = lambda g: f"{int(s.loc[g, 'survivors'])}/{int(s.loc[g, 'n'])}" if g in s.index else '-'
    extra = f" (CMP-204 young {f('CMP-204(Y)')}; naive {f('Naive')})" if blk == 'S13-E' else ''
    out.append(f"| {blk} | {des}{extra} | {f('Sham')} | - | young PSLN-344: **{f('PSLN-344(Y)')}** | {f('PSLN-212(Y)')} | - | - |")
s = S[S.block == 'S15-H'].set_index('group')
out.append(f"| S15-H | Aged; given 3 d before rgH5N1: vaccine alone {int(s.loc['3d Vaccine','survivors'])}/7; PSLN-344 alone {int(s.loc['3d PSLN-344','survivors'])}/7; vaccine + PSLN-344 {int(s.loc['3d Vaccine+PSLN-344','survivors'])}/7 (body-weight record duplicated, C2) | - | - | - | - | - | - |")
open('/tmp/work/snippets/t2_survival.md', 'w').write('\n'.join(out))

# ---------- 3. pooled sensitivity ----------
out = ['| Analysis set | Strata | PSLN-344 survivors | PSLN-212 survivors | Difference, pp (95% CI, Newcombe) | Stratified log-rank p | CMH p | Strata favouring PSLN-344 |', '|---|---|---|---|---|---|---|---|']
for _, r in P.iterrows():
    lr = '-' if pd.isna(r.strat_logrank_p) else f'{r.strat_logrank_p:.1e}'
    cmh = '<1e-15' if r.CMH_p < 1e-15 else f'{r.CMH_p:.1e}'
    out.append(f"| {r.analysis} | {r.strata} | {r.surv_344} ({r.pct_344:.0f}%) | {r.surv_212} ({r.pct_212:.0f}%) | {r.MH_RD_pp:.1f} ({r.RD_newcombe_lo:.1f} to {r.RD_newcombe_hi:.1f}) | {lr} | {cmh} | {r.strata_favouring_344} |")
open('/tmp/work/snippets/t3_pooled.md', 'w').write('\n'.join(out))

# ---------- 4. restoration by layer ----------
L = R.copy()
g = L.groupby('layer').agg(n=('RI', 'size'), median=('RI', 'median'), lo=('RI', 'min'), hi=('RI', 'max'),
                           endpoints=('analyte', lambda x: '; '.join(sorted(set(x)))[:140])).reset_index()
out = ['| Layer of the immune response | Endpoints | Median RI | Range | Reading |', '|---|---|---|---|---|']
reading = {'1': 'Near-complete rescue', '2': 'Substantial rescue', '3': 'Largely NOT rescued', '4': 'Substantial, but effector (GZMB) partial',
           '5': 'Substantial', '6': 'Substantial (HAI near-young)', '7': 'Partial: boosted titres stay below young', '8': 'Partial: memory below young'}
for _, r in g.iterrows():
    out.append(f"| {r.layer[2:]} | {r.n} | {r['median']:.2f} | {r.lo:.2f}-{r.hi:.2f} | {reading[r.layer[0]]} |")
open('/tmp/work/snippets/t4_restoration.md', 'w').write('\n'.join(out))

# ---------- 5. MoA interventions ----------
READ = [('Delivery: SP-A/D', 'Test: SP-A/D knockout vs WT (liposomes of PSLN-344 composition)', 'DiD+ alveolar macrophages, %, 16 h'),
        ('Gap-junction', 'Test: carbenoxolone vs saline (PSLN-344)', 'Recruited lung monocytes, %, d3'),
        ('Type I IFN: IFNAR-/- BM (no cDC)', 'Test: IFNAR-/- vs WT bone marrow (no cDC precursors), PSLN-344', 'Donor-derived moDC, %, d3'),
        ('GM-CSF rescue: IFNAR-/- BM + GM-CSF vs IFNAR-/- BM', 'Rescue: IFNAR-/- marrow + GM-CSF vs IFNAR-/- marrow', 'Donor-derived moDC, %, d3'),
        ('GM-CSF gain-of-function', 'Gain: PSLN-212 + rGM-CSF vs PSLN-212', 'Lung Ly6C+CD11c+MHC-II+ moDC-like, %, d5'),
        ('Type I IFN: IFNAR-/- vs WT BM: infiltrating', 'Test: IFNAR-/- vs WT marrow (young, n=3)', 'Infiltrating donor monocytes, %, d3'),
        ('CCR2: INCB3344 vs vehicle, lung monocytes', 'Test: CCR2 antagonist vs vehicle (PSLN-344)', 'Lung CD11b+Ly6C+ monocytes, %'),
        ('CCR2: INCB3344 vs vehicle, Ly6C+', 'Test: CCR2 antagonist vs vehicle (PSLN-344)', 'Lung Ly6C+ macrophages, %'),
        ('CCR2: INCB3344 vs vehicle, lung GZMB', 'Test: CCR2 antagonist vs vehicle (PSLN-344, young)', 'Lung GZMB+ CD8, %, d5'),
        ('Migration: PTX vs PSLN-344, antigen+', 'Test: pertussis toxin (blocks Gi chemokine signalling)', 'AF647-OVA+ DC in MLN, %, 36 h'),
        ('Migration: PTX vs PSLN-344, OT-I', 'Test: pertussis toxin', 'OT-I proliferation driven by MLN DC, %'),
        ('Migration: PTX in vivo, OT-I proliferation in MLN', 'Test: pertussis toxin in vivo (n=3)', 'OT-I proliferation in MLN, %, d4'),
        ('Migration: PTX in vivo, OT-I proliferation in lung', 'Test: pertussis toxin in vivo (n=3)', 'OT-I proliferation in lung, %, d4')]
out = ['| Intervention | Readout | Control | Intervention | Change | p (Welch / exact MW) | Block |', '|---|---|---|---|---|---|---|']
for key, test, readout in READ:
    r = M[M.label.str.startswith(key)].iloc[0]
    fp = lambda p: '<0.0001' if p < 1e-4 else f'{p:.4f}'
    out.append(f"| {test} | {readout} | {r.meanB:.1f} | {r.meanA:.1f} | {r['pct_change']:+.0f}% | {fp(r.p_welch)} / {fp(r.p_mwu)} | {r.block} |")
open('/tmp/work/snippets/t5_moa.md', 'w').write('\n'.join(out))

# ---------- 6. biomarker table ----------
out = ['| Tier / timing | Marker (our data) | n (344 v 212) | Sham | PSLN-212 | PSLN-344 | Young PSLN-212 | Separation 344 vs 212 | Source | Human-measurable analogue |', '|---|---|---|---|---|---|---|---|---|---|']
for _, r in BM.iterrows():
    fm = lambda x: '-' if pd.isna(x) else (f'{x:,.0f}' if x >= 100 else f'{x:.1f}')
    sep = 'complete (AUC 1.0)' if r.complete_separation else f'AUC {r.AUC_344_vs_212:.2f}'
    src = r.source.replace('S09-A panel1[A:U] (16h (as printed))', 'S09-A (16 h)').replace('S09-A panel2[X:AS] (16h (as printed))', 'S09-A (72 h; printed "16h")')
    out.append(f"| {r.tier} | {r.marker} | {r.n} | {fm(r.sham)} | {fm(r.PSLN212)} | {fm(r.PSLN344)} | {fm(r.young212)} | {sep} | {src} | {r.human_analogue} |")
open('/tmp/work/snippets/t6_biomarkers.md', 'w').write('\n'.join(out))

# ---------- 7. integrity register (full) ----------
out = []
for _, r in IR.iterrows():
    out.append(f"**{r.id} ({r.severity}) - {r.blocks}.** *Evidence:* `{r.cells_or_evidence}`\n")
    out.append(f"- *Finding:* {r.finding}\n- *Impact:* {r.impact}\n- *How handled here:* {r.handling}\n- *Remediation:* {r.remediation}\n")
open('/tmp/work/snippets/t7_integrity.md', 'w').write('\n'.join(out))

# ---------- 8. full head-to-head appendix ----------
Hh = H[H.excluded.isna()].copy()
out = ['| Block | Endpoint | Time | Scale | PSLN-212 | PSLN-344 | Young 212 | Effect (95% CI) | p (Welch) | p (exact MW) | FDR q | RI |', '|---|---|---|---|---|---|---|---|---|---|---|---|']
for _, h in Hh.iterrows():
    kind = 'titre' if h.summary344 >= 100 and h.scale == 'log2' else 'x'
    f = lambda v: '-' if pd.isna(v) else (f'{v:,.0f}' if abs(v) >= 100 else f'{v:.2f}')
    eff = f'{h.est:+.2f} pp ({h.lo:+.2f} to {h.hi:+.2f})' if h.scale == 'linear %' else f'{h.est:.2f}x ({h.lo:.2f}-{h.hi:.2f})'
    t = h.time if isinstance(h.time, str) else ''
    if h.block.startswith('S09-A panel2'): t = '72 h (printed "16h"; see M3)'
    ri = '-' if pd.isna(h.restoration_index) else f'{h.restoration_index:.2f}'
    out.append(f"| {h.block} | {h.analyte} | {t} | {h.scale} | {f(h.summary212)} | {f(h.summary344)} | {f(h.summaryY)} | {eff} | {h.p_welch:.2g} | {h.p_mwu:.2g} | {fq(h.q_BH)} | {ri} |")
open('/tmp/work/snippets/t8_h2h_full.md', 'w').write('\n'.join(out))
Hx = H[H.excluded.notna()]
out = ['| Block | Endpoint | Time | Reason excluded from the decision family |', '|---|---|---|---|']
for _, h in Hx.iterrows():
    out.append(f"| {h.block} | {h.analyte} | {h.time if isinstance(h.time, str) else ''} | {h.excluded} |")
open('/tmp/work/snippets/t9_excluded.md', 'w').write('\n'.join(out))
print('snippets written'); print(open('/tmp/work/snippets/t1_headline.md').read()); print(open('/tmp/work/snippets/t3_pooled.md').read())
print(open('/tmp/work/snippets/t4_restoration.md').read()); print(open('/tmp/work/snippets/t5_moa.md').read())
