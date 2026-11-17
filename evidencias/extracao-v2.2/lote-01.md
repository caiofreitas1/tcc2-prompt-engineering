# Extração em escala — lote 1 (D103)

Executor: subagentes Claude Opus 5.5 (Read e Write), um por estudo; validação e registro por
Claude Code (Claude Opus 5.5), 15/11/2026 (UTC). Prompt ex-v2.2 congelado (SHA-256
`f738eb50…c96d`). Estudos, em ordem crescente de ID: S1, S4, S6, S14, S25, S53, S62, S65,
S77, S90, S109, S114, S120, S124, S129. Uma rodada (r1); saídas brutas em `rodadas/`,
manifesto com SHA-256 do prompt e de cada saída.

- 40 comparações: 1 `principal_declarado`, 14 `desempate_ordem`, 25 `cobertura`.
  S120 tem 7 comparações, com exceção ao alvo de três justificada por variantes focais
  (Oracle, TopK, Human × B, E, BE) avaliadas em linhas separadas; a conferir pelo autor.
- Validador: 13 saídas sem erro; S6 (5 erros) e S62 (1 erro) corrigidas à mão
  (`correcoes-manuais.jsonl`, confirmação do autor pendente). S6 revela lacuna do prompt:
  comparador com contraste de pacote na mesma tabela, mas tratado como linha de base.
- Citações: o verificador aproximado não achou 169 de 484 trechos. Na triagem por
  fragmentos, os de menor correspondência (S14, S25, S53, S62, S65, S77, S114, S120) foram
  conferidos por amostra no texto extraído e estavam presentes, com palavras coladas,
  colunas intercaladas ou glifos de fórmulas corrompidos. Não houve conferência exaustiva.
- Consumo: janela de 5 horas de 3% para 100%; semanal de 42% para 54% (cerca de 0,8 ponto
  por extração, acima da estimativa de 0,67; S14 tem 181 páginas).
- As fichas não foram conferidas pelo autor.
