import pandas as pd, numpy as np
DF = pd.read_csv('/tmp/work/tidy_values.csv', dtype={'day':object,'hour':object})
SV = pd.read_csv('/tmp/work/tidy_survival.csv')
