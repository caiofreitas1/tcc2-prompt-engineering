import csv,json,glob,time,sys,urllib.request,collections
import xml.etree.ElementTree as E
sc=sys.argv[1]
reg=list(csv.DictReader(open('dados/registros.csv')))
est={e['id']:e for e in csv.DictReader(open('dados/estudos.csv'))}
ids=sorted({r['arxiv'] for r in reg if r['busca_id']=='B1' and r['arxiv'] and est[r['estudo_id']]['corpus']=='candidato'})
print(len(ids),'ids arXiv')
out=open(sc+'/s2.jsonl','w',encoding='utf-8')
url='https://api.semanticscholar.org/graph/v1/paper/batch?fields=venue,publicationVenue,publicationTypes,journal,externalIds'
ok=0
for k in range(0,len(ids),400):
    lote=ids[k:k+400]
    for t in range(6):
        try:
            rq=urllib.request.Request(url,data=json.dumps({'ids':['ARXIV:'+i for i in lote]}).encode(),headers={'Content-Type':'application/json'})
            r=json.load(urllib.request.urlopen(rq,timeout=60))
            for i,x in zip(lote,r): out.write(json.dumps({'arxiv':i,'r':x},ensure_ascii=False)+'\n'); ok+=x is not None
            break
        except Exception as e:
            print('retry',k,t,e,flush=True); time.sleep(8*(t+1))
    time.sleep(2)
print('respostas',ok)
