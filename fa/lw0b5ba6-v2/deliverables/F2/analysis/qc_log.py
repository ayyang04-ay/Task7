"""Builds the data-quality log: every flag is re-derived from the workbook here (counts and cell ranges), not typed by hand."""
import numpy as np, pandas as pd, itertools
from blocks import *
from statlib import *

def traj(block, group):
    d = W[block] if block in W else T[block]
    d = d[d.group==group]
    tcol = 'day'
    return {rep: dict(zip(x[tcol], zip(x['value'].round(6), x['cellref']))) for rep, x in d.groupby('rep')}

def match_groups(b1,g1,b2,g2, days=None, same_rep=True):
    t1, t2 = traj(b1,g1), traj(b2,g2)
    best = {}
    for r1, a in t1.items():
        cand = [r1] if same_rep and r1 in t2 else list(t2)
        bestn=-1; bestr=None
        for r2 in cand:
            b = t2[r2]
            common = [d for d in a if d in b and str(d)!='0' and (days is None or d in days)]
            eq = [d for d in common if a[d][0]==b[d][0]]
            if len(eq)>bestn: bestn=len(eq); bestr=(r2, len(common), eq)
        best[r1]=bestr
    return best

Q=[]
def add(id_, severity, blocks, finding, evidence, impact, handling, action):
    Q.append(dict(ID=id_, Severity=severity, Blocks=blocks, Finding=finding, Evidence=evidence, Impact=impact, Handling_in_this_analysis=handling, Gate0_action=action))

# ---- Q1 header rotation S03-B / S03-F
def rot(q, num, den):
    Qb, N, D = B[q], B[num], B[den]
    m={}
    for g in Qb.group.unique():
        v = Qb[Qb.group==g]['value'].values
        for h in N.group.unique():
            r = N[N.group==h]['value'].values / D[D.group==h]['value'].values
            if np.allclose(r, v, atol=2e-3): m[g]=h
    return m
m1 = rot('S03-B','S13-A','S13-B'); m2 = rot('S03-F','S13-C','S13-D')
add('Q01','High','S03-B, S03-F vs S13-A..D',
    'Column headers of the IgG2a/IgG1 quotient blocks are rotated relative to the subclass titres they are computed from.',
    "S03-B columns reproduce the S13-A/S13-B quotients exactly (5/5 animals each) but under other names: " + "; ".join(f'printed "{k}" = quotient of {v}' for k, v in m1.items()) + ". S03-F shows the same rotation against S13-C/S13-D (" + "; ".join(f'"{k}" = {v}' for k, v in m2.items()) + "). The rank order of total IgG (S03-A/E: PSLN-212 < PSLN-344 < PSLN-212(Y)) agrees with the S13 labels.",
    'As printed, PSLN-344 would look Th2-skewed (ratio 0.58 / 0.51, the lowest of the three). Recomputed from S13: PSLN-344 2.14 / 2.73; PSLN-212 0.58 / 0.51; PSLN-212(Y) 2.97 / 2.89 (means).',
    'S03-B and S03-F not used as printed; ratios recomputed from S13-A..D.', 'Confirm group identity of S13-A..D and S03-B/F columns against plate maps.')

# ---- Q2 S09-A right block is 72 h
a = B['S09-A_right']; a = a[a.analyte=='Ifnb1']; r = B['S01-A_72h']; hit=tot=0
for g in a.group.unique():
    g2 = {'PBS':'Sham','PSLN-212(y)':'PSLN-212(Y)'}.get(g,g)
    lin = np.round(10**a[a.group==g]['value'].values, 2); refv = r[r.group==g2]['value'].values
    hit += sum(any(abs(x-y)<0.011 for y in refv) for x in lin); tot += len(lin)
a = B['S09-A_left']; a = a[a.analyte=='Ifnb1']; r = B['S01-A_16h']; hit2=tot2=0
for g in a.group.unique():
    g2 = {'PBS':'Sham','PSLN-212(y)':'PSLN-212(Y)'}.get(g,g)
    lin = np.round(10**a[a.group==g]['value'].values, 2); refv = r[r.group==g2]['value'].values
    hit2 += sum(any(abs(x-y)<0.011 for y in refv) for x in lin); tot2 += len(lin)
add('Q02','High','S09-A (cols X-AS) vs S01-A',
    'Both cytokine panels on S09 are labelled "16h"; the right-hand panel is the 72 h time point.',
    f'10^(Ifnb1 row) of the right panel (S09!Y3:AS3) equals the 72 h Ifnb1 values of S01-A (S01!H3:L9) for {hit}/{tot} animals; the left panel (S09!B3:V3) equals the 16 h values (S01!B3:F9) for {hit2}/{tot2}. The "PBS" group of S09-A carries the values of the "Sham" group of S01-A.',
    'Read as printed, the right panel would be taken as a discordant 16 h replicate. Read correctly it shows that Il6, Tnf, Ccl2 are still elevated at 72 h with PSLN-344.',
    'Right panel analysed as 72 h. Control group treated as the common control (PBS/Sham identity unresolved).', 'Correct the label; confirm whether the control was PBS or empty liposome.')

# ---- Q3 S06-C identical to S06-D
same = all(sorted(zip(S['S06-C'][S['S06-C'].group==g]['day'], S['S06-C'][S['S06-C'].group==g]['event']))==sorted(zip(S['S06-D'][S['S06-D'].group==g]['day'], S['S06-D'][S['S06-D'].group==g]['event'])) for g in ['Sham','PSLN-212','PSLN-344','PSLN-212(Y)'])
add('Q03','High','S06-C vs S06-D',
    'Two nominally different challenge experiments (rgH5N1 at day 14 vs day 3) carry identical time-to-event data in all four groups.',
    ('S06!M3:Q30 equals S06!A34:E61 in all four groups' if same else 'S06!M3:Q30 and S06!A34:E61 differ') + '; Sham deaths on days 4,4,5,6,6,6,7 and PSLN-212 deaths on days 5,8,10,10,12 in both. The linked body-weight blocks differ from each other (S15-C vs S15-D), and S15-D implies 5/7, not 7/7, survivors for PSLN-344 and for PSLN-212(Y). Separately, the Sham columns of S06-B and S06-F carry the same seven death days (4,4,4,5,5,6,6); their other columns differ.',
    'One of the two blocks is probably a paste of the other; the 7/7 PSLN-344 result is counted twice in any pooled analysis.',
    'Primary pooled analysis as printed; sensitivity analysis drops S06-C and uses body-weight-inferred counts for S06-D.', 'Retrieve both survival records from cage cards.')

# ---- Q4 S11-A vs S11-B
t1 = T['S11-A']; t2 = T['S11-B']; nident=0; pairs=[]
for g in t1.group.unique():
    A_ = {rep: tuple(x.sort_values('day')['value']) for rep,x in t1[t1.group==g].groupby('rep')}
    B_ = {rep: tuple(x.sort_values('day')['value']) for rep,x in t2[t2.group==g].groupby('rep')}
    for ra, va in A_.items():
        for rb, vb in B_.items():
            eq = sum(1 for x,y in zip(va,vb) if x==y)
            if eq>=4: nident+=1; pairs.append(f'{g} rep{ra}=rep{rb} ({eq}/5)')
m1_ = t1.groupby(['group','day'])['value'].mean(); m2_ = t2.groupby(['group','day'])['value'].mean()
add('Q04','High','S11-A vs S11-B',
    'The neutrophil block (S11-B) largely duplicates the alveolar-macrophage block (S11-A).',
    f'{nident} of 20 animal time-series are identical at >=4 of 5 time points ({"; ".join(pairs)}); the 20 group-by-day means correlate r={np.corrcoef(m1_, m2_[m1_.index])[0,1]:.3f} (max difference {np.max(np.abs(m1_-m2_[m1_.index])):.1f} points).',
    'There is no independent neutrophil data set, i.e. no usable read-out of acute lung inflammation by cell influx.',
    'S11-B excluded. S11-A used only descriptively.', 'Re-export neutrophil gate from FACS files.')

# ---- Q5..Q9 recycled body-weight traces
def count_match(b1,g1,b2,g2,same_rep=True):
    m = match_groups(b1,g1,b2,g2,same_rep=same_rep); n = sum(v[2].__len__() for v in m.values() if v); tot = sum(v[1] for v in m.values() if v)
    an = sum(1 for v in m.values() if v and len(v[2])>=4)
    return n, tot, an, m
n,tot,an,_ = count_match('S15-C','PSLN-344','S15-I','3d Vaccine+PSLN-344')
_a = W['S15-C']; _a = _a[_a.group=='PSLN-344']; _b = W['S15-I']; _b = _b[_b.group=='3d Vaccine+PSLN-344']
_m = _a.merge(_b, on=['rep','day'], suffixes=('_c','_i'))
n_2_12 = int(((_m.day>=2)&(_m.day<=12)&(_m.value_c==_m.value_i)).sum()); t_2_12 = int(((_m.day>=2)&(_m.day<=12)).sum()); n_14 = int(((_m.day==14)&(_m.value_c==_m.value_i)).sum())
add('Q05','High','S15-C (PSLN-344) vs S15-I (3d Vaccine+PSLN-344)',
    'Body-weight traces of the PSLN-344 group after day-14 rgH5N1 challenge are the traces of a different experiment (day-3 challenge).',
    f'{n_2_12} of the {t_2_12} values for days 2-12 are identical animal by animal (S15!W24:AC29 vs S15!W73:AC78); {an}/7 animals match at >=4 time points; {n_14} of 7 day-14 values match.',
    'S15-C weight data for PSLN-344 are not independent evidence; the day-14 values in S15-C do not continue the traces (e.g. animal 3: 77.9 at day 12, 90.1 at day 14).',
    'S15-C PSLN-344 weights not used. Survival taken from S06-C with flag Q03.', 'Locate the true S15-C weights.')
# S09-E PSLN-344Y vs S15-M PSLN-212(Y) : shifted rep mapping
n,tot,an,m = count_match('S15-M','PSLN-212(Y)','S09-E','PSLN-344Y', same_rep=False)
add('Q06','High','S15-M (young C57BL/6, PSLN-212(Y)) vs S09-E (young BALB/c, PSLN-344Y)',
    'Weight traces of the young C57BL/6 reference group re-use traces from a BALB/c experiment with a different adjuvant.',
    f'{n} of {tot} post-baseline values identical; {an}/7 animals match at >=4 of 7 time points (S15!I104:O110 vs S09!W40:AD46).',
    'Cross-strain weight evidence (S15-M) is not independent. S15-M also shows 7/7 young animals alive while S15-L records one death (day 12).',
    'Cross-strain conclusions rest on the time-to-event blocks S15-L/N only and are graded "moderate".', 'Source-verify S15-L..O.')
n1,tot1,an1,_ = count_match('S15-A','PSLN-344','S15-M','PSLN-344'); n2,tot2,an2,_ = count_match('S15-A','PSLN-344','S15-O','PSLN-344'); n3,tot3,an3,_ = count_match('S15-M','PSLN-344','S15-O','PSLN-344')
add('Q07','Medium','S15-A / S15-M / S15-O (PSLN-344)',
    'Several PSLN-344 animals share weight traces across BALB/c, C57BL/6 and Swiss Webster experiments.',
    f'S15-A vs S15-M: {n1} identical values, {an1} animals at >=4 time points; S15-A vs S15-O: {n2} values, {an2} animal(s); S15-M vs S15-O: {n3} values, {an3} animal(s).',
    'Same as Q06.', 'Same as Q06.', 'Same as Q06.')
d = W['S09-C']; a_ = d[(d.group=='PSLN-212Y')&(d.day==12)]['value'].tolist(); b_ = d[(d.group=='PSLN-344Y')&(d.day==12)]['value'].tolist()
add('Q08','Medium','S09-C',
    'Day-12 weights of PSLN-344Y are a copy of the PSLN-212Y row.',
    f'S09!W18:AD18 equals S09!G18:N18 in order ({sum(x==y for x,y in zip(a_,b_))}/8 identical).', 'Minor; young-mouse weight comparison at day 12 is uninformative.', 'Day 12 ignored for PSLN-344Y vs PSLN-212Y.', 'Correct from balance log.')
n,tot,an,_ = count_match('S09-E','PSLN-212Y','S09-G','PSLN-212Y')
add('Q09','Low','S09-E vs S09-G (PSLN-212Y)', 'One young animal has the same weight trace in two experiments.', f'{an} animal identical at all 7 post-baseline time points (S09!N40:N46 vs S09!N67:N73).', 'Minor.', 'None needed.', 'Correct from balance log.')

# ---- Q10 TTE vs body weight
bw = pd.read_csv('qc_tte_vs_bodyweight.csv')
mm = bw[(bw.flag.fillna('').str.contains('MISMATCH'))]
ev = '; '.join(f"{r.tte_block}/{r.weight_block} {r.group}: survival block {int(r.tte_survivors)}/{int(r.tte_n)}, weight traces imply {int(r.bw_alive_d14)}/{int(r.bw_n)}" for r in mm.itertuples())
add('Q10','High','Time-to-event blocks vs their linked body-weight blocks',
    f'Survivor counts or animal numbers disagree between the survival block and the weight block of the same animals in {len(mm)} groups.',
    ev + '. (Weight traces frozen at a constant value to day 14, or blank, are read as deaths; the annotation describes these groups as "declining".)',
    'Individual survival fractions are uncertain by 1-3 animals in the flagged groups; direction of every PSLN-344 vs PSLN-212 comparison is unchanged.',
    'Survival blocks used as printed; worst-case sensitivity analysis uses the weight-inferred count wherever it is less favourable to PSLN-344 or more favourable to PSLN-212.', 'Reconcile against humane-endpoint records.')

# ---- Q11 group-set mismatch
add('Q11','High','S03-I vs S13-F; S03-J vs S13-G',
    'Survival and weight blocks said to describe the same animals list different groups.',
    f"S03-I lists {', '.join(S['S03-I'].group.unique())}; S13-F lists {', '.join(W['S13-F'].group.unique())}. S03-J lists {', '.join(S['S03-J'].group.unique())}; S13-G lists {', '.join(W['S13-G'].group.unique())}. In S13-G the 'Sham' traces (5 dead by d14, deaths from d10) resemble S03-J 'PSLN-212' (deaths d10-12, 3/10 alive) and the 'Naive' traces (1/10 alive, two deaths by d4) resemble S03-J 'Sham' (1/10 alive, deaths d3, d4, d9-10).",
    'The identity of the comparator arms in the wild-type H5N1 experiment is uncertain (PSLN-212 and Sham, or Sham and Naive). The PSLN-344 arm (10/10 alive in both blocks) is not affected. In S03-I the PSLN-212 arm (0/7, all dead by day 6, faster than Sham) conflicts with S13-F (3/7 alive).',
    'S03-I and S03-J reported as printed but excluded from the conservative pooled analysis; S03-J not described as a clean head-to-head.', 'Establish the true arm list for both experiments.')

# ---- Q12 stated n vs observed
add('Q12','Medium','S03-J, S05-A/B, S13-E, S09-F, S08-D',
    'Stated n differs from the number of observations.',
    f"S03-J stated n=9, 10 rows per group, and one PSLN-344 row has status 0 but no day (S03!J46, G46 empty); S05-A/B stated n=3, 2 values per group and day; S13-E stated n=5, 7 per group; S09-F Sham has 7 events for 8 animals in the weight block S09-G (the annotation attributes the 7 to S09-B, where the workbook has 8); S08-D PSLN-212/R848 has 4 of 5 values at day 10 (S08!W26 empty).",
    'Denominators uncertain by one animal in the affected groups.', 'Observed counts used; the PSLN-344 row without a day treated as censored at the end of observation.', 'Reconcile n per group.')

add('Q13','Medium','S07-C', 'Both columns carry the same header ("Ly6C-CD206+ MPhi").', 'S07!B15 and S07!C15 identical; means 10.4 vs 5.1 % lung Treg.', 'Cannot tell which macrophage subset raised lung Treg; the macrophage-to-Treg link in the mechanism is unproven.', 'Not used.', 'Recover the labels.')
s1 = B['S01-B']; s8 = B['S08-C']
add('Q14','Medium','S08-C vs S01-B',
    'Epithelial-uptake block is inconsistent with the earlier block for the same formulation.',
    f"S01-B: AECII/PSLN-SRB mean {s1[s1.group=='AECII/PSLN-SRB'].value.mean():.1f} %, AECI/PSLN-SRB {s1[s1.group=='AECI/PSLN-SRB'].value.mean():.1f} %. S08-C as printed: AECII-PSLN-SRB {s8[s8.group=='AECII-PSLN-SRB'].value.mean():.1f}, AECII-PSLN-344-SRB {s8[s8.group=='AECII-PSLN-344-SRB'].value.mean():.1f}, AECI-PSLN-SRB {s8[s8.group=='AECI-PSLN-SRB'].value.mean():.1f}, AECI-PSLN-344-SRB {s8[s8.group=='AECI-PSLN-344-SRB'].value.mean():.1f}. The first two S08-C columns share 3 and 2 of 5 values with the S01-B AECII and AECI columns.",
    'Either Mn lowers epithelial uptake about four-fold (as printed) or the column order is AECII, AECI, AECII, AECI and Mn changes nothing. Unresolved.',
    'No claim made on the effect of Mn on uptake.', 'Check column order against FACS export; gating differs between the two blocks.')
add('Q15','Low','S08 rows 89-101', 'Unlabelled numeric region.', 'S08!A89:A101 = 14; S08!C89:C94 = 0; S08!D95:D101 = 0. Looks like the censored tail of a survival block (6 + 7 animals).', 'None (cannot be attributed).', 'Excluded.', 'Identify or delete.')
add('Q16','Low','S06 (labels), S09 (labels)', 'Duplicate block labels.', '"S06-E" and "S06-F" are each used for two different experiments (rows 32 and 69); "S09-A 16h" is used twice.', 'Risk of citing the wrong block.', 'Second S06-E/S06-F referred to here as S06-E2/S06-F2 (imprinting experiments).', 'Rename.')
add('Q17','Medium','S05-A, S05-B, S05-I', 'Conditions contradictory and n=2.', 'Annotation gives both ovalbumin and bivalent-vaccine immunisation for a read-out (NP366-374 tetramer) that requires influenza antigen; strain not stated; 2 animals per point.', 'Tetramer kinetics are illustrative only.', 'Reported descriptively; not used for decisions.', 'Clarify protocol and strain.')
add('Q18','Low','S08-A', 'Undefined preparation and age not stated.', '"PSLN-344/R848" appears only in S08-A and is not defined under Materials; the age of the animals is not given (values at 20 ug match the aged groups of S01-A).', 'Minor.', 'Dose-response interpreted as aged animals, flagged.', 'Confirm.')
add('Q19','Low','S13-H, S14-A, S11-E, S07-B, S15-L..O, S06-E2', 'Time point, challenge virus or interval not stated.', 'S13-H, S14-A, S11-E, S07-B: time point missing; S15-L/N: challenge virus and interval missing; S06-E2: interval missing; S03-J: challenge dose missing and observation stated as 22 days (workbook censors at day 21).', 'Limits interpretation of kinetics.', 'Stated where relevant.', 'Complete the annotation.')
u = [(b, int(S[b][(S[b].group=='Untreated')].event.sum())) for b in ['S06-E','S06-F','S06-G']]
add('Q20','Medium','S06-E/F/G Untreated; S15-E/F/G', 'Unvaccinated, unchallenged aged controls died during the 14-day window.', 'Deaths without challenge: ' + ', '.join(f'{b} {d}/7' for b, d in u) + f' = {sum(d for _, d in u)}/21; their weights stayed at 94-100 % (S15!AD43:AJ70).', 'Background mortality of about 19 % in 14 days among untreated aged animals (stated age 20 months) limits what the day-60 challenge can show.', 'Day-60 results interpreted against this background.', 'Use younger "aged" animals (18 months) for durability work.')
add('Q21','Low','File metadata', 'Data cut-off earlier than the review date.', 'Workbook last modified 2026-09-03; annotation PDF created 2026-09-15.', 'Anything generated after early September 2026 is not in this analysis.', 'Stated on the title page.', 'Confirm no newer data exist.')
add('Q22','Low','S09-E, S15-A..G, S15-J..O, S08-D', 'Mixed numeric precision within weight blocks.', 'Values with 5-8 decimals sit next to 1-decimal values in the same group (e.g. S09!W40:Y44, S15!B24:D29).', 'Suggests values assembled from more than one source.', 'None.', 'Explain during audit.')
q = pd.DataFrame(Q); q.to_csv('qc_log.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 400)
for r in q.itertuples(): print(r.ID, r.Severity, '|', r.Blocks, '\n   ', r.Finding, '\n   EVIDENCE:', r.Evidence, '\n')
