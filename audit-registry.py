# Builds a registry of every verified value from the shipped workbook: survival
# percentages and the full pairwise log-rank matrix for Fig. 6, the 6E/6G identity
# count, Fig. 3J arms, the subclass correction and its foreclosure, tolerability
# controls, within-age adjuvant folds and the age-versus-formulation diagonals.
#
# Usage: python3 -I audit-registry.py
#
# Companion to audit-golden.py. That script checks stated values; this one prints
# the full verified set so a reviewer can trace any figure in the golden to source.
# Log-rank is Mantel-Cox implemented from the standard library, so this runs
# without lifelines or scipy.

import openpyxl, statistics as st, math, re
wb=openpyxl.load_workbook('adz5242_data_file_s1.xlsx',data_only=True)
def V(sh,cc,rr):
    ws=wb[sh]; return [float(ws.cell(r,c).value) for r in rr for c in cc
                       if isinstance(ws.cell(r,c).value,(int,float))]
def M(sh,cc,rr): return st.mean(V(sh,cc,rr))
def geo(v):
    v=[x for x in v if x>0]; return 10**(sum(math.log10(x) for x in v)/len(v))
ws6=wb['Fig.6']
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
B={'6A':(2,1,4,3,30),'6C':(2,7,4,3,30),'6E':(2,13,4,3,30),'6G':(33,1,4,34,68),
   '6H':(33,7,5,34,68),'6I':(33,13,5,34,68),'6J':(70,1,5,71,105),
   '6Kx':(70,7,4,71,105),'6Lx':(70,13,4,71,105)}
S={}
for k,(hr,c0,nc,r0,r1) in B.items():
    S[k]=blk(hr,c0,nc,r0,r1)
    for arm,rows in S[k].items():
        R['%s %s surv'%(k,arm)]=100*sum(1 for d,e in rows if e==0)/len(rows)
for k in ['6A','6C','6E','6H','6I','6J']:
    a=S[k]; cand=a['AMnESTI']
    R['%s p vs sham'%k]=lr(cand,a['Sham']); R['%s p vs comp'%k]=lr(cand,a['NanoSTING'])
    R['%s p vs young'%k]=lr(cand,a['NanoSTING(Y)']); R['%s comp vs sham'%k]=lr(a['NanoSTING'],a['Sham'])
    if 'Untreated' in a: R['%s p vs untr'%k]=lr(cand,a['Untreated'])
# 6E vs 6G identity
same=sum(1 for arm in S['6E'] for p,q in zip(S['6E'][arm],S['6G'][arm]) if p==q)
R['6E==6G pairs']=same
# 3J
w3=wb['Fig. 3']
for i,nm in enumerate(['Sham','NanoSTING','AMnESTI']):
    rows=[(w3.cell(r,7).value,w3.cell(r,8+i).value) for r in range(17,47) if isinstance(w3.cell(r,8+i).value,(int,float))]
    R['3J %s censored'%nm]=sum(1 for d,e in rows if e==0); R['3J %s n'%nm]=len(rows)
# subclass
for lbl,a,b,r0 in (('H1N1',1,5,3),('H3N2',9,13,10)):
    pr=[M('Fig. 3',[7+i],range(r0,r0+5)) for i in range(3)]
    tr=[st.mean([x/y for x,y in zip(V('Fig. S8',[a+i],range(3,8)),V('Fig. S8',[b+i],range(3,8)))]) for i in range(3)]
    sm=[M('Fig. S8',[a+i],range(3,8))+M('Fig. S8',[b+i],range(3,8)) for i in range(3)]
    tt=[M('Fig. 3',[3+i],range(r0,r0+5)) for i in range(3)]
    for i in range(3):
        R['%s printed%d'%(lbl,i)]=pr[i]; R['%s true%d'%(lbl,i)]=tr[i]; R['%s sum/tot%d'%(lbl,i)]=sm[i]/tt[i]
    R['%s alt'%lbl]=sm[2]/tt[0]
# tolerability S3
for i,an in enumerate(['Ifnb1','Tnf','Isg15']):
    R['S3 cand %s'%an]=M('Fig. S3',[3+i*5],range(3,8)); R['S3 CT %s'%an]=M('Fig. S3',[4+i*5],range(3,8))
R['S1J min']=min(V('Fig. S1',range(22,27),[26])); R['S1J n']=len(V('Fig. S1',range(22,27),[26]))
R['S1B pct']=100*(M('Fig. S1',range(8,11),[7])/M('Fig. S1',range(8,11),[6])-1)
# within-age folds
R['1A16 aged fold']=M('Fig.1',range(2,7),[8])/M('Fig.1',range(2,7),[5])
R['1A16 young fold']=M('Fig.1',range(2,7),[10])/M('Fig.1',range(2,7),[9])
R['1J fold a']=M('Fig.1',range(12,17),[32])/M('Fig.1',range(7,12),[32])
R['1J fold y']=M('Fig.1',range(22,27),[32])/M('Fig.1',range(17,22),[32])
R['1K fold a']=M('Fig.1',range(12,17),[36])/M('Fig.1',range(7,12),[36])
R['1K fold y']=M('Fig.1',range(22,27),[36])/M('Fig.1',range(17,22),[36])
R['1L fold a']=M('Fig.1',range(12,17),[38])/M('Fig.1',range(7,12),[38])
R['1L fold y']=M('Fig.1',range(22,27),[38])/M('Fig.1',range(17,22),[38])
R['2D fold a']=M('Fig. 2',[12],range(3,8))/M('Fig. 2',[11],range(3,8))
R['2D fold y']=M('Fig. 2',[15],range(3,8))/M('Fig. 2',[13],range(3,8))
R['2F fold a']=M('Fig. 2',[12],range(10,15))/M('Fig. 2',[11],range(10,15))
R['2F fold y']=M('Fig. 2',[15],range(10,15))/M('Fig. 2',[13],range(10,15))
R['INCB CD8 fold']=M('Fig. 2',[8],range(30,35))/M('Fig. 2',[9],range(30,35))
R['INCB Mphi fold']=M('Fig.7',[5],range(10,15))/M('Fig.7',[6],range(10,15))
R['1A16 diag']=M('Fig.1',range(2,7),[8])/M('Fig.1',range(2,7),[9])
R['1A16 held']=M('Fig.1',range(2,7),[8])/M('Fig.1',range(2,7),[10])
R['1A72 diag']=M('Fig.1',range(8,13),[8])/M('Fig.1',range(8,13),[9])
R['1A72 held']=M('Fig.1',range(8,13),[8])/M('Fig.1',range(8,13),[10])
R['3A of young']=M('Fig. 3',[4],range(3,8))/M('Fig. 3',[5],range(3,8))
R['3C of young']=geo(V('Fig. 3',[14],range(3,8)))/geo(V('Fig. 3',[15],range(3,8)))
R['TRM of young']=M('Fig.5',[3],range(54,59))/M('Fig.5',[4],range(54,59))
R['IFNg14 of young']=M('Fig.5',[3],range(33,38))/M('Fig.5',[4],range(33,38))
R['IFNg60 of young']=M('Fig.5',[3],range(40,45))/M('Fig.5',[4],range(40,45))
for k in sorted(R): print('  %-24s %.4g'%(k,R[k]))
