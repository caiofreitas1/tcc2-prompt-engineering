"""Gera o apêndice com os estudos do corpus definitivo a partir de dados/estudos.csv.

Lista identificador do estudo, título e identificador registrado (DOI ou arXiv), sem
autores: os metadados de autoria não foram conferidos. Uso: python3 scripts/gerar_apendice_estudos.py
"""
import csv, json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / 'monografia/capitulos/08-apendice-estudos.tex'
ESC = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_',
       '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}


def tex(t):
    return ''.join(ESC.get(c, c) for c in t)


def main():
    fichas = {json.loads(l)['estudo_id'] for l in open(RAIZ / 'dados/fichas.jsonl', encoding='utf-8') if l.strip()}
    est = [r for r in csv.DictReader(open(RAIZ / 'dados/estudos.csv', encoding='utf-8')) if r['corpus'] == 'definitivo']
    est.sort(key=lambda r: int(r['id'][1:]))
    linhas = [r'\section{Estudos incluídos}\label{ap:estudos}',
              f'Os {len(est)} estudos do corpus definitivo, pelo identificador usado no texto. Título e identificador vêm '
              r'dos registros das bases; ano e autoria não foram conferidos para esta lista. Estudos marcados com $\dagger$ '
              'ainda não têm ficha de extração.',
              r'{\scriptsize', r'\begin{description}\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}']
    for r in est:
        marca = '' if r['id'] in fichas else r'$^\dagger$'
        linhas.append(rf'\item[{r["id"]}{marca}] {tex(r["titulo"])}. \texttt{{{tex(r["identificador"])}}}.')
    linhas += [r'\end{description}', '}']
    SAIDA.write_text('\n'.join(linhas) + '\n', encoding='utf-8')
    print(len(est), 'estudos;', sum(1 for r in est if r['id'] not in fichas), 'sem ficha')


if __name__ == '__main__':
    main()
