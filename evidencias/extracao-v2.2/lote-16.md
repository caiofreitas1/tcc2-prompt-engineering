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

## Situação do corpus

Atualizada depois de D106 em `situacao-2026-11-16.md` (S2085 virou ficha final por correção
registrada; restam S1610 e S667 sem ficha).
