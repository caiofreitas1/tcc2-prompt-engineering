# Calibração do Codex como segundo extrator (piloto, ex-v2.2)

Executor: Codex CLI 0.169.0, modelo gpt-6.1-sol (esforço high), `codex exec` com sandbox
`workspace-write`, uma sessão por estudo, 16/11/2026; comparação por Claude Code (Claude
Opus 5.5). Prompt ex-v2.2 congelado (`f738eb50…c96d`), o mesmo dos lotes do Opus. Saídas
brutas em `extracao-v2.2-codex/rodadas/`, sem alteração. Antes da rodada, um teste
confirmou que o Codex abre as imagens das páginas (`view_image`).

Referência: as fichas ex-v2.2 finais do piloto (`extracao-v2.2/`), cuja seleção coincide com
as comparações aprovadas ou corrigidas pelo autor.

## Resultado

- Validador: as 10 saídas sem erro de rótulo.
- Comparações de referência reproduzidas com os mesmos valores: 18 de 21 (S303, S500, S570,
  S1304, S1679, S1775 e S2183 completas).
- Divergências:
  1. S964: na Fig. 4 (LLaMA, grupo Avg), registrou 1-shot = 0,48; na figura, 0,48 é o
     rótulo da barra de 2-shot e o 1-shot é 0,43 (conferido em imagem ampliada da p. 5).
     Erro de leitura de valor.
  2. S50: escolheu a linha ADELT (Small), primeira da Tabela 1 (70,8), embora a
     contribuição declarada cite os valores do ADELT (Base) (73,0), usados na referência.
  3. S1695: extração descritiva pela média de test pass rate (0,14), e não pela razão de
     piores casos (4,32%); o mesmo erro da rodada 1 do Opus.
  Além disso, a S964 ganhou a tarefa `depuracao` e uma terceira comparação (reparo das
  traduções pelo pipeline com agente), ausentes da referência.
- Citações: o verificador aproximado não achou 85 de 644 trechos (13%; nos lotes do Opus,
  cerca de 35%).
- Tokens informados pelo Codex: 76 mil a 107 mil por estudo.

## Limites

- A comparação não é simétrica: as regras da ex-v2.2 foram calibradas com as saídas do
  Opus nesses mesmos estudos, e o Opus só chegou às 21 comparações depois de duas rodadas.
  Na rodada 1 do Opus, com o prompt inicial, cinco estudos divergiram.
- Dez estudos não estimam a taxa de erro de nenhum dos dois extratores em estudos novos.
- A adoção do Codex depende de decisão do autor.
