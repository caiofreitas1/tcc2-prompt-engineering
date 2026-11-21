/* Prompt em Código — Guia e Explorador (site/DESIGN.md).
   Sem framework: lê dados.json, mantém o estado da consulta no hash e monta o DOM com
   nós de texto (nenhum dado é interpretado como HTML). Não ordena por resultado, não
   calcula média nem diferença entre valores de estudos distintos. */
(function () {
  'use strict';

  const TAREFAS = { geracao: 'Geração', depuracao: 'Depuração', traducao: 'Tradução', refatoracao: 'Refatoração' };
  const MEC = {
    instrucao: 'Instrução', contexto: 'Contexto', restricoes: 'Restrições', exemplos: 'Exemplos',
    decomposicao: 'Decomposição', feedback: 'Feedback', raciocinio: 'Raciocínio', amostragem: 'Amostragem',
    multiagente: 'Multiagente', otimizacao_prompt: 'Otimização de prompt', outro: 'Outro',
    nenhum: 'Nenhum mecanismo acrescentado',
  };
  const DIR = {
    melhora: ['↑', 'Melhora'], piora: ['↓', 'Piora'], igual: ['=', 'Igual'],
    sem_direcao: ['—', 'Sem direção'], descritiva: ['≡', 'Descritiva'],
  };
  const EVIDENCIA = { favoravel: '+', contraria: '−', dividida: '±', indireta: '≈', insuficiente: '?' };
  const RECURSOS = [
    ['testes', 'Tenho testes executáveis.', ''],
    ['executor', 'Consigo executar o código, mesmo sem suíte de testes.', ''],
    ['compilador', 'Tenho compilador para a linguagem de destino.', ''],
    ['analisador', 'Tenho analisador estático.', 'Por exemplo, um scanner de vulnerabilidades ou um medidor de complexidade.'],
    ['contexto', 'Tenho repositório, histórico ou documentação de onde recuperar contexto.', ''],
    ['exemplos', 'Tenho exemplos que posso incluir no prompt.', 'Uma descrição da tarefa e sua assinatura, sozinhas, não contam como demonstração.'],
    ['pequeno', 'Uso um modelo pequeno, executado localmente.', 'A linha G14 discute, entre outros casos, modelos de até 8 bilhões de parâmetros.'],
  ];
  const NOME_CONDICAO = {
    testes: 'testes executáveis', executor: 'executor de código', compilador: 'compilador',
    analisador: 'analisador estático', contexto: 'contexto recuperável', exemplos: 'exemplos',
    pequeno: 'modelo pequeno local', varias: 'várias chamadas',
    reproducao: 'uma forma de reproduzir o defeito', diagnostico: 'mensagem, saída ou relato do defeito',
  };
  const UNIDADE = {
    percentual: 'percentual', proporcao: 'proporção', contagem: 'contagem', qualitativo: 'qualitativo',
    tempo: 'tempo', energia: 'energia', temperatura: 'temperatura', nao_informado: 'unidade não informada pela fonte',
  };
  const SENTIDO = { maior_melhor: 'maior é melhor', menor_melhor: 'menor é melhor', nao_informado: 'sentido não informado pela fonte' };
  const ESTADOS = [
    [/\bnao_informado\b/g, 'não informado pela fonte'], [/\bnao_conferido\b/g, 'não conferido'],
    [/\bnao_aplicavel\b/g, 'não se aplica'], [/\bfonte_indisponivel\b/g, 'fonte indisponível'],
  ];
  const POR_PAGINA = 25;

  let D = null;            // dados.json
  let VERSAO = null;       // versao.json (só existe na publicação)
  const idx = { comp: new Map(), estudo: new Map(), compsDoEstudo: new Map(), linha: new Map(), cenario: new Map() };
  let seq = 0;
  let rotaAnterior = '';
  let navegouAqui = false;
  const main = document.getElementById('conteudo');

  /* ---------- utilitários ---------- */
  function h(tag, attrs, ...filhos) {
    const el = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (v === null || v === undefined || v === false) continue;
      if (k === 'class') el.className = v;
      else if (k.slice(0, 2) === 'on') el.addEventListener(k.slice(2), v);
      else if (v === true) el.setAttribute(k, '');
      else el.setAttribute(k, v);
    }
    for (const f of filhos.flat(Infinity)) {
      if (f === null || f === undefined || f === false) continue;
      el.append(f.nodeType ? f : document.createTextNode(String(f)));
    }
    return el;
  }
  const norm = (s) => String(s == null ? '' : s).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  const hum = (s) => ESTADOS.reduce((t, [re, por]) => t.replace(re, por), String(s == null ? '' : s));
  const numEstudo = (id) => parseInt(String(id).slice(1), 10);
  function dataBR(iso) {
    const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso || '');
    return m ? h('time', { datetime: m[0] }, `${m[3]}/${m[2]}/${m[1]}`) : null;
  }
  function plural(n, um, varios) { return `${n} ${n === 1 ? um : varios}`; }
  function listaE(itens, conj) {
    if (itens.length <= 1) return itens.join('');
    return itens.slice(0, -1).join(', ') + ` ${conj} ` + itens[itens.length - 1];
  }
  function valor(v, unidade) {
    if (v === null || v === undefined) return 'Sem valor registrado';
    return String(v).replace('.', ',') + (unidade === 'percentual' ? '%' : '');
  }
  function campo(dt, dd, classe) {
    if (dd === null || dd === undefined || dd === '' || (Array.isArray(dd) && !dd.length)) return null;
    return h('div', { class: classe }, h('dt', null, dt), h('dd', null, dd));
  }
  function recolhivel(rotulo, corpo, { aberto = true, classe = '' } = {}) {
    const id = 'rc-' + (++seq);
    corpo.id = id; corpo.hidden = !aberto; corpo.classList.add('rc-corpo');
    const b = h('button', {
      type: 'button', class: 'rc-botao', 'aria-expanded': String(aberto), 'aria-controls': id,
      onclick: () => { const ab = b.getAttribute('aria-expanded') !== 'true'; b.setAttribute('aria-expanded', String(ab)); corpo.hidden = !ab; },
    }, rotulo);
    return h('div', { class: 'rc ' + classe }, b, corpo);
  }
  // replaceChildren não achata listas e escreve «null»; este auxiliar faz as duas coisas.
  function trocar(el, ...filhos) {
    el.replaceChildren(...filhos.flat(Infinity).filter((f) => f !== null && f !== undefined && f !== false));
  }
  function focar(el, rolar = true) {
    if (!el) return;
    if (!el.hasAttribute('tabindex') && !/^(A|BUTTON|INPUT|SELECT|SUMMARY)$/.test(el.tagName)) el.setAttribute('tabindex', '-1');
    el.focus({ preventScroll: true });
    if (rolar) el.scrollIntoView({ block: 'start' });
  }

  /* ---------- rotas ---------- */
  function lerRota() {
    const bruto = location.hash.replace(/^#\/?/, '');
    const corte = bruto.indexOf('?');
    const caminho = corte < 0 ? bruto : bruto.slice(0, corte);
    return { partes: caminho.split('/').filter(Boolean).map(decodeURIComponent), q: new URLSearchParams(corte < 0 ? '' : bruto.slice(corte + 1)) };
  }
  function hashDe(caminho, params) {
    const s = params ? params.toString() : '';
    return '#/' + caminho + (s ? '?' + s : '');
  }
  function substituir(hash) { history.replaceState(null, '', hash); rotaAnterior = hash; }
  function hrefEstudo(id, cmp) { return hashDe('estudo/' + id, cmp ? new URLSearchParams({ cmp }) : null); }

  /* ---------- peças compartilhadas ---------- */
  function selosEvidencia(texto) {
    return h('span', { class: 'selos' }, texto.split(';').map((parte, i, todas) => {
      const t = parte.trim();
      const cat = Object.keys(EVIDENCIA).find((k) => norm(t).indexOf(k) === 0) || 'insuficiente';
      return h('span', { class: 'selo selo-' + cat }, h('span', { 'aria-hidden': 'true' }, EVIDENCIA[cat] + ' '), t,
        i < todas.length - 1 ? h('span', { class: 'so-leitor' }, ';') : null);
    }));
  }
  function seloDirecao(d) {
    const [simbolo, nome] = DIR[d] || DIR.sem_direcao;
    return h('span', { class: 'dir dir-' + d }, h('span', { 'aria-hidden': 'true' }, simbolo + ' '), nome);
  }
  function textoRevisao(r) {
    if (r.revisao_humana === 'confirmada') {
      const modo = r.conferencia === 'formulario' ? 'conferência registrada por bloco'
        : r.conferencia === 'declaracao_autor' ? 'conferência declarada pelo autor para a ficha' : null;
      return ['Revisão humana confirmada', modo ? ` · ${modo}` : '', r.data_revisao ? [' · ', dataBR(r.data_revisao)] : ''];
    }
    return r.revisao_humana === 'pendente' ? 'Revisão humana pendente' : 'Revisão humana sem registro';
  }
  // Transforma menções Sxxx e Sxxx-Cn de um texto da tabela em links para o registro.
  function comLinks(texto) {
    const partes = [];
    let ultimo = 0;
    const re = /S\d+(?:-C\d+)?/g;
    let m;
    while ((m = re.exec(texto))) {
      const ref = m[0];
      const est = ref.split('-')[0];
      const existe = ref.indexOf('-C') > 0 ? idx.comp.has(ref) : idx.estudo.has(ref);
      if (!existe) continue;
      partes.push(texto.slice(ultimo, m.index));
      partes.push(h('a', { href: hrefEstudo(est, ref.indexOf('-C') > 0 ? ref : null), class: 'id' }, ref));
      ultimo = m.index + ref.length;
    }
    partes.push(texto.slice(ultimo));
    return partes;
  }
  function linkFonte(estudo) {
    if (!estudo || !estudo.url) return null;
    const onde = /^arxiv:/i.test(estudo.identificador) ? 'no arXiv' : 'pelo DOI';
    return h('a', { href: estudo.url, rel: 'noopener', target: '_blank' }, `Abrir a fonte ${onde}`,
      h('span', { class: 'so-leitor' }, ` (${estudo.id}, abre em nova aba)`));
  }

  // Um bloco por comparação: um ID, um modelo, um benchmark, uma métrica e sua unidade.
  function blocoComparacao(c, { nivel = 'h4', linkEstudo = true, destaque = false } = {}) {
    const estudo = idx.estudo.get(c.estudo);
    const semDirecao = c.direcao === 'sem_direcao'
      ? 'Falta um par numérico ou um sentido definido para a métrica.'
      : c.direcao === 'descritiva' ? 'O registro apresenta um resultado sem comparador.' : null;
    const detalhes = h('dl', { class: 'campos' },
      campo('Mecanismos acrescentados à base', c.acrescentados.length ? c.acrescentados.map((m) => MEC[m] || m).join(', ') : 'Nenhum registrado'),
      campo('Condições da comparação', hum(c.condicoes)),
      campo('Denominador', hum(c.denominador)),
      campo('Origem da extração', [`Extração por IA · ${c.executor || 'executor não registrado'}`,
        c.modelo_executor ? ` · ${c.modelo_executor}` : '', c.data ? [' · ', dataBR(c.data) || hum(c.data)] : '']));
    return h('article', { class: 'comparacao' + (destaque ? ' destaque' : ''), id: 'cmp-' + c.id },
      h('header', null,
        h(nivel, { class: 'cmp-titulo' }, h('span', { class: 'id' }, c.id), ' · ', hum(c.benchmark)),
        h('p', { class: 'cmp-contexto' }, `${hum(c.modelo)} · ${TAREFAS[c.tarefa] || c.tarefa}`)),
      h('dl', { class: 'par completo' },
        campo('Métrica', `${hum(c.metrica)} · ${UNIDADE[c.unidade] || c.unidade} · ${SENTIDO[c.sentido] || c.sentido}`),
        campo(c.comparador ? `Base · ${hum(c.comparador)}` : 'Base · sem comparador', h('span', { class: 'num' }, valor(c.base, c.unidade)), 'valor'),
        campo(`Intervenção · ${hum(c.tecnica)}`, h('span', { class: 'num' }, valor(c.intervencao, c.unidade)), 'valor'),
        campo('Direção nesta métrica', [seloDirecao(c.direcao), semDirecao ? h('span', { class: 'secundario' }, ' ' + semDirecao) : null]),
        campo('Onde está na fonte', hum(c.localizador), 'larga'),
        campo('Conferência', ['Extração por IA · ', textoRevisao(c)], 'larga')),
      h('details', null, h('summary', null, `Detalhes de ${c.id}`), detalhes),
      h('p', { class: 'acoes' },
        linkEstudo ? h('a', { href: hrefEstudo(c.estudo, c.id) }, `Ver ${c.id} no estudo ${c.estudo}`) : null,
        linkFonte(estudo)));
  }

  function paginacao(total, pagina, hrefPagina, rotulo) {
    const paginas = Math.max(1, Math.ceil(total / POR_PAGINA));
    if (paginas <= 1) return null;
    const link = (texto, p) => (p < 1 || p > paginas)
      ? h('span', { class: 'botao', 'aria-disabled': 'true' }, texto)
      : h('a', { class: 'botao', href: hrefPagina(p) }, texto);
    const de = (pagina - 1) * POR_PAGINA + 1;
    return h('nav', { class: 'paginacao', 'aria-label': 'Paginação de ' + rotulo },
      link('Anterior', pagina - 1),
      h('span', { class: 'secundario' }, `Página ${pagina} de ${paginas} · ${de} a ${Math.min(total, de + POR_PAGINA - 1)} de ${total}`),
      link('Próxima', pagina + 1));
  }

  /* ---------- Guia ---------- */
  function estadoGuia(q) {
    const e = { tarefa: '', r: new Set(), ch: '', rep: '', diag: '', cenario: '', linha: '' };
    const cen = idx.cenario.get(q.get('cenario'));
    if (cen && !q.has('tarefa')) return aplicarCenario(cen, q.get('linha'));
    if (TAREFAS[q.get('tarefa')]) e.tarefa = q.get('tarefa');
    q.getAll('r').forEach((x) => { if (RECURSOS.some((r) => r[0] === x)) e.r.add(x); });
    if (['uma', 'varias'].includes(q.get('ch'))) e.ch = q.get('ch');
    if (['teste', 'outro', 'nao'].includes(q.get('rep'))) e.rep = q.get('rep');
    if (['sim', 'nao'].includes(q.get('diag'))) e.diag = q.get('diag');
    if (cen) e.cenario = cen.id;
    if (idx.linha.has(q.get('linha'))) e.linha = q.get('linha');
    return e;
  }
  function aplicarCenario(c, linha) {
    return { tarefa: c.tarefa, r: new Set(c.recursos), ch: c.chamadas, rep: c.reproducao, diag: c.diagnostico,
      cenario: c.id, linha: idx.linha.has(linha) ? linha : '' };
  }
  function paramsGuia(e) {
    const p = new URLSearchParams();
    if (e.tarefa) p.set('tarefa', e.tarefa);
    RECURSOS.forEach(([k]) => { if (e.r.has(k)) p.append('r', k); });
    if (e.ch) p.set('ch', e.ch);
    if (e.tarefa === 'depuracao') { if (e.rep) p.set('rep', e.rep); if (e.diag) p.set('diag', e.diag); }
    if (e.cenario) p.set('cenario', e.cenario);
    if (e.linha) p.set('linha', e.linha);
    return p;
  }
  function condicoes(e) {
    const c = new Set(e.r);
    if (e.ch === 'varias') c.add('varias');
    if (e.tarefa === 'depuracao') {
      if (e.rep === 'teste' || e.rep === 'outro') c.add('reproducao');
      if (e.diag === 'sim') c.add('diagnostico');
    }
    return c;
  }
  // Mesma regra de scripts/gerar_site.py (faltas e classificar).
  function faltas(regra, cond) {
    if (!regra.length) return [];
    const pend = regra.map((alt) => alt.filter((t) => !cond.has(t)));
    if (pend.some((p) => !p.length)) return [];
    const unicos = [];
    pend.forEach((p) => { if (!unicos.some((u) => u.join() === p.join())) unicos.push(p); });
    return unicos.filter((p) => !unicos.some((u) => u !== p && u.length < p.length && u.every((t) => p.includes(t))));
  }
  function grupoDaLinha(l, cond) {
    if (l.grupo !== 'normal') return 'lacuna';
    return faltas(l.regra, cond).length ? 'falta' : 'aplicavel';
  }
  function textoRegra(regra) {
    if (!regra.length) return 'nenhum dos recursos do formulário';
    if (regra.every((alt) => alt.length === 1)) return listaE(regra.map((alt) => NOME_CONDICAO[alt[0]]), 'ou');
    return regra.map((alt) => listaE(alt.map((t) => NOME_CONDICAO[t]), 'e')).join('; ou ');
  }
  function motivo(l, grupo, e, cond) {
    if (grupo === 'lacuna') return l.grupo === 'lacuna_parcial' ? 'Lacuna parcial, por variante.' : null;
    if (grupo === 'aplicavel') return l.incerta ? 'Aplicação parcial. Confira a variante e as condições estudadas.' : null;
    const f = faltas(l.regra, cond);
    if (f.some((alt) => alt.includes('reproducao')) && e.rep === 'nao') {
      return (e.r.has('testes') ? 'A suíte roda, mas não reproduz o defeito. Ela pode apontar regressões. ' : 'Você indicou que não consegue reproduzir o defeito. ')
        + `A linha ${l.id} exige uma forma de observar a falha.`;
    }
    const nomes = (alt) => listaE(alt.map((t) => (t === 'varias' && e.ch === 'uma') ? 'várias chamadas (você indicou uma)' : NOME_CONDICAO[t]), 'e');
    const simples = f.every((alt) => alt.length === 1);
    return 'Para esta linha, falta indicar ' + (simples ? listaE(f.map(nomes), 'ou') : f.map(nomes).join('; ou ')) + '.';
  }

  function verGuia(q) {
    let e = estadoGuia(q);
    const controles = {};
    const status = h('p', { class: 'so-leitor', role: 'status' });
    const resultados = h('div', { id: 'guia-resultados' });

    function mudar(alteracao) {
      alteracao(e);
      e.cenario = '';
      substituir(hashDe('guia', paramsGuia(e)));
      sincronizar();
      desenharResultados(true);
    }
    function sincronizar() {
      Object.keys(TAREFAS).forEach((t) => { controles['t-' + t].checked = e.tarefa === t; });
      RECURSOS.forEach(([k]) => { controles['r-' + k].checked = e.r.has(k); });
      controles.ch.value = e.ch; controles.rep.value = e.rep; controles.diag.value = e.diag;
      controles.depuracao.hidden = e.tarefa !== 'depuracao';
    }

    const fTarefa = h('fieldset', null, h('legend', null, 'O que você precisa fazer?'),
      h('div', { class: 'opcoes-tarefa' }, Object.entries(TAREFAS).map(([k, nome]) => {
        const inp = h('input', { type: 'radio', name: 'tarefa', value: k, onchange: () => mudar((s) => { s.tarefa = k; s.linha = ''; }) });
        controles['t-' + k] = inp;
        return h('label', { class: 'opcao' }, inp, h('span', null, nome));
      })));
    const fRecursos = h('fieldset', null, h('legend', null, 'Quais recursos você tem?'),
      h('p', { class: 'ajuda', id: 'ajuda-recursos' }, 'Marque o que você pode usar. Uma caixa em branco significa que o recurso ainda não foi indicado.'),
      RECURSOS.map(([k, rotulo, ajuda]) => {
        const inp = h('input', { type: 'checkbox', value: k, 'aria-describedby': ajuda ? 'ajuda-' + k : null,
          onchange: () => mudar((s) => {
            if (inp.checked) s.r.add(k); else { s.r.delete(k); if (k === 'testes' && s.rep === 'teste') s.rep = ''; }
          }) });
        controles['r-' + k] = inp;
        return h('label', { class: 'opcao' }, inp, h('span', null, rotulo, ajuda ? h('span', { class: 'ajuda', id: 'ajuda-' + k }, ' ' + ajuda) : null));
      }));
    const seletor = (nome, rotulo, ajuda, opcoes, aoMudar) => {
      const sel = h('select', { 'aria-describedby': ajuda ? 'ajuda-' + nome : null, onchange: () => mudar((s) => aoMudar(s, sel.value)) },
        opcoes.map(([v, t]) => h('option', { value: v }, t)));
      controles[nome] = sel;
      return h('label', { class: 'campo' }, h('span', null, rotulo), sel, ajuda ? h('span', { class: 'ajuda', id: 'ajuda-' + nome }, ajuda) : null);
    };
    const fChamadas = seletor('ch', 'Quantas chamadas ao modelo você pode usar?',
      'Várias chamadas podem permitir uma nova tentativa ou etapa. Confira o orçamento específico de cada estudo.',
      [['', 'Ainda não sei'], ['uma', 'Uma chamada'], ['varias', 'Várias chamadas']], (s, v) => { s.ch = v; });
    controles.depuracao = h('div', null,
      seletor('rep', 'Você consegue reproduzir o defeito?', 'Uma suíte que roda, mas não dispara a falha, não reproduz o defeito.',
        [['', 'Ainda não sei'], ['teste', 'Por teste'], ['outro', 'Por depurador ou contraexemplo'], ['nao', 'Não']],
        (s, v) => { s.rep = v; if (v === 'teste') s.r.add('testes'); }),
      seletor('diag', 'Você tem uma mensagem, saída ou relato do defeito?', '',
        [['', 'Ainda não sei'], ['sim', 'Sim'], ['nao', 'Não']], (s, v) => { s.diag = v; }));
    const corpoForm = h('form', { onsubmit: (ev) => ev.preventDefault(), 'aria-label': 'Condições de uso' },
      fTarefa, fRecursos, fChamadas, controles.depuracao,
      h('button', { type: 'button', class: 'botao', onclick: () => focar(document.getElementById('titulo-resultados')) }, 'Ir aos resultados'));
    const painelForm = h('section', { class: 'painel', 'aria-label': 'Condições' },
      recolhivel('Editar condições', corpoForm, { aberto: !e.cenario, classe: 'rc-desktop' }));

    function blocoCenarios(aberto) {
      const corpo = h('div', { class: 'cenarios' },
        h('p', { class: 'ajuda' }, 'Estes oito cenários são sintéticos. Foram usados para examinar a tabela de apoio. Você pode alterar as condições depois de escolher um exemplo.'),
        Object.entries(TAREFAS).map(([t, nome]) => h('div', { class: 'cenarios-grupo', role: 'group', 'aria-label': 'Cenários de ' + nome.toLowerCase() },
          h('span', null, nome),
          D.cenarios.filter((c) => c.tarefa === t).map((c) => h('button', {
            type: 'button', class: 'botao chip', 'aria-pressed': String(e.cenario === c.id),
            'aria-label': `Cenário ${c.id}: ${c.nome_botao}${e.cenario === c.id ? ' (em uso)' : ''}`,
            onclick: () => { location.hash = hashDe('guia', paramsGuia(aplicarCenario(c, ''))); },
          }, c.nome_botao, e.cenario === c.id ? h('span', { class: 'secundario' }, ' · Em uso') : null)))));
      return recolhivel(aberto ? 'Comece por um dos 8 cenários' : 'Usar um dos 8 cenários', corpo, { aberto });
    }

    function cartaoLinha(l, grupo, cond) {
      const painelId = 'painel-' + l.id;
      const painel = h('div', { class: 'linha-painel', id: painelId, hidden: true });
      const acao = h('span', { class: 'acao', 'aria-hidden': 'true' }, 'Abrir');
      const botao = h('button', {
        type: 'button', class: 'linha-botao', 'aria-expanded': 'false', 'aria-controls': painelId, id: 'botao-' + l.id,
        'aria-label': `Abrir linha ${l.id}, ${l.agrupamento}`,
        onclick: () => alternar(!painel.hidden ? '' : l.id),
      }, h('span', { class: 'id' }, l.id), h('span', null, l.agrupamento, l.tarefa === 'todas' ? ' · Todas as tarefas' : ''), acao);
      const txtMotivo = motivo(l, grupo, e, cond);
      const artigo = h('article', { class: 'linha', id: 'linha-' + l.id },
        h('h4', null, botao),
        h('div', { class: 'linha-resumo' },
          h('p', null, h('span', { class: 'rotulo' }, 'Evidência da linha '), selosEvidencia(l.evidencia)),
          h('p', null, h('span', { class: 'rotulo' }, 'Resultado medido '), l.resultado_medido)),
        txtMotivo ? h('p', { class: 'motivo' }, txtMotivo) : null,
        painel);
      artigo.abrir = (aberto) => {
        if (aberto && !painel.childNodes.length) preencherPainel(l, painel);
        painel.hidden = !aberto;
        botao.setAttribute('aria-expanded', String(aberto));
        botao.setAttribute('aria-label', `${aberto ? 'Recolher' : 'Abrir'} linha ${l.id}, ${l.agrupamento}`);
        acao.textContent = aberto ? 'Recolher' : 'Abrir';
      };
      return artigo;
    }
    function preencherPainel(l, painel) {
      const comps = l.comparacoes.map((r) => idx.comp.get(r.id)).filter(Boolean);
      const semRegistro = l.comparacoes.concat(l.estudos).filter((r) => !r.registrada);
      trocar(painel,
        h('dl', { class: 'campos' },
          campo('Condição estudada e verificação', l.condicao),
          campo('Resultado medido', l.resultado_medido),
          campo('Indicação da tabela', comLinks(l.indicacao)),
          campo('Força descritiva', l.forca),
          campo('Ressalvas', comLinks(l.ressalvas))),
        h('aside', { class: 'aviso' },
          h('h5', null, 'Como este Guia classificou a linha'),
          h('p', null, l.grupo === 'normal' ? `Recursos considerados: ${textoRegra(l.regra)}. ` : 'Linha tratada como lacuna declarada. ', l.nota),
          h('p', null, 'Esta classificação é uma decisão editorial do site. O texto científico é o da tabela.')),
        h('h5', null, `Comparações citadas (${comps.length})`),
        comps.length ? comps.map((c) => blocoComparacao(c, { nivel: 'h6' })) : h('p', { class: 'vazio' }, 'Esta linha não cita comparações com par de valores.'),
        l.estudos.length ? [h('h5', null, 'Estudos citados'),
          h('ul', { class: 'lista-estudos' }, l.estudos.filter((r) => r.registrada).map((r) => {
            const s = idx.estudo.get(r.id);
            return h('li', null, h('a', { href: hrefEstudo(r.id) }, h('span', { class: 'id' }, r.id), ' · ', s.titulo));
          }))] : null,
        semRegistro.length ? h('p', { class: 'secundario' }, 'Referência sem registro nesta versão: ' + semRegistro.map((r) => r.id).join(', ') + '.') : null);
    }
    let cartoes = [];
    function alternar(id) {
      e.linha = id;
      cartoes.forEach((c) => c.abrir(c.id === 'linha-' + id));
      substituir(hashDe('guia', paramsGuia(e)));
    }

    function desenharResultados(anunciar) {
      cartoes = [];
      if (!e.tarefa) {
        trocar(resultados, blocoCenarios(true), h('p', { class: 'vazio' }, 'Selecione uma tarefa para consultar o Guia.'));
        return;
      }
      const cond = condicoes(e);
      const linhas = D.linhas.filter((l) => l.tarefa === e.tarefa || l.tarefa === 'todas');
      const grupos = { aplicavel: [], falta: [], lacuna: [] };
      linhas.forEach((l) => grupos[grupoDaLinha(l, cond)].push(l));
      const defs = [
        ['aplicavel', 'Aplicáveis às condições marcadas', 'Estas linhas têm ao menos uma forma de uso compatível com os recursos informados. Leia o resultado medido e as ressalvas: uma linha aplicável pode ter evidência dividida, indireta ou contrária.'],
        ['falta', 'Exigem recurso não marcado', 'Estas linhas dependem de um recurso que você ainda não indicou.'],
        ['lacuna', 'Lacunas declaradas', 'A revisão identificou evidência insuficiente para estas condições. Abra a linha para ver o que chegou a ser medido.'],
      ];
      const cen = idx.cenario.get(e.cenario);
      const secoes = defs.map(([k, titulo, ajuda]) => {
        const cs = grupos[k].map((l) => cartaoLinha(l, k, cond));
        cartoes = cartoes.concat(cs);
        return h('section', { class: 'grupo', 'aria-labelledby': 'grupo-' + k },
          h('h3', { id: 'grupo-' + k, tabindex: '-1' }, `${titulo} (${grupos[k].length})`),
          h('p', { class: 'ajuda' }, ajuda),
          cs.length ? cs : h('p', { class: 'vazio' }, k === 'aplicavel'
            ? 'Nenhuma linha atende aos recursos marcados. Veja os recursos exigidos e as lacunas desta tarefa.'
            : 'Nenhuma linha deste grupo para as condições atuais.'));
      });
      trocar(resultados,
        h('h2', { id: 'titulo-resultados', tabindex: '-1' }, `${TAREFAS[e.tarefa]} · ${plural(linhas.length, 'linha', 'linhas')}`),
        cen ? h('div', { class: 'cenario-em-uso' },
          h('p', null, h('strong', null, `Cenário ${cen.id} · ${cen.nome_botao}`)),
          h('p', null, cen.resumo),
          h('details', null, h('summary', null, 'Descrição completa e hipótese do exame'),
            h('dl', null, campo('Domínio: ', cen.dominio), campo('Modelo: ', cen.modelo), campo('Verificação: ', cen.verificacao),
              campo('Orçamento: ', cen.orcamento), campo('Objetivo: ', cen.objetivo), campo('Hipótese do exame: ', cen.hipotese)))) : null,
        h('p', { class: 'ajuda' }, `As ${D.meta.n_linhas} linhas de apoio foram elaboradas a partir de sínteses de ${D.meta.fichas_nas_sinteses} fichas e aparecem na ordem da tabela, sem ranking.`),
        h('div', { class: 'saltos' },
          defs.map(([k, titulo]) => h('button', { type: 'button', class: 'botao', onclick: () => focar(document.getElementById('grupo-' + k)) },
            `${titulo.split(' ')[0]} ${k === 'falta' ? 'recurso ' : ''}(${grupos[k].length})`)),
          h('a', { class: 'botao', href: '#/sobre?sec=como-ler' }, 'Como ler')),
        blocoCenarios(false),
        secoes);
      if (e.linha) cartoes.forEach((c) => c.abrir(c.id === 'linha-' + e.linha));
      if (anunciar) status.textContent = `${TAREFAS[e.tarefa]}: ${grupos.aplicavel.length} aplicáveis, ${grupos.falta.length} exigem recurso, ${grupos.lacuna.length} lacunas.`;
    }

    sincronizar();
    desenharResultados(false);
    const vista = h('div', null,
      h('h1', { tabindex: '-1' }, 'Guia por tarefa'),
      h('p', { class: 'introducao' }, 'Consulte o que os estudos mediram para sua tarefa e seus recursos.'),
      status,
      h('div', { class: 'colunas' }, painelForm, resultados));
    return { titulo: 'Guia', vista, foco: () => (e.linha && document.getElementById('botao-' + e.linha)) || (e.cenario && document.getElementById('titulo-resultados')) || null };
  }

  /* ---------- Explorador ---------- */
  function estadoExplorador(q) {
    const vista = ['matriz', 'estudos'].includes(q.get('vista')) ? q.get('vista') : '';
    return {
      vista, q: q.get('q') || '',
      tarefa: TAREFAS[q.get('tarefa')] ? q.get('tarefa') : '',
      mec: MEC[q.get('mec')] ? q.get('mec') : '',
      dir: DIR[q.get('dir')] ? q.get('dir') : '',
      p: Math.max(1, parseInt(q.get('p'), 10) || 1),
    };
  }
  function paramsExplorador(e, extra) {
    const p = new URLSearchParams();
    const s = Object.assign({}, e, extra || {});
    if (s.vista) p.set('vista', s.vista);
    if (s.vista !== 'estudos') {
      if (s.vista !== 'matriz') { if (s.tarefa) p.set('tarefa', s.tarefa); if (s.mec) p.set('mec', s.mec); }
      if (s.dir) p.set('dir', s.dir);
    }
    if (s.q) p.set('q', s.q);
    if (s.p > 1) p.set('p', String(s.p));
    return p;
  }
  function temMecanismo(c, mec) { return mec === 'nenhum' ? !c.acrescentados.length : c.acrescentados.includes(mec); }
  function filtrarComparacoes(e, { ignorarEixos = false } = {}) {
    const termos = norm(e.q).split(/\s+/).filter(Boolean);
    return D.comparacoes.filter((c) => (ignorarEixos || !e.tarefa || c.tarefa === e.tarefa)
      && (ignorarEixos || !e.mec || temMecanismo(c, e.mec))
      && (!e.dir || c.direcao === e.dir)
      && termos.every((t) => c._busca.includes(t)));
  }

  function verExplorador(q) {
    const e = estadoExplorador(q);
    const saida = h('div', { id: 'explorador-saida' });
    const contador = h('span', null);
    let espera = null;

    const aba = (vista, rotulo) => h('a', {
      href: hashDe('explorador', paramsExplorador({ vista, q: '', tarefa: e.tarefa, mec: e.mec, dir: e.dir, p: 1 })),
      'aria-current': e.vista === vista ? 'page' : null,
    }, rotulo);

    function atualizar() {
      e.p = 1;
      substituir(hashDe('explorador', paramsExplorador(e)));
      desenhar();
    }
    const busca = h('input', {
      type: 'search', value: e.q, autocomplete: 'off',
      placeholder: e.vista === 'estudos' ? 'ID ou título' : 'ID, modelo, benchmark…',
      oninput: () => { clearTimeout(espera); espera = setTimeout(() => { e.q = busca.value.trim(); atualizar(); }, 250); },
    });
    const seletor = (chave, rotulo, opcoes) => {
      const sel = h('select', { onchange: () => { e[chave] = sel.value; atualizar(); } },
        h('option', { value: '' }, chave === 'mec' ? 'Todos' : 'Todas'), opcoes.map(([v, t]) => h('option', { value: v }, t)));
      sel.value = e[chave];
      return h('label', { class: 'campo' }, h('span', null, rotulo), sel);
    };
    const controles = [h('label', { class: 'campo' }, h('span', null, e.vista === 'estudos' ? 'Buscar estudo' : 'Buscar'), busca,
      e.vista === 'estudos' ? null : h('span', { class: 'ajuda' }, 'Procura em ID, título do estudo, técnica, comparador, modelo, benchmark e métrica. Todos os termos precisam aparecer.'))];
    const selects = [];
    if (e.vista === '') {
      selects.push(seletor('tarefa', 'Tarefa', Object.entries(TAREFAS)));
      selects.push(seletor('mec', 'Mecanismo acrescentado', D.meta.mecanismos.concat('nenhum').map((m) => [m, MEC[m]])));
    }
    if (e.vista !== 'estudos') selects.push(seletor('dir', 'Direção da comparação', Object.entries(DIR).map(([k, v]) => [k, v[1]])));
    const formulario = h('form', { role: 'search', 'aria-label': e.vista === 'estudos' ? 'Buscar estudos' : 'Filtrar comparações', onsubmit: (ev) => ev.preventDefault() },
      controles, selects,
      h('div', { class: 'botoes' },
        h('button', { type: 'button', class: 'botao', onclick: () => {
          e.q = ''; e.tarefa = ''; e.mec = ''; e.dir = ''; busca.value = '';
          formulario.querySelectorAll('select').forEach((s) => { s.value = ''; });
          atualizar();
        } }, 'Limpar filtros'),
        h('button', { type: 'button', class: 'botao botao-acao so-estreito', onclick: () => focar(document.getElementById('titulo-lista')) }, 'Ver resultados')));
    const painel = h('section', { class: 'painel', 'aria-label': 'Filtros' },
      recolhivel(h('span', null, 'Filtros ', contador), formulario, { aberto: false, classe: 'rc-desktop' }));

    function desenhar() {
      const ativos = [e.q, e.vista === '' && e.tarefa, e.vista === '' && e.mec, e.vista !== 'estudos' && e.dir].filter(Boolean).length;
      contador.textContent = `(${ativos})`;
      if (e.vista === 'matriz') desenharMatriz();
      else if (e.vista === 'estudos') desenharEstudos();
      else desenharLista();
    }
    function desenharLista() {
      const itens = filtrarComparacoes(e);
      const paginas = Math.max(1, Math.ceil(itens.length / POR_PAGINA));
      const p = Math.min(e.p, paginas);
      trocar(saida,
        h('h2', { id: 'titulo-lista', tabindex: '-1', class: 'total', role: 'status' }, plural(itens.length, 'comparação', 'comparações')),
        h('p', { class: 'ajuda' }, `${D.meta.n_comparacoes} comparações em um corpus de ${D.meta.n_estudos} estudos, na ordem das extrações. Há estudos com ficha e sem comparação extraída.`),
        itens.length ? itens.slice((p - 1) * POR_PAGINA, p * POR_PAGINA).map((c) => blocoComparacao(c, { nivel: 'h3' }))
          : h('p', { class: 'vazio' }, 'Nenhuma comparação corresponde aos filtros atuais.'),
        paginacao(itens.length, p, (n) => hashDe('explorador', paramsExplorador(e, { p: n })), 'comparações'));
    }
    function desenharMatriz() {
      const base = filtrarComparacoes(e, { ignorarEixos: true });
      const mecs = D.meta.mecanismos.concat('nenhum');
      const conta = (t, m) => base.filter((c) => c.tarefa === t && temMecanismo(c, m)).length;
      const celula = (t, m) => {
        const n = conta(t, m);
        if (!n) return h('span', { class: 'secundario' }, '0');
        return h('a', {
          href: hashDe('explorador', paramsExplorador({ vista: '', tarefa: t, mec: m, dir: e.dir, q: e.q, p: 1 })),
          'aria-label': `Ver ${plural(n, 'comparação', 'comparações')} de ${TAREFAS[t].toLowerCase()} com ${m === 'nenhum' ? 'nenhum mecanismo acrescentado' : MEC[m].toLowerCase() + ' acrescentado'}`,
        }, n);
      };
      const tabela = h('div', { class: 'matriz-larga matriz-envelope' }, h('table', { class: 'matriz' },
        h('caption', null, 'Comparações por mecanismo acrescentado e tarefa'),
        h('thead', null, h('tr', null, h('th', { scope: 'col' }, 'Mecanismo acrescentado'), Object.values(TAREFAS).map((t) => h('th', { scope: 'col' }, t)))),
        h('tbody', null, mecs.map((m) => h('tr', null, h('th', { scope: 'row' }, MEC[m]), Object.keys(TAREFAS).map((t) => h('td', null, celula(t, m))))))));
      const celular = h('div', { class: 'matriz-celular' }, Object.entries(TAREFAS).map(([t, nome], i) => h('details', { open: i === 0 },
        h('summary', null, nome), h('ul', null, mecs.map((m) => h('li', null, h('span', null, MEC[m]), celula(t, m)))))));
      trocar(saida,
        h('h2', { id: 'titulo-lista', tabindex: '-1', class: 'total' }, 'Comparações por tarefa e mecanismo acrescentado'),
        h('p', { class: 'ajuda', role: 'status' }, `${plural(base.length, 'comparação considerada', 'comparações consideradas')} com os filtros atuais.`),
        tabela, celular,
        h('aside', { class: 'aviso' }, h('p', null, 'Cada célula conta comparações distintas. Uma comparação com vários mecanismos acrescentados aparece em mais de uma célula. As contagens descrevem o que foi extraído; não indicam qual mecanismo funciona melhor.')));
    }
    function desenharEstudos() {
      const termos = norm(e.q).split(/\s+/).filter(Boolean);
      const itens = D.estudos.filter((s) => termos.every((t) => s._busca.includes(t)));
      const paginas = Math.max(1, Math.ceil(itens.length / POR_PAGINA));
      const p = Math.min(e.p, paginas);
      trocar(saida,
        h('h2', { id: 'titulo-lista', tabindex: '-1', class: 'total', role: 'status' }, plural(itens.length, 'estudo', 'estudos')),
        itens.length ? h('ul', null, itens.slice((p - 1) * POR_PAGINA, p * POR_PAGINA).map((s) => h('li', { class: 'item-estudo' },
          h('a', { href: hrefEstudo(s.id) }, h('span', { class: 'id' }, s.id), ' · ', s.titulo),
          h('span', { class: 'secundario' }, `Ano do registro ${s.ano} · ${s.tarefas.map((t) => TAREFAS[t] || t).join(', ')} · `,
            s.n_comparacoes ? plural(s.n_comparacoes, 'comparação', 'comparações') : 'sem comparação extraída'))))
          : h('p', { class: 'vazio' }, 'Nenhum estudo corresponde à busca.'),
        paginacao(itens.length, p, (n) => hashDe('explorador', paramsExplorador(e, { p: n })), 'estudos'));
    }

    desenhar();
    const vista = h('div', null,
      h('h1', { tabindex: '-1' }, 'Explorador'),
      h('p', { class: 'introducao' }, 'Consulte cada comparação extraída dos estudos, com seus valores e sua localização na fonte.'),
      h('nav', { class: 'abas', 'aria-label': 'Vistas do Explorador' }, aba('', 'Comparações'), aba('matriz', 'Matriz'), aba('estudos', 'Estudos')),
      h('div', { class: 'colunas' }, painel, saida));
    const mesmaVista = /^#\/explorador/.test(rotaAnterior) && estadoExplorador(new URLSearchParams(rotaAnterior.split('?')[1] || '')).vista === e.vista;
    return { titulo: 'Explorador', vista, foco: () => (mesmaVista ? document.getElementById('titulo-lista') : null) };
  }

  /* ---------- Estudo ---------- */
  function verEstudo(id, q) {
    const s = idx.estudo.get(id);
    if (!s) {
      return { titulo: 'Estudo não encontrado', vista: h('div', null, h('h1', { tabindex: '-1' }, 'Estudo não encontrado'),
        h('p', null, `O identificador «${id}» não consta entre as fichas desta versão.`),
        h('p', null, h('a', { class: 'botao', href: '#/explorador?vista=estudos' }, 'Abrir o índice de estudos'))) };
    }
    const comps = (idx.compsDoEstudo.get(id) || []);
    const alvo = q.get('cmp');
    const alvoValido = alvo && comps.some((c) => c.id === alvo);
    const grupoTecnicas = (papel, titulo) => {
      const ts = s.tecnicas.filter((t) => t.papel === papel);
      if (!ts.length) return null;
      return [h('h4', null, `${titulo} (${ts.length})`), h('ul', { class: 'marcadores' }, ts.map((t) => h('li', null, hum(t.nome),
        t.acrescentados.length ? h('span', { class: 'secundario' }, ' · acrescenta ' + t.acrescentados.map((m) => (MEC[m] || m).toLowerCase()).join(', ')) : null)))];
    };
    const lista = (titulo, itens) => (itens.length ? [h('h3', null, titulo), h('ul', { class: 'marcadores' }, itens.map((x) => h('li', null, hum(x))))] : null);
    const ficha = h('section', { class: 'painel ficha', 'aria-label': 'Ficha do estudo' },
      h('h3', null, 'Tarefas'), h('p', null, s.tarefas.map((t) => TAREFAS[t] || t).join(', ')),
      h('h3', null, 'Técnicas'), grupoTecnicas('focal', 'Focais'), grupoTecnicas('comparador', 'Comparadores'),
      s.tecnicas.some((t) => t.papel === 'componente') ? h('details', null, h('summary', null, 'Componentes das técnicas'), grupoTecnicas('componente', 'Componentes')) : null,
      lista('Modelos', s.modelos), lista('Benchmarks', s.benchmarks), lista('Linguagens', s.linguagens),
      h('h3', null, `Riscos registrados (${s.riscos.length})`),
      s.riscos.length ? h('details', null, h('summary', null, 'Ver riscos descritos na ficha'),
        s.riscos.map((r) => h('p', { class: 'risco' }, h('strong', null, hum(String(r.categoria || '').replace(/_/g, ' ')) + '. '), hum(r.descricao),
          r.localizador ? h('span', { class: 'secundario' }, ` (${hum(r.localizador)})`) : null)))
        : h('p', { class: 'secundario' }, 'Nenhum risco registrado na ficha.'),
      h('h3', null, 'Conferência da ficha'),
      h('p', null, `Extração por IA · ${s.executor || 'executor não registrado'}${s.modelo_executor ? ' · ' + s.modelo_executor : ''}`, s.data ? [' · ', dataBR(s.data) || hum(s.data)] : ''),
      h('p', null, textoRevisao(s)),
      s.metadados_conferidos !== 'sim' ? h('p', { class: 'secundario' }, 'Título, ano e identificador vêm do registro da busca e ainda não foram conferidos no original.') : null);
    const versao = /^v\d+$/.test(s.versao) || (s.versao && !/^nao_/.test(s.versao)) ? ` · Versão cadastrada ${s.versao}` : '';
    const vista = h('div', null,
      h('p', null, navegouAqui
        ? h('button', { type: 'button', class: 'botao', onclick: () => history.back() }, '← Voltar')
        : h('a', { class: 'botao', href: '#/explorador?vista=estudos' }, '← Índice de estudos')),
      h('div', { class: 'cabecalho-estudo' },
        h('p', { class: 'secundario' }, `Estudo `, h('span', { class: 'id' }, s.id), ` · Ano do registro ${s.ano}`),
        h('h1', { tabindex: '-1' }, s.titulo),
        h('p', null, h('span', { class: 'id' }, s.identificador), versao, ' · ', linkFonte(s) || 'Sem link para a fonte nesta versão')),
      alvo && !alvoValido ? h('aside', { class: 'aviso' }, h('p', null, 'Esta comparação não consta neste estudo. Veja abaixo as comparações do estudo.')) : null,
      h('div', { class: 'colunas colunas-estudo' }, ficha,
        h('section', { 'aria-labelledby': 'titulo-comps' },
          h('h2', { id: 'titulo-comps' }, `Comparações do estudo (${comps.length})`),
          comps.length ? comps.map((c) => blocoComparacao(c, { nivel: 'h3', linkEstudo: false, destaque: c.id === alvo }))
            : h('p', { class: 'vazio' }, 'Este estudo tem ficha no corpus. Nenhuma comparação foi extraída para ele nesta versão.'))));
    return { titulo: `${s.id} · ${s.titulo}`, vista, foco: () => (alvoValido ? document.getElementById('cmp-' + alvo) : null) };
  }

  /* ---------- Sobre ---------- */
  function verSobre(q) {
    const m = D.meta;
    const mod = m.estudos_revisados_por_modalidade || {};
    const secoes = [
      ['metodo', 'Método e recorte', [
        h('p', null, 'Este site apresenta os dados de uma revisão rápida da literatura sobre engenharia de prompt para geração, depuração, tradução e refatoração de código. A revisão é o Trabalho de Conclusão de Curso de Caio César de Freitas, no curso de Engenharia de Sistemas da UFMG.'),
        h('p', null, 'A busca foi feita no arXiv, no IEEE Xplore e na ACM Digital Library, para publicações de ', dataBR(m.periodo_inicio), ' a ', dataBR(m.data_corte), ', em português ou inglês. Segundo o resumo da monografia, ela resultou em 2.304 estudos únicos; 715 tinham a tarefa no título e foram triados por dois modelos de linguagem, com conferência do autor; no texto completo, o autor conferiu os 419 estudos lidos pelos modelos e incluiu 332.'),
        h('p', null, 'As principais limitações declaradas são a exigência da tarefa no título, a exclusão dos estudos que estão só no arXiv e a extração por IA, conferida pelo autor só numa amostra.'),
      ]],
      ['como-ler', 'Como ler', [
        h('p', null, 'Comece pela tarefa e pelas condições de uso. Cada linha do Guia reúne estudos sobre um agrupamento de técnicas. Leia juntos a condição estudada, o resultado medido, a indicação e as ressalvas. «Aplicável» significa que os recursos marcados permitem ao menos uma forma de uso descrita. A evidência dessa forma de uso pode ser dividida, indireta ou contrária.'),
        h('p', null, '«Favorável», «contrária» e «dividida» descrevem a direção das comparações do agrupamento. «Favorável» indica que a maioria das comparações registrou melhora na métrica de cada estudo, e não que a técnica funcionará em outro projeto. «Indireta» indica evidência que vem de outra condição, domínio ou métrica. «Insuficiente» indica que o corpus não tem contraste para a condição. Leia os qualificadores: uma linha pode ser favorável em um estudo e indireta fora dele.'),
        h('p', null, 'Quando a linha é «favorável ao pacote», várias mudanças foram avaliadas em conjunto e o ganho não se atribui a um mecanismo único. Abra uma comparação para ver o que foi acrescentado, qual foi a base e em que modelo, benchmark e métrica os valores foram obtidos. A força descritiva informa quantas comparações e estudos sustentam a linha, sem nota.'),
        h('p', null, 'Benchmarks, métricas e modelos diferem entre os estudos. Por isso o site preserva a ordem da tabela, não ranqueia técnicas, não calcula média e apresenta cada par de valores separadamente. «Melhora» e «piora» descrevem a diferença entre os dois valores de uma comparação, no sentido da métrica; não indicam significância estatística.'),
        h('p', null, `Das ${m.n_comparacoes} comparações, ${m.direcoes.melhora} registram melhora, ${m.direcoes.piora} piora, ${m.direcoes.igual} valores iguais, ${m.direcoes.sem_direcao} não têm direção calculável e ${m.direcoes.descritiva} são descritivas. Essa proporção reflete a escolha das comparações pelos autores dos estudos e o viés de publicação; não estima efeito nem a chance de sucesso no seu projeto.`),
        h('p', null, 'Compilação, aprovação em testes, similaridade textual e alertas de scanner têm alcances diferentes. Resultados de benchmark não demonstram, por si, produtividade, segurança ou redução de custo.'),
      ]],
      ['cobertura', 'Cobertura do Guia e do Explorador', [
        h('p', null, `O Guia tem ${m.n_linhas} linhas de apoio (tabela ${m.tabela_versao}), elaboradas a partir de sínteses de ${m.fichas_nas_sinteses} fichas. O Explorador tem ${m.n_comparacoes} comparações de um corpus de ${m.n_estudos} estudos; ${m.estudos_sem_comparacao} estudos têm ficha e nenhuma comparação extraída.`),
        h('p', null, 'As extrações posteriores às sínteses parciais ampliaram o corpus do Explorador. Elas não foram incorporadas retroativamente às linhas do Guia.'),
        h('p', null, 'A separação das linhas do Guia em aplicáveis, com recurso faltante e lacunas, e o preenchimento dos oito cenários, são decisões editoriais deste site, feitas a partir da coluna de condição da tabela. Os cenários são sintéticos; o exame documentado na monografia usou os cenários com a versão 1 da tabela, e a versão 2 incorpora ajustes posteriores.'),
      ]],
      ['conferencia', 'Conferência humana', [
        h('p', null, `As fichas e as comparações foram extraídas por IA. O autor conferiu uma amostra de ${m.estudos_revisados} estudos`, m.ultima_revisao ? [' (registro de ', dataBR(m.ultima_revisao), ')'] : '', `: em ${mod.formulario || 0}, o julgamento de cada bloco da ficha está gravado em formulário; nos outros ${mod.declaracao_autor || 0}, o autor declarou que todos os blocos estavam corretos, sem gravá-los um a um.`),
        h('p', null, `Com isso, ${m.comparacoes_revisadas} das ${m.n_comparacoes} comparações têm revisão humana confirmada; as demais aparecem como pendentes. Segundo a monografia, houve correções em 18 de 571 blocos da amostra (3,2%), proporção descritiva que não estima a taxa de erro do corpus.`),
        h('p', null, 'Em cada comparação, consulte o estado da revisão e o localizador para encontrar o resultado na fonte. Contagens e direções podem mudar com correções fora da amostra. A conferência da extração, a dos metadados do registro e a revisão por pares do artigo são informações distintas.'),
      ]],
      ['versao', 'Versão e documentos', [
        h('ul', null,
          h('li', null, `Tabela de apoio ${m.tabela_versao} · extração ${m.extracao_versao} · data de corte da busca `, dataBR(m.data_corte)),
          h('li', null, 'Publicação: ', VERSAO && VERSAO.commit ? [`revisão ${String(VERSAO.commit).slice(0, 7)}`, VERSAO.data ? [' de ', dataBR(VERSAO.data)] : ''] : 'cópia local, sem revisão de publicação registrada'),
          h('li', null, h('a', { href: m.repositorio, rel: 'noopener' }, 'Repositório do projeto'), ' (protocolo, dados, decisões e código do site)'),
          h('li', null, m.monografia_url ? h('a', { href: m.monografia_url }, 'Ler a monografia (PDF)') : 'Link público da monografia pendente nesta versão.')),
        h('p', null, 'O site publica dados derivados: valores, localizadores e links para as fontes. Não reproduz trechos dos artigos nem distribui seus arquivos.'),
        h('p', null, 'O design do site foi especificado pelo Codex e a implementação foi feita pelo Claude Code, assistentes de IA, a pedido do autor.'),
      ]],
    ];
    const indice = h('nav', { class: 'painel lateral-fixa indice', 'aria-label': 'Nesta página' },
      recolhivel('Nesta página', h('ul', null, secoes.map(([id, titulo]) => h('li', null, h('a', { href: '#/sobre?sec=' + id }, titulo)))), { aberto: false, classe: 'rc-desktop' }));
    const vista = h('div', null,
      h('h1', { tabindex: '-1' }, 'Sobre a revisão'),
      h('div', { class: 'colunas colunas-sobre' }, indice,
        h('div', { class: 'prosa' }, secoes.map(([id, titulo, corpo]) => h('section', { id: 'sec-' + id, 'aria-labelledby': 'tit-' + id },
          h('h2', { id: 'tit-' + id, tabindex: '-1' }, titulo), corpo)))));
    return { titulo: 'Sobre', vista, foco: () => document.getElementById('tit-' + q.get('sec')) };
  }

  /* ---------- montagem ---------- */
  function renderizar() {
    const r = lerRota();
    const nome = r.partes[0] || 'guia';
    let tela;
    if (nome === 'guia') tela = verGuia(r.q);
    else if (nome === 'explorador') tela = verExplorador(r.q);
    else if (nome === 'estudo' && r.partes[1]) tela = verEstudo(r.partes[1], r.q);
    else if (nome === 'sobre') tela = verSobre(r.q);
    else {
      tela = { titulo: 'Página não encontrada', vista: h('div', null, h('h1', { tabindex: '-1' }, 'Página não encontrada'),
        h('p', null, 'O endereço não corresponde a uma tela deste site.'), h('p', null, h('a', { class: 'botao', href: '#/guia' }, 'Abrir o Guia'))) };
    }
    const area = nome === 'estudo' ? 'explorador' : nome;
    document.querySelectorAll('[data-nav]').forEach((a) => {
      if (a.dataset.nav === area) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
    });
    trocar(main, tela.vista);
    document.title = `${tela.titulo} · Prompt em Código`;
    const alvo = tela.foco && tela.foco();
    if (alvo) focar(alvo);
    else { window.scrollTo(0, 0); if (rotaAnterior !== '') focar(main.querySelector('h1'), false); }
    rotaAnterior = location.hash || '#/guia';
  }

  function preparar(dados) {
    D = dados;
    D.estudos.forEach((s) => { idx.estudo.set(s.id, s); s._busca = norm(`${s.id} ${s.titulo}`); });
    D.comparacoes.forEach((c) => {
      idx.comp.set(c.id, c);
      if (!idx.compsDoEstudo.has(c.estudo)) idx.compsDoEstudo.set(c.estudo, []);
      idx.compsDoEstudo.get(c.estudo).push(c);
      const s = idx.estudo.get(c.estudo);
      c._busca = norm([c.id, c.estudo, s ? s.titulo : '', c.tecnica, c.comparador, c.modelo, c.benchmark, c.metrica].join(' '));
    });
    idx.compsDoEstudo.forEach((lista) => lista.sort((a, b) => parseInt(a.id.split('-C')[1], 10) - parseInt(b.id.split('-C')[1], 10)));
    D.estudos.sort((a, b) => numEstudo(a.id) - numEstudo(b.id));
    D.linhas.forEach((l) => idx.linha.set(l.id, l));
    D.cenarios.forEach((c) => idx.cenario.set(c.id, c));
    const m = D.meta;
    document.getElementById('procedencia').textContent = `Extração por IA. O autor conferiu uma amostra de ${m.estudos_revisados} estudos.`;
    const corte = dataBR(m.data_corte);
    document.getElementById('rodape-versao').replaceChildren(`Tabela ${m.tabela_versao} · Extração ${m.extracao_versao} · Corte `, corte);
  }

  function falha(erro) {
    const arquivo = h('input', { type: 'file', accept: 'application/json,.json', onchange: () => {
      const f = arquivo.files[0];
      if (f) f.text().then((t) => iniciar(JSON.parse(t))).catch(falha);
    } });
    trocar(main, h('div', { role: 'alert' },
      h('h1', null, 'Não foi possível carregar os dados desta versão.'),
      h('p', { class: 'secundario' }, String(erro && erro.message ? erro.message : erro)),
      h('p', null, h('button', { type: 'button', class: 'botao botao-acao', onclick: carregar }, 'Tentar novamente')),
      location.protocol === 'file:' ? h('label', { class: 'campo' }, h('span', null, 'Abrir dados.json deste site'), arquivo) : null));
  }
  function iniciar(dados) {
    if (!dados || !dados.meta || !Array.isArray(dados.linhas) || !Array.isArray(dados.comparacoes) || !Array.isArray(dados.estudos) || !Array.isArray(dados.cenarios)) {
      throw new Error('dados.json não tem as coleções esperadas (meta, linhas, cenarios, comparacoes, estudos).');
    }
    preparar(dados);
    renderizar();
  }
  function carregar() {
    trocar(main, h('p', { role: 'status' }, 'Carregando os dados da revisão…'));
    fetch('versao.json').then((r) => (r.ok ? r.json() : null)).catch(() => null).then((v) => { VERSAO = v; })
      .then(() => fetch('dados.json'))
      .then((r) => { if (!r.ok) throw new Error('dados.json: resposta ' + r.status); return r.json(); })
      .then(iniciar).catch(falha);
  }

  /* ---------- tema e eventos globais ---------- */
  const seletorTema = document.getElementById('tema');
  const midiaEscura = window.matchMedia('(prefers-color-scheme: dark)');
  function preferenciaTema() { try { return localStorage.getItem('tema') || 'sistema'; } catch (e) { return 'sistema'; } }
  function aplicarTema(p) {
    const escuro = p === 'escuro' || (p !== 'claro' && midiaEscura.matches);
    document.documentElement.setAttribute('data-tema', escuro ? 'escuro' : 'claro');
  }
  seletorTema.value = preferenciaTema();
  seletorTema.addEventListener('change', () => {
    try { localStorage.setItem('tema', seletorTema.value); } catch (e) { /* preferência não guardada */ }
    aplicarTema(seletorTema.value);
  });
  midiaEscura.addEventListener('change', () => aplicarTema(preferenciaTema()));

  document.getElementById('pular').addEventListener('click', (ev) => { ev.preventDefault(); focar(main.querySelector('h1') || main); });
  window.addEventListener('hashchange', () => { navegouAqui = true; if (D) renderizar(); });
  carregar();
})();
