import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
COL = {'PSLN-344': '#0072B2', 'PSLN-212': '#D55E00', 'Sham': '#8A8A8A', 'PSLN-212(Y)': '#009E73', 'CMP-204': '#CC79A7',
       'PSLN-344(Y)': '#56B4E9', 'PSLN-212/R848': '#B8860B', 'PSLN-R848': '#E69F00', 'Vaccine': '#8A8A8A', 'Untreated': '#444444', 'PBS': '#BBBBBB', 'CT': '#000000'}
NICE = {'PSLN-344': 'PSLN-344 (aged)', 'PSLN-212': 'PSLN-212 (aged)', 'Sham': 'Sham: vaccine + empty liposome (aged)', 'PSLN-212(Y)': 'PSLN-212 (young benchmark)',
        'CMP-204': 'CMP-204 (cGAMP, aged)'}
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'axes.titlesize': 10, 'axes.labelsize': 9, 'xtick.labelsize': 8, 'ytick.labelsize': 8,
                     'legend.fontsize': 8, 'axes.spines.top': False, 'axes.spines.right': False, 'figure.dpi': 110, 'savefig.dpi': 220,
                     'axes.titleweight': 'bold', 'axes.titlelocation': 'left'})
FIGDIR = '/tmp/outputs/figures/'
