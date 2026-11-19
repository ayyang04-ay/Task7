import pandas as pd, numpy as np
b=pd.read_csv('bodyweight.csv'); b=b[b.day>0].copy()
b['hp']=b.value.apply(lambda x: abs(round(x,1)-x)>1e-6)
hp=b[b.hp].copy(); hp['r']=hp.value.round(5)
ex=hp.groupby('r').filter(lambda d: len(d.drop_duplicates(['block','group','animal']))>1)
ex=ex.sort_values(['r','block'])[['r','block','group','animal','day','value','cell']]; ex.columns=['shared_value','block','group','animal','day','value','cell']
ex.to_csv('bw_dup_exact.csv',index=False)
hp['frac']=((hp.value*10)%1).round(4); hp=hp[(hp.frac>0.0005)&(hp.frac<0.9995)]
rows=[]
for f,d in hp.groupby('frac'):
    dd=d.drop_duplicates(['block','group','animal','day'])
    if dd[['block','group','animal']].drop_duplicates().shape[0]>1:
        for _,r in dd.iterrows(): rows.append(dict(signature=f,block=r.block,group=r.group,animal=r.animal,day=r.day,value=r.value,cell=r.cell))
pd.DataFrame(rows).to_csv('bw_dup_signatures.csv',index=False)
print('exact dup rows',len(ex),'distinct values',ex.shared_value.nunique(),'; signature rows',len(rows),'signatures',pd.DataFrame(rows).signature.nunique())
