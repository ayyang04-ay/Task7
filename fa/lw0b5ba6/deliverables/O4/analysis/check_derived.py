import pandas as pd, numpy as np, itertools
c = pd.read_csv('tidy_continuous.csv')
def v(b, g): return c[(c.block == b) & (c.group == g)].value.values
rows = []
groups = ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)']
for ratio_blk, num_blk, den_blk, ag in [('S03-B', 'S13-A', 'S13-B', 'CA09 H1N1'), ('S03-F', 'S13-C', 'S13-D', 'Aichi H3N2')]:
    derived = {g: v(num_blk, g) / v(den_blk, g) for g in groups}
    printed = {g: v(ratio_blk, g) for g in groups}
    for pg in groups:
        for dg in groups:
            err = np.max(np.abs(printed[pg] - derived[dg]) / derived[dg])
            rows.append(dict(antigen=ag, printed_block=ratio_blk, printed_label=pg, derived_from=f'{num_blk}/{den_blk}', derived_label=dg,
                             max_rel_error=err, match=err < 0.002))
R = pd.DataFrame(rows)
print(R[R.match].to_string(index=False))
R.to_csv('check_IgG2a_IgG1_labels.csv', index=False)
# geometric mean ratios under the S13 labelling
for num_blk, den_blk, ag in [('S13-A', 'S13-B', 'H1N1'), ('S13-C', 'S13-D', 'H3N2')]:
    for g in groups:
        r = v(num_blk, g) / v(den_blk, g)
        print(ag, g, 'IgG2a/IgG1 per animal', np.round(r, 3), 'geo-mean', round(float(np.exp(np.mean(np.log(r)))), 3))
# Tfh:Tfr printed vs (100 - Foxp3%)/Foxp3%
for g in ['Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']:
    f = v('S04-B_Foxp3', g); q = v('S04-B_TfhTfr', g)
    print('S04-B', g, 'printed Tfh:Tfr', np.round(q, 4), ' (100-Foxp3)/Foxp3', np.round((100 - f) / f, 4), ' identical:', np.allclose(q, (100 - f) / f, rtol=1e-5))
