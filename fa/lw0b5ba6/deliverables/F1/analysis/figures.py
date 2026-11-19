"""
figures.py -- all figures of the proposal, drawn at (close to) their printed width (<= 7.0 in) so that text stays >= 6.5 pt.
Every number shown is computed here from the workbook cells (via psln_blocks) or read from the analysis tables T5-T14.
"""
from paths import TABLES, FIGS, OUT as OUTDIR, BUILD, PANDOC
import numpy as np, pandas as pd, matplotlib, warnings, textwrap
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Polygon
import psln_blocks as pb
from stats_util import clopper_pearson
warnings.filterwarnings('ignore')
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 7.5, 'axes.spines.top': False, 'axes.spines.right': False, 'figure.dpi': 120, 'savefig.dpi': 250,
                     'axes.titlesize': 8.2, 'axes.titleweight': 'bold', 'axes.labelsize': 7.5, 'xtick.labelsize': 7, 'ytick.labelsize': 7, 'legend.fontsize': 6.8,
                     'axes.linewidth': 0.7, 'xtick.major.width': 0.7, 'ytick.major.width': 0.7})
COL = {'Sham': '#8c8c8c', 'PSLN-212': '#E69F00', 'PSLN-344': '#0072B2', 'PSLN-212(Y)': '#009E73', 'CMP-204': '#CC79A7', 'PSLN-212/R848': '#D55E00', 'Vaccine': '#8c8c8c'}
LAB = {'Sham': 'Vehicle + vaccine (aged)', 'PSLN-212': 'PSLN-212 (aged)', 'PSLN-344': 'PSLN-344 (aged)', 'PSLN-212(Y)': 'PSLN-212 (young benchmark)'}
OUT = FIGS; T = TABLES
df = pb.tidy(); sv = df[df.kind == 'surv']
S5 = pd.read_csv(T + 'T5_survival_by_block.csv')
def canvas(w, h):
    fig = plt.figure(figsize=(w, h)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, w); ax.set_ylim(0, h); ax.axis('off'); return fig, ax
def m(block, group, analyte=None, x=None, geo=False):
    t = df[(df.block == block) & (df.group == group)]
    if analyte is not None: t = t[t.analyte.str.contains(analyte, regex=False)]
    if x is not None: t = t[t.x.astype(str) == str(x)]
    v = t.value.to_numpy(float)
    return 10 ** np.mean(np.log10(np.where(v <= 0, 5, v))) if geo else v.mean()

# ------------------------------------------------------------------ Figure 1: survivors by experiment
def fig_survival_table():
    rows = [('S03-I', 'Bivalent vaccine; CA09 H1N1 on day 14', 'a'), ('S03-J', 'rgH5N1 vaccine; wild-type H5N1 on day 2', 'a'),
            ('S06-A', 'H3N2 vaccine; PR8 H1N1 on day 14', ''), ('S06-B', 'H3N2 vaccine; PR8 H1N1 on day 3', ''),
            ('S06-C', 'Bivalent vaccine; rgH5N1 on day 14', 'b'), ('S06-D', 'Bivalent vaccine; rgH5N1 on day 3', 'c'),
            ('S06-E (rows 34-68)', 'H3N2 vaccine; PR8 H1N1 on day 60', ''), ('S06-F (rows 34-68)', 'Bivalent vaccine; rgH5N1 on day 60', ''),
            ('S06-G', 'H1N1 vaccine; Perth H3N2 on day 60', ''), ('S15-L', 'C57BL/6, bivalent; challenge not stated', ''),
            ('S15-N', 'Swiss Webster, bivalent; challenge not stated', '')]
    groups = ['Sham', 'PSLN-212', 'PSLN-344', 'PSLN-212(Y)']
    Wf, Hf = 7.0, 5.45; x0, cw, rh = 3.28, 0.915, 0.27
    fig, ax = canvas(Wf, Hf)
    cmap = matplotlib.colormaps['Blues']; shade = lambda f: cmap(0.05 + 0.75 * f); tcol = lambda f: 'w' if f > 0.6 else 'k'
    ytop = Hf - 0.78
    hdr = {'Sham': 'Vehicle + vaccine\n(aged)', 'PSLN-212': 'PSLN-212\n(aged)', 'PSLN-344': 'PSLN-344\n(aged)', 'PSLN-212(Y)': 'PSLN-212, young\n(benchmark)'}
    ax.text(0.05, Hf - 0.16, 'Survivors / animals challenged in each aged-animal experiment', fontsize=8.6, fontweight='bold', va='center')
    for j, g in enumerate(groups):
        ax.text(x0 + j * cw + cw / 2, ytop + 0.22, hdr[g], ha='center', va='bottom', fontsize=7.2, fontweight='bold', color=COL[g], linespacing=1.1)
    tot = {g: [0, 0] for g in groups}; tot8 = {g: [0, 0] for g in groups}
    for i, (blk, desc, flag) in enumerate(rows):
        y = ytop - i * rh
        ax.text(x0 - 0.1, y, blk.replace(' (rows 34-68)', ''), ha='right', va='center', fontsize=7.6, fontweight='bold')
        if flag: ax.text(x0 - 0.63, y + 0.03, flag, ha='right', va='center', fontsize=7.2, color='#b00020', fontweight='bold')
        ax.text(x0 - 0.78, y, desc, ha='right', va='center', fontsize=7.2)
        for j, g in enumerate(groups):
            r = S5[(S5.block == blk) & (S5.group == g)]
            if len(r) == 0:
                ax.add_patch(Rectangle((x0 + j * cw, y - rh / 2 + 0.012), cw - 0.025, rh - 0.024, color='#f2f2f2')); ax.text(x0 + j * cw + cw / 2, y, 'no arm', ha='center', va='center', fontsize=6.6, color='#888'); continue
            s, n = int(r.survivors.iloc[0]), int(r.n.iloc[0])
            ax.add_patch(Rectangle((x0 + j * cw, y - rh / 2 + 0.012), cw - 0.025, rh - 0.024, color=shade(s / n)))
            ax.text(x0 + j * cw + cw / 2, y, f'{s}/{n}', ha='center', va='center', fontsize=8.2, fontweight='bold', color=tcol(s / n))
            tot[g][0] += s; tot[g][1] += n
            if flag in ('', 'b'): tot8[g][0] += s; tot8[g][1] += n
    ybar = ytop - len(rows) * rh + 0.05
    ax.plot([0.05, x0 + 4 * cw], [ybar, ybar], color='k', lw=0.7)
    for k, (lab, TT) in enumerate([('All 11 experiments, as printed', tot), ('8 headline experiments (see notes)', tot8)]):
        y = ybar - 0.25 - k * 0.44
        ax.text(x0 - 0.1, y, lab, ha='right', va='center', fontsize=7.4, fontweight='bold')
        for j, g in enumerate(groups):
            s, n = TT[g]; lo, hi = clopper_pearson(s, n)
            ax.add_patch(Rectangle((x0 + j * cw, y - 0.19), cw - 0.025, 0.38, color=shade(s / n), ec='k', lw=0.6))
            ax.text(x0 + j * cw + cw / 2, y + 0.07, f'{s}/{n} = {100*s/n:.0f}%', ha='center', va='center', fontsize=7.4, fontweight='bold', color=tcol(s / n))
            ax.text(x0 + j * cw + cw / 2, y - 0.09, f'95% CI {100*lo:.0f}-{100*hi:.0f}%', ha='center', va='center', fontsize=6.3, color=tcol(s / n))
    yl = 0.62
    ax.text(0.05, yl, 'a', fontsize=7, color='#b00020', fontweight='bold'); ax.text(0.17, yl, 'control-arm labels conflict with the paired body-weight block (defects D2, D3); the PSLN-344 and young arms agree in both', fontsize=6.5)
    ax.text(0.05, yl - 0.15, 'b', fontsize=7, color='#b00020', fontweight='bold'); ax.text(0.17, yl - 0.15, 'table identical to S06-D (defect D1); counted once', fontsize=6.5)
    ax.text(0.05, yl - 0.30, 'c', fontsize=7, color='#b00020', fontweight='bold'); ax.text(0.17, yl - 0.30, 'table identical to S06-C and in conflict with its own weight block (defect D1); not counted', fontsize=6.5)
    ax.text(0.05, yl - 0.47, 'Headline set: the eight experiments left when b is counted once and a and c are left out.', fontsize=6.5, style='italic')
    fig.savefig(OUT + 'fig1_survival_by_experiment.png'); plt.close(fig)

# ------------------------------------------------------------------ Figure 2: pooled Kaplan-Meier
def km(times, events, tmax=14):
    t = np.asarray(times, float); e = np.asarray(events, int); xs = [0]; ys = [1.0]; s = 1.0
    for u in np.unique(t[e == 1]):
        n = (t >= u).sum(); d = ((t == u) & (e == 1)).sum(); s *= 1 - d / n; xs += [u, u]; ys += [ys[-1], s]
    xs.append(tmax); ys.append(ys[-1]); return xs, ys
def fig_km():
    blocks = ['S06-A', 'S06-B', 'S06-C', 'S06-E (rows 34-68)', 'S06-F (rows 34-68)', 'S06-G', 'S15-L', 'S15-N']
    fig = plt.figure(figsize=(6.6, 2.9)); ax = fig.add_axes([0.085, 0.155, 0.60, 0.75])
    for g in ['PSLN-212(Y)', 'PSLN-344', 'PSLN-212', 'Sham']:
        t = sv[sv.block.isin(blocks) & (sv.group == g)]; xs, ys = km(t.value, t.event)
        ax.plot(xs, [100 * y for y in ys], color=COL[g], lw=1.9, label=f'{LAB[g]}\n{int((t.event==0).sum())} of {len(t)} survived')
    ax.set_xlabel('Days after lethal influenza challenge'); ax.set_ylabel('Survival (%)'); ax.set_ylim(-3, 103); ax.set_xlim(0, 14.3)
    ax.legend(frameon=False, fontsize=7.2, loc='center left', bbox_to_anchor=(1.02, 0.5), labelspacing=1.1)
    ax.set_title('Pooled survival in the 8 headline experiments (aged animals)', loc='left')
    fig.savefig(OUT + 'fig2_pooled_survival.png'); plt.close(fig)

# ------------------------------------------------------------------ Figure 3: restoration index
def fig_restoration():
    R = pd.read_csv(T + 'T11_restoration_and_biomarker_triage.csv').iloc[::-1].reset_index(drop=True)
    dcol = {'1 Innate sensing': '#0072B2', '2 Monocyte/DC': '#56B4E9', '3 GC / Tfh': '#009E73', '4 Antibody': '#E69F00', '5 CD8 T cell': '#D55E00', '6 Regulatory milieu': '#CC79A7'}
    nice = {'IFNg': 'IFN-γ'}
    fig = plt.figure(figsize=(6.8, 7.6)); ax = fig.add_axes([0.50, 0.085, 0.48, 0.865])
    for i, r in R.iterrows():
        c = dcol[r.domain]
        ax.plot([max(r.RI_lo, -0.1), min(r.RI_hi, 1.6)], [i, i], color=c, lw=1.3); ax.plot(r.restoration_index, i, 'o', color=c, ms=4.2)
        ax.text(-0.14, i, f"{r.endpoint.replace('IFNg', 'IFN-γ')}  [{r.block}]", ha='right', va='center', fontsize=6.6)
    ax.axvline(0, color='#E69F00', lw=1); ax.axvline(1, color='#009E73', lw=1)
    ax.text(0, len(R) + 0.2, 'aged,\nPSLN-212', ha='center', va='bottom', fontsize=6.8, color='#b37a00', fontweight='bold', linespacing=1.0)
    ax.text(1, len(R) + 0.2, 'young\nbenchmark', ha='center', va='bottom', fontsize=6.8, color='#009E73', fontweight='bold', linespacing=1.0)
    ax.set_yticks([]); ax.spines['left'].set_visible(False); ax.set_xlim(-0.1, 1.6); ax.set_ylim(-0.8, len(R) - 0.2)
    ax.set_xlabel('Restoration index of PSLN-344 in aged animals\n(0 = no better than PSLN-212 in aged; 1 = young benchmark;\nbars = bootstrap 95% CI)', fontsize=7)
    handles = [plt.Line2D([0], [0], marker='o', color=c, lw=1.3, ms=4, label={'1 Innate sensing': 'Interferon', '2 Monocyte/DC': 'Monocyte / dendritic cell', '3 GC / Tfh': 'Germinal centre / Tfh',
               '4 Antibody': 'Antibody', '5 CD8 T cell': 'CD8 T cell', '6 Regulatory milieu': 'Suppressive cells'}[d]) for d, c in dcol.items()]
    fig.legend(handles=handles, frameon=False, fontsize=6.6, loc='lower left', bbox_to_anchor=(0.03, 0.004), ncol=2, columnspacing=1.2, handlelength=1.6)
    fig.savefig(OUT + 'fig3_restoration_index.png'); plt.close(fig)

# ------------------------------------------------------------------ Figure 4: gated plan
def fig_plan():
    Wf, Hf = 7.0, 4.0; fig, ax = canvas(Wf, Hf)
    def box(x, y, w, h, title, body, fc, ec):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.0,rounding_size=0.05', fc=fc, ec=ec, lw=1.0))
        ax.text(x + 0.07, y + h - 0.09, title, fontsize=7.6, fontweight='bold', va='top'); ax.text(x + 0.07, y + h - 0.29, body, fontsize=6.8, va='top', linespacing=1.3)
    def gate(x, y, label):
        ax.add_patch(Polygon([[x, y + 0.2], [x + 0.2, y], [x, y - 0.2], [x - 0.2, y]], closed=True, fc='#fff3cd', ec='#b8860b', lw=1.0)); ax.text(x, y, label, ha='center', va='center', fontsize=6.8, fontweight='bold')
    def arr(x0, y0, x1, y1, rad=0.0):
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle='-|>', mutation_scale=8, lw=0.9, color='#333', connectionstyle=f'arc3,rad={rad}'))
    B, G, O, P = ('#dbe9f6', '#2b6ca3'), ('#d8f0e3', '#1b7f4d'), ('#fde5d2', '#c0561a'), ('#ece3f5', '#6a3d9a')
    ax.text(0.05, Hf - 0.15, 'Release funding one gate at a time', fontsize=8.6, fontweight='bold', va='center')
    y1 = Hf - 1.25; h = 0.88
    box(0.05, y1, 2.55, h, 'Step 0  Records audit', 'trace every flagged block to source;\ncorrect or withdraw; re-issue the dataset', *B)
    gate(2.92, y1 + h / 2, 'G0')
    box(3.24, y1, 3.05, h, 'Study 1  Confirm, attribute, compare', 'blinded, randomised, both sexes; Mn-only and\ncGAMP+Mn arms; enhanced-vaccine comparator;\nbiomarkers in the challenged animals', *G)
    gate(6.62, y1 + h / 2, 'G1')
    arr(2.61, y1 + h / 2, 2.71, y1 + h / 2); arr(3.13, y1 + h / 2, 3.23, y1 + h / 2); arr(6.30, y1 + h / 2, 6.41, y1 + h / 2)
    y2 = y1 - 1.18
    box(0.08, y2, 1.95, h, 'Study 2  Dose, durability', 'lowest effective dose, margin;\nday-90 challenge with\nunchallenged aged controls', *G)
    box(2.13, y2, 1.98, h, 'Study 3  Safety, Mn exposure', 'brain and lung manganese;\nhistopathology; resolution\nto day 28; repeat dose', *O)
    gate(4.43, y2 + h / 2, 'G2')
    box(4.75, y2, 1.55, h, 'Study 4  Ferret,\nhuman cells', '', *P)
    ax.text(4.82, y2 + h - 0.45, 'nasal vs lung delivery;\ndonor cells aged 65+', fontsize=6.8, va='top', linespacing=1.3)
    gate(6.62, y2 + h / 2, 'G3')
    yb = y1 - 0.14
    ax.plot([6.62, 6.62, 1.04], [y1 + h / 2 - 0.21, yb, yb], color='#333', lw=0.9, solid_joinstyle='round')
    arr(1.04, yb, 1.04, y2 + h + 0.01); arr(3.12, yb, 3.12, y2 + h + 0.01)
    ax.add_patch(FancyBboxPatch((0.02, y2 - 0.05), 4.14, h + 0.1, boxstyle='round,pad=0.0,rounding_size=0.06', fc='none', ec='#777', lw=0.7, ls=(0, (3, 2))))
    arr(4.12, y2 + h / 2, 4.22, y2 + h / 2); arr(4.64, y2 + h / 2, 4.74, y2 + h / 2); arr(6.31, y2 + h / 2, 6.41, y2 + h / 2)
    y3 = y2 - 0.62
    box(0.05, y3, 6.25, 0.46, 'Study 5  Manufacturing readiness (runs alongside from G0)', '', '#f3f3f3', '#888888')
    ax.text(0.12, y3 + 0.1, 'encapsulation ≥ 70%; Mn content; particle specification; 2-8 °C stability; endotoxin; device compatibility', fontsize=6.6, va='center')
    gl = [('G0', 'primary survival tables verified at source; corrected dataset re-issued'),
          ('G1', 'effect replicates in both sexes; CDN-1807 adds to Mn alone; not worse than the enhanced-vaccine comparator'),
          ('G2', 'effective dose has a ≥ 2-fold tolerability margin; no brain manganese accumulation; lung changes resolve; protection at day 90'),
          ('G3', 'efficacy in a second species and activity in human cells shown: decision to start IND-enabling work')]
    for i, (g, t) in enumerate(gl):
        ax.text(0.05, y3 - 0.2 - i * 0.17, g, fontsize=6.8, fontweight='bold', color='#6b4e00', va='center'); ax.text(0.36, y3 - 0.2 - i * 0.17, t, fontsize=6.6, color='#333', va='center')
    fig.savefig(OUT + 'fig4_gated_plan.png'); plt.close(fig)

# ------------------------------------------------------------------ Figure 5: mechanism
def fig_mechanism():
    f0 = lambda v: f'{v:.0f}'; f1 = lambda v: f'{v:.1f}'
    ig = lambda g: np.mean(df[(df.block == 'S13-A') & (df.group == g)].sort_values('rep').value.to_numpy() / df[(df.block == 'S13-B') & (df.group == g)].sort_values('rep').value.to_numpy())
    CAUSAL, ASSOC, GAP = '#d8f0e3', '#dbe9f6', '#f3f3f3'; EC = {CAUSAL: '#1b7f4d', ASSOC: '#2b6ca3', GAP: '#888888'}
    B = {
     'dose': (0, 0, 'PSLN-344 + inactivated vaccine', 'one intranasal dose, 20 µg (in the mouse this reaches the lung)', GAP),
     'am': (1, 0, '1  Alveolar-macrophage uptake', f"needs surfactant proteins A/D: {f0(m('S01-C','WT'))}% of macrophages take up liposome vs {f0(m('S01-C','SPA/D'))}% in knock-out [S01-C]", CAUSAL),
     'aec': (2, 0, '2  Cargo reaches lung epithelium', f"type II cells {f1(m('S01-B','AECII/PSLN-SRB'))}% vs {f1(m('S01-B','AECII/FreeSRB'))}% with free dye [S01-B]; gap-junction blocker cuts monocyte influx {f0(100*(1-m('S11-C','CBX+')/m('S11-C','CBX-')))}% [S11-C]", CAUSAL),
     'ifn': (2, 1, '3  STING to type I interferon', f"lung Ifnb1 at 16 h: {f0(m('S01-A','PSLN-344',x='16h'))}-fold (aged PSLN-212 {f0(m('S01-A','PSLN-212',x='16h'))}; young {f0(m('S01-A','PSLN-212(Y)',x='16h'))}) [S01-A]; dose-dependent [S08-A]", ASSOC),
     'gm': (1, 1, '4  GM-CSF', f"lung Gm-csf {f1(m('S02-F','PSLN-344',x='16h'))}- and {f1(m('S02-F','PSLN-344',x='36h'))}-fold at 16 and 36 h (PSLN-212 {f1(m('S02-F','PSLN-212',x='16h'))} and {f1(m('S02-F','PSLN-212',x='36h'))}) [S02-F]", ASSOC),
     'mono': (0, 1, '5  CCR2+ monocyte influx', f"monocytes on day 4: {f0(m('S01-D','PSLN-344',x=4))}% (PSLN-212 {f0(m('S01-D','PSLN-212',x=4))}%) [S01-D]; CCR2 blocker: {f1(m('S07-B','PSLN-344','monocytes'))}% to {f1(m('S07-B','PSLN-344+INCB3344','monocytes'))}% [S07-B]", CAUSAL),
     'modc': (0, 2, '6  Monocyte to dendritic cell', f"needs interferon receptor: {f1(m('S02-H','WT w/o cDC'))}% to {f1(m('S02-H','IFN w/o cDC'))}%; GM-CSF restores {f1(m('S02-H','GMCSF'))}% [S02-H]; GM-CSF rescues PSLN-212 [S02-G]", CAUSAL),
     'mig': (1, 2, '7  DC migration, antigen transport', f"CCR7+ DC {f0(m('S02-A','PSLN-344'))}% (PSLN-212 {f0(m('S02-A','PSLN-212'))}%) [S02-A]; antigen+ DC in node {f1(m('S02-C','PSLN-344'))}% ({f1(m('S02-C','PSLN-212'))}%), blocked by pertussis toxin [S02-C]", CAUSAL),
     'cost': (2, 2, '8  DC co-stimulation: weakest link', f"CD40+ {f0(m('S02-D CD40','PSLN-344'))}% and CD86+ {f0(m('S02-D CD86','PSLN-344'))}%; aged PSLN-212 {f0(m('S02-D CD40','PSLN-212'))}% and {f0(m('S02-D CD86','PSLN-212'))}%; young {f0(m('S02-D CD40','PSLN-212(Y)'))}% and {f0(m('S02-D CD86','PSLN-212(Y)'))}% [S02-D]", ASSOC),
     'gc': (2, 3, '9a  Germinal centre, Tfh', f"GC B cells {f1(m('S03-K','PSLN-344'))}% ({f1(m('S03-K','PSLN-212'))}%) [S03-K]; helper:regulatory ratio {f1(m('S04-B Tfh:Tfr','PSLN-344'))} ({f1(m('S04-B Tfh:Tfr','PSLN-212'))}) [S04-B]", ASSOC),
     'ab': (1, 3, '10a  Antibody', f"HAI titre {f0(m('S03-C','PSLN-344',geo=True))} ({f0(m('S03-C','PSLN-212',geo=True))}) [S03-C]; IgG2a/IgG1 {f1(ig('PSLN-344'))} ({f1(ig('PSLN-212'))}) [S13-A, S13-B]", ASSOC),
     'prot': (0, 3, '11  Protection', "survival 79-85% (PSLN-212 11-14%) [S03, S06, S15]; antigen required: adjuvant alone 0 of 7 [S15-H]", CAUSAL),
     'cd8': (2, 4, '9b  Lung CD8 T cells', f"primed in the lung itself [S05-C]; IFN-γ+ CD8 to H5N1, not in the vaccine: {f1(m('S05-F','PSLN-344'))}% ({f1(m('S05-F','PSLN-212'))}%) [S05-F]; need CCR2+ monocytes [S02-I]", CAUSAL),
     'trm': (1, 4, '10b  Resident memory CD8', f"lung TRM day 25: {f1(m('S05-I','PSLN-344'))}% (aged PSLN-212 {f1(m('S05-I','PSLN-212'))}%; young {f1(m('S05-I','PSLN-212(Y)'))}%) [S05-I]", ASSOC),
     'brake': (0, 4, 'Aged-lung suppressor cells recede', f"CD206+ macrophages {f0(m('S11-E','PSLN-344'))}% ({f0(m('S11-E','PSLN-212'))}%) [S11-E]; lung Treg {f1(m('S04-D','PSLN-344'))}% ({f1(m('S04-D','PSLN-212'))}%) [S04-D]", ASSOC),
    }
    Wf, Hf = 7.0, 6.8; bw, bh, gx, gy = 2.15, 0.98, 0.15, 0.2; x0 = 0.05; ytop = Hf - 0.42
    fig, ax = canvas(Wf, Hf)
    ax.text(0.05, Hf - 0.15, 'Mechanism of action supported by the dataset', fontsize=8.6, fontweight='bold', va='center')
    pos = {}
    for k, (c, r, title, body, col) in B.items():
        x = x0 + c * (bw + gx); y = ytop - (r + 1) * bh - r * gy
        ax.add_patch(FancyBboxPatch((x, y), bw, bh, boxstyle='round,pad=0.0,rounding_size=0.05', fc=col, ec=EC[col], lw=1.0))
        ax.text(x + 0.07, y + bh - 0.09, title, fontsize=7.5, fontweight='bold', va='top')
        ax.text(x + 0.07, y + bh - 0.30, '\n'.join(textwrap.wrap(body, 37)), fontsize=6.7, va='top', linespacing=1.28)
        pos[k] = (x, y)
    def pt(k, side):
        x, y = pos[k]; return {'r': (x + bw, y + bh / 2), 'l': (x, y + bh / 2), 't': (x + bw / 2, y + bh), 'b': (x + bw / 2, y)}[side]
    def arrow(a, sa, b, sb, ls='-', rad=0.0):
        ax.add_patch(FancyArrowPatch(pt(a, sa), pt(b, sb), arrowstyle='-|>', mutation_scale=9, lw=1.0, color='#333', ls=ls, connectionstyle=f'arc3,rad={rad}', shrinkA=1, shrinkB=1))
    arrow('dose', 'r', 'am', 'l'); arrow('am', 'r', 'aec', 'l'); arrow('aec', 'b', 'ifn', 't'); arrow('ifn', 'l', 'gm', 'r'); arrow('gm', 'l', 'mono', 'r'); arrow('mono', 'b', 'modc', 't')
    arrow('modc', 'r', 'mig', 'l'); arrow('mig', 'r', 'cost', 'l'); arrow('cost', 'b', 'gc', 't'); arrow('gc', 'l', 'ab', 'r'); arrow('ab', 'l', 'prot', 'r')
    # 8 -> 9b along the right margin
    x8, y8 = pos['cost']; x9, y9 = pos['cd8']
    ax.plot([x8 + bw, x8 + bw + 0.09, x8 + bw + 0.09], [y8 + bh * 0.3, y8 + bh * 0.3, y9 + bh / 2], color='#333', lw=1.0)
    ax.add_patch(FancyArrowPatch((x8 + bw + 0.09, y9 + bh / 2), (x9 + bw, y9 + bh / 2), arrowstyle='-|>', mutation_scale=9, lw=1.0, color='#333', shrinkA=0, shrinkB=1))
    arrow('cd8', 'l', 'trm', 'r')
    xt, yt = pos['trm']; xp, yp = pos['prot']
    ax.add_patch(FancyArrowPatch((xt + 0.35, yt + bh), (xp + bw - 0.25, yp), arrowstyle='-|>', mutation_scale=9, lw=1.0, color='#333', shrinkA=1, shrinkB=1))
    arrow('brake', 't', 'prot', 'b', ls='--')
    ly = pos['brake'][1] - 0.22
    for i, (col, lab) in enumerate([(CAUSAL, 'link tested by an intervention in our data (knock-out, blocker, rescue or omission)'), (ASSOC, 'link supported by a group difference only')]):
        xx = [0.05, 4.35][i]
        ax.add_patch(FancyBboxPatch((xx, ly - 0.05), 0.2, 0.1, boxstyle='round,pad=0.0,rounding_size=0.02', fc=col, ec=EC[col], lw=0.8)); ax.text(xx + 0.27, ly, lab, fontsize=6.6, va='center')
    ax.text(0.05, ly - 0.2, 'Values are PSLN-344 in aged animals, with aged PSLN-212 in brackets unless stated. Not tested in the data: STING knock-out,', fontsize=6.5, va='center', color='#444')
    ax.text(0.05, ly - 0.34, 'Mn-only control, CD8 depletion, serum transfer. On-target action and the protective arm are therefore inferred, not proven.', fontsize=6.5, va='center', color='#444')
    fig.savefig(OUT + 'fig5_mechanism.png'); plt.close(fig)

# ------------------------------------------------------------------ Figure 6: record defects
def fig_defects():
    fig, axs = plt.subplots(2, 2, figsize=(7.0, 6.3)); fig.subplots_adjust(left=0.08, right=0.985, top=0.925, bottom=0.075, hspace=0.5, wspace=0.27)
    v = lambda b, g: df[(df.block == b) & (df.group == g)].sort_values('rep').value.to_numpy(float)
    ax = axs[0, 0]; groups = ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)']; x = np.arange(3)
    printed = [v('S03-B', g) for g in groups]; comp = [v('S13-A', g) / v('S13-B', g) for g in groups]
    for i in range(3):
        ax.bar(x[i] - 0.2, printed[i].mean(), 0.38, color='#bbbbbb', label='as printed in S03-B' if i == 0 else None); ax.plot(np.full(5, x[i] - 0.2) + np.linspace(-0.1, 0.1, 5), printed[i], 'k.', ms=3)
        ax.bar(x[i] + 0.2, comp[i].mean(), 0.38, color='#0072B2', label='recomputed from S13-A / S13-B' if i == 0 else None); ax.plot(np.full(5, x[i] + 0.2) + np.linspace(-0.1, 0.1, 5), comp[i], 'k.', ms=3)
    ax.set_xticks(x); ax.set_xticklabels(['PSLN-212\n(aged)', 'PSLN-344\n(aged)', 'PSLN-212\n(young)']); ax.set_ylabel('IgG2a / IgG1 ratio, anti-CA09'); ax.set_ylim(0, 5.9)
    ax.legend(frameon=False, loc='upper center', ncol=1, fontsize=6.5)
    ax.set_title('a  D4: ratio block has its headers rotated\n    (same 15 values, different owners)', loc='left')
    ax = axs[0, 1]
    a = df[df.block == 'S11-A']; b = df[df.block == 'S11-B']; mm = a.merge(b, on=['group', 'x', 'rep'], suffixes=('_A', '_B')); same = mm.value_A == mm.value_B
    ax.plot(mm.value_A[~same], mm.value_B[~same], 'o', color='#999999', ms=3, label=f'different ({int((~same).sum())})')
    ax.plot(mm.value_A[same], mm.value_B[same], 'o', color='#D55E00', ms=3.6, label=f'identical to the decimal ({int(same.sum())} of {len(mm)})')
    lim = [14, 56]; ax.plot(lim, lim, 'k:', lw=0.7); ax.set_xlim(lim); ax.set_ylim(lim)
    ax.set_xlabel('S11-A alveolar macrophages (%),\nsame group, day and animal position'); ax.set_ylabel('S11-B "neutrophils" (%)'); ax.legend(frameon=False, loc='upper left', fontsize=6.5)
    ax.set_title('b  D5: "neutrophil" block repeats the\n    macrophage block', loc='left')
    ax = axs[1, 0]
    w = df[df.kind == 'weight'].copy(); w['col'] = w.cell.str.extract(r'!([A-Z]+)\d+')[0]; w['x'] = w.x.astype(float)
    for blk, g, c, ls, lab in [('S15-C', 'PSLN-344', '#0072B2', '-', 'S15-C: challenge on day 14'), ('S15-I', '3d Vaccine+PSLN-344', '#D55E00', '--', 'S15-I: challenge on day 3')]:
        t = w[(w.block == blk) & (w.group == g)]
        for k, (col, tt) in enumerate(t.groupby('col', sort=False)):
            tt = tt.sort_values('x'); ax.plot(tt.x, tt.value, ls, color=c, lw=1.9 if ls == '-' else 1.0, marker='o' if ls == '--' else None, ms=2.2, label=lab if k == 0 else None, alpha=0.9)
    ta = w[(w.block == 'S15-C') & (w.group == 'PSLN-344') & (w.x.between(2, 12))].set_index(['col', 'x']).value
    tb_ = w[(w.block == 'S15-I') & (w.group == '3d Vaccine+PSLN-344') & (w.x.between(2, 12))].set_index(['col', 'x']).value
    n_same = int((ta == tb_.reindex(ta.index)).sum()); n_all = len(ta)
    ax.set_xlabel('Days after challenge'); ax.set_ylabel('Body weight (% of day 0)'); ax.legend(frameon=False, loc='lower left', fontsize=6.5)
    ax.set_title(f'c  D7: two experiments share seven animals\n    ({n_same} of {n_all} values, day 2 to 12, identical)', loc='left')
    ax = axs[1, 1]; ax.axis('off')
    rows = []
    for g, gl in [('Sham', 'Vehicle'), ('PSLN-212', 'PSLN-212'), ('PSLN-344', 'PSLN-344'), ('PSLN-212(Y)', 'Young')]:
        c = sv[(sv.block == 'S06-C') & (sv.group == g)]; d = sv[(sv.block == 'S06-D') & (sv.group == g)]
        def fmt(t):
            if (t.event == 0).all(): return 'none'
            return ', '.join(str(int(x)) for x in t[t.event == 1].value)
        rows.append([gl, fmt(c), fmt(d)])
    tb = ax.table(cellText=rows, colLabels=['Group', 'S06-C', 'S06-D'], loc='upper center', cellLoc='left', colWidths=[0.2, 0.4, 0.4], bbox=[0.0, 0.38, 0.97, 0.56])
    tb.auto_set_font_size(False); tb.set_fontsize(6.5)
    for (r, c), cell in tb.get_celld().items():
        cell.set_edgecolor('#cccccc'); cell.set_linewidth(0.6)
        if r == 0: cell.set_facecolor('#eeeeee'); cell.set_text_props(fontweight='bold')
    ax.set_title('d  D1: two studies, one survival table\n    (days on which animals died)', loc='left')
    ax.text(0.0, 0.30, 'S06-C: challenge on day 14. S06-D: challenge on day 3.\nSeven animals per group. The weight block of S06-D\n(S15-D) shows two deaths on PSLN-344 and two in young\nanimals, so it does not match this table.', fontsize=6.6, transform=ax.transAxes, color='#b00020', va='top', linespacing=1.3)
    fig.savefig(OUT + 'fig6_record_defects.png'); plt.close(fig)

# ------------------------------------------------------------------ Figure 7: durability / background
def fig_durability():
    D = pd.read_csv(T + 'T8_durability_background.csv'); order = [0, 2, 3, 4, 5]
    labs = ['PSLN-344 aged,\nchallenged day 14', 'PSLN-344 aged,\nchallenged day 60', 'Aged, untreated,\nNOT challenged\n(same 14-day window)', 'PSLN-212 young,\nchallenged day 60', 'PSLN-212 aged,\nchallenged day 60']
    cols = ['#0072B2', '#0072B2', '#555555', '#009E73', '#E69F00']
    fig = plt.figure(figsize=(5.6, 3.0)); ax = fig.add_axes([0.1, 0.24, 0.88, 0.66])
    for k, i in enumerate(order):
        r = D.iloc[i]; ax.bar(k, r.pct, color=cols[k], alpha=0.85 if k != 1 else 0.55, width=0.65); ax.errorbar(k, r.pct, yerr=[[r.pct - r.lo], [r.hi - r.pct]], color='k', capsize=2.5, lw=0.8)
        ax.text(k, 3 if r.pct > 20 else r.hi + 2, f'{int(r.survivors)}/{int(r.n)}', ha='center', va='bottom', color='w' if r.pct > 20 else 'k', fontweight='bold', fontsize=7.5)
    ax.set_xticks(range(5)); ax.set_xticklabels(labs, fontsize=6.6); ax.set_ylabel('Alive after 14 days of observation (%)'); ax.set_ylim(0, 108)
    ax.set_title('Day-60 protection cannot be separated from age-related deaths', loc='left')
    fig.savefig(OUT + 'fig7_durability_background.png'); plt.close(fig)

# ------------------------------------------------------------------ Figure 8: tolerability
def fig_tolerability():
    fig = plt.figure(figsize=(7.0, 5.6))
    ax = fig.add_axes([0.085, 0.585, 0.38, 0.355])
    w = df[df.block == 'S08-D'].copy(); w['x'] = w.x.astype(float)
    names = {'Vaccine': 'Vaccine alone (aged)', 'PSLN-212(Y)': 'PSLN-212 (young)', 'PSLN-212': 'PSLN-212 (aged)', 'CMP-204': 'CMP-204 (aged)', 'PSLN-344': 'PSLN-344 (aged)', 'PSLN-212/R848': 'PSLN-212/R848 (aged)'}
    for g in names:
        mm = w[w.group == g].groupby('x').value.agg(['mean', 'std'])
        ax.errorbar(mm.index, mm['mean'], yerr=mm['std'], color=COL[g], lw=1.7 if g in ('PSLN-344', 'PSLN-212/R848') else 0.9, marker='o', ms=2.2, capsize=1.5, label=names[g])
    ax.axhline(100, color='k', lw=0.4, ls=':'); ax.set_xlabel('Days after intranasal immunisation'); ax.set_ylabel('Body weight (% of day 0), mean ± SD')
    ax.legend(frameon=False, fontsize=6.2, loc='lower left', handlelength=1.5); ax.set_title('a  Weight after dosing [S08-D]', loc='left')
    ax = fig.add_axes([0.585, 0.585, 0.40, 0.355]); t = df[df.block == 'S10-A']
    for ai, a in enumerate(['Ifnb1', 'Tnf', 'Isg15']):
        for gi, g in enumerate(['PBS', 'Sham', 'PSLN-344', 'CT']):
            vv = t[(t.group == g) & t.analyte.str.contains(a)].value.to_numpy(); x = ai * 5 + gi
            ax.bar(x, vv.mean(), color={'PBS': '#cccccc', 'Sham': '#8c8c8c', 'PSLN-344': '#0072B2', 'CT': '#D55E00'}[g], width=0.8, label={'PBS': 'PBS', 'Sham': 'Vehicle', 'PSLN-344': 'PSLN-344', 'CT': 'Cholera toxin'}[g] if ai == 0 else None)
            ax.plot(np.full(len(vv), x) + np.linspace(-0.2, 0.2, len(vv)), vv, 'k.', ms=2.5)
    ax.set_xticks([1.5, 6.5, 11.5]); ax.set_xticklabels(['Ifnb1', 'Tnf', 'Isg15'], style='italic'); ax.set_ylabel('Brain transcript, fold vs untreated'); ax.legend(frameon=False, fontsize=6.4)
    ax.set_title('b  Brain transcripts at 36 h [S10-A]', loc='left')
    ax = fig.add_axes([0.085, 0.09, 0.9, 0.335])
    S = pd.read_csv(T + 'T9_group_summaries.csv'); S = S[S.block.str.startswith('S09-A')].copy(); S['an'] = S.analyte.str.split().str[0]
    gs = ['CMP-204', 'PSLN-212', 'PSLN-344', 'PSLN-212(y)', 'PSLN-212/R848']; ans = ['Ifnb1', 'Il6', 'Tnf', 'Il10', 'Ccl2', 'Ccl3', 'Ccl5']
    M = np.zeros((len(ans), 2 * len(gs)))
    for pi, blk in enumerate(['S09-A (cols A-U)', 'S09-A (cols X-AS)']):
        for gi, g in enumerate(gs):
            for ai, a in enumerate(ans): M[ai, pi * len(gs) + gi] = S[(S.block == blk) & (S.group == g) & (S.an == a)]['mean'].iloc[0]
    ax.imshow(M, cmap='YlOrRd', vmin=0, vmax=3.2, aspect='auto')
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            val = 10 ** M[i, j]; ax.text(j, i, f'{val:.0f}' if val >= 10 else f'{val:.1f}', ha='center', va='center', fontsize=6.6, color='w' if M[i, j] > 1.9 else 'k')
    short = {'CMP-204': 'CMP-204\n(aged)', 'PSLN-212': 'PSLN-212\n(aged)', 'PSLN-344': 'PSLN-344\n(aged)', 'PSLN-212(y)': 'PSLN-212\n(young)', 'PSLN-212/R848': 'PSLN-212/\nR848 (aged)'}
    ax.set_xticks(range(2 * len(gs))); ax.set_xticklabels([short[g] for g in gs] * 2, fontsize=6.3); ax.set_yticks(range(len(ans))); ax.set_yticklabels(ans, fontsize=7, style='italic')
    ax.axvline(len(gs) - 0.5, color='k', lw=1.0); ax.spines[:].set_visible(False); ax.tick_params(length=0)
    ax.text(2, -0.72, '16 h', ha='center', fontsize=7.2, fontweight='bold'); ax.text(7, -0.72, '72 h (panel printed "16h"; defect D6)', ha='center', fontsize=7.2, fontweight='bold')
    ax.set_title('c  Lung transcripts, geometric-mean fold vs untreated [S09-A]', loc='left', pad=15)
    fig.savefig(OUT + 'fig8_tolerability.png'); plt.close(fig)

# ------------------------------------------------------------------ Figure 9: dose response
def fig_dose():
    F = pd.read_csv(T + 'T14_dose_response_fit.csv'); d = df[df.block == 'S08-A'].copy(); d['dose'] = d.x.astype(float)
    fig = plt.figure(figsize=(6.2, 2.9)); ax = fig.add_axes([0.095, 0.16, 0.56, 0.74]); xx = np.logspace(0, np.log10(40), 100)
    for g in ['CMP-204', 'PSLN-212', 'PSLN-344']:
        t = d[d.group == g]; p = F[F.group == g].iloc[0]
        ax.plot(t.dose, t.value, 'o', color=COL[g], ms=3, alpha=0.8)
        ax.plot(xx, 1 + (p.Emax_fold - 1) * xx ** p.hill / (p.ED50_ug ** p.hill + xx ** p.hill), color=COL[g], lw=1.5, label=f'{g}\nmaximum {p.Emax_fold:.0f}-fold,\nhalf-maximal at {p.ED50_ug:.0f} µg')
    ax.axhspan(32.6, 62, color='#009E73', alpha=0.08); ax.text(1.05, 36.5, 'seen with protective regimens (≥ 32.6-fold; S01-A)', fontsize=6.2, color='#00664d')
    ax.axvline(20, color='k', lw=0.5, ls=':'); ax.text(20.8, 1.15, 'dose used in every\nchallenge study', fontsize=6.2, va='bottom')
    ax.set_xscale('log'); ax.set_yscale('log'); ax.set_xticks([1, 5, 10, 20, 40]); ax.set_xticklabels(['1', '5', '10', '20', '40']); ax.set_yticks([1, 3, 10, 30, 60]); ax.set_yticklabels(['1', '3', '10', '30', '60'])
    ax.minorticks_off(); ax.set_ylim(0.8, 62)
    ax.set_xlabel('Dose (µg per animal, intranasal)'); ax.set_ylabel('Lung Ifnb1 at 16 h (fold vs untreated)')
    ax.legend(frameon=False, fontsize=6.8, loc='center left', bbox_to_anchor=(1.02, 0.5), labelspacing=1.2); ax.set_title('Interferon dose-response [S08-A], n = 3 per dose', loc='left')
    fig.savefig(OUT + 'fig9_dose_response.png'); plt.close(fig)

if __name__ == '__main__':
    import os, glob
    for f in glob.glob(OUT + '*.png'): os.remove(f)
    fig_survival_table(); fig_km(); fig_restoration(); fig_plan(); fig_mechanism(); fig_defects(); fig_durability(); fig_tolerability(); fig_dose()
    from PIL import Image
    for f in sorted(glob.glob(OUT + '*.png')):
        im = Image.open(f); print(os.path.basename(f), im.size, f'{im.size[0]/250:.2f} x {im.size[1]/250:.2f} in')
