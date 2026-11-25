#!/usr/bin/env python3
"""Compara cada arquivo de monografia/capitulos/ com sua tradução em monografia/capitulos-en/.

A tradução para o inglês foi feita por IA. Este script não avalia a qualidade do texto; ele acusa
divergências mecânicas que indicam número trocado, identificador perdido ou trecho omitido:

- rótulos (\\label), remissões (\\ref) e chaves de citação;
- identificadores de estudos e de comparações (S1, S6-C1) e marcas de afirmação (% AFIRMACAO: A61);
- quantidade de seções, tabelas, figuras, itens e linhas de tabela;
- números do texto, depois de normalizar separadores de milhar e de decimal e as datas.

Uso: python3 scripts/verificar_traducao.py [--raiz CAMINHO]
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

MESES_PT = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro',
            'outubro', 'novembro', 'dezembro']
MESES_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
            'October', 'November', 'December']
ESTRUTURA = [r'\\section\b', r'\\subsection\b', r'\\subsubsection\b', r'\\paragraph\b', r'\\begin\{table\*?\}',
             r'\\begin\{figure\*?\}', r'\\begin\{itemize\}', r'\\begin\{enumerate\}', r'\\begin\{description\}',
             r'\\item\b', r'\\hline\b', r'\\caption\b', r'\\tabularnewline\b', r'\\input\b']


def sem_comentarios(texto):
    """Retira comentários de LaTeX; as marcas de afirmação são lidas antes, em marcas()."""
    return '\n'.join(re.sub(r'(?<!\\)%.*', '', linha) for linha in texto.splitlines())


def marcas(texto):
    return Counter(re.findall(r'%\s*AFIRMACAO:\s*(A\d+)', texto))


def chaves(texto, comando):
    achadas = []
    for grupo in re.findall(r'\\' + comando + r'\{([^}]*)\}', texto):
        achadas.extend(c.strip() for c in grupo.split(','))
    return Counter(achadas)


def citacoes(texto):
    # \citetexto{autores}{chave} (português) e \citet{chave} (inglês) citam a mesma chave.
    texto = re.sub(r'\\citetexto\{[^}]*\}\{', r'\\citet{', texto)
    achadas = []
    for grupo in re.findall(r'\\cite[a-z]*\{([^}]*)\}', texto):
        achadas.extend(c.strip() for c in grupo.split(','))
    return Counter(achadas)


def identificadores(texto):
    return Counter(re.findall(r'\bS\d+(?:-C\d+)?\b', texto))


def estrutura(texto):
    return {padrao: len(re.findall(padrao, texto)) for padrao in ESTRUTURA}


def numeros(texto, idioma):
    """Números do texto como cadeias de dígitos, sem separadores e sem zeros à esquerda."""
    t = re.sub(r'\\citetexto\{[^}]*\}\{', r'\\citet{', texto)
    # Argumentos que não são texto: caminhos, rótulos, chaves, medidas e especificações de coluna.
    t = re.sub(r'\\(?:input|label|ref|url|texttt|includegraphics|cite[a-z]*)(?:\[[^\]]*\])?\{[^}]*\}', ' ', t)
    t = re.sub(r'\\begin\{tabular\}\{.*\}', ' ', t)
    t = re.sub(r'\\(?:fontsize|setlength|renewcommand\*?|providecommand\*?|multicolumn|hspace|vspace)'
               r'(?:\{[^}]*\})+', ' ', t)
    t = re.sub(r'\\begin\{[a-z*]+\}(?:\[[^\]]*\])?', ' ', t)
    t = re.sub(r'\[!?[htbp]+\]', ' ', t)
    t = t.replace('{,}', ',').replace('{.}', '.')
    meses = MESES_PT if idioma == 'pt' else MESES_EN
    for i, mes in enumerate(meses, 1):
        if idioma == 'pt':
            t = re.sub(r'(\d{1,2}) de ' + mes + r'\b', r'\1 %d ' % i, t)
            t = re.sub(r'\b' + mes + r' de (\d{4})', r'%d \1' % i, t)
        else:
            t = re.sub(r'(\d{1,2}) ' + mes + r'\b', r'\1 %d ' % i, t)
            t = re.sub(r'\b' + mes + r' (\d{4})', r'%d \1' % i, t)
    t = re.sub(r'(?<=\d)/(?=\d)', ' ', t)
    achados = []
    for n in re.findall(r'\d+(?:[.,]\d+)*', t):
        digitos = re.sub(r'[.,]', '', n).lstrip('0') or '0'
        achados.append(digitos)
    return Counter(achados)


def diferenca(a, b):
    falta = a - b
    sobra = b - a
    partes = []
    if falta:
        partes.append('só no português: ' + ', '.join(f'{k}×{v}' if v > 1 else k for k, v in sorted(falta.items())))
    if sobra:
        partes.append('só no inglês: ' + ', '.join(f'{k}×{v}' if v > 1 else k for k, v in sorted(sobra.items())))
    return '; '.join(partes)


def comparar(pt, en):
    """Devolve a lista de divergências entre o texto em português e o texto em inglês."""
    erros = []
    if marcas(pt) != marcas(en):
        erros.append('marcas de afirmação — ' + diferenca(marcas(pt), marcas(en)))
    pt, en = sem_comentarios(pt), sem_comentarios(en)
    for nome, funcao in (('rótulos', lambda t: chaves(t, 'label')), ('remissões', lambda t: chaves(t, 'ref')),
                         ('citações', citacoes), ('identificadores', identificadores)):
        a, b = funcao(pt), funcao(en)
        if a != b:
            erros.append(f'{nome} — ' + diferenca(a, b))
    ea, eb = estrutura(pt), estrutura(en)
    for padrao in ESTRUTURA:
        if ea[padrao] != eb[padrao]:
            erros.append(f'estrutura {padrao}: {ea[padrao]} no português, {eb[padrao]} no inglês')
    a, b = numeros(pt, 'pt'), numeros(en, 'en')
    if a != b:
        erros.append('números — ' + diferenca(a, b))
    return erros


def verificar(raiz):
    pt_dir, en_dir = raiz / 'monografia/capitulos', raiz / 'monografia/capitulos-en'
    erros = []
    if not en_dir.is_dir():
        return erros
    nomes_pt = {p.name for p in pt_dir.glob('*.tex')} - {'00-resumo.tex'}
    nomes_en = {p.name for p in en_dir.glob('*.tex')}
    for nome in sorted(nomes_pt - nomes_en):
        erros.append(f'{nome}: sem tradução em capitulos-en/')
    for nome in sorted(nomes_en - nomes_pt):
        erros.append(f'{nome}: tradução sem original em capitulos/')
    for nome in sorted(nomes_pt & nomes_en):
        pt = (pt_dir / nome).read_text(encoding='utf-8')
        en = (en_dir / nome).read_text(encoding='utf-8')
        erros.extend(f'{nome}: {e}' for e in comparar(pt, en))
    return erros


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raiz', default=Path(__file__).resolve().parents[1], type=Path)
    args = parser.parse_args()
    erros = verificar(args.raiz)
    for e in erros:
        print('ERRO', e)
    print(f'Tradução: {len(erros)} divergência(s).')
    return 1 if erros else 0


if __name__ == '__main__':
    sys.exit(main())
