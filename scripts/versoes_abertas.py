#!/usr/bin/env python3
"""Localiza versões abertas de estudos com acesso_aberto=nao_conferido via OpenAlex.

Consulta a API do OpenAlex pelo DOI do estudo (ou pelo título, sem DOI), guarda as
respostas em dados/brutos/<pasta>/openalex.jsonl e registra as versões encontradas
em dados/versoes_abertas.csv. acesso_aberto passa a sim (há local aberto), nao (o
OpenAlex encontrou o trabalho sem local aberto) ou fica nao_conferido (não encontrado).
"""
import argparse
import csv
import json
import pathlib
import re
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
API = 'https://api.openalex.org/works'
CAMPOS = ['estudo_id', 'url', 'tipo', 'versao', 'origem', 'data']


def buscar(estudo):
    ident = estudo['identificador']
    if ident.lower().startswith('doi:'):
        url = f"{API}/doi:{urllib.parse.quote(ident[4:])}"
    else:
        url = f"{API}?{urllib.parse.urlencode({'filter': 'title.search:' + re.sub(r'[,:|]', ' ', estudo['titulo']), 'per-page': 1})}"
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            dados = json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return url, None
        raise
    if 'results' in dados:
        dados = dados['results'][0] if dados['results'] else None
    return url, dados


def locais_abertos(obra):
    vistos = []
    for loc in obra.get('locations') or []:
        if not loc.get('is_oa'):
            continue
        link = loc.get('pdf_url') or loc.get('landing_page_url')
        if link and link not in [v[0] for v in vistos]:
            fonte = (loc.get('source') or {}).get('display_name') or ''
            vistos.append((link, fonte, loc.get('version') or ''))
    return vistos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pasta', help='pasta em dados/brutos para as respostas')
    ap.add_argument('--data', required=True)
    a = ap.parse_args()
    caminho = ROOT / 'dados/estudos.csv'
    with open(caminho, encoding='utf-8') as f:
        estudos = list(csv.DictReader(f))
    pasta = ROOT / 'dados/brutos' / a.pasta
    pasta.mkdir(parents=True, exist_ok=True)
    versoes_csv = ROOT / 'dados/versoes_abertas.csv'
    novo = not versoes_csv.exists()
    contagem = {'sim': 0, 'nao': 0, 'nao_conferido': 0}
    with open(pasta / 'openalex.jsonl', 'a', encoding='utf-8') as bruto, \
         open(versoes_csv, 'a', newline='', encoding='utf-8') as saida:
        w = csv.DictWriter(saida, fieldnames=CAMPOS, lineterminator='\n')
        if novo:
            w.writeheader()
        for e in estudos:
            if e['corpus'] != 'candidato' or e['acesso_aberto'] != 'nao_conferido':
                continue
            url, obra = buscar(e)
            bruto.write(json.dumps({'estudo_id': e['id'], 'consulta': url, 'resposta': obra},
                                   ensure_ascii=False) + '\n')
            if obra and not e['identificador'].lower().startswith('doi:'):
                # Busca por título: aceitar só título idêntico após normalização.
                norm = lambda t: re.sub(r'[^a-z0-9]', '', (t or '').lower())
                if norm(obra.get('title')) != norm(e['titulo']):
                    obra = None
            if obra is None:
                contagem['nao_conferido'] += 1
            else:
                locais = locais_abertos(obra)
                e['acesso_aberto'] = 'sim' if locais else 'nao'
                contagem[e['acesso_aberto']] += 1
                for link, fonte, versao in locais:
                    w.writerow({'estudo_id': e['id'], 'url': link, 'tipo': fonte,
                                'versao': versao, 'origem': 'openalex', 'data': a.data})
            time.sleep(0.15)
    with open(caminho, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(estudos[0]), lineterminator='\n')
        w.writeheader()
        w.writerows(estudos)
    print(contagem)


if __name__ == '__main__':
    main()
