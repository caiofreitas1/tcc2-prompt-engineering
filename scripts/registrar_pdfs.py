#!/usr/bin/env python3
"""Registra PDFs baixados para os estudos pendentes das etapas 1 e 3 (D85).

Procura PDFs numa pasta (padrão: ~/Downloads), só os modificados a partir de --desde, e os associa a estudos pendentes de
evidencias/lote/pdfs-pendentes.csv (etapa 1) ou evidencias/lote/capes-lista.csv (etapa 3), por:
1. nome do arquivo igual a `salvar_como` (ex.: S123.pdf);
2. sufixo do DOI no nome do arquivo (ex.: 3643795.3648391.pdf, como a ACM salva);
3. título do estudo nas duas primeiras páginas do PDF, quando só um estudo combina.
Confere o cabeçalho %PDF-, move o arquivo para fontes/artigos/lote/<id>.pdf, extrai o texto com
o mesmo Ghostscript de preparar_texto_completo.py e atualiza evidencias/lote/textos.csv. Arquivos
sem correspondência ficam onde estão. Sem --gravar, só mostra as correspondências.
"""
import argparse
import csv
import datetime as dt
import hashlib
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from preparar_texto_completo import CAMPOS, PDFS, QUADRO, TEXTOS, extrair  # noqa: E402

PENDENTES = ROOT / 'evidencias/lote/pdfs-pendentes.csv'
CAPES = ROOT / 'evidencias/lote/capes-lista.csv'


def ler(caminho):
    with open(caminho, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def norm(texto):
    return re.sub(r'[^a-z0-9]', '', texto.lower())


def inicio_do_pdf(pdf):
    try:
        saida = subprocess.run(['gs', '-q', '-dSAFER', '-dBATCH', '-dNOPAUSE', '-dFirstPage=1', '-dLastPage=2',
                                '-sDEVICE=txtwrite', '-sOutputFile=-', str(pdf)], capture_output=True, timeout=60)
    except subprocess.TimeoutExpired:
        return ''
    return norm(saida.stdout.decode('utf-8', errors='replace'))


def doi_de(item):
    m = re.search(r'10\.\d{4,}/[^\s?#]+', item.get('doi') or item.get('link') or '')
    return m.group(0).lower() if m else ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', default=str(pathlib.Path.home() / 'Downloads'))
    ap.add_argument('--data', required=True)
    ap.add_argument('--desde', required=True,
                    help='data e hora local (AAAA-MM-DDTHH:MM); arquivos anteriores não são lidos')
    ap.add_argument('--obtido-por', default='download do autor')
    ap.add_argument('--gravar', action='store_true')
    a = ap.parse_args()

    quadro = ler(QUADRO)
    obtidos = {x['estudo_id'] for x in quadro if x['situacao'].startswith('obtido') and
               not x['situacao'].startswith('obtido_sem')}
    pend = {x['estudo_id']: dict(x, etapa='1') for x in ler(PENDENTES)}
    pend.update({x['estudo_id']: dict(x, etapa='3') for x in ler(CAPES)})
    pend = {i: x for i, x in pend.items() if i not in obtidos}
    titulos = {i: norm(x['titulo'])[:80] for i, x in pend.items()}

    achados = {}
    desde = dt.datetime.fromisoformat(a.desde).timestamp()
    for pdf in sorted(pathlib.Path(a.dir).glob('*.pdf')):
        if pdf.stat().st_mtime < desde:
            continue
        if pdf.read_bytes()[:5] != b'%PDF-':
            print(f'{pdf.name}: não é PDF')
            continue
        nome = pdf.name.lower()
        cand = [i for i, x in pend.items() if nome == x['salvar_como'].lower()]
        if not cand:
            cand = [i for i, x in pend.items() if doi_de(x) and doi_de(x).split('/', 1)[1] in nome]
        if not cand:
            texto = inicio_do_pdf(pdf)
            cand = [i for i, t in titulos.items() if len(t) >= 20 and t in texto]
        if len(cand) != 1:
            print(f'{pdf.name}: {"sem correspondência" if not cand else "ambíguo " + ",".join(cand)}')
            continue
        sid = cand[0]
        if sid in achados:
            print(f'{pdf.name}: {sid} já associado a {achados[sid].name}; ignorado')
            continue
        achados[sid] = pdf
        print(f'{pdf.name} -> {sid} (etapa {pend[sid]["etapa"]})')

    if not a.gravar:
        return
    por_id = {x['estudo_id']: x for x in quadro}
    for sid, pdf in achados.items():
        dados = pdf.read_bytes()
        destino = PDFS / f'{sid}.pdf'
        shutil.move(pdf, destino)
        caracteres = extrair(destino, TEXTOS / f'{sid}.txt')
        situacao = f'obtido ({a.obtido_por})' if caracteres else 'obtido_sem_texto: extração excedeu 300 s'
        linha = por_id.get(sid)
        if linha is None:
            linha = {'estudo_id': sid, 'etapa': pend[sid]['etapa'], 'semente': '', 'url': pend[sid]['link']}
            quadro.append(linha)
        linha.update(situacao=situacao, bytes=len(dados), sha256=hashlib.sha256(dados).hexdigest(),
                     caracteres=caracteres, data=a.data)
        print(sid, situacao, len(dados), caracteres, flush=True)
    with open(QUADRO, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS, lineterminator='\n')
        w.writeheader()
        w.writerows(quadro)
    restantes = [x for x in ler(PENDENTES) if x['estudo_id'] not in achados]
    with open(PENDENTES, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['estudo_id', 'titulo', 'link', 'salvar_como'], lineterminator='\n')
        w.writeheader()
        w.writerows(restantes)


if __name__ == '__main__':
    main()
