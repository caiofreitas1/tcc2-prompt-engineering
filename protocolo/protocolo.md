# Protocolo operacional — consolidação documental de T01

**Situação em 25/10/2026:** proposta derivada da análise inicial, reconciliada com
o ponto de controle e a confirmação registrada na issue #1. Ainda aguarda
confirmação atual do autor e manifestação do orientador; não é relato de execução
da RSL completa. Responsável por esta consolidação documental: Codex.
**Recorte proposto:** 2021-01-01 a 2026-09-07, português ou inglês.
Registrar qualquer mudança em contexto/decisoes.md antes de aplicá-la.

## Proveniência, estágio e confirmação

Fontes: proposta de TCC I, seções 1 e 4; análise inicial, seções 1.2–1.5 e 2.4;
ponto de controle de 03/10, campo «Estado atual» (originais e transcrições em
`fontes/legado/`). A [issue #1](https://github.com/caiofreitas1/tcc2-prompt-engineering/issues/1)
registra, em 25/10/2026, que o autor não realizou atividades do TCC após 03/10.
Assim, busca sistemática completa, deduplicação, triagem e constituição do corpus
definitivo continuam pendentes. O piloto não substitui essas etapas.

O objetivo permanece a RSL sobre prompting para geração, tradução, refatoração e
depuração, com taxonomia de apoio à implementação. O núcleo são modelos
pré-treinados usados por prompting. Não se propõem aqui treinamento de modelos,
experimentos próprios com LLMs ou comparação universal de ferramentas.

Confirmar com o autor o recorte, os critérios, a data de corte e a contribuição
prática (P1–P2 de [estado-atual.md](../contexto/estado-atual.md)); registrar a posição
do orientador e a viabilidade (P3). A disponibilidade das bases e o agendamento da
defesa permanecem pendentes (P4–P5). Não tratar o protocolo como aprovado nem a
issue como concluída enquanto faltarem confirmações obrigatórias.

## Questões
- QP1: quais técnicas são avaliadas e que evidências de eficácia são apresentadas,
  sob quais modelos, tarefas, métricas e condições?
- QP2: quais riscos técnicos são identificados e quais estratégias de mitigação
  são propostas ou avaliadas?
- QP3: como relacionar técnicas, tarefas e condições em uma taxonomia útil?

## Escopo e seleção
Critérios propostos, ainda sujeitos a P1/P3: incluir estudos primários, no recorte
e idiomas previstos, com texto completo,
prompting aplicado a geração, tradução, refatoração ou depuração e avaliação empírica
ou estudo de caso descrito. Testes entram quando apoiam essas tarefas.
Excluir duplicações e versões sobrepostas, textos sem detalhe técnico, tarefas fora
do escopo e trabalhos centrados apenas em treinamento ou arquitetura.
Separar preprints de publicações revisadas por pares. Priorizar a versão publicada
quando aplicável, preservando a versão lida. Fontes metodológicas e revisões podem
apoiar a fundamentação; não contar como estudos primários.

Literatura cinzenta permanece proposta como síntese complementar, identificada por
tipo de fonte e separada do corpus empírico, sem equivalência automática com
publicações revisadas por pares. Isso recupera o tratamento explícito da análise
inicial, seção 1.5.2; não registra coleta nem acrescenta fontes de busca.

A restrição do corpus a estudos primários empíricos é evolução em relação à
proposta de TCC I, seção 4.3, que também admitia estudos secundários e propostas de
ferramentas/revisões. A análise inicial já estabelecia essa restrição. A evolução e
as explicitações desta versão constam em [decisoes.md](../contexto/decisoes.md),
D03–D07; nenhuma nova restrição foi aplicada a estudos nesta execução.

## Busca (ainda proposta)
Bases previstas: ACM Digital Library, IEEE Xplore e arXiv, além de referências e citações.
O acesso atual à consulta, à exportação e aos textos completos em cada base ainda
não foi conferido; não inferir acesso institucional ou disponibilidade de PDFs a
partir dos links do piloto. Registrar impedimentos por base e submetê-los ao autor
antes de decidir substituições ou reduções de cobertura. Nesta T01 não houve
tentativa de busca acadêmica nem teste de acesso às bases.
Calibrar a expressão abaixo e adaptar a sintaxe por base. Registrar consulta exata,
campos, filtros, data real, quantidade exportada e arquivo de origem em dados/buscas.csv.
Não substituir a busca em bases por resultados da web sem documentar a alteração.

```text
("prompt engineering" OR prompting OR "in-context learning" OR "chain of thought"
 OR "self-planning" OR "self-debugging")
AND ("code generation" OR "code translation" OR refactoring OR debugging OR "program repair")
AND ("large language model" OR LLM OR "generative AI")
```

## Deduplicação e triagem
Preservar exportações brutas em dados/brutos/. Deduplicar por DOI, arXiv e título
normalizado, conferindo possíveis falsos positivos. Registrar grupos e representante.
Aplicar critérios em título/resumo e depois no texto completo. Usar incluir, excluir
ou duvida; fornecer critério e justificativa em dados/triagem.csv. Não excluir só por
ausência de um termo no título. Casos incertos seguem para revisão do autor.

## Extração e qualidade
Usar os contratos de dados/README.md. Separar estudo, relatório/versão e comparação.
Registrar tarefa, técnica, modelo/versão, linguagem, benchmark, comparador, métrica,
unidade, valores, chamadas, testes, amostragem, custo, ameaças e artefatos.
Avaliar objetivo, procedimento, comparador, métricas e ameaças com evidência para
cada julgamento. A rubrica deverá ser confirmada antes da aplicação em lote.
Usar os julgamentos para apreciar a confiabilidade da síntese, sem exclusão apenas
por qualidade, nota global automática ou limiar novo (proposta de TCC I, seção 4.4).
Não foram aplicados julgamentos de qualidade nesta consolidação.

## Síntese e contribuição prática
Agrupar por tarefa e mecanismo, aceitando múltiplos rótulos. Não ranquear técnicas
por resultados de estudos incompatíveis. Identificar resultados medidos, inferências
do TCC e sugestões dos autores. A matriz candidata deve ligar orientação a evidência,
contexto, limitação e verificação. Oito cenários (dois por tarefa) permanecem planejados;
sua aplicação não demonstra eficácia das técnicas nem substitui estudo com usuários.
Para cada cenário, a proposta herdada é registrar entrada, recomendação, evidência,
ambiguidades e verificação; examinar se a orientação é localizável, justificada e
suficientemente específica, com posterior revisão do orientador (análise inicial,
seção 2.4). A aplicação e a revisão ainda não ocorreram. A confirmação dessa forma
de avaliação e da adequação da contribuição prática é parte de P2/P3; não criar
cenários nem executar sua avaliação em T01.

## Auditoria e relato
Calcular contagens a partir dos registros efetivos, preservando denominadores.
Conferir uma amostra e divergências com autor/orientador conforme disponibilidade.
Relatar assistência por IA e limites de acesso, cobertura e revisão independente.
Não alegar dupla triagem ou concordância entre revisores sem sua realização.
Datas previstas no histórico não comprovam entrega, acesso, revisão ou agendamento.
Reavaliar a viabilidade do cronograma com o orientador; preservar os prazos
documentados em `contexto/estado-atual.md` sem inventar um novo plano aprovado.
