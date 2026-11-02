#!/usr/bin/env python3
"""Confere uma nova coleta da busca ACM contra os registros B3 de 29/10/2026.

Lê dados/brutos/<pasta>/captura.json.gz (HTML bruto de cada página de resultados e
a extração feita no navegador), reextrai os registros do HTML em Python, confere
paginação, duplicatas e total exibido, e compara os DOIs com os registros B3 de
dados/registros.csv e com as páginas preservadas em 29/10. Grava registros.csv e
comparacao.csv na pasta da coleta e manifesto.txt com o SHA-256 de cada arquivo.
Não altera dados/registros.csv nem dados/estudos.csv.
"""
import argparse
import csv
import gzip
import hashlib
import html
import json
import pathlib
import re
from datetime import datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
CORTE = '2026-09-07'
ITEM = '<li class="search__item issue-item-container">'


def texto(fragmento):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', fragmento))).strip()


def itens(pagina_html, pagina):
    """Registros de uma página: [posição, tipo, data exibida, DOI, título, data de publicação]."""
    out = []
    for i, bloco in enumerate(pagina_html.split(ITEM)[1:]):
        doi = re.search(r'<input name="(10\.[^"]+)" class="issue-Item__checkbox"', bloco)
        tipo = re.search(r'<div class="issue-heading">(.*?)</div>', bloco, re.S)
        data = re.search(r'<div class="bookPubDate[^"]*"(?: data-title="Published: ([^"]+)")?>(.*?)</div>', bloco, re.S)
        titulo = re.search(r'<h4 class="issue-item__title">(.*?)</h4>', bloco, re.S)
        publicado = ''
        if data and data.group(1):
            publicado = datetime.strptime(data.group(1).strip(), '%d %B %Y').date().isoformat()
        out.append([pagina * 50 + i + 1, texto(tipo.group(1)) if tipo else '',
                    texto(data.group(2)) if data else '', doi.group(1) if doi else '',
                    texto(titulo.group(1)) if titulo else '', publicado])
    return out


def manifesto(pasta):
    # notas.md é documentação editável; o manifesto cobre capturas e derivados.
    linhas = [f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}'
              for p in sorted(pasta.iterdir()) if p.name not in ('manifesto.txt', 'notas.md')]
    (pasta / 'manifesto.txt').write_text('\n'.join(linhas) + '\n')


def main(root=ROOT, pasta_nome='acm-verificacao-2026-11-01', anterior='acm-2026-10-29'):
    pasta = root / 'dados/brutos' / pasta_nome
    with gzip.open(pasta / 'captura.json.gz', 'rt', encoding='utf-8') as f:
        cap = json.load(f)
    chaves = sorted(k for k in cap['html'] if k.startswith('p-'))
    problemas = []
    novos = []
    truncados = []
    for k in chaves:
        p = int(k[2:])
        regs = itens(cap['html'][k], p)
        js = cap['paginas'][k]
        # A extração do navegador e a do HTML bruto devem coincidir. O navegador lia
        # só o link do título, que não inclui o subtítulo.
        if len(regs) != len(js) or any(r[:4] != j[:4] for r, j in zip(regs, js)):
            problemas.append(f'{k}: extração do navegador difere do HTML')
        for r, j in zip(regs, js):
            if r[4] != j[4]:
                if r[4].startswith(j[4]):
                    truncados.append(r[3])
                else:
                    problemas.append(f'{k}: título de {r[3]} difere do HTML')
        novos += [[k] + r for r in regs]
    totais = {l['total_exibido'] for l in cap['log']}
    tamanhos = [len(cap['paginas'][k]) for k in chaves]
    total = int(totais.pop()) if len(totais) == 1 else None
    if total is None:
        problemas.append(f'total exibido variou: {sorted(totais)}')
    if tamanhos[-1] != 0:
        problemas.append('última página consultada não veio vazia')
    if any(n != 50 for n in tamanhos[:-2]):
        problemas.append(f'página intermediária incompleta: {tamanhos}')
    if [r[1] for r in novos] != list(range(1, len(novos) + 1)):
        problemas.append('posições fora de sequência')
    final = cap['paginas'].get('verificacao-final-000')
    if final is not None and final != cap['paginas']['p-000']:
        problemas.append('primeira página mudou entre o início e o fim da coleta')
    dois = [r[4].lower() for r in novos]
    repetidos = sorted({d for d in dois if dois.count(d) > 1})
    if repetidos:
        problemas.append(f'DOIs repetidos: {repetidos}')
    if any(not d for d in dois):
        problemas.append('registro sem DOI')
    if total is not None and len(set(dois)) != total:
        problemas.append(f'{len(set(dois))} DOIs distintos para {total} exibidos')

    with open(pasta / 'registros.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['pagina', 'posicao', 'tipo', 'data_exibida', 'doi', 'titulo', 'data_publicacao'])
        w.writerows(novos)

    with open(root / 'dados/registros.csv', encoding='utf-8') as f:
        b3 = {r['doi'].lower(): r for r in csv.DictReader(f) if r['busca_id'] == 'B3'}
    hist = {}
    for arq in sorted((root / 'dados/brutos' / anterior).glob('pagina-*.json')):
        for r in json.loads(arq.read_text(encoding='utf-8')):
            hist[r[3].lower()] = r
    if set(hist) != set(b3):
        problemas.append('páginas de 29/10 e registros B3 não coincidem')
    novo = {r[4].lower(): r for r in novos}
    linhas = []
    for doi in sorted(set(novo) | set(b3)):
        n, h, reg = novo.get(doi), hist.get(doi), b3.get(doi)
        situacao = 'ambos' if n and reg else ('so_nova' if n else 'so_anterior')
        linhas.append({
            'doi': doi, 'situacao': situacao,
            'registro_id': reg['id'] if reg else '', 'estudo_id': reg['estudo_id'] if reg else '',
            'tipo_igual': 'sim' if n and h and n[2] == h[1] else ('nao' if n and h else ''),
            'data_exibida_igual': 'sim' if n and h and n[3] == h[2] else ('nao' if n and h else ''),
            'titulo_igual': 'sim' if n and h and n[5] == h[4] else ('nao' if n and h else ''),
            'data_publicacao': n[6] if n else '',
            'apos_corte': ('sim' if n[6] > CORTE else 'nao') if n and n[6] else ''})
    with open(pasta / 'comparacao.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]), lineterminator='\n')
        w.writeheader()
        w.writerows(linhas)
    manifesto(pasta)

    conta = lambda campo, valor: sum(1 for l in linhas if l[campo] == valor)
    resumo = {'total_exibido': total, 'paginas': tamanhos, 'linhas': len(novos),
              'dois_distintos': len(set(dois)), 'ambos': conta('situacao', 'ambos'),
              'so_nova': conta('situacao', 'so_nova'), 'so_anterior': conta('situacao', 'so_anterior'),
              'tipo_diferente': conta('tipo_igual', 'nao'), 'data_diferente': conta('data_exibida_igual', 'nao'),
              'titulo_diferente': conta('titulo_igual', 'nao'), 'titulo_truncado_no_navegador': truncados, 'sem_data_publicacao': conta('data_publicacao', ''),
              'publicados_apos_corte': conta('apos_corte', 'sim'), 'problemas': problemas}
    print(json.dumps(resumo, ensure_ascii=False))
    return resumo


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('pasta', nargs='?', default='acm-verificacao-2026-11-01')
    main(pasta_nome=ap.parse_args().pasta)
