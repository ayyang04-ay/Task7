"""10_biomarkers.py -- regimen-level biomarker screen.
Protective regimens (pooled day-14 survival, S03-I/S06-A/S06-C): aged PSLN-344 20/21, young PSLN-212(Y) 21/21.
Non-protective: aged Sham 0/21, aged PSLN-212 3/21. CMP-204 (aged) 3/7 in S03-I is shown as intermediate where measured.
NOTE: biomarker and survival come from different animals -> this ranks regimen-level separation, not individual-level correlates."""
import pandas as pd, numpy as np
from scipy import stats
C=pd.read_csv('/tmp/work/tidy/continuous.csv'); C['time']=C['time'].astype(str)
C.loc[C.block.isin(['S03-C','S03-G'])&(C.value<10),'value']=5.0
CAND=[ # block, time, measurand substring, label, stage, human analogue, direction(+1 higher=protective)
('S01-A','16h','Ifnb1','Lung Ifnb1, 16 h','PD (hours)','Nasal-fluid IFN-b/IFN-l; blood ISG score at 24 h',+1),
('S01-D','4','monocytes','Lung Ly6C+ monocytes, d4','Early cellular (d2-5)','Blood CD14+ monocyte activation (e.g., SIGLEC1/CD169)',+1),
('S01-E','4','CD11b+ DC','Lung CD11b+ DC, d4','Early cellular (d2-5)','-- (tissue only)',+1),
('S01-F','72h','cDC1','Lung cDC1, 72 h','Early cellular (d2-5)','-- (tissue only)',+1),
('S02-A','72h','CCR7','CCR7+ migratory DC, 72 h','Early cellular (d2-5)','-- (tissue only)',+1),
('S02-C','36h','AF647','Antigen+ DC in MLN, 36 h','Early cellular (d2-5)','-- (tissue only)',+1),
('S02-D CD40','d3','CD40','MLN DC CD40+, d3','Early cellular (d2-5)','-- (tissue only)',+1),
('S02-D CD86','d3','CD86','MLN DC CD86+, d3','Early cellular (d2-5)','-- (tissue only)',+1),
('S04-A','d7','ICOS-high','ICOS-high Tfh, d7','Germinal centre (d7)','Blood ICOS+PD-1+CXCR5+ cTfh at d7',+1),
('S04-B Foxp3','d7','Tfr','Tfr (Foxp3+) in Tfh gate, d7','Germinal centre (d7)','Blood cTfr:cTfh ratio at d7',-1),
('S03-K','d7','GC B','GC B cells, d7','Germinal centre (d7)','Blood plasmablasts d7 (proxy)',+1),
('S03-C','d14','HAI','HAI anti-CA09, d14','Antibody (d14-28)','HAI GMT & seroconversion (licensure surrogate)',+1),
('S03-G','d14','HAI','HAI anti-Aichi, d14','Antibody (d14-28)','HAI GMT & seroconversion',+1),
('S03-D','d14','Neutralising','Neut anti-CA09, d14','Antibody (d14-28)','Microneutralisation titre',+1),
('S03-A','d14','IgG','IgG anti-CA09, d14','Antibody (d14-28)','HA-specific IgG (ELISA)',+1),
('S05-D','d3','Ki-67','Lung Ki-67+ CD8, d3','CD8 (d3-25)','Blood Ki-67+ CD8 at d7',+1),
('S05-F','d14','IFN-g','IFN-g+ CD8 (H5 restim), d14','CD8 (d3-25)','IFN-g ELISpot to conserved NP/M1',+1),
('S05-I','d25','TRM','Lung TRM CD69+CD103+, d25','CD8 (d3-25)','Nasal TRM (curettage; exploratory)',+1),
('S05-G','d60','IFN-g','IFN-g+ CD8 (H5 restim), d60','Memory (d60)','IFN-g ELISpot at d180',+1),
]
def get(blk,t,sub,g):
    d=C[(C.block==blk)&(C.time==t)&(C.measurand.str.contains(sub,regex=False))&(C.group==g)]
    return d.value.values
rows=[]
for blk,t,sub,lab,stage,hum,sgn in CAND:
    prot=np.concatenate([get(blk,t,sub,'PSLN-344'),get(blk,t,sub,'PSLN-212(Y)')])
    nonp=np.concatenate([get(blk,t,sub,'Sham'),get(blk,t,sub,'PSLN-212')])
    if len(prot)==0 or len(nonp)==0: continue
    auc=stats.mannwhitneyu(prot*sgn,nonp*sgn).statistic/(len(prot)*len(nonp))
    if sgn>0: gap=prot.min()-nonp.max(); thr=(prot.min()+nonp.max())/2
    else: gap=nonp.min()-prot.max(); thr=(nonp.min()+prot.max())/2
    cmp=get(blk,t,sub,'CMP-204')
    rows.append(dict(stage=stage,biomarker=lab,block=blk,n_protective=len(prot),n_nonprotective=len(nonp),AUC=auc,
                     separation_gap=gap,cut_between=thr if gap>0 else np.nan,
                     aged344_mean=get(blk,t,sub,'PSLN-344').mean(),aged212_mean=get(blk,t,sub,'PSLN-212').mean(),
                     young212_mean=get(blk,t,sub,'PSLN-212(Y)').mean(),sham_mean=get(blk,t,sub,'Sham').mean() if len(get(blk,t,sub,'Sham')) else np.nan,
                     cmp204_mean=cmp.mean() if len(cmp) else np.nan,human_analogue=hum))
R=pd.DataFrame(rows); R.to_csv('/tmp/work/tables/biomarker_screen.csv',index=False)
pd.set_option('display.width',250); pd.set_option('display.max_colwidth',40)
print(R.drop(columns=['human_analogue']).round(3).to_string(index=False))
