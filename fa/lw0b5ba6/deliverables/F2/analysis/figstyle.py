import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
COL = {"Sham": "#7F7F7F", "PBS": "#7F7F7F", "Vaccine": "#7F7F7F", "PSLN-212": "#E69F00", "PSLN-344": "#0072B2", "PSLN-212(Y)": "#009E73",
       "PSLN-344(Y)": "#56B4E9", "CMP-204": "#CC79A7", "PSLN-R848": "#8C564B", "PSLN-212/R848": "#D55E00", "PSLN-344/R848": "#D55E00",
       "Untreated": "#000000", "CT": "#D55E00", "Naive": "#BBBBBB"}
LAB = {"Sham": "Sham (vaccine + empty liposome), aged", "PSLN-212": "PSLN-212 (CDN, no Mn), aged", "PSLN-344": "PSLN-344 (CDN + Mn), aged",
       "PSLN-212(Y)": "PSLN-212, young benchmark", "PSLN-344(Y)": "PSLN-344, young", "CMP-204": "CMP-204 (cGAMP liposome), aged",
       "Untreated": "Untreated, unchallenged, aged"}
def style():
    mpl.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9, "axes.spines.top": False,
                         "axes.spines.right": False, "legend.frameon": False, "legend.fontsize": 8, "xtick.labelsize": 8, "ytick.labelsize": 8,
                         "figure.dpi": 110, "savefig.dpi": 200, "axes.titleweight": "bold", "axes.titlelocation": "left"})
