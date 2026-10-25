# Protocolo operacional — versão herdada para confirmação

**Situação:** derivado da análise inicial; não equivale a aprovação do orientador.
**Recorte proposto:** 2021-01-01 a 2026-09-07, português ou inglês.
Registrar qualquer mudança em contexto/decisoes.md antes de aplicá-la.

## Questões
- QP1: quais técnicas são avaliadas e que evidências de eficácia são apresentadas,
  sob quais modelos, tarefas, métricas e condições?
- QP2: quais riscos técnicos são identificados e quais estratégias de mitigação
  são propostas ou avaliadas?
- QP3: como relacionar técnicas, tarefas e condições em uma taxonomia útil?

## Escopo e seleção
Incluir estudos primários, no recorte e idiomas previstos, com texto completo,
prompting aplicado a geração, tradução, refatoração ou depuração e avaliação empírica
ou estudo de caso descrito. Testes entram quando apoiam essas tarefas.
Excluir duplicações e versões sobrepostas, textos sem detalhe técnico, tarefas fora
do escopo e trabalhos centrados apenas em treinamento ou arquitetura.
Separar preprints de publicações revisadas por pares. Priorizar a versão publicada
quando aplicável, preservando a versão lida. Fontes metodológicas e revisões podem
apoiar a fundamentação; não contar como estudos primários.

## Busca (ainda proposta)
Bases previstas: ACM Digital Library, IEEE Xplore e arXiv, além de referências e citações.
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

## Síntese e contribuição prática
Agrupar por tarefa e mecanismo, aceitando múltiplos rótulos. Não ranquear técnicas
por resultados de estudos incompatíveis. Identificar resultados medidos, inferências
do TCC e sugestões dos autores. A matriz candidata deve ligar orientação a evidência,
contexto, limitação e verificação. Oito cenários (dois por tarefa) permanecem planejados;
sua aplicação não demonstra eficácia das técnicas nem substitui estudo com usuários.

## Auditoria e relato
Calcular contagens a partir dos registros efetivos, preservando denominadores.
Conferir uma amostra e divergências com autor/orientador conforme disponibilidade.
Relatar assistência por IA e limites de acesso, cobertura e revisão independente.
Não alegar dupla triagem ou concordância entre revisores sem sua realização.
