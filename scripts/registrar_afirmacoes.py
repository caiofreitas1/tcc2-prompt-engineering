"""Registra em dados/afirmacoes.csv as afirmações marcadas nas subseções geradas da síntese.

Entrada: pares <nome>.tex e <nome>.jsonl (marcadores provisórios como DEP-3), passados como
argumento. Cada marcador ganha um ID definitivo (A<n>, continuando a numeração), o comentário
`% AFIRMACAO:` é reescrito no .tex e a afirmação entra como rascunho, sem revisor.
O .tex é copiado para monografia/capitulos/ com o nome indicado.

Uso: python3 scripts/registrar_afirmacoes.py <dir-entrada> <nome> <destino.tex> [<nome> <destino.tex> ...]
"""
import csv, json, re, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CSV = RAIZ / 'dados/afirmacoes.csv'
CAMPOS = ['id', 'texto', 'extracao_ids', 'bibkey', 'destino', 'status', 'revisor', 'data_revisao']


def main():
    entrada = Path(sys.argv[1])
    pares = list(zip(sys.argv[2::2], sys.argv[3::2]))
    linhas = list(csv.DictReader(open(CSV, encoding='utf-8')))
    extr = {json.loads(l)['id'] for l in open(RAIZ / 'dados/extracoes.jsonl', encoding='utf-8') if l.strip()}
    n = max(int(r['id'][1:]) for r in linhas if re.fullmatch(r'A\d+', r['id']))
    for nome, destino in pares:
        tex = (entrada / f'{nome}.tex').read_text(encoding='utf-8')
        destino_rel = f'monografia/capitulos/{destino}'
        linhas = [r for r in linhas if r['destino'] != destino_rel]  # idempotente por destino
        mapa = {}
        for l in open(entrada / f'{nome}.jsonl', encoding='utf-8'):
            if not l.strip():
                continue
            a = json.loads(l)
            ids = [i for i in a.get('extracao_ids', []) if i in extr]
            faltam = [i for i in a.get('extracao_ids', []) if i not in extr]
            if faltam:
                print(f'{a["marcador"]}: IDs inexistentes ignorados: {faltam}')
            n += 1
            mapa[a['marcador']] = f'A{n}'
            texto = a['texto'] if not a.get('estudos') or ids else a['texto'] + ' [estudos: ' + ', '.join(a['estudos']) + ']'
            linhas.append({'id': f'A{n}', 'texto': texto, 'extracao_ids': ';'.join(ids), 'bibkey': '',
                           'destino': destino_rel, 'status': 'rascunho', 'revisor': '', 'data_revisao': ''})
        def troca(m):
            k = m.group(1)
            if k not in mapa:
                print(f'marcador sem afirmação no jsonl: {k}')
                return m.group(0)
            return f'% AFIRMACAO: {mapa[k]}'
        tex = re.sub(r'% AFIRMACAO:\s*([A-Z]+-\d+)', troca, tex)
        sem = set(mapa) - set(re.findall(r'% AFIRMACAO:\s*([A-Z]+-\d+)', (entrada / f'{nome}.tex').read_text(encoding='utf-8')))
        if sem:
            print(f'{nome}: afirmações sem marcador no .tex: {sorted(sem)}')
        (RAIZ / destino_rel).write_text(tex, encoding='utf-8')
        print(f'{nome}: {len(mapa)} afirmações -> {destino_rel}')
    with open(CSV, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(linhas)


if __name__ == '__main__':
    main()
