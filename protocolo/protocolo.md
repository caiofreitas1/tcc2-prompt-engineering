# Protocolo operacional — consolidação documental de T01

**Situação em 25/10/2026:** protocolo derivado da análise inicial, reconciliado com
o ponto de controle e as confirmações do autor na issue #1 e neste chat. Recorte,
critérios e contribuição prática confirmados pelo autor em 25/10/2026 (A3–A4 em
`contexto/estado-atual.md`). O orientador revisará ao final do trabalho, conforme
decisão do autor (A2/A4); essa revisão ainda não ocorreu. Não é relato de execução
da RSL completa. Responsável por esta consolidação documental: Codex.
**Recorte confirmado pelo autor:** 2021-01-01 a 2026-09-07, português ou inglês.
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

O autor confirmou recorte, critérios, data de corte e contribuição prática
(P1–P2 de [estado-atual.md](../contexto/estado-atual.md)). As decisões são tomadas
pelo autor com apoio do agente; a revisão do orientador ocorrerá ao final (P3),
sem exigir aprovação prévia para iniciar a execução. A defesa ainda não foi marcada
e o acesso institucional a artigos depende da rede da UFMG (P4–P5). Essas
informações atendem ao registro de situação exigido em T01; a execução da busca
e o agendamento não foram realizados nesta issue. Não declarar aprovação do
orientador ou conclusão das etapas acadêmicas a partir da confirmação do protocolo.

## Questões
- QP1: quais técnicas são avaliadas e que evidências de eficácia são apresentadas,
  sob quais modelos, tarefas, métricas e condições?
- QP2: quais riscos técnicos são identificados e quais estratégias de mitigação
  são propostas ou avaliadas?
- QP3: como relacionar técnicas, tarefas e condições em uma taxonomia útil?

## Escopo e seleção
Critérios confirmados pelo autor (A3/P1): incluir estudos primários, no recorte
e idiomas previstos, com texto completo, prompting aplicado a geração, tradução,
refatoração ou depuração e avaliação empírica ou estudo de caso descrito.
Testes entram quando apoiam essas tarefas.
Excluir duplicações e versões sobrepostas, textos sem detalhe técnico, tarefas fora
do escopo e trabalhos centrados apenas em treinamento ou arquitetura.
Separar preprints de publicações revisadas por pares. Priorizar a versão publicada
quando aplicável, preservando a versão lida. Fontes metodológicas e revisões podem
apoiar a fundamentação; não contar como estudos primários.

Literatura cinzenta será usada como apoio em síntese complementar, identificada por
tipo de fonte e separada do corpus empírico, sem equivalência automática com
publicações revisadas por pares. Isso recupera o tratamento explícito da análise
inicial, seção 1.5.2; não registra coleta nem acrescenta fontes de busca.

A restrição do corpus a estudos primários empíricos é evolução em relação à
proposta de TCC I, seção 4.3, que também admitia estudos secundários e propostas de
ferramentas/revisões. A análise inicial já estabelecia essa restrição. A evolução e
as explicitações desta versão constam em [decisoes.md](../contexto/decisoes.md),
D03–D07 e D10–D12. O autor confirmou os critérios; nenhuma seleção foi executada
nesta T01.

## Busca (ainda proposta)
Bases previstas: ACM Digital Library, IEEE Xplore e arXiv, além de referências e citações.
O autor informou acesso institucional a artigos apenas na rede da UFMG (A2/P5).
Consulta, exportação e textos completos não foram testados individualmente em
ACM, IEEE e arXiv. Não inferir VPN ou acesso remoto, nem disponibilidade de PDFs
a partir dos links do piloto. Registrar impedimentos por base e submetê-los ao autor
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
contexto, limitação e verificação. O autor confirmou a classificação multirrótulo e
a tabela de apoio à escolha (taxonomia e matriz), com avaliação planejada em oito
cenários, dois por tarefa (A4/P2). Essa aplicação não demonstra eficácia das técnicas
nem substitui estudo com usuários.
Para cada cenário, registrar entrada, recomendação, evidência,
ambiguidades e verificação; examinar se a orientação é localizável, justificada e
suficientemente específica, com posterior revisão do orientador (análise inicial,
seção 2.4; confirmação do autor em A4). A aplicação e a revisão ainda não
ocorreram. A revisão do orientador será ao final do trabalho (A2/A4), sem
condicionar as decisões iniciais à sua aprovação prévia. A avaliação examinará
clareza, justificativa nas fontes e orientação concreta; não medirá ganhos de
produtividade ou eficácia. A criação dos cenários e sua aplicação pertencem às
tarefas posteriores, não a T01.

## Auditoria e relato
Calcular contagens a partir dos registros efetivos, preservando denominadores.
Conferir uma amostra e divergências com autor/orientador conforme disponibilidade.
Relatar assistência por IA e limites de acesso, cobertura e revisão independente.
Não alegar dupla triagem ou concordância entre revisores sem sua realização.
Datas previstas no histórico não comprovam entrega, acesso, revisão ou agendamento.
Reexaminar a viabilidade do cronograma e preservar os prazos documentados em
`contexto/estado-atual.md` sem inventar um novo plano aprovado. A revisão do
orientador segue o momento definido pelo autor: ao final do trabalho. Sua
aprovação não foi obtida nem é presumida nesta consolidação.
