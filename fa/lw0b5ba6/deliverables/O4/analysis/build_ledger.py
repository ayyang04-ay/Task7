import pandas as pd, numpy as np, json
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
A = '/tmp/outputs/analysis/'; OUT = '/tmp/outputs/PSLN-344_evidence_ledger.xlsx'
K = json.load(open(A + 'keynums.json'))
claims = pd.read_csv(A + 'claims.csv')
S = pd.read_csv(A + 'block_group_summary.csv')
# key values for each claim (auto-generated where possible)
def kv_for_block(bk):
    out = []
    for key in K:
        if key.split('_')[0] == bk or key == bk:
            g = K[key].get('groups', {})
            parts = [f"{gg}: n={d['n']}, mean={d['mean']:.4g}, SD={d['sd']:.3g}" + (f", GM={d['gm']:.4g}" if d.get('gm') else '') for gg, d in g.items() if d.get('sd') is not None]
            mn = K[key].get('mn')
            if mn: parts.append(f"PSLN-344 vs PSLN-212: effect={mn['effect']:.4g} (95% CI {mn['lo']:.3g} to {mn['hi']:.3g}), p={mn['p']:.2g}")
            out.append(f"[{key}] " + '; '.join(parts))
    return ' || '.join(out)
vals = []
for _, r in claims.iterrows():
    b = str(r.blocks).split(';')[0].strip().split(',')[0].strip()
    v = kv_for_block(b) if b.startswith('S') and '-' in b else ''
    vals.append(v[:32000])
claims['key_values_auto'] = vals
README = pd.DataFrame({'item': [
    'Purpose', 'How to trace a number', 'Cell references', 'Statistics', 'Integrity', 'Group naming', 'Reproduce'],
    'description': [
    'Evidence ledger supporting PSLN-344_Portfolio_Proposal.pdf (data cut 1 Nov 2026). Every number in the proposal maps to a claim ID (sheet Claims) and from there to workbook cells and analysis outputs.',
    'Find the claim ID quoted in the proposal (e.g. E12c) in sheet Claims -> read blocks/cells -> confirm per-animal values in sheet Tidy_continuous / Tidy_survival / Tidy_bodyweight (column "cell") -> confirm statistics in Group_summary / Contrasts / Survival_* sheets.',
    'Cells are given as Sheet!A1 addresses of psln_program_dataset.xlsx. Group summary rows give the first:last cell of each group.',
    'Titres, ratios and qPCR fold-changes analysed on log2 scale (geometric means); percentages on raw scale. Welch t-tests with 95% CI, Hedges g, Tukey HSD (stated method), BH q-values. Survival: log-rank, Fisher exact, exact stratified test, Mantel-Haenszel risk difference. HAI 0 (<1:10) set to 5.',
    'Integrity_register lists 5 critical, 8 major, 10 minor findings and 1 soft signal; Integrity_checks and Dup_* sheets reproduce the evidence.',
    'Printed names normalised: "PSLN-212Y"/"PSLN-212(y)" -> "PSLN-212(Y)"; "Naïve" -> "Naive". (Y) = young (7-8 weeks); others aged (>=20 months) unless the block states otherwise. S06 rows 71-105 blocks are cited as S06-E\' and S06-F\' because their printed IDs duplicate S06-E/S06-F.',
    'Scripts in analysis/ (see proposal Appendix B for run order).']})
sheets = [('README', README), ('Claims', claims),
          ('Group_summary', S), ('Contrasts', pd.read_csv(A + 'block_contrasts.csv')), ('Tukey_HSD', pd.read_csv(A + 'block_tukey_hsd.csv')),
          ('Mechanism_contrasts', pd.read_csv(A + 'mechanism_contrasts.csv')),
          ('Survival_counts', pd.read_csv(A + 'survival_counts.csv')), ('Survival_tests', pd.read_csv(A + 'survival_tests.csv')),
          ('Survival_pooled', pd.read_csv(A + 'survival_pooled_sensitivity.csv')), ('Survival_strata_flags', pd.read_csv(A + 'survival_strata_flags.csv')),
          ('BW_vs_survival', pd.read_csv(A + 'bw_vs_survival_reconciliation.csv')),
          ('Biomarkers', pd.read_csv(A + 'biomarker_candidates.csv')),
          ('Safety_S08D_weights', pd.read_csv(A + 'safety_S08D_bodyweight.csv')), ('Safety_S10A_CNS', pd.read_csv(A + 'safety_S10A_CNS.csv')),
          ('Dose_response_S08A', pd.read_csv(A + 'dose_response_S08A_emax.csv')),
          ('Design_power_cont', pd.read_csv(A + 'design_power_continuous.csv')), ('Design_power_surv', pd.read_csv(A + 'design_power_survival.csv')),
          ('Integrity_register', pd.read_csv(A + 'integrity_register.csv')), ('Integrity_checks', pd.read_csv(A + 'integrity_checks.csv')),
          ('Dup_trajectories', pd.read_csv(A + 'dup_animal_trajectories_distinct.csv')), ('Dup_chance_benchmark', pd.read_csv(A + 'dup_chance_benchmark.csv')),
          ('Dup_exact_highprec_bw', pd.read_csv(A + 'dup_exact_highprecision_bw.csv')), ('Dup_S11A_vs_S11B', pd.read_csv(A + 'dup_S11A_vs_S11B_positionwise.csv')),
          ('IgG2a_IgG1_label_check', pd.read_csv(A + 'check_IgG2a_IgG1_labels.csv')),
          ('Tidy_continuous', pd.read_csv(A + 'tidy_continuous.csv')), ('Tidy_survival', pd.read_csv(A + 'tidy_survival.csv')), ('Tidy_bodyweight', pd.read_csv(A + 'tidy_bodyweight.csv'))]
with pd.ExcelWriter(OUT, engine='openpyxl') as xw:
    for name, df in sheets:
        df.to_excel(xw, sheet_name=name[:31], index=False)
wb = load_workbook(OUT)
for ws in wb.worksheets:
    for c in ws[1]:
        c.font = Font(bold=True); c.fill = PatternFill('solid', fgColor='DCE6F2'); c.alignment = Alignment(wrap_text=True, vertical='top')
    ws.freeze_panes = 'A2'
    for col in ws.columns:
        L = max(len(str(c.value)) if c.value is not None else 0 for c in list(col)[:200])
        ws.column_dimensions[col[0].column_letter].width = min(max(10, L * 0.9), 70)
    if ws.title in ('README', 'Claims', 'Integrity_register'):
        for row in ws.iter_rows(min_row=2):
            for c in row: c.alignment = Alignment(wrap_text=True, vertical='top')
wb.save(OUT)
print('ledger written with', len(sheets), 'sheets;', len(claims), 'claims')
