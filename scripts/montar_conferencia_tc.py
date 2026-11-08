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


def escolher(a, b, semente, minimo=15):
    """Protocolo, seção 7: 20% das exclusões consensuais, com mínimo de 15 (corrigido em D78).

    Se o sorteio de 20% der menos que o mínimo, completa com as exclusões de menor valor
    sorteado, na mesma semente; com menos exclusões que o mínimo, entram todas.
    """
    lista, consensuais = [], []
    for i in a:
        da, db = a[i]['decisao'], b[i]['decisao']
        if da == db == 'excluir':
            consensuais.append(i)
        else:
            lista.append((i, 'obrigatoria'))
    ordem = sorted(consensuais, key=lambda i: random.Random(f'{semente}-{i}').random())
    # As sorteadas (valor < 0,2) são as primeiras de `ordem`; o mínimo estende o corte.
    n = sum(sorteado(i, semente) for i in consensuais)
    escolhidas = set(ordem[:max(n, minimo)])
    lista += [(i, 'exclusao_sorteada') for i in consensuais if i in escolhidas]
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
