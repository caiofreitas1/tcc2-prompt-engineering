"""Gera o formulário de julgamento do exame dos cenários a partir de evidencias/sinteses/exame-cenarios-v1.md.

Cada cenário (seção `## `) vira um cartão com o texto do exame e campos de julgamento por critério,
pré-preenchidos com a proposta. O autor confirma ou altera, e o julgamento é gravado na coleção
`exame_cenarios_autor` do artifact. Uso: python3 scripts/gerar_formulario_exame.py
"""
import html, json, re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FONTE = RAIZ / 'evidencias/sinteses/exame-cenarios-v1.md'
SAIDA = RAIZ / 'evidencias/sinteses/exame/formulario.html'


def inline(t):
    t = html.escape(t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', t)
    return t


def md(bloco):
    out, lista, tab = [], None, []
    def fecha():
        nonlocal lista, tab
        if lista:
            out.append(f'</{lista}>'); lista = None
        if tab:
            linhas = [l for l in tab if not re.fullmatch(r'\|[-| ]+\|', l)]
            cel = [[c.strip() for c in l.strip('|').split('|')] for l in linhas]
            if not cel:
                tab = []
                return
            h = ''.join(f'<th>{inline(c)}</th>' for c in cel[0])
            b = ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in cel[1:])
            out.append(f'<div class="tab"><table><tr>{h}</tr>{b}</table></div>'); tab = []
    for l in bloco.splitlines():
        if l.startswith('|'):
            if lista: out.append(f'</{lista}>'); lista = None
            tab.append(l); continue
        if tab: fecha()
        m = re.match(r'^(\s*)(- |\d+\. )(.*)', l)
        if m:
            tipo = 'ul' if m.group(2) == '- ' else 'ol'
            if lista != tipo:
                if lista: out.append(f'</{lista}>')
                out.append(f'<{tipo}>'); lista = tipo
            out.append(f'<li>{inline(m.group(3))}</li>'); continue
        if lista and l.startswith('  ') and l.strip():
            out[-1] = out[-1][:-5] + ' ' + inline(l.strip()) + '</li>'; continue
        fecha()
        if not l.strip() or l.strip() == '---':
            continue
        out.append(f'<p>{inline(l)}</p>')
    fecha()
    return '\n'.join(out)


def main():
    txt = FONTE.read_text(encoding='utf-8')
    partes = re.split(r'^## ', txt, flags=re.M)
    intro, secoes = partes[0], partes[1:]
    cenarios, sintese = [], ''
    for s in secoes:
        titulo, corpo = s.split('\n', 1)
        if titulo.startswith('Síntese'):
            sintese = md(corpo); continue
        cid = titulo.split(' ')[0]
        prop = {}
        for l in corpo.splitlines():
            m = re.match(r'\| (C|J|O) \| (\w+) \| (.*) \|$', l)
            if m:
                prop[m.group(1)] = {'j': m.group(2), 'just': m.group(3)}
        corpo_sem_tab = '\n'.join(l for l in corpo.splitlines() if not l.startswith('|'))
        cenarios.append({'id': cid, 'titulo': titulo, 'html': md(corpo_sem_tab), 'proposta': prop})
    tpl = (RAIZ / 'evidencias/sinteses/exame/modelo.html').read_text(encoding='utf-8')
    dados = json.dumps({'intro': md(intro.split('\n', 1)[1]), 'cenarios': cenarios, 'sintese': sintese}, ensure_ascii=False)
    SAIDA.write_text(tpl.replace('/*DADOS*/{}', dados.replace('</', '<\\/')), encoding='utf-8')
    print(len(cenarios), 'cenários;', sum(len(c['proposta']) for c in cenarios), 'propostas')


if __name__ == '__main__':
    main()
