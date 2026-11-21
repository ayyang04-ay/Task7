import pandas as pd, numpy as np
from fig_style import *
B = pd.read_csv('biomarker_table.csv'); B['time']=B['time'].astype(str)
sel = [
 ('Innate response in lung', [
   ('S01-A','Ifnb1','16h','IFN-β mRNA, 16 h'), ('S09-A','Ccl2','panel1(A-U)','CCL2 mRNA, 16 h (n=3)'), ('S01-D','lung monocytes','4','Monocytes, day 4'),
   ('S01-E','lung CD11b+ DC','4','CD11b+ DC, day 4'), ('S01-F','lung cDC1','72h','cDC1, 72 h')]),
 ('DC migration and priming', [
   ('S02-A','lung CCR7+','72h','CCR7+ migratory DC (lung)'), ('S02-C','MLN OVA','36h','Antigen-bearing DC, lymph node'), ('S02-D CD40','CD40+','d3','CD40+ DC (lymph node)'),
   ('S02-D CD86','CD86+','d3','CD86+ DC (lymph node)'), ('S02-E','OT-I','72h','CD8 priming by DC ex vivo')]),
 ('Tfh / germinal center', [
   ('S03-K','MLN GC','d7','Germinal-center B cells, day 7'), ('S04-A','Tfh ICOS-hi','d7','ICOS-high Tfh, day 7'), ('S04-B Tfh:Tfr','Tfh:Tfr','d7','Tfh:Tfr ratio, day 7')]),
 ('Serum antibody, day 14 (single dose)', [
   ('S03-A','serum IgG','d14','IgG, H1N1'), ('S03-E','serum IgG','d14','IgG, H3N2'), ('S03-C','HAI','d14','HAI, H1N1'), ('S03-G','HAI','d14','HAI, H3N2'),
   ('S03-D','neutralizing','d14','Neutralizing, H1N1'), ('S03-H','neutralizing','d14','Neutralizing, H3N2')]),
 ('CD8 T cells', [
   ('S05-D','lung Ki67','d3','Ki-67+ CD8 (lung), day 3'), ('S05-E','lung GZMB','d3','GZMB+ CD8 (lung), day 3'), ('S05-F','MLN IFNg','d14','IFN-γ+ CD8 vs H5N1, day 14'),
   ('S05-G','MLN IFNg','d60','IFN-γ+ CD8 vs H5N1, day 60'), ('S05-I','lung CD8 TRM','d25','Lung-resident memory CD8, day 25')]),
]
rows=[]
for sec, items in sel:
    for blk, key, t, lab in items:
        r = B[(B.block==blk)&(B.analyte.str.contains(key, regex=False))&(B.time==t)]
        assert len(r)==1, (blk,key,t,len(r))
        r = r.iloc[0]; rows.append((sec, f"{lab}  [{blk}]", r.P212_pct_of_young, r.P344_pct_of_young))
rows.append(('Protection', 'Survival after lethal challenge  [7 blocks pooled]', 100*4/49, 100*39/49))
fig, ax = plt.subplots(figsize=(FIGW, 6.9))
fig.subplots_adjust(left=0.36, right=0.985, top=0.985, bottom=0.07)
y = 0; yt=[]; yl=[]; last=None
for sec, lab, p212, p344 in rows:
    if sec != last:
        y -= 0.55; ax.text(0.36, y+0.05, sec, fontsize=7.6, fontweight='bold', va='center', ha='left', color='#222222'); y -= 0.85; last = sec
    ax.plot([p212, p344], [y, y], color='#BBBBBB', lw=1.2, zorder=1)
    ax.plot(p212, y, 'o', color=COL['PSLN-212'], ms=5.2, zorder=3); ax.plot(p344, y, 'o', color=COL['PSLN-344'], ms=5.2, zorder=3)
    ax.text(232, y, f"{p212:.0f}%" if p212>=9.5 else f"{p212:.1f}%", color=COL['PSLN-212'], fontsize=6.8, va='center', ha='right')
    ax.text(560, y, f"{p344:.0f}%", color=COL['PSLN-344'], fontsize=6.8, va='center', ha='right')
    yt.append(y); yl.append(lab); y -= 0.9
ax.text(243, 0.35, 'Aged +\nPSLN-212', color=COL['PSLN-212'], fontsize=6.6, ha='right', va='center', fontweight='bold'); ax.text(590, 0.35, 'Aged +\nPSLN-344', color=COL['PSLN-344'], fontsize=6.6, ha='right', va='center', fontweight='bold')
ax.axvline(100, color=COL['PSLN-212(Y)'], lw=1.2, ls='--'); ax.text(94, 0.35, 'young + PSLN-212 = 100%', color=COL['PSLN-212(Y)'], fontsize=6.8, ha='right', va='center')
ax.set_xscale('log'); ax.set_xlim(0.35, 640); ax.set_xticks([0.5,1,2,5,10,20,50,100,200]); ax.set_xticklabels(['0.5','1','2','5','10','20','50','100','200'])
ax.set_yticks(yt); ax.set_yticklabels(yl, fontsize=6.9); ax.set_ylim(y, 1.2)
ax.set_xlabel('Response in aged animals as % of the young + PSLN-212 benchmark (log scale)')
ax.xaxis.label.set_size(7.5)
ax.grid(axis='x', color='#EEEEEE', lw=0.6); ax.set_axisbelow(True)
fig.savefig(OUT+'Fig3_restoration_vs_young.png'); print('ok')
pd.DataFrame(rows, columns=['stage','endpoint','PSLN212_pct_of_young','PSLN344_pct_of_young']).to_csv('restoration_selected.csv', index=False)
