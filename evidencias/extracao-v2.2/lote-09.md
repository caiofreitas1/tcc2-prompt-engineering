# Extração em escala — lote 9 (D103, D105)

Claude Opus 5.5 (subagentes, Read e Write), 16/11/2026, prompt ex-v2.2 congelado
(`f738eb50…c96d`), uma rodada (r1). Estudos: S821, S834, S836, S842, S845, S852, S855,
S878, S887, S892, S895, S902, S910, S917, S919, S939, S951, S957, S958, S979.

- 19 saídas sem erro no validador viraram fichas finais, sem correção manual.
- S958 sem ficha final: a primeira comparação (CoT × solução humana, Tabela II) mede
  energia em mWh, informada pelo artigo, e o extrator deixou `unidade` nula porque o
  vocabulário do contrato (contagem, percentual, proporção, qualitativo, tempo) não tem
  unidade de energia. Fica para decisão do autor, junto com a S654 do lote 7: ampliar o
  vocabulário de `unidade` ou fixar outra regra para esses casos. A saída bruta fica em
  `rodadas/S958-r1.json`.
- Exceções ao alvo de três, a conferir: S836 (8), S842 (5), S892 (4), S895 (4).
- Citações: 189 de 588 não achadas pelo verificador aproximado.
- As fichas não foram conferidas pelo autor.
