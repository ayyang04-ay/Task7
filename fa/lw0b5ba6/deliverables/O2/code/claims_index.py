"""Independent recomputation of every headline number in the proposal, directly from per-animal source values."""
import pandas as pd, numpy as np
from scipy import stats
t = pd.read_csv('/tmp/work/tidy.csv'); t['time'] = t['time'].astype(str)
s = pd.read_csv('/tmp/work/survival.csv'); b = pd.read_csv('/tmp/work/bodyweight.csv')
C = []

def cells(block, group=None, **kw):
    d = t[t.block == block]
    if group: d = d[d.group == group]
    for k, v in kw.items(): d = d[d[k].astype(str) == v]
    return f"{d.cell.iloc[0]}..{d.cell.iloc[-1]}" if len(d) else ''

def v(block, group, **kw):
    d = t[(t.block == block) & (t.group == group)]
    for k, vv in kw.items(): d = d[d[k].astype(str) == vv]
    return d.value.values.astype(float)

def gm(x): return float(np.exp(np.mean(np.log(x))))

def add(cid, section, claim, value, source, analysis):
    C.append(dict(ID=cid, Section=section, Claim=claim, Recomputed_value=value, Source_block_and_cells=source, Analysis=analysis))

def surv(block, group):
    d = s[(s.block == block) & (s.group == group)]
    return int(len(d) - d.event.sum()), int(len(d))

# ---------------- antibody ----------------
def titre(cid, sec, label, block, floor=None):
    a = v(block, 'PSLN-212'); c = v(block, 'PSLN-344'); y = v(block, 'PSLN-212(Y)')
    if floor: a, c, y = [np.where(x <= 0, floor, x) for x in (a, c, y)]
    la, lc = np.log10(a), np.log10(c)
    w = stats.ttest_ind(lc, la, equal_var=False)
    se = np.sqrt(lc.var(ddof=1) / 5 + la.var(ddof=1) / 5)
    df = se ** 4 / ((lc.var(ddof=1) / 5) ** 2 / 4 + (la.var(ddof=1) / 5) ** 2 / 4); tc = stats.t.ppf(.975, df)
    r = 10 ** (lc.mean() - la.mean())
    add(cid, sec, f'{label}: GMT PSLN-212 vs PSLN-344 (young benchmark); ratio 344/212',
        f'{gm(a):,.0f} vs {gm(c):,.0f} (young {gm(y):,.0f}); x{r:.2f} (95% CI {10**(np.log10(r)-tc*se):.2f}-{10**(np.log10(r)+tc*se):.2f}); Welch p={w.pvalue:.2g}',
        f'{block}: {cells(block)}', 'Geometric mean; Welch t-test on log10 titres' + ('; <LOD (0) set to 5' if floor else ''))
titre('C01', '3.1', 'IgG anti-CA09 d14', 'S03-A')
titre('C02', '3.1', 'HAI anti-CA09 d14', 'S03-C', floor=5)
titre('C03', '3.1', 'HAI anti-Aichi d14', 'S03-G', floor=5)
titre('C04', '3.1', 'Neutralisation anti-CA09 d14', 'S03-D')
titre('C05', '3.1', 'IgG anti-CA09 d28 post-boost', 'S13-I')
y = np.log10(v('S03-C', 'PSLN-212(Y)')); c = np.log10(v('S03-C', 'PSLN-344'))
add('C06', '3.1', 'HAI CA09: aged PSLN-344 vs young PSLN-212', f'ratio x{10**(c.mean()-y.mean()):.2f}, Welch p={stats.ttest_ind(c,y,equal_var=False).pvalue:.2f}', f'S03-C: {cells("S03-C")}', 'Welch on log10')
for cid, blk in [('C07', 'S13-I'), ('C08', 'S13-J')]:
    c = np.log10(v(blk, 'PSLN-344')); y = np.log10(v(blk, 'PSLN-212(Y)'))
    add(cid, '3.1', f'Post-boost IgG, aged PSLN-344 / young PSLN-212 [{blk}]', f'x{10**(c.mean()-y.mean()):.2f}', f'{blk}: {cells(blk)}', 'ratio of geometric means')

def pct(cid, sec, label, block, **kw):
    a = v(block, 'PSLN-212', **kw); c = v(block, 'PSLN-344', **kw); yy = v(block, 'PSLN-212(Y)', **kw) if len(v(block, 'PSLN-212(Y)', **kw)) else None
    w = stats.ttest_ind(c, a, equal_var=False)
    add(cid, sec, f'{label}: PSLN-212 vs PSLN-344' + (' (young)' if yy is not None else ''),
        f'{a.mean():.2f} vs {c.mean():.2f}' + (f' (young {yy.mean():.2f})' if yy is not None else '') + f'; diff {c.mean()-a.mean():+.2f}; Welch p={w.pvalue:.2g}',
        f'{block}: {cells(block)}', 'arithmetic mean; Welch t-test')
pct('C09', '3.1/5', 'GC B cells MLN d7 (%)', 'S03-K')
pct('C10', '3.1/5', 'ICOS-hi Tfh MLN d7 (%)', 'S04-A_ICOShi')
pct('C11', '3.1/5', 'IFN-g+ CD8 (H5 restim) d14 (%)', 'S05-F')
pct('C12', '3.1/5', 'IFN-g+ CD8 (H5 restim) d60 (%)', 'S05-G')
pct('C13', '3.1/5', 'Lung TRM CD8 d25 (%)', 'S05-I')
pct('C14', '5', 'Lung monocytes d4 (%)', 'S01-D', time='4')
pct('C15', '5', 'CCR7+ migratory DC (%)', 'S02-A')
pct('C16', '5', 'Antigen+ MLN DC (%)', 'S02-C')
pct('C17', '5', 'cDC1 (%)', 'S01-F')
pct('C18', '5', 'CD40+ MLN CD11b+ DC (%)', 'S02-D_CD40')
pct('C19', '5', 'CD86+ MLN CD11b+ DC (%)', 'S02-D_CD86')
pct('C20', '5', 'Tfr d7 (%)', 'S04-B_Tfr')
pct('C21', '5', 'Lung Treg d7 (%)', 'S04-D')
pct('C22', '5', 'CD206+ macrophages (%)', 'S11-E')
# ---------------- innate ----------------
a = v('S01-A_16h', 'PSLN-212'); c = v('S01-A_16h', 'PSLN-344'); y = v('S01-A_16h', 'PSLN-212(Y)')
add('C23', '5/6', 'Lung Ifnb1 16 h fold: PSLN-212 vs PSLN-344 (young); ratio; restoration index',
    f'{gm(a):.1f} vs {gm(c):.1f} (young {gm(y):.1f}); x{gm(c)/gm(a):.2f}, Welch p={stats.ttest_ind(np.log(c),np.log(a),equal_var=False).pvalue:.2g}; RI={(np.log10(gm(c))-np.log10(gm(a)))/(np.log10(gm(y))-np.log10(gm(a))):.2f}',
    f'S01-A 16h: {cells("S01-A_16h")}', 'geometric means; Welch on log')
a = v('S01-A_72h', 'PSLN-212'); c = v('S01-A_72h', 'PSLN-344')
add('C24', '5/6', 'Lung Ifnb1 72 h: ratio 344/212', f'x{gm(c)/gm(a):.2f}, Welch p={stats.ttest_ind(np.log(c),np.log(a),equal_var=False).pvalue:.2f}', f'S01-A 72h: {cells("S01-A_72h")}', 'geometric; Welch on log')
a = v('S08-A', 'PSLN-212', time='20'); c = v('S08-A', 'PSLN-344', time='20'); r8 = v('S08-A', 'PSLN-344/R848', time='20')
add('C25', '5/9', 'Ifnb1 at 20 ug: PSLN-212 vs PSLN-344 vs PSLN-344/R848', f'{gm(a):.1f} vs {gm(c):.1f} vs {gm(r8):.1f}; 344/212 x{gm(c)/gm(a):.2f}', f'S08-A: {cells("S08-A")}', 'geometric means (n=3)')
for an, cid in [('Ccl2', 'C26')]:
    a = v('S09-A_blk1(B:V)', 'PSLN-212', analyte=an); c = v('S09-A_blk1(B:V)', 'PSLN-344', analyte=an)
    add(cid, '5/6', f'Lung {an} 16 h fold (log10 data): PSLN-212 vs PSLN-344; ratio', f'{10**a.mean():.1f} vs {10**c.mean():.0f}; x{10**(c.mean()-a.mean()):.0f}', f'S09-A panel 1: {cells("S09-A_blk1(B:V)")}', 'values stored as log10; 10^mean')
a = v('S02-F', 'PSLN-212', time='36h'); c = v('S02-F', 'PSLN-344', time='36h')
add('C27', '5/6', 'Gm-csf 36 h fold: PSLN-212 vs PSLN-344; ratio', f'{gm(a):.1f} vs {gm(c):.1f}; x{gm(c)/gm(a):.1f}; Welch p={stats.ttest_ind(np.log(c),np.log(a),equal_var=False).pvalue:.1g}', f'S02-F: {cells("S02-F")}', 'geometric; Welch on log')
for cid, blk, g1, g2, lab in [('C28', 'S01-B', 'AECII/PSLN-SRB', 'AECI/PSLN-SRB', 'AECII vs AECI uptake (%)'), ('C29', 'S01-B', 'AECII/PSLN-SRB', 'AECII/FreeSRB', 'Liposome vs free dye, AECII (%)'),
                              ('C30', 'S01-C', 'WT', 'SPA/D', 'AM uptake WT vs SP-A/D KO (%)'), ('C31', 'S11-C', 'CBX-', 'CBX+', 'Recruited monocytes saline vs CBX (%)'),
                              ('C32', 'S07-B_Mono', 'PSLN-344', 'PSLN-344+INCB3344', 'Monocytes vehicle vs CCR2 antagonist (%)'), ('C33', 'S07-B_Ly6C+Mphi', 'PSLN-344', 'PSLN-344+INCB3344', 'Ly6C+ Mphi vehicle vs CCR2 antagonist (%)'),
                              ('C34', 'S02-I', 'PSLN-344(Y)', 'PSLN-344(Y)+INCB3344', 'GZMB+ CD8 (young) vehicle vs CCR2 antagonist (%)'), ('C35', 'S02-H', 'WT w/o cDC', 'IFN w/o cDC', 'moDC WT vs IFNAR-/- BM (%)'),
                              ('C36', 'S02-H', 'GMCSF', 'IFN w/o cDC', 'moDC IFNAR-/- + GM-CSF vs IFNAR-/- (%)'), ('C37', 'S02-G', 'PSLN-212+GM-CSF', 'PSLN-212', 'moDC PSLN-212+GM-CSF vs PSLN-212 (%)'),
                              ('C38', 'S02-C', 'PSLN-344', 'PTX', 'Antigen+ MLN DC PSLN-344 vs pertussis toxin (%)')]:
    x1 = v(blk, g1); x2 = v(blk, g2)
    add(cid, '5', lab, f'{x1.mean():.2f} vs {x2.mean():.2f} ({(x2.mean()-x1.mean())/x1.mean()*100:+.0f}%); Student p={stats.ttest_ind(x1,x2).pvalue:.2g}', f'{blk}: {cells(blk)}', 'arithmetic means; Student t (stated method)')
a = v('S07-A', 'PSLN-212', time='5'); c = v('S07-A', 'PSLN-344', time='5')
add('C39', '5', 'Ly6C+CCR2+ macrophages day 5 (x1e5): PSLN-212 vs PSLN-344', f'{a.mean():.1f} vs {c.mean():.1f} ({(c.mean()-a.mean())/a.mean()*100:+.0f}%)', f'S07-A: {cells("S07-A")}', 'arithmetic means (n=3)')
# ---------------- survival ----------------
tierA = ['S03-I', 'S03-J', 'S06-A', 'S06-B', 'S06-C', 'S06-E_r34', 'S06-F_r34', 'S06-G', 'S15-L', 'S15-N']
tierB = ['S06-A', 'S06-B', 'S06-F_r34', 'S15-L', 'S15-N']
for cid, lab, blocks in [('C40', 'Tier A pooled survival (S06-D excluded)', tierA), ('C41', 'Tier B pooled survival', tierB), ('C42', 'Tier C (S06-B)', ['S06-B']), ('C43', 'Day-60 pooled', ['S06-E_r34', 'S06-F_r34', 'S06-G'])]:
    A = [surv(bb, 'PSLN-344') for bb in blocks]; B = [surv(bb, 'PSLN-212') for bb in blocks]
    add(cid, '1/3.2', lab + ': PSLN-344 vs PSLN-212', f'{sum(x[0] for x in A)}/{sum(x[1] for x in A)} vs {sum(x[0] for x in B)}/{sum(x[1] for x in B)}', '; '.join(blocks) + ' (ET14 rows)', 'survivors/n at end of observation; MH RD & stratified log-rank in ET5')
U = [surv(bb, 'Untreated') for bb in ['S06-E_r34', 'S06-F_r34', 'S06-G']]
add('C44', '3.2/4', 'Unchallenged aged controls surviving 14 days', f'{sum(x[0] for x in U)}/{sum(x[1] for x in U)}', 'S06!L62:L68, S06!R62:R68, S06!F99:F105', 'count')
bl = [bb for bb in tierA if 'PSLN-212(Y)' in s[s.block == bb].group.values]
A = [surv(bb, 'PSLN-344') for bb in bl]; Y = [surv(bb, 'PSLN-212(Y)') for bb in bl]
add('C45', '3.2', 'Aged PSLN-344 vs young PSLN-212 benchmark (blocks with both)', f'{sum(x[0] for x in A)}/{sum(x[1] for x in A)} vs {sum(x[0] for x in Y)}/{sum(x[1] for x in Y)}', ', '.join(bl), 'count; stratified log-rank in ET5')
add('C46', '3.2', '3-day study: vaccine+PSLN-344 vs vaccine vs PSLN-344 alone', f"{surv('S15-H','3d Vaccine+PSLN-344')} vs {surv('S15-H','3d Vaccine')} vs {surv('S15-H','3d PSLN-344')}", 'S15!A72:D93', '(survivors, n)')
add('C47', '3.2', '14-month mice, naive: PSLN-344 vs PSLN-212 (two challenges)', f"{sum(surv(bb,'Naive+PSLN-344')[0] for bb in ['S06-E_r71','S06-F_r71'])}/14 vs {sum(surv(bb,'Naive+PSLN-212')[0] for bb in ['S06-E_r71','S06-F_r71'])}/14", 'S06!G70:Q98', 'count')
add('C48', '3.2', '14-month mice, imprinted: PSLN-344 vs PSLN-212', f"{sum(surv(bb,'Imprinting+PSLN-344')[0] for bb in ['S06-E_r71','S06-F_r71'])}/14 vs {sum(surv(bb,'Imprinting+PSLN-212')[0] for bb in ['S06-E_r71','S06-F_r71'])}/14", 'S06!G70:Q98', 'count')
add('C49', '3.2/8', 'Young mice: PSLN-344(Y) vs PSLN-212(Y) survival (S09-B, D, F)', '; '.join(f"{bb}: {surv(bb,'PSLN-344(Y)')[0]}/8 vs {surv(bb,'PSLN-212(Y)')[0]}/8" for bb in ['S09-B', 'S09-D', 'S09-F']), 'S09!A11:D88', 'count')
# ---------------- tolerability / safety ----------------
d = b[(b.block == 'S08-D') & (b.day > 0)]
nad = d.groupby(['group', 'animal']).value.min().groupby('group').agg(['mean', 'std'])
add('C50', '3.3', 'Post-vaccination weight nadir (% d0): PSLN-344 vs vaccine alone vs PSLN-212/R848',
    f"{nad.loc['PSLN-344','mean']:.1f}+/-{nad.loc['PSLN-344','std']:.1f} vs {nad.loc['Vaccine','mean']:.1f}+/-{nad.loc['Vaccine','std']:.1f} vs {nad.loc['PSLN-212/R848','mean']:.1f}+/-{nad.loc['PSLN-212/R848','std']:.1f}",
    'S08!B21:AE26', 'per-animal minimum over d2-d10; mean+/-SD')
for an in ['Ifnb1', 'Tnf', 'Isg15']:
    x = v(f'S10-A_{an}', 'PSLN-344'); p = v(f'S10-A_{an}', 'PBS'); ct = v(f'S10-A_{an}', 'CT')
    from statsmodels.stats.multicomp import pairwise_tukeyhsd
    dd = t[t.block == f'S10-A_{an}']; tk = pairwise_tukeyhsd(np.log10(dd.value), dd.group); tb = pd.DataFrame(tk._results_table.data[1:], columns=tk._results_table.data[0])
    tp = float(tb[((tb.group1 == 'PBS') & (tb.group2 == 'PSLN-344')) | ((tb.group1 == 'PSLN-344') & (tb.group2 == 'PBS'))]['p-adj'].iloc[0])
    add(f'C51-{an}', '3.3', f'CNS {an} 36 h: PBS vs PSLN-344 vs cholera toxin (geometric means)', f'{gm(p):.2f} vs {gm(x):.2f} vs {gm(ct):.2f}; 344 vs PBS Student(log) p={stats.ttest_ind(np.log10(x),np.log10(p)).pvalue:.2g}; Tukey(log) p={tp:.2f}', f'S10-A: {cells("S10-A_"+an)}', 'geometric means; tests on log10 scale')
for an in ['Il6', 'Tnf', 'Ccl2']:
    x = v('S09-A_blk2(Y:AS)', 'PSLN-344', analyte=an)
    add(f'C52-{an}', '3.3', f'S09-A 2nd panel (labelled 16 h, matches 72 h) PSLN-344 lung {an} fold', f'{10**x.mean():.1f}', f'S09-A panel 2: {cells("S09-A_blk2(Y:AS)")}', '10^mean(log10)')
ee = t[t.block == 'S08-B']
add('C53', '1/2', 'Encapsulation efficiency (A260) PSLN-344; PSLN-R848 (contains no CDN-1807)', f"{ee[ee.group=='PSLN-344'].value.mean():.1f}+/-{ee[ee.group=='PSLN-344'].value.std():.1f}; {ee[ee.group=='PSLN-R848'].value.mean():.1f}", 'S08!A10:O11', 'mean+/-SD, n=3')
# ---------------- comparators ----------------
for blk, lab, fl in [('S03-C', 'HAI CA09', 5), ('S03-A', 'IgG CA09', None), ('S01-A_16h', 'Ifnb1 16 h', None)]:
    c = v(blk, 'PSLN-344'); m = v(blk, 'CMP-204')
    if fl: c, m = np.where(c <= 0, fl, c), np.where(m <= 0, fl, m)
    add(f'C54-{lab}', '9', f'PSLN-344 vs CMP-204 (cGAMP liposome): {lab}', f'x{gm(c)/gm(m):.1f}', f'{blk}: {cells(blk)}', 'ratio of geometric means')
for an in ['Il10', 'Tnf']:
    x = v('S09-A_blk1(B:V)', 'PSLN-212/R848', analyte=an)
    add(f'C55-{an}', '9', f'PSLN-212/R848 lung {an} 16 h fold', f'{10**x.mean():.0f}', f'S09-A panel 1: {cells("S09-A_blk1(B:V)")}', '10^mean(log10)')
# ---------------- integrity ----------------
c6 = s[s.block == 'S06-C'].sort_values(['group', 'day']).reset_index(); d6 = s[s.block == 'S06-D'].sort_values(['group', 'day']).reset_index()
add('C56', '4', 'S06-D rows identical to S06-C', f"{int(((c6.day.values==d6.day.values)&(c6.event.values==d6.event.values)&(c6.group.values==d6.group.values)).sum())}/{len(c6)}", 'S06!M3:Q30 vs S06!A34:E61', 'row-wise comparison')
a = t[t.block == 'S11-A']; n = t[t.block == 'S11-B']; m = a.merge(n, on=['group', 'time', 'rep'])
add('C57', '4', 'S11-A vs S11-B identical position-matched values', f"{int(np.isclose(m.value_x,m.value_y).sum())}/{len(m)}", 'S11!B3:U7 vs S11!B10:U14', 'position-matched equality')
r344 = (v('S13-A', 'PSLN-344') / v('S13-B', 'PSLN-344')).mean(); r212 = (v('S13-A', 'PSLN-212') / v('S13-B', 'PSLN-212')).mean()
add('C58', '4', 'IgG2a:IgG1 (CA09) recomputed from S13-A/B: PSLN-344 vs PSLN-212; S03-B printed values for the same labels',
    f"{r344:.2f} vs {r212:.2f}; S03-B printed: PSLN-344 {v('S03-B','PSLN-344').mean():.2f}, PSLN-212 {v('S03-B','PSLN-212').mean():.2f}", 'S13!A2:G7; S03!G2:I7', 'mean of per-animal ratios')
x = b[(b.block == 'S15-C') & (b.group == 'PSLN-344') & (b.day.between(2, 12))].set_index(['animal', 'day']).value
y = b[(b.block == 'S15-I') & (b.group == '3d Vaccine+PSLN-344') & (b.day.between(2, 12))].set_index(['animal', 'day']).value
cc = x.index.intersection(y.index)
add('C59', '4', 'S15-C PSLN-344 weights identical to S15-I vaccine+PSLN-344 (d2-d12)', f'{int(np.isclose(x[cc],y[cc]).sum())}/{len(cc)}', 'S15!W24:AC29 vs S15!W73:AC78', 'position-matched equality')
ex = pd.read_csv('/tmp/work/bw_dup_exact.csv'); sg = pd.read_csv('/tmp/work/bw_dup_signatures.csv')
add('C60', '4', 'Body-weight values reused across experiments', f'{ex.shared_value.nunique()} distinct values in {len(ex)} cells; {sg.signature.nunique()} shared fractional signatures', 'see ET9, ET10', 'exact match of >1-dp values; sub-0.1 fractional part match')
pd.DataFrame(C).to_csv('/tmp/work/claims_index.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 140)
print(pd.DataFrame(C)[['ID', 'Claim', 'Recomputed_value']].to_string(index=False))
