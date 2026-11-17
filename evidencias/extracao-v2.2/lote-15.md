# Extração em escala — lote 15 (D103, D105)

Claude Opus 5.5 (subagentes, Read e Write), 16/11/2026, prompt ex-v2.2 congelado
(`f738eb50…c96d`), uma rodada (r1). 15 estudos, para parar abaixo de cerca de 85% da
janela de 5 horas: S1924, S1943, S1951, S1960, S1970, S1977, S2000, S2046, S2048, S2051,
S2053, S2054, S2055, S2056, S2057 (S2054–S2057 vieram do antigo lote C4 do Codex, D105).

- 15 fichas finais. Correção manual registrada (`correcoes-manuais.jsonl`), sem alterar a
  saída bruta: S1977, quatro sistemas comparadores (Expert Prompt, CoT, Self-Refine,
  ReAct+AST) com `avaliada_isoladamente` = nao e `tipo_contrafactual` = pacote passaram a
  nenhum, como na S6, S216, S724 e S1415.
- S1960 sem comparação: uso real de um serviço com modelo ajustado para Ansible, com um só
  formato de prompt; fica para o autor avaliar a inclusão.
- S2000: só resultado descritivo (`sem_comparador` = sim).
- Exceções ao alvo de três, a conferir: S2054 (4), S2056 (4).
- Citações: 149 de 429 não achadas pelo verificador aproximado.
- As fichas não foram conferidas pelo autor.
