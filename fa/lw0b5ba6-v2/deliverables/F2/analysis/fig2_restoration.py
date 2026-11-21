import numpy as np, pandas as pd
from figstyle import *
r = pd.read_csv('restoration_index.csv')
order = [
 ('Innate sensing and antigen-presenting cells', ['S01-A_16h','S01-F','S02-A','S02-B','S02-C','S02-D_CD40','S02-D_CD86','S02-E']),
 ('Germinal centre / antibody', ['S03-K','S04-A_ICOShi','S04-B_TfhTfr','S13-H','S03-A','S03-E','S03-C','S03-G','S03-D','S03-H','S13-A','S13-B']),
 ('CD8 T cells', ['S05-D','S05-E','S05-F','S05-G','S05-H','S05-I','S14-A_H1N1','S14-A_H3N2']),
 ('Read-outs where lower = "young-like"', ['S04-B_Tfr','S04-D','S11-E','S01-G']),
]
short = {'S01-A_16h':'Lung Ifnb1 mRNA, 16 h','S01-F':'Lung cDC1, 72 h','S02-A':'Migratory CCR7+ CD11b+ DC, lung','S02-B':'CD11b+ DC in lymph node','S02-C':'Antigen-carrying DC in lymph node',
 'S02-D_CD40':'CD40+ lymph-node DC','S02-D_CD86':'CD86+ lymph-node DC','S02-E':'CD8 priming by lymph-node DC (ex vivo)','S03-K':'Germinal-centre B cells, day 7','S04-A_ICOShi':'Tfh (ICOS-high), day 7',
 'S04-B_TfhTfr':'Tfh:Tfr ratio, day 7','S13-H':'IgG+ B cells in lymph node','S03-A':'IgG anti-H1N1, day 14','S03-E':'IgG anti-H3N2, day 14','S03-C':'HAI titre, H1N1','S03-G':'HAI titre, H3N2',
 'S03-D':'Neutralising titre, H1N1','S03-H':'Neutralising titre, H3N2','S13-A':'IgG2a anti-H1N1','S13-B':'IgG1 anti-H1N1','S05-D':'Ki-67+ lung CD8, day 3','S05-E':'Granzyme B+ lung CD8, day 3',
 'S05-F':'IFN-γ+ CD8 to H5N1 antigen, day 14','S05-G':'IFN-γ+ CD8 to H5N1 antigen, day 60','S05-H':'Granzyme B+ CD8, day 60','S05-I':'Lung resident-memory CD8, day 25','S14-A_H1N1':'IFN-γ+ CD8 to H1N1 antigen',
 'S14-A_H3N2':'IFN-γ+ CD8 to H3N2 antigen','S04-B_Tfr':'Tfr, day 7','S04-D':'Lung Treg, day 7','S11-E':'CD206+ lung macrophages','S01-G':'Lung cDC2, 72 h'}
fig, ax = plt.subplots(figsize=(6.2, 5.15))
y=0; yt=[]; yl=[]
for sec, blocks in order:
    ax.text(0.55, y-0.05, sec, fontsize=7.0, fontweight='bold', va='center', ha='left', color='#222'); y+=1
    for b in blocks:
        x = r[r.block==b].iloc[0]
        ax.plot([x.pct_of_young_212, x.pct_of_young_344],[y,y], color='#bbbbbb', lw=1.2, zorder=1)
        ax.scatter(x.pct_of_young_212, y, s=22, color=COL['PSLN-212'], zorder=3, edgecolor='white', lw=0.4)
        ax.scatter(x.pct_of_young_344, y, s=22, color=COL['PSLN-344'], zorder=3, edgecolor='white', lw=0.4)
        yt.append(y); yl.append(f'{short[b]}  [{b.replace("_"," ")}]'); y+=1
    y+=0.4
ax.axvline(100, color=COL['PSLN-212(Y)'], lw=1.4, zorder=0); 
ax.set_xscale('log'); ax.set_xlim(0.5, 520); ax.set_ylim(y-0.6, -0.9)
ax.set_xticks([1,3,10,30,100,300]); ax.set_xticklabels(['1%','3%','10%','30%','100%','300%'])
ax.set_yticks(yt); ax.set_yticklabels(yl, fontsize=6.3)
fig.text(0.5, 0.012, 'Response in aged mice as % of the young-adult benchmark (young mice given PSLN-212 = 100%), log scale', ha='center', fontsize=7)
ax.scatter([],[],color=COL['PSLN-212'],label='PSLN-212, aged mice'); ax.scatter([],[],color=COL['PSLN-344'],label='PSLN-344, aged mice'); ax.plot([],[],color=COL['PSLN-212(Y)'],label='Young benchmark')
ax.legend(loc='upper center', bbox_to_anchor=(0.22, 1.065), frameon=False, fontsize=7, ncol=3, columnspacing=1.2, handletextpad=0.3)
ax.tick_params(axis='y', length=0); ax.grid(axis='x', color='#eeeeee', lw=0.6); ax.set_axisbelow(True)
fig.subplots_adjust(left=0.455, right=0.985, top=0.945, bottom=0.085)
fig.savefig(OUT+'fig2_restoration_vs_young.png'); print('ok')
