"""Register of record defects found in the workbook/annotation, with the cells involved, the effect on conclusions and how each was handled."""
from paths import TABLES, FIGS, OUT as OUTDIR, BUILD, PANDOC
import pandas as pd, numpy as np
import psln_blocks as pb
from evidence import RANGE, R, df, sv, v
T = TABLES

# numbers used in the register, computed from the cells
a = df[df.block == 'S11-A']; b = df[df.block == 'S11-B']
mm = a.merge(b, on=['group', 'x', 'rep'], suffixes=('_A', '_B')); n_s11 = int((mm.value_A == mm.value_B).sum())
w = df[df.kind == 'weight'].copy(); w['col'] = w.cell.str.extract(r'!([A-Z]+)\d+')[0]; w['xf'] = w.x.astype(float)
ta = w[(w.block == 'S15-C') & (w.group == 'PSLN-344') & (w.xf.between(2, 12))].set_index(['col', 'xf']).value
tb = w[(w.block == 'S15-I') & (w.group == '3d Vaccine+PSLN-344') & (w.xf.between(2, 12))].set_index(['col', 'xf']).value
n_s15ci = int((ta == tb.reindex(ta.index)).sum()); n_s15ci_all = len(ta)
reuse = pd.read_csv(T + 'T3d_reused_weight_traces_summary.csv'); n_traces = int(reuse.animals.sum()); n_pairs = len(reuse)
days = lambda blk, g: ', '.join(str(int(x)) for x in sorted(sv[(sv.block == blk) & (sv.group == g) & (sv.event == 1)].value))

D = [
 dict(id='D1', sev='High', where=R('S06-D', 'S06-C', 'S15-D', 'S15-C'),
      what=f"The survival tables for the day-14 and the day-3 rgH5N1 challenge (S06-C and S06-D) are identical, animal for animal: vehicle deaths on days {days('S06-D','Sham')}, PSLN-212 deaths on days {days('S06-D','PSLN-212')} "
           "with two survivors, no deaths in the other two arms. One of them is presumably a copy. S06-C agrees with its weight block (S15-C: no deaths on PSLN-344 or in young animals), although that weight block shares its PSLN-344 traces with S15-I (D7). "
           "S06-D does not agree with its weight block (S15-D: two deaths on PSLN-344 and two in young animals).",
      effect="The table can count as one experiment, not two, and which challenge day it belongs to is uncertain. By its weight block the day-3 result for PSLN-344 would be 5 of 7, not 7 of 7.",
      handling="The table is counted once (as S06-C) in the headline figures and S06-D is left out of the rapid-protection figure. Table 2 shows the result with both copies removed."),
 dict(id='D2', sev='High', where=R('S03-I', 'S13-F'),
      what="The survival table lists the arms Sham, CMP-204, PSLN-212, PSLN-344, young; the weight block for 'the animals of S03-I' lists young, Sham, PSLN-212, PSLN-344, Naive. In the table PSLN-212 loses all 7 animals by day 6; "
           "in the weight block 'PSLN-212' has 3 survivors of 7 and the fast-dying pattern sits under 'Naive'.",
      effect="PSLN-344 (7 of 7) and the young benchmark (7 of 7) agree in both blocks. The size of the PSLN-344 advantage over PSLN-212 in this experiment depends on which block is right (7/7 vs 0/7, p = 0.0006; or 7/7 vs 3/7, p = 0.07), "
             "and the 3-of-7 result printed for the cGAMP formulation may belong to PSLN-212.",
      handling="Excluded from the headline figures; shown as printed in Figure 1 with a flag."),
 dict(id='D3', sev='High', where=R('S03-J', 'S13-G'),
      what="The survival table lists Sham, PSLN-212, PSLN-344; the weight block for 'the animals of S03-J' lists PSLN-344, Sham, Naive. The table's 'Sham' (9 of 10 dead) behaves like the weight block's 'Naive' (9 of 10 dead); the table's 'PSLN-212' "
           "(7 dead on days 10–12) behaves like the weight block's 'Sham' (5 carried-forward traces and a sixth animal still falling at day 14). The block label states n = 9 but each arm has 10 records, and the tenth PSLN-344 record has no day.",
      effect="PSLN-344 protects 10 of 10 against wild-type H5N1 in both blocks. Whether the comparator that protected 3 of 10 was PSLN-212 or vaccine with empty vehicle is unresolved.",
      handling="Excluded from the headline figures; the PSLN-344 arm is counted in the rapid-protection figure (10 of 10; 9 of 9 if the record without a day is dropped)."),
 dict(id='D4', sev='Medium', where=R('S03-B', 'S03-F', 'S13-A', 'S13-B', 'S13-C', 'S13-D'),
      what="The IgG2a/IgG1 ratio blocks carry the right 30 values under the wrong headers: the column printed 'PSLN-344' holds the PSLN-212 ratios, 'PSLN-212(Y)' holds the PSLN-344 ratios and 'PSLN-212' holds the young ratios "
           "(every value reproduced from the subclass titres in S13-A to S13-D).",
      effect="Read as printed, PSLN-344 would appear to give the lowest IgG2a/IgG1 ratio (0.58); the recomputed value is 2.14, close to young (2.97).", handling="Recomputed ratios used throughout."),
 dict(id='D5', sev='Medium', where=R('S11-A', 'S11-B'),
      what=f"{n_s11} of the 100 'neutrophil' values are identical, to the decimal, to the alveolar-macrophage value at the same group, day and animal position (chiefly the first animal of every group and the second animal of three groups); "
           "a further 5 (the second PSLN-212 animal) repeat the fourth PSLN-212 animal of the macrophage block.",
      effect="There is no usable neutrophil data, which is the read-out one would want for lung tolerability.", handling="S11-B not used. Replaced by a BAL neutrophil endpoint in Study 3."),
 dict(id='D6', sev='Medium', where=R('S09-A (cols X-AS)', 'S09-A (cols A-U)', 'S01-A'),
      what="Both cytokine panels are labelled '16h'. The Ifnb1 row of the second panel reproduces the 72-hour values of S01-A for all seven groups (21 of 21 values), so the second panel is 72-hour data. "
           "The control column is labelled 'PBS' here and 'Sham' in S01-A for the same animals.",
      effect="Taken at face value, the 72-hour inflammatory read-out would be mistaken for a replicate of the 16-hour one. Whether the control was buffer or empty liposome is unclear.", handling="Second panel treated as 72 h and flagged wherever quoted."),
 dict(id='D7', sev='Medium', where=R('S15-C', 'S15-I', 'S09-E', 'S15-M', 'S15-A', 'S09-G', 'S09-C'),
      what=f"Body-weight traces recur across experiments that should be independent: all seven PSLN-344 animals of S15-C reappear in S15-I ({n_s15ci} of {n_s15ci_all} values from day 2 to day 12 identical); "
           f"in total {n_traces} animal traces are shared between {n_pairs} pairs of blocks (including young BALB/c traces of S09-E reappearing as young C57BL/6 in S15-M). "
           "The day-12 row of S09-C is identical for PSLN-212 and PSLN-344 (8 values), and the day-4 vehicle row of S15-A equals the day-4 PSLN-212 row of S15-M (7 values). The chance of two unrelated animals sharing one value is under 1%.",
      effect="Weight blocks cannot be treated as independent evidence. The survival tables paired with them are distinct from one another, apart from D1.", handling="Weights used only as supporting evidence (morbidity, and as a cross-check on survival tables)."),
 dict(id='D8', sev='Medium', where=R('S08-C', 'S01-B'),
      what=f"S08-C, as printed, gives {v('S08-C','AECI-PSLN-SRB').mean():.1f}% dye-positive type I epithelial cells for the Mn-free liposome; S01-B gives {v('S01-B','AECI/PSLN-SRB').mean():.1f}% for the same measurement. "
           f"Column B of S08-C (printed as the Mn liposome in type II cells, {v('S08-C','AECII-PSLN-344-SRB').mean():.1f}%) matches the S01-B type I value, which suggests columns B and C are transposed.",
      effect="As printed, Mn²⁺ cuts delivery to the epithelium four- to five-fold; with the columns transposed it does not change it. The question is open.", handling="Not used for any conclusion; repeat requested in Step 0 / Study 1."),
 dict(id='D9', sev='Medium', where='annotation PDF (block entries); ' + R('S15-L', 'S15-N', 'S06-E (rows 71-105)', 'S07-B', 'S11-E', 'S13-H', 'S14-A H1N1', 'S08-A', 'S02-C'),
      what="Conditions missing from the annotation: challenge virus, dose and day for the C57BL/6 and Swiss Webster studies (S15-L, S15-N); challenge day for the imprinting PR8 study; time points for S07-B, S11-E, S13-H and S14-A; animal age for S08-A; "
           "which adjuvant the pertussis-toxin groups received (S02-C, S02-E). 'PSLN-344/R848' (S08-A) is not in the materials list. Encapsulation of PSLN-R848 is reported by absorbance of CDN-1807, which that formulation does not contain. Manganese content is not reported, and it is not stated whether the 'sham' vehicle contains Mn²⁺.",
      effect="The two non-BALB/c strain experiments cannot be classed as matched or mismatched challenge; no manganese dose can be calculated.", handling="Results used as printed with the gap stated."),
 dict(id='D10', sev='Low', where=R('S07-C'), what="Both columns are headed 'Ly6C-CD206+ MΦ'. One should be the Ly6C+CD206- subset.",
      effect="The experiment shows that transferred macrophages change lung regulatory T cells (10.4% vs 5.1%) but not which subset does it.", handling="Not used to assign direction."),
 dict(id='D11', sev='Low', where=R('S03-J', 'S05-A', 'S05-B', 'S13-E', 'S09-F', 'S08-D'),
      what="Stated n differs from the records: S03-J states 9, has 10; S05-A and S05-B state 3, have 2 per time point; S13-E states 5, has 7; S09-F has 7 vehicle survival records for 8 animals in its weight block "
           "(the annotation attributes this shortfall to S09-B, which has 8); PSLN-212/R848 in S08-D has 4 of 5 animals on day 10.",
      effect="No effect on the main conclusions. The missing R848 animal is probably a death and is counted as a tolerability signal.", handling="Observed counts used."),
 dict(id='D12', sev='Low', where=R('S05-A', 'S05-B'),
      what="The conditions are self-contradictory (animals 'immunised with ovalbumin' and also 'vaccinated with the bivalent vaccine'), the tetramer named (NP366-374) does not fit the default BALB/c strain†, and there are 2 animals per time point.",
      effect="Tetramer data support the CD8 story (higher with PSLN-344) but cannot carry weight.", handling="Not used for any numbered claim."),
 dict(id='D13', sev='Low', where=R('S06-E (rows 34-68)', 'S06-E (rows 71-105)', 'S06-F (rows 34-68)', 'S06-F (rows 71-105)'),
      what="Sheet S06 uses the labels S06-E and S06-F twice (rows 34–68: day-60 challenges; rows 71–105: imprinting studies).", effect="Risk of citing the wrong block.", handling="Blocks cited with their row ranges."),
 dict(id='D14', sev='Low', where=R('S08 rows 89-101'), what="Thirteen values (day 14, flag 0; 6 in column C, 7 in column D) with no block label, header or group names.", effect="None; cannot be interpreted.", handling="Not used."),
 dict(id='D15', sev='Low', where=R('S13-F', 'S13-G', 'S15-A', 'S15-E', 'S15-I'),
      what="Dead animals are handled two ways in the weight blocks: cells left blank (mostly vehicle groups) or the last weight carried forward to day 14 (mostly adjuvant groups).",
      effect="Group mean weight curves after the first death are not comparable between arms.", handling="Per-animal lowest weight used instead of group mean curves."),
 dict(id='D16', sev='Low', where=R('S06-C', 'S15-C', 'S06-E (rows 34-68)', 'S15-E', 'S06-G', 'S15-G', 'S15-L', 'S15-M'),
      what="Survival tables and weight-implied deaths differ by one animal in five groups: S06-C PSLN-212 (5 vs 6 deaths), S06-E PSLN-212 (7 vs 6), S06-E PSLN-344 (2 vs 1), S06-G PSLN-344 (3 vs 2), S15-L young (1 vs 0).",
      effect="Net effect on the PSLN-344 total across the eleven experiments is zero once D1 is included (68 of 80 either way).", handling="Survival tables used; worst-case reading reported (66 of 80 vs 15 of 80)."),
]
DEF = pd.DataFrame(D)
if __name__ == '__main__':
    pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 120)
    print(DEF[['id', 'sev', 'what']].to_string()); print(len(DEF), 'defects;', (DEF.sev == 'High').sum(), 'high')
    DEF.to_csv(T + 'T17_record_defects.csv', index=False)
