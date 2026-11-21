from blocks import *
import pandas as pd
d = pd.concat(S.values()); d['day'] = d['day'].fillna(21)
d.to_csv('tte_all.csv', index=False)
