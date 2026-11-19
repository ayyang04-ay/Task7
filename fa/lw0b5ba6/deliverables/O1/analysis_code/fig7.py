import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({'font.size':8,'font.family':'DejaVu Sans'})
fig, ax = plt.subplots(figsize=(11,3.9)); ax.axis('off'); ax.set_xlim(0,100); ax.set_ylim(0,40)
boxes = [
 (0.5, 'GATE 0\nData-integrity remediation', 'Source-verify every survival\nrecord and all Tier B/C blocks\n(I-01..I-23); correct labels;\ndefine dose, Mn2+ content and\nS15-L/N challenge conditions.\nNo new animals.', '#fde0dd'),
 (25.5,'GATE 1\nIndependent confirmation', 'S1: blinded replication, aged,\n2 strains, both sexes, n=25/arm,\nwith Mn2+-only and licensed-\nbenchmark arms.\nS2: Mn2+ biodistribution and\nCNS safety.  S3: CMC.', '#fee6ce'),
 (50.5,'GATE 2\nTranslational de-risking', 'S4: dose-ranging/reactogenicity.\nS5: per-animal correlates.\nS6: durability and boost.\nS7: ferret, human-relevant\ndelivery.  S8: mechanism\nclosure (STING-KO, uptake).', '#e5f5e0'),
 (75.5,'IND-enabling\n(GLP tox, GMP)', 'Only if Gates 0-2 pass.\nRoute-matched repeat-dose\ntoxicology in 2 species;\nGMP process; antigen\npartner.', '#deebf7')]
for x,t,b,c in boxes:
    ax.add_patch(FancyBboxPatch((x,10),23,27,boxstyle='round,pad=0.3',fc=c,ec='#444444',lw=0.8))
    ax.text(x+11.5,35.5,t,ha='center',va='top',fontsize=8.5,weight='bold')
    ax.text(x+11.5,28.0,b,ha='center',va='top',fontsize=7.3, linespacing=1.35)
for x in [24.0,49.0,74.0]:
    ax.annotate('',xy=(x+1.6,23.5),xytext=(x-0.2,23.5),arrowprops=dict(arrowstyle='->',lw=1.4))
kills = [(12,'KILL if survival records cannot be\nverified, or fabrication is found'),
         (37,'KILL if PSLN-344 minus PSLN-212 < 40 pts,\nMn2+ accumulates in brain, or the\nlicensed benchmark is clearly better'),
         (62,'KILL/re-formulate if no dose gives\nefficacy with nadir loss <=5%, or no\ntranslation in the second species')]
for x,t in kills:
    ax.text(x,0.5,t,ha='center',va='bottom',fontsize=7,color='#b2182b', linespacing=1.3)
ax.set_title('Fig. 7  Proposed gated plan: spend is released one gate at a time, with pre-specified pass and kill criteria (Section 2)', fontsize=9, loc='left')
plt.tight_layout(); plt.savefig('/tmp/outputs/figures/fig7_gated_plan.png', dpi=200)
