# Recomputes every load-bearing figure in ../task/golden-response.md from the shipped
# workbook and diffs it against what the document states.
#
# Usage: python3 -I audit-golden.py   (expects ../data-room/adjuvant_program_dataset.xlsx alongside)
#
# Run this after any edit to the data room, per the build constraint that the
# golden is recomputed from the shipped room after its last edit. Exits noisily
# on any mismatch.

import openpyxl, statistics as st, math
wb=openpyxl.load_workbook('../data-room/adjuvant_program_dataset.xlsx',data_only=True)
def V(sh,cc,rr):
    ws=wb[sh]; return [float(ws.cell(r,c).value) for r in rr for c in cc
                       if isinstance(ws.cell(r,c).value,(int,float))]
def M(sh,cc,rr): return st.mean(V(sh,cc,rr))
fails=[]
def chk(label, got, claimed, tol=0.006):
    ok = abs(got-claimed) <= max(tol, abs(claimed)*tol)
    print('  %-52s computed %-10.4g claimed %-10.4g %s'%(label,got,claimed,'OK' if ok else '<<< MISMATCH'))
    if not ok: fails.append(label)

print('MECHANISM')
chk('S01-C WT',   M('S01',range(2,6),[20]), 43.10)
chk('S01-C SPA/D',M('S01',range(2,6),[21]), 12.65)
chk('S11-C CBX-',M('S11',[2],range(17,22)), 7.28)
chk('S11-C CBX+',M('S11',[1],range(17,22)), 3.08)
chk('S02-H WT',   M('S02',[2],range(30,35)), 19.70)
chk('S02-H IFNAR',M('S02',[4],range(30,35)), 2.09)
chk('S02-H rescue',M('S02',[6],range(30,35)), 12.40)
chk('S02-F 36h cand',M('S02',range(2,7),[18]), 8.74)
chk('S02-F 36h comp',M('S02',range(7,12),[18]), 1.59)
chk('S02-F 36h sham',M('S02',range(12,17),[18]), 1.21)
chk('S02-I cand',  M('S02',[8],range(30,35)), 6.77)
chk('S02-I +INCB', M('S02',[9],range(30,35)), 1.39)
chk('S07-B Mphi',  M('S07',[5],range(10,15)), 15.35)
chk('S07-B Mphi+INCB',M('S07',[6],range(10,15)), 2.52)
chk('S07-B mono',  M('S07',[2],range(10,15)), 9.86)
chk('S07-B mono+INCB',M('S07',[3],range(10,15)), 3.26)
chk('S05-C lung',  M('S05',[1],range(13,16)), 59.00)
chk('S05-C lung+PTX',M('S05',[2],range(13,16)), 55.07)
chk('S05-C MLN',   M('S05',[3],range(13,16)), 30.90)
chk('S05-C MLN+PTX',M('S05',[4],range(13,16)), 6.83)
print('  INCB lung cytotoxic CD8 fold-change: %.2f (golden says 4.9 and 6.1 on the two readouts)'%(6.77/1.39))

print('\nDAY-3')
chk('S05-A cand',M('S05',[5,6],[3]),6.68); chk('S05-A comp',M('S05',[2,3],[3]),2.09)
chk('S05-D cand',M('S05',[3],range(19,24)),9.38); chk('S05-D comp',M('S05',[2],range(19,24)),3.48)
chk('S05-E cand',M('S05',[3],range(26,31)),5.69); chk('S05-E comp',M('S05',[2],range(26,31)),2.99)

print('\n2x2 TABLE')
for lbl,sh,rr,cols,claims in (
  ('Ifnb1 16h','S01',[5,8,9,10],[range(2,7)]*4,[16.64,37.11,37.60,50.70]),
  ('Ifnb1 72h','S01',[5,8,9,10],[range(8,13)]*4,[3.43,4.43,1.59,3.13])):
    for r,cc,c in zip(rr,cols,claims): chk('%s row%d'%(lbl,r), M(sh,cc,[r]), c)
for lbl,rr,claims in (('S01-E d4',[32],[8.28,18.88,21.40,22.60]),('S01-F',[36],[22.80,37.52,43.42,44.26]),
                      ('S01-G',[38],[75.30,59.46,54.08,51.36])):
    for i,(g,c) in enumerate(zip([range(7,12),range(12,17),range(17,22),range(22,27)],claims)):
        chk('%s grp%d'%(lbl,i+1), M('S01',g,rr), c)
for lbl,rr,claims in (('S02-C',range(3,8),[1.77,7.09,9.39,11.12]),('S02-E',range(10,15),[0.77,18.65,26.24,31.40])):
    for cc,c in zip([[11],[12],[13],[15]],claims): chk('%s c%d'%(lbl,cc[0]), M('S02',cc,rr), c)

print('\nHUMORAL')
chk('S03-A cand',M('S03',[4],range(3,8)),7891.6,1e-4); chk('S03-A comp',M('S03',[3],range(3,8)),437.0,1e-4)
chk('S03-A ratio',M('S03',[4],range(3,8))/M('S03',[3],range(3,8)),18.06)
def geo(v): return 10**(sum(math.log10(x) for x in v if x>0)/len([x for x in v if x>0]))
chk('S03-C cand geo',geo(V('S03',[14],range(3,8))),367.58)
chk('S03-C comp geo',geo(V('S03',[13],range(3,8))),45.95)
chk('S03-C ratio',geo(V('S03',[14],range(3,8)))/geo(V('S03',[13],range(3,8))),8.00)
chk('S03-C cand arith',M('S03',[14],range(3,8)),416.0,1e-4)
chk('S03-C sham arith',M('S03',[11],range(3,8)),6.0,1e-4)

print('\nTOLERABILITY / DOSE')
chk('S08-D cand d10',M('S08',range(17,22),[26]),99.78)
chk('S08-D comp+R848 d10',M('S08',range(22,27),[26]),90.65)
chk('S08-A 20ug',M('S08',range(8,11),[6]),45.83); chk('S08-A 40ug',M('S08',range(8,11),[7]),50.23)

print('\n72h PANEL (10^mean log10)')
for i,(an,c) in enumerate(zip(['Ifnb1','Il6','Ccl2','Ccl3','Ccl5','Tnf','Il10'],
                              [4.01,7.19,27.41,9.23,2.01,8.44,4.16])):
    chk('S09-A b2 cand %s'%an, 10**M('S09',range(40,43),[3+i]), c)

print('\n18 ENDPOINTS')
E=[('Ifnb1 16h','S01',[8],range(2,7),[9],range(2,7)),('Ifnb1 72h','S01',[8],range(8,13),[9],range(8,13))]
vals={}
vals['Ifnb1 16h']=M('S01',range(2,7),[8])/M('S01',range(2,7),[9])
vals['Ifnb1 72h']=M('S01',range(8,13),[8])/M('S01',range(8,13),[9])
vals['Ly6C mono d4']=M('S01',range(12,17),[26])/M('S01',range(17,22),[26])
vals['AM d6']=M('S11',range(12,17),[6])/M('S11',range(17,22),[6])
vals['IgG H1N1']=M('S03',[4],range(3,8))/M('S03',[5],range(3,8))
vals['IgG H3N2']=M('S03',[4],range(10,15))/M('S03',[5],range(10,15))
vals['HAI H1N1']=geo(V('S03',[14],range(3,8)))/geo(V('S03',[15],range(3,8)))
# Roster row 8 was hard-coded as 2.1438/2.9718, so it was not derived from the workbook
# at all. Recomputed here: per-animal IgG2a over IgG1 from S13-A and S13-B, then the
# group mean of those ratios, which is the reduction the golden names for this row. The
# correct pairing is used, i.e. the one the subclass-sum argument below forces.
def _per_animal_ratio(num_col, den_col, rr=range(3,8)):
    sh=wb['S13']
    return st.mean([float(sh.cell(r,num_col).value)/float(sh.cell(r,den_col).value) for r in rr])
_ig_aged_cand  = _per_animal_ratio(2, 6)   # S13-A / S13-B, PSLN-344 column
_ig_young_par  = _per_animal_ratio(3, 7)   # S13-A / S13-B, PSLN-212(Y) column
chk('S13 IgG2a:IgG1 aged+cand  (per animal)', _ig_aged_cand, 2.1438, 1e-3)
chk('S13 IgG2a:IgG1 young+parent (per animal)', _ig_young_par, 2.9718, 1e-3)
vals['IgG2a:IgG1']=_ig_aged_cand/_ig_young_par
vals['GC B']=M('S03',[14],range(17,22))/M('S03',[15],range(17,22))
vals['ICOS Tfh']=M('S04',range(7,12),[4])/M('S04',range(7,12),[5])
vals['Tfr']=M('S04',[3],range(8,13))/M('S04',[4],range(8,13))
vals['NP d3']=M('S05',[5,6],[3])/M('S05',[8,9],[3])
vals['NP d7']=M('S05',[5,6],[5])/M('S05',[8,9],[5])
vals['Ki67']=M('S05',[3],range(19,24))/M('S05',[4],range(19,24))
vals['GZMB']=M('S05',[3],range(26,31))/M('S05',[4],range(26,31))
vals['IFNg d14']=M('S05',[3],range(33,38))/M('S05',[4],range(33,38))
vals['IFNg d60']=M('S05',[3],range(40,45))/M('S05',[4],range(40,45))
vals['TRM']=M('S05',[3],range(54,59))/M('S05',[4],range(54,59))
for k,v in vals.items(): print('   %-14s %.4f'%(k,v))
# Every one of the eighteen, diffed against the ratio column the golden prints. Printing
# is not checking: the earlier version printed all eighteen and asserted only min and
# max, so the middle fourteen could drift silently, and the humoral/cellular means would
# not catch compensating errors.
ROSTER = {'Ifnb1 16h':0.987,'Ifnb1 72h':2.785,'Ly6C mono d4':0.948,'AM d6':0.661,
          'IgG H1N1':0.618,'IgG H3N2':0.406,'HAI H1N1':0.758,'IgG2a:IgG1':0.721,
          'GC B':0.666,'ICOS Tfh':0.752,'Tfr':1.517,'NP d3':0.678,'NP d7':0.941,
          'Ki67':0.944,'GZMB':0.592,'IFNg d14':0.693,'IFNg d60':0.687,'TRM':0.656}
chk('roster size', len(vals), 18, 1e-9)
assert set(vals)==set(ROSTER), 'roster membership changed: %s'%(set(vals)^set(ROSTER))
for k,c in ROSTER.items(): chk('roster %s'%k, vals[k], c, 1e-3)
hib=[v for k,v in vals.items() if k not in ('Ifnb1 72h','Tfr')]
print('  higher-is-better: n=%d  min %.4f  max %.4f'%(len(hib),min(hib),max(hib)))
chk('higher-is-better count', len(hib), 16, 1e-9)
chk('higher-is-better min', min(hib), 0.406, 1e-3)
chk('higher-is-better max', max(hib), 0.987, 1e-3)
assert max(hib) < 1.0, 'golden says all sixteen higher-is-better endpoints fall below 1.0'
assert min(vals['Ifnb1 72h'], vals['Tfr']) > 1.0, 'golden says both higher-is-worse endpoints sit above 1.0'
# "Three endpoints are effectively matched (0.95, 0.94, 0.94)" -- never checked, and the
# claim is about which three, not just that three exist.
_matched = sorted(k for k,v in vals.items()
                  if k not in ('Ifnb1 72h','Tfr','Ifnb1 16h') and v > 0.93)
chk('effectively-matched count', len(_matched), 3, 1e-9)
assert set(_matched)=={'Ly6C mono d4','NP d7','Ki67'}, \
    'golden names monocyte recruitment d4, day-7 NP CD8 and CD8 proliferation: got %s'%_matched
print('\nADJUVANT EFFECT WITHIN COHORT (PSLN-344 / PSLN-212)')
# Checks the golden's claim that six of the seven readouts rise in aged animals, that
# the five priming readouts span 1.65 to 24.35 aged and 1.02 to 1.35 young, and that
# the sixth, the 72 h interferon residual, is the one where the young gain is larger.
four_arm = [
  ('Ifnb1 16h',  [M('S01',range(2,7),[r]) for r in (5,8,9,10)],  'priming'),
  ('Ifnb1 72h',  [M('S01',range(8,13),[r]) for r in (5,8,9,10)], 'residual'),
  ('CD11b+ DC',  [M('S01',g,[32]) for g in (range(7,12),range(12,17),range(17,22),range(22,27))], 'priming'),
  ('cDC1 72h',   [M('S01',g,[36]) for g in (range(7,12),range(12,17),range(17,22),range(22,27))], 'priming'),
  ('cDC2 72h',   [M('S01',g,[38]) for g in (range(7,12),range(12,17),range(17,22),range(22,27))], 'down'),
  ('node DC',    [M('S02',cc,range(3,8)) for cc in ([11],[12],[13],[15])], 'priming'),
  ('OT-I',       [M('S02',cc,range(10,15)) for cc in ([11],[12],[13],[15])], 'priming'),
]
prim_a=[]; prim_y=[]; raised=0
for lbl,v,kind in four_arm:
    ra, ry = v[1]/v[0], v[3]/v[2]
    print('   %-11s aged %7.2f  young %7.2f  (%s)'%(lbl,ra,ry,kind))
    if ra > 1: raised += 1
    if kind=='priming': prim_a.append(ra); prim_y.append(ry)
    if kind=='residual': res_a, res_y = ra, ry
chk('readouts raised in aged', raised, 6, 1e-9)
chk('priming aged min', min(prim_a), 1.65, 1e-2); chk('priming aged max', max(prim_a), 24.35, 1e-2)
chk('priming young min', min(prim_y), 1.02, 1e-2); chk('priming young max', max(prim_y), 1.35, 1e-2)
chk('residual aged', res_a, 1.29, 1e-2); chk('residual young', res_y, 1.97, 1e-2)
assert res_y > res_a, 'golden says the young gain is larger on the 72h residual'

print('\n2x2 SIGNIFICANCE (Ifnb1 16h, S01-A, Welch t)')
# The golden's age-specificity claim was corrected after an independent run pointed
# out that PSLN-344 also raises the young response significantly. These three p-values
# are what the corrected claim rests on, so they are checked rather than asserted.
def _ibeta(a,b,x):
    if x<=0: return 0.0
    if x>=1: return 1.0
    def cf(a,b,x):
        qab,qap,qam=a+b,a+1,a-1; c=1.0; d=1-qab*x/qap
        d=1/d if abs(d)>1e-30 else 1e30; h=d
        for mm in range(1,300):
            m2=2*mm; aa=mm*(b-mm)*x/((qam+m2)*(a+m2))
            d=1+aa*d; c=1+aa/c
            d=1/d if abs(d)>1e-30 else 1e30; h*=d*c
            aa=-(a+mm)*(qab+mm)*x/((a+m2)*(qap+m2))
            d=1+aa*d; c=1+aa/c
            d=1/d if abs(d)>1e-30 else 1e30; de=d*c; h*=de
            if abs(de-1)<3e-16: break
        return h
    lb=math.lgamma(a+b)-math.lgamma(a)-math.lgamma(b)+a*math.log(x)+b*math.log(1-x)
    return math.exp(lb)*cf(a,b,x)/a if x<(a+1)/(a+b+2) else 1-math.exp(lb)*cf(b,a,1-x)/b
def welch_p(a,b):
    na,nb=len(a),len(b); va,vb=st.variance(a),st.variance(b)
    t=(st.mean(a)-st.mean(b))/math.sqrt(va/na+vb/nb)
    df=(va/na+vb/nb)**2/((va/na)**2/(na-1)+(vb/nb)**2/(nb-1))
    return _ibeta(df/2,0.5,df/(df+t*t))
_arm={k:V('S01',range(2,7),[r]) for k,r in (('aged+nS',5),('aged+AM',8),('young+nS',9),('young+AM',10))}
for lbl,x,y,claim in (('age deficit  aged+nS vs young+nS','aged+nS','young+nS',None),
                      ('restoration  aged+AM vs young+nS','aged+AM','young+nS',0.857),
                      ('aged+AM vs young+AM','aged+AM','young+AM',0.012),
                      ('young gain   young+nS vs young+AM','young+nS','young+AM',0.014)):
    pv=welch_p(_arm[x],_arm[y])
    print('   %-36s p = %.3g  (%.2f vs %.2f)'%(lbl,pv,st.mean(_arm[x]),st.mean(_arm[y])))
    if claim is None:
        # The golden says "p < 0.0001" here. The earlier check was chk(..., 0.0, 2e-3),
        # which passes anything below 0.002 -- so the "< 0.0001" assertion was never
        # actually tested. Test the inequality the document states.
        ok = pv < 1e-4
        print('  %-52s computed %-10.3g claimed < 1e-4   %s'%(lbl,pv,'OK' if ok else '<<< MISMATCH'))
        if not ok: fails.append(lbl)
    else:
        chk(lbl, pv, claim, 2e-3)
assert welch_p(_arm['young+nS'],_arm['young+AM'])<0.05, \
    'the golden now says PSLN-344 raises the young response significantly'

print('\nS15-H: does the package exclude a non-specific antiviral state?')
# The golden now asserts that adjuvant alone protects nobody at the 3-day interval,
# which is what retires the alternative. Recomputed here because that claim is
# load-bearing for the mechanism section.
_s = wb['S15']
for ci, arm, exp_surv, exp_deaths in ((2,'3d Vaccine',0,[4,5,5,5,6,6,7]),
                                      (3,'3d PSLN-344',0,[5,5,6,6,6,7,8]),
                                      (4,'3d Vaccine+PSLN-344',6,[12])):
    ev=[(_s.cell(r,1).value,_s.cell(r,ci).value) for r in range(73,101) if _s.cell(r,ci).value is not None]
    deaths=sorted(t for t,e in ev if e==1); surv=sum(1 for _,e in ev if e==0)
    print('   %-20s n=%d  survive %d  deaths on %s'%(arm,len(ev),surv,deaths))
    chk('S15-H %s survivors'%arm, surv, exp_surv, 1e-9)
    assert deaths==exp_deaths, 'S15-H %s death days %s != %s'%(arm,deaths,exp_deaths)

hum=[vals[k] for k in ['IgG H1N1','IgG H3N2','HAI H1N1','IgG2a:IgG1','GC B','ICOS Tfh']]
cel=[vals[k] for k in ['NP d3','NP d7','Ki67','GZMB','IFNg d14','IFNg d60','TRM']]
chk('humoral mean (6)',st.mean(hum),0.654); chk('cellular mean (7)',st.mean(cel),0.741)

# ---------------------------------------------------------------------------
# PROTECTION SECTION
#
# This whole section was absent until an independent audit pointed out that the
# script checked no survival percentage and no log-rank p-value anywhere -- i.e.
# nothing in the build pipeline verified the golden's single most load-bearing
# argument. Mantel-Cox, standard treatment: a risk set of one still contributes to
# the expectation but contributes zero variance, which is the edge case that makes a
# naive implementation disagree with these numbers on two cells.
print('\nPROTECTION: survival and log-rank')

def arms(sheet, label_cell, day_col, first_arm_col, narms, r0, r1):
    sh = wb[sheet]
    out = []
    for i in range(narms):
        c = first_arm_col + i
        ev = [(sh.cell(r, day_col).value, sh.cell(r, c).value)
              for r in range(r0, r1 + 1) if sh.cell(r, c).value is not None]
        out.append([(t, int(e)) for t, e in ev if isinstance(t, (int, float))])
    return out

def logrank(a, b):
    times = sorted({t for t, e in a + b if e == 1})
    O, E, V = 0.0, 0.0, 0.0
    for t in times:
        na = sum(1 for x, _ in a if x >= t); nb = sum(1 for x, _ in b if x >= t)
        n = na + nb
        if n == 0: continue
        da = sum(1 for x, e in a if x == t and e == 1)
        d = da + sum(1 for x, e in b if x == t and e == 1)
        if d == 0: continue
        O += da; E += d * na / n
        if n > 1:
            V += d * (na / n) * (1 - na / n) * (n - d) / (n - 1)
    if V == 0: return None
    chi = (O - E) ** 2 / V
    return math.erfc(math.sqrt(chi / 2))

def surv(arm): return sum(1 for _, e in arm if e == 0)

# Every cell of the golden's log-rank table and every survival fraction, diffed against
# the printed value. The earlier version asserted only `p_par <= 0.0151` and
# `p_young >= 0.0597`, i.e. range membership -- a block drifting from 0.0083 to 0.0001
# would have passed -- and printed the survival fractions without checking any of them,
# though that table is the most-quoted thing in the document. An independent audit
# flagged both. Columns: label, header row, first arm col, row range, then the claimed
# cand-vs-parent p, cand-vs-young p (None where the arms are identical),
# parent-vs-sham p, and the claimed survivor counts for cand / parent / sham.
SIX = [('S06-A', 1,  2,  3,  30, 0.0083, 0.317, 0.0267, 6, 1, 0),
       ('S06-B', 1,  8,  3,  30, 0.0009, 0.141, 0.088,  5, 0, 0),
       ('S06-C', 1,  14, 3,  30, 0.0068, None,  0.0024, 7, 2, 0),
       ('S06-E', 33, 8,  34, 68, 0.0016, 0.141, 0.111,  5, 0, 0),
       ('S06-F', 33, 14, 34, 68, 0.0094, 0.141, 0.066,  5, 1, 0),
       ('S06-G', 70, 2,  71, 105, 0.0151, 0.060, 0.0063, 4, 0, 0)]
for lbl, hdr, acol, r0, r1, c_par, c_young, c_psham, n_cand, n_par, n_sham in SIX:
    sham, parent, cand, young = arms('S06', hdr, acol - 1, acol, 4, r0, r1)
    p_sham  = logrank(cand, sham)
    p_par   = logrank(cand, parent)
    p_young = logrank(cand, young)
    p_parent_sham = logrank(parent, sham)
    print('   %-6s PSLN-344 %d/%d  parent %d/%d  sham %d/%d  young %d/%d  | vs sham %s  vs parent %s  vs young %s  | parent vs sham %s'
          % (lbl, surv(cand), len(cand), surv(parent), len(parent), surv(sham), len(sham),
             surv(young), len(young),
             '%.4f' % p_sham if p_sham else 'n/a',
             '%.4f' % p_par if p_par else 'n/a',
             '%.4f' % p_young if p_young else 'identical',
             '%.4f' % p_parent_sham if p_parent_sham else 'n/a'))
    # n = 7 per arm throughout, which the golden states and nothing checked.
    for nm, a in (('cand', cand), ('parent', parent), ('sham', sham), ('young', young)):
        chk('%s %s n' % (lbl, nm), len(a), 7, 1e-9)
    chk('%s survivors cand' % lbl,   surv(cand),   n_cand, 1e-9)
    chk('%s survivors parent' % lbl, surv(parent), n_par,  1e-9)
    chk('%s survivors sham' % lbl,   surv(sham),   n_sham, 1e-9)
    chk('%s PSLN-344 vs sham' % lbl, p_sham, 0.0002, 1e-4)
    chk('%s PSLN-344 vs parent' % lbl, p_par, c_par, 5e-4)
    # The whole parent-vs-sham row. Nothing computed it, and it carries the
    # Recommendation's claim that the manganese rather than the liposome does the work:
    # the parent fails to separate from vaccine alone in three of the six.
    chk('%s parent vs sham' % lbl, p_parent_sham, c_psham, 1e-3)
    if c_young is None:
        assert p_young is None, '%s: golden says the cand and young arms are identical' % lbl
    else:
        chk('%s PSLN-344 vs young' % lbl, p_young, c_young, 1e-3)
_par_fails = [s[0] for s in SIX if s[7] > 0.05]   # s[7] is the claimed parent-vs-sham p
chk('parent fails to separate from sham in N of 6', len(_par_fails), 3, 1e-9)
print('   parent does not separate from sham in: %s' % ', '.join(_par_fails))

# S06-D duplicates S06-C exactly, which is why the golden collapses it.
c_arms = arms('S06', 1, 13, 14, 4, 3, 30)
d_arms = arms('S06', 32, 1, 2, 4, 34, 61)
assert c_arms == d_arms, 'S06-D is no longer identical to S06-C'
print('   S06-C and S06-D: all %d time-and-event pairs identical' % sum(len(a) for a in c_arms))

# The S06-G ceiling reading: an age-matched arm that met no virus did no better.
g = arms('S06', 70, 1, 2, 5, 71, 105)
cand_g, untr_g = g[2], g[4]
p_untr = logrank(cand_g, untr_g)
print('   S06-G PSLN-344 %d/%d vs untreated %d/%d  p = %.4f'
      % (surv(cand_g), len(cand_g), surv(untr_g), len(untr_g), p_untr))
chk('S06-G PSLN-344 vs untreated', p_untr, 0.855, 2e-3)
chk('S06-G untreated survivors', surv(untr_g), 4, 1e-9)

# S15-L and S15-N: no stated challenge virus, both favourable, neither in the six.
for lbl, hdr in (('S15-L', 102), ('S15-N', 133)):
    sham, parent, cand = arms('S15', hdr, 1, 2, 3, hdr + 1, hdr + 30)
    print('   %-6s PSLN-344 %d/%d  parent %d/%d  sham %d/%d' % (lbl, surv(cand), len(cand),
          surv(parent), len(parent), surv(sham), len(sham)))
    chk('%s PSLN-344 survivors' % lbl, surv(cand), 6, 1e-9)
    chk('%s sham survivors' % lbl, surv(sham), 0, 1e-9)

# S03-J: the header says n=9 and every arm holds 10. The annotation used to say 9.
sh = wb['S03']
for col, name, exp in (('H', 'Sham', 1), ('I', 'PSLN-212', 3), ('J', 'PSLN-344', 10)):
    rows = [r for r in range(17, 47) if sh['%s%d' % (col, r)].value is not None]
    cens = sum(1 for r in rows if sh['%s%d' % (col, r)].value == 0)
    print('   S03-J %-8s %d observations, %d censored' % (name, len(rows), cens))
    chk('S03-J %s observations' % name, len(rows), 10, 1e-9)
    chk('S03-J %s censored' % name, cens, exp, 1e-9)

# ---------------------------------------------------------------------------
# GAP CLOSURE
#
# A second independent reference audit enumerated 24 load-bearing claims in the golden
# that this script did not cover. The tightened checks above close the "too loose" and
# "printed but not diffed" classes. This section closes the "not computed at all" class.
# Each block names the golden claim it protects, because a check whose claim has moved
# is a second, conflicting standard rather than a safeguard.
print('\nGAP CLOSURE')

# "Nine challenge blocks sit on the S06 sheet" -- the denominator the whole heterosubtypic
# derivation starts from, and nothing counted it.
import re as _re
_s06 = wb['S06']
_labels = [(c.row, c.column, _re.search(r'\bS06-[A-Z]\b', c.value).group(0))
           for row in _s06.iter_rows() for c in row
           if isinstance(c.value, str) and _re.search(r'\bS06-[A-Z]\b', c.value)]
print('   S06 label cells: %s' % ', '.join('%s@r%dc%d' % (l, r, cc) for r, cc, l in _labels))
chk('S06 challenge block label cells', len(_labels), 9, 1e-9)
chk('S06 distinct printed labels', len({l for _, _, l in _labels}), 7, 1e-9)

# "S06-C and S06-D: all 28 time-and-event pairs identical" -- the identity was asserted
# but the count 28 was only interpolated into a print string.
chk('S06-C/S06-D pair count', sum(len(a) for a in c_arms), 28, 1e-9)

# S06-E and S06-F: the candidate arm sits one and two animals below the unvaccinated
# unchallenged arm and the test cannot resolve gaps that small. Only S06-G's untreated
# comparison was checked.
for lbl, hdr, acol, r0, r1, gap, claim in (('S06-E', 33, 8, 34, 68, 1, 0.5937),
                                           ('S06-F', 33, 14, 34, 68, 2, 0.1414)):
    a = arms('S06', hdr, acol - 1, acol, 5, r0, r1)
    cand_, untr_ = a[2], a[4]
    p = logrank(cand_, untr_)
    print('   %-6s cand %d/%d vs untreated %d/%d  p = %.4f' % (lbl, surv(cand_), len(cand_),
                                                               surv(untr_), len(untr_), p))
    chk('%s untreated survivors' % lbl, surv(untr_), surv(cand_) + gap, 1e-9)
    chk('%s cand vs untreated' % lbl, p, claim, 2e-3)
    assert p > 0.05, '%s: golden says the test cannot resolve a gap that small' % lbl

# The imprinting blocks at S06 rows 69-105: the stated reason the two re-used labels are
# retained for the imprinting question is that both candidate arms run 85.7% whether or
# not the animals had prior exposure.
for lbl, daycol in (('PR8 block', 7), ('Perth block', 13)):
    sh = wb['S06']
    got = {}
    for c in range(daycol + 1, daycol + 5):
        nm = sh.cell(70, c).value
        ev = [(sh.cell(r, daycol).value, sh.cell(r, c).value) for r in range(71, 106)
              if sh.cell(r, c).value is not None]
        got[nm] = sum(1 for _, e in ev if e == 0), len(ev)
    print('   %-12s %s' % (lbl, '  '.join('%s %d/%d' % (k, v[0], v[1]) for k, v in got.items())))
    for nm, (s_, n_) in got.items():
        if 'PSLN-344' in nm:
            chk('%s %s survivors' % (lbl, nm), s_, 6, 1e-9)
            chk('%s %s pct' % (lbl, nm), 100.0 * s_ / n_, 85.7, 1e-2)

# S15-L and S15-N parent arms: only the candidate and sham arms were checked.
for lbl, hdr, claim in (('S15-L', 102, 0), ('S15-N', 133, 2)):
    _, parent_, _ = arms('S15', hdr, 1, 2, 3, hdr + 1, hdr + 30)
    chk('%s parent survivors' % lbl, surv(parent_), claim, 1e-9)

# S03-J "animals were followed to day 21" -- a data-derived statement the annotation
# disagrees with (it says 22 days of monitoring), so it is worth pinning to the data.
_s03j = [wb['S03'].cell(r, 7).value for r in range(17, 47)]
chk('S03-J last observed day', max(x for x in _s03j if isinstance(x, (int, float))), 21, 1e-9)

# S09-A block 1 is half the two-sided evidence for the timepoint inference; only block 2
# was checked. Block 1's Ifnb1 must reproduce the 16 h column, block 2's the 72 h column.
chk('S09-A b1 cand Ifnb1', 10 ** M('S09', range(17, 20), [3]), 36.3, 2e-3)
print('      S01-A 16h cand %.2f / 72h cand %.2f -- the two anchors block 1 and 2 match'
      % (M('S01', range(2, 7), [8]), M('S01', range(8, 13), [8])))

# S10-A CNS cytokines: the whole of the CNS tolerability check was uncomputed.
_cns = {'Ifnb1': (3, 4), 'Tnf': (8, 9), 'Isg15': (13, 14)}
_cand_cns = {k: M('S10', [cc[0]], range(3, 8)) for k, cc in _cns.items()}
_ct_cns = {k: M('S10', [cc[1]], range(3, 8)) for k, cc in _cns.items()}
print('   S10-A cand %s | CT %s'
      % ({k: round(v, 3) for k, v in _cand_cns.items()}, {k: round(v, 3) for k, v in _ct_cns.items()}))
chk('S10-A cand min', min(_cand_cns.values()), 1.13, 1e-2)
chk('S10-A cand max', max(_cand_cns.values()), 1.59, 1e-2)
chk('S10-A CT min', min(_ct_cns.values()), 2.68, 1e-2)
chk('S10-A CT max', max(_ct_cns.values()), 5.50, 1e-2)
assert min(_ct_cns.values()) > max(_cand_cns.values()), \
    'golden rests the CNS check on the positive control having moved and the candidate not'

# S08-D: "4 of 5 animals remaining at day 10 with a minimum of 84.7%" -- the positive
# control argument. Only the two group means were checked.
_r848 = [wb['S08'].cell(26, c).value for c in range(22, 27)]
_present = [x for x in _r848 if isinstance(x, (int, float))]
print('   S08-D parent+R848 day 10: %s' % _r848)
chk('S08-D parent+R848 animals at d10', len(_present), 4, 1e-9)
chk('S08-D parent+R848 minimum', min(_present), 84.7, 1e-3)

# S08-A "a 9.6% increase for twice the dose" -- the derived percentage the plateau
# reading rests on; the two means were checked, the conclusion was not.
_d20, _d40 = M('S08', range(8, 11), [6]), M('S08', range(8, 11), [7])
chk('S08-A 40ug over 20ug, percent', 100.0 * (_d40 / _d20 - 1), 9.6, 1e-2)

# "Two headline numbers change": the diagonal reading versus the formulation-held
# reading, 0.99 -> 0.73 and 2.78 -> 1.42. The whole paragraph was uncomputed.
_a16, _y16 = M('S01', range(2, 7), [8]), M('S01', range(2, 7), [10])
_a72, _y72 = M('S01', range(8, 13), [8]), M('S01', range(8, 13), [10])
chk('Ifnb1 16h, formulation held', _a16 / _y16, 0.73, 1e-2)
chk('Ifnb1 72h, formulation held', _a72 / _y72, 1.42, 1e-2)
chk('Ifnb1 16h, on the diagonal', vals['Ifnb1 16h'], 0.987, 1e-3)
chk('Ifnb1 72h, on the diagonal', vals['Ifnb1 72h'], 2.785, 1e-3)

# cDC2 moves down in both cohorts, 0.79 aged and 0.95 young. Computed in the four_arm
# loop and printed, never checked.
_cdc2 = [M('S01', g, [38]) for g in (range(7, 12), range(12, 17), range(17, 22), range(22, 27))]
chk('cDC2 aged ratio', _cdc2[1] / _cdc2[0], 0.79, 1e-2)
chk('cDC2 young ratio', _cdc2[3] / _cdc2[2], 0.95, 1e-2)

# S05-C fold-changes 0.93 and 0.22: the four means were checked, the two ratios the
# golden actually leans on were not.
chk('S05-C lung fold', M('S05',[2],range(13,16))/M('S05',[1],range(13,16)), 0.93, 1e-2)
chk('S05-C MLN fold',  M('S05',[4],range(13,16))/M('S05',[3],range(13,16)), 0.22, 1e-2)

# The 4.9-fold and 6.1-fold CCR2-blockade figures were printed with a comment saying
# what the golden claims, and neither was checked.
chk('INCB CD8 fold',  M('S02',[8],range(30,35))/M('S02',[9],range(30,35)), 4.9, 1e-2)
chk('INCB Mphi fold', M('S07',[5],range(10,15))/M('S07',[6],range(10,15)), 6.1, 1e-2)

# S04-C 1.893 and S13-H 0.954: the two numbers carrying "the roster matters because the
# counts depend on it".
chk('S04-C Tfr d30 ratio', M('S04',[3],range(22,27))/M('S04',[4],range(22,27)), 1.893, 1e-3)
chk('S13-H MLN IgG ratio', M('S13',[3],range(53,58))/M('S13',[4],range(53,58)), 0.954, 1e-3)
assert M('S13',[3],range(53,58))/M('S13',[4],range(53,58)) > max(vals[k] for k in _matched), \
    'golden says S13-H sits above all three matched endpoints'

# THE SUBCLASS ARGUMENT. Entirely uncomputed, which is why this script could not catch
# the one real defect the second audit found: the golden named "per animal" as the
# reduction for figures that are ratios of group means. Both routes are checked now, and
# the golden states both.
print('   subclass panels, S03-B / S03-F label rotation')
def _gm(sh, col, rr): return M(sh, [col], rr)
for tag, sub_a, sub_b, tot_col, tot_rows, c_gm, c_pa in (
        ('H1N1', (3, 'S13'), (7, 'S13'), 3, range(3, 8),  16.1, 18.8),
        ('H3N2', (11, 'S13'), (15, 'S13'), 3, range(10, 15), 11.3, 12.5)):
    a = V('S13', [sub_a[0]], range(3, 8)); b = V('S13', [sub_b[0]], range(3, 8))
    t = V('S03', [tot_col], tot_rows)
    gm = (st.mean(a) + st.mean(b)) / st.mean(t)
    pa = st.mean([(x + y) / z for x, y, z in zip(a, b, t)])
    chk('printed-assignment impossibility %s, group means' % tag, gm, c_gm, 1e-3)
    chk('printed-assignment impossibility %s, per animal' % tag, pa, c_pa, 1e-2)
    assert pa > gm, 'golden says reducing per animal makes the impossibility larger'
# Correctly paired, the two subclasses account for 0.559, 0.346 and 0.551 of total IgG.
for nm, cs, cg, ct, claim in (('parent', 1, 5, 3, 0.559), ('cand', 2, 6, 4, 0.346),
                              ('young', 3, 7, 5, 0.551)):
    sub = [x + y for x, y in zip(V('S13', [cs], range(3, 8)), V('S13', [cg], range(3, 8)))]
    frac = st.mean(sub) / M('S03', [ct], range(3, 8))
    chk('correctly-paired subclass fraction, %s' % nm, frac, claim, 1e-3)
    assert frac < 1.0, 'a subclass sum cannot exceed its own total IgG'
# And the rotation itself: each printed column equals another arm's recomputed column.
_recomp = [_per_animal_ratio(c, c + 4) for c in (1, 2, 3)]
_printed = [M('S03', [c], range(3, 8)) for c in (7, 8, 9)]
print('      recomputed %s vs printed %s' % ([round(x, 3) for x in _recomp],
                                             [round(x, 3) for x in _printed]))
assert all(abs(_printed[i] - _recomp[(i - 1) % 3]) < 1e-3 for i in range(3)), \
    'the printed subclass ratios are no longer a one-position rotation of the recomputed set'

# S02-H: the golden now states that all three cited arms are cDC-precursor-depleted and
# that the undepleted pair is a different contrast.
chk('S02-H undepleted WT', M('S02',[3],range(30,35)), 27.22, 1e-3)
chk('S02-H undepleted IFNAR', M('S02',[5],range(30,35)), 6.07, 1e-3)

# Roster row 3 is read at day 4 because that is the peak in both compared arms. The
# golden now says so, and names the day-8 reading that would break the unanimity claim.
_D = {0: 24, 2: 25, 4: 26, 6: 27, 8: 28}
_cand_d = {d: M('S01', range(12, 17), [r]) for d, r in _D.items()}
_youn_d = {d: M('S01', range(17, 22), [r]) for d, r in _D.items()}
_rat_d = {d: _cand_d[d] / _youn_d[d] for d in _D}
print('   S01-D by day: %s' % {d: round(v, 4) for d, v in _rat_d.items()})
chk('S01-D cand at d4', _cand_d[4], 30.56, 1e-3)
chk('S01-D young at d4', _youn_d[4], 32.22, 1e-3)
assert max(_cand_d, key=_cand_d.get) == 4 and max(_youn_d, key=_youn_d.get) == 4, \
    'golden says day 4 is the peak of the response in both compared arms'
chk('S01-D ratio at d8', _rat_d[8], 1.31, 1e-2)
# Pooled as a ratio of the two arms' five-day means -- NOT the mean of the five per-day
# ratios, which is 1.007 because the day-8 outlier drags it above 1.0. The golden said
# "the mean across all five days" without naming the reduction and this check caught it;
# the sentence now names it. Exactly the defect class the second reference audit found in
# the subclass paragraph, reintroduced and then caught, which is the point of the check.
chk('S01-D pooled five-day ratio', st.mean(_cand_d.values()) / st.mean(_youn_d.values()),
    0.996, 1e-3)
_above = [d for d, v in _rat_d.items() if v > 1.0]
chk('S01-D days above 1.0', len(_above), 1, 1e-9)
assert _above == [8], 'golden says only the day-8 reading exceeds 1.0, got %s' % _above

# The exclusivity claim: only these blocks carry a young-plus-candidate arm ALONGSIDE
# aged+parent, aged+candidate and young+parent. The golden rests its limit paragraph on
# it and nothing examined S02-I, S09-B..G or S13-E.
_FOUR = ('PSLN-212', 'PSLN-344', 'PSLN-212(Y)')
def _owning_label(labels, r, c):
    cand_ = [l for l in labels if l[0] <= r]
    if not cand_: return None
    top = max(l[0] for l in cand_)
    same = [l for l in cand_ if l[0] == top and l[1] <= c]
    return max(same, key=lambda l: l[1])[2] if same else None
_blocks = {}
for sh in wb:
    labs = [(c.row, c.column, _re.search(r'\bS\d\d-[A-Z]\b', c.value).group(0))
            for row in sh.iter_rows() for c in row
            if isinstance(c.value, str) and _re.search(r'\bS\d\d-[A-Z]\b', c.value)]
    for row in sh.iter_rows():
        for c in row:
            if not isinstance(c.value, str): continue
            nm = c.value.strip()
            key = None
            if nm in _FOUR: key = nm
            elif nm in ('PSLN-344(Y)', 'PSLN-344Y'): key = 'young+cand'
            if key:
                lab = _owning_label(labs, c.row, c.column)
                if lab: _blocks.setdefault(lab, set()).add(key)
_full = sorted(b for b, s in _blocks.items() if s >= {'young+cand', *_FOUR})
print('   blocks carrying all four arms: %s' % ', '.join(_full))
chk('four-arm blocks', len(_full), 6, 1e-9)
assert set(_full) == {'S01-A', 'S01-E', 'S01-F', 'S01-G', 'S02-C', 'S02-E'}, \
    'the golden limit paragraph names exactly these six blocks (seven panels, S01-A twice)'
_yc_only = sorted(b for b, s in _blocks.items() if 'young+cand' in s and not s >= {'young+cand', *_FOUR})
print('   blocks with a young+cand arm but NOT the full set: %s' % ', '.join(_yc_only))
assert 'S02-I' in _yc_only, 'golden names S02-I as the exception that supports no age contrast'

# ---------------------------------------------------------------------------
# CORRESPONDENCE
#
# Everything above recomputes the workbook and diffs it against what this script says
# the golden claims. That is a recomputation check, and it has a blind spot the gap
# closure does not remove: the claimed values live in THIS FILE, as a hand-maintained
# transcription of the document. Edit a figure in the golden without editing the script
# and nothing notices -- a deliberate tamper proved it. So the claims are also asserted
# to appear literally in the golden text, which makes the transcription provable rather
# than parallel. This is the class the second reference audit's finding belonged to: a
# figure whose stated reduction no longer matched the number, which no amount of
# recomputation could have caught.
print('\nCORRESPONDENCE: every claimed figure appears literally in the golden')
_golden = open('../task/golden-response.md').read()
_LITERALS = [
    # log-rank table, all four rows
    '0.0002','0.0083','0.0009','0.0068','0.0016','0.0094','0.0151',
    '0.0267','0.088','0.0024','0.111','0.066','0.0063','0.317','0.141','0.060','0.855',
    # survival fractions
    '85.7','71.4','57.1','14.3','28.6',
    # the subclass argument, both reductions
    '16.1-fold','11.3-fold','18.8-fold','12.5-fold','0.559','0.346','0.551',
    # roster-dependency figures
    '1.893','0.954',
    # S02-H depletion pairing
    '27.22','6.07',
    # S01-D day-4 peak and its sensitivity
    '30.56','32.22','0.996',
    # dose and tolerability
    '9.6','84.7','99.78','90.65','45.83','50.23','1.13','1.59','2.68','5.50',
    # mechanism chain
    '43.10','12.65','7.28','3.08','19.70','2.09','12.40','8.74','1.21',
    '6.77','1.39','15.35','2.52','9.86','3.26','59.00','55.07','30.90','6.83',
    '0.93','0.22','4.9','6.1',
    # the 2x2 and the two re-readings
    '0.79','0.95','0.73','1.42','1.65','24.35','1.02','1.35','1.29','1.97','3.13',
    # the analyte panel and both timepoint anchors
    '36.3','4.01','27.41','9.23','8.44','7.19','4.16','2.01',
    # the eighteen, and the two pooled means
    '0.987','2.785','0.948','0.661','0.618','0.406','0.758','0.721','0.666','0.752',
    '1.517','0.678','0.941','0.944','0.592','0.693','0.687','0.656','0.654','0.741',
    # humoral headline figures
    '7891.6','437.0','18.06','367.58','45.95','8.00','416.0',
]
_absent = [x for x in _LITERALS if x not in _golden]
print('   %d claimed figures checked against the golden text, %d absent'
      % (len(_LITERALS), len(_absent)))
if _absent:
    print('   ABSENT FROM THE GOLDEN: %s' % ', '.join(_absent))
    fails.append('correspondence: %d claimed figures no longer appear in the golden' % len(_absent))

print('\n%s'%('AUDIT FAILURES: '+', '.join(fails) if fails else 'all other checks OK'))
# This script exited 0 even with chk() mismatches recorded, so a scripted gate reading
# the exit status saw green whenever no assert happened to fire. Every "audit-golden
# passes" claim made before this line existed was weaker than it sounded: it meant no
# assertion tripped, not that nothing mismatched.
import sys as _sys
_sys.exit(1 if fails else 0)
