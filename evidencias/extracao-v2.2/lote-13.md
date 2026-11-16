# Extração em escala — lote 13 (D103, D105)

Claude Opus 5.5 (subagentes, Read e Write), 16/11/2026, prompt ex-v2.2 congelado
(`f738eb50…c96d`), uma rodada (r1). Estudos: S1666, S1674, S1678, S1685, S1690, S1693,
S1694, S1698, S1704, S1706, S1707, S1708, S1711, S1725, S1727, S1734, S1736, S1740,
S1743, S1747.

- 19 saídas sem erro no validador viraram fichas finais, sem correção manual.
- S1711 sem ficha final: as duas comparações medem temperatura em °C, e o vocabulário de
  `unidade` não a prevê; fica com S654, S958 e S1234 para a decisão do autor sobre os
  vocabulários de `unidade` e `sentido`.
- S1743: as Tabelas II e IV estão em resolução insuficiente nas imagens de 110 dpi; os
  valores vêm do texto extraído, sem conferência visual (`conferido_pdf` = nao nas quatro
  comparações). Recomenda-se incluir a S1743 na amostra de conferência.
- S1704 sem comparação: análise de dados sociais (LDA, hashtags, emoções), sem avaliação
  de técnica de prompting; fica para o autor avaliar a inclusão.
- Só resultado descritivo (`sem_comparador` = sim): S1690, S1698, S1706, S1725, S1740.
- Exceções ao alvo de três, a conferir: S1693 (10), S1674 (7), S1708 (5), S1678 (4),
  S1743 (4), S1747 (4).
- Citações: 123 de 618 não achadas pelo verificador aproximado.
- As fichas não foram conferidas pelo autor.
