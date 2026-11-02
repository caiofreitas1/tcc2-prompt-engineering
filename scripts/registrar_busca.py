#!/usr/bin/env python3
"""Registra uma exportação de dados/brutos/ em dados/buscas.csv e dados/registros.csv.

Gera manifesto.txt (SHA-256 de cada arquivo bruto) e acrescenta uma linha por
registro exportado, na ordem da exportação, sem deduplicar.
"""
import argparse
import csv
import hashlib
import json
import pathlib
import re
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
NS = {'a': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}


def limpar(texto):
    return re.sub(r'\s+', ' ', texto or '').strip()


def ler_arxiv(pasta):
    for pagina in sorted(pasta.glob('pagina-*.xml')):
        for e in ET.parse(pagina).getroot().findall('a:entry', NS):
            ident = e.findtext('a:id', '', NS).rsplit('/abs/', 1)[-1]
            yield {'titulo': limpar(e.findtext('a:title', '', NS)),
                   'ano': e.findtext('a:published', '', NS)[:4],
                   'doi': limpar(e.findtext('arxiv:doi', '', NS)).lower(),
                   'arxiv': re.sub(r'v\d+$', '', ident)}


def ler_ris(pasta):
    for arquivo in sorted(pasta.glob('pagina-*.ris')):
        campos = {}
        for linha in arquivo.read_text(encoding='utf-8-sig').splitlines():
            marca, valor = linha[:5], linha[6:].strip()
            if marca == 'ER  -':
                doi = campos.get('DO', '').lower()
                arxiv = re.search(r'arxiv\.(\d{4}\.\d{4,5})', doi)
                yield {'titulo': limpar(campos.get('TI') or campos.get('T1')),
                       'ano': (campos.get('PY') or campos.get('Y1') or '')[:4],
                       'doi': doi, 'arxiv': arxiv.group(1) if arxiv else ''}
                campos = {}
            elif re.fullmatch(r'[A-Z][A-Z0-9]  -', marca):
                campos.setdefault(marca[:2], valor)


def ler_acm(pasta):
    # Itens extraídos das páginas de resultados: [posição, tipo, data, doi, título].
    for arquivo in sorted(pasta.glob('pagina-*.json')):
        for _, _, data, doi, titulo in json.loads(arquivo.read_text(encoding='utf-8')):
            ano = re.search(r'\b(19|20)\d{2}\b', data)
            yield {'titulo': limpar(titulo), 'ano': ano.group(0) if ano else '',
                   'doi': doi.lower(), 'arxiv': ''}


LEITORES = {'arxiv': ler_arxiv, 'ris': ler_ris, 'acm': ler_acm}


def manifesto(pasta):
    # notas.md é documentação editável; o manifesto cobre só as capturas.
    linhas = [f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}'
              for p in sorted(pasta.iterdir()) if p.name not in ('manifesto.txt', 'notas.md')]
    caminho = pasta / 'manifesto.txt'
    caminho.write_text('\n'.join(linhas) + '\n')
    return caminho


def acrescentar(arquivo, campos, linhas):
    with open(arquivo, 'a', newline='', encoding='utf-8') as f:
        csv.DictWriter(f, fieldnames=campos, lineterminator='\n').writerows(linhas)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('busca_id')
    ap.add_argument('pasta')
    ap.add_argument('--leitor', choices=LEITORES, required=True)
    ap.add_argument('--base', required=True)
    ap.add_argument('--data', required=True)
    ap.add_argument('--filtros', required=True)
    ap.add_argument('--executor', required=True)
    a = ap.parse_args()
    pasta = ROOT / a.pasta
    with open(ROOT / 'dados/buscas.csv', encoding='utf-8') as f:
        if any(r['id'] == a.busca_id for r in csv.DictReader(f)):
            raise SystemExit(f'Busca {a.busca_id} já registrada.')
    with open(ROOT / 'dados/registros.csv', encoding='utf-8') as f:
        if any(r['busca_id'] == a.busca_id for r in csv.DictReader(f)):
            raise SystemExit(f'Há registros de {a.busca_id} sem busca: importação parcial anterior.')
    # Ler e validar todas as entradas antes de gravar qualquer tabela.
    consulta = (pasta / 'consulta.txt').read_text().strip()
    if not consulta:
        raise SystemExit('consulta.txt vazio.')
    registros = list(LEITORES[a.leitor](pasta))
    if not registros:
        raise SystemExit('Nenhum registro lido.')
    linhas = [{'id': f'{a.busca_id}-{n:04d}', 'busca_id': a.busca_id, 'estudo_id': '', **r}
              for n, r in enumerate(registros, 1)]
    arquivo = manifesto(pasta).relative_to(ROOT).as_posix()
    acrescentar(ROOT / 'dados/registros.csv',
                ['id', 'busca_id', 'titulo', 'ano', 'doi', 'arxiv', 'estudo_id'], linhas)
    acrescentar(ROOT / 'dados/buscas.csv',
                ['id', 'data', 'base', 'consulta', 'campos_filtros', 'total_exportado',
                 'arquivo_exportacao', 'executor'],
                [{'id': a.busca_id, 'data': a.data, 'base': a.base, 'consulta': consulta,
                  'campos_filtros': a.filtros, 'total_exportado': len(linhas),
                  'arquivo_exportacao': arquivo, 'executor': a.executor}])
    print(f'{a.busca_id}: {len(linhas)} registros')


if __name__ == '__main__':
    main()
