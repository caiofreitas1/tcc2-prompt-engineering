"""Sorteia a amostra da conferência humana das fichas ex-v2.2 (protocolo, seção 7).

Tamanho: max(10, teto(0,20 × N)), com N = estudos do corpus definitivo. Os estudos
obrigatórios entram primeiro; os demais saem de uma amostra sistemática, com início
aleatório e semente fixa, sobre a lista das fichas finais ordenada por extrator, por
haver ou não correção manual aplicada por IA, por tarefas e por uma chave aleatória.
Essa ordenação distribui a amostra entre os estratos na proporção da população
(estratificação implícita), sem fixar cotas.

Complemento (D114): quando o corpus cresce depois do sorteio, a amostra gravada fica fixa
e só se sorteiam os estudos que faltam para o novo tamanho, pelo mesmo método, sobre as
fichas que não estavam no quadro original (`conferencia/quadro-original.txt`, 292 fichas).
O sorteio original se reproduz com as correções manuais vigentes no commit adeb97b; depois
dele, D110 registrou correções em S2056 e S2059, o que muda a ordenação do quadro atual.

Uso: python3 scripts/sortear_conferencia.py [--complemento] [--gravar]
"""
import csv, glob, json, math, random, sys, collections
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FICHAS = RAIZ / 'evidencias/extracao-v2.2'
SAIDA = FICHAS / 'conferencia/amostra.csv'
QUADRO_ORIGINAL = FICHAS / 'conferencia/quadro-original.txt'
SEMENTE = 20261117
OBRIGATORIOS = {
    'S1608': 'obrigatório: texto extraído ilegível, leitura só pelas imagens',
    'S1743': 'obrigatório: tabelas ilegíveis nas imagens, valores só do texto',
}


def quadro():
    man = {r['estudo_id']: r for r in csv.DictReader(open(FICHAS / 'rodadas/manifesto.csv', encoding='utf-8'))}
    cor = collections.Counter()
    for linha in open(FICHAS / 'correcoes-manuais.jsonl', encoding='utf-8'):
        c = json.loads(linha)
        if not c.get('situacao'):
            cor[c['estudo_id']] += 1
    linhas = []
    for f in sorted(glob.glob(str(FICHAS / 'S*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        sid = Path(f).stem
        linhas.append({
            'estudo_id': sid,
            'executor': man[sid]['executor'],
            'modelo_executor': man[sid]['modelo_executor'],
            'tarefas': '+'.join(sorted(d['ficha']['tarefas'])),
            'correcoes_vigentes': cor[sid],
        })
    return linhas


def sortear(linhas, n_corpus):
    n = max(10, math.ceil(0.20 * n_corpus))
    rng = random.Random(SEMENTE)
    resto = [l for l in linhas if l['estudo_id'] not in OBRIGATORIOS]
    for l in resto:
        l['_chave'] = rng.random()
    resto.sort(key=lambda l: (l['executor'], l['correcoes_vigentes'] > 0, l['tarefas'], l['_chave']))
    k = n - len(OBRIGATORIOS)
    passo = len(resto) / k
    inicio = rng.random() * passo
    escolhidos = [resto[int(inicio + i * passo)] for i in range(k)]
    amostra = [dict(l, motivo=OBRIGATORIOS[l['estudo_id']]) for l in linhas if l['estudo_id'] in OBRIGATORIOS]
    amostra += [dict(l, motivo='sorteio sistemático') for l in escolhidos]
    for l in amostra:
        l.pop('_chave', None)
    amostra.sort(key=lambda l: int(l['estudo_id'][1:]))
    return n, amostra


def complementar(linhas, n_corpus):
    n = max(10, math.ceil(0.20 * n_corpus))
    campos = ['estudo_id', 'executor', 'modelo_executor', 'tarefas', 'correcoes_vigentes', 'motivo']
    fixa = list(csv.DictReader(open(SAIDA, encoding='utf-8')))
    original = set(QUADRO_ORIGINAL.read_text(encoding='utf-8').split())
    novas = [l for l in linhas if l['estudo_id'] not in original]
    k = n - len(fixa)
    rng = random.Random(SEMENTE)
    for l in novas:
        l['_chave'] = rng.random()
    novas.sort(key=lambda l: (l['executor'], l['correcoes_vigentes'] > 0, l['tarefas'], l['_chave']))
    escolhidos = []
    if k > 0:
        passo = len(novas) / k
        inicio = rng.random() * passo
        escolhidos = [novas[int(inicio + i * passo)] for i in range(k)]
    amostra = [{c: r[c] for c in campos} for r in fixa]
    amostra += [dict({c: l[c] for c in campos[:-1]}, motivo='complemento sistemático (D114)') for l in escolhidos]
    amostra.sort(key=lambda l: int(l['estudo_id'][1:]))
    print(f'amostra fixa: {len(fixa)}; quadro do complemento: {len(novas)}; sorteados: {len(escolhidos)}')
    return n, amostra


def main():
    corpus = [r for r in csv.DictReader(open(RAIZ / 'dados/estudos.csv', encoding='utf-8')) if r.get('corpus') == 'definitivo']
    linhas = quadro()
    if '--complemento' in sys.argv:
        n, amostra = complementar(linhas, len(corpus))
    else:
        n, amostra = sortear(linhas, len(corpus))
    print(f'corpus definitivo: {len(corpus)}; fichas no quadro: {len(linhas)}; amostra: {n}; semente: {SEMENTE}')
    for campo in ('executor', 'tarefas'):
        pop = collections.Counter(l[campo] for l in linhas)
        am = collections.Counter(l[campo] for l in amostra)
        print(f'\n{campo}: população × amostra')
        for v, c in pop.most_common():
            print(f'  {v}: {c} × {am[v]}')
    pc = sum(1 for l in linhas if int(l['correcoes_vigentes']))
    ac = sum(1 for l in amostra if int(l['correcoes_vigentes']))
    print(f'\ncom correção manual vigente: {pc} × {ac}')
    if '--gravar' in sys.argv:
        SAIDA.parent.mkdir(parents=True, exist_ok=True)
        with open(SAIDA, 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=['estudo_id', 'executor', 'modelo_executor', 'tarefas', 'correcoes_vigentes', 'motivo'])
            w.writeheader()
            w.writerows(amostra)
        print(f'\ngravado: {SAIDA.relative_to(RAIZ)}')


if __name__ == '__main__':
    main()
