# Extração em escala — lote 7 (D103, D105)

Claude Opus 5.5 (subagentes, Read e Write), 16/11/2026, prompt ex-v2.2 congelado
(`f738eb50…c96d`), uma rodada (r1). Primeiro lote depois da troca do plano do autor
(D105), com 20 estudos: S579, S582, S588, S591, S597, S603, S604, S613, S629, S633, S634,
S641, S645, S647, S650, S654, S667, S670, S674, S682.

- 18 saídas sem erro no validador viraram fichas finais, sem correção manual.
- S667 sem saída: um classificador de segurança interrompeu a gravação do subagente, que
  relatou ter lido o texto inteiro antes. O estudo trata de jailbreak de modelos para gerar
  código malicioso. Não houve nova tentativa; o estudo saiu da fila automática e fica para
  decisão do autor (extração manual ou revisão da inclusão).
- S654 sem ficha final: a saída bruta (`rodadas/S654-r1.json`) tem `unidade` nula na
  segunda comparação (MoT × CodeCoT no SWE-bench Lite, Fig. 6b, «Score» 1,33 → 2,33). O
  artigo não define a métrica nem a unidade; os valores coincidem com 4/300 e 7/300 das 300
  tarefas do conjunto, o que sugere percentual resolvido, mas isso seria inferência. O
  validador não aceita `nao_informado` em `unidade`; fica para decisão do autor.
- Sem nenhuma comparação extraída, a avaliar a inclusão como S261, S320 e S398: S633
  (plataforma de avaliação CodeArena; um só prompt one-shot para todos os modelos), S641
  (avaliação de modelos com um procedimento de prompting fixo) e S682 (a técnica focal e o
  outro comparador são embeddings aprendidos; o prompt manual é a única condição de
  prompting).
- Exceções ao alvo de três, a conferir: S604 (15), S670 (8), S603 (4).
- Citações: 160 de 587 não achadas pelo verificador aproximado.
- Consumo: janela de 5 horas de 0% para 23% e semanal de 0% para 3% nas 20 execuções.
- As fichas não foram conferidas pelo autor.
