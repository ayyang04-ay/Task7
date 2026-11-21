"""Print the self-contained HTML proposal to a paginated, text-searchable PDF with the headless Chromium that ships inside
kaleido 0.2.1 (conda env "genomics"), then report what landed on each page.  Optional: PNG screenshots for layout checks.

usage:  make_pdf.py <in.html> <out.pdf> [--shots DIR]
"""
import sys, re, os, json
from kaleido.scopes.plotly import PlotlyScope
HERE = os.path.dirname(os.path.abspath(__file__))
PRINT_CSS = '''
@page { size: 8.5in 11in; margin: 0.7in 0.72in 0.75in 0.72in; }
.docbody { max-width: none !important; margin: 0 !important; padding: 0 !important; font-size: 9.5pt !important; line-height: 1.36 !important; }
h1 { font-size: 19pt !important; margin-top: 0 !important; }
h2 { font-size: 14.5pt !important; margin-top: 18px !important; } h3 { font-size: 11.5pt !important; margin-top: 14px !important; }
h2, h3, p.label { page-break-inside: avoid; break-inside: avoid; }
h2::after, h3::after, p.label::after { content: ""; display: block; height: 150px; margin-bottom: -150px; }      /* keep a heading with what follows */
.keep { page-break-inside: avoid; break-inside: avoid; }
table { font-size: 7.9pt !important; margin: 6px 0 10px 0 !important; } th, td { padding: 3px 5px !important; }
tr { page-break-inside: avoid; break-inside: avoid; } thead { display: table-header-group; }
figure { page-break-inside: avoid; break-inside: avoid; margin: 4px 0 8px 0 !important; }
img { max-width: 100% !important; max-height: 8.7in; width: auto; display: block; margin: 0 auto !important; }
figcaption { font-size: 8.2pt !important; margin-bottom: 4px !important; } code { font-size: 8.2pt !important; }
p { margin: 6px 0 !important; orphans: 2; widows: 2; } ul, ol { margin: 5px 0 !important; } hr { margin: 12px 0 !important; }
'''
def load(path, for_print):
    h = open(path, encoding='utf-8').read()
    styles = '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', h, re.S))
    styles = re.sub(r'(^|\})\s*body\s*\{', r'\1 .docbody {', styles)
    body = re.search(r'<body[^>]*>(.*)</body>', h, re.S).group(1)
    if for_print:
        # keep a heading together with a figure or paragraph that follows it directly
        body = re.sub(r'(<h[23][^>]*>(?:(?!</h[23]>).)*</h[23]>)\s*(<figure>(?:(?!</figure>).)*</figure>|<p>(?:(?!</p>).)*</p>)', r'<div class="keep">\1\2</div>', body, flags=re.S)
        # short tables stay on one page
        def small_table(m):
            t = m.group(0)
            return t.replace('<table', '<table class="keep"', 1) if (t.count('<tr') <= 11 and len(re.sub(r'<[^>]+>', '', t)) < 1500) else t
        body = re.sub(r'<table(?:(?!</table>).)*</table>', small_table, body, flags=re.S)
        # a bold one-line label stays with the list or table it introduces
        body = re.sub(r'<p>(<strong>[^<]*</strong>)</p>', r'<p class="label">\1</p>', body)
        # ... and a heading or label moves together with a short table that follows it
        body = re.sub(r'(<h[23][^>]*>(?:(?!</h[23]>).)*</h[23]>|<p class="label">(?:(?!</p>).)*</p>)\s*(<table class="keep"(?:(?!</table>).)*</table>)', r'<div class="keep">\1\2</div>', body, flags=re.S)
        styles += PRINT_CSS
    return f'<style>{styles}</style><div class="docbody">{body}</div>'
def main():
    src, out = sys.argv[1], sys.argv[2]
    scope = PlotlyScope(plotlyjs=os.path.join(HERE, 'html_via_kaleido.js'))
    fig = {'data': [], 'layout': {'meta': {'key': 'pdf', 'html': load(src, True), 'mode': 'pdf'}}}
    pdf = scope.transform(fig, format='pdf', width=816, height=1056, scale=1)      # 8.5 x 11 in at 96 px/in
    open(out, 'wb').write(pdf)
    import pypdf
    r = pypdf.PdfReader(out)
    print(f'{out}: {len(r.pages)} pages, {len(pdf)/1e6:.1f} MB, page size {float(r.pages[0].mediabox.width)/72:.1f} x {float(r.pages[0].mediabox.height)/72:.1f} in')
    for i, p in enumerate(r.pages):
        xs, ys = [], []
        def visitor(text, cm, tm, fd, fs):
            if text.strip(): xs.append(tm[4] * cm[0] + tm[5] * cm[2] + cm[4]); ys.append(tm[4] * cm[1] + tm[5] * cm[3] + cm[5])
        t = [l for l in p.extract_text(visitor_text=visitor).split('\n') if l.strip()]
        print(f'  p{i+1:2d}: left margin {min(xs)/72:.2f} in, top {(792-max(ys))/72:.2f} in, lowest text {min(ys)/72:.2f} in, images {len(p.images)} | first: {t[0][:46]!r} | last: {t[-1][:46]!r}')
    if '--preview' in sys.argv:      # the print styling rendered on screen at the printed text width (678 px = 7.06 in), for a visual check
        d = sys.argv[sys.argv.index('--preview') + 1]; os.makedirs(d, exist_ok=True)
        W, CH = 678, 1000
        fig = {'data': [], 'layout': {'meta': {'key': 'preview', 'html': load(src, True), 'mode': 'measure', 'selector': 'h2'}}}
        m = json.loads(scope.transform(fig, format='png', width=W, height=CH, scale=1))
        offs = range(0, m['totalHeight'], CH) if '--preview-offsets' not in sys.argv else [int(x) for x in sys.argv[sys.argv.index('--preview-offsets') + 1].split(',')]
        for off in offs:
            fig['layout']['meta'].update(mode='shot', offset=off)
            open(os.path.join(d, f'preview_{off:06d}.png'), 'wb').write(scope.transform(fig, format='png', width=W, height=CH, scale=2))
        print('print-style preview written to', d, '(total height', m['totalHeight'], 'px)')
    if '--shots' in sys.argv:
        d = sys.argv[sys.argv.index('--shots') + 1]; os.makedirs(d, exist_ok=True)
        W, CH = 1128, 1500
        fig = {'data': [], 'layout': {'meta': {'key': 'screen', 'html': load(src, False), 'mode': 'measure', 'selector': 'h2'}}}
        m = json.loads(scope.transform(fig, format='png', width=W, height=CH, scale=1))
        for off in range(0, m['totalHeight'], CH):
            fig['layout']['meta'].update(mode='shot', offset=off)
            open(os.path.join(d, f'screen_{off:06d}.png'), 'wb').write(scope.transform(fig, format='png', width=W, height=CH, scale=1))
        print('screenshots written to', d)
if __name__ == '__main__':
    main()
