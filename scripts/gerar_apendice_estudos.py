"""Gera o apêndice com os estudos do corpus definitivo a partir de dados/estudos.csv.

Lista identificador do estudo, título e identificador registrado (DOI ou arXiv), sem
autores: os metadados de autoria não foram conferidos. Para os estudos registrados pelo arXiv,
usa o identificador da publicação em periódico ou anais quando dados/publicacoes.csv a traz (D135).
Uso: python3 scripts/gerar_apendice_estudos.py
"""
import csv, json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / 'monografia/capitulos/08-apendice-estudos.tex'
PUBLICACOES = RAIZ / 'dados/publicacoes.csv'
ESC = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_',
       '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}


def tex(t):
    return ''.join(ESC.get(c, c) for c in t)


def publicado(p):
    """Texto do identificador da publicação: DOI, endereço curto dos anais ou nome do evento."""
    if p['tipo'] == 'doi':
        return rf'\texttt{{{tex("doi:" + p["identificador"])}}}'
    curto = p['identificador'].split('://', 1)[-1]
    return rf'\texttt{{{tex(curto)}}}' if len(curto) <= 50 else tex(p['local'])


def montar():
    fichas = {json.loads(l)['estudo_id'] for l in open(RAIZ / 'dados/fichas.jsonl', encoding='utf-8') if l.strip()}
    est = [r for r in csv.DictReader(open(RAIZ / 'dados/estudos.csv', encoding='utf-8')) if r['corpus'] == 'definitivo']
    est.sort(key=lambda r: int(r['id'][1:]))
    ids = {r['id'] for r in est}
    pub = {p['estudo_id']: p for p in csv.DictReader(open(PUBLICACOES, encoding='utf-8'))
           if p['estudo_id'] in ids and p['tipo'] in ('doi', 'url')}
    so_arxiv = sum(1 for r in est if r['identificador'].startswith('arXiv') and r['id'] not in pub)
    linhas = [r'\section{Estudos incluídos}\label{ap:estudos}',
              f'Os {len(est)} estudos do corpus definitivo, pelo identificador usado no texto. Título e identificador vêm '
              r'dos registros das bases; ano e autoria não foram conferidos para esta lista.'
              + (rf' Os {len(pub)} estudos marcados com $\ast$ foram lidos na versão do arXiv; o identificador é o da '
                 r'publicação em periódico ou em anais, localizada em 21/11/2026 pela comparação do título e dos autores com '
                 r'os do registro do arXiv.' if pub else '')
              + (rf' Outros {so_arxiv} continuam identificados pelo arXiv, sem publicação localizada.' if pub and so_arxiv else '')
              + (r' Estudos marcados com $\dagger$ ainda não têm ficha de extração.' if any(r['id'] not in fichas for r in est) else ''),
              r'{\scriptsize\raggedright', r'\begin{description}\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}']
    for r in est:
        marca = ('' if r['id'] in fichas else r'$^\dagger$') + (r'$^\ast$' if r['id'] in pub else '')
        ident = publicado(pub[r['id']]) if r['id'] in pub else rf'\texttt{{{tex(r["identificador"])}}}'
        linhas.append(rf'\item[{r["id"]}{marca}] {tex(r["titulo"])}. {ident}.')
    linhas += [r'\end{description}', '}']
    return '\n'.join(linhas) + '\n', len(est), sum(1 for r in est if r['id'] not in fichas), len(pub)


def main():
    texto, total, sem_ficha, publicados = montar()
    SAIDA.write_text(texto, encoding='utf-8')
    print(total, 'estudos;', sem_ficha, 'sem ficha;', publicados, 'com identificador da publicação')


if __name__ == '__main__':
    main()
