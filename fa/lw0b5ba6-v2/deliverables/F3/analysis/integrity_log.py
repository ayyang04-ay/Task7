"""integrity_log.py - the discrepancy log: what was found, what it would do to the conclusions if taken at face value,
how it was handled in this analysis, and what the audit has to close.  Numbers come from the fact registry."""
from facts import FACTS
f = lambda k: FACTS[k]['text']

LOG = [
 dict(id='D1', rank='High', blocks='S03-B, S03-F vs S13-A to S13-D', title='IgG2a:IgG1 tables carry rotated column labels',
      finding=(f"The per-animal IgG2a/IgG1 quotients recomputed from the raw subclass titers [S13-A/B, S13-C/D] reproduce the printed values of S03-B and S03-F only after shifting the column "
               f"headers by one position: the column printed as PSLN-344 holds the PSLN-212 animals, the column printed as PSLN-212(Y) holds the PSLN-344 animals, and the column printed as "
               f"PSLN-212 holds the young animals. The raw-block labels are the ones that agree with the total-IgG rank order in S03-A and S03-E."),
      face=f"PSLN-344 would show an IgG2a:IgG1 ratio of {f('sub_h1_344_printed')} (H1N1) and {f('sub_h3_344_printed')} (H3N2), i.e. lower than PSLN-212, instead of {f('sub_h1_344')} and {f('sub_h3_344')}.",
      handling='Ratios recomputed from the raw subclass blocks; S03-B and S03-F not used.', audit='Correct the headers of S03-B and S03-F against the ELISA plate records.'),
 dict(id='D2', rank='High', blocks='S03-I vs S13-F', title='Matched-strain challenge: survival table and weight table disagree on groups and on PSLN-212 outcome',
      finding=(f"S13-F is annotated as the body weights of the S03-I animals, but its groups are PSLN-212(Y), Sham, PSLN-212, PSLN-344 and Naive, whereas S03-I lists Sham, CMP-204, PSLN-212, PSLN-344 and "
               f"PSLN-212(Y). In S03-I all 7 PSLN-212 animals die by day 6; in S13-F {f('s13f_212_recover')} PSLN-212 animals regain weight and {f('s13f_212_flat')} carry a repeated value from day 10. "
               f"The S13-F 'Naive' pattern (all lost by day 8) resembles the S03-I 'PSLN-212' column, and the S13-F 'PSLN-212' pattern resembles the S03-I 'CMP-204' column ({f('surv_S03-I_cmp')} alive)."),
      face=f"The PSLN-212 result in the matched-strain challenge is either {f('surv_S03-I_212')} or 3/7, and a CMP-204 arm either exists ({f('surv_S03-I_cmp')}) or does not. PSLN-344 is {f('surv_S03-I_344')} in both tables.",
      handling=f"Survival table used as printed in the pooled analysis; worst-case analysis uses 3/7 for PSLN-212 (PSLN-344 7/7 vs 3/7 alone gives {f('fisher_7v3')}). The comparison with CMP-204 on survival is not relied on.",
      audit='Establish from animal-room records which five groups were in this experiment and re-export both tables with animal IDs.'),
 dict(id='D3', rank='High', blocks='S03-J vs S13-G', title='Wild-type H5N1 challenge: groups differ between tables; n and one time value inconsistent',
      finding=(f"S03-J lists Sham, PSLN-212, PSLN-344; S13-G (same animals per the annotation) lists PSLN-344, Sham, Naive. The S13-G 'Naive' arm ({f('s13g_naive_recover')} recovering, early losses) resembles the S03-J "
               f"'Sham' column ({f('surv_S03-J_sham')}); the S13-G 'Sham' arm ({f('s13g_sham_recover')} recovering) resembles the S03-J 'PSLN-212' column ({f('surv_S03-J_212')}). S03-J is labeled n=9 but has 10 rows per group; "
               f"S13-G is labeled n=10. One PSLN-344 row in S03-J has an event code but no day. The annotation gives 22 days of observation; survivors are recorded at day 21."),
      face='A PSLN-212 arm may not have been part of the wild-type H5N1 experiment at all, in which case it says nothing about PSLN-344 versus PSLN-212.',
      handling=f"PSLN-344 result ({f('surv_S03-J_344')}) used; the row without a day treated as alive at day 21. The two control arms are reported without relying on their identity. The worst-case analysis drops the PSLN-212 arm of this block.",
      audit='Confirm group identities and n (9 or 10) from BSL-3 records; supply the missing time value.'),
 dict(id='D4', rank='High', blocks='S06-E, S06-F, S06-G (rows 34-105); S15-E, S15-F, S15-G', title="'Untreated' animals in the day-60 blocks were not challenged",
      finding=(f"Per the annotation these animals received no vaccine, no adjuvant and no virus. {f('untreated_dead_frac')} died during the 14-day window, with recorded body weights staying within {f('untreated_bw_range')} of baseline."),
      face=f"Read as infected controls, these animals ({f('untreated_surv')} alive) would make PSLN-344 ({f('d60_344_frac')} alive) look no better than no treatment.",
      handling='Used as the estimate of background mortality in animals of this age, not as a challenge control. Challenged controls are the Sham arms.',
      audit='Rename the group (for example "unchallenged, age-matched") in the locked dataset.'),
 dict(id='D5', rank='Medium', blocks='S09-A (columns X to AS) vs S01-A', title="Second cytokine panel carries the same '16h' label as the first",
      finding=(f"Both S09-A panels are labeled '16h'. The Ifnb1 group means of the second panel match the 72 h data of S01-A (root-mean-square difference {f('rms_p2_72')} log10 units) and not the 16 h data ({f('rms_p2_16')})."),
      face='The later time point would be missed, and with it the only information on how quickly lung cytokines resolve.',
      handling='Second panel treated as a 72 h time point; every statement that depends on this says so.', audit='Confirm the time point from the qPCR run records and relabel.'),
 dict(id='D6', rank='Medium', blocks='S09-A vs S01-A, S08-A', title='Mixed scales for the same measurand',
      finding='S09-A stores log10 fold-change; S01-A and S08-A store linear fold-change for the same transcript. Titers are stored on a linear scale.',
      face='Reading S09-A as linear would understate induction by orders of magnitude (a stored value of 2.77 means 590-fold, not 2.77-fold).',
      handling='S09-A back-transformed; titers and fold-changes analyzed on the log scale (geometric means).', audit='State scale in every block header.'),
 dict(id='D7', rank='High', blocks='S11-A vs S11-B', title='Neutrophil block shares values with the alveolar-macrophage block',
      finding=(f"{f('s11_same')} cells are identical between the two blocks; the first replicate is identical in {f('s11_rep1')} group-by-time cells and the second in {f('s11_rep2')}. "
               f"The annotation says the two blocks came from different lung preparations."),
      face='Neutrophil influx is a basic lung-safety readout; as delivered, the block cannot support any statement about it.',
      handling='S11-B excluded. The workbook therefore contains no usable neutrophil data for either formulation.', audit='Re-export S11-B from the flow-cytometry files.'),
 dict(id='D8', rank='Medium', blocks='S13-F, S13-G, S15-A to S15-O', title='Animals that left the study are encoded two ways in the body-weight blocks',
      finding='Some groups use blank cells after the last weighing (for example Sham in S15-A to S15-O). Others repeat the last value unchanged to day 14 (for example PSLN-212 in S15-A to S15-G, and the Sham and Naive groups of S13-G).',
      face='Group means computed from the cells as printed would treat dead animals as stable at about 80% of baseline.',
      handling='Trailing repeated values treated as end of observation (three identical final cells, or two below 90%); post-challenge weight summaries use survivors only.',
      audit='Store one row per animal with an explicit status column.'),
 dict(id='D9', rank='High', blocks='S15-C/S15-I; S09-E/S15-M; S15-A/S15-M/S15-O; S09-C', title='Identical body-weight series recur in different experiments',
      finding=(f"{f('dup_s15c_s15i')} cells (days 2-12) are identical between the PSLN-344 arm of S15-C (challenge on day 14) and the vaccine + PSLN-344 arm of S15-I (challenge on day 3). Six of the seven young C57BL/6 "
               f"trajectories in S15-M share four to seven of their seven post-baseline values with young BALB/c PSLN-344 trajectories in S09-E; two PSLN-344 trajectories of S15-A (BALB/c) largely reappear in S15-M (C57BL/6) and in part in S15-O (Swiss Webster); the day-4 Sham row of S15-A equals the "
               f"day-4 PSLN-212 row of S15-M; the day-12 row of S09-C is identical in the PSLN-212Y and PSLN-344Y groups ({f('dup_s09c')} values)."),
      face='Body-weight curves would be presented as independent confirmation in three strains when part of the data is shared between blocks.',
      handling='Body weight used only as supporting evidence; no conclusion rests on it. Survival tables are the primary record.', audit='Re-export every body-weight block from the balance records; this is the largest audit item.'),
 dict(id='D10', rank='Medium', blocks='S06-C/S15-C, S06-D/S15-D, S06-E/S15-E, S06-G/S15-G, S15-L/S15-M, S09-F/S09-G', title='Survival and weight tables differ by one or two animals',
      finding=("PSLN-344: 7/7 alive in S06-D but two animals carry repeated values from day 8 in S15-D; 5/7 in S06-E vs 6/7 in S15-E; 4/7 in S06-G vs 5 to 7 of 7 in S15-G. PSLN-212: 2/7 vs 1/7 (S06-C/S15-C), 0/7 vs 1/7 "
               "(S06-E/S15-E). Young benchmark: 7/7 vs 5/7 (S06-D/S15-D), 6/7 vs 7/7 (S15-L/S15-M). S09-F has 7 Sham rows; S09-G has 8 Sham animals."),
      face='Individual experiment results could move by one or two animals in either direction.',
      handling=f"Survival tables used as printed. A worst-case analysis takes, for each arm, whichever table is less favorable to PSLN-344: {f('sens_worst_344')} vs {f('sens_worst_212')}.",
      audit='Reconcile each animal across the two tables.'),
 dict(id='D11', rank='Medium', blocks='S08-C vs S01-B', title='Dye-uptake block with Mn-containing particle has a header order that conflicts with S01-B',
      finding=(f"For the same condition (liposomal dye without Mn, type I epithelial cells) S01-B gives {f('s01b_aec1')} and S08-C gives {f('s08c_col3')}. If the S08-C columns are read in the order "
               f"type II / type I for the plain particle, then type II / type I for the Mn particle, the two blocks agree ({f('s08c_col1')} and {f('s08c_col2')} vs {f('s01b_aec2')} and {f('s01b_aec1')})."),
      face=f"As printed, adding Mn²⁺ would cut delivery to type II cells from {f('s08c_col1')} to {f('s08c_col2')}; on the reconciled order it is {f('s08c_col1')} vs {f('s08c_col3')}.",
      handling='Not used for any claim. Whether Mn²⁺ changes cell targeting is left open.', audit='Confirm column order from the flow-cytometry export.'),
 dict(id='D12', rank='Medium', blocks='S07-C', title='Both arms carry the same label',
      finding=f"Both columns are labeled 'Ly6C-CD206+ MΦ' (means {f('s07c_b')} and {f('s07c_c')}); the annotation says one arm received Ly6C+CD206- and the other Ly6C-CD206+ macrophages.",
      face='The direction of the macrophage-to-regulatory-T-cell link cannot be assigned.', handling='Excluded; that link is shown as untested in the mechanism.', audit='Restore the column labels.'),
 dict(id='D13', rank='Low', blocks='S05-A, S05-B (and S05-I by reference)', title='Tetramer time course: n and conditions unclear',
      finding="Labeled n=3, two values per time point. The conditions text describes both ovalbumin immunization and influenza vaccination; the NP tetramer named is not stated to match the mouse strain used.",
      face='A CD8 kinetics claim would rest on two animals per point under ambiguous conditions.', handling='Described only; not used for any claim.', audit='Clarify conditions, strain and n.'),
 dict(id='D14', rank='Low', blocks='S13-E', title='Stated n differs from rows', finding='Labeled n=5; 7 rows per group.', face='Denominators would be wrong.', handling='7 per group used.', audit='Correct the label.'),
 dict(id='D15', rank='Low', blocks='S08 rows 89-101', title='Unlabeled data region', finding='13 values (day 14, event code 0) with no header, group names or block label.',
      face='Could be mistaken for part of S08-D.', handling='Excluded.', audit='Identify or delete.'),
 dict(id='D16', rank='Low', blocks='S06', title='Block labels reused; one challenge interval missing',
      finding="Labels 'S06-E' and 'S06-F' are each used for two different experiments (rows 32-68 and rows 69-98). The interval between vaccination and challenge is not given for the PR8 challenge of previously infected animals.",
      face='Results from the day-60 and the prior-infection experiments could be confused.', handling='Blocks separated by row range.', audit='Give each block a unique ID.'),
 dict(id='D17', rank='Medium', blocks='S15-L to S15-O', title='Other-strain experiments: challenge virus and interval not stated',
      finding='The annotation gives strain, age and vaccine for the C57BL/6 and Swiss Webster experiments but not the challenge virus or day. Their body-weight blocks are among those affected by D9.',
      face='The three-strain claim cannot be described fully.', handling='Included in pooled survival (survival tables only) and shown separately; flagged.', audit='Add the missing design details.'),
 dict(id='D18', rank='Low', blocks='S02-C, S02-E; S08-A', title='Arms not fully defined',
      finding="The 'PTX' arm in S02-C and S02-E does not state which adjuvant or age group received pertussis toxin. S08-A has an arm 'PSLN-344/R848' that is not in the materials list (which has PSLN-212/R848).",
      face='The PTX arm cannot be attributed to a formulation, and the S08-A arm cannot be matched to a described preparation.', handling='PTX arm used only as a migration-block control; the S08-A arm reported as printed.', audit='Complete the arm definitions.'),
 dict(id='D19', rank='Low', blocks='S03-C, S03-G; S13-I', title='Values below the assay floor recorded as numbers',
      finding='Three Sham HAI values are recorded as 0 although the lowest dilution tested was 1:10; two Sham IgG values in S13-I sit at 10.',
      face='Geometric means cannot be computed with zeros; arithmetic means would mislead.', handling='HAI zeros set to 5 (half the lowest dilution).', audit='Record as "<10".'),
 dict(id='D20', rank='Low', blocks='annotation vs workbook', title='Annotation and workbook are not fully in step',
      finding=("The annotation reports 7 Sham rows for S09-B; the workbook has 8 in S09-B and 7 in S09-F. The annotation describes PSLN-212 observations as declining in S13-F and S15-A where the workbook has every cell "
               "filled. The workbook was last saved on 3 September 2026 and the annotation is dated 15 September 2026."),
      face='The two files may describe different versions of the data.', handling='Workbook taken as the record; annotation used for definitions.', audit='Regenerate the annotation from the locked workbook.'),
]
DESIGN_LIMITS = [
 'All animals are female; there are no male data.',
 'Group sizes are 2 to 10; most immunology blocks have 5 animals and most challenge arms 7.',
 'The workbook holds one set of values per block; it does not say whether experiments were repeated, randomized or scored blind.',
 'Every efficacy experiment used a single adjuvant dose (20 µg) and a single administration.',
 'The antigen throughout is in-house formalin-inactivated whole virus, not a licensed split, subunit or recombinant vaccine.',
 'Particle size, charge, morphology, Mn content and stability are described as measured in the annotation, but no such data are in the workbook.',
 'There is no lung virus load, no mucosal IgA, no histopathology and no measurement of manganese in any tissue.',
]
if __name__ == '__main__':
    for e in LOG: print(e['id'], e['rank'], '|', e['title'])
    print(len(LOG), 'entries;', sum(1 for e in LOG if e['rank'] == 'High'), 'high')
