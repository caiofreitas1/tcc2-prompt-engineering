#!/usr/bin/env python3
"""Sorteia e obtém as versões abertas da medição de texto completo (D50).

Sorteia N estudos que seguem pela regra de união nas amostras do piloto e têm
acesso_aberto=sim. Baixa os PDFs para fontes/artigos/medicao/ (fora do Git, sem
executá-los) e grava em evidencias/piloto/medicao-texto.csv a fonte, o hash e a
situação de cada um.
"""
import argparse
import csv
import hashlib
import pathlib
import random
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
PASTA = ROOT / 'fontes/artigos/medicao'
LIMITE_BYTES = 30 * 1024 * 1024
CAMPOS = ['ordem', 'estudo_id', 'titulo', 'url', 'situacao', 'bytes', 'sha256', 'data']


def quadro():
    with open(ROOT / 'dados/estudos.csv', encoding='utf-8') as f:
        estudos = {e['id']: e for e in csv.DictReader(f)}
    ids = set()
    for n in (1, 2):
        with open(ROOT / f'evidencias/piloto/comparacao-amostra-{n}.csv', encoding='utf-8') as f:
            ids |= {r['estudo_id'] for r in csv.DictReader(f)
                    if r['uniao'] == 'segue' and estudos[r['estudo_id']]['acesso_aberto'] == 'sim'}
    return sorted(ids, key=lambda i: int(i[1:])), estudos


def url_aberta(sid, registros):
    arxiv = next((r['arxiv'] for r in registros if r['estudo_id'] == sid and r['arxiv']), '')
    if arxiv:
        return f'https://arxiv.org/pdf/{arxiv}'
    doi = next((r['doi'] for r in registros if r['estudo_id'] == sid and r['doi']), '')
    return f'https://dl.acm.org/doi/pdf/{doi}'


def baixar(url, destino):
    pedido = urllib.request.Request(url, headers={'User-Agent': 'tcc2-rsl/1.0'})
    try:
        with urllib.request.urlopen(pedido, timeout=60) as r:
            conteudo = r.read(LIMITE_BYTES + 1)
    except (urllib.error.URLError, TimeoutError) as e:
        return f'fonte_indisponivel: {e}', 0, ''
    if len(conteudo) > LIMITE_BYTES or not conteudo.startswith(b'%PDF-'):
        return 'fonte_indisponivel: resposta não é PDF', 0, ''
    destino.write_bytes(conteudo)
    return 'obtido', len(conteudo), hashlib.sha256(conteudo).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=12)
    ap.add_argument('--semente', type=int, required=True)
    ap.add_argument('--data', required=True)
    a = ap.parse_args()
    ids, estudos = quadro()
    with open(ROOT / 'dados/registros.csv', encoding='utf-8') as f:
        registros = list(csv.DictReader(f))
    amostra = random.Random(a.semente).sample(ids, a.n)
    PASTA.mkdir(parents=True, exist_ok=True)
    with open(ROOT / 'evidencias/piloto/medicao-texto.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS, lineterminator='\n')
        w.writeheader()
        for n, sid in enumerate(amostra, 1):
            url = url_aberta(sid, registros)
            situacao, tamanho, sha = baixar(url, PASTA / f'{sid}.pdf')
            w.writerow({'ordem': n, 'estudo_id': sid, 'titulo': estudos[sid]['titulo'], 'url': url,
                        'situacao': situacao, 'bytes': tamanho, 'sha256': sha, 'data': a.data})
            print(sid, situacao, tamanho)
            time.sleep(3)
    print(f'{a.n} de {len(ids)} estudos; semente {a.semente}')


if __name__ == '__main__':
    main()
