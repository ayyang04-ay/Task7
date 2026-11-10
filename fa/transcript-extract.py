import json, glob, os, re
BASE='runs/Anton_4ce55343502b4d17b2182158ad6e4533_job_91694a59_2026-11-09'
def load(path):
    d=json.load(open(path))
    out=[]
    for ctx in d['contexts']:
        for el in ctx['conversation']['data']:
            for item in el['contents']:
                if not isinstance(item,dict): continue
                t=item.get('type')
                if t=='Text': out.append(('text',item.get('data') or ''))
                elif t=='Thinking': out.append(('thinking',item.get('data') or ''))
                elif t=='ToolUse':
                    out.append(('tooluse',json.dumps(item.get('data') or item.get('input') or '')))
                elif t=='ToolResult':
                    c=item.get('content')
                    s=''
                    if isinstance(c,list):
                        s=' '.join(x.get('data','') if isinstance(x,dict) else str(x) for x in c)
                    else: s=str(c)
                    out.append(('toolresult',s))
                else:
                    out.append((str(t).lower(), json.dumps(item)[:4000]))
    return out, d.get('thinking_summary_status')
def runs():
    for p in sorted(glob.glob(os.path.join(BASE,'transcripts','attempt_*.json'))):
        rid=re.search(r'attempt_(\d+)_([0-9a-f]+)\.json',p)
        yield rid.group(1), rid.group(2), p
if __name__=='__main__':
    print('%-4s %-10s %7s %7s %7s %7s %9s'%('att','id','elems','think','think+','tooluse','chars'))
    for n,rid,p in runs():
        els,st=load(p)
        th=[t for k,t in els if k=='thinking']
        thn=[t for t in th if t.strip()]
        print('%-4s %-10s %7d %7d %7d %7d %9d'%(n,rid,len(els),len(th),len(thn),
              sum(1 for k,_ in els if k=='tooluse'), sum(len(t) for _,t in els)))
