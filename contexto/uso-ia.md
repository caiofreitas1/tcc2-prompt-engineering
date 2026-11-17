# Registro de assistência por IA

Cada atividade deve registrar data, ferramenta, modelo quando exposto, entrada,
saída, verificação e responsável. Não inferir modelo a partir do estilo do texto.
Dados ausentes devem ser explicitados. Não registrar raciocínio interno do modelo.

| Data | Atividade | Ferramenta/modelo | Verificação | Revisão humana |
|---|---|---|---|---|
| 2026-10-25 | Preparação da estrutura, skills e tarefas | ChatGPT Work; modelo não informado ao fluxo | Ver contexto/entrega.md | Pendente |

Elaborar o relato de uso de IA na metodologia com o orientador. Revisões por agentes
não equivalem a revisores humanos independentes ou a concordância entre avaliadores.

## T02 — 26/10/2026

- Executor: Codex (IA); ambiente identifica GPT-6, sem expor a variante específica.
- Entradas: instruções do projeto, protocolo confirmado, issue #2, linha S1 do
  piloto, registro arXiv e texto primário completo arXiv:2303.06689v5.
- Ferramentas: navegação web e download HTTPS, Python (`pypdf` para extração,
  `pypdfium2` para renderização), inspeção visual das páginas e tabelas relevantes,
  `decimal` para recálculo e Git para preparar a revisão.
- Saídas: fichamento `evidencias/S1.md`, registro S1 atualizado, extrações E1–E2,
  afirmações A1–A5 em rascunho, referência arXiv e recuperação da fonte com hash.
- Verificação: confronto com Table 1 (p. 7), método nas pp. 3–7, orçamento em
  Table 4 (p. 10), ameaças na p. 15 e métricas no Apêndice C (pp. 21–22);
  valores reportados separados de derivados e de inferências. Resultado de
  `make check`: zero erros estruturais e dez testes aprovados após corrigir o
  isolamento dos dados sintéticos nos testes (D18). `git diff --check`, vínculos,
  hash e cálculos decimais conferidos; download exercitado em diretório temporário.
- Revisão humana: pendente. Não foram executados experimentos com LLMs, código
  do artigo ou testes do benchmark. A avaliação humana relatada pelos autores do
  artigo não é revisão deste trabalho. Não houve atuação de segundo revisor humano.

## T03 — 27/10/2026

- Executor: Codex (IA); ambiente identifica GPT-6, sem expor a variante específica.
- Entrada: decisão do autor de usar IEEE Conference Template; orientações do
  repositório, issue #3, esqueleto existente e fontes IEEE/CTAN.
- Saída: adoção de IEEEtran/conference em `monografia/main.tex`, ajustes editoriais
  nos arquivos de introdução/metodologia, proveniência em `monografia/TEMPLATE.md`
  e registros de situação/decisões. Não houve produção de resultados científicos.
- Verificação: compilação por `make pdf` e inspeção da página completa renderizada
  por Poppler; título, autoria, português, colunas e seções conferidos. Diagnósticos
  e resultado de `make check` relatados no registro de T03 e no PR.
- Revisão humana: pendente. Na primeira preparação, orientador e elementos
  institucionais adicionais ainda não estavam confirmados. Não se certificou
  homologação pelo curso nem submissão a evento IEEE.
- Resultado final de T03: `make check` com zero erros e dez testes aprovados;
  `make pdf` com uma página A4, log sem avisos/overfull/underfull, metadados e
  quatro fontes Type 1 incorporadas. Página final inteira inspecionada visualmente.
  `make release-check` falhou com 17 bloqueios esperados, discriminados no registro
  do template; não se contornaram as barreiras de entrega.

### Complemento de T03 — orientador

Em 27/10/2026, o autor indicou o perfil institucional de seu orientador no DCC/UFMG.
Codex conferiu o nome Eduardo Magno Lages Figueiredo na página e atualizou o
registro de origem e a identificação em nota de orientação no documento IEEE.
A informação não representa revisão humana do trabalho nem aprovação do docente.
A pergunta sobre elementos institucionais adicionais permanece sem resposta.
Em seguida, o autor confirmou «Somente o artigo IEEE» para os elementos da entrega.
A pendência de elementos adicionais foi resolvida e a flag de template foi
atualizada com origem nessa declaração. O orientador permanece em nota de
orientação; não se atribuiu a ele coautoria, aceite ou revisão já executada.

Verificação após os complementos: `make check` com zero erros e dez testes
aprovados; `make pdf` recompilado, nota de orientação e página inteira inspecionadas,
sem avisos no log. `make release-check` registra 16 bloqueios após a confirmação
da flag do template, preservando as barreiras acadêmicas restantes.

## Protocolo v2 — 27/10/2026

- Executor: Claude Code (Claude Opus 5.5), em sessão com o autor.
- Entradas: repositório na main `81a09e7`, respostas do autor no chat (D25–D27),
  API do arXiv (títulos/resumos de S1–S6 e contagens), Crossref (metadados das
  referências do método) e páginas da ACM sobre o acesso aberto à Digital Library.
- Saídas: `protocolo/protocolo.md` v2, `protocolo/prompts/`, D25–D31, contrato de
  dados v2 (`registros.csv`, `acesso_aberto`, `prompt_versao`, contrato 2 de
  extração), regras novas em `scripts/verificar.py` com sete testes novos, sete
  referências metodológicas no .bib e ajuste de T04–T07 no backlog.
- Verificação: `make check` (zero erros estruturais, 17 testes aprovados);
  calibração da expressão em S1–S6 por script local; DOIs conferidos no Crossref.
- Revisão humana: pendente (revisão do PR pelo autor). Contagens do arXiv são
  sondagens informais, não buscas registradas.

## T04 — buscas, auditoria e correções — 29/10/2026

- Executores: Claude Code (Claude Opus 5.5) nas buscas, na deduplicação e nas
  correções; Codex (IA) na auditoria independente do PR #20.
- Entradas: protocolo v2, API do arXiv, IEEE Xplore (navegador do app), ACM DL (Chrome
  do autor via Claude in Chrome), APIs do OpenAlex, Crossref e Semantic Scholar.
- Saídas: buscas B1–B3, `dados/registros.csv`, candidatos em `dados/estudos.csv`,
  `dados/resumos.csv`, `dados/versoes_abertas.csv`, `dados/deduplicacao.csv`,
  contagens em `dados/fluxos.csv`, scripts de busca e deduplicação, D33–D38,
  relatório de auditoria em `evidencias/auditorias/`.
- Verificação: `make check` (zero erros estruturais, 22 testes aprovados); auditoria
  por IA com parecer "seguir após correções", achados tratados em D37.
- Revisão humana: pendente (ponto de controle da seção 7 após a busca).

## T04 — verificação complementar da ACM — 01/11/2026

- Executor: Claude Code (Claude Opus 5.5), a pedido do autor (D39).
- Entradas: busca B3 de 29/10, ACM DL (Chrome do autor via Claude in Chrome, sem login).
- Saídas: coleta em `dados/brutos/acm-verificacao-2026-11-01/`, `scripts/verificar_acm.py`,
  `dados/correcoes_registros.csv`, regra de correções em `scripts/deduplicar.py` e
  `scripts/verificar.py`, recontagens em `dados/fluxos.csv`, D39–D41, ajuste do rascunho
  tr-v1 e relatório em `evidencias/verificacoes/T04-acm-2026-11-01.md`.
- Verificação: `make check`; reextração em Python do HTML bruto comparada à extração
  do navegador; deduplicação reexecutada duas vezes sem alteração.
- Revisão humana: pendente (revisão do autor; a triagem não foi liberada).

## T05 — lote piloto — 01/11/2026

- Executores: Claude Code (Claude Opus 5.5) como IA-A, no sorteio e no formulário do
  autor; Claude Sonnet 5.5 como IA-B, em subagente separado.
- Entradas: `dados/estudos.csv`, `dados/resumos.csv`, prompt tr-v1.
- Saídas: `scripts/amostrar_piloto.py`, `evidencias/piloto/amostra-1.csv`, decisões de
  IA-A e IA-B seladas (SHA-256 em D43), artefato privado para a triagem cega do autor.
- Revisão humana: em andamento (triagem independente do autor).

## T05 — guia de triagem e auditoria — 01–02/11/2026

- Executores: Claude Code (Claude Opus 5.5) no guia e nas correções; Codex (IA) na
  auditoria do guia, a pedido do autor.
- Entradas: protocolo (seções 3, 6–8), prompt tr-v1, D41–D43.
- Saídas: guia em Claude Docs (https://claude.ai/artifact/4TVMdTnmvSDoW7dbL83D6b),
  `evidencias/auditorias/T05-guia-triagem-2026-11-02.md`, D44.
- Revisão humana: codificação do κ confirmada pelo autor em 02/11/2026 (D45); triagem
  independente do autor pendente.

## T05 — análise do lote piloto — 02/11/2026

- Executor: Claude Code (Claude Opus 5.5).
- Atividade: abertura dos selos, cálculo de revocação e κ (`scripts/analisar_piloto.py`),
  leitura das perdas, projeção de horas e propostas de recuo e tr-v2.
- Evidências: `evidencias/piloto-triagem.md`, `evidencias/piloto/`, D46.
- Revisão humana: decisões da amostra feitas pelo autor (02/11/2026); análise e
  propostas ainda não revisadas por ele.

## T05 — amostra 2 do piloto — 02/11/2026

- Executores: IA-A (claude-opus-5-5) e IA-B (claude-sonnet-5-5), em subagentes; Claude
  Code (Claude Opus 5.5) na preparação de tr-v2, do sorteio e do formulário.
- Evidências: `protocolo/prompts/triagem-titulo-resumo-v2.md`,
  `evidencias/piloto/amostra-2.csv`, D47–D49.
- Revisão humana: tr-v2 segue a decisão do autor (D47); triagem cega dele pendente.

## T05 — análise da amostra 2 — 02/11/2026

- Executor: Claude Code (Claude Opus 5.5).
- Atividade: abertura dos selos, cálculo de revocação e κ, extrapolação de volume.
- Evidências: `evidencias/piloto-triagem.md`, `evidencias/piloto/`, D50.
- Revisão humana: decisões da amostra feitas pelo autor (02/11/2026); análise ainda não
  revisada por ele.

## T05 — preparação da medição de texto completo — 02/11/2026

- Executores: IA-A (claude-opus-5-5) e IA-B (claude-sonnet-5-5), em subagentes, com tc-v1;
  Claude Code (Claude Opus 5.5) no sorteio, na obtenção dos PDFs e no formulário.
- Evidências: `evidencias/piloto/medicao-texto.csv`, D51.
- Revisão humana: conferência cega do autor pendente.

## T05 — análise da medição de texto completo — 02/11/2026

- Executor: Claude Code (Claude Opus 5.5).
- Atividade: abertura dos selos, comparação das decisões, verificação do tempo e projeção.
- Evidências: `evidencias/piloto-triagem.md`, `evidencias/piloto/autor-medicao.jsonl`, D52.
- Revisão humana: conferência feita pelo autor em 02/11/2026, com tempo a confirmar; análise
  ainda não revisada por ele.

## T05 — teste de custo da leitura por texto — 02/11/2026

- Executores: IA-A (claude-opus-5-5) e IA-B (claude-sonnet-5-5), em subagentes, com tc-v1; Claude Code
  (Claude Opus 5.5) na extração com Ghostscript e na comparação.
- Evidências: `evidencias/piloto/ia-a-tc-v1-texto.jsonl`, `evidencias/piloto/ia-b-tc-v1-texto.jsonl`, D55.
- Revisão humana: não houve; aguarda o autor.

## T10 — rascunho de introdução, fundamentação e metodologia — 02/11/2026

- Executor: Claude Code (Claude Opus 5.5).
- Atividade: redação de rascunho em `monografia/capitulos/01` a `03`, com metadados conferidos na API do
  arXiv e no Crossref. Fontes da fundamentação lidas pelo resumo (exceto Brown et al., seção 1.1, e S1).
- Afirmações empíricas de estudos: nenhuma nova; os números da metodologia vêm dos registros do projeto.
- Revisão humana: pendente.

## T10 — análise da auditoria e correções do esboço — 03/11/2026

- Executores: Codex (IA), auditoria; Claude Code (Claude Opus 5.5), reconferência e correções.
- Atividade: correções em `monografia/capitulos/01`, `02`, `03` e `05`, novo apêndice `07-apendice-busca.tex` e
  quatro referências (S3–S6), com metadados na API do arXiv e na DataCite.
- Evidências: `evidencias/auditorias/T10-esboco-PDF-2026-11-03.md`, D56–D58.
- Revisão humana: pendente.

## T05/T10 — tc-v2 e reexame de casos — 03/11/2026

- Executores: Claude Code (Claude Opus 5.5), tc-v2 e alterações no texto; IA-A (claude-opus-5-5) e IA-B (claude-sonnet-5-5), em
  subagentes novos, no reexame de quatro casos; Codex (IA), reavaliação do esboço.
- Evidências: D59, D60, `evidencias/piloto/ia-a-tc-v2-reexame.jsonl`, `evidencias/piloto/ia-b-tc-v2-reexame.jsonl`.
- Revisão humana: o autor aprovou as propostas de D58; não revisou tc-v2 nem o reexame.

## T05 — triagem de título e resumo do lote — 03/11/2026

- Executores: IA-A (claude-opus-5-5) e IA-B (claude-sonnet-5-5), em subagentes novos, com tr-v2; Claude Code (Claude Opus 5.5) na montagem,
  validação e resumo.
- Evidências: `evidencias/lote/lista.csv`, `evidencias/piloto-triagem.md`, D65.
- Revisão humana: conferência das exclusões pendente.

## T05 — conferência das exclusões e importação — 05/11/2026

- Executores: autor (conferência de 85 fichas, sem IA); Claude Code (Claude Opus 5.5) na abertura dos selos, importação e contagens.
- Evidências: `evidencias/lote/autor-conferencia.jsonl`, `dados/triagem.csv`, `evidencias/lote/texto-completo.csv`, D67.
- Revisão humana: a conferência é do autor; a importação não foi revisada por ele.

## T06 — conferência cega do texto completo e importação — 08/11/2026

- Executores: autor (conferência cega de 230 estudos, sem consultar IA sobre eles); Claude Code (Claude Opus 5.5) na abertura dos selos,
  importação, contagens e correção do sorteio de `scripts/montar_conferencia_tc.py`.
- Evidências: `evidencias/lote/autor-texto-completo.jsonl`, `dados/triagem.csv`, `dados/estudos.csv`, D78.
- Revisão humana: a conferência é do autor; a importação e as contagens não foram revisadas por ele.

## T10 — metodologia executada e resultados preliminares — 08/11/2026

- Executor: Claude Code (Claude Opus 5.5), redação, contagens e compilação.
- Evidências: `monografia/capitulos/03-metodologia.tex`, `monografia/capitulos/04-resultados.tex`, `dados/fluxos.csv`, D82.
- Revisão humana: pendente; o autor ainda não leu o texto.

## T10 — resumo, ameaças à validade e conclusão parcial (08/11/2026)

- Pedido do autor: redigir o resumo, as ameaças à validade e a conclusão parcial para o texto de 08/11 («Faz sentido»).
- Executor: Claude Code (Claude Opus 5.5), redação a partir dos números já registrados na metodologia, nos resultados e em `dados/fluxos.csv`; compilação e inspeção das páginas 1, 7 e 8.
- Evidências: `monografia/main.tex` (resumo), `monografia/capitulos/05-discussao.tex`, `monografia/capitulos/06-conclusao.tex`. Nenhuma afirmação sobre resultados dos estudos primários; apenas contagens do processo.
- Revisão humana: pendente; o autor ainda não leu o texto.

## T10 — ajustes de revisão do texto inicial (08/11/2026)

- Pedido do autor: analisar seis pontos de revisão e aplicar cinco («Sim, aplicar»), D89.
- Executor: Claude Code (Claude Opus 5.5), conferência dos pontos em `contexto/decisoes.md` (D55, D64, D66, D67, D80, D81, D83), em `dados/triagem.csv` e nas amostras de calibração; redação em `monografia/main.tex` e nos capítulos 03, 04 e 06.
- Revisão humana: pendente; o autor ainda não leu as novas passagens.

## T10 — formulação do limite de X4 (08/11/2026)

- Pedido do autor: adotar a formulação proposta para o limite de X4 («Usar sua proposta»), D90.
- Executor: Claude Code (Claude Opus 5.5), formulação a partir dos motivos do autor em D80 e D81 e redação em `monografia/capitulos/03-metodologia.tex` e `05-discussao.tex`.
- Revisão humana: o autor aprovou a formulação; a releitura de S314 e S373 continua pendente.

## T10 — segunda rodada de ajustes de revisão (08/11/2026)

- Pedido do autor: avaliar cinco pontos de revisão e aplicar quatro («Sim, aplicar»), D91.
- Executor: Claude Code (Claude Opus 5.5), recálculo do κ com as decisões anteriores às revisões de S314 e S373 e redação em `monografia/main.tex` e nos capítulos 03, 04 e 05.
- Revisão humana: pendente; o autor ainda não leu as novas passagens.

## T06 — nona leva do texto completo (08/11/2026)

- Pedido do autor: começar os próximos passos depois do envio do texto inicial (D92).
- Executores: IA-A (Claude Opus 5.5) e IA-B (Claude Sonnet 5.5), em subagentes, com tc-v2; Claude Code (Claude Opus 5.5) na montagem dos grupos, no selo, na escolha dos estudos para o autor e no formulário.
- Revisão humana: pendente; o autor confere os 63 estudos no formulário cego.

## T06 — décima leva do texto completo, etapa 3 (08/11/2026)

- Pedido do autor: «Pode ler os 64 agora» (D95).
- Executores: IA-A (Claude Opus 5.5) e IA-B (Claude Sonnet 5.5), em subagentes, com tc-v2; Claude Code (Claude Opus 5.5) no registro dos PDFs, nos grupos, no selo e no formulário.
- Revisão humana: pendente; o autor confere os 64 estudos no formulário cego.

## T07 — ficha de extração e piloto (10/11/2026)

- Pedido do autor: registrar a proposta de extração revista («Sim, registrar»), D97.
- Executores: Claude Code (Claude Opus 5.5), proposta, prompt ex-v2, atualização do protocolo e sorteio do piloto; Codex (IA), dois pareceres de auditoria sobre a proposta.
- Revisão humana: o autor aprovou a proposta; as fichas do piloto ainda não existem.

## T07 — piloto da extração (11/11/2026)

- Agendado em D97; executado por Claude Code (Claude Opus 5.5): metadados e I4 por API, extração ex-v2 em 10 subagentes Opus, verificação das citações e formulário de conferência (D98).
- Revisão humana: pendente; o autor confere as 10 fichas inteiras no formulário.

## T06 — última leva do texto completo, etapa 3 (11/11/2026)

- Agendada em D95/D96 e executada por Claude Code (Claude Opus 5.5): grupos g97–g105, selo e formulário (D100).
- Executores da leitura: IA-A (Claude Opus 5.5) e IA-B (Claude Sonnet 5.5), em subagentes, com tc-v2.
- Revisão humana: pendente; o autor confere os 36 estudos (nº 384–419) no formulário cego.

## T07 — calibração da ficha de extração (13/11/2026)

- Pedido do autor: «Terminei a conferência do piloto» e respostas sobre agregado, leitura do PDF e qualidade (D101).
- Executores: Claude Code (Claude Opus 5.5), análise das correções, prompt ex-v2.1, imagens das páginas e comparação; subagentes Claude Opus 5.5 na reaplicação (23 extrações em três rodadas).
- Revisão humana: conferência do autor das 10 fichas ex-v2 (13/11/2026); as fichas ex-v2.1 ainda não foram conferidas pelo autor.
- Formulário de conferência das fichas ex-v2.1 publicado em 13/11/2026 (`evidencias/piloto/formulario-ex-v2.1.html`, coleção `extracao_v21_autor`), com as correções anteriores do autor por estudo; verificação aproximada das citações por `scripts/verificar_citacoes_piloto.py` (60 de 242 não achadas no texto extraído, a conferir no PDF).

## T07 — segunda calibração da ficha de extração (14/11/2026)
- Pedido do autor: «Feito», com as propostas P1–P10 e a indicação de não considerar o novo documento do Codex (13/11/2026); reaplicação agendada pelo agente para depois da renovação da janela de 5 horas (D102).
- Executores: Claude Code (Claude Opus 5.5), importação da conferência, prompt ex-v2.2, validador de rótulos, comparação com as notas do autor e correções manuais registradas; subagentes Claude Opus 5.5 limitados a Read e Write, 15 extrações em duas rodadas (14/11/2026).
- Revisão humana: conferência do autor das 10 fichas ex-v2.1 (13/11/2026). As fichas ex-v2.2 não foram conferidas pelo autor. O autor confirmou a correção S570 `outro` → `instrucao` e os esclarecimentos da rodada 2 (14/11/2026).
- Verificação: `scripts/validar_ficha_extracao.py` sem erros nas 10 fichas finais; verificação aproximada das citações (62 de 253 não achadas no texto extraído, a conferir no PDF).


## T07 — extração em escala, lote 1 (15/11/2026)
- Pedido do autor: «Seguir com Opus» (14/11/2026); confirmação da regra de `contexto` (D103).
- Executores: subagentes Claude Opus 5.5 limitados a Read e Write, 15 extrações (S1–S129); Claude Code (Claude Opus 5.5), validação, 6 correções manuais registradas e relatório (`evidencias/extracao-v2.2/lote-01.md`).
- Revisão humana: nenhuma ficha do lote conferida pelo autor.

## T07 — extração em escala, lote 2 (15/11/2026)
- Pedido do autor: «Pode começar, assim que o limite semanal acabar, eu reseto ele» (15/11/2026).
- Executores: subagentes Claude Opus 5.5 limitados a Read e Write, 15 extrações (S137–S261); Claude Code (Claude Opus 5.5), validação, 2 correções manuais registradas e relatório (`evidencias/extracao-v2.2/lote-02.md`).
- Revisão humana: nenhuma ficha do lote conferida pelo autor.

## T07 — extração em escala, lote 3 (16/11/2026)
- Executores: subagentes Claude Opus 5.5 limitados a Read e Write, 15 extrações (S271–S323); Claude Code (Claude Opus 5.5), validação e relatório (`evidencias/extracao-v2.2/lote-03.md`).
- Revisão humana: nenhuma ficha do lote conferida pelo autor.

## T07 — calibração do Codex no piloto (16/11/2026)
- Pedido do autor: paralelizar a extração com a assinatura do Codex; «Instalei o codex cli» (16/11/2026).
- Executores: Codex CLI 0.169.0 (gpt-6.1-sol, esforço high), 10 extrações ex-v2.2 dos estudos do piloto; Claude Code (Claude Opus 5.5), roteiro de execução, comparação com as fichas finais e relatório (`evidencias/piloto/calibracao-codex.md`).
- Revisão humana: nenhuma; a adoção do Codex como segundo extrator aguarda decisão do autor.

## T07 — extração em escala, lote 4 e lote C1 (16/11/2026)
- Pedido do autor: «Sim, adotar» o Codex como segundo extrator (D104).
- Executores: subagentes Claude Opus 5.5 (Read e Write), 12 extrações (S325–S365); Codex CLI 0.169.0 (gpt-6.1-sol, esforço high), 10 extrações gravadas de 15 lançadas (S2233–S2131; 5 interrompidas pelo limite da assinatura); Claude Code (Claude Opus 5.5), roteiro, validação e relatório (`evidencias/extracao-v2.2/lote-04.md`).
- Revisão humana: nenhuma ficha do lote conferida pelo autor.

## T07 — extração em escala, lote 5 (16/11/2026)
- Executores: subagentes Claude Opus 5.5 limitados a Read e Write, 20 extrações (S383–S399 e S397–S479); Claude Code (Claude Opus 5.5), validação, 3 correções manuais registradas e relatórios (`lote-04.md`, `lote-05.md`).
- Revisão humana: nenhuma ficha do lote conferida pelo autor.

## T07 — extração em escala, lote 6 (16/11/2026)
- Executores: subagentes Claude Opus 5.5 limitados a Read e Write, 15 extrações (S491–S569); Claude Code (Claude Opus 5.5), retomada agendada a pedido do autor, validação, 1 correção manual registrada e relatório (`evidencias/extracao-v2.2/lote-06.md`).
- Revisão humana: nenhuma ficha do lote conferida pelo autor.

## T07 — extração em escala, lotes C2 e C3 (16/11/2026)
- Executores: Codex CLI 0.169.0 (gpt-6.1-sol, esforço high), 16 extrações (S2170–S2086); Claude Code (Claude Opus 5.5), roteiro, validação e relatório (`evidencias/extracao-v2.2/lote-C2-C3.md`).
- Revisão humana: nenhuma ficha do lote conferida pelo autor.

## T07 — extração em escala, lote 7 (16/11/2026)
- Executores: subagentes Claude Opus 5.5 limitados a Read e Write, 20 execuções (S579–S682), 18 fichas finais; Claude Code (Claude Opus 5.5), validação e relatório (`evidencias/extracao-v2.2/lote-07.md`).
- S667: gravação interrompida por classificador de segurança, sem nova tentativa.
- Revisão humana: nenhuma ficha do lote conferida pelo autor.

## T07 — extração em escala, lote 8 (16/11/2026)
- Executores: subagentes Claude Opus 5.5 limitados a Read e Write, 20 extrações (S692–S810); Claude Code (Claude Opus 5.5), validação, 5 correções manuais registradas e relatório (`evidencias/extracao-v2.2/lote-08.md`).
- Revisão humana: nenhuma ficha do lote conferida pelo autor.

## T07 — extração em escala, lote 9 (16/11/2026)
- Executores: subagentes Claude Opus 5.5 limitados a Read e Write, 20 extrações (S821–S979), 19 fichas finais; Claude Code (Claude Opus 5.5), validação e relatório (`evidencias/extracao-v2.2/lote-09.md`).
- Revisão humana: nenhuma ficha do lote conferida pelo autor.

## T07 — extração em escala, lote 10 (16/11/2026)
- Executores: subagentes Claude Opus 5.5 limitados a Read e Write, 20 extrações (S996–S1133); Claude Code (Claude Opus 5.5), validação e relatório (`evidencias/extracao-v2.2/lote-10.md`).
- Revisão humana: nenhuma ficha do lote conferida pelo autor.

## T07 — extração em escala, lote 11 (16/11/2026)
- Executores: subagentes Claude Opus 5.5 limitados a Read e Write, 20 extrações (S1141–S1503), 19 fichas finais; Claude Code (Claude Opus 5.5), validação, 3 correções manuais registradas e relatório (`evidencias/extracao-v2.2/lote-11.md`).
- Revisão humana: nenhuma ficha do lote conferida pelo autor.

## T07 — extração em escala, lote 12 (16/11/2026)
- Executores: subagentes Claude Opus 5.5 limitados a Read e Write, 20 extrações (S1556–S1653); Claude Code (Claude Opus 5.5), validação e relatório (`evidencias/extracao-v2.2/lote-12.md`).
- Revisão humana: nenhuma ficha do lote conferida pelo autor.

## T07 — extração em escala, lote 13 (16/11/2026)
- Executores: subagentes Claude Opus 5.5 limitados a Read e Write, 20 extrações (S1666–S1747), 19 fichas finais; Claude Code (Claude Opus 5.5), validação e relatório (`evidencias/extracao-v2.2/lote-13.md`).
- Revisão humana: nenhuma ficha do lote conferida pelo autor.

## T07 — extração em escala, lote 14 (16/11/2026)
- Executores: subagentes Claude Opus 5.5 limitados a Read e Write, 18 extrações (S1763–S1898); Claude Code (Claude Opus 5.5), validação e relatório (`evidencias/extracao-v2.2/lote-14.md`).
- Revisão humana: nenhuma ficha do lote conferida pelo autor.

## T07 — extração em escala, lote 15 (16/11/2026)
- Executores: subagentes Claude Opus 5.5 limitados a Read e Write, 15 extrações (S1924–S2057); Claude Code (Claude Opus 5.5), validação, 4 correções manuais registradas e relatório (`evidencias/extracao-v2.2/lote-15.md`).
- Revisão humana: nenhuma ficha do lote conferida pelo autor.

## T07 — extração em escala, lote 16 (16/11/2026)
- Executores: subagentes Claude Opus 5.5 limitados a Read e Write, 4 extrações (S2059–S2085), 3 fichas finais; Claude Code (Claude Opus 5.5), validação e relatório (`evidencias/extracao-v2.2/lote-16.md`, com a situação do corpus ao fim da extração).
- Revisão humana: nenhuma ficha do lote conferida pelo autor.

## T07 — D106: contrato, fichas retidas e reexame de elegibilidade (16/11/2026)
- Executores: Claude Code (Claude Opus 5.5), ampliação do contrato, validadores e testes, 7 correções manuais registradas em 5 fichas e situação da extração (`evidencias/extracao-v2.2/situacao-2026-11-16.md`); subagentes Claude Opus 5.5 limitados a Read e Write, reexame de elegibilidade de 8 estudos nos textos primários (`evidencias/extracao-v2.2/reexame-elegibilidade-2026-11-16.md`).
- Encaminhamentos decididos pelo autor (D106), depois de parecer do Codex trazido por ele. O reexame é recomendação de IA; a inclusão fica para adjudicação do autor.
- Revisão humana: o autor confirmou as correções de S724, S810, S1415 e S1977 como consistência de registros, sem conferência integral das fichas.

## T07 — D107: adjudicação, confirmações e contrafactuais dos comparadores (17/11/2026)
- Executores: Claude Code (Claude Opus 5.5), registro da adjudicação do autor, recálculo dos fluxos, verificação dos 82 trechos do reexame e reavaliação dos contrafactuais de S6, S216, S724, S1415 e S1977 com conferência nas imagens das páginas (`evidencias/extracao-v2.2/contrafactuais-comparadores-2026-11-17.md`).
- Revisão humana: adjudicação de inclusão e confirmação das correções de S62, S479 e S552 pelo autor; a reavaliação dos contrafactuais é proposta, sem alteração das fichas.

## T07 — D108: contrafactual dos comparadores (17/11/2026)
- Executores: Claude Code (Claude Opus 5.5), aplicação em S6, S216, S724, S1415 e S1977 e das propostas validadas; subagentes Claude Opus 5.5 limitados a Read e Write, revisão dirigida de 431 comparadores em 113 estudos, com conferência das tabelas nas imagens (`evidencias/extracao-v2.2/d108-revisao-comparadores.md`).
- Regra decidida pelo autor («Sim, aplicar»); aplicação de IA, não conferida pelo autor.

## T07 — D109: preparação da conferência humana (17/11/2026)
- Executor: Claude Code (Claude Opus 5.5). Sorteio da amostra de 61 estudos (`scripts/sortear_conferencia.py`, semente 20261117) e geração e publicação do formulário (`scripts/gerar_formulario_conferencia.py`, artifact privado com a coleção `extracao_v22_autor`), em `evidencias/extracao-v2.2/conferencia/`.
- A verificação aproximada das citações (`scripts/verificar_citacoes_aprox.py`) só orienta a leitura; a conferência é do autor no PDF e ainda não começou.

## T08–T11 — síntese e redação da versão da banca (17/11/2026, D110)
- Executores: Claude Code (Claude Opus 5.5), com importação das fichas (`scripts/importar_fichas.py`), contagens por script (`scripts/sintetizar.py`, `evidencias/sinteses/`), integração e revisão do texto; 13 subagentes Claude Opus 5.5 (Read e Write) redigiram sínteses parciais sobre extratos das fichas, e 5 subagentes redigiram as subseções de resultados em LaTeX a partir delas.
- Checagem automática: todos os IDs de comparação e de estudo citados existem; as frases não foram conferidas no original. Correções de Claude Code nas subseções: contagens de contrafactual por script, retirada de referências às partes internas da síntese e da tabela de mecanismos duplicada.
- As 97 afirmações novas (A6–A102) entram em `dados/afirmacoes.csv` como rascunho, sem revisor. Nada aqui é revisão humana.
- Cenários v1 (`evidencias/sinteses/cenarios-v1.md`) e tabela de apoio v1 (`evidencias/sinteses/tabela-apoio-v1.csv`) aguardam o autor.

## T09 — cenários e exame (17/11/2026, D111)
- Executor: Claude Code (Claude Opus 5.5). Ajuste dos cenários para a v2 a pedido do autor, congelamento com SHA-256, exame da tabela de apoio v1 com conferência dos estudos nas fichas e proposta de julgamento; formulário publicado (`scripts/gerar_formulario_exame.py`).
- Julgamento final pendente do autor; as propostas não são revisão humana.

## T07 — extração de S1610 e S1617 (17/11/2026, D113)
- Executores: subagentes Claude Opus 5.5 (Read e Write), ex-v2.2 congelada, imagens a 110 dpi; validador sem erros; fichas finais idênticas às saídas brutas; manifesto acrescido. Claude Code reimportou as fichas, recalculou as contagens e atualizou o texto e as afirmações A103 e A104 (rascunho).

## T06–T07 — última leva da etapa 3 e extração dos 29 estudos (17/11/2026, D114)
- Executores: Claude Code (Claude Opus 5.5), conferência dos selos de D100, importação das 36 decisões cegas do autor e dos selos das IAs (`scripts/importar_texto_completo.py`), recomendação sobre S1778 (aceita pelo autor), consulta de datas na Crossref, complemento da amostra (`scripts/sortear_conferencia.py --complemento`), republicação do formulário de conferência, reimportação, contagens e atualização do texto; 29 subagentes Claude Opus 5.5 (Read e Write), um por estudo, com a ex-v2.2 congelada e imagens a 110 dpi.
- A recomendação inicial sobre S1778 dizia que o modelo do COM não era identificado; o extrator achou os modelos na Fig. 2. O motivo registrado foi corrigido antes do commit, e a decisão do autor não muda.
- Validador sem erros nas 29 saídas brutas; uma correção de unidade em S1883 (registro em `correcoes-manuais.jsonl`, confirmação do autor pendente). Afirmações A105–A117 em rascunho; A45 e A46 atualizadas. Nada aqui é revisão humana.

## T07 — extração de S667 pelo Codex e parecer de elegibilidade (17/11/2026)
- A pedido do autor («Delegue a extração para o Codex»), S667 foi extraído pelo Codex CLI 0.169.0 (gpt-6.1-sol, esforço high fixado na chamada, porque a configuração local estava em xhigh), com o mesmo prompt operacional das 26 fichas anteriores do Codex e uma instrução a mais: citar só o necessário, sem reproduzir prompts maliciosos completos, porque o estudo trata de jailbreak. Saída bruta validada sem erro; ficha final idêntica à bruta; manifesto acrescido.
- Claude Code (Claude Opus 5.5) leu S1721, S1929, S1886, S433 e S2053 no texto extraído e nas imagens das páginas e redigiu `evidencias/lote/parecer-elegibilidade-2026-11-17.md`, com recomendações. A decisão é do autor e ainda não foi tomada.
- D115: o autor aceitou todas as recomendações do parecer («Sim, seguir todas»). Claude Code registrou as decisões, reimportou, repôs a amostra (S1935 no lugar de S1721), republicou o formulário e atualizou contagens, texto e afirmações (A45, A46, A89; A118 nova, rascunho).

## T07 — correções da conferência humana (17/11/2026, D116)
- Os julgamentos são do autor (formulário, 10 estudos gravados). Claude Code (Claude Opus 5.5) aplicou as 43 alterações de campo nas fichas finais, com registro em `correcoes-manuais.jsonl`, reimportou e recalculou as contagens. A reformatação de S1743 pela gravação mudou só a disposição do JSON.
