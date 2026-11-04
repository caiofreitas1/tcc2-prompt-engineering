import csv,collections,glob,math,sys
import xml.etree.ElementTree as E
sys.path.insert(0,'scripts')
from analisar_piloto import tarefa_no_titulo
reg=list(csv.DictReader(open('dados/registros.csv')))
est={e['id']:e for e in csv.DictReader(open('dados/estudos.csv'))}
por=collections.defaultdict(list)
for r in reg: por[r['estudo_id']].append(r)
n={'a':'http://www.w3.org/2005/Atom','x':'http://arxiv.org/schemas/atom'}
pub=set()
for p in glob.glob('dados/brutos/arxiv-2026-10-29/pagina-*.xml'):
    for e in E.parse(p).getroot().findall('a:entry',n):
        if e.find('x:journal_ref',n) is not None or e.find('x:doi',n) is not None:
            pub.add(e.find('a:id',n).text.split('/abs/')[1].split('v')[0])
cand=[i for i,e in est.items() if e['corpus']=='candidato']
def P(i):
    return any(r['busca_id'] in('B2','B3') or r['arxiv'] in pub or r['doi'] for r in por[i])
def T(i): return tarefa_no_titulo(est[i]['titulo'])
def A(i): return est[i]['acesso_aberto']=='sim'
S=[]
for k in (1,2):
    for x in csv.DictReader(open(f'evidencias/piloto/comparacao-amostra-{k}.csv')):
        x['am']=k; S.append(x)
def Wil(k,n,z=1.96):
    p=k/n;d=1+z*z/n;c=p+z*z/(2*n);h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n));return (c-h)/d,(c+h)/d
cen={'T (titulo)':lambda i:T(i),'P (indicio revisao)':lambda i:P(i),'P e aberto':lambda i:P(i) and A(i),'T e P':lambda i:T(i) and P(i),'T e P e aberto':lambda i:T(i) and P(i) and A(i),'T ou (P e aberto)':lambda i:T(i) or (P(i) and A(i)),'Tudo':lambda i:True}
inc=[x for x in S if x['autor']=='incluir']
print('incluir autor total',len(inc))
fat=10/12+.2*2/12
for nome,f in cen.items():
    N=sum(1 for i in cand if f(i))
    sub=[x for x in S if f(x['estudo_id'])]
    seg=sum(x['uniao']=='segue' for x in sub)
    ki=sum(1 for x in inc if f(x['estudo_id']))
    ft=N*seg/len(sub)
    h=ft*fat*3/60+1.3
    pct=ft*.25
    ta=(N-sum(1 for x in S if f(x['estudo_id'])))*0.0155
    lo,hi=Wil(seg,len(sub))
    print(f"{nome:22s} N={N:5d} amostra={len(sub):3d} seguem={seg:3d} ({seg/len(sub):.2f}; IC {lo:.2f}-{hi:.2f}) incluir_mantidos={ki}/{len(inc)} ({ki/len(inc):.0%}) FT={ft:6.0f} h_autor={h:5.1f} lim_FT={pct:5.0f}% lim_TA={ta:4.0f}% corpus~{ft*9/12:5.0f}")
print('so arXiv sem indicio',sum(1 for i in cand if not P(i)))
print('P sem aberto',sum(1 for i in cand if P(i) and not A(i)))
print('P: por base',collections.Counter(tuple(sorted({r['busca_id'] for r in por[i]})) for i in cand if P(i)))
print('losses sample1 under',{nome:[x['estudo_id'] for x in inc if x['uniao']=='sai' and f(x['estudo_id'])] for nome,f in cen.items()})
anos=collections.Counter()
for i in cand:
    if not P(i): anos[por[i][0]['ano']]+=1
print('so arXiv por ano',sorted(anos.items()))
pa=collections.Counter(por[i][0]['ano'] for i in cand if P(i)); print('P por ano',sorted(pa.items()))

print('=== com Semantic Scholar')
import json,re
s2={}
try:
    for l in open(sys.argv[1],encoding='utf-8'):
        o=json.loads(l); s2[o['arxiv']]=o['r']
except IndexError: pass
PRE=re.compile(r'arxiv|corr\b|preprint|biorxiv|techrxiv|ssrn|research square|authorea',re.I)
def venue(r):
    if not r: return None
    v=(r.get('venue') or '').strip()
    pv=(r.get('publicationVenue') or {}).get('name') or ''
    j=(r.get('journal') or {}).get('name') or ''
    ext=r.get('externalIds') or {}
    doi=(ext.get('DOI') or '')
    nomes=[x for x in (v,pv,j) if x and not PRE.search(x)]
    if nomes: return nomes[0]
    if doi and not doi.lower().startswith('10.48550'): return 'doi:'+doi
    return None
V={i:venue(r) for i,r in s2.items()}
print('ids',len(s2),'com resposta',sum(1 for r in s2.values() if r),'com venue',sum(1 for v in V.values() if v))
sem=[i for i in cand if not P(i)]
novo=[i for i in sem if any(V.get(r['arxiv']) for r in por[i])]
print('so arXiv sem indicio',len(sem),'com venue S2',len(novo),'restam',len(sem)-len(novo))
print('exemplos',[V.get(por[i][0]['arxiv'])[:50] for i in novo[:12]])
print(collections.Counter(V.get(por[i][0]['arxiv'])[:30] for i in novo).most_common(14))
def P2(i): return P(i) or i in set_novo
set_novo=set(novo)
cen2={'P2 (indicio ampliado)':P2,'P2 e aberto':lambda i:P2(i) and A(i),'T e P2':lambda i:T(i) and P2(i),'T e P2 e aberto':lambda i:T(i) and P2(i) and A(i),'T ou (P2 e aberto)':lambda i:T(i) or (P2(i) and A(i)),'T':T}
for nome,f in cen2.items():
    N=sum(1 for i in cand if f(i)); sub=[x for x in S if f(x['estudo_id'])]; seg=sum(x['uniao']=='segue' for x in sub); ki=sum(1 for x in inc if f(x['estudo_id']))
    ft=N*seg/len(sub); lo,hi=Wil(seg,len(sub)); 
    print(f"{nome:22s} N={N:5d} amostra={len(sub):3d} seguem={seg:3d} ({seg/len(sub):.2f}; {lo:.2f}-{hi:.2f}) incl={ki}/79 ({ki/79:.0%}) FT={ft:6.0f} ({N*lo:.0f}-{N*hi:.0f}) h={ft*fat*3/60+1.3:5.1f} lim_FT={ft*.25:5.0f}% lim_TA={N*.0155:4.0f}% corpus~{ft*.75:5.0f}")
print('12 medicao', {x:(P2(x),T(x)) for x in 'S213 S430 S448 S2261 S508 S427 S149 S1584 S619 S2128 S1539 S306'.split()})
print('aberto na P2',sum(1 for i in cand if P2(i) and A(i)),'P2 sem aberto',sum(1 for i in cand if P2(i) and not A(i)))
print('so ACM sem arxiv',sum(1 for i in cand if {r['busca_id'] for r in por[i]}=={'B3'}), 'so IEEE',sum(1 for i in cand if {r['busca_id'] for r in por[i]}=={'B2'}), 'so IEEE aberto',sum(1 for i in cand if {r['busca_id'] for r in por[i]}=={'B2'} and A(i)))
