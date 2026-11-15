# Extração em escala — lote 2 (D103)

Executor: subagentes Claude Opus 5.5 (Read e Write), um por estudo; validação e registro por
Claude Code (Claude Opus 5.5), 15/11/2026. Prompt ex-v2.2 congelado (`f738eb50…c96d`).
Estudos, em ordem crescente de ID (S1610 adiada até a decisão de I4 pelo autor): S137,
S140, S149, S150, S170, S176, S193, S195, S202, S207, S213, S216, S233, S247, S261. Uma
rodada (r1). O subagente da S193 parou no limite de 5 horas depois de gravar a saída
(JSON completo, validado); não houve nova execução.

- 46 comparações: 3 `principal_declarado`, 11 `desempate_ordem`, 32 `cobertura`.
- Exceções ao alvo de três, por variantes focais avaliadas em linhas separadas, a conferir:
  S140 (10: cinco estratégias em dois cenários, o segundo com feedback de testes), S213 (7),
  S137 (5). Na S137, as três primeiras comparações têm 0 → 0 (InCoder-6B, primeiro modelo
  da Tabela 4), resultado da regra de ordem.
- S261 sem comparação: a única condição de prompting é a linha de base zero-shot do GPT-3.5
  contra um modelo ajustado (fora do escopo). Fica para o autor avaliar se o estudo atende
  aos critérios de inclusão.
- Validador: 14 saídas sem erro; S216 com a mesma incoerência da S6 (comparador com
  `avaliada_isoladamente` = nao e `tipo_contrafactual` = pacote), corrigida à mão em duas
  técnicas (`correcoes-manuais.jsonl`). Na mesma ficha, outros comparadores receberam
  sim/pacote: a regra para linhas de base com contraste de pacote varia entre execuções.
- Citações: o verificador aproximado não achou 192 de 555 trechos. Trechos de menor
  correspondência conferidos por amostra (S176, S193, S195) estavam no texto extraído,
  intercalados entre colunas; não houve conferência exaustiva.
- Consumo: semanal de 55% para 69% (cerca de 0,93 ponto por extração).
- As fichas não foram conferidas pelo autor.
