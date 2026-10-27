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
