"""Tabelas descritivas da síntese (T08) a partir de dados/fichas.jsonl, extracoes.jsonl e qualidade.csv.

Contagens por estudos distintos, salvo quando a unidade é a comparação. Nenhuma tabela
calcula média entre benchmarks ou ranqueia técnicas. A direção de cada comparação
(melhora, piora, igual) só é dada quando há sentido definido e dois números (D106), e
descreve a comparação extraída, não o efeito de um mecanismo isolado.

Uso: python3 scripts/sintetizar.py  (grava em evidencias/sinteses/tabelas/)
"""
import csv, json, collections, re, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / 'scripts'))
from validar_ficha_extracao import variacao, MECANISMOS, RISCOS

SAIDA = RAIZ / 'evidencias/sinteses/tabelas'
TAREFAS = ['geracao', 'depuracao', 'traducao', 'refatoracao']
MEC = ['instrucao', 'contexto', 'restricoes', 'exemplos', 'decomposicao', 'feedback', 'raciocinio',
       'amostragem', 'multiagente', 'otimizacao_prompt', 'outro']
CRIT = ['objetivo', 'procedimento', 'comparador', 'metricas', 'ameacas', 'reprodutibilidade', 'contaminacao']
JULG = ['atende', 'parcial', 'nao_atende', 'nao_informado']
FAMILIAS = [  # ordem importa: o primeiro padrão que casar define a família
    ('GPT-4 / GPT-4o / GPT-4.x', r'gpt-?4'), ('GPT-5', r'gpt-?5'), ('GPT-3.5 / ChatGPT', r'gpt-?3\.5|chatgpt'),
    ('Codex / davinci', r'codex|davinci'), ('OpenAI o-series', r'\bo[134](-mini|-preview)?\b'),
    ('Claude', r'claude'), ('Gemini / PaLM / Bard', r'gemini|palm|bard|gemma'),
    ('Code Llama', r'code ?llama'), ('Llama', r'llama'), ('DeepSeek', r'deepseek'), ('Qwen', r'qwen'),
    ('StarCoder / SantaCoder', r'starcoder|santacoder'), ('Mistral / Mixtral / Codestral', r'mistral|mixtral|codestral'),
    ('Phi', r'\bphi'), ('WizardCoder', r'wizard'), ('CodeGen / CodeT5', r'codegen|codet5'), ('Copilot', r'copilot'),
]
BENCH = [('HumanEval (e variantes)', r'humaneval'), ('MBPP (e variantes)', r'mbpp'), ('APPS', r'\bapps\b'),
         ('CodeContests', r'codecontests|code contests'), ('LiveCodeBench', r'livecodebench'),
         ('ClassEval', r'classeval'), ('Defects4J', r'defects4j'), ('QuixBugs', r'quixbugs'),
         ('SWE-bench', r'swe-?bench'), ('BigCodeBench', r'bigcodebench'), ('CodeNet / Avatar / transcoder', r'codenet|avatar|transcoder'),
         ('LeetCode', r'leetcode'), ('DS-1000', r'ds-?1000'), ('CoderEval', r'codereval'), ('xCodeEval', r'xcodeeval')]


def ler():
    F = [json.loads(l) for l in open(RAIZ / 'dados/fichas.jsonl', encoding='utf-8') if l.strip()]
    E = [json.loads(l) for l in open(RAIZ / 'dados/extracoes.jsonl', encoding='utf-8') if l.strip()]
    E = [e for e in E if e.get('prompt_versao') == 'ex-v2.2']
    Q = list(csv.DictReader(open(RAIZ / 'dados/qualidade.csv', encoding='utf-8')))
    S = {r['id']: r for r in csv.DictReader(open(RAIZ / 'dados/estudos.csv', encoding='utf-8'))}
    return F, E, Q, S


def gravar(nome, cab, linhas):
    with open(SAIDA / nome, 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(cab)
        w.writerows(linhas)


def nm(x):
    if isinstance(x, str):
        return x
    if isinstance(x, dict):
        return ' '.join(str(x.get(k) or '') for k in ('nome', 'versao'))
    return str(x)


def familias(texto):
    t = texto.lower()
    for nome, p in FAMILIAS:
        if re.search(p, t):
            return nome
    return None


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    F, E, Q, S = ler()
    N = len(F)
    md = [f'# Síntese descritiva (tabelas geradas por `scripts/sintetizar.py`)\n',
          f'Fichas: {N}; comparações ex-v2.2: {len(E)}. Extração por IA; conferência humana em andamento (D109, D110).\n']

    # 1. Corpus: ano e tarefas
    anos = collections.Counter(S[f['estudo_id']]['ano'] for f in F)
    gravar('01-ano.csv', ['ano', 'estudos'], sorted(anos.items()))
    tar = collections.Counter(t for f in F for t in f['tarefas'])
    combos = collections.Counter('+'.join(sorted(f['tarefas'])) for f in F)
    gravar('02-tarefas.csv', ['tarefa', 'estudos'], [(t, tar[t]) for t in TAREFAS])
    gravar('02b-combinacoes-tarefas.csv', ['tarefas', 'estudos'], combos.most_common())
    md.append('## Corpus\n')
    md.append('Ano (registro): ' + '; '.join(f'{a}: {n}' for a, n in sorted(anos.items())) + '.\n')
    md.append('Tarefas (multirrótulo): ' + '; '.join(f'{t}: {tar[t]}' for t in TAREFAS) + f'; estudos com mais de uma tarefa: {sum(1 for f in F if len(f["tarefas"]) > 1)}.\n')

    # 2. Modelos, benchmarks, linguagens (estudos distintos)
    fam = collections.Counter(); bench = collections.Counter(); ling = collections.Counter(); nmod = []
    for f in F:
        fs = {familias(nm(m)) for m in f['modelos']} - {None}
        fam.update(fs); nmod.append(len(f['modelos']))
        bs = set()
        for b in f['benchmarks']:
            for nome, p in BENCH:
                if re.search(p, nm(b).lower()):
                    bs.add(nome)
        bench.update(bs)
        ling.update({nm(l).split(' ')[0].strip() if isinstance(l, dict) else l.strip() for l in f['linguagens']})
    gravar('03-familias-modelos.csv', ['familia', 'estudos'], fam.most_common())
    gravar('04-benchmarks.csv', ['benchmark', 'estudos'], bench.most_common())
    gravar('05-linguagens.csv', ['linguagem', 'estudos'], ling.most_common(30))
    md.append('Famílias de modelos (estudos): ' + '; '.join(f'{k}: {v}' for k, v in fam.most_common(12)) + '.\n')
    md.append('Benchmarks (estudos): ' + '; '.join(f'{k}: {v}' for k, v in bench.most_common(10)) + f'; estudos sem nenhum desses: {sum(1 for f in F if not any(re.search(p, nm(b).lower()) for b in f["benchmarks"] for _, p in BENCH))}.\n')
    md.append('Linguagens (estudos): ' + '; '.join(f'{k}: {v}' for k, v in ling.most_common(10)) + '.\n')
    md.append(f'Sem comparador: {sum(f["sem_comparador"] == "sim" for f in F)}; com técnica só classificada (sem número): {sum(1 for f in F if f.get("so_classificadas"))}; sem nenhuma comparação extraída: {sum(1 for f in F if not any(e["estudo_id"] == f["estudo_id"] for e in E))}.\n')

    # 3. Mecanismos das técnicas focais por tarefa (estudos distintos)
    md.append('## Mecanismos (técnicas focais; estudos distintos)\n')
    lin = []; acr = []
    for t in TAREFAS:
        Ft = [f for f in F if t in f['tarefas']]
        c = collections.Counter(m for f in Ft for m in {m for x in f['tecnicas'] if x['papel'] == 'focal' for m in x['mecanismos']})
        a = collections.Counter(m for f in Ft for m in {m for x in f['tecnicas'] if x['papel'] == 'focal' for m in (x.get('mecanismos_acrescentados') or [])})
        lin.append([t, len(Ft)] + [c[m] for m in MEC]); acr.append([t, len(Ft)] + [a[m] for m in MEC])
    gravar('06-mecanismos-focais-por-tarefa.csv', ['tarefa', 'estudos'] + MEC, lin)
    gravar('07-mecanismos-acrescentados-por-tarefa.csv', ['tarefa', 'estudos'] + MEC, acr)
    md.append('| tarefa | estudos | ' + ' | '.join(MEC) + ' |\n|' + '---|' * (len(MEC) + 2) + '\n' + '\n'.join('| ' + ' | '.join(map(str, l)) + ' |' for l in acr) + '\n')
    md.append('(mecanismos acrescentados pela técnica focal ao prompt base; a tabela 06 traz o pacote completo)\n')

    # 4. Contrafactual das técnicas focais
    md.append('## Contrafactual das técnicas focais (técnicas, não estudos)\n')
    cf = collections.Counter(); cft = collections.defaultdict(collections.Counter)
    for f in F:
        for x in f['tecnicas']:
            if x['papel'] != 'focal':
                continue
            cf[x['tipo_contrafactual']] += 1
            for t in f['tarefas']:
                cft[t][x['tipo_contrafactual']] += 1
    tipos = ['pacote', 'ingrediente', 'contraste_pareado', 'cumulativo', 'nenhum']
    gravar('08-contrafactual-focais.csv', ['tarefa'] + tipos, [[t] + [cft[t][k] for k in tipos] for t in TAREFAS] + [['total'] + [cf[k] for k in tipos]])
    md.append('Total: ' + '; '.join(f'{k}: {cf[k]}' for k in tipos) + '.\n')
    cc = collections.Counter(x['tipo_contrafactual'] for f in F for x in f['tecnicas'] if x['papel'] == 'componente')
    md.append('Componentes (ingredientes registrados das técnicas focais): ' + '; '.join(f'{k}: {cc[k]}' for k in tipos) + '.\n')
    linhas_e = []
    for t in TAREFAS + ['todas']:
        Ft = F if t == 'todas' else [f for f in F if t in f['tarefas']]
        def tem(f, ks):
            return any(x['papel'] != 'comparador' and x['tipo_contrafactual'] in ks for x in f['tecnicas'])
        linhas_e.append([t, len(Ft), sum(tem(f, ['pacote']) for f in Ft), sum(tem(f, ['ingrediente', 'contraste_pareado']) for f in Ft),
                         sum(tem(f, ['cumulativo']) for f in Ft),
                         sum(1 for f in Ft if all(x['tipo_contrafactual'] == 'nenhum' for x in f['tecnicas'] if x['papel'] != 'comparador'))])
    gravar('08b-contrafactual-estudos.csv', ['tarefa', 'estudos', 'com_pacote', 'com_ingrediente_ou_pareado', 'com_cumulativo', 'so_nenhum'], linhas_e)
    md.append('Estudos (técnica focal ou componente; um estudo pode ter vários tipos): ' + '; '.join(f'{l[0]}: {l[1]} estudos, pacote {l[2]}, ingrediente ou pareado {l[3]}, cumulativo {l[4]}, só nenhum {l[5]}' for l in linhas_e) + '.\n')

    # 5. Comparações: direção por tarefa e mecanismo acrescentado
    md.append('## Comparações extraídas (unidade: comparação)\n')
    dirc = collections.defaultdict(collections.Counter); est = collections.defaultdict(set)
    total = collections.Counter()
    for e in E:
        v = variacao(e)
        k = v or ('descritiva' if e.get('comparador') in (None, '') else 'sem_direcao')
        total[k] += 1
        for m in (e.get('mecanismos_acrescentados') or ['(nenhum acrescentado)']):
            dirc[(e['tarefa'], m)][k] += 1; est[(e['tarefa'], m)].add(e['estudo_id'])
    cols = ['melhora', 'igual', 'piora', 'sem_direcao', 'descritiva']
    linhas = sorted([[t, m, len(est[(t, m)]), sum(c.values())] + [c[k] for k in cols] for (t, m), c in dirc.items()], key=lambda l: (TAREFAS.index(l[0]) if l[0] in TAREFAS else 9, -l[3]))
    gravar('09-direcao-comparacoes.csv', ['tarefa', 'mecanismo_acrescentado', 'estudos', 'comparacoes'] + cols, linhas)
    md.append('Total: ' + '; '.join(f'{k}: {total[k]}' for k in cols) + '. «sem_direcao»: sem sentido definido ou sem dois números; «descritiva»: sem comparador.\n')
    sel = collections.Counter(e.get('selecao') for e in E); der = collections.Counter(e.get('derivacao') for e in E)
    md.append('Seleção: ' + '; '.join(f'{k}: {v}' for k, v in sel.items()) + '. Derivação: ' + '; '.join(f'{k}: {v}' for k, v in der.items()) + '.\n')
    pv = collections.Counter((e['tarefa'], variacao(e)) for e in E if e.get('selecao') == 'principal_declarado')
    md.append('Só comparações principais declaradas: ' + '; '.join(f'{t}: {pv[(t,"melhora")]} melhora, {pv[(t,"igual")]} igual, {pv[(t,"piora")]} piora' for t in TAREFAS) + '.\n')
    md.append('Os autores escolhem a comparação principal, e estudos com resultado favorável tendem a ser publicados; a proporção de melhoras não estima efeito.\n')

    # 6. Qualidade
    md.append('## Qualidade (estudos; julgamento por IA)\n')
    qc = collections.defaultdict(collections.Counter)
    for q in Q:
        qc[q['criterio']][q['julgamento']] += 1
    gravar('10-qualidade.csv', ['criterio'] + JULG, [[c] + [qc[c][j] for j in JULG] for c in CRIT])
    md.append('| critério | ' + ' | '.join(JULG) + ' |\n|' + '---|' * (len(JULG) + 1) + '\n' + '\n'.join('| ' + c + ' | ' + ' | '.join(str(qc[c][j]) for j in JULG) + ' |' for c in CRIT) + '\n')

    # 7. Riscos e mitigações
    md.append('## Riscos e mitigações (estudos distintos)\n')
    rk = ['correcao_funcional', 'seguranca', 'alucinacao', 'contaminacao', 'nao_determinismo', 'custo', 'manutenibilidade', 'outro']
    rl = []
    for t in TAREFAS + ['todas']:
        Ft = F if t == 'todas' else [f for f in F if t in f['tarefas']]
        c = collections.Counter(r for f in Ft for r in {x.get('categoria') if isinstance(x, dict) else 'outro' for x in f['riscos']})
        mit = sum(1 for f in Ft if f['mitigacoes']); mav = sum(1 for f in Ft if any(isinstance(m, dict) and m.get('avaliada') == 'sim' for m in f['mitigacoes']))
        rl.append([t, len(Ft)] + [c[r] for r in rk] + [mit, mav])
    gravar('11-riscos-mitigacoes.csv', ['tarefa', 'estudos'] + rk + ['com_mitigacao', 'com_mitigacao_avaliada'], rl)
    md.append('| tarefa | estudos | ' + ' | '.join(rk) + ' | com mitigação | mitigação avaliada |\n|' + '---|' * (len(rk) + 4) + '\n' + '\n'.join('| ' + ' | '.join(map(str, l)) + ' |' for l in rl) + '\n')

    # 8. Componentes fora do escopo e heterogeneidade
    fe = collections.Counter(x.get('natureza') if isinstance(x, dict) else 'outro' for f in F for x in f['componentes_fora_escopo'])
    md.append('## Outros\n')
    md.append(f'Estudos com componente fora do escopo de prompting: {sum(1 for f in F if f["componentes_fora_escopo"])} (' + '; '.join(f'{k}: {v}' for k, v in fe.most_common()) + ').\n')
    md.append(f'Estudos com registro de heterogeneidade (busca dirigida): {sum(1 for f in F if f["heterogeneidade"])}; registros: {sum(len(f["heterogeneidade"]) for f in F)}.\n')
    (SAIDA.parent / 'resumo-quantitativo.md').write_text('\n'.join(md), encoding='utf-8')
    print('\n'.join(md))


if __name__ == '__main__':
    main()
