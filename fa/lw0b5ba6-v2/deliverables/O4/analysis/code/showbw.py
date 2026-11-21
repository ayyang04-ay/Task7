import pandas as pd, sys
bw = pd.read_csv('bw.csv'); surv = pd.read_csv('survival.csv')
for bb, g, sb in [('S15-C','PSLN-212','S06-C'),('S15-D','PSLN-344','S06-D'),('S15-D','PSLN-212(Y)','S06-D'),('S15-E','PSLN-212','S06-E'),('S15-E','PSLN-344','S06-E'),
                  ('S15-G','PSLN-344','S06-G'),('S15-G','Untreated','S06-G'),('S15-M','PSLN-212(Y)','S15-L'),('S13-F','PSLN-212','S03-I'),('S13-G','Sham','S03-J'),('S13-G','Naïve','S03-J')]:
    d = bw[(bw.block==bb)&(bw.group==g)]
    p = d.pivot(index='day', columns='col', values='value')
    p = p[list(dict.fromkeys(d.col))]
    s = surv[(surv.block==sb)&(surv.group==g)]
    print(f'--- {bb} {g}   | survival {sb}: deaths on days {sorted(s[s.event==1].day.tolist())}, survivors {int((s.event==0).sum())}')
    print(p.to_string())
