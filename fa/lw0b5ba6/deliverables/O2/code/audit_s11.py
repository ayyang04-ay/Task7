import pandas as pd, numpy as np
from scipy import stats
t=pd.read_csv('tidy.csv')
a=t[t.block=='S11-A'].copy(); b=t[t.block=='S11-B'].copy(); d=t[t.block=='S11-D'].copy()
m=a.merge(b,on=['group','time','rep'],suffixes=('_AM','_NEU'))
m['same']=np.isclose(m.value_AM,m.value_NEU)
print("S11-A (alveolar macrophages) vs S11-B (neutrophils): position-matched identical values")
print(m.groupby('rep').same.agg(['sum','size']))
print("total identical:",m.same.sum(),"of",len(m))
tab=m.pivot_table(index=['group','time'],columns='rep',values='same',aggfunc='first')
print(tab.astype(int).to_string())
# list identical cells
print(m[m.same][['group','time','rep','cell_AM','cell_NEU','value_AM']].to_string(index=False))
# chance estimate: within-group SD at 0.1 resolution
sd = pd.concat([a,b]).groupby(['block','group','time']).value.std().median()
p_match = 0.1/(2*np.sqrt(np.pi)*sd)   # P(two indep normal draws (same mean, sd) rounded to 0.1 coincide) ~ 0.1*1/(2 sqrt(pi) sd)
print("median within-group SD %.2f -> P(chance exact match) ~ %.4f"%(sd,p_match))
print("P(>= %d matches of %d by chance) = %.3g"%(m.same.sum(),len(m),stats.binom.sf(m.same.sum()-1,len(m),p_match)))
# control comparison: S11-A vs S11-D (NK) same positions
m2=a.merge(d,on=['group','time','rep'],suffixes=('_AM','_NK'))
print("control: S11-A vs S11-D identical positions:",np.isclose(m2.value_AM,m2.value_NK).sum(),"of",len(m2))
m3=b.merge(d,on=['group','time','rep'],suffixes=('_NEU','_NK'))
print("control: S11-B vs S11-D identical positions:",np.isclose(m3.value_NEU,m3.value_NK).sum(),"of",len(m3))

print("\nS01-B vs S08-C position matched")
s1=t[t.block=='S01-B']; s8=t[t.block=='S08-C']
for g1,g8 in [('AECII/PSLN-SRB','AECII-PSLN-SRB'),('AECI/PSLN-SRB','AECII-PSLN-344-SRB'),('AECI/PSLN-SRB','AECI-PSLN-SRB'),('AECII/PSLN-SRB','AECI-PSLN-344-SRB')]:
    x=s1[s1.group==g1].sort_values('rep'); y=s8[s8.group==g8].sort_values('rep')
    print(f"{g1:18s} {list(x.value)}  |  {g8:20s} {list(y.value)}   cells {list(x.cell)[0]}.. vs {list(y.cell)[0]}..")
for g in s8.group.unique():
    x=s8[s8.group==g].value
    print("S08-C",g,"mean %.2f sd %.2f"%(x.mean(),x.std()))
for g in s1.group.unique():
    x=s1[s1.group==g].value
    print("S01-B",g,"mean %.2f sd %.2f"%(x.mean(),x.std()))
