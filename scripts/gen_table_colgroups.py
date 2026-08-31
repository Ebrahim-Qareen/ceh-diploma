import io,os,re,html,math
# Regenerates the per-table <colgroup> plan for every session page.
# Idempotent: drops any existing plan first, then recomputes from the table's
# own content. Run from the repo root after adding or editing a table.
#   python3 scripts/gen_table_colgroups.py
BASE=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'docs')
import glob
FILES=sorted(os.path.relpath(f,BASE) for f in glob.glob(os.path.join(BASE,'session-*','index.html')))
TABLE=re.compile(r'(<table\b[^>]*>)(.*?)(</table>)',re.S)
ROW=re.compile(r'<tr\b[^>]*>(.*?)</tr>',re.S)
CELL=re.compile(r'<(th|td)\b([^>]*)>(.*?)</\1>',re.S)
TAGS=re.compile(r'<[^>]+>')
CG=re.compile(r'<colgroup>.*?</colgroup>',re.S)
LONG=55; MINPX=190; BASEMW=660; CAPMW=1180

def tlen(f):
    return len(' '.join(html.unescape(TAGS.sub(' ',f)).split()))

def plan(body):
    rows=[]
    for r in ROW.findall(body):
        cells=CELL.findall(r)
        if not cells or any('colspan' in a.lower() for _,a,_ in cells): continue
        rows.append([(t,tlen(i)) for t,_,i in cells])
    if not rows: return None,None
    n=max(len(r) for r in rows); rows=[r for r in rows if len(r)==n]
    if not rows or n<2: return None,None
    head=[0.0]*n; avg=[[] for _ in range(n)]; mx=[0.0]*n; has_long=[False]*n
    for r in rows:
        header_row = all(t=='th' for t,_ in r)
        for i,(t,L) in enumerate(r):
            if header_row: head[i]=max(head[i],L)
            else:
                avg[i].append(L); mx[i]=max(mx[i],L)
                if L>LONG: has_long[i]=True
    w=[]
    for i in range(n):
        a=sum(avg[i])/len(avg[i]) if avg[i] else 0.0
        # a single long outlier must still earn width — max-aware, not just mean
        w.append(max(a, head[i]*0.85, mx[i]*0.45, 4.0))
    p=[x**0.62 for x in w]; tot=sum(p); pct=[100.0*x/tot for x in p]
    FLOOR=max(6.0,min(11.0,44.0/n)); CAP=62.0
    for _ in range(14):
        pct=[min(CAP,max(FLOOR,x)) for x in pct]; t=sum(pct)
        if abs(t-100.0)<0.01: break
        free=[i for i,x in enumerate(pct) if FLOOR<x<CAP]
        if not free: break
        d=(100.0-t)/len(free)
        for i in free: pct[i]+=d
    r=[int(round(x)) for x in pct]; r[r.index(max(r))]+=100-sum(r)
    # this table's own min-width: whatever makes every prose column >= MINPX
    need=BASEMW
    for i in range(n):
        if has_long[i] and r[i]>0:
            need=max(need, math.ceil(MINPX*100.0/r[i]))
    need=min(need,CAPMW)
    return ''.join('<col style="width:%d%%">'%x for x in r), (need if need>BASEMW else None)

for f in FILES:
    p=os.path.join(BASE,f); s=io.open(p,encoding='utf-8').read(); n=[0]; widened=[0]
    def sub(m):
        open_,body,close=m.groups()
        body=CG.sub('',body)                                  # idempotent: drop old plan
        open_=re.sub(r'\s*style="min-width:\d+px"','',open_)
        cg,mw=plan(body)
        if not cg: return open_+body+close
        n[0]+=1
        if mw:
            widened[0]+=1
            open_=open_[:-1]+' style="min-width:%dpx">'%mw
        return '%s<colgroup>%s</colgroup>%s%s'%(open_,cg,body,close)
    s=TABLE.sub(sub,s)
    io.open(p,'w',encoding='utf-8',newline='').write(s)
    print('%-24s colgroups=%-3d widened=%d'%(f,n[0],widened[0]))
