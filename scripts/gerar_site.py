"""Gera site/dados.json, a única fonte de dados do site «Prompt em Código» (D131).

Entradas: a tabela de apoio v2, a regra de recursos por linha e o preenchimento dos
cenários (decisões editoriais do site), os cenários v2, as comparações ex-v2.2, as fichas
e o cadastro dos estudos. A saída é determinística: não leva data nem commit, para que
`make check` possa conferir se o arquivo versionado corresponde às fontes.

O site publica só dados derivados. Cada coleção é montada por lista permitida de campos:
trechos citados dos artigos, caminhos de PDF e de texto extraído e a origem interna das
fichas não são exportados. Nenhuma média, nota ou ordenação por resultado é calculada.

Uso: python3 scripts/gerar_site.py           (grava site/dados.json)
     python3 scripts/gerar_site.py --conferir  (falha se o arquivo estiver desatualizado)
"""
import collections
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / 'scripts'))
from validar_ficha_extracao import variacao  # noqa: E402  (regra de direção, D106)

SAIDA = RAIZ / 'site/dados.json'
FONTES = {
    'tabela': 'evidencias/sinteses/tabela-apoio-v2.csv',
    'recursos': 'evidencias/sinteses/tabela-apoio-v2-recursos.csv',
    'cenarios': 'evidencias/sinteses/cenarios-v2.md',
    'preenchimento': 'evidencias/sinteses/cenarios-v2-preenchimento.csv',
    'extracoes': 'dados/extracoes.jsonl',
    'fichas': 'dados/fichas.jsonl',
    'estudos': 'dados/estudos.csv',
}
TAREFAS = ['geracao', 'depuracao', 'traducao', 'refatoracao']
# Ordem fixa dos mecanismos na matriz (site/DESIGN.md, seção 4).
MECANISMOS = ['instrucao', 'contexto', 'restricoes', 'exemplos', 'decomposicao', 'feedback', 'raciocinio',
              'amostragem', 'multiagente', 'otimizacao_prompt', 'outro']
DIRECOES = ['melhora', 'piora', 'igual', 'sem_direcao', 'descritiva']
# Condições que o formulário do Guia sabe informar.
CONDICOES = ['testes', 'executor', 'compilador', 'analisador', 'contexto', 'exemplos', 'pequeno', 'varias',
             'reproducao', 'diagnostico']
GRUPOS = ['normal', 'lacuna', 'lacuna_parcial']
# As duas versões da tabela usam as sínteses de 302 fichas (monografia, QP3, «Como ler a
# tabela e o que ela não faz»); o Explorador cobre as 332 fichas do corpus.
FICHAS_NAS_SINTESES = 302
PROIBIDOS = ('citacoes', 'trecho', 'fonte', 'texto_fonte', 'ficha_origem', 'prompt_sha256', 'selecao_motivo')
REF = re.compile(r'S\d+(?:-C\d+)?')
ID_COMPARACAO = re.compile(r'^S\d+-C\d+$')


def ler_csv(chave):
    with open(RAIZ / FONTES[chave], encoding='utf-8', newline='') as fh:
        return list(csv.DictReader(fh))


def ler_jsonl(chave):
    with open(RAIZ / FONTES[chave], encoding='utf-8') as fh:
        return [json.loads(l) for l in fh if l.strip()]


def direcao(e):
    """Mesma regra de scripts/sintetizar.py: sem direção calculável, a comparação é
    descritiva quando não tem comparador e «sem direção» nos demais casos."""
    return variacao(e) or ('descritiva' if e.get('comparador') in (None, '') else 'sem_direcao')


def analisar_regra(texto):
    """'a+b | c' -> [['a', 'b'], ['c']]; regra vazia -> [] (nenhum recurso exigido)."""
    alternativas = []
    for alt in texto.split('|'):
        itens = [t.strip() for t in alt.split('+') if t.strip()]
        for t in itens:
            if t not in CONDICOES:
                raise ValueError(f'condição desconhecida na regra: {t!r}')
        if itens:
            alternativas.append(itens)
    return alternativas


def faltas(regra, condicoes):
    """Para cada alternativa da regra, o que falta; [] se alguma está satisfeita ou se
    a regra é vazia. Alternativas cujo conjunto contém outro são descartadas."""
    if not regra:
        return []
    pend = [[t for t in alt if t not in condicoes] for alt in regra]
    if any(not p for p in pend):
        return []
    unicos = []
    for p in pend:
        if p not in unicos:
            unicos.append(p)
    return [p for p in unicos if not any(set(q) < set(p) for q in unicos)]


def classificar(linha, condicoes):
    """Grupo do Guia: 'lacuna' tem precedência; depois 'falta'; senão 'aplicavel'."""
    if linha['grupo'] != 'normal':
        return 'lacuna'
    return 'falta' if faltas(linha['regra'], condicoes) else 'aplicavel'


def condicoes_do_cenario(c):
    cond = set(c['recursos'])
    if c['chamadas'] == 'varias':
        cond.add('varias')
    if c['reproducao'] in ('teste', 'outro'):
        cond.add('reproducao')
    if c['reproducao'] == 'teste':
        cond.add('testes')
    if c['diagnostico'] == 'sim':
        cond.add('diagnostico')
    return cond


def nome(x):
    if isinstance(x, dict):
        return str(x.get('nome') or '').strip()
    return str(x).strip()


def url_fonte(identificador, versao):
    ident = (identificador or '').strip()
    if ident.lower().startswith('arxiv:'):
        v = versao if re.fullmatch(r'v\d+', versao or '') else ''
        return 'https://arxiv.org/abs/' + ident[6:] + v
    if ident.lower().startswith('doi:'):
        return 'https://doi.org/' + ident[4:]
    return None


def ultima_data(valores):
    """Maior data ISO registrada; ignora vazios e marcadores como nao_informado."""
    datas = [v for v in valores if isinstance(v, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', v)]
    return max(datas) if datas else None


def sem_marcacao(t):
    return re.sub(r'\*(.+?)\*', r'\1', t).replace('`', '')


def ler_cenarios():
    texto = (RAIZ / FONTES['cenarios']).read_text(encoding='utf-8')
    preench = {r['id']: r for r in ler_csv('preenchimento')}
    cenarios = []
    for bloco in re.split(r'^### ', texto, flags=re.M)[1:]:
        cab, _, corpo = bloco.partition('\n')
        cid, _, titulo = cab.partition(' — ')
        campos = {m.group(1): sem_marcacao(' '.join(m.group(2).split()))
                  for m in re.finditer(r'^- \*\*(.+?):\*\*\s*(.*?)(?=^- \*\*|\Z)', corpo, flags=re.M | re.S)}
        p = preench[cid.strip()]
        recursos = [r for r in p['recursos'].split(';') if r]
        for r in recursos:
            if r not in CONDICOES:
                raise ValueError(f'cenário {cid}: recurso desconhecido {r!r}')
        cenarios.append({
            'id': cid.strip(), 'titulo': titulo.strip(), 'nome_botao': p['nome_botao'], 'tarefa': p['tarefa'],
            'recursos': recursos, 'chamadas': p['chamadas'], 'reproducao': p['reproducao'],
            'diagnostico': p['diagnostico'], 'resumo': p['resumo'],
            'dominio': campos['Tarefa e domínio'], 'modelo': campos['Modelo'],
            'verificacao': campos['Recursos de verificação'], 'orcamento': campos['Orçamento'],
            'objetivo': campos['Objetivo'], 'hipotese': campos['H-' + cid.strip()],
        })
    if sorted(c['id'] for c in cenarios) != sorted(preench):
        raise ValueError('cenários e preenchimento não têm os mesmos IDs')
    return cenarios


def referencias(linha, ids_comparacoes, ids_estudos):
    """Comparações e estudos citados pela linha, na ordem: primeiro `estudos_ids`, depois
    as menções explícitas nos textos da linha. Um ID de estudo sozinho nunca vira C1."""
    comp, est = [], []

    def registrar(ref, origem):
        if '-C' in ref:
            if all(r['id'] != ref for r in comp):
                comp.append({'id': ref, 'origem': origem, 'registrada': ref in ids_comparacoes})
        elif all(r['id'] != ref for r in est):
            est.append({'id': ref, 'origem': origem, 'registrada': ref in ids_estudos})

    for ref in REF.findall(linha['estudos_ids']):
        registrar(ref, 'lista')
    for campo in ('indicacao', 'ressalvas', 'condicao_verificacao', 'resultado_medido', 'forca'):
        for ref in REF.findall(linha[campo]):
            registrar(ref, 'texto')
    return comp, est


def montar():
    tabela = ler_csv('tabela')
    recursos = {r['id']: r for r in ler_csv('recursos')}
    extracoes = [e for e in ler_jsonl('extracoes')
                 if e.get('prompt_versao') == 'ex-v2.2' and ID_COMPARACAO.match(e['id'])]
    fichas = ler_jsonl('fichas')
    cadastro = {r['id']: r for r in ler_csv('estudos')}
    ids_comparacoes = {e['id'] for e in extracoes}
    ids_estudos = {f['estudo_id'] for f in fichas}
    if len(ids_comparacoes) != len(extracoes):
        raise ValueError('IDs de comparação repetidos')
    if sorted(recursos) != sorted(l['id'] for l in tabela):
        raise ValueError('tabela de apoio e regra de recursos não têm os mesmos IDs')

    linhas = []
    for l in tabela:
        r = recursos[l['id']]
        if r['grupo'] not in GRUPOS:
            raise ValueError(f'{l["id"]}: grupo {r["grupo"]!r}')
        comp, est = referencias(l, ids_comparacoes, ids_estudos)
        linhas.append({
            'id': l['id'], 'tarefa': l['tarefa'], 'agrupamento': l['agrupamento'],
            'condicao': l['condicao_verificacao'], 'resultado_medido': l['resultado_medido'],
            'evidencia': l['evidencia'], 'indicacao': l['indicacao'], 'forca': l['forca'],
            'ressalvas': l['ressalvas'], 'grupo': r['grupo'], 'regra': analisar_regra(r['regra']),
            'incerta': r['incerta'] == 'sim', 'nota': r['nota'], 'comparacoes': comp, 'estudos': est,
        })

    comparacoes = []
    for e in extracoes:
        res = e.get('resultado') or {}
        comparacoes.append({
            'id': e['id'], 'estudo': e['estudo_id'], 'tarefa': e['tarefa'], 'tecnica': e.get('tecnica'),
            'comparador': e.get('comparador'), 'modelo': e.get('modelo'), 'benchmark': e.get('benchmark'),
            'metrica': e.get('metrica'), 'sentido': e.get('sentido'), 'unidade': e.get('unidade'),
            'base': res.get('baseline'), 'intervencao': res.get('intervencao'), 'direcao': direcao(e),
            'mecanismos': e.get('mecanismos') or [], 'acrescentados': e.get('mecanismos_acrescentados') or [],
            'condicoes': e.get('condicoes'), 'denominador': e.get('denominador'),
            'localizador': e.get('localizador'), 'revisao_humana': e.get('revisao_humana'),
            'revisor': e.get('revisor'), 'data_revisao': e.get('data_revisao'),
            'conferencia': e.get('conferencia'), 'executor': e.get('executor'),
            'modelo_executor': e.get('modelo_executor'), 'data': e.get('data'),
        })

    por_estudo = collections.Counter(c['estudo'] for c in comparacoes)
    estudos = []
    for f in sorted(fichas, key=lambda f: int(f['estudo_id'][1:])):
        sid = f['estudo_id']
        cad = cadastro[sid]
        leitura = f.get('leitura')
        estudos.append({
            'id': sid, 'titulo': cad['titulo'], 'ano': cad['ano'], 'identificador': cad['identificador'],
            'versao': cad['versao'], 'url': url_fonte(cad['identificador'], cad['versao']),
            'metadados_conferidos': cad['metadados_conferidos'], 'tarefas': f.get('tarefas') or [],
            'tecnicas': [{'nome': t.get('nome_original'), 'papel': t.get('papel'),
                          'acrescentados': t.get('mecanismos_acrescentados') or [],
                          'contrafactual': t.get('tipo_contrafactual')} for t in f.get('tecnicas') or []],
            'modelos': [nome(m) for m in f.get('modelos') or []],
            'benchmarks': [nome(b) for b in f.get('benchmarks') or []],
            'linguagens': [nome(x) for x in f.get('linguagens') or []],
            'riscos': [{'categoria': r.get('categoria'), 'descricao': r.get('descricao'),
                        'localizador': r.get('localizador')} for r in f.get('riscos') or []],
            'sem_comparador': f.get('sem_comparador'),
            'leitura': leitura.get('status') if isinstance(leitura, dict) else leitura,
            'revisao_humana': f.get('revisao_humana'), 'revisor': f.get('revisor'),
            'data_revisao': f.get('data_revisao'), 'conferencia': f.get('conferencia'),
            'executor': f.get('executor'), 'modelo_executor': f.get('modelo_executor'), 'data': f.get('data'),
            'n_comparacoes': por_estudo.get(sid, 0),
        })

    revisadas = [f for f in fichas if f.get('revisao_humana') == 'confirmada']
    meta = {
        'site': 'Prompt em Código', 'tabela_versao': 'v2', 'extracao_versao': 'ex-v2.2',
        'data_corte': '2026-09-07', 'periodo_inicio': '2021-01-01',
        'fichas_nas_sinteses': FICHAS_NAS_SINTESES, 'n_linhas': len(linhas), 'n_comparacoes': len(comparacoes),
        'n_estudos': len(estudos), 'estudos_sem_comparacao': sum(1 for s in estudos if not s['n_comparacoes']),
        'estudos_revisados': len(revisadas),
        'estudos_revisados_por_modalidade': dict(sorted(collections.Counter(
            f.get('conferencia') or 'sem_registro' for f in revisadas).items())),
        'comparacoes_revisadas': sum(1 for c in comparacoes if c['revisao_humana'] == 'confirmada'),
        'direcoes': {d: sum(1 for c in comparacoes if c['direcao'] == d) for d in DIRECOES},
        'ultima_extracao': ultima_data(f.get('data') for f in fichas),
        'ultima_revisao': ultima_data(f.get('data_revisao') for f in fichas),
        'tarefas': TAREFAS, 'mecanismos': MECANISMOS,
        'repositorio': 'https://github.com/caiofreitas1/tcc2-prompt-engineering',
        'monografia_url': None,
        'fontes_sha256': {FONTES[k]: hashlib.sha256((RAIZ / FONTES[k]).read_bytes()).hexdigest()
                          for k in sorted(FONTES)},
    }
    return {'meta': meta, 'linhas': linhas, 'cenarios': ler_cenarios(), 'comparacoes': comparacoes,
            'estudos': estudos}


def serializar(dados):
    return json.dumps(dados, ensure_ascii=False, separators=(',', ':')) + '\n'


def main(args):
    texto = serializar(montar())
    if '--conferir' in args:
        atual = SAIDA.read_text(encoding='utf-8') if SAIDA.exists() else ''
        if atual != texto:
            print('site/dados.json desatualizado: execute python3 scripts/gerar_site.py')
            return 1
        print('site/dados.json corresponde às fontes')
        return 0
    SAIDA.parent.mkdir(exist_ok=True)
    SAIDA.write_text(texto, encoding='utf-8')
    d = json.loads(texto)
    print(f'{SAIDA.relative_to(RAIZ)}: {len(d["linhas"])} linhas, {len(d["cenarios"])} cenários, '
          f'{len(d["comparacoes"])} comparações, {len(d["estudos"])} estudos, {len(texto.encode()) // 1024} KB')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
