import subprocess, json, os, sys
R = os.path.dirname(os.path.abspath(__file__))
OK_SUBJ = ["feat: adiciona modulo de exportacao","feat: habilita ativacao no config","chore: pronto para integracao"]
BAD_SUBJ = ["wip: experimento com cache","wip: tentativa abandonada de ativacao","feat: primeira tentativa de ativacao (descartada)"]
TAG='v1.0.0'
x = 0

def g(*a):
    try:
        p = subprocess.run(['git']+list(a), cwd=R, capture_output=True, text=True)
        if p.returncode != 0: return None
        return p.stdout.strip()
    except Exception:
        return None

def validar(r=None):
    global R, x
    if r: R=r
    out=[]
    if g('rev-parse','--is-inside-work-tree')!='true': return [('repo',False)]
    out.append(('branch', g('rev-parse','--abbrev-ref','HEAD')=='main'))
    out.append(('limpo', g('status','--porcelain')==''))
    s=(g('log','--format=%s','HEAD') or '').split('\n')
    out.append(('integrou', all(i in s for i in OK_SUBJ)))
    out.append(('sem_lixo', not any(i in s for i in BAD_SUBJ)))
    out.append(('release_commit', (g('log','-1','--format=%s') or '').startswith('release:')))
    c=None
    try: c=json.load(open(os.path.join(R,'app','config.json')))
    except Exception: pass
    ok = isinstance(c,dict) and c.get('activated') is True and c.get('version')=='1.0.0' and c.get('release')==TAG and set(['core','export']).issubset(set(c.get('modules') or []))
    out.append(('config', bool(ok)))
    conf=False
    for f in (g('ls-files') or '').split('\n'):
        try:
            for l in open(os.path.join(R,f),errors='ignore').read().split('\n'):
                if l.startswith('<'*7+' ') or l.startswith('>'*7+' '): conf=True
        except Exception: pass
    out.append(('sem_conflito', not conf))
    out.append(('tag_anotada', g('cat-file','-t','refs/tags/'+TAG)=='tag'))
    a=g('rev-parse',TAG+'^{commit}'); b=g('rev-parse','HEAD')
    out.append(('tag_no_head', a is not None and a==b))
    out.append(('tag_msg', g('cat-file','-t','refs/tags/'+TAG)=='tag' and len(g('tag','-l','--format=%(contents)',TAG) or '')>=10))
    x = len([q for q in out if q[1]])
    return out

if __name__ == '__main__':
    for n,k in validar(): print(n, k)
