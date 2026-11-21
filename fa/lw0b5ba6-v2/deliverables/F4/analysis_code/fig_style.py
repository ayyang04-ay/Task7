import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
COL = {'Sham':'#7f7f7f', 'PSLN-212':'#E08214', 'PSLN-344':'#1F5FA8', 'PSLN-212(Y)':'#2E8B57', 'PSLN-344(Y)':'#7FB3E6', 'CMP-204':'#8E5BA8',
       'PSLN-212/R848':'#C0392B', 'PSLN-R848':'#E6A6A0', 'Untreated':'#B8860B', 'Vaccine':'#7f7f7f', 'PBS':'#BBBBBB', 'CT':'#000000', 'Naive':'#BBBBBB'}
LAB = {'Sham':'Aged + vaccine alone', 'PSLN-212':'Aged + PSLN-212', 'PSLN-344':'Aged + PSLN-344', 'PSLN-212(Y)':'Young + PSLN-212 (benchmark)',
       'PSLN-344(Y)':'Young + PSLN-344', 'CMP-204':'Aged + CMP-204 (cGAMP)', 'Untreated':'Aged, not challenged (background)'}
FIGW = 7.3   # inches: figures are designed at page width so text stays legible in print
plt.rcParams.update({'font.size': 7.5, 'axes.titlesize': 8.3, 'axes.labelsize': 7.5, 'legend.fontsize': 6.8, 'xtick.labelsize': 7, 'ytick.labelsize': 7,
                     'axes.spines.top': False, 'axes.spines.right': False, 'figure.dpi': 150, 'savefig.dpi': 220, 'font.family': 'DejaVu Sans',
                     'axes.linewidth': 0.7, 'xtick.major.width': 0.7, 'ytick.major.width': 0.7, 'lines.linewidth': 1.4})
import os
OUT = os.path.join(os.environ.get('PSLN_OUT', '/tmp/outputs'), 'figures', '')
os.makedirs(OUT, exist_ok=True)
