# Extração em escala — lote 12 (D103, D105)

Claude Opus 5.5 (subagentes, Read e Write), 16/11/2026, prompt ex-v2.2 congelado
(`f738eb50…c96d`), uma rodada (r1). Estudos: S1556, S1562, S1565, S1583, S1592, S1598,
S1601, S1604, S1606, S1607, S1608, S1613, S1614, S1620, S1625, S1631, S1640, S1642,
S1644, S1653.

- As 20 saídas passaram no validador e viraram fichas finais, sem correção manual.
- S1608: o texto extraído do PDF está ilegível (codificação de fontes); o subagente leu o
  artigo pelas imagens das páginas. Por isso as 37 citações não puderam ser achadas no
  texto pelo verificador; os valores foram conferidos nas páginas (`conferido_pdf` = sim).
  Recomenda-se incluir a S1608 na amostra de conferência.
- Sem nenhuma comparação extraída, a avaliar a inclusão: S1640 (descrição de uso em
  CODESYS, sem contraste de prompting), S1642 (técnica focal só classificada) e S1653
  (análise observacional de características de prompts reais, por regressão).
- Exceções ao alvo de três, a conferir: S1620 (6), S1556 (5), S1565 (4), S1606 (4).
- Citações: 157 de 510 não achadas pelo verificador aproximado (37 delas da S1608).
- As fichas não foram conferidas pelo autor.
