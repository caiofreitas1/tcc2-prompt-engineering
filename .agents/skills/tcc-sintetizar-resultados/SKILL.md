---
name: tcc-sintetizar-resultados
description: "Sintetizar extrações conferidas da RSL por tarefa, técnica e contexto, construindo taxonomia e matriz rastreáveis. Usar após extração; não usar para inventar corpus ou ranquear resultados incompatíveis."
---

# tcc-sintetizar-resultados

Ler AGENTS.md, protocolo/protocolo.md e dados/README.md na raiz do projeto ativo.
Selecionar extrações conferido_original; separar piloto e corpus definitivo, preprints e
publicações revisadas. Informar as revisões humanas ainda pendentes.
Montar grupos por tarefa, mecanismo de prompting, modelo, benchmark, métrica e orçamento.
Tratar categorias combináveis como multirrótulo; distinguir técnica, recurso e processo.
Comparar números apenas em condições justificadamente compatíveis. Não calcular média
de pass@1 entre benchmarks/modelos nem tratar pontos percentuais como ganho relativo.
Preservar resultados negativos e contraditórios. Separar efeito observado, interpretação
do TCC e hipótese; não atribuir causalidade ou significância sem suporte no estudo.
Criar síntese em evidencias/sinteses/ com IDs das extrações, contexto, limites e lacunas.
Propor regras da matriz com entrada, recomendação candidata, base, limitações e verificação.
Não chamar os oito cenários planejados de validação de eficácia. Registrar sua aplicação
somente quando executada. Entregar resposta provisória a cada QP e executar make check.
