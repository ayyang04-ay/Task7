import pandas as pd
W = pd.read_csv('/tmp/work/weight_copy_sig.csv')
nonw = pd.read_csv('/tmp/work/nonweight_copy.csv')
s11 = nonw[(nonw.A=='S11-A')&(nonw.B=='S11-B')].iloc[0]
s01 = nonw[(nonw.A=='S01-B')&(nonw.B=='S08-C')].iloc[0]
top = W.sort_values('p_min').head(3)

REG = [
# id, severity, blocks, finding, evidence (cells), analysis, decision impact
('I-01','Critical','S08-D, S09-C, S09-E, S09-G, S15-A, S15-C, S15-F, S15-I, S15-J, S15-K, S15-M, S15-O',
 'Body-weight values duplicated across independent experiments/groups, either verbatim or with an identical 4-5-decimal fractional part plus an integer offset ("copy-and-shift").',
 f'{len(W)} block-group pairs significant after Bonferroni correction (2,628 pairs x 2 tests). Strongest: S15-C PSLN-344 vs S15-I "3d Vaccine+PSLN-344": 40 of 48 same-animal/same-day values identical (e.g., S15!W25:AC25 = S15!W74:AC74), chance expectation 0.4, p=1e-74; S08-D CMP-204 vs S15-F PSLN-212(Y): 14 of 20 high-precision values share 5-decimal fractional parts at integer offsets (e.g., S08!G22=97.79487 vs S15!B54=99.79487), p=2e-26; S15-A Sham day 4 = S15-M PSLN-212 day 4 for 7/7 animals incl. 89.42307692 and 90.10989011 (S15!I5:O5 = S15!W105:AC105).',
 'Positional-concordance test: same-animal-position matches vs chance rate estimated from off-position matches (binomial); fractional-fingerprint test for high-precision values; carried-forward repeats removed before testing.',
 'All challenge body-weight data excluded from the evidence base. Because these blocks are the paired records of the survival experiments, survival data require source verification before they can support investment.'),
('I-02','Critical','S11-A, S11-B',
 'Alveolar-macrophage (S11-A) and neutrophil (S11-B) percentages are identical for the same animals in 35/100 positions; replicate 1 identical in 19/20 group-timepoints, replicate 2 in 15/20.',
 f'e.g., S11!B3:C3 = S11!B10:C10 (23.5, 17.2); S11!Q5:R5 = S11!Q12:R12 (53.0, 44.1). Chance expectation {s11.expected:.2f}; p={s11.p:.0e}. Structurally identical block S11-D shows no such overlap.',
 'Same positional-concordance test across structurally parallel blocks.',
 'S11-A and S11-B excluded. Alveolar-macrophage and neutrophil kinetics are unknown.'),
('I-03','Critical','S09-C',
 'Day-12 body weights identical for all 8 PSLN-212Y and all 8 PSLN-344Y animals.',
 'S09!G18:N18 = S09!W18:AD18 (97.7, 95.2, 93.3, 93.5, 99.1, 96.9, 100.3, 99.8).',
 'Exact-match scan.', 'Excluded (weights not used).'),
('I-04','Major','S03-B, S03-F',
 'Printed group labels of the IgG2a/IgG1 ratio blocks are rotated relative to the primary subclass titres. As printed, PSLN-344 appears the most Th2-skewed group; recomputed from primary titres, it is Th1-skewed.',
 'S03-B "PSLN-212" = S13-A/S13-B PSLN-212(Y) ratios (max |diff| 1.8e-4); "PSLN-344" = PSLN-212 (3e-7); "PSLN-212(Y)" = PSLN-344 (3e-7). Same rotation in S03-F vs S13-C/S13-D.',
 'Per-animal recomputation of IgG2a/IgG1 from S13-A..D and best-match assignment.',
 'S03-B/F replaced by ratios recomputed from S13 primary titres. Source files must confirm which labels are correct.'),
('I-05','Major','S07-C',
 'Both transferred-macrophage groups carry the identical label "Ly6C-CD206+ MΦ", so the experiment (which macrophage subset raises lung Tregs) cannot be read.',
 'S07!B15 and S07!C15 identical; means 10.4% (B16:B20) vs 5.1% (C16:C20).',
 'Header inspection.', 'The "CD206+ macrophage -> Treg" arm of the MoA is unsupported until relabelled from source.'),
('I-06','Major','S09-A (columns X-AS)',
 'Second S09-A panel is labelled "16h" but reproduces the 72-h Ifnb1 values of S01-A.',
 'Mean |difference| of group log10 means vs S01-A 72 h = 0.02; vs S01-A 16 h = 0.90 (6 shared groups).',
 'Cross-block consistency check.', 'Treated as an unconfirmed 72-h panel; not used for primary claims.'),
('I-07','Major','S13-F, S13-G (vs S03-I, S03-J)',
 'Body-weight blocks stated to be "the animals of S03-I/S03-J" do not match those survival blocks. The group sets differ (S13-F has Naive and no CMP-204; S13-G has Naive and no PSLN-212), and the death counts conflict.',
 'S03-J Sham: 9/10 deaths incl. days 3 and 4 (S03!G17:H26) vs 10/10 Sham weights recorded to day 14 with only 2 carried-forward runs (S13!L43:U50). S03-I PSLN-212: 7/7 dead by day 6 (S03!A31:D37) vs 3 S13-F "PSLN-212" animals recovering to day 14 (S13!T40:V40).',
 'Survival-weight concordance analysis.', 'S13-F/G excluded. S03-I and S03-J downgraded to Tier B.'),
('I-08','Major','S08 rows 89-101',
 'Unlabelled survival-format region: 13 animals in two columns, all censored at day 14. No block label, group or condition.',
 'S08!A89:D101 (col C: 6 rows, col D: 7 rows).', 'Coverage audit.', 'Cannot be used. Origin must be established.'),
('I-09','Moderate','S03-J',
 'Stated n=9 but 10 records per group. One PSLN-344 record has an event value but no time.',
 'S03!G15 "n=9"; S03!J46=0 with S03!G46 blank.', 'n audit.', 'PSLN-344 10/10 survival reported with this caveat.'),
('I-10','Moderate','S13-E','Stated n=5, 7 records per group.','S13!R1 vs S13!S3:V30.','n audit.','Usable with caveat.'),
('I-11','Moderate','S05-A, S05-B',
 'Stated n=3 but 2 values per group per timepoint. Conditions are contradictory (OVA immunisation vs bivalent vaccine; NP366 tetramer readout).',
 'S05!B3:I10.', 'n audit + annotation review.', 'Excluded from inference.'),
('I-12','Moderate','S09-F, S09-G',
 'S09-F Sham has 7 survival records (stated 8) while S09-G has 8 Sham weight columns. The annotation attributes the 7-animal Sham group to S09-B, which actually has 8.',
 'S09!B66:B72 (7) vs S09!O66:V66 (8); S09!B12:B19 (8).', 'n audit.', 'Usable with caveat (young-animal data only).'),
('I-13','Moderate','S06-C, S06-D',
 'Identical PSLN-212 outcome vectors (deaths d5, 8, 10, 10, 12; 2 survivors) and identical Sham vectors in two experiments. S15-D weights imply 2 deaths each in PSLN-344 and PSLN-212(Y) that S06-D does not record.',
 'S06!M10:O16 vs S06!A41:C47; S15!W37:W40 (79.5 carried d8-14), S15!AC36:AC40 (85.2 carried).',
 'Monte Carlo from pooled aged PSLN-212 outcomes: P(identical vectors) ~0.06% per pair.',
 'Downgraded to Tier B; excluded in sensitivity analysis.'),
('I-14','Moderate','S06-G, S06-E',
 'Unchallenged aged "Untreated" controls died: 3/7 in S06-G and 1/7 in S06-E (4/21 = 19% in 14 days). The 3 PSLN-344 deaths in S06-G are not reflected in the S15-G weights.',
 'S06!F99:F105; S06!L62:L68; S15!W63:AC70.', 'Survival-weight concordance.',
 'Background mortality in the aged colony biases aged survival downward and needs explaining (husbandry / health status).'),
('I-15','Moderate','S01-B, S08-C',
 'AECII/PSLN-SRB values for animals 1-2 are identical in two experiments that state different gating strategies.',
 f'S01!B14:C14 = S08!A14:A15 (17.7, 17.5); p={s01.p:.0e} (Bonferroni-significant).', 'Positional concordance.',
 'Possible reuse of control data. Kept for the PSLN vs free-SRB contrast (effect >40x) with caveat.'),
('I-16','Minor','S06','Block labels "S06-E" and "S06-F" are each used twice on the sheet.','S06!G32/G69, S06!M32/M69.','Label audit.','Renamed S06-E2/S06-F2 (imprinting) in this analysis.'),
('I-17','Minor','S15 (all weight blocks), S13-G',
 'Dead animals are handled inconsistently in weight blocks: blank after death in some groups, last value carried forward in others, sometimes within the same block.',
 'e.g., S15-A Sham blank (S15!I7:O10) vs S15-A PSLN-212 carried forward (S15!P6:P10 = 81.6).', 'Run-length analysis.', 'Group-mean weight curves computed from the workbook would be biased.'),
('I-18','Minor','S07-B, S11-E, S13-H, S14-A; S15-L, S15-N; S02-G, S02-H, S05-C, S08-A; S02-C/E',
 'Missing metadata: timepoint not stated (S07-B, S11-E, S13-H, S14-A); challenge virus and timing not stated (S15-L, S15-N); age not stated (S02-G, S02-H, S05-C, S08-A); adjuvant of the PTX group not stated (S02-C/E).',
 'Annotation PDF.', 'Annotation review.', 'Usable only descriptively for those dimensions.'),
('I-19','Minor','S10-A','Annotation says the block is reported as mean with SD, but it contains 5 per-animal values per group (PBS group means = 1.000 exactly).','S10!A3:N7.','Annotation vs data.','Treated as per-animal values; needs confirmation.'),
('I-20','Minor','S08-B',
 '"Encapsulation efficiency of CDN-1807 by A260" is reported for CMP-204 (cGAMP) and PSLN-R848 (no CDN-1807). A260 may be confounded by Mn coordination in PSLN-344.',
 'S08!A11:O11.', 'Method review.', 'Encapsulation efficiency needs an orthogonal assay (HPLC/LC-MS).'),
('I-21','Minor','Materials / S08-A','PSLN-344/R848 is used in S08-A but not defined. The Mn2+ content of PSLN-344 is not stated anywhere. "20 µg of adjuvant" is not defined as CDN, lipid or total mass.','Annotation p.1; S08!K2.','Annotation review.','Dose and Mn exposure cannot be scaled to humans until defined.'),
('I-22','Info','S04-B Tfh:Tfr','The "Tfh:Tfr" block is exactly (100 - Foxp3%)/Foxp3% of S04-B Foxp3. It is not an independent measurement.','S04!A15:D19 vs S04!A8:D12 (max |diff| 4e-6).','Arithmetic check.','Not counted as independent evidence.'),
('I-23','Info','All','Female mice only. No viral-load, histopathology, Mn-biodistribution or licensed-comparator data anywhere in the package.','Annotation p.1.','Scope review.','Gaps addressed in the next-step plan.'),
]
R = pd.DataFrame(REG, columns=['id','severity','blocks','finding','evidence_cells','analysis','decision_impact'])
R.to_csv('/tmp/work/integrity_register.csv', index=False)

# ---- evidence tier per block
TIER = {}
A_ = ['S01-A_16h','S01-A_72h','S01-C','S01-D','S01-E','S01-F','S01-G','S02-A','S02-B','S02-D_CD40','S02-D_CD86','S02-F','S02-I','S03-A','S03-C','S03-D','S03-E','S03-G','S03-H','S03-K','S03-L_Aicda','S03-L_E47',
      'S04-A_ICOSlo','S04-A_ICOShi','S04-B_Foxp3','S04-C','S04-D','S05-D','S05-E','S05-F','S05-G','S05-H','S06-A','S06-B','S06-E','S06-F','S07-A','S09-A_panel1_A-U','S09-B','S09-D',
      'S11-C','S11-D','S12-A','S13-A','S13-B','S13-C','S13-D','S13-I','S13-J']
B_ = {'S01-B':'I-15','S02-C':'I-18 (PTX adjuvant)','S02-E':'I-18 (PTX adjuvant)','S02-G':'I-18 (age)','S02-H':'I-18 (age)','S03-I':'I-07','S03-J':'I-07, I-09','S05-C':'I-18','S05-I':'ambiguous reference to S05-A conditions',
      'S06-C':'I-13','S06-D':'I-13','S06-G':'I-14','S06-E2_imprint':'I-16 (14-month animals)','S06-F2_imprint':'I-16 (14-month animals)','S07-B_Mono':'I-18','S07-B_Ly6CMac':'I-18','S08-A':'I-18, I-21','S08-B':'I-20','S08-C':'I-15',
      'S08-D':'I-01 (CMP-204 column implicated)','S09-F':'I-12','S10-A_Ifnb1':'I-19','S10-A_Tnf':'I-19','S10-A_Isg15':'I-19','S11-E':'I-18','S13-E':'I-10','S13-H':'I-18','S14-A_H1N1':'I-18','S14-A_H3N2':'I-18',
      'S15-H':'I-01 (paired weights copied)','S15-L':'I-18','S15-N':'I-18'}
C_ = {'S03-B':'I-04 (use recomputed S13 ratios)','S03-F':'I-04 (use recomputed S13 ratios)','S05-A':'I-11','S05-B':'I-11','S07-C':'I-05','S09-A_panel2_X-AS':'I-06','S11-A':'I-02','S11-B':'I-02',
      'S09-C':'I-01, I-03','S09-E':'I-01','S09-G':'I-01','S13-F':'I-07','S13-G':'I-07','S15-A':'I-01','S15-B':'I-01 (family)','S15-C':'I-01','S15-D':'I-01 (family), I-13','S15-E':'I-01 (family)','S15-F':'I-01',
      'S15-G':'I-01 (family), I-14','S15-I':'I-01','S15-J':'I-01','S15-K':'I-01','S15-M':'I-01','S15-O':'I-01','S08-UNLABELLED':'I-08'}
D_ = {'S04-B_TfhTfr':'I-22 (derived)'}
rows=[]
for b in A_: rows.append((b,'A','usable',''))
for b,r in B_.items(): rows.append((b,'B','usable with caveat',r))
for b,r in C_.items(): rows.append((b,'C','excluded / not usable as printed',r))
for b,r in D_.items(): rows.append((b,'D','derived (not independent)',r))
T = pd.DataFrame(rows, columns=['block','tier','meaning','register_ref'])
df = pd.read_csv('/tmp/work/tidy.csv')
missing = set(df.block.unique()) - set(T.block)
print('blocks without tier:', missing)
T.to_csv('/tmp/work/evidence_tiers.csv', index=False)
print(T.tier.value_counts())
print(R[['id','severity','blocks']].to_string())
