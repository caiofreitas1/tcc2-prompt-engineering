#!/usr/bin/env python3
"""Sorteia a amostra do lote piloto da triagem de título e resumo (protocolo, seção 7).

Sorteia N estudos `candidato` de dados/estudos.csv com semente fixa, sem reposição,
excluindo os já presentes em amostras anteriores, e grava em evidencias/piloto/ o
arquivo da amostra com título e resumo (a entrada dos triadores, sem decisões).
"""
import argparse
import csv
import pathlib
import random

ROOT = pathlib.Path(__file__).resolve().parents[1]
CAMPOS = ['ordem', 'estudo_id', 'titulo', 'resumo', 'fonte_resumo']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('saida', help='nome do arquivo em evidencias/piloto/')
    ap.add_argument('--n', type=int, default=100)
    ap.add_argument('--semente', type=int, required=True)
    ap.add_argument('--excluir', nargs='*', default=[], help='amostras anteriores a não repetir')
    a = ap.parse_args()
    with open(ROOT / 'dados/estudos.csv', encoding='utf-8') as f:
        estudos = {e['id']: e for e in csv.DictReader(f) if e['corpus'] == 'candidato'}
    with open(ROOT / 'dados/resumos.csv', encoding='utf-8') as f:
        resumos = {r['estudo_id']: r for r in csv.DictReader(f)}
    usados = set()
    for nome in a.excluir:
        with open(ROOT / 'evidencias/piloto' / nome, encoding='utf-8') as f:
            usados |= {r['estudo_id'] for r in csv.DictReader(f)}
    # Ordem numérica dos IDs antes do sorteio: o resultado depende só da semente.
    universo = sorted((i for i in estudos if i not in usados), key=lambda i: int(i[1:]))
    amostra = random.Random(a.semente).sample(universo, a.n)
    pasta = ROOT / 'evidencias/piloto'
    pasta.mkdir(parents=True, exist_ok=True)
    with open(pasta / a.saida, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS, lineterminator='\n')
        w.writeheader()
        for n, sid in enumerate(amostra, 1):
            r = resumos[sid]
            w.writerow({'ordem': n, 'estudo_id': sid, 'titulo': estudos[sid]['titulo'],
                        'resumo': r['resumo'], 'fonte_resumo': r['fonte']})
    print(f'{len(amostra)} de {len(universo)} candidatos; semente {a.semente}')


if __name__ == '__main__':
    main()
