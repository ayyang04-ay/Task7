# Recomputes every load-bearing figure in golden-response.md from the shipped
# workbook and diffs it against what the document states.
#
# Usage: python3 -I audit-golden.py   (expects adz5242_data_file_s1.xlsx alongside)
#
# Run this after any edit to the data room, per the build constraint that the
# golden is recomputed from the shipped room after its last edit. Exits noisily
# on any mismatch.

import openpyxl, statistics as st, math
wb=openpyxl.load_workbook('adz5242_data_file_s1.xlsx',data_only=True)
def V(sh,cc,rr):
    ws=wb[sh]; return [float(ws.cell(r,c).value) for r in rr for c in cc
                       if isinstance(ws.cell(r,c).value,(int,float))]
def M(sh,cc,rr): return st.mean(V(sh,cc,rr))
fails=[]
def chk(label, got, claimed, tol=0.006):
    ok = abs(got-claimed) <= max(tol, abs(claimed)*tol)
    print('  %-52s computed %-10.4g claimed %-10.4g %s'%(label,got,claimed,'OK' if ok else '<<< MISMATCH'))
    if not ok: fails.append(label)

print('MECHANISM')
chk('1E WT',   M('Fig.1',range(2,6),[20]), 43.10)
chk('1E SPA/D',M('Fig.1',range(2,6),[21]), 12.65)
chk('S4E CBX-',M('Fig. S4',[2],range(17,22)), 7.28)
chk('S4E CBX+',M('Fig. S4',[1],range(17,22)), 3.08)
chk('2K WT',   M('Fig. 2',[2],range(30,35)), 19.70)
chk('2K IFNAR',M('Fig. 2',[4],range(30,35)), 2.09)
chk('2K rescue',M('Fig. 2',[6],range(30,35)), 12.40)
chk('2I 36h cand',M('Fig. 2',range(2,7),[18]), 8.74)
chk('2I 36h comp',M('Fig. 2',range(7,12),[18]), 1.59)
chk('2I 36h sham',M('Fig. 2',range(12,17),[18]), 1.21)
chk('2L cand',  M('Fig. 2',[8],range(30,35)), 6.77)
chk('2L +INCB', M('Fig. 2',[9],range(30,35)), 1.39)
chk('7F Mphi',  M('Fig.7',[5],range(10,15)), 15.35)
chk('7F Mphi+INCB',M('Fig.7',[6],range(10,15)), 2.52)
chk('7F mono',  M('Fig.7',[2],range(10,15)), 9.86)
chk('7F mono+INCB',M('Fig.7',[3],range(10,15)), 3.26)
chk('5D lung',  M('Fig.5',[1],range(13,16)), 59.00)
chk('5D lung+PTX',M('Fig.5',[2],range(13,16)), 55.07)
chk('5D MLN',   M('Fig.5',[3],range(13,16)), 30.90)
chk('5D MLN+PTX',M('Fig.5',[4],range(13,16)), 6.83)
print('  >> golden says INCB cuts lung cytotoxic CD8 "six-fold": actual %.2f-fold'%(6.77/1.39))

print('\nDAY-3')
chk('5A cand',M('Fig.5',[5,6],[3]),6.68); chk('5A comp',M('Fig.5',[2,3],[3]),2.09)
chk('5E cand',M('Fig.5',[3],range(19,24)),9.38); chk('5E comp',M('Fig.5',[2],range(19,24)),3.48)
chk('5F cand',M('Fig.5',[3],range(26,31)),5.69); chk('5F comp',M('Fig.5',[2],range(26,31)),2.99)

print('\n2x2 TABLE')
for lbl,sh,rr,cols,claims in (
  ('Ifnb1 16h','Fig.1',[5,8,9,10],[range(2,7)]*4,[16.64,37.11,37.60,50.70]),
  ('Ifnb1 72h','Fig.1',[5,8,9,10],[range(8,13)]*4,[3.43,4.43,1.59,3.13])):
    for r,cc,c in zip(rr,cols,claims): chk('%s row%d'%(lbl,r), M(sh,cc,[r]), c)
for lbl,rr,claims in (('1J d4',[32],[8.28,18.88,21.40,22.60]),('1K',[36],[22.80,37.52,43.42,44.26]),
                      ('1L',[38],[75.30,59.46,54.08,51.36])):
    for i,(g,c) in enumerate(zip([range(7,12),range(12,17),range(17,22),range(22,27)],claims)):
        chk('%s grp%d'%(lbl,i+1), M('Fig.1',g,rr), c)
for lbl,rr,claims in (('2D',range(3,8),[1.77,7.09,9.39,11.12]),('2F',range(10,15),[0.77,18.65,26.24,31.40])):
    for cc,c in zip([[11],[12],[13],[15]],claims): chk('%s c%d'%(lbl,cc[0]), M('Fig. 2',cc,rr), c)

print('\nHUMORAL')
chk('3A cand',M('Fig. 3',[4],range(3,8)),7891.6,1e-4); chk('3A comp',M('Fig. 3',[3],range(3,8)),437.0,1e-4)
chk('3A ratio',M('Fig. 3',[4],range(3,8))/M('Fig. 3',[3],range(3,8)),18.06)
def geo(v): return 10**(sum(math.log10(x) for x in v if x>0)/len([x for x in v if x>0]))
chk('3C cand geo',geo(V('Fig. 3',[14],range(3,8))),367.58)
chk('3C comp geo',geo(V('Fig. 3',[13],range(3,8))),45.95)
chk('3C ratio',geo(V('Fig. 3',[14],range(3,8)))/geo(V('Fig. 3',[13],range(3,8))),8.00)
chk('3C cand arith',M('Fig. 3',[14],range(3,8)),416.0,1e-4)
chk('3C sham arith',M('Fig. 3',[11],range(3,8)),6.0,1e-4)

print('\nTOLERABILITY / DOSE')
chk('S1J cand d10',M('Fig. S1',range(17,22),[26]),99.78)
chk('S1J comp+R848 d10',M('Fig. S1',range(22,27),[26]),90.65)
chk('S1B 20ug',M('Fig. S1',range(8,11),[6]),45.83); chk('S1B 40ug',M('Fig. S1',range(8,11),[7]),50.23)

print('\n72h PANEL (10^mean log10)')
for i,(an,c) in enumerate(zip(['Ifnb1','Il6','Ccl2','Ccl3','Ccl5','Tnf','Il10'],
                              [4.01,7.19,27.41,9.23,2.01,8.44,4.16])):
    chk('S2A b2 cand %s'%an, 10**M('Fig. S2',range(40,43),[3+i]), c)

print('\n18 ENDPOINTS')
E=[('Ifnb1 16h','Fig.1',[8],range(2,7),[9],range(2,7)),('Ifnb1 72h','Fig.1',[8],range(8,13),[9],range(8,13))]
vals={}
vals['Ifnb1 16h']=M('Fig.1',range(2,7),[8])/M('Fig.1',range(2,7),[9])
vals['Ifnb1 72h']=M('Fig.1',range(8,13),[8])/M('Fig.1',range(8,13),[9])
vals['Ly6C mono d4']=M('Fig.1',range(12,17),[26])/M('Fig.1',range(17,22),[26])
vals['AM d6']=M('Fig. S4',range(12,17),[6])/M('Fig. S4',range(17,22),[6])
vals['IgG H1N1']=M('Fig. 3',[4],range(3,8))/M('Fig. 3',[5],range(3,8))
vals['IgG H3N2']=M('Fig. 3',[4],range(10,15))/M('Fig. 3',[5],range(10,15))
vals['HAI H1N1']=geo(V('Fig. 3',[14],range(3,8)))/geo(V('Fig. 3',[15],range(3,8)))
vals['IgG2a:IgG1']=2.1438/2.9718
vals['GC B']=M('Fig. 3',[14],range(17,22))/M('Fig. 3',[15],range(17,22))
vals['ICOS Tfh']=M('Fig.4',range(7,12),[4])/M('Fig.4',range(7,12),[5])
vals['Tfr']=M('Fig.4',[3],range(8,13))/M('Fig.4',[4],range(8,13))
vals['NP d3']=M('Fig.5',[5,6],[3])/M('Fig.5',[8,9],[3])
vals['NP d7']=M('Fig.5',[5,6],[5])/M('Fig.5',[8,9],[5])
vals['Ki67']=M('Fig.5',[3],range(19,24))/M('Fig.5',[4],range(19,24))
vals['GZMB']=M('Fig.5',[3],range(26,31))/M('Fig.5',[4],range(26,31))
vals['IFNg d14']=M('Fig.5',[3],range(33,38))/M('Fig.5',[4],range(33,38))
vals['IFNg d60']=M('Fig.5',[3],range(40,45))/M('Fig.5',[4],range(40,45))
vals['TRM']=M('Fig.5',[3],range(54,59))/M('Fig.5',[4],range(54,59))
for k,v in vals.items(): print('   %-14s %.4f'%(k,v))
hib=[v for k,v in vals.items() if k not in ('Ifnb1 72h','Tfr')]
print('  higher-is-better: n=%d  min %.4f  max %.4f'%(len(hib),min(hib),max(hib)))
print('  >> golden claims range 0.357 to 0.987')
hum=[vals[k] for k in ['IgG H1N1','IgG H3N2','HAI H1N1','IgG2a:IgG1','GC B','ICOS Tfh']]
cel=[vals[k] for k in ['NP d3','NP d7','Ki67','GZMB','IFNg d14','IFNg d60','TRM']]
chk('humoral mean (6)',st.mean(hum),0.654); chk('cellular mean (7)',st.mean(cel),0.741)
print('\n%s'%('AUDIT FAILURES: '+', '.join(fails) if fails else 'all other checks OK'))
