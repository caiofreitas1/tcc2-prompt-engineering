#!/usr/bin/env python3
"""Monta dados/resumos.csv: um resumo por estudo, para a triagem de título e resumo.

Usa primeiro as exportações originais (arXiv: Atom; IEEE: RIS). Para estudos sem
resumo nas exportações (registros só da ACM), consulta pelo DOI o OpenAlex, o
Crossref e o Semantic Scholar, nessa ordem, guardando as respostas em
dados/brutos/<pasta>/. Textos com menos de 60 caracteres não contam como resumo.
Estudos sem resumo em nenhuma fonte ficam com resumo vazio e fonte nao_encontrado.
"""
import argparse
import csv
import html
import json
import pathlib
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
NS = {'a': 'http://www.w3.org/2005/Atom'}


def limpar(t):
    return re.sub(r'\s+', ' ', t or '').strip()


def resumos_arxiv(pasta):
    out = {}
    for pagina in sorted(pasta.glob('pagina-*.xml')):
        for e in ET.parse(pagina).getroot().findall('a:entry', NS):
            ident = re.sub(r'v\d+$', '', e.findtext('a:id', '', NS).rsplit('/abs/', 1)[-1])
            out[ident] = limpar(e.findtext('a:summary', '', NS))
    return out


def resumos_ris(pasta):
    out = []
    for arquivo in sorted(pasta.glob('pagina-*.ris')):
        campos = {}
        for linha in arquivo.read_text(encoding='utf-8-sig').splitlines():
            marca, valor = linha[:5], linha[6:].strip()
            if marca == 'ER  -':
                out.append(limpar(campos.get('AB')))
                campos = {}
            elif re.fullmatch(r'[A-Z][A-Z0-9]  -', marca):
                campos.setdefault(marca[:2], valor)
    return out


def obter(url):
    for tentativa in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code != 429 or tentativa == 3:
                raise
            time.sleep(5 * (tentativa + 1))


def de_openalex(obra):
    idx = (obra or {}).get('abstract_inverted_index')
    if not idx:
        return ''
    pos = sorted((p, w) for w, ps in idx.items() for p in ps)
    return limpar(' '.join(w for _, w in pos))


def de_crossref(resp):
    ab = ((resp or {}).get('message') or {}).get('abstract') or ''
    ab = re.sub(r'<jats:title>.*?</jats:title>', ' ', ab, flags=re.S)
    return limpar(html.unescape(re.sub(r'<[^>]+>', ' ', ab)))


def de_semanticscholar(resp):
    return limpar((resp or {}).get('abstract'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pasta', help='pasta em dados/brutos para as respostas das APIs')
    a = ap.parse_args()
    with open(ROOT / 'dados/registros.csv', encoding='utf-8') as f:
        registros = list(csv.DictReader(f))
    with open(ROOT / 'dados/buscas.csv', encoding='utf-8') as f:
        buscas = {b['id']: b for b in csv.DictReader(f)}
    pasta_de = {bid: ROOT / pathlib.Path(b['arquivo_exportacao']).parent for bid, b in buscas.items()}
    por_registro = {}
    for bid, b in buscas.items():
        regs = [r for r in registros if r['busca_id'] == bid]
        if b['base'] == 'arxiv':
            ab = resumos_arxiv(pasta_de[bid])
            for r in regs:
                por_registro[r['id']] = ('arxiv', ab.get(r['arxiv'], ''))
        elif b['base'] == 'ieee_xplore':
            abs_ = resumos_ris(pasta_de[bid])
            assert len(abs_) == len(regs), bid
            for r, ab in zip(regs, abs_):
                por_registro[r['id']] = ('ieee_xplore', ab)
    estudos = {}
    for r in registros:
        estudos.setdefault(r['estudo_id'], []).append(r)
    saida = []
    brutos = ROOT / 'dados/brutos' / a.pasta
    brutos.mkdir(parents=True, exist_ok=True)
    with open(brutos / 'openalex.jsonl', 'a', encoding='utf-8') as fo, \
         open(brutos / 'crossref.jsonl', 'a', encoding='utf-8') as fc, \
         open(brutos / 'semanticscholar.jsonl', 'a', encoding='utf-8') as fs:
        for sid, regs in estudos.items():
            escolha = next(((r['id'],) + por_registro[r['id']] for r in regs
                            if por_registro.get(r['id'], ('', ''))[1]), None)
            if escolha is None:
                doi = next((r['doi'] for r in regs if r['doi']), '')
                escolha = (regs[0]['id'], 'nao_encontrado', '')
                if doi:
                    fontes = [
                        ('openalex', 'https://api.openalex.org/works/doi:' + urllib.parse.quote(doi), fo, de_openalex),
                        ('crossref', 'https://api.crossref.org/works/' + urllib.parse.quote(doi), fc, de_crossref),
                        ('semanticscholar', 'https://api.semanticscholar.org/graph/v1/paper/DOI:'
                         + urllib.parse.quote(doi) + '?fields=title,abstract', fs, de_semanticscholar)]
                    for nome, url, arq, extrair in fontes:
                        resp = obter(url)
                        arq.write(json.dumps({'estudo_id': sid, 'consulta': url, 'resposta': resp}, ensure_ascii=False) + '\n')
                        texto = extrair(resp)
                        time.sleep(1.2 if nome == 'semanticscholar' else 0.2)
                        if len(texto) >= 60:
                            escolha = (regs[0]['id'], nome, texto)
                            break
            saida.append({'estudo_id': sid, 'registro_id': escolha[0], 'fonte': escolha[1], 'resumo': escolha[2]})
    saida.sort(key=lambda x: int(x['estudo_id'][1:]))
    with open(ROOT / 'dados/resumos.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['estudo_id', 'registro_id', 'fonte', 'resumo'], lineterminator='\n')
        w.writeheader()
        w.writerows(saida)
    contagem = {}
    for s in saida:
        contagem[s['fonte']] = contagem.get(s['fonte'], 0) + 1
    print(len(saida), contagem)


if __name__ == '__main__':
    main()
