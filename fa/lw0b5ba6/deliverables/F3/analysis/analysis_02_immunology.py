"""
Analysis 2 - every single-timepoint ("scalar") block: descriptive statistics, the stated tests
(one-way ANOVA + Tukey HSD; Student/Welch t for two-group blocks) and robustness checks.

Scale rules (applied before testing; stated in every output row):
  * flow-cytometry percentages ............ linear
  * qPCR fold-change vs untreated ......... log10   (ratio data; geometric mean reported alongside the arithmetic mean)
  * antibody titres ....................... log2    (geometric mean titre, GMT); HAI values printed as 0 are below
                                                    the 1:10 starting dilution and are set to 5 (half the LOD)
  * S09-A is already stored as log10 ...... analysed as stored; back-transformed for reporting
Outputs: immunology_descriptives.csv, immunology_contrasts.csv, immunology_tukey.csv
"""
import numpy as np, pandas as pd, itertools, warnings
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multitest import multipletests
warnings.filterwarnings('ignore')
pd.set_option('display.width',260); pd.set_option('display.max_rows',900); pd.set_option('display.max_colwidth',60)

d = pd.read_csv('tidy_all_observations.csv')
d['group']=d.group.str.strip()

# block -> (measurand, unit, scale, timepoint)
B = {
 'S01-A/16h': ('Lung Ifnb1 mRNA, 16 h, adjuvant alone','fold vs untreated','log10','16 h'),
 'S01-A/72h': ('Lung Ifnb1 mRNA, 72 h, adjuvant alone','fold vs untreated','log10','72 h'),
 'S01-B': ('SRB+ alveolar epithelial cells, 16 h','%','linear','16 h'),
 'S01-C': ('DiD+ alveolar macrophages, 16 h (WT vs Sftpa1/Sftpd KO)','%','linear','16 h'),
 'S01-F': ('Lung cDC1, 72 h','%','linear','72 h'),
 'S01-G': ('Lung cDC2, 72 h','%','linear','72 h'),
 'S02-A': ('Lung CCR7+ migratory CD11b+ DC, 72 h','%','linear','72 h'),
 'S02-B': ('MLN CD11b+CD103- DC, 72 h','%','linear','72 h'),
 'S02-C': ('MLN OVA-AF647+ DC, 36 h','%','linear','36 h'),
 'S02-D CD40': ('CD40+ of MLN CD11b+ DC, day 3','%','linear','d3'),
 'S02-D CD86': ('CD86+ of MLN CD11b+ DC, day 3','%','linear','d3'),
 'S02-E': ('OT-I proliferation driven by sorted MLN CD11b+ DC (ex vivo)','%','linear','DC d3 + 3 d co-culture'),
 'S02-G': ('Lung Ly6C+CD11c+MHC-II+ cells (moDC-like), day 5, +/- rGM-CSF','%','linear','d5'),
 'S02-H': ('Donor CD45.2+ moDC in lung, day 3 (BM transfer; WT vs Ifnar-KO)','%','linear','d3'),
 'S02-I': ('Lung GZMB+ CD8 T, day 5, +/- CCR2 antagonist (young)','%','linear','d5'),
 'S03-A': ('Serum IgG anti-CA09 H1N1, day 14','titre','log2','d14'),
 'S03-C': ('HAI anti-CA09 H1N1, day 14','titre','log2','d14'),
 'S03-D': ('Neutralising titre anti-CA09 H1N1, day 14','titre','log2','d14'),
 'S03-E': ('Serum IgG anti-Aichi H3N2, day 14','titre','log2','d14'),
 'S03-G': ('HAI anti-Aichi H3N2, day 14','titre','log2','d14'),
 'S03-H': ('Neutralising titre anti-Aichi H3N2, day 14','titre','log2','d14'),
 'S03-B': ('IgG2a/IgG1 quotient anti-H1N1 AS PRINTED (labels do not reconcile with S13-A/B)','ratio','log10','d14'),
 'S03-F': ('IgG2a/IgG1 quotient anti-H3N2 AS PRINTED (labels do not reconcile with S13-C/D)','ratio','log10','d14'),
 'S03-K': ('MLN germinal-centre B cells, day 7','%','linear','d7'),
 'S03-L/Aicda': ('MLN B-cell Aicda mRNA, day 5','fold vs untreated','log10','d5'),
 'S03-L/E47': ('MLN B-cell E47 mRNA, day 5','fold vs untreated','log10','d5'),
 'S04-A/ICOSlo': ('MLN ICOS-low Tfh, day 7','%','linear','d7'),
 'S04-A/ICOShi': ('MLN ICOS-high Tfh, day 7','%','linear','d7'),
 'S04-B Foxp3': ('MLN Tfr (Foxp3+ of CXCR5+ICOShi CD4), day 7','%','linear','d7'),
 'S04-B Tfh:Tfr': ('MLN Tfh:Tfr quotient, day 7','ratio','log10','d7'),
 'S04-C': ('MLN Tfr, day 30','%','linear','d30'),
 'S04-D': ('Lung Treg (CD4+Foxp3+), day 7','%','linear','d7'),
 'S05-C': ('OT-I proliferation in vivo, day 4, +/- pertussis toxin (PSLN-344 + OVA)','%','linear','d4'),
 'S05-D': ('Lung Ki-67+ CD8 T, day 3','%','linear','d3'),
 'S05-E': ('Lung GZMB+ CD8 T, day 3','%','linear','d3'),
 'S05-F': ('MLN IFN-g+ CD8 T after rgH5N1 restimulation, day 14','%','linear','d14'),
 'S05-G': ('MLN IFN-g+ CD8 T after rgH5N1 restimulation, day 60','%','linear','d60'),
 'S05-H': ('MLN GZMB+ CD8 T after rgH5N1 restimulation, day 60','%','linear','d60'),
 'S05-I': ('Lung resident-memory CD8 T (CD69+CD103+), day 25','%','linear','d25'),
 'S07-B/Mono': ('Lung CD11b+Ly6C+ monocytes +/- CCR2 antagonist','%','linear','not stated'),
 'S07-B/Ly6C+Mac': ('Lung Ly6C+ macrophages +/- CCR2 antagonist','%','linear','not stated'),
 'S07-C': ('Lung Treg after macrophage transfer (BOTH GROUPS CARRY THE SAME LABEL)','%','linear','d4 after transfer'),
 'S08-B': ('Encapsulation efficiency','%','linear','n/a'),
 'S08-C': ('SRB+ alveolar epithelial cells, PSLN vs PSLN-344 (labels conflict with S01-B)','%','linear','16 h'),
 'S10-A/Ifnb1': ('CNS Ifnb1 mRNA, 36 h','fold vs untreated','log10','36 h'),
 'S10-A/Tnf': ('CNS Tnf mRNA, 36 h','fold vs untreated','log10','36 h'),
 'S10-A/Isg15': ('CNS Isg15 mRNA, 36 h','fold vs untreated','log10','36 h'),
 'S11-C': ('Lung recruited monocytes, day 3, +/- carbenoxolone (PSLN-344)','%','linear','d3'),
 'S11-E': ('Lung CD206+ macrophages','%','linear','not stated'),
 'S12-A': ('Donor CD45.2+ monocytes infiltrating lung, day 3 (WT vs Ifnar-KO BM; young)','%','linear','d3'),
 'S13-A': ('Serum IgG2a anti-CA09 H1N1, day 14','titre','log2','d14'),
 'S13-B': ('Serum IgG1 anti-CA09 H1N1, day 14','titre','log2','d14'),
 'S13-C': ('Serum IgG2a anti-Aichi H3N2, day 14','titre','log2','d14'),
 'S13-D': ('Serum IgG1 anti-Aichi H3N2, day 14','titre','log2','d14'),
 'S13-H': ('IgG+ of MLN B220+ cells','%','linear','not stated'),
 'S13-I': ('Serum IgG anti-CA09 H1N1, day 28 after day-14 boost','titre','log2','d28'),
 'S13-J': ('Serum IgG anti-Aichi H3N2, day 28 after day-14 boost','titre','log2','d28'),
 'S14-A H1N1': ('MLN IFN-g+ CD8 T after CA09 H1N1 restimulation','%','linear','not stated (as S05-F)'),
 'S14-A H3N2': ('MLN IFN-g+ CD8 T after Aichi H3N2 restimulation','%','linear','not stated (as S05-F)'),
}
# add recomputed IgG2a/IgG1 quotients from the primary titres (same animal order, S13-A/B and S13-C/D)
extra=[]
for name,nb,db in [('IgG2a/IgG1 anti-H1N1 RECOMPUTED from S13-A / S13-B','S13-A','S13-B'),('IgG2a/IgG1 anti-H3N2 RECOMPUTED from S13-C / S13-D','S13-C','S13-D')]:
    n=d[d.block==nb]; m=d[d.block==db]
    for g in n.group.unique():
        a=n[n.group==g].sort_values('rep'); b=m[m.group==g].sort_values('rep')
        for (_,ra),(_,rb) in zip(a.iterrows(),b.iterrows()):
            extra.append(dict(sheet='S13',block=name,kind='scalar',group=g,cell=f'{ra.cell}/{rb.cell}',value=ra.value/rb.value,rep=ra.rep,col_order=ra.col_order))
    B[name]=(name,'ratio','log10','d14')
d=pd.concat([d,pd.DataFrame(extra)],ignore_index=True)

def tr(v,scale,block):
    v=np.asarray(v,float)
    if scale=='log10': return np.log10(v)
    if scale=='log2':
        v=np.where(v<=0,5.0,v)       # HAI below 1:10 -> 5
        return np.log2(v)
    return v
def back(m,scale):
    return 10**m if scale=='log10' else (2**m if scale=='log2' else m)

desc=[]; cons=[]; tuk=[]
KEY=[('PSLN-344','PSLN-212'),('PSLN-344','PSLN-212(Y)'),('PSLN-344','Sham'),('PSLN-212','Sham'),('PSLN-212(Y)','PSLN-212'),
     ('PSLN-344','CMP-204'),('PSLN-212','CMP-204'),('PSLN-344(Y)','PSLN-212(Y)'),('PSLN-344(Y)','PSLN-344'),('PSLN-344','PBS'),('PSLN-344','CT'),('CT','PBS'),('Sham','PBS'),
     ('PSLN-344','PSLN-212/R848'),('PSLN-344','PSLN-R848'),('PSLN-212/R848','PSLN-212')]
for blk,(meas,unit,scale,tp) in B.items():
    x=d[d.block==blk]
    if len(x)==0: print('missing',blk); continue
    groups=list(dict.fromkeys(x.group))
    data={g:x[x.group==g].sort_values('rep').value.astype(float).values for g in groups}
    tdata={g:tr(v,scale,blk) for g,v in data.items()}
    for g in groups:
        v=data[g]; t=tdata[g]; cells=x[x.group==g].cell
        ci=stats.t.interval(0.95,len(t)-1,loc=t.mean(),scale=stats.sem(t)) if len(t)>1 else (np.nan,np.nan)
        desc.append(dict(block=blk,measurand=meas,unit=unit,scale=scale,timepoint=tp,group=g,cells=f'{x.sheet.iloc[0]}!{cells.iloc[0]}:{cells.iloc[-1]}',
                         n=len(v),mean=v.mean(),sd=v.std(ddof=1),median=np.median(v),min=v.min(),max=v.max(),
                         centre_on_test_scale=back(t.mean(),scale),ci95_lo=back(ci[0],scale),ci95_hi=back(ci[1],scale),
                         values=' '.join(f'{q:g}' for q in v)))
    # omnibus + Tukey (stated method)
    if len(groups)>=3:
        F,pA=stats.f_oneway(*[tdata[g] for g in groups])
        allv=np.concatenate([tdata[g] for g in groups]); lab=np.concatenate([[g]*len(tdata[g]) for g in groups])
        tk=pairwise_tukeyhsd(allv,lab)
        tkd={(a,b):p for a,b,p in zip(tk._results_table.data[1:] and [r[0] for r in tk._results_table.data[1:]],[r[1] for r in tk._results_table.data[1:]],tk.pvalues)}
        for (a,b),p in tkd.items(): tuk.append(dict(block=blk,g1=a,g2=b,tukey_p=p,anova_F=F,anova_p=pA,scale=scale))
    else:
        F,pA=np.nan,np.nan; tkd={}
    pairs=[p for p in KEY if p[0] in groups and p[1] in groups]
    if len(groups)==2: pairs=[(groups[0],groups[1])]
    if blk in('S02-C','S02-E'): pairs+= [('PTX','PSLN-344'),('PTX','PSLN-212(Y)'),('PTX','PSLN-344(Y)')]
    if blk=='S02-G': pairs=[('PSLN-212+GM-CSF','PSLN-212'),('PSLN-212','GM-CSF'),('PSLN-212+GM-CSF','GM-CSF')]
    if blk=='S02-H': pairs=[('IFN w/o cDC','WT w/o cDC'),('IFN w/ cDC','WT w/ cDC'),('GMCSF','IFN w/o cDC'),('GMCSF','WT w/o cDC'),('WT w/ cDC','WT w/o cDC')]
    if blk=='S05-C': pairs=[('Lung+PTX','Lung'),('MLN+PTX','MLN'),('Lung','MLN')]
    if blk=='S01-B': pairs=[('AECII/PSLN-SRB','AECII/FreeSRB'),('AECI/PSLN-SRB','AECI/FreeSRB'),('AECII/PSLN-SRB','AECI/PSLN-SRB')]
    if blk=='S08-C': pairs=[('AECII-PSLN-344-SRB','AECII-PSLN-SRB'),('AECI-PSLN-344-SRB','AECI-PSLN-SRB')]
    if blk=='S08-B': pairs=[('PSLN-344','PSLN-212'),('PSLN-344','CMP-204')]
    for a,b in pairs:
        ta,tb=tdata[a],tdata[b]; va,vb=data[a],data[b]
        w=stats.ttest_ind(ta,tb,equal_var=False); st=stats.ttest_ind(ta,tb,equal_var=True)
        try: mw=stats.mannwhitneyu(va,vb,alternative='two-sided',method='exact').pvalue
        except Exception: mw=np.nan
        diff=ta.mean()-tb.mean()
        se=np.sqrt(ta.var(ddof=1)/len(ta)+tb.var(ddof=1)/len(tb))
        dfw=se**4/((ta.var(ddof=1)/len(ta))**2/(len(ta)-1)+(tb.var(ddof=1)/len(tb))**2/(len(tb)-1)) if se>0 else np.nan
        tcrit=stats.t.ppf(0.975,dfw) if se>0 else np.nan
        lo,hi=diff-tcrit*se,diff+tcrit*se
        if scale=='linear':
            eff=f'{va.mean():.3g} vs {vb.mean():.3g}'; est=diff; elo=lo; ehi=hi; efftype='difference of means'
            fold=va.mean()/vb.mean() if vb.mean()!=0 else np.nan
        else:
            base=10 if scale=='log10' else 2
            eff=f'{base**ta.mean():.4g} vs {base**tb.mean():.4g} (geometric means)'; est=base**diff; elo=base**lo; ehi=base**hi; efftype='ratio of geometric means'
            fold=est
        sp=np.sqrt(((len(ta)-1)*ta.var(ddof=1)+(len(tb)-1)*tb.var(ddof=1))/(len(ta)+len(tb)-2))
        cons.append(dict(block=blk,measurand=meas,scale=scale,g1=a,g2=b,n1=len(va),n2=len(vb),summary=eff,effect_type=efftype,effect=est,ci95_lo=elo,ci95_hi=ehi,fold=fold,
                         hedges_g=(diff/sp*(1-3/(4*(len(ta)+len(tb))-9)) if sp>0 else np.nan),
                         welch_p=w.pvalue,student_p=st.pvalue,mannwhitney_exact_p=mw,tukey_p=tkd.get((a,b),tkd.get((b,a),np.nan)),anova_p=pA))
D=pd.DataFrame(desc); C=pd.DataFrame(cons); T=pd.DataFrame(tuk)
# BH-FDR across the family of aged PSLN-344 vs aged PSLN-212 contrasts
m=(C.g1=='PSLN-344')&(C.g2=='PSLN-212')
C.loc[m,'welch_p_BH_family_344v212']=multipletests(C.loc[m,'welch_p'],method='fdr_bh')[1]
C.loc[m,'welch_p_holm_family_344v212']=multipletests(C.loc[m,'welch_p'],method='holm')[1]
# restoration index: share of the aged(212)->young(212) gap closed by PSLN-344, with bootstrap CI
ri=[]
rng=np.random.default_rng(7)
for blk,(meas,unit,scale,tp) in B.items():
    x=d[d.block==blk]; gs=set(x.group)
    if not {'PSLN-212','PSLN-344','PSLN-212(Y)'}<=gs: continue
    a=tr(x[x.group=='PSLN-212'].value,scale,blk); b=tr(x[x.group=='PSLN-344'].value,scale,blk); y=tr(x[x.group=='PSLN-212(Y)'].value,scale,blk)
    gap=y.mean()-a.mean()
    r=(b.mean()-a.mean())/gap if gap!=0 else np.nan
    bs=[]
    for _ in range(5000):
        aa=rng.choice(a,len(a)); bb=rng.choice(b,len(b)); yy=rng.choice(y,len(y)); g=yy.mean()-aa.mean()
        if g!=0: bs.append((bb.mean()-aa.mean())/g)
    gap_t=stats.ttest_ind(y,a,equal_var=False).pvalue
    ri.append(dict(block=blk,measurand=meas,scale=scale,aged212=back(a.mean(),scale),aged344=back(b.mean(),scale),young212=back(y.mean(),scale),
                   age_gap_welch_p=gap_t,restoration_pct=100*r,boot_lo=100*np.percentile(bs,2.5),boot_hi=100*np.percentile(bs,97.5),
                   aged344_vs_young212_welch_p=stats.ttest_ind(b,y,equal_var=False).pvalue))
R=pd.DataFrame(ri)
D.to_csv('immunology_descriptives.csv',index=False); C.to_csv('immunology_contrasts.csv',index=False); T.to_csv('immunology_tukey.csv',index=False); R.to_csv('immunology_restoration_index.csv',index=False)
if __name__=='__main__':
    f=lambda v: f'{v:.3g}'
    print(D[['block','group','cells','n','mean','sd','centre_on_test_scale','ci95_lo','ci95_hi']].to_string(float_format=f))
    print(C[['block','g1','g2','summary','effect','ci95_lo','ci95_hi','welch_p','mannwhitney_exact_p','tukey_p','anova_p']].to_string(float_format=f))
    print(R.to_string(float_format=f))
