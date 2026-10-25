---
name: tcc-extrair-evidencias
description: "Extrair métodos, resultados e limitações de artigos primários para a RSL do TCC, com versão e localizadores. Usar em fichamentos e conferência do piloto; não transformar documentos anteriores ou resumos em evidências verificadas."
---

# tcc-extrair-evidencias

Ler AGENTS.md, protocolo/protocolo.md e dados/README.md na raiz do projeto ativo.
Identificar estudo e versão; abrir o texto primário completo e preservar sua referência.
Se houver apenas relatório anterior, resumo ou snippet, registrar fonte_indisponivel
ou nao_conferido; não promover seus números para conferido_original. Explicitar o acesso faltante.
Conferir metadados e preencher dados/estudos.csv somente com o que foi consultado.
Criar fichamento em evidencias/ usando evidencias/modelos/fichamento.md e registrar
comparações independentes em dados/extracoes.jsonl. Incluir todos os campos do contrato.
Para cada resultado, registrar métrica, escala, baseline, intervenção, denominador quando
aplicável, tabela/seção/página, arquivo primário e versão; separar tarefas e benchmarks.
Preservar amostragem, tentativas, orçamento, ferramentas e testes; pass@1 não significa
uma única interação com o modelo. Não inferir produtividade a partir de acurácia.
Recalcular derivados em script ou conta reproduzível: diferença em p.p. = final - inicial;
variação relativa (%) = 100 * (final - inicial) / inicial, somente com inicial diferente de zero.
Marcar divergências entre texto e tabela sem decidir arbitrariamente qual é correta.
Usar nao_informado apenas após conferir a fonte; manter revisão humana pendente até
manifestação real do revisor. Entregar fichamento, registros, lacunas e executar make check.
