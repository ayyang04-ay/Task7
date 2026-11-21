import pandas as pd, numpy as np
bw = pd.read_csv('bw.csv'); surv = pd.read_csv('survival.csv')
def infer(series):
    """series: list of (day, value) sorted. returns (status, inferred_death_window, note)"""
    days = [d for d,_ in series]; v = [x for _,x in series]
    # trailing missing
    last = max(i for i,x in enumerate(v) if x is not None and not (isinstance(x,float) and np.isnan(x)))
    if last < len(v)-1:
        return 'dead(blank)', (days[last], days[last+1])
    # trailing identical run (LOCF) of length >=2 ending at last day
    run = 1
    for i in range(len(v)-1, 0, -1):
        if v[i] == v[i-1]: run += 1
        else: break
    if run >= 3 or (run >= 2 and v[-1] < 90):
        first = len(v)-run
        return 'dead(LOCF)', (days[first], days[first+1])
    return 'alive', None
pairs = [('S03-I','S13-F'),('S03-J','S13-G'),('S06-A','S15-A'),('S06-B','S15-B'),('S06-C','S15-C'),('S06-D','S15-D'),
         ('S06-E','S15-E'),('S06-F','S15-F'),('S06-G','S15-G'),('S15-H','S15-I'),('S06-E2_imprint','S15-J'),('S06-F2_imprint','S15-K'),
         ('S15-L','S15-M'),('S15-N','S15-O'),('S09-B','S09-C'),('S09-D','S09-E'),('S09-F','S09-G')]
norm = lambda g: g.replace('Naïve','Naive').replace('Y)','Y)').strip()
out=[]
for sb, bb in pairs:
    S = surv[surv.block==sb]; B = bw[bw.block==bb]
    bgroups = list(dict.fromkeys(B.group)); sgroups = list(dict.fromkeys(S.group))
    for g in dict.fromkeys(sgroups + bgroups):
        s = S[S.group==g]
        b = B[B.group==g]
        sd = int(s.event.sum()) if len(s) else None
        sn = len(s) if len(s) else None
        if len(b):
            st = []
            for a,d in b.groupby('animal', sort=False):
                ser = list(zip(d.day, [None if pd.isna(x) else x for x in d.value]))
                st.append(infer(ser))
            nb = len(st); bd = sum(1 for x in st if x[0]!='alive')
            nblank = sum(1 for x in st if x[0]=='dead(blank)'); nlocf = sum(1 for x in st if x[0]=='dead(LOCF)')
        else:
            nb=bd=nblank=nlocf=None
        flag = ''
        if sd is None or nb is None: flag='GROUP MISSING IN ONE BLOCK'
        elif sd != bd: flag='MISMATCH'
        out.append(dict(surv_block=sb, bw_block=bb, group=g, surv_n=sn, surv_deaths=sd, bw_n=nb, bw_inferred_deaths=bd, blank=nblank, locf=nlocf, flag=flag))
o = pd.DataFrame(out)
pd.set_option('display.width',250)
print(o.to_string())
o.to_csv('concordance.csv', index=False)
