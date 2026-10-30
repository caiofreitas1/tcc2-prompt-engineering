#!/usr/bin/env python3
"""Agrupa os registros de dados/registros.csv em estudos (protocolo, seção 5).

Registros com o mesmo DOI, identificador arXiv ou título normalizado formam um
grupo (versões sobrepostas também se agrupam, critério X1). Grupos já ligados a um
estudo de dados/estudos.csv mantêm o ID; os demais recebem novo ID (S7, S8...) com
corpus `candidato`; candidatos sem registros são removidos. Grupos unidos pelo título
com anos distantes ou DOIs distintos são listados para conferência na triagem.
Pode ser reexecutado depois de novas buscas.
"""
import collections
import csv
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
CAMPOS_ESTUDOS = ['id', 'titulo', 'identificador', 'versao', 'ano', 'origem', 'corpus',
                  'metadados_conferidos', 'fonte_primaria', 'acesso_aberto']
# S6 foi lido no ECOOP 2025 (DOI); a versão arXiv do mesmo trabalho consta do protocolo, 4.3.
CHAVES_EXTRAS = {'S6': ['arxiv:2501.13978']}


def titulo_norm(t):
    return re.sub(r'[^a-z0-9]', '', t.lower())


def chaves(reg):
    ks = []
    if reg.get('doi'):
        ks.append('doi:' + reg['doi'].lower())
    if reg.get('arxiv'):
        ks.append('arxiv:' + reg['arxiv'])
    if len(titulo_norm(reg.get('titulo', ''))) >= 20:
        ks.append('ti:' + titulo_norm(reg['titulo']))
    return ks


def chaves_estudo(s):
    ident = s['identificador']
    ks = []
    if ident.lower().startswith('doi:'):
        ks.append('doi:' + ident[4:].lower())
    elif ident.startswith('arXiv:'):
        ks.append('arxiv:' + ident[6:])
    if len(titulo_norm(s['titulo'])) >= 20:
        ks.append('ti:' + titulo_norm(s['titulo']))
    return ks + CHAVES_EXTRAS.get(s['id'], [])


class Uniao:
    def __init__(self):
        self.pai = {}

    def achar(self, x):
        self.pai.setdefault(x, x)
        while self.pai[x] != x:
            self.pai[x] = self.pai[self.pai[x]]
            x = self.pai[x]
        return x

    def unir(self, a, b):
        self.pai[self.achar(a)] = self.achar(b)


def ler(nome):
    with open(ROOT / 'dados' / nome, encoding='utf-8') as f:
        return list(csv.DictReader(f))


def gravar(nome, campos, linhas):
    with open(ROOT / 'dados' / nome, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=campos, lineterminator='\n')
        w.writeheader()
        w.writerows(linhas)


def main():
    registros, estudos = ler('registros.csv'), ler('estudos.csv')
    u = Uniao()
    suspeitos = []
    por_titulo = collections.defaultdict(list)
    for r in registros:
        ks = chaves(r)
        for k in ks:
            if not k.startswith('ti:'):
                u.unir('r:' + r['id'], k)
        u.achar('r:' + r['id'])
        for k in ks:
            if k.startswith('ti:'):
                por_titulo[k].append(r)
    for s in estudos:
        for k in chaves_estudo(s):
            if not k.startswith('ti:'):
                u.unir('s:' + s['id'], k)
            else:
                por_titulo[k].append({'id': 's:' + s['id'], 'ano': s['ano'], 'doi': ''})
    # Títulos iguais unem grupos, salvo indício de trabalhos distintos.
    for k, regs in por_titulo.items():
        anos = {int(r['ano']) for r in regs if r.get('ano', '').isdigit()}
        dois = {r['doi'] for r in regs if r.get('doi') and 'arxiv' not in r['doi']}
        nos = [r['id'] if r['id'].startswith('s:') else 'r:' + r['id'] for r in regs]
        if (anos and max(anos) - min(anos) > 2) or len(dois) > 1:
            suspeitos.append((k, [r['id'] for r in regs], sorted(anos), sorted(dois)))
        for n in nos[1:]:
            u.unir(nos[0], n)
    grupo_estudo = {}
    for s in estudos:
        grupo_estudo.setdefault(u.achar('s:' + s['id']), s['id'])
    proximo = max(int(s['id'][1:]) for s in estudos) + 1
    grupos = collections.defaultdict(list)
    for r in registros:
        grupos[u.achar('r:' + r['id'])].append(r)
    novos = []
    for g, regs in grupos.items():
        sid = grupo_estudo.get(g)
        if sid is None:
            sid = f'S{proximo}'
            proximo += 1
            grupo_estudo[g] = sid
            base = next((r for r in regs if r['doi'] and 'arxiv' not in r['doi']), regs[0])
            ident = f"doi:{base['doi']}" if base['doi'] and 'arxiv' not in base['doi'] else f"arXiv:{base['arxiv']}"
            anos = [int(r['ano']) for r in regs if r['ano'].isdigit()]
            aberto = 'sim' if any(r['arxiv'] or r['doi'].startswith('10.1145/') for r in regs) else 'nao_conferido'
            novos.append({'id': sid, 'titulo': base['titulo'], 'identificador': ident,
                          'versao': 'nao_conferido', 'ano': min(anos) if anos else '',
                          'origem': 'busca_T04', 'corpus': 'candidato',
                          'metadados_conferidos': 'nao', 'fonte_primaria': 'nao_conferido',
                          'acesso_aberto': aberto})
        for r in regs:
            r['estudo_id'] = sid
    gravar('registros.csv', ['id', 'busca_id', 'titulo', 'ano', 'doi', 'arxiv', 'estudo_id'], registros)
    usados = {r['estudo_id'] for r in registros}
    estudos = [s for s in estudos if s['corpus'] != 'candidato' or s['id'] in usados]
    gravar('estudos.csv', CAMPOS_ESTUDOS, estudos + novos)
    print(f'{len(registros)} registros; {len(grupos)} estudos; {len(novos)} novos')
    for k, ids, anos, dois in suspeitos:
        print('CONFERIR', k[3:60], ids, anos, dois)


if __name__ == '__main__':
    main()
