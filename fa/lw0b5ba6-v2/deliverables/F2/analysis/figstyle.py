import matplotlib, os
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.titlesize':10,'axes.labelsize':9,'xtick.labelsize':8,'ytick.labelsize':8,
                     'legend.fontsize':8,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':150,'savefig.dpi':220,'axes.titleweight':'bold',
                     'axes.titlelocation':'left'})
COL = {'Sham':'#7f7f7f','PBS':'#7f7f7f','Vaccine':'#7f7f7f','PSLN-212':'#E69F00','PSLN-344':'#0072B2','PSLN-212(Y)':'#009E73','PSLN-344(Y)':'#56B4E9',
       'CMP-204':'#CC79A7','PSLN-212/R848':'#D55E00','PSLN-R848':'#b07aa1','CT':'#D55E00','Untreated':'#bbbbbb','PSLN-344/R848':'#D55E00'}
NAME = {'Sham':'Vaccine + empty liposome (aged)','PSLN-212':'PSLN-212 (aged)','PSLN-344':'PSLN-344 (aged)','PSLN-212(Y)':'PSLN-212 (young)','PSLN-344(Y)':'PSLN-344 (young)',
        'CMP-204':'CMP-204, cGAMP liposome (aged)','Vaccine':'Vaccine alone (aged)'}
OUT = os.path.join(os.environ.get('PSLN_OUT', '/tmp/outputs'), 'figures') + '/'
os.makedirs(OUT, exist_ok=True)
