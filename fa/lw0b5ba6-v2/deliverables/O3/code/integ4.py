from load import *
import numpy as np, pandas as pd, itertools
tc = DF[DF['day'].notna() & DF['animal_col'].notna()].copy()
tc['day'] = pd.to_numeric(tc['day'], errors='coerce')
bw_blocks = [b for b in tc.block.unique() if 'body weight' in tc[tc.block==b].measurand.iloc[0]]
vec = {}
for (b,g,c), d in tc[tc.block.isin(bw_blocks)].groupby(['block','group','animal_col']):
    s = d.set_index('day')['value'].sort_index()
    fresh = s[(s.index!=0)]
    prev = s.shift(1)
    fresh = s[(s.index!=0) & ~(np.isclose(s, prev))]  # exclude LOCF repeats
    vec[(b,g,c)] = (s, fresh)
keys=list(vec)
rows=[]
for i in range(len(keys)):
    for j in range(i+1,len(keys)):
        (sa,fa),(sb,fb) = vec[keys[i]], vec[keys[j]]
        common = fa.index.intersection(fb.index)
        eq = [d for d in common if abs(fa[d]-fb[d])<1e-9]
        # fractional-part match for high-precision values (>=4 decimals)
        frac=[]
        for d in sa.index.intersection(sb.index):
            if d==0: continue
            x,y = sa[d], sb[d]
            sx, sy = repr(float(x)), repr(float(y))
            if ('.' in sx and len(sx.split('.')[1])>=4) and ('.' in sy and len(sy.split('.')[1])>=4):
                if abs((x%1)-(y%1))<1e-6 and abs(x-y)>1e-9:
                    frac.append(d)
        if len(eq)>=3 or len(frac)>=2:
            rows.append(dict(a=f"{keys[i][0]}:{keys[i][1]}[{keys[i][2]}]", b=f"{keys[j][0]}:{keys[j][1]}[{keys[j][2]}]",
                             same_block=keys[i][0]==keys[j][0], fresh_identical=len(eq), days_identical=str(sorted(eq)),
                             frac_only_matches=len(frac), frac_days=str(sorted(frac))))
R = pd.DataFrame(rows).sort_values(['fresh_identical','frac_only_matches'],ascending=False)
pd.set_option('display.width',250); pd.set_option('display.max_rows',500); pd.set_option('display.max_colwidth',60)
print(R.to_string(index=False))
R.to_csv('/tmp/work/bw_duplication_pairs.csv',index=False)
print('\nN pairs:',len(R))
# which blocks are implicated
imp = pd.concat([R.a.str.split(':').str[0], R.b.str.split(':').str[0]]).value_counts()
print(imp)
