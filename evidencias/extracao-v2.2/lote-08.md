# Extração em escala — lote 8 (D103, D105)

Claude Opus 5.5 (subagentes, Read e Write), 16/11/2026, prompt ex-v2.2 congelado
(`f738eb50…c96d`), uma rodada (r1). Estudos: S692, S695, S699, S703, S715, S724, S732,
S739, S740, S755, S759, S760, S771, S782, S783, S795, S799, S800, S806, S810.

- 18 saídas sem erro no validador; as 20 viraram fichas finais.
- Correções manuais registradas (`correcoes-manuais.jsonl`), sem alterar as saídas brutas:
  - S724: três sistemas comparadores (Original + µFix, Vanilla Repair, ClarifyGPT-auto)
    com `avaliada_isoladamente` = nao e `tipo_contrafactual` = pacote; o tipo passou a
    nenhum, como na S6 e na S216.
  - S810: dois componentes do Forest of Thinking com `decomposicao` em
    `mecanismos_acrescentados` e fora de `mecanismos`; o mecanismo foi acrescentado a
    `mecanismos`, como na S62.
- S800 sem comparação: uma única condição de prompting (prompt de sistema fixo); os
  contrastes do estudo são entre modelos. Fica para o autor avaliar a inclusão, como as
  S633, S641 e S682 do lote 7.
- Exceções ao alvo de três, a conferir: S715 (6), S692 (5), S759 (4).
- Citações: 215 de 677 não achadas pelo verificador aproximado.
- Consumo: os lotes 7 e 8 levaram a janela de 5 horas a 40% e o semanal a 6%.
- As fichas não foram conferidas pelo autor.
