# Protocolo — versão 2

**Situação em 27/10/2026:** versão 2 preparada por Claude Code (Claude Opus 5.5) a
partir das decisões do autor registradas em 27/10/2026 (D25–D31 em
[decisoes.md](../contexto/decisoes.md)). Entra em vigor com a integração do PR
pelo autor (PR #17, merge `7f2bd8e`) e foi confirmada por ele em 27/10/2026, antes
de qualquer busca (D32). A versão 1 (consolidação de T01,
commit `ba176e2`) permanece no histórico do Git. Recorte temático, questões,
período, idiomas e contribuição prática confirmados em 25/10 (D10–D12) não mudam.
Nenhuma busca, triagem ou extração foi executada nesta versão.

## 1. Tipo de estudo e diretrizes

Revisão sistemática da literatura (RSL) conduzida segundo Kitchenham, Budgen e
Brereton (2015) e relatada segundo PRISMA 2020 (Page et al., 2021). A busca em
bases é complementada por uma rodada de *snowballing* (Wohlin, 2014). A RSL é
executada majoritariamente por IA, com verificação humana pelo autor em pontos
de controle definidos na seção 7.

**Recuo previsto (D27):** se a decisão de 31/10 (seção 8) indicar inviabilidade,
o trabalho passa a revisão rápida declarada (Cartaxo, Pinto e Soares, 2020),
aplicando a restrição de título da seção 4.2 antes da triagem em lote. O recuo
é registrado em decisoes.md com motivo e números do piloto; não é aplicado depois
de iniciada a triagem em lote. Em 02/11/2026 o autor decidiu não aplicar o recuo
por causa do teto de horas e manter a RSL completa (D47).

**Decisão de 03/11/2026 (D64):** depois da resposta do orientador (D62) e da projeção de
esforço (D53, D63), o autor adotou a revisão rápida declarada, antes de iniciar a triagem
em lote. Substitui D47. Concessões a relatar: bloco de tarefas só no título, simulado nos
títulos sem nova busca nas bases; sem *snowballing* amplo (seção 4.4); leitura pelo texto
extraído (seção 6). A execução ocorre em duas etapas: primeiro os candidatos com indício de
revisão por pares, depois os demais. Se em 10/11 a segunda etapa não couber, o trabalho
para na primeira e declara o corte de preprints, sugerido pelo orientador; a etapa não é
feita pela metade. As verificações da seção 7 não mudam.

## 2. Questões de pesquisa

- **QP1:** quais técnicas de prompting são avaliadas e que evidências de eficácia
  são apresentadas, sob quais modelos, tarefas, métricas e condições?
- **QP2:** quais riscos técnicos são identificados e quais estratégias de
  mitigação são propostas ou avaliadas?
- **QP3:** como relacionar técnicas, tarefas e condições em uma taxonomia útil?

Tarefas no escopo: geração, tradução, refatoração e depuração de código
(incluindo reparo de programas), por prompting de modelos pré-treinados.

## 3. Critérios de seleção

Os códigos são usados em `dados/triagem.csv`, coluna `criterio`. Uma inclusão
exige todos os critérios I; uma exclusão cita pelo menos um critério X.

| Código | Critério de inclusão |
|---|---|
| I1 | Estudo primário. |
| I2 | Aplica prompting de modelo pré-treinado a geração, tradução, refatoração ou depuração/reparo de código. Testes entram quando apoiam essas tarefas. |
| I3 | Apresenta avaliação empírica ou estudo de caso suficientemente descrito. |
| I4 | Primeira versão pública entre 01/01/2021 e 07/09/2026; a versão lida pode ser posterior. |
| I5 | Texto em português ou inglês. |
| I6 | Texto completo disponível em acesso aberto (D26). |

| Código | Critério de exclusão |
|---|---|
| X1 | Duplicata ou versão sobreposta de estudo já registrado (agrupar, não descartar o registro). |
| X2 | Sem detalhe técnico suficiente para identificar técnica, tarefa e avaliação. |
| X3 | Tarefa fora do escopo (ex.: apenas sumarização, revisão de código ou perguntas sobre código). |
| X4 | Centrado apenas em treinamento, ajuste fino ou arquitetura do modelo. No texto completo, também outra intervenção avaliada que não seja prompting (D59). |

**Alteração de 05/11/2026 (D69):** I6 passa a aceitar texto obtido pelo autor por acesso
institucional (Portal de Periódicos da CAPES, UFMG), além do acesso aberto; X6 vale só
para texto que não se obtém por nenhum dos dois caminhos. Substitui D26 e D14 nesse ponto.
Os PDFs institucionais são baixados manualmente pelo autor, não são redistribuídos e
formam uma etapa 3, lida depois das etapas 1 e 2. É alteração posterior aos dados, para
reduzir o viés de disponibilidade.

**Alteração de 08/11/2026 (D84):** para a versão da banca (18/11/2026), a etapa 2 (estudos só no
arXiv, sem indício de revisão por pares) fica de fora, e a etapa 3 é lida depois da etapa 1. O
corpus da banca passa a ser o de estudos com indício de revisão por pares, abertos ou por acesso
institucional. A inclusão da etapa 2 na versão final depende de conversa com o orientador. É
alteração posterior aos dados, antecipando a decisão prevista para 10/11/2026.
| X5 | Estudo secundário, posicionamento ou tutorial (pode apoiar a fundamentação). |
| X6 | Texto completo sem versão em acesso aberto. |
| X7 | Fora do período ou do idioma. |

**Alteração de 03/11/2026 (D59):** depois da medição de 12 textos, o autor decidiu como
aplicar I2 e X4 no texto completo. I2 exige resultado de código obtido por prompting, com
a estratégia de prompt descrita, sem exigir comparador de prompting; código como etapa
intermediária é elegível se for avaliado; estudo observacional que só descreve o uso,
sem resultado sobre os prompts, vai ao autor como `duvida`. Essa regra está em tc-v2. No
título e resumo, tr-v2 mantém a redação anterior de X4, com a qual foi calibrada. Decisões
e pareceres anteriores não são reescritos. Esta alteração posterior aos dados é relatada
como desvio do protocolo.

Preprints e publicações revisadas por pares são identificados separadamente; a
versão publicada é preferida quando aberta, preservando a versão lida.
Literatura cinzenta segue como apoio complementar separado do corpus (D04).

## 4. Busca

### 4.1 Bases e acesso

| Base | Uso | Texto completo |
|---|---|---|
| arXiv | Busca pela API oficial | Aberto |
| ACM Digital Library | Busca e exportação | Aberto desde 01/01/2026 na edição Basic |
| IEEE Xplore | Busca e exportação de metadados | Somente via versão aberta localizada (arXiv, repositório do autor ou OpenAlex); sem versão aberta → X6 |

Não são usados artigos pagos nem acesso pela rede da UFMG (D26). O viés de
disponibilidade decorrente é ameaça à validade a relatar.

### 4.2 Expressão de busca

Aplicada a título e resumo; a sintaxe é adaptada por base e registrada em
`dados/buscas.csv` com a consulta exata. Onde a base não aceitar truncamento,
`transpil*` é substituído por `transpiler OR transpilation`.

```text
("prompt engineering" OR prompting OR prompt OR prompts OR "in-context learning"
 OR "few-shot" OR "zero-shot" OR "chain-of-thought" OR "chain of thought")
AND ("code generation" OR "program synthesis" OR "code translation"
 OR "program translation" OR "code migration" OR transpil* OR refactoring
 OR refactor OR debugging OR debug OR "program repair" OR "bug fixing"
 OR "bug fix" OR "bug repair")
AND ("large language model" OR "large language models" OR LLM OR LLMs
 OR "language model" OR "language models" OR "generative AI" OR ChatGPT
 OR "GPT-4" OR Codex)
```

Em relação à v1, foram retirados os nomes de técnicas do piloto
(«self-planning», «self-debugging»), que favoreciam estudos já conhecidos, e
acrescentados sinônimos de prompting, tarefas e modelos (D28).

**Variante de recuo (seção 1):** o bloco de tarefas é aplicado somente ao título.

### 4.3 Validação por estudos conhecidos

Os estudos do piloto funcionam como conjunto de referência (*quasi-gold
standard*; Zhang, Babar e Tell, 2011).

Calibração preliminar em 27/10/2026 (Claude Code), aplicando a expressão a título
e resumo de S1–S6 obtidos na API do arXiv (S6 pela versão arXiv:2501.13978v2):

| Estudo | Expressão ampla | Variante de título |
|---|---|---|
| S1, S4, S6 | recuperado | recuperado |
| S2 | recuperado | recuperado (termo `debug`) |
| S3 (Reflexion) | não recuperado: resumo sem termos de prompting nem de tarefa | não recuperado |
| S5 (usuários com assistentes) | não recuperado: resumo sem termo de tarefa | não recuperado |

S3 e S5 não descrevem técnica de prompting para as tarefas no título/resumo e
devem ser encontrados pelo *snowballing* ou confirmados como fora do escopo na
triagem. Essa calibração não substitui a validação na T04: conferir nas
exportações reais de cada base se S1, S2, S4 e S6 foram recuperados e registrar
o resultado. Uma falha leva a ajuste documentado da expressão antes da triagem.

Sondagem informal de volume (API do arXiv, 27/10, sem exportação nem registro
como busca): 1.509 registros na expressão ampla e 516 na variante de título.

**Resultado na T04 (29/10/2026, Claude Code):** S1 recuperado no arXiv (B1) e na ACM
(B3, versão TOSEM); S2 e S6 no arXiv; S4 no arXiv e na ACM. S3 e S5 não foram
recuperados, como na calibração. A expressão não precisou de ajuste. Pendente a
verificação do autor (seção 7).

**Encaminhamento (D59, 03/11/2026):** S1, S2, S4 e S6 passam pelo lote e pelo texto
completo como os demais, sem entrada automática no corpus. S3 e S5, se não aparecerem no
*snowballing* e o autor decidir considerá-los, entram como outra fonte, com contagem própria
e sem atribuir sua descoberta ao *snowballing*.

### 4.4 Snowballing

Uma rodada, para trás (referências) e para a frente (citações), sobre os estudos
incluídos no texto completo, via OpenAlex. Cada direção é uma linha em
`dados/buscas.csv` (base `snowballing_backward` ou `snowballing_forward`), com
exportação preservada. Os registros novos passam pela mesma triagem.

**Alteração de 03/11/2026 (D64):** na revisão rápida, não há *snowballing* amplo: uma rodada
sobre centenas de incluídos não cabe no prazo. É concessão a relatar. S3 e S5 ficam fora,
salvo decisão do autor de considerá-los como outra fonte (D59).

## 5. Registros e deduplicação

- `dados/brutos/`: exportações originais, nunca editadas.
- `dados/registros.csv`: uma linha por registro exportado, ligada à busca de
  origem e, após deduplicação, ao estudo (`estudo_id`). Grupos de duplicatas são
  os registros que compartilham `estudo_id`.
- Deduplicação por DOI, identificador arXiv e título normalizado; possíveis
  falsos positivos conferidos antes de agrupar.
- As contagens do fluxograma PRISMA são calculadas desses registros.

## 6. Triagem com dois triadores de IA

**Triadores (D29):** IA-A = Claude Opus 5.5 (sessão principal do Claude Code);
IA-B = Claude Sonnet 5.5 em subagente separado, com o mesmo prompt e sem acesso
às decisões de IA-A. Modelos do mesmo fornecedor podem ter erros correlacionados;
a verificação humana por amostragem compensa parcialmente e a limitação é relatada.
Desde a amostra 2 do piloto, IA-A também roda em subagente separado, sem o contexto
da sessão principal (D48).

**Prompts:** versionados em [prompts/](prompts/). Cada decisão de IA registra
`prompt_versao`. Os prompts são calibrados no lote piloto e congelados antes do
lote principal; qualquer mudança gera nova versão e é registrada.

**Título e resumo:** cada registro é triado por IA-A e IA-B. Segue para o texto
completo se ao menos um triador decidir `incluir` ou `duvida` (regra de união,
para maximizar a revocação). Exclusão exige as duas IAs.

**Texto completo:** IA-A e IA-B leem o texto aberto. Divergências vão ao autor.
Toda inclusão é confirmada pelo autor; somente a decisão humana `incluir` no
texto completo coloca o estudo no corpus definitivo (verificada em `make check`).
Desde D64, IA-A e IA-B leem o texto extraído do PDF e voltam ao PDF em caso de dúvida
ou de tabela desordenada.

## 7. Verificação humana (pontos de controle)

| Ponto | Verificação pelo autor | Uso |
|---|---|---|
| Após a busca (T04) | Expressões, exportações e recuperação de S1, S2, S4 e S6 | Liberar a triagem |
| Lote piloto (T05) | Triagem independente de 100 registros aleatórios, sem ver as decisões das IAs | κ de Cohen autor × consenso das IAs; revocação |
| Exclusões de título e resumo (T05) | Amostra aleatória de 100 exclusões consensuais das IAs | Estimar estudos relevantes perdidos |
| Texto completo (T06) | Todas as divergências e inclusões; 20% (mínimo 15) das exclusões consensuais | Constituir o corpus |
| Extração (T07) | Estudo como unidade (ficha, extrações e qualidade): `max(10, teto(0,20 × N))` estudos, com N = incluídos finais, priorizando os que sustentam afirmações e distribuídos por tarefa e técnica; os 10 do piloto contam se conferidos na versão final da ficha (D97) | Confirmar `revisao_humana` dos estudos conferidos |
| Texto (T12) | Cada afirmação de `dados/afirmacoes.csv` contra o original | Marcar `sustentada` |

**Regra de parada no piloto:** se o autor incluir um registro que as duas IAs
excluíram, o prompt é revisado (nova versão) e reaplicado a uma nova amostra de
50 registros; no máximo duas revisões. Persistindo a perda, registrar a revocação
observada como limitação. Com amostras desse tamanho, as estimativas são
imprecisas; relatar contagens brutas junto com κ.

Também é calculado κ entre IA-A e IA-B em todos os registros triados.

**Complemento de 03/11/2026 (D66):** estudo com exclusão consensual que o autor marcar como
`incluir` ou `duvida` na conferência, ou que já tenha essa decisão nas amostras do piloto,
segue ao texto completo. O relato separa quantos os modelos teriam perdido e quantos foram
resgatados. O resgate não coloca o estudo no corpus.

## 8. Decisão de 31/10/2026: RSL completa ou recuo

Critérios propostos para aprovação do autor no PR:

1. registros únicos após deduplicação ≤ 2.500;
2. lote piloto sem perda de estudo incluído pelo autor após no máximo uma revisão
   do prompt;
3. projeção das horas do autor até 08/11 ≤ 12 h, calculada pelo tempo medido no piloto
   e cobrindo todos os pontos de controle da seção 7 até o texto completo (D33).

Atendidos os três, segue a RSL completa. Caso contrário, aplicar o recuo da
seção 1. A decisão, os números e a data são registrados em decisoes.md.

**Alteração de 02/11/2026 (D47):** depois de conhecer os resultados do piloto, o autor
decidiu que o teto de 12 h do critério 3 deixa de decidir o recuo, porque pode dedicar
mais horas. Sua disponibilidade não demonstra a viabilidade: o esforço restante, com o
tempo medido das conferências de texto completo, será projetado e o cronograma da
seção 12, atualizado. A busca ampla e as verificações da seção 7 não mudam. O critério
2 e a regra de parada também não mudam. Esta alteração posterior aos dados é relatada
como desvio do protocolo.

## 9. Extração

Contrato em [dados/README.md](../dados/README.md). Extrações novas usam
`contrato: 2`, que exige:

- citação literal (`citacoes`) com localizador para cada valor extraído; o
  `make check` confirma que o trecho existe no texto do PDF (`texto_fonte`);
- campos da QP2: `riscos` e `mitigacoes`, com categoria e localizador.

Categorias iniciais de risco: `correcao_funcional`, `seguranca`, `alucinacao`,
`contaminacao`, `nao_determinismo`, `custo`, `manutenibilidade`, `outro`.

Todos os incluídos recebem a classificação (tarefa, técnica, modelo, benchmark,
riscos e mitigações), que alimenta QP2 e QP3. A extração numérica detalhada da
QP1 é feita para cada comparação reportada; não se comparam números entre
condições incompatíveis.

**Complemento de 10/11/2026 (D97):** a extração usa o prompt `ex-v2`
(`protocolo/prompts/extracao-v2.md`), versão de piloto até a calibração em 10 estudos.
Cada estudo incluído recebe uma ficha classificatória completa (tarefas, técnicas com nome
original, mecanismo atribuído pelo TCC e papel focal, comparador ou componente, modelos,
benchmarks, métricas, riscos, mitigações e os sete critérios de qualidade). A extração
numérica não é exaustiva: até três comparações por estudo como alvo, escolhidas sem
considerar ganho, perda, significância ou tamanho do efeito, nesta ordem: resultado
principal declarado pelo estudo; na falta ou empate, a primeira tabela com resultados
elegíveis de prompting para tarefas do escopo, a primeira métrica pertinente e o primeiro
modelo; depois, cobertura de técnicas focais e tarefas ainda não representadas. Técnica
focal sem número extraído fica marcada como só classificada. Resultados nulos, inversões e
condições discrepantes são registrados à parte, como busca dirigida de heterogeneidade, sem
serem tratados como amostra neutra. A taxonomia é multirrótulo, com dicionário de
mecanismos; frequências contam estudos distintos e informam a sobreposição. O trabalho
segue por lotes: metadados e I4 do lote, extração, conferência. A seleção de comparações
é simplificação da revisão rápida e limita as conclusões da QP1.

## 10. Qualidade

Rubrica por estudo, adaptada de Dybå e Dingsøyr (2008) e acrescida de critérios
específicos de LLMs (Sallou, Durieux e Panichella, 2024):

| Critério | Pergunta |
|---|---|
| objetivo | O objetivo e as perguntas do estudo estão claros? |
| procedimento | O desenho e a execução estão descritos o bastante para entender o resultado? |
| comparador | Há linha de base ou comparador adequado? |
| metricas | As métricas e a análise são adequadas e explicadas? |
| ameacas | As ameaças à validade são discutidas? |
| reprodutibilidade | Modelo/versão, parâmetros, prompts e artefatos são informados? |
| contaminacao | O risco de o benchmark estar nos dados de treino é tratado? |

Julgamentos: `atende`, `parcial`, `nao_atende`, `nao_informado`, com localizador e
justificativa. A qualidade qualifica a síntese; não exclui estudos nem gera nota
global (D07).

## 11. Síntese e contribuição prática

Sem alteração em relação a D12: agrupar por tarefa e mecanismo (multirrótulo);
não ranquear técnicas entre estudos incompatíveis; separar resultado medido,
inferência do TCC e sugestão dos autores. A taxonomia e a tabela de apoio à
escolha são examinadas em oito cenários, dois por tarefa, quanto a clareza,
justificativa nas fontes e orientação concreta; isso não mede eficácia.
Complemento de 10/11/2026 (D97): os cenários têm origem sintética declarada, são
aprovados pelo autor e congelados antes do exame, junto com a versão da tabela aplicada;
incluem situações de evidência insuficiente, em que a ausência de recomendação pode ser a
resposta adequada. Registram-se, por cenário e critério, julgamento, justificativa e
ambiguidades.

## 12. Cronograma (D33–D34)

O texto de 08/11 é o texto completo (D33), não mais um texto com resultados
parciais (D30). Todas as etapas da revisão precisam terminar antes dessa data.
A tabela original é a de D34, preservada no histórico. A tabela abaixo é a de D64, que
substitui D33: em 08/11 entra o texto com resultados preliminares da primeira etapa, a
confirmar pelo autor na disciplina; a versão da banca é a de 18/11 (D62).

| Período | Etapa |
|---|---|
| 03–04/11 | T05: congelamento dos prompts; triagem de título e resumo; conferência de 100 exclusões |
| 04–07/11 | T06: texto completo da primeira etapa; T07: teste de extração e extração |
| **08/11** | **Texto com resultados preliminares da primeira etapa** |
| 09–13/11 | T06 e T07: segunda etapa; reavaliação do limite do plano em 10/11 |
| 14–17/11 | T08 e T09: síntese e cenários; T11 e T12 |
| **18/11** | **Versão da banca** |
| **19/11** | **Defesa** |
| 20–29/11 | Ajustes da banca e verificação final |
| **29/11** | **Texto final** |

## 13. Relato e uso de IA

Relatar as contagens PRISMA a partir dos registros, os modelos, as versões dos
prompts, os pontos de verificação humana com tamanhos de amostra e κ, e o
registro de [uso de IA](../contexto/uso-ia.md). Não alegar dupla triagem humana:
a dupla triagem é feita por dois modelos, com verificação humana por amostragem.

## Referências do método

- Cartaxo, B.; Pinto, G.; Soares, S. Rapid Reviews in Software Engineering. In:
  *Contemporary Empirical Methods in Software Engineering*. Springer, 2020,
  p. 357–384. doi:10.1007/978-3-030-32489-6_13.
- Dybå, T.; Dingsøyr, T. Empirical studies of agile software development: A
  systematic review. *Information and Software Technology*, 50(9–10):833–859, 2008.
  doi:10.1016/j.infsof.2008.01.006.
- Kitchenham, B. A.; Budgen, D.; Brereton, P. *Evidence-Based Software Engineering
  and Systematic Reviews*. Chapman and Hall/CRC, 2015. doi:10.1201/b19467.
- Page, M. J. et al. The PRISMA 2020 statement: an updated guideline for reporting
  systematic reviews. *BMJ*, 372:n71, 2021. doi:10.1136/bmj.n71.
- Sallou, J.; Durieux, T.; Panichella, A. Breaking the Silence: the Threats of Using
  LLMs in Software Engineering. In: *ICSE-NIER 2024*, p. 102–106.
  doi:10.1145/3639476.3639764.
- Wohlin, C. Guidelines for snowballing in systematic literature studies and a
  replication in software engineering. In: *EASE 2014*, p. 1–10.
  doi:10.1145/2601248.2601268.
- Zhang, H.; Babar, M. A.; Tell, P. Identifying relevant studies in software
  engineering. *Information and Software Technology*, 53(6):625–637, 2011.
  doi:10.1016/j.infsof.2010.12.010.

Metadados conferidos no Crossref em 27/10/2026 por Claude Code.
