"""Validação dos rótulos de uma saída de extração ex-v2.2 (D102).

Confere enumerações e coerências simples antes de aceitar o JSON de uma rodada. Não
confere conteúdo: valores, citações e julgamentos continuam dependendo da conferência.

Uso: python3 scripts/validar_ficha_extracao.py arquivo.json [arquivo.json ...]
"""
import json
import sys

TAREFAS = {'geracao', 'traducao', 'refatoracao', 'depuracao'}
MECANISMOS = {'instrucao', 'exemplos', 'raciocinio', 'decomposicao', 'contexto', 'feedback',
              'multiagente', 'restricoes', 'amostragem', 'otimizacao_prompt', 'outro'}
PAPEIS = {'focal', 'comparador', 'componente'}
SIM_NAO = {'sim', 'nao'}
CONTRAFACTUAL = {'pacote': 'sim', 'ingrediente': 'sim', 'contraste_pareado': 'sim',
                 'cumulativo': 'nao', 'nenhum': 'nao'}
NATUREZA = {'ajuste_fino', 'embeddings_aprendidos', 'decodificacao', 'orcamento',
            'selecao_modelo', 'outro'}
RISCOS = {'correcao_funcional', 'seguranca', 'alucinacao', 'contaminacao',
          'nao_determinismo', 'custo', 'manutenibilidade', 'outro'}
SENTIDO = {'maior_melhor', 'menor_melhor'}
UNIDADE = {'percentual', 'proporcao', 'contagem', 'tempo', 'qualitativo'}
SELECAO = {'principal_declarado', 'desempate_ordem', 'cobertura'}
DERIVACAO = {'direta', 'contraste_pareado'}
CRITERIOS = ['objetivo', 'procedimento', 'comparador', 'metricas', 'ameacas',
             'reprodutibilidade', 'contaminacao']
JULGAMENTOS = {'atende', 'parcial', 'nao_atende', 'nao_informado'}


def validar(d):
    erros = []

    def err(onde, msg):
        erros.append(f'{onde}: {msg}')

    def enum(onde, valor, permitidos):
        if valor not in permitidos:
            err(onde, f'{valor!r} fora de {sorted(permitidos)}')

    def mecs(onde, lista):
        if not isinstance(lista, list):
            err(onde, 'não é lista')
            return set()
        for m in lista:
            enum(onde, m, MECANISMOS)
        return set(lista)

    for parte in ('ficha', 'extracoes', 'qualidade', 'leitura'):
        if parte not in d:
            err(parte, 'ausente')
    f = d.get('ficha', {})
    for t in f.get('tarefas', []):
        enum('ficha.tarefas', t, TAREFAS)
    for i, t in enumerate(f.get('tecnicas', [])):
        o = f'ficha.tecnicas[{i}] {t.get("nome_original", "")[:40]!r}'
        todos = mecs(o + '.mecanismos', t.get('mecanismos'))
        acres = mecs(o + '.mecanismos_acrescentados', t.get('mecanismos_acrescentados', []))
        if not acres <= todos:
            err(o, f'acrescentados fora de mecanismos: {sorted(acres - todos)}')
        enum(o + '.papel', t.get('papel'), PAPEIS)
        enum(o + '.avaliada_isoladamente', t.get('avaliada_isoladamente'), SIM_NAO)
        tc = t.get('tipo_contrafactual')
        enum(o + '.tipo_contrafactual', tc, CONTRAFACTUAL)
        if tc in CONTRAFACTUAL and t.get('avaliada_isoladamente') != CONTRAFACTUAL[tc]:
            err(o, f'tipo_contrafactual {tc} exige avaliada_isoladamente={CONTRAFACTUAL[tc]}')
    for i, c in enumerate(f.get('componentes_fora_escopo', [])):
        enum(f'ficha.componentes_fora_escopo[{i}].natureza', c.get('natureza'), NATUREZA)
    for i, r in enumerate(f.get('riscos', [])):
        enum(f'ficha.riscos[{i}].categoria', r.get('categoria'), RISCOS)
    for i, m in enumerate(f.get('mitigacoes', [])):
        enum(f'ficha.mitigacoes[{i}].avaliada', m.get('avaliada'), SIM_NAO)
    enum('ficha.sem_comparador', f.get('sem_comparador'), SIM_NAO)

    ex = d.get('extracoes', [])
    if len(ex) > 3 and not any('exce' in (e.get('selecao_motivo') or '').lower() for e in ex):
        err('extracoes', f'{len(ex)} comparações sem motivo de exceção')
    for i, e in enumerate(ex):
        o = f'extracoes[{i}]'
        enum(o + '.tarefa', e.get('tarefa'), TAREFAS)
        todos = mecs(o + '.mecanismos', e.get('mecanismos'))
        acres = mecs(o + '.mecanismos_acrescentados', e.get('mecanismos_acrescentados', []))
        if not acres <= todos:
            err(o, f'acrescentados fora de mecanismos: {sorted(acres - todos)}')
        enum(o + '.sentido', e.get('sentido'), SENTIDO)
        enum(o + '.unidade', e.get('unidade'), UNIDADE)
        enum(o + '.selecao', e.get('selecao'), SELECAO)
        enum(o + '.derivacao', e.get('derivacao'), DERIVACAO)
        enum(o + '.conferido_pdf', e.get('conferido_pdf'), SIM_NAO)
        res = e.get('resultado')
        if res is not None:
            for k in ('baseline', 'intervencao'):
                v = res.get(k)
                if v is not None and not isinstance(v, (int, float)):
                    err(o + f'.resultado.{k}', f'{v!r} não numérico')
            if e.get('comparador') is None and res.get('baseline') is not None:
                err(o, 'comparador null com baseline preenchido')
        if e.get('comparador') is None and f.get('sem_comparador') != 'sim' and \
                (res or {}).get('baseline') is None and 'prosa' not in (e.get('selecao_motivo') or ''):
            err(o, 'resultado sem comparador exige sem_comparador=sim na ficha')

    q = d.get('qualidade', [])
    if [x.get('criterio') for x in q] != CRITERIOS:
        err('qualidade', f'critérios {[x.get("criterio") for x in q]} ≠ {CRITERIOS}')
    for x in q:
        enum(f'qualidade.{x.get("criterio")}', x.get('julgamento'), JULGAMENTOS)
    return erros


def main(caminhos):
    falhou = False
    for c in caminhos:
        erros = validar(json.load(open(c, encoding='utf-8')))
        print(f'{c}: {"ok" if not erros else str(len(erros)) + " erro(s)"}')
        for e in erros:
            print('  -', e)
        falhou |= bool(erros)
    return 1 if falhou else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
