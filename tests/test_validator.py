import unittest, tempfile, subprocess, os, json, shutil, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import validator

E = dict(os.environ, GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@t', GIT_COMMITTER_NAME='t', GIT_COMMITTER_EMAIL='t@t')

def sh(d,*a):
    subprocess.run(['git']+list(a), cwd=d, env=E, check=True, capture_output=True)

def cm(d,msg,name,txt):
    p=os.path.join(d,name); os.makedirs(os.path.dirname(p),exist_ok=True)
    open(p,'w').write(txt); sh(d,'add','-A'); sh(d,'commit','-m',msg)

def cfg(**k):
    b=dict(app='git-unlock',version='1.0.0',activated=True,release='v1.0.0',modules=['core','export'])
    b.update(k); return json.dumps(b,indent=2)

def build(tag='annotated', extra=None, dirty=False, branch='main', **k):
    d=tempfile.mkdtemp()
    sh(d,'init','-b','main')
    cm(d,'chore: estrutura inicial','app/config.json',cfg(activated=False,release=None,modules=['core']))
    for i,s in enumerate(validator.OK_SUBJ): cm(d,s,'f%d.txt'%i,str(i))
    for i,s in enumerate(extra or []): cm(d,s,'e%d.txt'%i,str(i))
    cm(d,'release: v1.0.0','app/config.json',cfg(**k))
    if tag=='annotated': sh(d,'tag','-a','v1.0.0','-m','release final com decisoes explicadas')
    if tag=='light': sh(d,'tag','v1.0.0')
    if dirty: open(os.path.join(d,'sujo.txt'),'w').write('x')
    if branch!='main': sh(d,'checkout','-b',branch)
    return d

class T(unittest.TestCase):
    def run_(self, **k):
        d=build(**k); self.addCleanup(shutil.rmtree,d,ignore_errors=True)
        return dict(validator.validar(d))

    def test_ok(self):
        self.assertTrue(all(self.run_().values()))
    def test_sem_tag(self):
        self.assertFalse(self.run_(tag=None)['tag_anotada'])
    def test_tag_leve(self):
        r=self.run_(tag='light'); self.assertFalse(r['tag_anotada']); self.assertFalse(r['tag_msg'])
    def test_decoy(self):
        self.assertFalse(self.run_(extra=['wip: experimento com cache'])['sem_lixo'])
    def test_sujo(self):
        self.assertFalse(self.run_(dirty=True)['limpo'])
    def test_branch(self):
        self.assertFalse(self.run_(branch='outra')['branch'])
    def test_versao(self):
        self.assertFalse(self.run_(version='1.0.0-rc.1')['config'])
    def test_modulos(self):
        self.assertFalse(self.run_(modules=['core'])['config'])
    def test_release_vazio(self):
        self.assertFalse(self.run_(release=None)['config'])

if __name__ == '__main__':
    unittest.main()
