# Segunda calibração da ficha de extração (D102)

Executor: Claude Code (Claude Opus 5.5), 14/11/2026. Base: conferência das 10 fichas
ex-v2.1 pelo autor (`conferencia-autor-v2.1.jsonl`, formulário de 13/11/2026), as propostas
P1–P10 trazidas pelo autor em 13/11/2026 e a reaplicação do instrumento aos mesmos 10
estudos com subagentes Claude Opus 5.5 (Read e Write).

## Conferência do autor (ex-v2.1)

- 81 blocos julgados em 10 estudos; 26 marcados «Corrigir» (32%; na ex-v2, 43 de 85).
- Por estudo: S50 6; S500 3 (e a nota geral); S1695 3; S1775 3; S2183 3; S964 3; S570 2;
  S303 1; S1304 1; S1679 1.
- Minutos informados: 5 em cada uma das 10 fichas. Os salvamentos ficaram entre 00:08 e
  00:24 UTC de 14/11/2026 (21:08–21:24 de 13/11 no horário local); o registro não permite
  saber quanto da leitura ocorreu antes de abrir o formulário.
- Retificações do autor a orientações anteriores: em S50, o denominador do Pass@1 não é
  100 (o corpus não se liga inequivocamente à métrica); em S303, a discrepância «92 vs 74»
  do subconjunto v1.2 não está demonstrada e não deve voltar.

## Mudanças da ex-v2.2

As propostas P1–P10 e as notas do autor entraram no prompt
(`protocolo/prompts/extracao-v2.2.md`):

| Proposta | Regra | Estudos que motivaram |
|---|---|---|
| P1 | principal declarado só com técnica, métrica e comparador sem desempate | S1304, S1775 |
| P2 | resultado descritivo sem comparador; a condição nunca é seu próprio comparador | S1695 |
| P3 | tabela → figura → prosa; tabela com uma só condição não contém o contraste; diferença em prosa não vira valor calculado | S2183 |
| P4 | `tipo_contrafactual` (pacote, ingrediente, contraste pareado, cumulativo, nenhum) | S964, S2183 |
| P5 | contrastes pareados de matriz de ingredientes, por ordem fixa, só para completar três | S570 |
| P6 | `mecanismos` do pacote completo; `mecanismos_acrescentados` à parte; mesmo critério para variantes | S1679, S1775, S500, S964 |
| P7 | só agregado impresso compatível | — |
| P8 | rótulos de enumeração validados; linhas de tabela como citação; sem palavras acrescentadas | S303, S964 |
| P9 | ausência de relato não vira valor (execuções, denominador, versão) | S500, S50 |
| P10 | saídas brutas por rodada, versão do prompt e correções manuais à parte | — |

Notas do autor convertidas em regra: segurança operacional em `seguranca`; risco que leva
a código incorreto em `correcao_funcional`; contaminação controlada continua risco, com o
controle em mitigações; estímulo emocional em `instrucao`; permissões de ferramentas em
`restricoes`; pipeline encadeado em `decomposicao`; código fornecido no prompt em
`contexto`; cautela com arredondamento, escala e estimador na heterogeneidade; somas só
quando as linhas pertencem ao total; números de heterogeneidade conferidos no PDF.

Validador novo: `scripts/validar_ficha_extracao.py`. Nas fichas ex-v2.1, ele acusou na
S303 os cinco valores de `natureza` fora da lista que o autor havia apontado.

## Reaplicação

| Rodada | Prompt (SHA-256) | Estudos |
|---|---|---|
| 1 | ex-v2.2 inicial (`05a2c159…b917`) | os 10 |
| 2 | ex-v2.2 com quatro esclarecimentos (`f738eb50…c96d`) | S303, S570, S1304, S1695, S1775 |

Resultado da rodada 1 frente às notas do autor:
- Reproduziram as correções: S50, S500, S964, S1679, S2183.
- S303 e S1304: as linhas de base da tabela de resultados (ChatRepair 162 → 164; REINFIX
  GPT-4o 291 → 392), aprovadas pelo autor, foram descartadas como «não executadas» porque
  os valores vêm dos autores originais, e a seleção passou às ablações.
- S1695: a extração descritiva passou à primeira métrica da tabela («Test pass rate —
  Mean», 0,14), e não à razão de piores casos (4,32%) indicada pelo autor.
- S1775: acrescentou extração descritiva da abordagem multiagente, que o autor aceitara
  como só classificada, e registrou como `custo` o esforço manual que o autor pediu para
  tirar dessa categoria.
- S570: juntou as duas variantes do CYANEA numa técnica e perdeu a comparação da variante
  de camadas múltiplas, aprovada pelo autor.

Esclarecimentos da rodada 2:
- **Comparador da tabela:** linhas de base da tabela de resultados do estudo, no mesmo
  benchmark e métrica, contam como comparador mesmo com valores dos autores originais, com
  a origem registrada; números de outro artigo citados no texto, com outra amostra, prompt
  ou versão do benchmark, não contam.
- **Resultado descritivo:** em estudo sem comparador executado, o principal declarado
  exige técnica e métrica destacadas; em estudo com comparador, técnica focal só avaliada
  sem comparador vai para `so_classificadas`.
- **Custo:** só quando o próprio estudo trata o aspecto como custo.
- **Variantes:** formulações próprias avaliadas em linhas separadas são técnicas distintas.

Esses esclarecimentos não alteram os cinco estudos que ficaram na rodada 1. Neles, as
linhas de base são executadas, não há extração descritiva nem risco de custo, e as
variantes já eram técnicas separadas (os n-shot da S964 são parâmetro, não formulação).

Resultado da rodada 2: S303 voltou a ChatRepair 162 → 164 (`desempate_ordem`) com as
ablações de ferramentas de busca e máquina de estados; S1304 voltou a REINFIX 291 → 392
(`desempate_ordem`) com as ablações 154 → 177 e 158 → 177; S1695 passou a 4,32%,
`principal_declarado`, descritiva; S1775 ficou com as duas comparações e o multiagente em
`so_classificadas`; S570 recuperou a variante de camadas múltiplas (84,5) e manteve o
contraste pareado P3 → P1 (61,7 → 37,2). Com isso, as 21 comparações selecionadas coincidem
com as aprovadas ou corrigidas pelo autor nos 10 estudos. Mudanças de rótulo pelas regras
novas: S570 E0 passa de `principal_declarado` a `desempate_ordem` (duas variantes sem que
uma prevaleça); S303 E0, idem (sem comparador único no resumo).

## Fichas finais

- `extracao-v2.2/<ID>.json`: rodada 1 para S50, S500, S964, S1679 e S2183; rodada 2 para
  os demais (`rodadas/manifesto.csv`, com o SHA-256 do prompt e da saída bruta).
- Versão congelada: `protocolo/prompts/extracao-v2.2.md`, SHA-256
  `f738eb50041145174a68da20056cf8d03a7ca8d2dfd1fbd8fb55a87c46dac96d`.
- Correções manuais (`extracao-v2.2/correcoes-manuais.jsonl`), sem alterar as saídas
  brutas:
  1. S1304: divergência entre fontes S1304/S303 indicada pelo autor, de novo acrescentada
     à heterogeneidade (exige a leitura de S303).
  2. S1695: a frase «Diff max 0,00 é incompatível com variância positiva» passa a
     «aparente inconsistência», com arredondamento ou escala não informados.
  3. S570: a rodada 2 rotulou como `outro` a reformulação da especificação em linguagem
     natural; a rodada 1 usara `instrucao`, que o dicionário cobre. A ficha final usa
     `instrucao`, confirmada pelo autor em 14/11/2026.
- As correções de ex-v2.1 que eram manuais (métricas `parcial` em S303 e S1304) foram
  reproduzidas pela rodada 2.
- Validador: as 10 fichas finais passam.
- Citações: o verificador aproximado não achou 62 de 253 trechos no texto extraído. Nos
  trechos examinados, a causa foi texto de duas colunas intercalado, hifenização entre
  colunas ou palavras coladas (por exemplo, «Weuseddeterministic»). As linhas de tabela
  são citadas com «|» entre as células. A citação da S964 com palavra acrescentada foi
  corrigida pela rodada 1.

## Consumo

- Antes da rodada 1 (03:47 UTC, 14/11): janela de 5 horas 3%; semanal 31%.
- Depois da rodada 1 (03:55 UTC): 54%; 37%.
- Depois da rodada 2 (04:02 UTC): 80%; 41%.
- 15 extrações custaram 10 pontos do limite semanal, cerca de 0,67 ponto cada, valor
  próximo ao da calibração anterior.

## Limites

- A reaplicação usa o mesmo modelo do piloto, nos mesmos 10 estudos que orientaram as
  regras. A concordância com as correções do autor nesses estudos não estima a acurácia da
  extração em estudos novos; essa estimativa depende da conferência da amostra de 20% (P10).
- A rodada 1 mostrou variação de interpretação entre execuções do mesmo prompt (S570:
  variantes juntadas; mecanismo `instrucao` ou `outro`). Em escala, essa variação só aparece
  na conferência.
- Os esclarecimentos da rodada 2 foram derivados das aprovações anteriores do autor
  (S303, S1304, S1695, S1775) e confirmados por ele em 14/11/2026 («Confirmo os dois»).
