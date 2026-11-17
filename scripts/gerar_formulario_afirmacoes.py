"""Gera o formulário de conferência das afirmações empíricas (T12) a partir de dados/afirmacoes.csv.

Cada afirmação marcada no LaTeX com `% AFIRMACAO: A<n>` vira um cartão com:
- o trecho do texto em que aparece (arquivo e linha), com a marcação LaTeX simplificada;
- o texto registrado em dados/afirmacoes.csv;
- as comparações que a sustentam (dados/extracoes.jsonl): técnica, comparador, modelo, benchmark,
  métrica, valores, localizador, citações literais e o PDF local do estudo.
O autor julga cada afirmação como sustentada, a corrigir ou não verificável, e o julgamento é gravado
na coleção `afirmacoes_autor` do artifact, com o SHA-256 do texto registrado. Afirmações sem marcação no
texto (A1–A5, do piloto) ficam de fora e são listadas na saída.

Uso: python3 scripts/gerar_formulario_afirmacoes.py
"""
import csv, glob, hashlib, json, re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / 'evidencias/afirmacoes/conferencia/formulario.html'
MODELO = RAIZ / 'evidencias/afirmacoes/conferencia/modelo.html'


def limpar(t):
    for a, b in [(r'\%', '%'), (r'\#', '#'), (r'\&', '&'), ('~', ' '), ('$\\rightarrow$', '→'), ('$\\to$', '→'),
                 ('\\kappa', 'κ'), ('\\mu', 'μ'), ('\\times', '×'), ('\\chi', 'χ'), ('\\Delta', 'Δ'), ('\\to', '→'), ('``', '“'), ("''", '”'), ('--', '–')]:
        t = t.replace(a, b)
    t = re.sub(r'\\(?:textit|textbf|emph|texttt|text)\{([^{}]*)\}', r'\1', t)
    t = re.sub(r'\\(?:ref|label|cite)\{[^{}]*\}', '[ref]', t)
    t = re.sub(r'\$([^$]*)\$', r'\1', t)
    t = re.sub(r'\\item\s*', '• ', t)
    t = re.sub(r'\{([^{}]*)\}', r'\1', t)
    return re.sub(r'\s+', ' ', t).strip()


def trechos():
    out = {}
    for f in sorted(glob.glob(str(RAIZ / 'monografia/capitulos/*.tex'))):
        L = open(f, encoding='utf-8').read().split('\n')
        for i, l in enumerate(L):
            m = re.match(r'\s*% AFIRMACAO: (A\d+(?:\s*[,;]\s*A\d+)*)', l)
            if not m:
                continue
            bloco = []
            if f.endswith('05-discussao.tex'):
                # Na discussão, a marcação vem depois da frase que sustenta.
                for l2 in reversed(L[:i]):
                    s = l2.strip()
                    if s.startswith('% AFIRMACAO') and not bloco:
                        continue
                    if not s or s.startswith('% AFIRMACAO') or s.startswith('\\subsection'):
                        break
                    if not s.startswith('%'):
                        bloco.insert(0, s)
                for a in re.findall(r'A\d+', m.group(1)):
                    out.setdefault(a, []).append({'arquivo': str(Path(f).relative_to(RAIZ)), 'linha': i,
                                                  'texto': limpar(' '.join(bloco))})
                continue
            for l2 in L[i + 1:]:
                s = l2.strip()
                if not s or s.startswith('% AFIRMACAO') or s.startswith('\\paragraph') or s.startswith('\\end') \
                        or s.startswith('\\begin') or s.startswith('\\subsub') or (bloco and s.startswith('\\item')):
                    break
                if s.startswith('%'):
                    continue
                bloco.append(s)
            for a in re.findall(r'A\d+', m.group(1)):
                out.setdefault(a, []).append({'arquivo': str(Path(f).relative_to(RAIZ)), 'linha': i + 2,
                                              'texto': limpar(' '.join(bloco))})
    return out


def nm(v):
    if v is None:
        return ''
    if isinstance(v, str):
        return v
    if isinstance(v, dict):
        return v.get('nome') or json.dumps(v, ensure_ascii=False)
    return json.dumps(v, ensure_ascii=False)


def main():
    afs = list(csv.DictReader(open(RAIZ / 'dados/afirmacoes.csv', encoding='utf-8')))
    ext = {json.loads(l)['id']: json.loads(l) for l in open(RAIZ / 'dados/extracoes.jsonl', encoding='utf-8')}
    est = {r['id']: r for r in csv.DictReader(open(RAIZ / 'dados/estudos.csv', encoding='utf-8'))}
    tr = trechos()
    itens, fora = [], []
    for a in afs:
        if a['id'] not in tr:
            fora.append(a['id'])
            continue
        evid = []
        for eid in filter(None, a['extracao_ids'].split(';')):
            e = ext.get(eid)
            if not e:
                evid.append({'id': eid, 'ausente': True})
                continue
            sid = e['estudo_id']
            evid.append({'id': eid, 'estudo': sid, 'titulo': est.get(sid, {}).get('titulo', ''),
                         'pdf': f'fontes/artigos/lote/{sid}.pdf', 'tecnica': nm(e.get('tecnica')),
                         'comparador': nm(e.get('comparador')), 'modelo': nm(e.get('modelo')),
                         'benchmark': nm(e.get('benchmark')), 'metrica': nm(e.get('metrica')),
                         'sentido': e.get('sentido'), 'unidade': e.get('unidade'),
                         'resultado': e.get('resultado'), 'denominador': nm(e.get('denominador')),
                         'localizador': nm(e.get('localizador')), 'conferido_pdf': e.get('conferido_pdf'),
                         'revisao_humana': e.get('revisao_humana'), 'conferencia': e.get('conferencia'),
                         'citacoes': [{'trecho': c.get('trecho', ''), 'localizador': c.get('localizador', '')}
                                      for c in (e.get('citacoes') or [])][:6]})
        itens.append({'id': a['id'], 'texto': a['texto'], 'destino': a['destino'], 'trechos': tr[a['id']],
                      'sha256_texto': hashlib.sha256(a['texto'].encode('utf-8')).hexdigest(), 'evidencias': evid})
    itens.sort(key=lambda x: (x['trechos'][0]['arquivo'], x['trechos'][0]['linha']))
    dados = json.dumps(itens, ensure_ascii=False).replace('</', '<\\/')
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(MODELO.read_text(encoding='utf-8').replace('/*DADOS*/[]', dados), encoding='utf-8')
    print(len(itens), 'afirmações no formulário;', 'fora (sem marcação no texto):', ', '.join(fora) or 'nenhuma',
          ';', SAIDA.stat().st_size, 'bytes')


if __name__ == '__main__':
    main()
