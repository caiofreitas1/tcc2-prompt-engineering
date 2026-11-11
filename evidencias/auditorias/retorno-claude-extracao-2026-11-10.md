# Parecer sobre o retorno do Claude à proposta de extração

Escopo/commit: retorno transcrito pelo autor em 10/11/2026; arquivos locais no commit `95c2597`, com o parecer anterior ainda não versionado. Este documento analisa a proposta, sem registrar sua aprovação pelo autor nem executar a extração.

Executor/data/ferramenta: Codex (IA), 10/11/2026, leitura do protocolo, contratos, verificador, scripts e contagem direta do cadastro; skill local `tcc-auditar-ciencia`.

Natureza: revisão assistida por IA da coerência metodológica e do planejamento. Sem conferência de resultados de artigos, auditoria da conta do Claude ou medição de tempos.

Parecer: **retorno majoritariamente adequado, com correções localizadas antes da extração em escala**. Há melhora na definição da conferência humana e na explicitação da dependência dos metadados. Permanecem contradição na regra de seleção, confiança excessiva na automação e ambiguidades no orçamento de horas.

## Achados

| Gravidade | Trecho do retorno | Evidência e avaliação | Correção concreta |
|---|---|---|---|
| Alta | Selecionar comparações “sem olhar o tamanho do efeito”, mas incluir outro modelo “em que o efeito desaparece ou se inverte” | A terceira prioridade consulta a direção ou presença do efeito para escolher o resultado. Isso contradiz a descrição de seleção independente dos resultados. Preservar contradições é apropriado, mas deve ser distinguido da seleção primária. A formulação anterior do Codex sobre condições que alteram a interpretação também precisava dessa distinção. | Selecionar o núcleo por características previamente definidas de tarefa, técnica, modelo, benchmark e métrica. Registrar reversões, resultados nulos e outros achados discrepantes em busca complementar de heterogeneidade, explicitamente identificada, sem apresentar esse conjunto como amostra neutra dos resultados disponíveis. |
| Média | Prioridades 1 e 2: principal declarado pelo estudo e tarefas ainda não cobertas | Não há desempate quando o artigo não declara benchmark/métrica principais ou tem vários resultados principais. Cobrir tarefas não garante cobrir técnicas focais distintas na mesma tarefa. | Definir regra de desempate no instrumento e verificar a cobertura das técnicas focais. Quando alguma técnica ficar apenas classificada, registrar a ausência de extração numérica e não atribuir a ela a eficácia de outra técnica ou de um pacote não isolado. Três continua sendo alvo com exceções documentadas. |
| Média | Metadados e I4 são “pré-requisito da extração, e não uma tarefa paralela” | `scripts/verificar.py`, linhas 136–141, exige `metadados_conferidos=sim` para cada registro com `status=conferido_original`; o código aceita rascunhos `nao_conferido`. A dependência vale por estudo, sem exigir conclusão prévia dos 305 restantes para liberar um lote já verificado. I4 é requisito substantivo de elegibilidade, mas a linha 140 não calcula a primeira data pública. | Conferir identidade, versão e elegibilidade temporal de cada estudo antes de validar e usar sua extração. É possível trabalhar por lotes: metadados e I4 do lote, extração, conferência. Não substituir evidência pela simples mudança de uma flag. A análise anterior do Codex incluía o esforço dos metadados, mas não explicitava essa dependência por registro. |
| Média | A conferência é feita “quase toda por script”, “custa pouco” e pode terminar antes de 11/11 | O retorno não apresenta piloto, cobertura das fontes, rotina executada, lista de exceções ou medição que sustente essas previsões. Scripts podem recuperar e comparar informações, mas correspondência entre versões e primeira disponibilidade pública exigem tratamento explícito das ambiguidades. | Automatizar os casos com evidência suficiente, guardar fontes e datas recuperadas e separar pendências. Medir uma pequena amostra antes de prometer duração. Não confundir ano de publicação, data de atualização ou registro de DOI com a primeira versão pública prevista em I4. |
| Média | Total de “12 a 17 horas” e linhas separadas para dez fichas do piloto e 62 fichas | A soma literal das parcelas numéricas informadas é 11–16 horas: 2 + 1 + (1–2) + (6–10) + 1. Não inclui conferir as afirmações, revisar o texto ou eventuais exceções dos metadados. Os dez estudos do piloto podem estar contidos nos 62. | Apresentar subtotal, trabalho ainda não estimado e eventual margem em separado. Contar o piloto dentro dos 20% se os estudos integrarem o corpus final e as fichas tiverem sido conferidas integralmente na versão final do instrumento. Nesse caso, com N=306, faltariam 52 fichas adicionais. Recalcular se houver mudança de corpus ou retrabalho após o piloto. |
| Baixa | Renovação do limite em 11/11 “verificada na sua conta” | É relato de verificação pelo Claude, sem evidência de conta consultada nesta auditoria. Não há razão documental aqui para invalidá-lo, mas ele não é uma verificação independente do Codex. | Atribuir a informação ao responsável pela consulta. A presente análise não exige repetir essa consulta para avaliar a metodologia. |

## Regra operacional recomendada

1. Seleção primária: identificar as avaliações centrais das técnicas elegíveis e suas tarefas. Usar resultado, benchmark e métrica explicitamente declarados como principais quando existirem; definir um desempate reproduzível para ausência ou multiplicidade de principais. A escolha dentro dessa regra não depende de ganho, perda, significância ou tamanho de efeito.
2. Cobertura: verificar se as técnicas focais e tarefas relevantes estão representadas; documentar o que ficar apenas na classificação e o que for extraído numericamente. Não inventar comparação em estudo sem comparador.
3. Complemento: procurar e registrar limitações, resultados nulos, reversões e condições discrepantes reportadas no artigo. Identificar esse complemento como análise de heterogeneidade. Ele pode justificar exceções ao alvo de três, mas não autoriza calcular uma proporção de sucessos como se a seleção fosse exaustiva ou aleatória.
4. Calibração: definir a regra candidata antes do piloto e congelar a versão operacional depois da calibração. Se o piloto mudar o instrumento, reaplicar as mudanças aos seus dez estudos antes de contá-los entre os conferidos.

## Contagens e planejamento

Nova leitura de `dados/estudos.csv` em 10/11: 306 incluídos provisórios; um registro com `metadados_conferidos=sim` e 305 com `nao`. A amostra por estudo continua em 62 para esse N. As pendências da triagem e a conferência do período podem alterar o denominador. O custo humano das afirmações do texto permanece sem estimativa; não se pode apresentar 11–16 ou 12–17 horas como total fechado.

O conflito entre revisão humana de 100% no modo de entrega e amostragem no protocolo permanece real (`scripts/verificar.py`, linhas 258–265; protocolo, seção 7). O retorno o reconhece corretamente. A correção deve implementar o procedimento efetivamente adotado, mantendo identidade e data das revisões reais, cobertura da amostra e conferência de todas as afirmações finais. Este parecer não modifica a barreira de entrega.

## Fontes e limites

- `protocolo/protocolo.md`, seção 3: I4 exige primeira versão pública entre 01/01/2021 e 07/09/2026, permitindo versão lida posterior; seções 7 e 9–11: conferência, extração e síntese.
- `dados/README.md`, contratos de estudo e extração; `scripts/verificar.py`, linhas 118–159 e 258–265.
- Parecer anterior em `evidencias/auditorias/proposta-extracao-2026-11-09.md` e retorno transcrito no chat.
- A [documentação oficial da API do arXiv, seção 3.3.2.1](https://info.arxiv.org/help/api/user-manual.html) distingue `published`, referente à primeira versão submetida e processada, de `updated`, referente à versão recuperada. Essa distinção ilustra a necessidade de identificar a semântica da data usada; não comprova, sozinha, a primeira disponibilidade em outros canais.

A promessa de baixo custo da automação, os tempos humanos e a renovação da conta não foram verificados. Nenhuma classificação de estudo, número de artigo, prompt, protocolo ou revisão humana foi alterado.

## Verificação técnica

`make check`: zero erros estruturais e 44 testes aprovados (saída 0). `git diff --check` também passou. A única adição desta revisão é este parecer; o parecer anterior foi preservado. A verificação estrutural não certifica validade científica nem viabilidade do cronograma.

## Fechamento após a nova proposta do Claude

O autor encaminhou, ainda em 10/11/2026, uma nova resposta do Claude que incorpora a separação entre seleção principal e complemento de heterogeneidade, propõe desempate pela ordem de apresentação e confirma o fluxo por lotes. **A proposta está suficientemente definida para ser registrada e aplicada no piloto**, com as seguintes precisões na redação dos instrumentos:

- O desempate pela primeira tabela, métrica e modelo é usado quando não há principal explicitamente declarado ou quando restam principais empatados. Considerar a primeira tabela com resultados elegíveis de prompting para tarefas do escopo e a primeira métrica pertinente à comparação; tabelas descritivas e condições incompatíveis não satisfazem a regra. A ordem de apresentação torna a seleção reproduzível, sem garantir representatividade.
- Escrever `max(10, teto(0,20 × N))`, com N igual ao número final de estudos incluídos. Manter a prioridade das fichas que sustentam afirmações, além da distribuição por tarefas e técnicas; manter também a conferência de cada afirmação final no original.
- Ao registrar a decisão, sincronizar as seções 7 e 9 do protocolo e os contratos de dados afetados, além do registro de decisões e do prompt. A ex-v2 começa como versão de piloto e só é congelada após sua calibração. No estado local consultado, esses documentos ainda descrevem o procedimento anterior.

O ajuste da barreira de entrega pode ser uma tarefa separada do piloto, desde que concluído antes da entrega e aderente ao procedimento adotado. A aprovação metodológica deste parecer não registra uma decisão do autor nem confirma revisão humana de qualquer ficha.

Nesta releitura não houve alteração de código ou dados. A validação estrutural e `git diff --check` foram repetidos; a suíte de 44 testes já registrada acima corresponde ao mesmo código e não foi repetida para este adendo documental.
