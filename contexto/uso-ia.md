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
