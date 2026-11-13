# Calibração da ficha de extração após o piloto (D101)

Executor: Claude Code (Claude Opus 5.5), 13/11/2026. Base: conferência das 10 fichas do
piloto pelo autor (`conferencia-autor.jsonl`, formulário de 13/11/2026) e reaplicação do
instrumento aos mesmos 10 estudos com subagentes Claude Opus 5.5 (Read e Write).

## Conferência do autor (ex-v2)

- 85 blocos julgados em 10 estudos; 43 marcados «Corrigir» (51%).
- Por bloco: classificação 7/10; comparações 12/21; heterogeneidade 6/10; qualidade 6/10;
  citações da ficha 3/10; riscos 3/10; contexto 2/10; observações gerais 4/4 preenchidas.
- Minutos informados em 5 das 10 fichas (5 minutos cada); os demais ficaram em branco.
  O tempo de conferência por ficha continua sem medida suficiente para projetar as
  conferências da amostra de 20%.

## Problemas sistemáticos identificados

1. Intervenções que não são prompting (ajuste fino, tokens treináveis, parâmetros de
   decodificação, alocação de orçamento) contadas como técnicas focais e uma delas
   extraída como comparação (S500, S570, S964).
2. Regra de seleção: «principal declarado» aplicado sem principal único (S500, S1679);
   desempate só por tabela, sem figuras (S964); sem regra para condição versus agregado
   (S964); segunda comparação da mesma técnica e tarefa em outro benchmark (S50).
3. `avaliada_isoladamente` sem condição contrafactual (S1304) ou com valor fora do
   contrato (S303); mitigação marcada como avaliada sem comparação (S570).
4. Mecanismos incompletos: papel e diretrizes sem `instrucao` (S303); RAG com exemplos
   sem `exemplos` (S1775); seleção humana entre respostas sem `amostragem` (S1775);
   exemplos no prompt de mitigação (S1679).
5. Leitura só pelo texto extraído: valores de figuras não lidos (S964), tabela tratada
   como ilegível (S570) e número impresso inconsistente tratado como erro de extração
   (S1695).
6. Heterogeneidade sem inconsistências internas: totais que não batem (S303), narrativa
   contra tabela (S570), linhas de base diferentes entre figuras (S964), pioras em figuras
   (S1679).
7. Qualidade: `nao_atende` e `nao_informado` usados para a mesma situação (contaminação
   não discutida); ausência de seção de ameaças tratada como `nao_atende` (S570).
8. Citações cortadas no meio de palavra ou oração (S50, S303, S2183).
9. Comparador externo (números de outro artigo) tratado como linha de base (S1695);
   afirmação de vantagem registrada como risco de custo (S50).

## Decisões do autor (13/11/2026)

- Condição versus agregado: usar o agregado impresso (média ou total); sem agregado, a
  primeira condição.
- PDF: conferir no PDF os valores selecionados, cabeçalhos, legendas, unidades, notas e
  condições; ampliar a inspeção quando houver dúvida; registrar null com o motivo se a
  leitura continuar insegura; não estimar valores pela altura das barras.
- Qualidade: `nao_informado` quando, após busca no texto completo, faltarem informações
  para julgar; `nao_atende` com evidência de descumprimento ou inadequação; `parcial` para
  atendimento incompleto; `atende` com evidência suficiente; ausência de seção própria não
  determina o julgamento.

## Reaplicação

| Rodada | Prompt (SHA-256) | Leitura do PDF | Estudos |
|---|---|---|---|
| 1 | ex-v2.1 inicial (`292cc59b…`) | `Read` com páginas falhou (sem `pdftoppm`); 7 abriram o PDF inteiro, 1 não abriu | 10 |
| 2 | ex-v2.1 com regra de principal, tabela antes de figura, ingredientes e ablações (`d62f86db…`) | imagens das páginas geradas com Ghostscript (`fontes/artigos/paginas/`, fora do Git) | 10 |
| 3 | ex-v2.1 com principal de uma técnica, ordem das tabelas, silêncio = `nao_informado` e exemplos ilustrativos (`9935ba7d…`) | idem | S500, S1679, S964 |

Resultado da rodada 2 frente às correções do autor:
- Seleção igual à corrigida pelo autor em 8 de 10 estudos (S50, S303, S570, S964, S1304,
  S1695, S1775, S2183). Divergiram S500 (pass@1 como principal; o autor indicou
  correctness@5 por desempate) e S1679 (principal pelo resumo; o autor indicou desempate
  pela Tabela III). As regras foram esclarecidas e testadas na rodada 3.
- Componentes fora do escopo separados nos 10; ablações só completam o alvo de três.
- Valores de figura lidos (S964: 0,49/0,43 e 0,50/0,74, agregados impressos).
- Divergências que ficam para o autor: S570, ingredientes dos estilos de prompt marcados
  como avaliados isoladamente, porque a Tabela 1 permite contrastes que diferem em um único
  ingrediente (P1 × P3, P2 × P1, P5 × P3); S303 e S1304, métricas `atende` (o autor indicou
  `parcial`).

Resultado da rodada 3: S500 passou a correctness@5 por desempate (2,0 × 7,2); S1679
passou ao desempate pela Tabela III (269 → 299), com Refined Hints (269 → 801) e Syntax
Mitigation (450 → 335, menor é melhor, com `exemplos`) por cobertura e as pioras das Figs.
6–7 em heterogeneidade; S964 marcou contaminação como `nao_informado`. Com isso, a seleção
coincide com a corrigida pelo autor nos 10 estudos.

## Versão congelada e fichas finais

- `protocolo/prompts/extracao-v2.1.md`, SHA-256
  `9935ba7dc1528ecb2a150caff10d03306ebcc4f257815dcab8c3d05a53e55abd` (versão da rodada 3).
- Fichas finais em `extracao-v2.1/`: rodada 3 para S500, S964 e S1679; rodada 2 para os
  demais. Todas as rodadas ficam em `extracao-v2.1/rodadas/`.
- Correções do autor aplicadas à mão (`extracao-v2.1/correcoes-manuais.jsonl`): métricas
  `parcial` em S303 e S1304; divergências entre fontes acrescentadas à heterogeneidade de
  S1304 (exigem a leitura de S303, fora do alcance de uma extração por estudo).
- Pendente de decisão do autor: S570, ingredientes dos estilos de prompt.

## Limites

- A reaplicação é feita pelo mesmo modelo que fez o piloto; a concordância com as
  correções do autor não mede a taxa de erro da extração em escala.
- As fichas finais dos 10 estudos combinam a rodada mais recente com as correções do autor
  que o instrumento não reproduziu; cada correção aplicada à mão fica registrada.
