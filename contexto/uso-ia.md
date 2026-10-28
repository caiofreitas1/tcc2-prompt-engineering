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
