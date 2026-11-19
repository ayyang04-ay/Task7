import pandas as pd, numpy as np
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
out='/tmp/outputs/PSLN-344_evidence_tables.xlsx'
R=pd.read_csv('continuous_results.csv')
# tidy, readable efficacy table
groups=['Sham','Vaccine','CMP-204','PSLN-212','PSLN-344','PSLN-212(Y)','PSLN-344(Y)']
rows=[]
for _,r in R.iterrows():
    d={'Readout':r.readout,'Block':r.block,'Scale / transform':('log10 analysis; centre = geometric mean' if r.transform=='log' else ('values are log10 fold; centre = mean log10' if 'log10' in r.readout else 'linear; centre = mean')),'Note':r.note}
    for g in groups:
        if f'{g}|center' in R.columns and not pd.isna(r.get(f'{g}|center')):
            d[f'{g} n']=int(r[f'{g}|n']); d[f'{g} centre']=r[f'{g}|center']; d[f'{g} 95% CI']=f"{r[f'{g}|lo']:.4g} – {r[f'{g}|hi']:.4g}"
    for k in ['PSLN-344 vs PSLN-212','PSLN-344 vs Sham','PSLN-344 vs PSLN-212(Y)','PSLN-344 vs CMP-204','PSLN-344(Y) vs PSLN-212(Y)']:
        if f'{k}|welch_p' in R.columns and not pd.isna(r.get(f'{k}|welch_p')):
            if f'{k}|ratio' in R.columns and not pd.isna(r.get(f'{k}|ratio')):
                d[f'{k}: effect']=f"ratio {r[f'{k}|ratio']:.3g} (95% CI {r[f'{k}|ratio_lo']:.3g}–{r[f'{k}|ratio_hi']:.3g})"
            else:
                d[f'{k}: effect']=f"diff {r[f'{k}|diff']:+.3g} pts (95% CI {r[f'{k}|diff_lo']:+.3g} to {r[f'{k}|diff_hi']:+.3g})"
            d[f'{k}: Welch p']=r[f'{k}|welch_p']; d[f'{k}: Tukey p (one-way ANOVA)']=r.get(f'{k}|tukey_p'); d[f'{k}: Mann-Whitney p']=r[f'{k}|mw_p']; d[f"{k}: Hedges g"]=r[f'{k}|hedges_g']
    if not pd.isna(r.get('restoration_index')): d['Restoration index (344 aged vs 212 aged→212 young)']=r.restoration_index
    d['ANOVA p (all groups in block)']=r.get('anova_p')
    rows.append(d)
eff=pd.DataFrame(rows)
readme=pd.DataFrame({'Item':[
 'Purpose','Source files','How to trace a number','Statistics','Transforms','Integrity tiers','Sheets'],
 'Description':[
 'Evidence tables supporting the PSLN-344 portfolio-review proposal (1 Nov 2026). Every number in the proposal cites a block (e.g., S03-C) and one of these sheets (ET#).',
 'psln_program_dataset.xlsx (15 sheets; last saved 3 Sep 2026) and psln_program_annotation.pdf (15 Sep 2026). Values were re-read cell by cell; see ET13–ET15 for the per-animal source data with cell addresses.',
 'Find the readout in ET2/ET3–ET6, note the block, then filter ET13/ET14/ET15 by block and group to see each per-animal value and its cell address in the original workbook.',
 'Stated methods were applied: one-way ANOVA + Tukey HSD, two-way ANOVA, Student/Welch t-tests, log-rank. Added: Mann–Whitney (robustness), Fisher exact, Kaplan–Meier, Mantel–Haenszel/CMH and stratified log-rank for pooling. Log-rank verified against lifelines (max |Δp| 3e-16).',
 'Titres and fold-changes analysed on log10 scale (geometric means, ratio CIs). HAI values of 0 (<1:10 LOD) set to 5. Percentages analysed linearly.',
 'Tier A = all aged challenge blocks as printed, excluding the duplicated S06-D; Tier B = blocks whose survival and body-weight records agree in both PSLN-344 and PSLN-212 arms; Tier C = no detectable integrity flag (S06-B only).',
 'ET1 Claims index; ET2 Efficacy (continuous); ET3 Survival by block; ET4 Survival pairwise; ET5 Survival pooled; ET6 Mechanism & safety tests; ET7 Restoration index; ET8 Integrity findings; ET9 Body-weight exact duplicates; ET10 Body-weight offset signatures; ET11 Survival vs body-weight concordance; ET12 S11-A vs S11-B position match; ET13 Source data (continuous); ET14 Source data (survival); ET15 Source data (body weight).']})
sheets={'README':readme,'ET2_Efficacy_continuous':eff,'ET3_Survival_by_block':pd.read_csv('surv_summary.csv'),'ET4_Survival_pairwise':pd.read_csv('surv_pairwise.csv'),
        'ET5_Survival_pooled':pd.read_csv('pooled_survival.csv'),'ET6_Mechanism_safety':pd.read_csv('mech_results.csv'),'ET7_Restoration_index':pd.read_csv('fig2_data.csv'),
        'ET8_Integrity_findings':pd.read_csv('integrity_findings.csv'),'ET9_BW_exact_duplicates':pd.read_csv('bw_dup_exact.csv'),'ET10_BW_offset_signatures':pd.read_csv('bw_dup_signatures.csv'),
        'ET11_Surv_vs_BW':pd.read_csv('concordance.csv')}
t=pd.read_csv('tidy.csv')
a=t[t.block=='S11-A']; n=t[t.block=='S11-B']
m=a.merge(n,on=['group','time','rep'],suffixes=('_AM','_NEU'))[['group','time','rep','value_AM','cell_AM','value_NEU','cell_NEU']]
m['identical']=np.isclose(m.value_AM,m.value_NEU); sheets['ET12_S11A_vs_S11B']=m
sheets['ET13_Source_continuous']=t.drop(columns=['group_raw']).rename(columns={'group':'group (normalised)'})
sheets['ET14_Source_survival']=pd.read_csv('survival.csv')
sheets['ET15_Source_bodyweight']=pd.read_csv('bodyweight.csv')
pd.read_csv('pooled_survival.csv')
with pd.ExcelWriter(out,engine='openpyxl') as w:
    for k,v in sheets.items(): v.to_excel(w,sheet_name=k[:31],index=False)
wb=load_workbook(out)
for ws in wb.worksheets:
    for c in ws[1]: c.font=Font(bold=True,color='FFFFFF'); c.fill=PatternFill('solid',fgColor='305496'); c.alignment=Alignment(wrap_text=True,vertical='top')
    for col in ws.columns:
        L=max(len(str(c.value)) if c.value is not None else 0 for c in col[:200])
        ws.column_dimensions[get_column_letter(col[0].column)].width=min(max(10,L*0.9),70)
    ws.freeze_panes='B2'
for c in wb['README']['B']: c.alignment=Alignment(wrap_text=True,vertical='top')
wb['README'].column_dimensions['B'].width=140
ws=wb['ET8_Integrity_findings']
for row in ws.iter_rows(min_row=2):
    for c in row: c.alignment=Alignment(wrap_text=True,vertical='top')
    sev=row[1].value; col={'Critical':'F8CBAD','Major':'FFE699','Minor':'E2EFDA'}.get(sev)
    if col: row[1].fill=PatternFill('solid',fgColor=col)
for L,wd in zip('ABCDEFGH',[6,9,30,34,60,80,40,40]): ws.column_dimensions[L].width=wd
wb.save(out); print('saved',out,[ws.title for ws in wb.worksheets])
# ---- add claims index as ET1 ----
ci=pd.read_csv('/tmp/work/claims_index.csv')
wb=load_workbook(out)
ws=wb.create_sheet('ET1_Claims_index',1)
ws.append(list(ci.columns))
for r in ci.itertuples(index=False): ws.append(list(r))
for c in ws[1]: c.font=Font(bold=True,color='FFFFFF'); c.fill=PatternFill('solid',fgColor='305496')
for L,wd in zip('ABCDEF',[10,9,70,70,45,45]): ws.column_dimensions[L].width=wd
for row in ws.iter_rows(min_row=2):
    for c in row: c.alignment=Alignment(wrap_text=True,vertical='top')
ws.freeze_panes='C2'
wb.save(out); print('ET1 added')
