# Extração em escala — lote 16 (D103, D105)

Claude Opus 5.5 (subagentes, Read e Write), 16/11/2026, prompt ex-v2.2 congelado
(`f738eb50…c96d`), uma rodada (r1). Últimos estudos do corpus definitivo: S2059, S2060,
S2075, S2085 (do antigo lote C4 do Codex, D105).

- S2059, S2060 e S2075: sem erro no validador, fichas finais sem correção manual.
- S2085 sem ficha final: a técnica focal (few-shot por aprendizado em contexto automático,
  Prompt4Code) tem `avaliada_isoladamente` = nao e `tipo_contrafactual` = pacote. Diferente
  dos sistemas comparadores corrigidos antes (S6, S216, S724, S1415, S1977), é a técnica
  focal: o extrator registra que o contraste com zero-shot e one-shot também muda o prompt
  de usuário (G contra A), o que confunde o pacote. Escolher entre `cumulativo`, `nenhum` ou
  `avaliada_isoladamente` = sim é julgamento, não ajuste de rótulo; fica para o autor.
- Exceção ao alvo de três, a conferir: S2059 (4).
- Citações: 55 de 117 não achadas pelo verificador aproximado.
- As fichas não foram conferidas pelo autor.

## Situação do corpus ao fim da extração

306 estudos no corpus definitivo: 10 fichas do piloto e 289 fichas finais em
`evidencias/extracao-v2.2/`. Sete sem ficha final, todos para decisão do autor:
- S1610: decisão de I4 pendente, não extraído.
- S667: gravação interrompida por classificador de segurança (jailbreak para código
  malicioso), sem saída bruta.
- S654, S958, S1711: `unidade` fora do vocabulário (métrica não definida; mWh; °C).
- S1234: `sentido` não informado pelo artigo (número de linhas).
- S2085: rótulo da técnica focal (acima).
