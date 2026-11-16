# Extração em escala — lote 11 (D103, D105)

Claude Opus 5.5 (subagentes, Read e Write), 16/11/2026, prompt ex-v2.2 congelado
(`f738eb50…c96d`), uma rodada (r1), lançado logo após a renovação da janela de 5 horas.
Estudos: S1141, S1155, S1163, S1176, S1179, S1195, S1204, S1220, S1229, S1234, S1280,
S1286, S1359, S1368, S1415, S1429, S1450, S1458, S1502, S1503.

- 19 fichas finais. Correção manual registrada (`correcoes-manuais.jsonl`), sem alterar a
  saída bruta: S1415, três sistemas comparadores com `avaliada_isoladamente` = nao e
  `tipo_contrafactual` = pacote passaram a nenhum, como na S6, S216 e S724.
- S1234 sem ficha final: as duas comparações medem número de linhas (#Lines, Tabela 1), e
  o extrator deixou `sentido` nulo porque o artigo não diz se mais ou menos linhas é melhor.
  O validador só aceita maior_melhor ou menor_melhor. Fica para decisão do autor, junto com
  as lacunas de `unidade` da S654 e da S958.
- Sem nenhuma comparação extraída, a avaliar a inclusão: S1176 (a única condição de
  prompting é o prompt original; tabelas descritivas), S1280 (as análises comparativas não
  são de prompting) e S1368 (estudo observacional sobre adoção de sugestões de refatoração
  do ChatGPT).
- S1220: só resultado descritivo (`sem_comparador` = sim).
- Exceção ao alvo de três, a conferir: S1195 (5).
- Citações: 171 de 523 não achadas pelo verificador aproximado.
- As fichas não foram conferidas pelo autor.
