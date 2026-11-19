import pandas as pd, numpy as np
df = pd.read_csv('/tmp/work/tidy.csv')
m16 = df[df.block=='S01-A_16h'].groupby('group').value.mean()
m72 = df[df.block=='S01-A_72h'].groupby('group').value.mean()
for panel in ['S09-A_panel1_A-U','S09-A_panel2_X-AS']:
    p = df[(df.block==panel)&(df.analyte=='Ifnb1')].groupby('group').value.mean()
    rows=[]
    for g in p.index:
        gg = g.replace('(y)','(Y)')
        if gg in m16.index and g!='PBS':
            rows.append((g, round(p[g],3), round(np.log10(m16[gg]),3), round(np.log10(m72[gg]),3)))
    r = pd.DataFrame(rows, columns=['group','panel_mean_log10','S01A_16h_log10','S01A_72h_log10'])
    r['absdiff_16h']=(r.panel_mean_log10-r.S01A_16h_log10).abs().round(3); r['absdiff_72h']=(r.panel_mean_log10-r.S01A_72h_log10).abs().round(3)
    print(panel); print(r.to_string(index=False)); print('mean abs diff vs 16h:', r.absdiff_16h.mean().round(3), ' vs 72h:', r.absdiff_72h.mean().round(3))
