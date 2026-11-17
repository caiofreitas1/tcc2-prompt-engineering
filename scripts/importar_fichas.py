"""Importa as fichas finais ex-v2.2 para dados/ (fichas.jsonl, extracoes.jsonl e qualidade.csv).

As fichas finais estão em evidencias/extracao-v2.2/ (corpus) e evidencias/piloto/extracao-v2.2/
(piloto, 10 estudos), já com as correções manuais registradas. A importação é idempotente:
regrava as linhas geradas e preserva as extrações anteriores do contrato 1 (E1, E2).

As extrações entram com status nao_conferido e revisao_humana pendente: são extrações por IA,
ainda não conferidas pelo autor. Os estudos da amostra conferidos pelo autor (D116, D117; registro em
evidencias/extracao-v2.2/conferencia/julgamentos-autor.jsonl) recebem revisao_humana = confirmada, com
revisor, data e a origem do registro (formulário ou declaração do autor). O status continua
nao_conferido: conferido_original exige também metadados conferidos, ainda pendentes.

Uso: python3 scripts/importar_fichas.py
"""
import csv, glob, json, re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CORPUS = RAIZ / 'evidencias/extracao-v2.2'
PILOTO = RAIZ / 'evidencias/piloto/extracao-v2.2'
GERADO = re.compile(r'^S\d+-C\d+$')
QUALIDADE = ['estudo_id', 'criterio', 'julgamento', 'localizador', 'justificativa', 'avaliador', 'natureza', 'data']


def fichas():
    man = {r['estudo_id']: r for r in csv.DictReader(open(CORPUS / 'rodadas/manifesto.csv', encoding='utf-8'))}
    manp = {r['estudo_id']: r for r in csv.DictReader(open(PILOTO / 'rodadas/manifesto.csv', encoding='utf-8'))}
    for pasta, origem in ((CORPUS, 'corpus'), (PILOTO, 'piloto')):
        for f in sorted(glob.glob(str(pasta / 'S*.json')), key=lambda p: int(Path(p).stem[1:])):
            sid = Path(f).stem
            d = json.load(open(f, encoding='utf-8'))
            if origem == 'corpus':
                m = man[sid]
                executor, modelo, sha = m['executor'], m['modelo_executor'], m['prompt_sha256']
                data = d.get('data', 'nao_informado')
            else:
                # Piloto ex-v2.2: subagentes Claude Opus 5.5 em 14/11/2026 (calibracao-ex-v2.2.md).
                executor, modelo, sha, data = 'Claude Code (subagente)', 'Claude Opus 5.5', manp[sid]['prompt_sha256'], '2026-11-14'
            yield sid, origem, d, executor, modelo, sha, data, str(Path(f).relative_to(RAIZ))


def main():
    estudos = {r['id']: r for r in csv.DictReader(open(RAIZ / 'dados/estudos.csv', encoding='utf-8'))}
    antigas = [l for l in (RAIZ / 'dados/extracoes.jsonl').read_text(encoding='utf-8').splitlines()
               if l.strip() and not GERADO.match(json.loads(l).get('id', ''))]
    novas, linhas_q, linhas_f = [], [], []
    jul = RAIZ / 'evidencias/extracao-v2.2/conferencia/julgamentos-autor.jsonl'
    conf = {}
    if jul.exists():
        for l in jul.read_text(encoding='utf-8').splitlines():
            j = json.loads(l)
            conf[j['estudo_id']] = {'revisao_humana': 'confirmada', 'revisor': 'Caio César de Freitas',
                                    'data_revisao': (j.get('salvo_em') or j.get('data'))[:10],
                                    'conferencia': j['origem']}
    for sid, origem, d, executor, modelo, sha, data, arq in fichas():
        if estudos.get(sid, {}).get('corpus') != 'definitivo':
            continue
        f = d['ficha']
        texto = d.get('texto_fonte', f'fontes/textos/lote/{sid}.txt')
        fonte = f'fontes/artigos/lote/{sid}.pdf'
        base = {'executor': executor, 'modelo_executor': modelo, 'natureza': 'ia', 'data': data,
                'prompt_versao': 'ex-v2.2', 'prompt_sha256': sha, 'ficha_origem': arq}
        linhas_f.append(json.dumps({'estudo_id': sid, 'origem': origem, **f, 'texto_fonte': texto,
                                    'leitura': d.get('leitura'), **base, 'revisao_humana': 'pendente',
                                    **conf.get(sid, {})}, ensure_ascii=False))
        for k, e in enumerate(d['extracoes'], 1):
            ext = {'id': f'{sid}-C{k}', 'estudo_id': sid, 'contrato': 2, **e,
                   'resultado': e.get('resultado') or {'baseline': None, 'intervencao': None},
                   'fonte': fonte, 'texto_fonte': texto, 'riscos': f.get('riscos', []),
                   'mitigacoes': f.get('mitigacoes', []), 'status': 'nao_conferido',
                   'revisao_humana': 'pendente', **base, **conf.get(sid, {})}
            novas.append(json.dumps(ext, ensure_ascii=False))
        for q in d['qualidade']:
            linhas_q.append({'estudo_id': sid, 'criterio': q['criterio'], 'julgamento': q['julgamento'],
                             'localizador': q.get('localizador') or 'nao_informado',
                             'justificativa': q.get('justificativa') or 'nao_informado',
                             'avaliador': f'{executor} ({modelo})', 'natureza': 'ia', 'data': data})
    (RAIZ / 'dados/extracoes.jsonl').write_text('\n'.join(antigas + novas) + '\n', encoding='utf-8')
    (RAIZ / 'dados/fichas.jsonl').write_text('\n'.join(linhas_f) + '\n', encoding='utf-8')
    with open(RAIZ / 'dados/qualidade.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=QUALIDADE)
        w.writeheader()
        w.writerows(linhas_q)
    print(f'fichas: {len(linhas_f)}; extrações: {len(novas)} (+{len(antigas)} anteriores); qualidade: {len(linhas_q)} linhas')


if __name__ == '__main__':
    main()
