#!/usr/bin/env python3
"""Compara as decisões do autor com as de IA-A e IA-B no lote piloto (D44/D45).

Lê o arquivo do autor e os das duas IAs (JSONL com estudo_id e decisao), aplica a
regra de união e calcula revocação, perdas, κ de Cohen e tabelas de contingência.
Também estima o efeito da variante de recuo (bloco de tarefas só no título, protocolo,
seção 4.2) sobre os candidatos e sobre a amostra. Grava a comparação por estudo em CSV
e imprime o resultado.
"""
import argparse
import csv
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
CATEGORIAS = ['incluir', 'duvida', 'excluir']
BINARIO = ['segue', 'sai']
TAREFAS = re.compile(r'\b(?:code generation|program synthesis|code translation|program translation'
                     r'|code migration|transpil\w*|refactoring|refactor|debugging|debug|program repair'
                     r'|bug fixing|bug fix|bug repair)\b', re.I)


def tarefa_no_titulo(titulo):
    return bool(TAREFAS.search(re.sub(r'[-‐–]', ' ', titulo)))


def binario(decisao):
    return 'sai' if decisao == 'excluir' else 'segue'


def uniao(a, b):
    """Regra de união: exclusão exige as duas IAs (protocolo, seção 6)."""
    return 'sai' if a == 'excluir' and b == 'excluir' else 'segue'


def kappa(x, y, categorias):
    n = len(x)
    observada = sum(a == b for a, b in zip(x, y)) / n
    esperada = sum(x.count(c) * y.count(c) for c in categorias) / n ** 2
    return None if esperada == 1 else (observada - esperada) / (1 - esperada)


def tabela(x, y, lin, col):
    return {a: {b: sum(p == a and q == b for p, q in zip(x, y)) for b in col} for a in lin}


def ler(caminho):
    with open(caminho, encoding='utf-8') as f:
        return {r['estudo_id']: r for r in map(json.loads, f)}


def analisar(autor, ia_a, ia_b):
    ids = sorted(autor, key=lambda i: int(i[1:]))
    if set(ids) != set(ia_a) or set(ids) != set(ia_b):
        raise ValueError('os três arquivos precisam ter os mesmos estudos')
    au = [autor[i]['decisao'] for i in ids]
    a = [ia_a[i]['decisao'] for i in ids]
    b = [ia_b[i]['decisao'] for i in ids]
    un = [uniao(p, q) for p, q in zip(a, b)]
    au_bin = [binario(d) for d in au]
    incluir = [i for i, d in zip(ids, au) if d == 'incluir']
    perdas = [i for i, d, u in zip(ids, au, un) if d == 'incluir' and u == 'sai']
    perdas_duvida = [i for i, d, u in zip(ids, au, un) if d == 'duvida' and u == 'sai']
    seguem_autor = [i for i, d in zip(ids, au_bin) if d == 'segue']
    return {
        'n': len(ids),
        'revocacao': (len(incluir) - len(perdas), len(incluir)),
        'revocacao_complementar': (len(seguem_autor) - len(perdas) - len(perdas_duvida), len(seguem_autor)),
        'perdas': perdas,
        'perdas_duvida': perdas_duvida,
        'kappa_uniao': kappa(au_bin, un, BINARIO),
        'kappa_autor_a': kappa(au, a, CATEGORIAS),
        'kappa_autor_b': kappa(au, b, CATEGORIAS),
        'kappa_a_b': kappa(a, b, CATEGORIAS),
        'kappa_a_b_binario': kappa([binario(d) for d in a], [binario(d) for d in b], BINARIO),
        'autor_x_uniao': tabela(au, un, CATEGORIAS, BINARIO),
        'autor_x_a': tabela(au, a, CATEGORIAS, CATEGORIAS),
        'autor_x_b': tabela(au, b, CATEGORIAS, CATEGORIAS),
        'a_x_b': tabela(a, b, CATEGORIAS, CATEGORIAS),
        'linhas': [{'estudo_id': i, 'autor': d, 'ia_a': p, 'ia_b': q, 'uniao': u}
                   for i, d, p, q, u in zip(ids, au, a, b, un)],
    }


def recuo(linhas, estudos):
    """Efeito da variante de recuo; `estudos` são os candidatos, por id."""
    no_titulo = [l for l in linhas if tarefa_no_titulo(estudos[l['estudo_id']]['titulo'])]
    conta = lambda ls, d: sum(l['autor'] == d for l in ls)
    return {
        'candidatos': len(estudos),
        'candidatos_no_titulo': sum(tarefa_no_titulo(e['titulo']) for e in estudos.values()),
        'amostra_no_titulo': len(no_titulo),
        'amostra_segue': sum(l['uniao'] == 'segue' for l in no_titulo),
        'amostra_duas_incluem': sum(l['ia_a'] == l['ia_b'] == 'incluir' for l in no_titulo),
        'autor_incluir_no_titulo': conta(no_titulo, 'incluir'),
        'autor_incluir_fora': conta(linhas, 'incluir') - conta(no_titulo, 'incluir'),
        'perdas_no_titulo': [l['estudo_id'] for l in no_titulo if l['autor'] == 'incluir' and l['uniao'] == 'sai'],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--autor', required=True)
    ap.add_argument('--ia-a', required=True)
    ap.add_argument('--ia-b', required=True)
    ap.add_argument('--saida', required=True, help='CSV da comparação por estudo')
    args = ap.parse_args()
    r = analisar(ler(args.autor), ler(args.ia_a), ler(args.ia_b))
    with open(ROOT / 'dados/estudos.csv', encoding='utf-8') as f:
        estudos = {e['id']: e for e in csv.DictReader(f) if e['corpus'] == 'candidato'}
    r['recuo'] = recuo(r['linhas'], estudos)
    for l in r['linhas']:
        l['tarefa_no_titulo'] = 'sim' if tarefa_no_titulo(estudos[l['estudo_id']]['titulo']) else 'nao'
    with open(ROOT / args.saida, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['estudo_id', 'autor', 'ia_a', 'ia_b', 'uniao', 'tarefa_no_titulo'], lineterminator='\n')
        w.writeheader()
        w.writerows(r.pop('linhas'))
    print(json.dumps(r, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
