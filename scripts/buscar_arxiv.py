#!/usr/bin/env python3
"""Executa a busca do protocolo v2 (seção 4.2) na API oficial do arXiv.

Grava cada página Atom sem alteração em dados/brutos/<busca_id>/ e a consulta
exata em consulta.txt. Não altera os CSVs; o registro é feito por
scripts/registrar_busca.py.
"""
import argparse
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
API = 'https://export.arxiv.org/api/query'

PROMPTING = ['"prompt engineering"', 'prompting', 'prompt', 'prompts', '"in-context learning"',
             '"few-shot"', '"zero-shot"', '"chain-of-thought"', '"chain of thought"']
TAREFAS = ['"code generation"', '"program synthesis"', '"code translation"', '"program translation"',
           '"code migration"', 'transpil*', 'refactoring', 'refactor', 'debugging', 'debug',
           '"program repair"', '"bug fixing"', '"bug fix"', '"bug repair"']
MODELOS = ['"large language model"', '"large language models"', 'LLM', 'LLMs', '"language model"',
           '"language models"', '"generative AI"', 'ChatGPT', '"GPT-4"', 'Codex']
PERIODO = 'submittedDate:[202101010000 TO 202609072359]'


def bloco(termos, campos):
    return '(' + ' OR '.join(f'{c}:{t}' for t in termos for c in campos) + ')'


def consulta(variante):
    tarefas = ['ti'] if variante == 'titulo' else ['ti', 'abs']
    return ' AND '.join([bloco(PROMPTING, ['ti', 'abs']), bloco(TAREFAS, tarefas),
                         bloco(MODELOS, ['ti', 'abs']), PERIODO])


def baixar(q, start, n):
    url = API + '?' + urllib.parse.urlencode({'search_query': q, 'start': start, 'max_results': n,
                                              'sortBy': 'submittedDate', 'sortOrder': 'ascending'})
    with urllib.request.urlopen(url, timeout=120) as r:
        return r.read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('busca_id')
    ap.add_argument('--variante', choices=['ampla', 'titulo'], default='ampla')
    ap.add_argument('--pagina', type=int, default=500)
    a = ap.parse_args()
    q = consulta(a.variante)
    destino = ROOT / 'dados' / 'brutos' / a.busca_id
    destino.mkdir(parents=True, exist_ok=False)
    (destino / 'consulta.txt').write_text(q + '\n')
    start, total = 0, None
    while total is None or start < total:
        for tentativa in range(5):
            dados = baixar(q, start, a.pagina)
            texto = dados.decode('utf-8')
            total = int(re.search(r'<opensearch:totalResults>(\d+)<', texto).group(1))
            esperado = min(a.pagina, total - start)
            if texto.count('<entry>') == esperado:
                break
            time.sleep(10)
        else:
            sys.exit(f'Página em {start} incompleta após 5 tentativas.')
        (destino / f'pagina-{start // a.pagina + 1:03d}.xml').write_bytes(dados)
        print(f'{start + esperado}/{total}')
        start += a.pagina
        time.sleep(3)


if __name__ == '__main__':
    main()
