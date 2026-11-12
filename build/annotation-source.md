# Dataset annotation

## Animals

Female BALB/c mice. Young animals were 7 to 8 weeks of age at the start of each
experiment. Aged animals were 20 months of age or older, except where a block
states otherwise. C57BL/6 mice at 15 or 20 months, Swiss Webster mice, 7 to
8-week-old Sftpa1-/-Sftpd-/- mice, OT-I mice and Ifnar-deficient mice were used in
the blocks that name them. Animals were housed in a pathogen-free facility. All
procedures were carried out under institutional animal care and use protocol
PCL-26-0417.

## Materials

Two nanoparticle preparations appear throughout. Both are pulmonary-surfactant
biomimetic liposomes containing DPPC, DPPG, DPPE-PEG2000 and cholesterol,
prepared by reverse-phase evaporation or thin-film rehydration, and both encapsulate the cyclic dinucleotide STING agonist CDN-1807.
They differ in one respect: PSLN-344 incorporates Mn2+ by coordination
polymerization and PSLN-212 does not. Three further preparations appear in
individual blocks: CMP-204, which encapsulates cGAMP in place of CDN-1807;
PSLN-R848, which encapsulates the TLR7/8 agonist R848; and PSLN-212/R848, which
encapsulates both CDN-1807 and R848.

Where a block names "sham", the animals received empty liposome vehicle in saline
alongside the vaccine. Where a block names "PBS" or "vehicle", the animals received
buffer alone.

Encapsulation efficiency of CDN-1807 was determined by absorbance at 260 nm.
Particle size and zeta potential were measured by dynamic light scattering, and
particle morphology by transmission electron microscopy. Trehalose was added to 2.5
percent before lyophilisation, and lyophilised material was stored at minus 20
degrees Celsius.

## Viruses and vaccines

CA09 H1N1 (FR-201), PR8 H1N1 (NR-348), Aichi H3N2 (NR-3177) and Perth H3N2
(NR-41803) were obtained from BEI Resources. rgVN04 H5N1 comprises the H5 and N1
genes of A/Vietnam/1203/2004 on a PR8 backbone. Wild-type VN04 H5N1 was obtained
from the Centers for Disease Control. Viruses were expanded in embryonated chicken
eggs and purified by sucrose gradient ultracentrifugation. For challenge studies,
viruses were adapted in mice through three cycles of intranasal instillation and
lung homogenate preparation. Mouse LD50 was determined by a standard protocol.
Wild-type H5N1 work was performed under BSL-3 containment.

Inactivated vaccines were prepared with 0.02 percent formalin over 7 days at 4
degrees Celsius and purified. Vaccine concentration was quantified by BCA protein
assay and by SDS-PAGE on HA content.

Vaccine preparations used across blocks: a monovalent CA09 H1N1 vaccine at 0.5
micrograms HA per animal; a monovalent Aichi H3N2 vaccine at 1 microgram HA per
animal; a bivalent vaccine combining both at those HA contents; and an rgH5N1
vaccine. Ovalbumin and AF647-conjugated ovalbumin were used as protein antigens in
the blocks that name them.

## Routes and doses

Nanoparticles and vaccines were administered intranasally at 20 micrograms of
adjuvant per animal unless a block states another amount. Challenge viruses were
administered intranasally.

Intervention agents, with route and dose:

- Carbenoxolone (CBX), intraperitoneally at 25 mg/kg once daily for 3 consecutive days
  before vaccination.
- Pertussis toxin, intraperitoneally at 20 micrograms per animal immediately after
  vaccination and again at 24 hours.
- CCR2 antagonist INCB3344, intraperitoneally at 10 mg/kg in 5 percent DMSO every
  two days for three doses, beginning one week before vaccination.
- Recombinant GM-CSF, intranasally at 1.5 mg/kg for 4 consecutive days in one block
  and intratracheally in another, as each block states.
- Clodronate liposomes (Clodrosome), intranasally at 30 microlitres.
- Cholera toxin, intranasally, in the block that names it.

Adoptive transfers: bone marrow cells at 5 x 10^6 per animal; CFSE-labelled OT-I
CD8 T cells at 10^6 per animal; sorted lung macrophages, transferred intranasally.

## Stated statistical methods

One-way ANOVA with post hoc Tukey's test for multiple comparisons; two-way ANOVA
with post hoc Tukey's test; Student's t test; and log-rank analysis for
time-to-event data. Summary measures in this file are per-animal values; group
means and dispersion are computed downstream rather than stored here.

---

# Per-block annotation

Each entry gives the measurand, its units and scale, the timepoint, the stated n as
printed in the workbook, the group identities as printed, and the number of
observations present per group. Where the stated n and the observation count differ,
both are given as found.

## Sheet "S01"

### S01-A
Two panels under one label, at columns B to F and H to L.
- **Measurand**: Ifnb1 transcript abundance in total lung cells, by quantitative
  reverse-transcription PCR.
- **Units and scale**: linear, expressed relative to untreated animals.
- **Timepoint**: 16 hours after administration (columns B to F) and 72 hours after
  administration (columns H to L).
- **Conditions**: nanoparticle administered intranasally at 20 micrograms per
  animal, without vaccine.
- **Stated n**: 5.
- **Groups as printed**, each panel: Sham, CMP-204, PSLN-212, PSLN-R848,
  PSLN-212/R848, PSLN-344, PSLN-212(Y), PSLN-344(Y). Groups labelled (Y) are young
  animals; the remainder are aged.
- **Observations per group**: 5 in every group, both panels.

### S01-B
- **Measurand**: proportion of alveolar epithelial cells positive for sulforhodamine
  B, by flow cytometry. Type I cells were gated as PDPN+EpCAM+ and type II cells as
  MHC-II+EpCAM+.
- **Units and scale**: percent, linear.
- **Timepoint**: 16 hours after administration.
- **Conditions**: PSLN-SRB or free SRB administered intranasally at 20 micrograms SRB
  per animal, to aged animals.
- **Stated n**: 5.
- **Groups as printed**: AECII/PSLN-SRB, AECI/PSLN-SRB, AECII/FreeSRB, AECI/FreeSRB.
- **Observations per group**: 5.

### S01-C
- **Measurand**: proportion of alveolar macrophages positive for the lipophilic
  carbocyanine dye DiD, by flow cytometry, gated as DiD+ within
  CD11c+SiglecF+F4/80+.
- **Units and scale**: percent, linear.
- **Timepoint**: 16 hours after administration.
- **Conditions**: DiD-labelled liposomes of the same composition as PSLN-344,
  administered intranasally.
- **Stated n**: 4.
- **Groups as printed**: WT, SPA/D. The second group is Sftpa1-/-Sftpd-/-.
- **Observations per group**: 4.

### S01-D
- **Measurand**: lung monocytes, gated as CD11b+Ly6C+CD11c-Ly6G-, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: days 0, 2, 4, 6 and 8 after immunisation, one row per day.
- **Conditions**: inactivated CA09 H1N1 vaccine at 0.5 micrograms HA, administered
  intranasally with the stated adjuvant at 20 micrograms per animal.
- **Stated n**: 5.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).
- **Observations per group**: 5 at each of 5 timepoints.

### S01-E
- **Measurand**: lung CD11b+ dendritic cells, gated as
  CD11c+MHC-II+CD11b+F4/80-, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: days 0, 2, 4, 6 and 8 after immunisation, one row per day.
- **Conditions**: as S01-D.
- **Stated n**: 5.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y), PSLN-344(Y).
- **Observations per group**: 5 at each of 5 timepoints.

### S01-F
- **Measurand**: lung classical type 1 dendritic cells, gated as
  XCR1+CD172a-CD11c+CD26+, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: 72 hours after immunisation.
- **Conditions**: inactivated bivalent vaccine, CA09 H1N1 at 0.5 micrograms HA and
  Aichi H3N2 at 1 microgram HA, administered intranasally with the stated adjuvant
  at 20 micrograms per animal.
- **Stated n**: 5.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y), PSLN-344(Y).
- **Observations per group**: 5.

### S01-G
- **Measurand**: lung type 2 dendritic cells, gated as XCR1-CD172a+CD11c+CD26+, by
  flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: 72 hours after immunisation.
- **Conditions**: as S01-F.
- **Stated n**: 5.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y), PSLN-344(Y).
- **Observations per group**: 5.

## Sheet "S02"

Blocks S02-A, S02-B and S02-C sit side by side on rows 3 to 7. Blocks S02-D CD40, S02-D CD86 and
S02-E sit side by side on rows 10 to 14.

### S02-A
- **Measurand**: lung migratory CD11b+ dendritic cells, gated as CCR7+ within CD11b+F4/80-CD11c+MHC-II+, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: 72 hours after immunisation.
- **Conditions**: inactivated CA09 H1N1 vaccine at 0.5 micrograms HA, intranasal, with the stated adjuvant at 20 micrograms per animal.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

### S02-B
- **Measurand**: mediastinal lymph node CD11b+CD103- dendritic cells, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: 72 hours after immunisation.
- **Conditions**: as S02-A.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

### S02-C
- **Measurand**: mediastinal lymph node dendritic cells positive for AF647-conjugated ovalbumin, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: 36 hours after immunisation.
- **Conditions**: AF647-conjugated ovalbumin at 30 micrograms per animal, intranasal, with the stated adjuvant. The PTX group received pertussis toxin intraperitoneally at 20 micrograms per animal immediately after immunisation and again at 24 hours.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: PSLN-212, PSLN-344, PSLN-212(Y), PTX, PSLN-344(Y).

### S02-D CD40
- **Measurand**: CD40-positive cells within mediastinal lymph node CD11b+ dendritic cells, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: day 3 after vaccination.
- **Conditions**: inactivated CA09 H1N1 vaccine at 0.5 micrograms HA, intranasal, with the stated adjuvant.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

### S02-D CD86
- **Measurand**: CD86-positive cells within mediastinal lymph node CD11b+ dendritic cells, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: day 3 after vaccination.
- **Conditions**: as S02-D CD40.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

### S02-E
- **Measurand**: proliferation of naive CFSE-labelled OT-I CD8 T cells co-cultured with total CD11b+ dendritic cells sorted from mediastinal lymph nodes, read as stepwise CFSE dilution by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: dendritic cells harvested 72 hours after vaccination; co-culture at a dendritic cell to T cell ratio of 1:10 and read after 3 days.
- **Conditions**: donor animals immunised as in S02-C.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: PSLN-212, PSLN-344, PSLN-212(Y), PTX, PSLN-344(Y).

### S02-F
- **Measurand**: Gm-csf transcript abundance in lung, by quantitative reverse-transcription PCR.
- **Units and scale**: linear, expressed relative to untreated animals.
- **Timepoint**: 16, 36 and 72 hours after immunisation, one row per timepoint.
- **Conditions**: inactivated bivalent vaccine, CA09 H1N1 at 0.5 micrograms HA and Aichi H3N2 at 1 microgram HA, intranasal, with the stated adjuvant.
- **Stated n**: 5. **Observations per group**: 5 at each of 3 timepoints.
- **Groups as printed**: PSLN-344, PSLN-212, Sham.

### S02-G
- **Measurand**: lung Ly6C+CD11c+MHC-II+F4/80-to-intermediate cells, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: day 5 after immunisation.
- **Conditions**: inactivated bivalent vaccine with PSLN-212 or with PBS, intranasal. One day later, recombinant GM-CSF at 1.5 mg/kg or PBS was administered intranasally for 4 consecutive days.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: GM-CSF, PSLN-212, PSLN-212+GM-CSF.

### S02-H
- **Measurand**: CD45.2-positive monocyte-derived dendritic cells, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: day 3 after immunisation.
- **Conditions**: bone marrow cells from CD45.2+ wild-type or Ifnar-knockout donors, with or without removal of CD135+ cDC precursors by sorting, transferred into CD45.1+ wild-type recipients at 5 x 10^6 cells per animal. Recipients were then immunised intranasally with the bivalent vaccine formulated with PSLN-344 at 20 micrograms per animal. One group received Ifnar-knockout bone marrow with the CD135+ precursors removed, and recombinant GM-CSF intratracheally.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: WT w/o cDC, WT w/ cDC, IFN w/o cDC, IFN w/ cDC, GMCSF.

### S02-I
- **Measurand**: lung GZMB-positive CD8 T cells, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: day 5 after vaccination.
- **Conditions**: CCR2 antagonist INCB3344 at 10 mg/kg or vehicle, intraperitoneally, every two days for three doses before vaccination; then the bivalent vaccine formulated with PSLN-344, intranasal.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: PSLN-344(Y), PSLN-344(Y)+INCB3344.

## Sheet "S03"

Blocks S03-A, S03-B, S03-C and S03-D sit side by side on rows 3 to 7. Blocks S03-E, S03-F, S03-G and S03-H
sit side by side on rows 10 to 14. All animals in S03-A to S03-H and S03-K and S03-L received
the inactivated bivalent vaccine, CA09 H1N1 at 0.5 micrograms HA and Aichi H3N2 at
1 microgram HA, intranasally, with the stated adjuvant at 20 micrograms per animal.

### S03-A
- **Measurand**: serum IgG against CA09 H1N1, by ELISA. Plates were coated with CA09 H1N1 vaccine at 1 microgram per millilitre and bound antibody detected with HRP-conjugated goat anti-mouse IgG.
- **Units and scale**: reciprocal endpoint dilution titre, linear.
- **Timepoint**: day 14 after immunisation.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, CMP-204, PSLN-212, PSLN-344, PSLN-212(Y).

### S03-B
- **Measurand**: the quotient of serum IgG2a titre over serum IgG1 titre, both against CA09 H1N1, by ELISA with subclass-specific HRP-conjugated detection antibodies.
- **Units and scale**: dimensionless, linear.
- **Timepoint**: day 14 after immunisation.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: PSLN-212, PSLN-344, PSLN-212(Y).

### S03-C
- **Measurand**: haemagglutination inhibition titre against CA09 H1N1.
- **Units and scale**: reciprocal dilution titre, linear. The lowest dilution tested was 1 in 10.
- **Timepoint**: day 14 after immunisation.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, CMP-204, PSLN-212, PSLN-344, PSLN-212(Y).

### S03-D
- **Measurand**: neutralising antibody titre against CA09 H1N1.
- **Units and scale**: reciprocal dilution titre, linear.
- **Timepoint**: day 14 after immunisation.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, CMP-204, PSLN-212, PSLN-344, PSLN-212(Y).

### S03-E
- **Measurand**: serum IgG against Aichi H3N2, by ELISA. Plates were coated with Aichi H3N2 vaccine at 1 microgram per millilitre.
- **Units and scale**: reciprocal endpoint dilution titre, linear.
- **Timepoint**: day 14 after immunisation.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, CMP-204, PSLN-212, PSLN-344, PSLN-212(Y).

### S03-F
- **Measurand**: the quotient of serum IgG2a titre over serum IgG1 titre, both against Aichi H3N2.
- **Units and scale**: dimensionless, linear.
- **Timepoint**: day 14 after immunisation.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: PSLN-212, PSLN-344, PSLN-212(Y).

### S03-G
- **Measurand**: haemagglutination inhibition titre against Aichi H3N2.
- **Units and scale**: reciprocal dilution titre, linear. The lowest dilution tested was 1 in 10.
- **Timepoint**: day 14 after immunisation.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, CMP-204, PSLN-212, PSLN-344, PSLN-212(Y).

### S03-H
- **Measurand**: neutralising antibody titre against Aichi H3N2.
- **Units and scale**: reciprocal dilution titre, linear.
- **Timepoint**: day 14 after immunisation.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, CMP-204, PSLN-212, PSLN-344, PSLN-212(Y).

### S03-I
- **Measurand**: time to event, one row per animal. Column 1 gives elapsed days; the group column holds 1 or 0.
- **Units and scale**: days, integer.
- **Conditions**: animals vaccinated as in S03-A, then challenged intranasally with 10 x mLD50 CA09 H1N1 at 14 days after immunisation. Observation ran for 14 days after challenge.
- **Stated n**: 7. **Observations per group**: 7.
- **Groups as printed**: Sham, CMP-204, PSLN-212, PSLN-344, PSLN-212(Y).

### S03-J
- **Measurand**: time to event, one row per animal. Column 7 gives elapsed days; the group column holds 1 or 0.
- **Units and scale**: days, integer.
- **Conditions**: a single intranasal dose of reverse-genetics-derived rgH5N1 vaccine formulated with the stated adjuvant, then challenge with wild-type VN04 H5N1 at 2 days after immunisation. Observation ran for 22 days after challenge.
- **Stated n**: 9. **Observations per group**: Sham 10, PSLN-212 10, PSLN-344 10.
- **Groups as printed**: Sham, PSLN-212, PSLN-344.

### S03-K
- **Measurand**: germinal centre B cells in mediastinal lymph node, by flow cytometry, gated as CXCR5+GL7+ within B cells.
- **Units and scale**: percent, linear.
- **Timepoint**: day 7 after immunisation.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

### S03-L
- **Measurand**: Aicda and E47 transcript abundance in mediastinal lymph node B cells, by quantitative reverse-transcription PCR. Columns 12 to 14 are Aicda and columns 15 to 17 are E47.
- **Units and scale**: linear, expressed relative to untreated animals.
- **Timepoint**: day 5 after immunisation.
- **Stated n**: 3. **Observations per group**: 3 per analyte.
- **Groups as printed**, one per row: Sham, PSLN-212, PSLN-344.

## Sheet "S04"

All blocks: inactivated bivalent vaccine, intranasal, with the stated adjuvant at
20 micrograms per animal. Measurements are in mediastinal lymph node except S04-D, which is lung.

### S04-A
- **Measurand**: follicular helper CD4 T cells, gated as CD4+CXCR5+PD1+ and split by ICOS. Columns 2 to 6 are the ICOS-low subset and columns 7 to 11 the ICOS-high subset, as printed in the header row.
- **Units and scale**: percent, linear.
- **Timepoint**: day 7 after immunisation.
- **Stated n**: 5. **Observations per group**: 5 per subset.
- **Groups as printed**, one per row: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

### S04-B Foxp3+ in CXCR5+
- **Measurand**: follicular regulatory CD4 T cells, gated as CD4+CXCR5+ICOShiFoxp3+, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: day 7 after immunisation.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

### S04-B Tfh:Tfr
- **Measurand**: the quotient of the follicular helper T cell percentage over the follicular regulatory T cell percentage.
- **Units and scale**: dimensionless, linear.
- **Timepoint**: day 7 after immunisation.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

### S04-C
- **Measurand**: follicular regulatory CD4 T cells, gated as CD4+CXCR5+ICOShiFoxp3+, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: day 30 after immunisation.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

### S04-D
- **Measurand**: lung regulatory T cells, gated as CD4+Foxp3+, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: day 7 after immunisation.
- **Stated n**: 3. **Observations per group**: 3.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

## Sheet "S05"

### S05-A
- **Measurand**: NP366-374 tetramer-positive cells among gated CD8 T cells in lung, by flow cytometry. Cells were stained with fluorescently conjugated Tetra-NP366-374 for 1 hour on ice before surface staining for CD3 and CD8.
- **Units and scale**: percent, linear.
- **Timepoint**: days 3, 5 and 7 after immunisation, one row per day.
- **Conditions**: animals were immunised intranasally with ovalbumin at 30 micrograms per animal formulated with the stated adjuvant at 20 micrograms per animal. Aged animals were vaccinated intranasally with the bivalent vaccine formulated with sham, PSLN-212 or PSLN-344, with young animals receiving the vaccine formulated with PSLN-212.
- **Stated n**: 3. **Observations per group**: 2 at each of 3 timepoints.
- **Groups as printed**: PSLN-212, PSLN-344, PSLN-212Y.

### S05-B
- **Measurand**: NP366-374 tetramer-positive cells among gated CD8 T cells in mediastinal lymph node, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: days 3, 5 and 7 after immunisation, one row per day.
- **Conditions**: as S05-A.
- **Stated n**: 3. **Observations per group**: 2 at each of 3 timepoints.
- **Groups as printed**: PSLN-212, PSLN-344, PSLN-212Y.

### S05-C
- **Measurand**: proliferating adoptively transferred OT-I CD8 T cells, by CFSE dilution on flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: day 4 after immunisation.
- **Conditions**: 10^6 CFSE-labelled CD45.2+ OT-I cells transferred into CD45.1+ C57BL/6 recipients 24 hours before intranasal vaccination with ovalbumin formulated with PSLN-344. Pertussis toxin at 20 micrograms per animal or PBS was given intraperitoneally immediately after vaccination and again at 24 hours.
- **Stated n**: 3. **Observations per group**: 3.
- **Groups as printed**: Lung, Lung+PTX, MLN, MLN+PTX.

### S05-D
- **Measurand**: Ki-67-positive CD8 T cells in lung, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: day 3 after immunisation.
- **Conditions**: inactivated bivalent vaccine, intranasal, with the stated adjuvant.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

### S05-E
- **Measurand**: GZMB-positive CD8 T cells in lung, by intracellular staining and flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: day 3 after immunisation.
- **Conditions**: as S05-D.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

### S05-F
- **Measurand**: IFN-gamma-positive CD8 T cells among mediastinal lymph node cells, by intracellular staining and flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: cells prepared on day 14 after immunisation.
- **Conditions**: animals immunised with the inactivated bivalent vaccine and the stated adjuvant. Cell suspensions were restimulated in vitro with rgH5N1 vaccine and anti-CD28 before staining.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

### S05-G
- **Measurand**: IFN-gamma-positive CD8 T cells among mediastinal lymph node cells, by intracellular staining and flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: cells prepared on day 60 after immunisation.
- **Conditions**: as S05-F, restimulated in vitro with rgH5N1 vaccine and anti-CD28.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

### S05-H
- **Measurand**: GZMB-positive CD8 T cells among mediastinal lymph node cells, by intracellular staining and flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: cells prepared on day 60 after immunisation, from the same preparation as S05-G.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

### S05-I
- **Measurand**: lung resident memory CD8 T cells, gated as CD3+CD8b-CD69+CD103+ after exclusion of circulating CD8 T cells, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: day 25 after immunisation.
- **Conditions**: animals vaccinated as in S05-A.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

## Sheet "S06"

Every block on this sheet records time to event, one row per animal. The first
column of each block gives elapsed days and the group column holds 1 or 0. Units
are days, integer. Blocks S06-A, S06-B and S06-C sit side by side on rows 3 to 30; blocks
S06-D, S06-E and S06-F on rows 34 to 68; the three blocks at rows 71 to 105 are labelled S06-G,
S06-E and S06-F from left to right. Unless a block states otherwise, animals were aged
BALB/c, vaccinated once intranasally with the stated adjuvant at 20 micrograms per
animal, challenged intranasally, and observed for 14 days after challenge.

### S06-A
- **Vaccine**: Aichi H3N2 at 1 microgram HA. **Challenge**: 5 x mLD50 PR8 H1N1 on day 14 after immunisation.
- **Stated n**: 7. **Observations per group**: 7.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

### S06-B
- **Vaccine**: Aichi H3N2 at 1 microgram HA. **Challenge**: 5 x mLD50 PR8 H1N1 on day 3 after immunisation.
- **Stated n**: 7. **Observations per group**: 7.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

### S06-C
- **Vaccine**: bivalent, CA09 H1N1 at 0.5 micrograms HA and Aichi H3N2 at 1 microgram HA. **Challenge**: 5 x mLD50 rgH5N1 on day 14 after immunisation.
- **Stated n**: 7. **Observations per group**: 7.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

### S06-D
- **Vaccine**: bivalent, as S06-C. **Challenge**: 5 x mLD50 rgH5N1 on day 3 after immunisation.
- **Stated n**: 7. **Observations per group**: 7.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

### S06-E (rows 34 to 68)
- **Vaccine**: Aichi H3N2. **Challenge**: 5 x mLD50 PR8 H1N1 on day 60 after immunisation.
- **Stated n**: 7. **Observations per group**: 7.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y), Untreated. Animals in the Untreated group were 20 months of age and received no vaccine, no adjuvant and no challenge virus.

### S06-F (rows 34 to 68)
- **Vaccine**: bivalent, as S06-C. **Challenge**: 5 x mLD50 rgH5N1 on day 60 after immunisation.
- **Stated n**: 7. **Observations per group**: 7.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y), Untreated. Animals in the Untreated group were 20 months of age and received no vaccine, no adjuvant and no challenge virus.

### S06-G (rows 71 to 105)
- **Vaccine**: CA09 H1N1 at 0.5 micrograms HA. **Challenge**: 5 x mLD50 Perth H3N2 on day 60 after immunisation.
- **Stated n**: 7. **Observations per group**: 7.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y), Untreated. Animals in the Untreated group were 20 months of age and received no vaccine, no adjuvant and no challenge virus.

### S06-E (rows 71 to 105, columns G to L)
- **Conditions**: animals were 10 months of age and were infected with 1 x mLD50 PR8 H1N1 or given saline. Four months later the surviving animals were immunised intranasally with the bivalent vaccine formulated with the stated adjuvant. **Challenge**: 5 x LD50 PR8 H1N1.
- **Stated n**: 7. **Observations per group**: 7.
- **Groups as printed**: Naive+PSLN-212, Imprinting+PSLN-212, Naive+PSLN-344, Imprinting+PSLN-344.

### S06-F (rows 71 to 105, columns M to R)
- **Conditions**: as the preceding block. **Challenge**: 5 x LD50 Perth H3N2 on day 14 after immunisation.
- **Stated n**: 7. **Observations per group**: 7.
- **Groups as printed**: Naive+PSLN-212, Imprinting+PSLN-212, Naive+PSLN-344, Imprinting+PSLN-344.

## Sheet "S07"

### S07-A
- **Measurand**: lung Ly6C+CCR2+ macrophages, by flow cytometry.
- **Units and scale**: cell count, linear. The header row carries the notation (*10^5).
- **Timepoint**: days 0, 2, 5, 10 and 30 after immunisation, one row per day.
- **Conditions**: inactivated bivalent vaccine, intranasal, with the stated adjuvant.
- **Stated n**: 3. **Observations per group**: 3 at each of 5 timepoints.
- **Groups as printed**: PSLN-212, PSLN-344.

### S07-B
- **Measurand**: lung CD11b+Ly6C+ monocytes (columns 2 and 3) and Ly6C+ macrophages (columns 5 and 6), by flow cytometry, as printed in the header row.
- **Units and scale**: percent, linear.
- **Conditions**: CCR2 antagonist INCB3344 at 10 mg/kg or vehicle, intraperitoneally, every two days for three doses before vaccination; then the bivalent vaccine formulated with PSLN-344, intranasal.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: PSLN-344, PSLN-344+INCB3344, for each of the two cell populations.

### S07-C
- **Measurand**: lung regulatory T cells, gated as CD4+Foxp3+, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: day 4 after macrophage transfer.
- **Conditions**: donor aged animals received the bivalent vaccine formulated with PSLN-344 intranasally. Recipient aged animals were immunised intranasally with the bivalent vaccine alone, and two days later received clodronate liposomes intranasally at 30 microlitres. On day 4 after immunisation, Ly6C+CD206- and Ly6C-CD206+ lung macrophages were sorted from donors by FACS and transferred intranasally into recipients.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Ly6C-CD206+ MPhi, Ly6C-CD206+ MPhi.

## Sheet "S08"

### S08-A
- **Measurand**: Ifnb1 transcript abundance in lung, by quantitative reverse-transcription PCR.
- **Units and scale**: linear, expressed relative to untreated animals.
- **Timepoint**: 16 hours after administration.
- **Conditions**: nanoparticle administered intranasally, without vaccine, at 1, 5, 10, 20 and 40 micrograms per animal, one row per dose. Column 1 gives the dose.
- **Stated n**: 3. **Observations per group**: 3 at each of 5 doses.
- **Groups as printed**: CMP-204, PSLN-212, PSLN-344, PSLN-344/R848.

### S08-B
- **Measurand**: encapsulation efficiency of the nanoparticle preparation, determined by absorbance of CDN-1807 at 260 nm.
- **Units and scale**: percent, linear.
- **Stated n**: 3. **Observations per group**: 3.
- **Groups as printed**: CMP-204, PSLN-212, PSLN-R848, PSLN-212/R848, PSLN-344.

### S08-C
- **Measurand**: alveolar epithelial cells positive for sulforhodamine B, by flow cytometry. Type I cells were gated as PDPN+MHC-II- and type II cells as MHC-II+PDPN-, both within EpCAM+ airway epithelial cells after exclusion of MHC-II-PDPN- double negatives.
- **Units and scale**: percent, linear.
- **Timepoint**: 16 hours after administration.
- **Conditions**: PSLN-SRB or PSLN-344-SRB administered intranasally at 20 micrograms per animal to aged animals.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: AECII-PSLN-SRB, AECII-PSLN-344-SRB, AECI-PSLN-SRB, AECI-PSLN-344-SRB.

### S08-D
- **Measurand**: body weight.
- **Units and scale**: percent of each animal's own day 0 weight, linear. Every animal reads 100 at day 0.
- **Timepoint**: days 0, 2, 4, 6, 8 and 10 after immunisation, one row per day.
- **Conditions**: inactivated CA09 H1N1 vaccine at 0.5 micrograms HA, intranasal, with 20 micrograms of the stated adjuvant.
- **Stated n**: 5. **Observations per group**: 5, except the PSLN-212/R848 group, which has 4 at day 10.
- **Groups as printed**: PSLN-212(Y), CMP-204, PSLN-212, PSLN-344, PSLN-212/R848, Vaccine.

### S08, rows 89 to 101
A region of numeric data carrying no block label.
- **Measurand**: not stated.
- **Units and scale**: not stated. Column A holds 14 in every row. Columns C and D hold 0.
- **Timepoint**: not stated.
- **Conditions**: not stated.
- **Stated n**: none given.
- **Groups as printed**: none. No header row and no group names appear.
- **Observations present**: 6 values in column C, rows 89 to 94; 7 values in column D, rows 95 to 101.

## Sheet "S09"

### S09-A, columns A to U
- **Measurand**: transcript abundance in lung of Ifnb1, Il6, Ccl2, Ccl3, Ccl5, Tnf and Il10, by quantitative reverse-transcription PCR, one analyte per row as printed in column 1.
- **Units and scale**: log10, expressed relative to untreated animals. The scale is stated in the block label.
- **Timepoint**: as printed in the block label, 16 hours after administration.
- **Conditions**: nanoparticle administered intranasally at 20 micrograms per animal, without vaccine.
- **Stated n**: 3. **Observations per group**: 3 per analyte.
- **Groups as printed**: PBS, CMP-204, PSLN-212, PSLN-R848, PSLN-212/R848, PSLN-344, PSLN-212(y).

### S09-A, columns X to AS
- **Measurand**: as the preceding block, the same seven analytes in the same row order.
- **Units and scale**: log10, expressed relative to untreated animals. The scale is stated in the block label.
- **Timepoint**: as printed in the block label, 16 hours after administration.
- **Conditions**: as the preceding block.
- **Stated n**: 3. **Observations per group**: 3 per analyte.
- **Groups as printed**: PBS, CMP-204, PSLN-212, PSLN-R848, PSLN-212/R848, PSLN-344, PSLN-212(y).

### S09-B
- **Measurand**: time to event, one row per animal. Column 1 gives elapsed days; the group column holds 1 or 0.
- **Units and scale**: days, integer.
- **Conditions**: young BALB/c immunised intranasally with inactivated Aichi H3N2 vaccine at 1 microgram HA and the stated adjuvant, then challenged with 5 x mLD50 PR8 H1N1 on day 21 after immunisation. Observation ran for 14 days after challenge.
- **Stated n**: 8. **Observations per group**: 8, except the Sham group, which has 7.
- **Groups as printed**: Sham, PSLN-344Y, PSLN-212Y.

### S09-C
- **Measurand**: body weight.
- **Units and scale**: percent of each animal's own day 0 weight, linear.
- **Timepoint**: days 0, 2, 4, 6, 8, 10, 12 and 14 after challenge, one row per day.
- **Conditions**: the animals of S09-B.
- **Stated n**: 8. **Observations per group**: 8 at day 0, declining thereafter in the Sham group.
- **Groups as printed**: PSLN-212Y, Sham, PSLN-344Y.

### S09-D
- **Measurand**: time to event, one row per animal.
- **Units and scale**: days, integer.
- **Conditions**: young BALB/c immunised intranasally with inactivated CA09 H1N1 vaccine at 0.5 micrograms HA and the stated adjuvant, then challenged with 5 x mLD50 Perth H3N2 on day 21 after immunisation. Observation ran for 14 days after challenge.
- **Stated n**: 8. **Observations per group**: 8.
- **Groups as printed**: Sham, PSLN-344Y, PSLN-212Y.

### S09-E
- **Measurand**: body weight, percent of each animal's own day 0 weight.
- **Timepoint**: days 0 to 14 after challenge in 2-day steps.
- **Conditions**: the animals of S09-D.
- **Stated n**: 8. **Observations per group**: 8 at day 0, declining thereafter in the Sham group.
- **Groups as printed**: PSLN-212Y, Sham, PSLN-344Y.

### S09-F
- **Measurand**: time to event, one row per animal.
- **Units and scale**: days, integer.
- **Conditions**: young BALB/c immunised intranasally with the inactivated bivalent vaccine and the stated adjuvant, then challenged with 5 x mLD50 VN04 rgH5N1 on day 180 after immunisation. Observation ran for 14 days after challenge.
- **Stated n**: 8. **Observations per group**: 8.
- **Groups as printed**: Sham, PSLN-344Y, PSLN-212Y.

### S09-G
- **Measurand**: body weight, percent of each animal's own day 0 weight.
- **Timepoint**: days 0 to 14 after challenge in 2-day steps.
- **Conditions**: the animals of S09-F.
- **Stated n**: 8. **Observations per group**: 8 at day 0, declining thereafter in the Sham group.
- **Groups as printed**: PSLN-212Y, Sham, PSLN-344Y.

## Sheet "S10"

### S10-A
- **Measurand**: transcript abundance of Ifnb1, Tnf and Isg15 in the central nervous system, by quantitative reverse-transcription PCR. Columns 1 to 4 are Ifnb1, 6 to 9 are Tnf and 11 to 14 are Isg15, as printed in the header row.
- **Units and scale**: linear, expressed relative to untreated animals.
- **Timepoint**: 36 hours after immunisation.
- **Conditions**: aged animals received the inactivated bivalent vaccine intranasally, with PSLN-344, with cholera toxin, or without either.
- **Stated n**: 5. **Observations per group**: 5 per analyte.
- **Groups as printed**, for each analyte: PBS, Sham, PSLN-344, CT.
- **Summary measure**: this block is reported as mean with standard deviation.

## Sheet "S11"

All blocks on this sheet: aged animals received inactivated CA09 H1N1 vaccine at
0.5 micrograms HA intranasally with the stated adjuvant, except where noted. Lungs
for S11-A were harvested without intratracheal instillation; lungs for the
remaining blocks were harvested with intratracheal instillation.

### S11-A
- **Measurand**: alveolar macrophages in lung, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: days 0, 2, 4, 6 and 8 after immunisation, one row per day.
- **Stated n**: 5. **Observations per group**: 5 at each of 5 timepoints.
- **Groups as printed**: Vaccine, PSLN-212, PSLN-344, PSLN-212(Y).

### S11-B
- **Measurand**: neutrophils in lung, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: days 0, 2, 4, 6 and 8 after immunisation, one row per day.
- **Stated n**: 5. **Observations per group**: 5 at each of 5 timepoints.
- **Groups as printed**: Vaccine, PSLN-212, PSLN-344, PSLN-212(Y).

### S11-C
- **Measurand**: recruited monocytes in lung, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: day 3 after vaccination.
- **Conditions**: carbenoxolone (CBX) at 25 mg/kg or saline, intraperitoneally, once daily for 3 consecutive days, after which the CA09 H1N1 vaccine formulated with PSLN-344 was administered intranasally.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: CBX+, CBX-.

### S11-D
- **Measurand**: NK cells in lung, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: days 0, 2, 4, 6 and 8 after immunisation, one row per day.
- **Stated n**: 5. **Observations per group**: 5 at each of 5 timepoints.
- **Groups as printed**: Vaccine, PSLN-212, PSLN-344, PSLN-212(Y).

### S11-E
- **Measurand**: CD206-positive macrophages in lung, by flow cytometry.
- **Units and scale**: percent, linear.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

## Sheet "S12"

### S12-A
- **Measurand**: infiltrating CD45.2-positive CD11b+Ly6C+ monocytes, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: day 3 after immunisation.
- **Conditions**: bone marrow cells from CD45.2+ wild-type or Ifnar-knockout donors, with CD135+ pre-cDCs removed by sorting, transferred into CD45.1+ wild-type recipients at 5 x 10^6 cells per animal. Three days later the recipients were immunised with the bivalent vaccine formulated with PSLN-344. These animals were young.
- **Stated n**: 3. **Observations per group**: 3.
- **Groups as printed**: WT to WT, IFNAR-/- to WT.

## Sheet "S13"

Blocks S13-A, S13-B, S13-C, S13-D and S13-E sit side by side on rows 3 to 30. Blocks S13-H,
S13-I and S13-J sit side by side on rows 53 to 57. Animals in S13-A to S13-D and S13-H to
S13-J received the inactivated bivalent vaccine intranasally with the stated adjuvant.

### S13-A
- **Measurand**: serum IgG2a against CA09 H1N1, by ELISA with a subclass-specific HRP-conjugated detection antibody.
- **Units and scale**: reciprocal endpoint dilution titre, linear.
- **Timepoint**: day 14 after immunisation.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: PSLN-212, PSLN-344, PSLN-212(Y).

### S13-B
- **Measurand**: serum IgG1 against CA09 H1N1, by ELISA with a subclass-specific HRP-conjugated detection antibody.
- **Units and scale**: reciprocal endpoint dilution titre, linear.
- **Timepoint**: day 14 after immunisation.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: PSLN-212, PSLN-344, PSLN-212(Y).

### S13-C
- **Measurand**: serum IgG2a against Aichi H3N2, by ELISA with a subclass-specific HRP-conjugated detection antibody.
- **Units and scale**: reciprocal endpoint dilution titre, linear.
- **Timepoint**: day 14 after immunisation.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: PSLN-212, PSLN-344, PSLN-212(Y).

### S13-D
- **Measurand**: serum IgG1 against Aichi H3N2, by ELISA with a subclass-specific HRP-conjugated detection antibody.
- **Units and scale**: reciprocal endpoint dilution titre, linear.
- **Timepoint**: day 14 after immunisation.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: PSLN-212, PSLN-344, PSLN-212(Y).

### S13-E
- **Measurand**: time to event, one row per animal. Column 18 gives elapsed days; the group column holds 1 or 0.
- **Units and scale**: days, integer.
- **Conditions**: young BALB/c vaccinated as in S03-I, then challenged with 10 x mLD50 CA09 H1N1 at 14 days after immunisation. Observation ran for 14 days after challenge.
- **Stated n**: 5. **Observations per group**: 7.
- **Groups as printed**: Naive, Sham, CMP-204(Y), PSLN-344(Y).

### S13-F
- **Measurand**: body weight.
- **Units and scale**: percent of each animal's own day 0 weight, linear.
- **Timepoint**: days 0, 2, 4, 6, 8, 10, 12 and 14 after challenge, one row per day.
- **Conditions**: the animals of S03-I.
- **Stated n**: 7. **Observations per group**: 7 at day 0, declining thereafter in the Sham, PSLN-212 and Naive groups.
- **Groups as printed**: PSLN-212(Y), Sham, PSLN-212, PSLN-344, Naive.

### S13-G
- **Measurand**: body weight.
- **Units and scale**: percent of each animal's own day 0 weight, linear.
- **Timepoint**: days 0, 2, 4, 6, 8, 10, 12 and 14 after challenge, one row per day.
- **Conditions**: the animals of S03-J.
- **Stated n**: 10. **Observations per group**: 10.
- **Groups as printed**: PSLN-344, Sham, Naive.

### S13-H
- **Measurand**: IgG in mediastinal lymph node B220-positive cells, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: not stated. The animals were immunised as in S13-A.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

### S13-I
- **Measurand**: serum IgG against CA09 H1N1, by ELISA.
- **Units and scale**: reciprocal endpoint dilution titre, linear.
- **Timepoint**: day 28, following a boost on day 14.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, CMP-204, PSLN-212, PSLN-344, PSLN-212(Y).

### S13-J
- **Measurand**: serum IgG against Aichi H3N2, by ELISA.
- **Units and scale**: reciprocal endpoint dilution titre, linear.
- **Timepoint**: day 28, following a boost on day 14.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, CMP-204, PSLN-212, PSLN-344, PSLN-212(Y).

## Sheet "S14"

### S14-A H1N1
- **Measurand**: IFN-gamma-positive CD8 T cells among mediastinal lymph node cells, by intracellular staining and flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: not stated. The animals were immunised as in S05-F.
- **Conditions**: cell suspensions were restimulated in vitro with CA09 H1N1 vaccine and anti-CD28 before staining.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

### S14-A H3N2
- **Measurand**: IFN-gamma-positive CD8 T cells among mediastinal lymph node cells, by intracellular staining and flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: not stated. The animals were immunised as in S05-F.
- **Conditions**: as the preceding block, restimulated in vitro with Aichi H3N2 vaccine and anti-CD28.
- **Stated n**: 5. **Observations per group**: 5.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

## Sheet "S15"

Blocks on this sheet hold either body weight or time to event. Body weight is
given as percent of each animal's own day 0 weight on a linear scale, with every
animal reading 100 at day 0, recorded on days 0, 2, 4, 6, 8, 10, 12 and 14 after
challenge. Time to event is given as elapsed days, integer, one row per animal,
with the group column holding 1 or 0. Animals are aged BALB/c vaccinated once
intranasally with the stated adjuvant at 20 micrograms per animal and challenged
intranasally, except where a block states otherwise. Blocks S15-H and S15-I sit side
by side on rows 72 onward; S15-L and S15-M, and S15-N and S15-O, likewise.

### S15-A
- **Measurand**: body weight. **Conditions**: Aichi H3N2 vaccine at 1 microgram HA, challenged with 5 x mLD50 PR8 H1N1 on day 14 after immunisation.
- **Stated n**: 7. **Observations per group**: 7 at day 0, declining thereafter in the Sham and PSLN-212 groups.
- **Groups as printed**: PSLN-212(Y), Sham, PSLN-212, PSLN-344.

### S15-B
- **Measurand**: body weight. **Conditions**: Aichi H3N2 vaccine at 1 microgram HA, challenged with 5 x mLD50 PR8 H1N1 on day 3 after immunisation.
- **Stated n**: 7. **Observations per group**: 7 at day 0, declining thereafter.
- **Groups as printed**: PSLN-212(Y), Sham, PSLN-212, PSLN-344.

### S15-C
- **Measurand**: body weight. **Conditions**: bivalent vaccine, challenged with 5 x mLD50 rgH5N1 on day 14 after immunisation.
- **Stated n**: 7. **Observations per group**: 7 at day 0, declining thereafter.
- **Groups as printed**: PSLN-212(Y), Sham, PSLN-212, PSLN-344.

### S15-D
- **Measurand**: body weight. **Conditions**: bivalent vaccine, challenged with 5 x mLD50 rgH5N1 on day 3 after immunisation.
- **Stated n**: 7. **Observations per group**: 7 at day 0, declining thereafter.
- **Groups as printed**: PSLN-212(Y), Sham, PSLN-212, PSLN-344.

### S15-E
- **Measurand**: body weight. **Conditions**: Aichi H3N2 vaccine, challenged with 5 x mLD50 PR8 H1N1 on day 60 after immunisation.
- **Stated n**: 7. **Observations per group**: 7 at day 0, declining thereafter.
- **Groups as printed**: PSLN-212(Y), Sham, PSLN-212, PSLN-344, Untreated. Animals in the Untreated group were 20 months of age and received no vaccine, no adjuvant and no challenge virus.

### S15-F
- **Measurand**: body weight. **Conditions**: bivalent vaccine, challenged with 5 x mLD50 rgH5N1 on day 60 after immunisation.
- **Stated n**: 7. **Observations per group**: 7 at day 0, declining thereafter.
- **Groups as printed**: PSLN-212(Y), Sham, PSLN-212, PSLN-344, Untreated. Animals in the Untreated group were 20 months of age and received no vaccine, no adjuvant and no challenge virus.

### S15-G
- **Measurand**: body weight. **Conditions**: CA09 H1N1 vaccine at 0.5 micrograms HA, challenged with 5 x mLD50 Perth H3N2 on day 60 after immunisation.
- **Stated n**: 7. **Observations per group**: 7 at day 0, declining thereafter.
- **Groups as printed**: PSLN-212(Y), Sham, PSLN-212, PSLN-344, Untreated. Animals in the Untreated group were 20 months of age and received no vaccine, no adjuvant and no challenge virus.

### S15-H
- **Measurand**: time to event, one row per animal.
- **Conditions**: aged animals received the bivalent vaccine alone, PSLN-344 alone, or the bivalent vaccine combined with PSLN-344, intranasally, 3 days before challenge with 5 x mLD50 VN04 rgH5N1.
- **Stated n**: 7. **Observations per group**: 7.
- **Groups as printed**: 3d Vaccine, 3d PSLN-344, 3d Vaccine+PSLN-344.

### S15-I
- **Measurand**: body weight. **Conditions**: the animals of S15-H.
- **Stated n**: 7. **Observations per group**: 7 at day 0, declining thereafter in the 3d Vaccine and 3d PSLN-344 groups.
- **Groups as printed**: 3d Vaccine, 3d PSLN-344, 3d Vaccine+PSLN-344.

### S15-J
- **Measurand**: body weight.
- **Conditions**: animals were 10 months of age and were infected with 1 x mLD50 PR8 H1N1 or given saline. Four months later the surviving animals were immunised intranasally with the bivalent vaccine formulated with the stated adjuvant, then challenged with 5 x LD50 PR8 H1N1.
- **Stated n**: 7. **Observations per group**: 7 at day 0, declining thereafter.
- **Groups as printed**: Naive+PSLN-212, Imprinting+PSLN-212, Naive+PSLN-344, Imprinting+PSLN-344.

### S15-K
- **Measurand**: body weight.
- **Conditions**: as S15-J, challenged with 5 x LD50 Perth H3N2 on day 14 after immunisation.
- **Stated n**: 7. **Observations per group**: 7 at day 0, declining thereafter.
- **Groups as printed**: Naive+PSLN-212, Imprinting+PSLN-212, Naive+PSLN-344, Imprinting+PSLN-344.

### S15-L
- **Measurand**: time to event, one row per animal.
- **Conditions**: aged C57BL/6 animals, 20 months of age, immunised intranasally with the bivalent vaccine formulated with the stated adjuvant. Young C57BL/6 animals received the vaccine formulated with PSLN-212.
- **Stated n**: 7. **Observations per group**: 7.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

### S15-M
- **Measurand**: body weight. **Conditions**: the animals of S15-L, aged and young C57BL/6.
- **Stated n**: 7. **Observations per group**: 7 at day 0, declining thereafter in the Sham group.
- **Groups as printed**: PSLN-212(Y), Sham, PSLN-212, PSLN-344.

### S15-N
- **Measurand**: time to event, one row per animal.
- **Conditions**: aged Swiss Webster animals, 20 months of age, immunised intranasally with the bivalent vaccine formulated with the stated adjuvant. Young Swiss Webster animals received the vaccine formulated with PSLN-212.
- **Stated n**: 7. **Observations per group**: 7.
- **Groups as printed**: Sham, PSLN-212, PSLN-344, PSLN-212(Y).

### S15-O
- **Measurand**: body weight. **Conditions**: the animals of S15-N, aged and young Swiss Webster.
- **Stated n**: 7. **Observations per group**: 7 at day 0, declining thereafter in the Sham group.
- **Groups as printed**: PSLN-212(Y), Sham, PSLN-212, PSLN-344.
