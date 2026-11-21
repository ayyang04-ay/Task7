"""Approximate PDF -> PNG preview built from the actual PDF content stream (text positions, rules, fills, images),
for layout QA in an environment with no PDF rasteriser. Uses pypdf visitors + PIL."""
import sys, io, os
from pypdf import PdfReader
from PIL import Image, ImageDraw, ImageFont
FD = '/opt/conda/envs/core/lib/python3.11/site-packages/matplotlib/mpl-data/fonts/ttf/'
FONTS = {'DejaVuSans-Bold':'DejaVuSans-Bold.ttf','DejaVuSans-Oblique':'DejaVuSans-Oblique.ttf','DejaVuSans-BoldOblique':'DejaVuSans-BoldOblique.ttf','DejaVuSansMono':'DejaVuSansMono.ttf','DejaVuSans':'DejaVuSans.ttf'}
_cache = {}
def font(base, size_px):
    key = 'DejaVuSans'
    for k in ['DejaVuSans-BoldOblique','DejaVuSans-Bold','DejaVuSans-Oblique','DejaVuSansMono','DejaVuSans']:
        if base.endswith(k): key = k; break
    sz = max(4.0, round(float(size_px), 2))
    if (key, sz) not in _cache: _cache[(key, sz)] = ImageFont.truetype(FD+FONTS[key], sz)
    return _cache[(key, sz)]
def mul(m, n):  # m then n  (row-vector convention: [a b c d e f])
    a,b,c,d,e,f = m; A,B,C,D,E,F = n
    return [a*A+b*C, a*B+b*D, c*A+d*C, c*B+d*D, e*A+f*C+E, e*B+f*D+F]
def apply(m, x, y): return (m[0]*x + m[2]*y + m[4], m[1]*x + m[3]*y + m[5])

def render(pdf, outdir, dpi=120, pages=None, ss=3):
    os.makedirs(outdir, exist_ok=True)
    r = PdfReader(pdf); sc = ss*dpi/72.0; outs = []
    for pi, page in enumerate(r.pages):
        if pages and (pi+1) not in pages: continue
        W = float(page.mediabox.width); H = float(page.mediabox.height)
        im = Image.new('RGB', (int(W*sc), int(H*sc)), 'white'); dr = ImageDraw.Draw(im)
        P = lambda x, y: (x*sc, (H-y)*sc)
        imgs = {}
        try:
            for x in page.images: imgs[x.name.rsplit('.', 1)[0]] = x.data
        except Exception as e: pass
        state = dict(fill=(0,0,0), stroke=(0,0,0), lw=1.0); stack = []
        path = []; cur = None; rects = []
        texts = []
        def col(args): 
            v = [float(a) for a in args]
            if len(v) == 1: v = v*3
            return tuple(int(255*max(0,min(1,c))) for c in v[:3])
        def before(op, args, cm, tm):
            nonlocal path, cur, rects
            op = op.decode() if isinstance(op, bytes) else op
            if op == 'q': stack.append(dict(state))
            elif op == 'Q':
                if stack: state.update(stack.pop())
            elif op in ('rg','g'): state['fill'] = col(args)
            elif op in ('RG','G'): state['stroke'] = col(args)
            elif op == 'w': state['lw'] = float(args[0])
            elif op == 're':
                x,y,w,h = [float(a) for a in args]; rects.append([apply(cm,x,y), apply(cm,x+w,y+h)])
            elif op == 'm': cur = apply(cm, float(args[0]), float(args[1])); path.append([cur])
            elif op == 'l':
                if path: path[-1].append(apply(cm, float(args[0]), float(args[1])))
            elif op in ('S','s','f','F','f*','B','B*','b','n'):
                if op in ('f','F','f*','B','B*','b'):
                    for (a,b) in rects:
                        x0,y0 = P(*a); x1,y1 = P(*b); dr.rectangle([min(x0,x1),min(y0,y1),max(x0,x1),max(y0,y1)], fill=state['fill'])
                if op in ('S','s','B','B*','b'):
                    for (a,b) in rects:
                        x0,y0 = P(*a); x1,y1 = P(*b); dr.rectangle([min(x0,x1),min(y0,y1),max(x0,x1),max(y0,y1)], outline=state['stroke'])
                    for seg in path:
                        if len(seg) >= 2: dr.line([P(*p) for p in seg], fill=state['stroke'], width=max(1,int(round(state['lw']*sc))))
                path = []; rects = []
            elif op == 'Do':
                name = str(args[0]).lstrip('/')
                x0,y0 = apply(cm,0,0); x1,y1 = apply(cm,1,1)
                px0,py0 = P(x0,y1); px1,py1 = P(x1,y0)
                w = max(1,int(px1-px0)); h = max(1,int(py1-py0))
                if name in imgs:
                    try:
                        sub = Image.open(io.BytesIO(imgs[name])).convert('RGB').resize((w,h)); im.paste(sub, (int(px0), int(py0)))
                    except Exception as e: dr.rectangle([px0,py0,px1,py1], outline=(200,0,0))
                else: dr.rectangle([px0,py0,px1,py1], outline=(200,0,0))
        last = dict(x=None, y=None, adv=0.0)
        def vt(text, cm, tm, fd, fs):
            if not text or not text.strip('\n'): return
            m = mul(tm, cm); x, y = m[4], m[5]
            base = str(fd.get('/BaseFont','')) if fd else ''
            size = fs*abs(m[3]) if m[3] else fs
            t = text.rstrip('\n')
            if last['x'] is not None and abs(last['x']-x) < 0.01 and abs(last['y']-y) < 0.01:
                xx = x + last['adv']          # same text origin: continue on the same line after the previous run
            else:
                xx = x; last['adv'] = 0.0; last['x'] = x; last['y'] = y
            w = font(base, 100).getlength(t) * size / 100.0
            last['adv'] += w
            texts.append((t, xx, y, size, base, state['fill']))
        page.extract_text(visitor_operand_before=before, visitor_text=vt)
        for text, x, y, fs, base, colr in texts:
            f = font(base, fs*sc); px, py = P(x, y)
            dr.text((px, py - fs*sc*0.93), text, font=f, fill=colr)
        im = im.resize((im.width//ss, im.height//ss), Image.LANCZOS)
        out = os.path.join(outdir, f'page_{pi+1:02d}.png'); im.save(out); outs.append(out)
    return outs
if __name__ == '__main__':
    pages = [int(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else None
    for o in render(sys.argv[1], sys.argv[2], pages=pages): print(o)
