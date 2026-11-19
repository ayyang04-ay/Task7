"""Parse every block of the workbook into tidy tables with cell provenance."""
import re, json
import openpyxl
import pandas as pd
from blocks import XLSX, BLOCKS, SURV, BW

def norm_group(g):
    if g is None:
        return None
    g = str(g).strip().replace('\u00ef', 'i').replace('Naïve', 'Naive')
    g = re.sub(r'\s+', ' ', g)
    g = re.sub(r'PSLN-(\d+)\s*[Yy]$', r'PSLN-\1(Y)', g)      # PSLN-212Y -> PSLN-212(Y)
    g = re.sub(r'\((y)\)', '(Y)', g)                        # (y) -> (Y)
    return g

def load():
    return openpyxl.load_workbook(XLSX, data_only=True)

def tidy_continuous(wb):
    recs = []
    for bid, b in BLOCKS.items():
        ws = wb[b['sheet']]
        if b['kind'] == 'colgroups':
            for c in b['cols']:
                g_raw = ws[f"{c}{b['header_row']}"].value
                for r in b['rows']:
                    v = ws[f'{c}{r}'].value
                    if v is None:
                        continue
                    recs.append(dict(block=bid, sheet=b['sheet'], group_raw=g_raw, group=norm_group(g_raw), level='',
                                     value=float(v), cell=f"{b['sheet']}!{c}{r}", header_cell=f"{b['sheet']}!{c}{b['header_row']}"))
        elif b['kind'] == 'rowgroups':
            for r in b['rows']:
                g_raw = ws[f"{b['label_col']}{r}"].value
                for c in b['cols']:
                    v = ws[f'{c}{r}'].value
                    if v is None:
                        continue
                    recs.append(dict(block=bid, sheet=b['sheet'], group_raw=g_raw, group=norm_group(g_raw), level='',
                                     value=float(v), cell=f"{b['sheet']}!{c}{r}", header_cell=f"{b['sheet']}!{b['label_col']}{r}"))
        elif b['kind'] == 'spans':
            for r in b['rows']:
                lvl = ws[f"{b['time_col']}{r}"].value if b['time_col'] else ''
                for g, cols in b['groups'].items():
                    for c in cols:
                        v = ws[f'{c}{r}'].value
                        if v is None:
                            continue
                        recs.append(dict(block=bid, sheet=b['sheet'], group_raw=g, group=norm_group(g), level=str(lvl),
                                         value=float(v), cell=f"{b['sheet']}!{c}{r}", header_cell=''))
    df = pd.DataFrame(recs)
    df['measurand'] = df.block.map(lambda k: BLOCKS[k]['measurand'])
    df['scale'] = df.block.map(lambda k: BLOCKS[k]['scale'])
    return df

def tidy_survival(wb):
    recs = []
    for bid, s in SURV.items():
        ws = wb[s['sheet']]
        heads = {c: norm_group(ws[f"{c}{s['header_row']}"].value) for c in s['group_cols']}
        for r in s['rows']:
            d = ws[f"{s['days_col']}{r}"].value
            for c in s['group_cols']:
                ev = ws[f'{c}{r}'].value
                if ev is None:
                    continue
                recs.append(dict(block=bid, sheet=s['sheet'], group=heads[c], days=d, event=int(ev),
                                 cell_days=f"{s['sheet']}!{s['days_col']}{r}", cell_event=f"{s['sheet']}!{c}{r}",
                                 desc=s['desc'], cohort=s['cohort']))
    return pd.DataFrame(recs)

def tidy_bw(wb):
    recs = []
    for bid, w in BW.items():
        ws = wb[w['sheet']]
        for r in w['rows']:
            d = ws[f"{w['days_col']}{r}"].value
            for g, cols in w['groups'].items():
                for k, c in enumerate(cols):
                    v = ws[f'{c}{r}'].value
                    recs.append(dict(block=bid, sheet=w['sheet'], group=norm_group(g), animal=f'{g}#{k+1}', col=c,
                                     day=d, value=(float(v) if v is not None else None), cell=f"{w['sheet']}!{c}{r}"))
    return pd.DataFrame(recs)

if __name__ == '__main__':
    wb = load()
    cont = tidy_continuous(wb); surv = tidy_survival(wb); bw = tidy_bw(wb)
    cont.to_csv('/tmp/outputs/analysis/tidy_continuous.csv', index=False)
    surv.to_csv('/tmp/outputs/analysis/tidy_survival.csv', index=False)
    bw.to_csv('/tmp/outputs/analysis/tidy_bodyweight.csv', index=False)
    print(cont.shape, surv.shape, bw.shape)
    # quick checks of counts per block/group
    print(cont.groupby(['block', 'group', 'level']).size().reset_index(name='n').to_string())
