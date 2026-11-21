"""Shared figure style.  Figures are drawn at their printed size (7.2 in wide) so that text stays legible on a Letter/A4 page."""
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
W = 7.2     # figure width in inches = printed text width
mpl.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 7, 'axes.titlesize': 7.4, 'axes.labelsize': 7, 'xtick.labelsize': 6.5, 'ytick.labelsize': 6.5,
    'legend.fontsize': 6.4, 'axes.spines.top': False, 'axes.spines.right': False, 'figure.dpi': 150, 'savefig.dpi': 300,
    'axes.titleweight': 'bold', 'axes.linewidth': 0.6, 'lines.linewidth': 1.3, 'figure.facecolor': 'white',
    'xtick.major.width': 0.6, 'ytick.major.width': 0.6, 'xtick.major.size': 2.5, 'ytick.major.size': 2.5, 'axes.labelpad': 2, 'axes.titlepad': 4,
    'legend.handlelength': 1.6, 'legend.borderaxespad': 0.3, 'legend.labelspacing': 0.3})
COL = {
    'Sham': '#8c8c8c', 'Vaccine': '#8c8c8c', 'PBS': '#bdbdbd', 'Naive': '#4d4d4d', 'Untreated': '#000000',
    'PSLN-212': '#e08214', 'PSLN-344': '#1b5fa7', 'PSLN-212(Y)': '#5aae61', 'PSLN-344(Y)': '#74add1',
    'PSLN-212Y': '#5aae61', 'PSLN-344Y': '#74add1', 'PSLN-212(y)': '#5aae61',
    'CMP-204': '#9970ab', 'CMP-204(Y)': '#c2a5cf', 'PSLN-R848': '#b2182b', 'PSLN-212/R848': '#d6604d', 'PSLN-344/R848': '#d6604d', 'CT': '#b2182b',
    '3d Vaccine': '#8c8c8c', '3d PSLN-344': '#74add1', '3d Vaccine+PSLN-344': '#1b5fa7',
    'Naive+PSLN-212': '#e08214', 'Imprinting+PSLN-212': '#fdb863', 'Naive+PSLN-344': '#1b5fa7', 'Imprinting+PSLN-344': '#74add1',
}
NICE = {'PSLN-212': 'PSLN-212, aged', 'PSLN-344': 'PSLN-344, aged', 'PSLN-212(Y)': 'PSLN-212, young', 'PSLN-344(Y)': 'PSLN-344, young',
        'PSLN-212Y': 'PSLN-212, young', 'PSLN-344Y': 'PSLN-344, young', 'PSLN-212(y)': 'PSLN-212, young',
        'Sham': 'Sham', 'Vaccine': 'Vaccine alone', 'Untreated': 'Untreated, no challenge', 'CMP-204': 'CMP-204 (cGAMP), aged', 'CMP-204(Y)': 'CMP-204, young'}
def nice(g):
    return NICE.get(g, g)
