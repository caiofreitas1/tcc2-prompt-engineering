#!/usr/bin/env python3
"""Recalcula as contagens de seleção da revisão rápida (T05 e T06) em dados/fluxos.csv.

Mantém as linhas de busca e deduplicação e refaz as demais a partir de dados/triagem.csv,
evidencias/lote/texto-completo.csv, evidencias/lote/textos.csv e dados/estudos.csv.
Imprime as contagens; com --gravar, reescreve dados/fluxos.csv.
"""
import argparse
import collections
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANTER = {'identificados_arxiv', 'identificados_ieee', 'identificados_acm', 'identificados_bases',
          'duplicatas_removidas', 'estudos_unicos'}
CAMPOS = ['etapa', 'contagem', 'denominador', 'regra', 'origem', 'data']


def ler(rel):
    return list(csv.DictReader(open(ROOT / rel, encoding='utf-8', newline='')))


def contar():
    tri = ler('dados/triagem.csv')
    ia = collections.defaultdict(dict)
    autor = collections.defaultdict(dict)
    for x in tri:
        alvo = ia if x['natureza'] == 'ia' else autor
        alvo[x['fase']].setdefault(x['estudo_id'], {})[x['responsavel']] = x['decisao']
    tr = ia['titulo_resumo']
    segue = {i for i, d in tr.items() if {'incluir', 'duvida'} & set(d.values())}
    cons_tr = set(tr) - segue
    aut_tr = {i: list(d.values())[-1] for i, d in autor['titulo_resumo'].items()}
    tc = ler('evidencias/lote/texto-completo.csv')
    etapas = collections.Counter(x['etapa'] for x in tc)
    origem = collections.Counter(x['origem'] for x in tc)
    textos = ler('evidencias/lote/textos.csv')
    def situacoes(etapa):
        return collections.Counter(x['situacao'].split(':')[0].split(' (')[0] for x in textos if x['etapa'] == etapa)
    sit, sit3 = situacoes('1'), situacoes('3')
    lidos = ia['texto_completo']
    aut_tc = {i: list(d.values())[-1] for i, d in autor['texto_completo'].items()}
    dec_tc = collections.Counter(aut_tc.values())
    cons_tc = {i for i, d in lidos.items() if set(d.values()) == {'excluir'}}
    definitivo = sum(x['corpus'] == 'definitivo' for x in ler('dados/estudos.csv'))
    T, E, X, S = ('dados/triagem.csv', 'evidencias/lote/texto-completo.csv',
                  'evidencias/lote/textos.csv', 'dados/estudos.csv')
    return [
        ('triados_titulo_resumo', len(tr), 'estudos do lote (candidatos com a tarefa no título e S1, S2, S4, S6)',
         'estudos com decisão de IA-A e IA-B com tr-v2 (D65)', T),
        ('seguem_regra_uniao', len(segue), 'triados_titulo_resumo',
         'ao menos um modelo decidiu incluir ou duvida', T),
        ('exclusoes_consensuais_titulo_resumo', len(cons_tr), 'triados_titulo_resumo',
         'os dois modelos decidiram excluir', T),
        ('conferidas_autor_titulo_resumo', len(aut_tr), 'exclusoes_consensuais_titulo_resumo',
         'decisões do autor na conferência das exclusões (D67)', T),
        ('resgatados_conferencia', origem['resgate_conferencia'], 'conferidas_autor_titulo_resumo',
         'autor decidiu incluir ou duvida (D66)', E),
        ('resgatados_amostras', origem['resgate_amostra'], 'exclusoes_consensuais_titulo_resumo',
         'incluir ou duvida do autor nas amostras de calibração (D66)', E),
        ('texto_completo_total', len(tc), 'triados_titulo_resumo', 'seguem pela união ou por resgate', E),
        ('texto_completo_etapa1', etapas['1'], 'texto_completo_total',
         'indício de revisão por pares e texto aberto (D64, D69)', E),
        ('texto_completo_etapa2', etapas['2'], 'texto_completo_total', 'demais com acesso aberto', E),
        ('texto_completo_etapa3', etapas['3'], 'texto_completo_total', 'acesso institucional CAPES/UFMG (D69)', E),
        ('etapa1_texto_extraido', sit['obtido'], 'texto_completo_etapa1',
         'PDF obtido e texto extraído', X),
        ('etapa1_sem_texto_extraido', sit['obtido_sem_texto'], 'texto_completo_etapa1',
         'PDF obtido, extração excedeu 300 s', X),
        ('etapa1_pdf_pendente', sit['fonte_indisponivel'], 'texto_completo_etapa1',
         'PDF ainda não obtido ou sem PDF disponível', X),
        ('etapa3_texto_extraido', sit3['obtido'], 'texto_completo_etapa3',
         'PDF baixado pelo autor pelo acesso institucional e texto extraído (D86)', X),
        ('lidos_ia_texto_completo', len(lidos), 'etapa1_texto_extraido',
         'estudos com decisão de IA-A e IA-B com tc-v2', T),
        ('exclusoes_consensuais_texto_completo', len(cons_tc), 'lidos_ia_texto_completo',
         'os dois modelos decidiram excluir', T),
        ('conferidos_autor_texto_completo', len(aut_tc), 'lidos_ia_texto_completo',
         'última decisão do autor por estudo (D78-D81)', T),
        ('incluidos_autor_texto_completo', dec_tc['incluir'], 'conferidos_autor_texto_completo',
         'autor decidiu incluir', T),
        ('duvida_autor_texto_completo', dec_tc['duvida'], 'conferidos_autor_texto_completo',
         'autor decidiu duvida', T),
        ('excluidos_autor_texto_completo', dec_tc['excluir'], 'conferidos_autor_texto_completo',
         'autor decidiu excluir', T),
        ('exclusoes_consensuais_incluidas_autor', sum(aut_tc.get(i) == 'incluir' for i in cons_tc),
         'exclusoes_consensuais_texto_completo', 'os dois modelos excluíram e o autor incluiu', T),
        ('corpus_definitivo', definitivo, 'conferidos_autor_texto_completo',
         'corpus=definitivo (decisão humana incluir no texto completo)', S),
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gravar', action='store_true')
    ap.add_argument('--data', default='2026-11-08')
    a = ap.parse_args()
    linhas = contar()
    for etapa, n, *_ in linhas:
        print(f'{etapa}: {n}')
    if a.gravar:
        antigas = [x for x in ler('dados/fluxos.csv') if x['etapa'] in MANTER]
        novas = [dict(zip(CAMPOS, (e, n, d, r, o, a.data))) for e, n, d, r, o in linhas]
        with open(ROOT / 'dados/fluxos.csv', 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=CAMPOS, lineterminator='\n')
            w.writeheader()
            w.writerows(antigas + novas)


if __name__ == '__main__':
    main()
