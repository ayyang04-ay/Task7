import pandas as pd, numpy as np
R = pd.read_csv('/tmp/work/tidy/summary_survival.csv'); P = pd.read_csv('/tmp/work/tidy/pairwise_survival.csv')
F = pd.read_csv('/tmp/work/tidy/flagged_experiments.csv').set_index('experiment')['reason'].to_dict()
def surv(b, g):
    r = R[(R.block == b) & (R.group == g)]
    return f"{int(r.survivors.iloc[0])}/{int(r.n.iloc[0])}" if len(r) else '–'
def p(b, a, c):
    x = P[(P.block == b) & (((P.group_a == a) & (P.group_b == c)) | ((P.group_a == c) & (P.group_b == a)))]
    return x.p_logrank.iloc[0] if len(x) else np.nan
rows = []
order = ['S03-I', 'S03-J', 'S06-A', 'S06-B', 'S06-C', 'S06-D', 'S06-E', 'S06-F', 'S06-G', 'S15-L', 'S15-N']
for b in order:
    r0 = R[R.block == b].iloc[0]
    rows.append(dict(experiment=b, model=r0.model, challenge=r0.challenge, day=('' if pd.isna(r0.day) else int(r0.day)),
                     vehicle=surv(b, 'Sham'), PSLN212=surv(b, 'PSLN-212'), PSLN344=surv(b, 'PSLN-344'), young212=surv(b, 'PSLN-212(Y)'),
                     untreated_unchallenged=surv(b, 'Untreated'), p_344_vs_vehicle=p(b, 'PSLN-344', 'Sham'), p_344_vs_212=p(b, 'PSLN-344', 'PSLN-212'),
                     integrity_flag=F.get(b, '')))
T = pd.DataFrame(rows); T.to_csv('/tmp/work/tidy/aged_experiment_table.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 60)
print(T.to_string(index=False))
