# Extração em escala — lote 4 (Opus) e lote C1 (Codex) (D103, D104)

16/11/2026. Prompt ex-v2.2 congelado (`f738eb50…c96d`); uma rodada (r1) por estudo; o
manifesto passa a registrar `executor` e `modelo_executor` em todas as linhas.

## Lote 4 — Claude Opus 5.5 (subagentes, Read e Write)

S325, S328, S329, S342, S344, S348, S354, S357, S360, S361, S362, S365 (12, para poupar o
limite semanal). As 12 saídas passam no validador, sem correção manual. S325 tem extração
descritiva (`sem_comparador` = sim). Na S362, a figura não pôde ser lida com segurança; o
resultado ficou nulo, com `conferido_pdf` = nao e o motivo em `condicoes`. Citações: 95 de
321 não achadas pelo verificador aproximado.

## Lote C1 — Codex CLI 0.169.0 (gpt-6.1-sol, esforço high)

Lançados 15 estudos, do fim da lista: S2233, S2175, S2170, S2164, S2163, S2162, S2157, S2155,
S2152, S2145, S2141, S2140, S2135, S2131, S2130. Dez saídas gravadas, todas sem erro no
validador. Cinco sessões (S2170, S2164, S2145, S2135, S2130) pararam no limite de uso da
assinatura do Codex antes de gravar; ficam para o próximo lote do Codex.

- Exceções ao alvo de três, a conferir: S2152 (7) e S2162 (6), por variantes focais.
- S2163 sem comparação: técnica focal só classificada.
- Citações: 140 de 498 não achadas pelo verificador aproximado.

## Situação

- Estudos extraídos fora do piloto: 67 de 296 (57 pelo Opus, 10 pelo Codex).
- Consumo do Opus: semanal de 83% para 92% com os dois lotes e a orquestração.
- As fichas não foram conferidas pelo autor.
