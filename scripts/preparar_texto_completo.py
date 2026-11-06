#!/usr/bin/env python3
"""Sorteia estudos do texto completo, obtém as versões abertas e extrai o texto (D64).

Sorteia N estudos de uma etapa de evidencias/lote/texto-completo.csv que têm
acesso_aberto=sim e ainda não foram obtidos. Baixa os PDFs para fontes/artigos/lote/ e
extrai o texto com Ghostscript em modo seguro para fontes/textos/lote/ (ambos fora do
Git; os PDFs não são executados). Acrescenta fonte, hash e situação em
evidencias/lote/textos.csv.
"""
import argparse
import csv
import pathlib
import random
import re
import subprocess
import time

from preparar_medicao_texto import baixar

ROOT = pathlib.Path(__file__).resolve().parents[1]
PDFS = ROOT / 'fontes/artigos/lote'
TEXTOS = ROOT / 'fontes/textos/lote'
QUADRO = ROOT / 'evidencias/lote/textos.csv'
CAMPOS = ['estudo_id', 'etapa', 'semente', 'url', 'situacao', 'bytes', 'sha256', 'caracteres', 'data']


def ler(caminho):
    with open(ROOT / caminho, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def url_aberta(sid, registros, versoes):
    """Prefere o arXiv; depois o DOI da ACM; depois a versão aberta localizada no OpenAlex."""
    proprios = [r for r in registros if r['estudo_id'] == sid]
    arxiv = next((r['arxiv'] for r in proprios if r['arxiv']), '')
    if arxiv:
        return f'https://arxiv.org/pdf/{arxiv}'
    acm = next((r['doi'] for r in proprios if r['busca_id'] == 'B3' and r['doi']), '')
    if acm:
        return f'https://dl.acm.org/doi/pdf/{acm}'
    return versoes.get(sid, '')


def extrair(pdf, destino):
    """Texto do PDF sem figuras, com espaços compactados."""
    saida = subprocess.run(['gs', '-q', '-dSAFER', '-dBATCH', '-dNOPAUSE', '-sDEVICE=txtwrite',
                            '-sOutputFile=-', str(pdf)], capture_output=True, timeout=300)
    texto = saida.stdout.decode('utf-8', errors='replace')
    texto = '\n'.join(re.sub(r'[ \t]{2,}', ' ', linha).strip() for linha in texto.splitlines())
    texto = re.sub(r'\n{3,}', '\n\n', texto)
    destino.write_text(texto, encoding='utf-8')
    return len(texto)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, required=True)
    ap.add_argument('--etapa', default='1')
    ap.add_argument('--semente', type=int, required=True)
    ap.add_argument('--data', required=True)
    a = ap.parse_args()
    estudos = {e['id']: e for e in ler('dados/estudos.csv')}
    registros = ler('dados/registros.csv')
    versoes = {v['estudo_id']: v['url'] for v in ler('dados/versoes_abertas.csv')}
    feitos = {x['estudo_id'] for x in ler('evidencias/lote/textos.csv')} if QUADRO.exists() else set()
    universo = [x['estudo_id'] for x in ler('evidencias/lote/texto-completo.csv')
                if x['etapa'] == a.etapa and estudos[x['estudo_id']]['acesso_aberto'] == 'sim'
                and x['estudo_id'] not in feitos]
    amostra = random.Random(a.semente).sample(universo, min(a.n, len(universo)))
    PDFS.mkdir(parents=True, exist_ok=True)
    TEXTOS.mkdir(parents=True, exist_ok=True)
    novo = not QUADRO.exists()
    with open(QUADRO, 'a', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS, lineterminator='\n')
        if novo:
            w.writeheader()
        for sid in amostra:
            url = url_aberta(sid, registros, versoes)
            situacao, tamanho, sha = baixar(url, PDFS / f'{sid}.pdf') if url else ('fonte_indisponivel: sem URL', 0, '')
            caracteres = extrair(PDFS / f'{sid}.pdf', TEXTOS / f'{sid}.txt') if situacao == 'obtido' else 0
            w.writerow({'estudo_id': sid, 'etapa': a.etapa, 'semente': a.semente, 'url': url, 'situacao': situacao,
                        'bytes': tamanho, 'sha256': sha, 'caracteres': caracteres, 'data': a.data})
            print(sid, situacao, tamanho, caracteres, flush=True)
            time.sleep(3)
    print(f'{len(amostra)} de {len(universo)} estudos da etapa {a.etapa}; semente {a.semente}')


if __name__ == '__main__':
    main()
