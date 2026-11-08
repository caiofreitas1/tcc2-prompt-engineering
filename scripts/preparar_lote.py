#!/usr/bin/env python3
"""Monta o lote da revisão rápida (D64) e separa as duas etapas.

Seleciona os candidatos com a tarefa no título e S1, S2, S4 e S6 (D59). Os estudos da
amostra 2 já têm decisões com tr-v2 e não voltam ao lote; os da amostra 1 foram triados com
tr-v1 e voltam. Grava evidencias/lote/lista.csv e, em --saida, os arquivos JSONL para as IAs.
O indício de revisão por pares é registro no IEEE ou na ACM, DOI ou journal_ref no arXiv, ou
local de publicação no Semantic Scholar ou no OpenAlex; só define a ordem das etapas e não comprova
a revisão.
"""
import argparse
import csv
import glob
import json
import pathlib
import re
import xml.etree.ElementTree as ET

from analisar_piloto import tarefa_no_titulo

ROOT = pathlib.Path(__file__).resolve().parents[1]
REFERENCIA = ['S1', 'S2', 'S4', 'S6']
PREPRINT = re.compile(r'arxiv|corr\b|preprint|biorxiv|techrxiv|ssrn|research square|authorea', re.I)
ARXIV_ID = re.compile(r'(?:arxiv\.|arxiv\.org/(?:abs|pdf)/)(\d{4}\.\d{4,5})', re.I)
NS = {'a': 'http://www.w3.org/2005/Atom', 'x': 'http://arxiv.org/schemas/atom'}


def ler(caminho):
    with open(ROOT / caminho, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def local_publicado(resposta):
    """Local de publicação informado pelo Semantic Scholar, sem contar repositórios de preprints."""
    if not resposta:
        return ''
    nomes = [resposta.get('venue') or '',
             (resposta.get('publicationVenue') or {}).get('name') or '',
             (resposta.get('journal') or {}).get('name') or '']
    for nome in nomes:
        if nome.strip() and not PREPRINT.search(nome):
            return nome.strip()
    doi = (resposta.get('externalIds') or {}).get('DOI') or ''
    return 'doi:' + doi if doi and not doi.lower().startswith('10.48550') else ''


def arxiv_da_obra(obra):
    """Identificador arXiv da obra do OpenAlex. Se há versão publicada, o DOI principal é o da editora."""
    textos = [obra.get('doi') or '']
    for local in obra.get('locations') or []:
        textos += [local.get('landing_page_url') or '', local.get('pdf_url') or '']
    for texto in textos:
        m = ARXIV_ID.search(texto)
        if m:
            return m.group(1)
    return ''


def publicado_openalex(obra):
    """Identificador arXiv da obra do OpenAlex com local em periódico ou evento, ou ''."""
    for local in obra.get('locations') or []:
        fonte = local.get('source') or {}
        if fonte.get('type') in {'journal', 'conference'} and not PREPRINT.search(fonte.get('display_name') or ''):
            return arxiv_da_obra(obra)
    return ''


def publicados_no_arxiv():
    ids = set()
    for pagina in glob.glob(str(ROOT / 'dados/brutos/arxiv-2026-10-29/pagina-*.xml')):
        for e in ET.parse(pagina).getroot().findall('a:entry', NS):
            if e.find('x:journal_ref', NS) is not None or e.find('x:doi', NS) is not None:
                ids.add(e.find('a:id', NS).text.split('/abs/')[1].split('v')[0])
    return ids


def indicio(registros, arxiv_publicado, s2, openalex=frozenset()):
    """Devolve a origem do indício de revisão por pares, ou '' se não houver."""
    bases = {r['busca_id'] for r in registros}
    if bases & {'B2', 'B3'}:
        return 'base'
    if any(r['doi'] or r['arxiv'] in arxiv_publicado for r in registros):
        return 'arxiv'
    if any(local_publicado(s2.get(r['arxiv'])) for r in registros):
        return 'semantic_scholar'
    if any(r['arxiv'] in openalex for r in registros):
        return 'openalex'
    return ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--saida', required=True, help='pasta dos arquivos para as IAs')
    ap.add_argument('--tamanho', type=int, default=100)
    ap.add_argument('--s2', default='evidencias/piloto/cenarios-orientador/s2.jsonl')
    ap.add_argument('--openalex', default='evidencias/piloto/cenarios-orientador/openalex-arxiv.jsonl')
    a = ap.parse_args()

    estudos = {e['id']: e for e in ler('dados/estudos.csv')}
    resumos = {r['estudo_id']: r['resumo'] for r in ler('dados/resumos.csv')}
    registros = {}
    for r in ler('dados/registros.csv'):
        registros.setdefault(r['estudo_id'], []).append(r)
    amostra2 = {x['estudo_id'] for x in ler('evidencias/piloto/amostra-2.csv')}
    s2 = {}
    caminho_s2 = ROOT / a.s2
    if caminho_s2.exists():
        for linha in caminho_s2.read_text(encoding='utf-8').splitlines():
            o = json.loads(linha)
            if o['r'] or o['arxiv'] not in s2:
                s2[o['arxiv']] = o['r']
    openalex, consultados = set(), set()
    caminho_oa = ROOT / a.openalex
    if caminho_oa.exists():
        openalex = {publicado_openalex(json.loads(linha))
                    for linha in caminho_oa.read_text(encoding='utf-8').splitlines()} - {''}
        consultados = {arxiv_da_obra(json.loads(linha))
                       for linha in caminho_oa.read_text(encoding='utf-8').splitlines()}
    arxiv_publicado = publicados_no_arxiv()

    escolhidos = [i for i, e in estudos.items()
                  if (e['corpus'] == 'candidato' and tarefa_no_titulo(e['titulo'])) or i in REFERENCIA]
    escolhidos.sort(key=lambda i: int(i[1:]))
    linhas = []
    for i in escolhidos:
        origem = indicio(registros[i], arxiv_publicado, s2, openalex)
        arxivs = [r['arxiv'] for r in registros[i] if r['arxiv']]
        linhas.append({'estudo_id': i,
                       'etapa': 1 if origem else 2,
                       'indicio_revisao': origem,
                       'consulta_local': 'sim' if arxivs and all(x in s2 or x in consultados for x in arxivs) else 'nao',
                       'decisoes_tr_v2': 'amostra_2' if i in amostra2 else 'lote'})
    pasta = ROOT / 'evidencias/lote'
    pasta.mkdir(parents=True, exist_ok=True)
    with open(pasta / 'lista.csv', 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)

    lote = [x['estudo_id'] for x in linhas if x['decisoes_tr_v2'] == 'lote']
    saida = pathlib.Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)
    for k in range(0, len(lote), a.tamanho):
        with open(saida / f'lote-{k // a.tamanho + 1:02d}.jsonl', 'w', encoding='utf-8') as f:
            for i in lote[k:k + a.tamanho]:
                f.write(json.dumps({'estudo_id': i, 'titulo': estudos[i]['titulo'],
                                    'resumo': resumos.get(i, '')}, ensure_ascii=False) + '\n')
    n1 = sum(x['etapa'] == 1 for x in linhas)
    print(f'{len(linhas)} estudos; etapa 1: {n1}; etapa 2: {len(linhas) - n1}; no lote: {len(lote)}; '
          f'amostra 2: {len(linhas) - len(lote)}; sem consulta de local: '
          f"{sum(x['consulta_local'] == 'nao' and not x['indicio_revisao'] for x in linhas)}")


if __name__ == '__main__':
    main()
