FORMAT SAMPLE ONLY. Front matter plus the seven Fig.1 blocks. Ships as PDF; this
working copy is markdown purely so it is diffable. The remaining 94 blocks follow
the same shape on approval.

# Study annotation

## Animals

Female BALB/c mice. Young animals were 7 to 8 weeks of age at the start of each
experiment. Aged animals were 20 months of age or older, except where a block
states otherwise. C57BL/6 mice at 15 or 20 months, Swiss Webster mice, 7 to
8-week-old Sftpa1-/-Sftpd-/- mice, OT-I mice and Ifnar-deficient mice were used in
the blocks that name them. Animals were housed in a pathogen-free facility. The
protocol was reviewed and approved by the institutional animal care and use
committee under 2008N000173.

## Materials

Two nanoparticle preparations appear throughout. Both are pulmonary-surfactant
biomimetic liposomes containing DPPC, DPPG, DPPE-PEG2000 and cholesterol at a
molar ratio of 10:1:1:1, prepared by reverse-phase evaporation or thin-film
rehydration, and both encapsulate the cyclic dinucleotide STING agonist ADU-S100.
They differ in one respect: AMnESTI incorporates Mn2+ by coordination
polymerization and nanoSTING does not. Three further preparations appear in
individual blocks: PS-GAMP, which encapsulates cGAMP in place of ADU-S100;
nanoR848, which encapsulates the TLR7/8 agonist R848; and nanoSTING/R848, which
encapsulates both ADU-S100 and R848.

Where a block names "sham", the animals received empty liposome vehicle in saline
alongside the vaccine. Where a block names "PBS" or "vehicle", the animals received
buffer alone.

Encapsulation efficiency of ADU-S100 was determined by absorbance at 260 nm.
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

- Carbenoxolone, intraperitoneally at 25 mg/kg once daily for 3 consecutive days
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

## Sequencing

Single-cell RNA sequencing was performed on sorted CD45+ cells. Lung CD45+ cells
were taken on day 5 after immunisation. Mediastinal lymph node CD45+ cells were
taken on day 7 after immunisation. Sequencing was run in duplicate per group, with
samples pooled from two animals per group in each run. Bulk mRNA sequencing was
performed on sorted EpCAM+ cells 18 hours after administration.

## Stated statistical methods

One-way ANOVA with post hoc Tukey's test for multiple comparisons; two-way ANOVA
with post hoc Tukey's test; Student's t test; and log-rank analysis for
time-to-event data. Summary measures are reported as mean with standard error of
the mean, except where a block states standard deviation. Results are described as
representative of at least two independent experiments.

---

# Per-block annotation

Each entry gives the measurand, its units and scale, the timepoint, the stated n as
printed in the workbook, the group identities as printed, and the number of
observations present per group. Where the stated n and the observation count differ,
both are given as found.

## Sheet "Fig.1"

### Fig.1A
Two panels under one label, at columns B to F and H to L.
- **Measurand**: Ifnb1 transcript abundance in total lung cells, by quantitative
  reverse-transcription PCR.
- **Units and scale**: linear, expressed relative to untreated animals.
- **Timepoint**: 16 hours after administration (columns B to F) and 72 hours after
  administration (columns H to L).
- **Conditions**: nanoparticle administered intranasally at 20 micrograms per
  animal, without vaccine.
- **Stated n**: 5.
- **Groups as printed**, each panel: Sham, PSGAMP, NanoSTING, NanoR848,
  NanoSTING/R848, AMnESTI, NanoSTING(Y), AMnESTI(Y). Groups labelled (Y) are young
  animals; the remainder are aged.
- **Observations per group**: 5 in every group, both panels.

### Fig.1D
- **Measurand**: proportion of alveolar epithelial cells positive for sulforhodamine
  B, by flow cytometry. Type I cells were gated as PDPN+EpCAM+ and type II cells as
  MHC-II+EpCAM+.
- **Units and scale**: percent, linear.
- **Timepoint**: 16 hours after administration.
- **Conditions**: nanoSRB or free SRB administered intranasally at 20 micrograms SRB
  per animal, to aged animals.
- **Stated n**: 5.
- **Groups as printed**: AECII/NanoSRB, AECI/NanoSRB, AECII/FreeSRB, AECI/FreeSRB.
- **Observations per group**: 5.

### Fig.1E
- **Measurand**: proportion of alveolar macrophages positive for the lipophilic
  carbocyanine dye DiD, by flow cytometry, gated as DiD+ within
  CD11c+SiglecF+F4/80+.
- **Units and scale**: percent, linear.
- **Timepoint**: 16 hours after administration.
- **Conditions**: DiD-labelled liposomes of the same composition as AMnESTI,
  administered intranasally.
- **Stated n**: 4.
- **Groups as printed**: WT, SPA/D. The second group is Sftpa1-/-Sftpd-/-.
- **Observations per group**: 4.

### Fig.1I
- **Measurand**: lung monocytes, gated as CD11b+Ly6C+CD11c-Ly6G-, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: days 0, 2, 4, 6 and 8 after immunisation, one row per day.
- **Conditions**: inactivated CA09 H1N1 vaccine at 0.5 micrograms HA, administered
  intranasally with the stated adjuvant at 20 micrograms per animal.
- **Stated n**: 5.
- **Groups as printed**: Sham, NanoSTING, AMnESTI, NanoSTING(Y).
- **Observations per group**: 5 at each of 5 timepoints.

### Fig.1J
- **Measurand**: lung CD11b+ dendritic cells, gated as
  CD11c+MHC-II+CD11b+F4/80-, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: days 0, 2, 4, 6 and 8 after immunisation, one row per day.
- **Conditions**: as Fig.1I.
- **Stated n**: 5.
- **Groups as printed**: Sham, NanoSTING, AMnESTI, NanoSTING(Y), AMnESTI(Y).
- **Observations per group**: 5 at each of 5 timepoints.

### Fig.1K
- **Measurand**: lung classical type 1 dendritic cells, gated as
  XCR+CD172-CD11c+CD26+, by flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: 72 hours after immunisation.
- **Conditions**: inactivated bivalent vaccine, CA09 H1N1 at 0.5 micrograms HA and
  Aichi H3N2 at 1 microgram HA, administered intranasally with the stated adjuvant
  at 20 micrograms per animal.
- **Stated n**: 5.
- **Groups as printed**: Sham, NanoSTING, AMnESTI, NanoSTING(Y), AMnESTI(Y).
- **Observations per group**: 5.

### Fig.1L
- **Measurand**: lung type 2 dendritic cells, gated as XCR-CD172+CD11c+CD26+, by
  flow cytometry.
- **Units and scale**: percent, linear.
- **Timepoint**: 72 hours after immunisation.
- **Conditions**: as Fig.1K.
- **Stated n**: 5.
- **Groups as printed**: Sham, NanoSTING, AMnESTI, NanoSTING(Y), AMnESTI(Y).
- **Observations per group**: 5.
