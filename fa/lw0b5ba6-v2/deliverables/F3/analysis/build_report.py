"""build_report.py - renders the proposal (Markdown -> DOCX via pandoc) from the fact registry.
Every {{key}} in the text is replaced by FACTS[key]['text'] and logged for Appendix A.
Run:  micromamba run -n core python build_report.py   (then pandoc is called from the renv environment)"""
import re, json, textwrap, subprocess, os, sys
import numpy as np
from facts import FACTS, B, G
from integrity_log import LOG, DESIGN_LIMITS

USED = []          # keys in order of first use
def fact(key):
    if key not in FACTS: raise KeyError(f'unknown fact {key}')
    if key not in USED: USED.append(key)
    return FACTS[key]['text']
def sub(text):
    return re.sub(r'\{\{([\w\-\.]+)\}\}', lambda m: fact(m.group(1)), text)

# ------------------------------------------------------------------ pandoc grid tables
def _wrap_cell(text, width):
    out = []; prev_bullet = None
    for para in str(text).split('\n'):
        para = para.rstrip()
        if not para:
            out.append(''); prev_bullet = None; continue
        m = re.match(r'^(\d+\.|-)\s+', para)
        if m:
            ind = ' ' * len(m.group(0))
            if prev_bullet is False: out.append('')
            lines = textwrap.wrap(para, width=width, subsequent_indent=ind, break_long_words=False, break_on_hyphens=False)
            prev_bullet = True
        else:
            if prev_bullet is not None: out.append('')
            lines = textwrap.wrap(para, width=width, break_long_words=False, break_on_hyphens=False)
            prev_bullet = False
        out.extend(lines)
    return out or ['']
def grid(headers, rows, widths):
    assert len(headers) == len(widths)
    rows = [[sub(str(c)) for c in r] for r in rows]; headers = [sub(h) for h in headers]
    def line(ch='-'): return '+' + '+'.join(ch * (w + 2) for w in widths) + '+'
    def render(cells):
        wrapped = [_wrap_cell(c, w) for c, w in zip(cells, widths)]
        for col, w in zip(wrapped, widths):
            for ln in col:
                assert len(ln) <= w, (w, ln)
        h = max(len(c) for c in wrapped); out = []
        for i in range(h):
            out.append('| ' + ' | '.join((c[i] if i < len(c) else '').ljust(w) for c, w in zip(wrapped, widths)) + ' |')
        return out
    out = [line()] + render(headers) + [line('=')]
    for r in rows:
        assert len(r) == len(widths), r
        out += render(r) + [line()]
    return '\n'.join(out) + '\n'
PB = '\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n'
def fig(n, file, caption, width='6.7in'):
    return f'\n![**Figure {n}.** {sub(caption)}](/tmp/outputs/figures/{file}){{width={width}}}\n'
W = 118   # total character budget for table contents

# ------------------------------------------------------------------ biomarker separation flags
def gm(v): return float(np.exp(np.mean(np.log(np.asarray(v, float)))))
def separates(prot, unprot, higher=True):
    prot = np.asarray(prot, float); unprot = np.asarray(unprot, float)
    return bool(prot.min() > unprot.max()) if higher else bool(prot.max() < unprot.min())
def sep_static(bid, higher=True, hai=False):
    g = G(bid); f = (lambda v: [5 if x == 0 else x for x in v]) if hai else (lambda v: v)
    prot = f(g['PSLN-344']) + f(g['PSLN-212(Y)']); un = f(g['PSLN-212']) + (f(g['Sham']) if 'Sham' in g else [])
    return 'yes' if separates(prot, un, higher) else 'no'
def sep_tc(bid, t):
    g = G(bid); prot = g['PSLN-344'][t] + g['PSLN-212(Y)'][t]; un = g['PSLN-212'][t] + g['Sham'][t]
    return 'yes' if separates(prot, un) else 'no'
_q = {k: [a / b for a, b in zip(G('S13-A')[k], G('S13-B')[k])] for k in ['PSLN-212', 'PSLN-344', 'PSLN-212(Y)']}
SEP = dict(ifn=sep_static('S01-A_16h'), dc=sep_tc('S01-E', '4'), ccr7=sep_static('S02-A'), tfh=sep_static('S04-A_ICOShi'), tfr=sep_static('S04-B_Foxp3', higher=False), gc=sep_static('S03-K'),
           hai1=sep_static('S03-C', hai=True), hai3=sep_static('S03-G', hai=True), nt1=sep_static('S03-D'), nt3=sep_static('S03-H'),
           sub='yes' if separates(_q['PSLN-344'] + _q['PSLN-212(Y)'], _q['PSLN-212']) else 'no', ifng=sep_static('S05-F'), ifng60=sep_static('S05-G'), trm=sep_static('S05-I'),
           gmcsf='yes' if min(G('S02-F')['PSLN-344']['36h']) > max(G('S02-F')['PSLN-212']['36h'] + G('S02-F')['Sham']['36h']) else 'no')

exec(open('/tmp/outputs/analysis/report_text.py').read())     # defines build_markdown()

if __name__ == '__main__':
    md = build_markdown()
    left = re.findall(r'\{\{[^}]*\}\}', md)
    assert not left, left
    open('/tmp/outputs/analysis/proposal.md', 'w').write(md)
    json.dump(USED, open('/tmp/work/parsed/facts_used.json', 'w'), indent=1)
    print('markdown written;', len(USED), 'facts cited;', len(md.split()), 'words')
