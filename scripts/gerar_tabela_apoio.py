"""Gera a tabela de apoio v2 em LaTeX a partir de evidencias/sinteses/tabela-apoio-v2.csv (D119).

A tabela sai em duas partes (geração; depuração, tradução e refatoração), porque um float de duas
colunas não quebra página. Saída: monografia/capitulos/04c2-tabela-apoio-v2.tex.
Uso: python3 scripts/gerar_tabela_apoio.py
"""
import csv
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FONTE = RAIZ / 'evidencias/sinteses/tabela-apoio-v2.csv'
SAIDA = RAIZ / 'monografia/capitulos/04c2-tabela-apoio-v2.tex'
TAREFA = {'geracao': 'Geração', 'depuracao': 'Depuração', 'traducao': 'Tradução', 'refatoracao': 'Refatoração',
          'todas': 'Todas'}


def esc(t):
    for a, b in [('\\', r'\textbackslash{}'), ('&', r'\&'), ('%', r'\%'), ('#', r'\#'), ('_', r'\_'), ('~', r'\~{}')]:
        t = t.replace(a, b)
    return t


def tabela(linhas, legenda, rotulo):
    out = [r'\begin{table*}[!t]', r'\caption{' + legenda + r'}\label{' + rotulo + '}', r'\centering', r'\scriptsize',
           r'\setlength{\tabcolsep}{2.5pt}', r'\renewcommand*{\rr}{\raggedright\hspace{0pt}}',
           r'\begin{tabular}{p{0.55cm}p{2.0cm}p{2.4cm}p{1.9cm}p{5.6cm}p{1.6cm}p{3.1cm}}', r'\hline',
           r'\rr\textbf{ID} & \rr\textbf{Agrupamento} & \rr\textbf{Condição e verificação} & \rr\textbf{Resultado medido} & '
           r'\rr\textbf{Evidência e indicação} & \rr\textbf{Força} & \rr\textbf{Ressalvas}\tabularnewline', r'\hline']
    for r in linhas:
        ag = esc(r['agrupamento']) + (' (' + TAREFA[r['tarefa']].lower() + ')' if r['tarefa'] == 'todas' else '')
        out.append(r'\rr ' + r['id'] + r' & \rr ' + ag + r' & \rr ' + esc(r['condicao_verificacao']) + r' & \rr '
                   + esc(r['resultado_medido']) + r' & \rr \textit{' + esc(r['evidencia'].capitalize()) + '.} '
                   + esc(r['indicacao']) + r' & \rr ' + esc(r['forca']) + r' & \rr ' + esc(r['ressalvas'])
                   + r'\tabularnewline')
    out += [r'\hline', r'\end{tabular}', r'\par\smallskip',
            r'\parbox{\textwidth}{\scriptsize Evidência: favorável, contrária ou dividida, conforme a direção das '
            r'comparações; indireta, quando vem de outra condição, domínio ou métrica; insuficiente, quando o corpus não '
            r'tem contraste para a condição. Força: comparações e estudos, sem nota. Extração por IA, conferida por '
            r'amostra; sínteses das 302 fichas usadas na v1.}', r'\end{table*}']
    return '\n'.join(out)


def main():
    rows = list(csv.DictReader(open(FONTE, encoding='utf-8')))
    g = [r for r in rows if r['id'].startswith('G')]
    o = [r for r in rows if not r['id'].startswith('G')]
    txt = '% Gerado por scripts/gerar_tabela_apoio.py a partir de evidencias/sinteses/tabela-apoio-v2.csv.\n'
    txt += '\\providecommand*{\\rr}{\\raggedright\\hspace{0pt}}\n'
    txt += tabela(g, 'Tabela de apoio à escolha, versão 2: geração (G1--G12) e linhas comuns (G13--G14)', 'tab:apoio') + '\n\n'
    txt += tabela(o, 'Tabela de apoio à escolha, versão 2: depuração (D), tradução (T) e refatoração (R)', 'tab:apoiob') + '\n'
    SAIDA.write_text(txt, encoding='utf-8')
    print(len(g), '+', len(o), 'linhas')


if __name__ == '__main__':
    main()
