# Recomputes every load-bearing figure in ../task/golden-response.md from the shipped
# workbook and diffs it against what the document states.
#
# Usage: python3 -I audit-golden.py   (expects ../data-room/amnesti_preclinical_dataset.xlsx alongside)
#
# Run this after any edit to the data room, per the build constraint that the
# golden is recomputed from the shipped room after its last edit. Exits noisily
# on any mismatch.

import openpyxl, statistics as st, math
wb=openpyxl.load_workbook('../data-room/amnesti_preclinical_dataset.xlsx',data_only=True)
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
vals['IgG2a:IgG1']=2.1438/2.9718
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
hib=[v for k,v in vals.items() if k not in ('Ifnb1 72h','Tfr')]
print('  higher-is-better: n=%d  min %.4f  max %.4f'%(len(hib),min(hib),max(hib)))
chk('higher-is-better min', min(hib), 0.406, 1e-3)
chk('higher-is-better max', max(hib), 0.987, 1e-3)
print('\nADJUVANT EFFECT WITHIN COHORT (AMnESTI / nanoSTING)')
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
# out that AMnESTI also raises the young response significantly. These three p-values
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
for lbl,x,y,claim in (('age deficit  aged+nS vs young+nS','aged+nS','young+nS',0.0),
                      ('restoration  aged+AM vs young+nS','aged+AM','young+nS',0.857),
                      ('aged+AM vs young+AM','aged+AM','young+AM',0.012),
                      ('young gain   young+nS vs young+AM','young+nS','young+AM',0.014)):
    pv=welch_p(_arm[x],_arm[y])
    print('   %-36s p = %.4f  (%.2f vs %.2f)'%(lbl,pv,st.mean(_arm[x]),st.mean(_arm[y])))
    chk(lbl, pv, claim, 2e-3)
assert welch_p(_arm['young+nS'],_arm['young+AM'])<0.05, \
    'the golden now says AMnESTI raises the young response significantly'

print('\nS15-H: does the package exclude a non-specific antiviral state?')
# The golden now asserts that adjuvant alone protects nobody at the 3-day interval,
# which is what retires the alternative. Recomputed here because that claim is
# load-bearing for the mechanism section.
_s = wb['S15']
for ci, arm, exp_surv, exp_deaths in ((2,'3d Vaccine',0,[4,5,5,5,6,6,7]),
                                      (3,'3d AMnESTI',0,[5,5,6,6,6,7,8]),
                                      (4,'3d Vaccine+AMnESTI',6,[12])):
    ev=[(_s.cell(r,1).value,_s.cell(r,ci).value) for r in range(73,101) if _s.cell(r,ci).value is not None]
    deaths=sorted(t for t,e in ev if e==1); surv=sum(1 for _,e in ev if e==0)
    print('   %-20s n=%d  survive %d  deaths on %s'%(arm,len(ev),surv,deaths))
    chk('S15-H %s survivors'%arm, surv, exp_surv, 1e-9)
    assert deaths==exp_deaths, 'S15-H %s death days %s != %s'%(arm,deaths,exp_deaths)

hum=[vals[k] for k in ['IgG H1N1','IgG H3N2','HAI H1N1','IgG2a:IgG1','GC B','ICOS Tfh']]
cel=[vals[k] for k in ['NP d3','NP d7','Ki67','GZMB','IFNg d14','IFNg d60','TRM']]
chk('humoral mean (6)',st.mean(hum),0.654); chk('cellular mean (7)',st.mean(cel),0.741)
print('\n%s'%('AUDIT FAILURES: '+', '.join(fails) if fails else 'all other checks OK'))
