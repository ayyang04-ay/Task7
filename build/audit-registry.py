# Builds a registry of every verified value from the shipped workbook: survival
# percentages and the full pairwise log-rank matrix for S06, the S06-C/S06-D identity
# count, S03-J arms, the subclass correction and its foreclosure, tolerability
# controls, within-age adjuvant folds and the age-versus-formulation diagonals.
#
# Usage: python3 -I audit-registry.py
#
# Companion to audit-golden.py. That script checks stated values; this one prints
# the full verified set so a reviewer can trace any figure in the golden to source.
# Log-rank is Mantel-Cox implemented from the standard library, so this runs
# without lifelines or scipy.

import openpyxl, statistics as st, math, re
wb=openpyxl.load_workbook('../data-room/amnesti_preclinical_dataset.xlsx',data_only=True)
def V(sh,cc,rr):
    ws=wb[sh]; return [float(ws.cell(r,c).value) for r in rr for c in cc
                       if isinstance(ws.cell(r,c).value,(int,float))]
def M(sh,cc,rr): return st.mean(V(sh,cc,rr))
def geo(v):
    v=[x for x in v if x>0]; return 10**(sum(math.log10(x) for x in v)/len(v))
ws6=wb['S06']
def blk(hr,c0,nc,r0,r1):
    out={}
    for i in range(1,nc+1):
        nm=ws6.cell(hr,c0+i).value
        if not nm: continue
        rows=[(ws6.cell(r,c0).value,ws6.cell(r,c0+i).value) for r in range(r0,r1+1)
              if isinstance(ws6.cell(r,c0+i).value,(int,float))]
        out[str(nm).strip()]=rows
    return out
def lr(a,b):
    ts=sorted({t for t,e in a+b if e==1}); O=E=Var=0.0
    for t in ts:
        n1=sum(1 for x,_ in a if x>=t); n2=sum(1 for x,_ in b if x>=t)
        d1=sum(1 for x,e in a if x==t and e==1); d2=sum(1 for x,e in b if x==t and e==1)
        n=n1+n2; d=d1+d2
        if n<2 or d==0: continue
        O+=d1; E+=d*n1/n; Var+=d*(n1/n)*(1-n1/n)*((n-d)/(n-1))
    if Var<=0: return float('nan')
    return math.erfc(math.sqrt(((O-E)**2/Var)/2))

# build registry of every verified value
R={}
B={'S06-A':(2,1,4,3,30),'S06-B':(2,7,4,3,30),'S06-C':(2,13,4,3,30),'S06-D':(33,1,4,34,68),
   'S06-E':(33,7,5,34,68),'S06-F':(33,13,5,34,68),'S06-G':(70,1,5,71,105),
   'S06-Ex':(70,7,4,71,105),'S06-Fx':(70,13,4,71,105)}
S={}
for k,(hr,c0,nc,r0,r1) in B.items():
    S[k]=blk(hr,c0,nc,r0,r1)
    for arm,rows in S[k].items():
        R['%s %s surv'%(k,arm)]=100*sum(1 for d,e in rows if e==0)/len(rows)
for k in ['S06-A','S06-B','S06-C','S06-E','S06-F','S06-G']:
    a=S[k]; cand=a['AMnESTI']
    R['%s p vs sham'%k]=lr(cand,a['Sham']); R['%s p vs comp'%k]=lr(cand,a['PSLN-212'])
    R['%s p vs young'%k]=lr(cand,a['PSLN-212(Y)']); R['%s comp vs sham'%k]=lr(a['PSLN-212'],a['Sham'])
    if 'Untreated' in a: R['%s p vs untr'%k]=lr(cand,a['Untreated'])
# S06-C vs S06-D identity
same=sum(1 for arm in S['S06-C'] for p,q in zip(S['S06-C'][arm],S['S06-D'][arm]) if p==q)
R['S06-C==S06-D pairs']=same
# S03-J
w3=wb['S03']
for i,nm in enumerate(['Sham','PSLN-212','AMnESTI']):
    rows=[(w3.cell(r,7).value,w3.cell(r,8+i).value) for r in range(17,47) if isinstance(w3.cell(r,8+i).value,(int,float))]
    R['S03-J %s censored'%nm]=sum(1 for d,e in rows if e==0); R['S03-J %s n'%nm]=len(rows)
# subclass
for lbl,a,b,r0 in (('H1N1',1,5,3),('H3N2',9,13,10)):
    pr=[M('S03',[7+i],range(r0,r0+5)) for i in range(3)]
    tr=[st.mean([x/y for x,y in zip(V('S13',[a+i],range(3,8)),V('S13',[b+i],range(3,8)))]) for i in range(3)]
    sm=[M('S13',[a+i],range(3,8))+M('S13',[b+i],range(3,8)) for i in range(3)]
    tt=[M('S03',[3+i],range(r0,r0+5)) for i in range(3)]
    for i in range(3):
        R['%s printed%d'%(lbl,i)]=pr[i]; R['%s true%d'%(lbl,i)]=tr[i]; R['%s sum/tot%d'%(lbl,i)]=sm[i]/tt[i]
    R['%s alt'%lbl]=sm[2]/tt[0]
# tolerability, S10
for i,an in enumerate(['Ifnb1','Tnf','Isg15']):
    R['S10 cand %s'%an]=M('S10',[3+i*5],range(3,8)); R['S10 CT %s'%an]=M('S10',[4+i*5],range(3,8))
R['S08-D min']=min(V('S08',range(22,27),[26])); R['S08-D n']=len(V('S08',range(22,27),[26]))
R['S08-A pct']=100*(M('S08',range(8,11),[7])/M('S08',range(8,11),[6])-1)
# within-age folds
R['S01-A16 aged fold']=M('S01',range(2,7),[8])/M('S01',range(2,7),[5])
R['S01-A16 young fold']=M('S01',range(2,7),[10])/M('S01',range(2,7),[9])
R['S01-E fold a']=M('S01',range(12,17),[32])/M('S01',range(7,12),[32])
R['S01-E fold y']=M('S01',range(22,27),[32])/M('S01',range(17,22),[32])
R['S01-F fold a']=M('S01',range(12,17),[36])/M('S01',range(7,12),[36])
R['S01-F fold y']=M('S01',range(22,27),[36])/M('S01',range(17,22),[36])
R['S01-G fold a']=M('S01',range(12,17),[38])/M('S01',range(7,12),[38])
R['S01-G fold y']=M('S01',range(22,27),[38])/M('S01',range(17,22),[38])
R['S02-C fold a']=M('S02',[12],range(3,8))/M('S02',[11],range(3,8))
R['S02-C fold y']=M('S02',[15],range(3,8))/M('S02',[13],range(3,8))
R['S02-E fold a']=M('S02',[12],range(10,15))/M('S02',[11],range(10,15))
R['S02-E fold y']=M('S02',[15],range(10,15))/M('S02',[13],range(10,15))
R['INCB CD8 fold']=M('S02',[8],range(30,35))/M('S02',[9],range(30,35))
R['INCB Mphi fold']=M('S07',[5],range(10,15))/M('S07',[6],range(10,15))
R['S01-A16 diag']=M('S01',range(2,7),[8])/M('S01',range(2,7),[9])
R['S01-A16 held']=M('S01',range(2,7),[8])/M('S01',range(2,7),[10])
R['S01-A72 diag']=M('S01',range(8,13),[8])/M('S01',range(8,13),[9])
R['S01-A72 held']=M('S01',range(8,13),[8])/M('S01',range(8,13),[10])
R['S03-A of young']=M('S03',[4],range(3,8))/M('S03',[5],range(3,8))
R['S03-C of young']=geo(V('S03',[14],range(3,8)))/geo(V('S03',[15],range(3,8)))
R['TRM of young']=M('S05',[3],range(54,59))/M('S05',[4],range(54,59))
R['IFNg14 of young']=M('S05',[3],range(33,38))/M('S05',[4],range(33,38))
R['IFNg60 of young']=M('S05',[3],range(40,45))/M('S05',[4],range(40,45))
for k in sorted(R): print('  %-24s %.4g'%(k,R[k]))
