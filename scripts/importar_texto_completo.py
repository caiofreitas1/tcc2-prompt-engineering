#!/usr/bin/env python3
"""Importa a conferência cega do texto completo (T06) e abre os selos de IA-A e IA-B.

Entradas: os documentos da coleção `texto_completo_autor` do formulário, salvos como JSON
(um arquivo por estudo), e os JSONL selados de IA-A e IA-B com tc-v2. Saídas:
- evidencias/lote/autor-texto-completo.jsonl: decisões do autor, na ordem do formulário;
- dados/triagem.csv: linhas da fase texto_completo (refeitas a cada execução);
- dados/estudos.csv: corpus=definitivo para os estudos que o autor incluiu.
A data de cada decisão de IA vem da leva em que o estudo foi lido (D68 a D77), pela
posição no JSONL cumulativo; a do autor, do horário de gravação em UTC-3.
"""
import argparse
import csv
import datetime as dt
import glob
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
AUTOR = 'Caio César de Freitas'
# Fim (exclusivo) de cada leva no JSONL cumulativo e a data da leitura.
LEVAS = [(36, '2026-11-05'), (196, '2026-11-06'), (256, '2026-11-07')]
CAMPOS_TRIAGEM = ['estudo_id', 'fase', 'decisao', 'criterio', 'motivo', 'responsavel',
                  'natureza', 'prompt_versao', 'data']


def data_leva(pos):
    for fim, data in LEVAS:
        if pos < fim:
            return data
    raise ValueError(f'posição {pos} fora das levas registradas')


def data_local(iso):
    t = dt.datetime.fromisoformat(iso.replace('Z', '+00:00'))
    return t.astimezone(dt.timezone(dt.timedelta(hours=-3))).date().isoformat()


def codigos(criterio):
    """Mantém só os códigos do protocolo; o texto original fica no JSONL selado (D78)."""
    return ';'.join(dict.fromkeys(re.findall(r'\b[IX][1-7]\b', criterio)))


def ler_ia(caminho, responsavel):
    linhas = []
    for pos, texto in enumerate(open(caminho, encoding='utf-8')):
        x = json.loads(texto)
        linhas.append({'estudo_id': x['estudo_id'], 'fase': 'texto_completo',
                       'decisao': x['decisao'], 'criterio': codigos(x['criterio']),
                       'motivo': ' '.join(x['motivo'].split()), 'responsavel': responsavel,
                       'natureza': 'ia', 'prompt_versao': 'tc-v2', 'data': data_leva(pos)})
    return linhas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--autor', required=True, help='diretório com um JSON por estudo')
    ap.add_argument('--ia-a', default=ROOT / 'evidencias/lote/selado/ia-a-tc-v2.jsonl')
    ap.add_argument('--ia-b', default=ROOT / 'evidencias/lote/selado/ia-b-tc-v2.jsonl')
    a = ap.parse_args()

    autor = sorted((json.load(open(p, encoding='utf-8')) for p in glob.glob(f'{a.autor}/*.json')),
                   key=lambda x: x['ordem'])
    ia_a, ia_b = ler_ia(a.ia_a, 'ia-A'), ler_ia(a.ia_b, 'ia-B')
    ids_a = [x['estudo_id'] for x in ia_a]
    assert sorted(ids_a) == sorted(x['estudo_id'] for x in ia_b), 'IA-A e IA-B leram estudos diferentes'
    assert {x['estudo_id'] for x in autor} <= set(ids_a), 'decisão do autor fora dos estudos lidos'

    with open(ROOT / 'evidencias/lote/autor-texto-completo.jsonl', 'w', encoding='utf-8') as f:
        for x in autor:
            f.write(json.dumps(x, ensure_ascii=False, sort_keys=True) + '\n')

    humanas = [{'estudo_id': x['estudo_id'], 'fase': 'texto_completo', 'decisao': x['decisao'],
                'criterio': x['criterio'], 'motivo': ' '.join(x['motivo'].split()),
                'responsavel': AUTOR, 'natureza': 'humano', 'prompt_versao': '',
                'data': data_local(x['salvo_em'])} for x in autor]
    caminho = ROOT / 'dados/triagem.csv'
    antigas = [x for x in csv.DictReader(open(caminho, encoding='utf-8', newline=''))
               if x['fase'] != 'texto_completo']
    with open(caminho, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS_TRIAGEM)  # \r\n, como no arquivo original
        w.writeheader()
        w.writerows(antigas + ia_a + ia_b + humanas)

    incluidos = {x['estudo_id'] for x in autor if x['decisao'] == 'incluir'}
    caminho = ROOT / 'dados/estudos.csv'
    with open(caminho, encoding='utf-8', newline='') as f:
        leitor = csv.DictReader(f)
        campos, estudos = leitor.fieldnames, list(leitor)
    for s in estudos:
        if s['id'] in incluidos:
            s['corpus'] = 'definitivo'
    with open(caminho, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=campos, lineterminator='\n')
        w.writeheader()
        w.writerows(estudos)
    print(f'autor: {len(autor)}; IA: {len(ia_a)} + {len(ia_b)}; corpus definitivo: {len(incluidos)}')


if __name__ == '__main__':
    main()
