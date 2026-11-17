"""Gera o formulário de conferência humana das fichas ex-v2.2 a partir da amostra sorteada.

Cada ficha final entra com o hash do arquivo, as correções manuais vigentes e a
marcação das citações pelo verificador aproximado. Uso: python3 scripts/gerar_formulario_conferencia.py
"""
import csv, json, hashlib, sys, re
from pathlib import Path
R = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R / 'scripts'))
from verificar_citacoes_piloto import norm, toks, verif
from verificar_citacoes_aprox import indice, aprox, blocos, compacto

am = list(csv.DictReader(open(R / 'evidencias/extracao-v2.2/conferencia/amostra.csv', encoding='utf-8')))
es = {r['id']: r for r in csv.DictReader(open(R / 'dados/estudos.csv', encoding='utf-8'))}
man = {r['estudo_id']: r for r in csv.DictReader(open(R / 'evidencias/extracao-v2.2/rodadas/manifesto.csv', encoding='utf-8'))}
cor = {}
for l in open(R / 'evidencias/extracao-v2.2/correcoes-manuais.jsonl', encoding='utf-8'):
    c = json.loads(l)
    if not c.get('situacao'):
        cor.setdefault(c['estudo_id'], []).append({k: c.get(k) for k in ('campo', 'tecnica', 'valor_bruto', 'valor_final', 'motivo', 'aplicada_por', 'decisao', 'confirmacao_autor')})

def url(i):
    if i.startswith('doi:'): return 'https://doi.org/' + i[4:]
    if i.startswith('arXiv:'): return 'https://arxiv.org/abs/' + i[6:]
    return ''

dados, resumo = [], {'contiguo': 0, 'intercalado': 0, 'aproximada': 0, 'nao': 0}
for a in am:
    sid = a['estudo_id']
    p = R / f'evidencias/extracao-v2.2/{sid}.json'
    bruto = p.read_bytes()
    d = json.loads(bruto)
    texto = norm(open(R / d.get('texto_fonte', f'fontes/textos/lote/{sid}.txt'), encoding='utf-8', errors='replace').read())
    tt = toks(texto); ix = indice(tt); ct = compacto(texto)
    def v2(trecho):
        v = verif(trecho, texto, tt)
        if v != 'nao': return v
        tr = norm(trecho)
        partes = [compacto(x) for x in re.split(r'\.\.\.|…|\[\.\.\.\]', tr) if len(compacto(x)) >= 12]
        if partes and all(x in ct for x in partes): return 'aproximada'
        if aprox(toks(tr), ix) or blocos(toks(tr), ct): return 'aproximada'
        return 'nao'
    def marca(lst):
        out = []
        for c in lst or []:
            v = v2(c.get('trecho', ''))
            resumo[v] += 1
            out.append({'trecho': c.get('trecho', ''), 'localizador': c.get('localizador', ''), 'v': v})
        return out
    f = d['ficha']
    f['citacoes'] = marca(f.get('citacoes'))
    for e in d['extracoes']:
        e['citacoes'] = marca(e.get('citacoes'))
    dados.append({
        'id': sid, 'titulo': es[sid]['titulo'], 'url': url(es[sid]['identificador']),
        'identificador': es[sid]['identificador'], 'executor': man[sid]['executor'], 'modelo_executor': man[sid]['modelo_executor'],
        'data_extracao': d.get('data', 'data não registrada na ficha'), 'motivo_amostra': a['motivo'], 'sha256_ficha': hashlib.sha256(bruto).hexdigest(),
        'leitura': d['leitura'], 'ficha': f, 'extracoes': d['extracoes'], 'qualidade': d['qualidade'],
        'correcoes': cor.get(sid, []),
    })

tpl = open(R / 'evidencias/extracao-v2.2/conferencia/modelo.html', encoding='utf-8').read()
js = json.dumps(dados, ensure_ascii=False).replace('</', '<\\/')
out = R / 'evidencias/extracao-v2.2/conferencia/formulario.html'
out.write_text(tpl.replace('/*DADOS*/[]', js), encoding='utf-8')
print(len(dados), 'estudos;', resumo, out.stat().st_size, 'bytes')
