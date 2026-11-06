#!/usr/bin/env python3
"""Escolhe os estudos que o autor confere no texto completo (protocolo, seção 7).

Lê as decisões de IA-A e IA-B (JSONL selados) e separa: conferência obrigatória (inclusão,
dúvida ou divergência) e exclusões consensuais, das quais 20% entram por sorteio estável
(semente fixa por estudo). Grava a lista, ainda selada, em evidencias/lote/selado/ e imprime
os estudos para o formulário, em ordem embaralhada, sem revelar o motivo da escolha.
"""
import argparse
import csv
import json
import pathlib
import random

ROOT = pathlib.Path(__file__).resolve().parents[1]


def sorteado(estudo_id, semente, proporcao=0.2):
    return random.Random(f'{semente}-{estudo_id}').random() < proporcao


def escolher(a, b, semente):
    lista = []
    for i in a:
        da, db = a[i]['decisao'], b[i]['decisao']
        if da == db == 'excluir':
            if sorteado(i, semente):
                lista.append((i, 'exclusao_sorteada'))
        else:
            lista.append((i, 'obrigatoria'))
    return lista


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ia-a', nargs='+', required=True)
    ap.add_argument('--ia-b', nargs='+', required=True)
    ap.add_argument('--semente', type=int, default=20261106)
    a = ap.parse_args()
    ler = lambda arqs: {x['estudo_id']: x for p in arqs for x in map(json.loads, open(p, encoding='utf-8')) if x}
    ia_a, ia_b = ler(a.ia_a), ler(a.ia_b)
    assert set(ia_a) == set(ia_b), 'IA-A e IA-B leram estudos diferentes'
    lista = escolher(ia_a, ia_b, a.semente)
    with open(ROOT / 'evidencias/lote/selado/conferencia-tc.csv', 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['estudo_id', 'motivo_da_conferencia'])
        w.writerows(lista)
    ids = [i for i, _ in lista]
    random.Random(a.semente).shuffle(ids)
    print(json.dumps(ids))


if __name__ == '__main__':
    main()
