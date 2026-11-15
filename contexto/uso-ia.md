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
