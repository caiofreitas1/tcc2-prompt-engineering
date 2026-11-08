# Parecer sobre o texto inicial de 08/11/2026

Escopo: leitura integral e inspeção visual do PDF `build/main.pdf`, sem modificar o PDF nem a monografia.
Base: commit `0b5e1d7b636e11e92807521a5b0a2eca8c15942a`.
PDF: SHA-256 `30b28a8ac12851f4fe63b718cb04e82dbd6e302c523e51a55dd77f6101b549d2`.
Executor/data: Codex (IA), 08/11/2026. Natureza: auditoria assistida por IA; não constitui revisão humana.

## Parecer

**Utilizável com limites como texto inicial e parcial, com correções pontuais recomendadas antes do envio.**
O texto explica o problema, delimita quatro tarefas, apresenta o processo já executado e declara que a extração, a síntese e as respostas às questões de pesquisa ainda estão pendentes. A linguagem é predominantemente acadêmica e compreensível. A transparência sobre desvios, limitações e uso de IA é um ponto favorável.

A fragilidade principal é substantiva: os resultados apresentados são da operação da revisão, enquanto os resultados sobre técnicas de prompting e a contribuição prática ainda não existem. A avaliação de aceitabilidade como texto inicial não comprova atendimento às exigências da disciplina ou do orientador. Não foi conferida uma regra externa de entrega.

O roteiro fornecido pelo usuário corresponde a uma versão anterior: o arquivo atual tem **9 páginas, 11 marcações “Pendente:” e o orientador como coautor**, sem a antiga nota de orientação. As referências ocupam as páginas 8 e 9.

## Achados e correções propostas

| Prioridade | Local no PDF | Evidência e implicação | Correção proposta |
|---|---|---|---|
| Alta para o envio | p. 4, III-E, último parágrafo sobre releitura dos 12 estudos | “A adoção desse formato no lote não foi decidida; se adotado, será preciso definir quando voltar ao PDF.” As pp. 2 e 5 já relatam a adoção do texto extraído e o retorno ao PDF em dúvida ou tabela desordenada. D64 registra a decisão em 03/11. | Substituir por: “Naquele momento, a adoção desse formato no lote ainda não havia sido decidida. Em 03/11/2026, o autor o adotou, com retorno ao PDF em caso de dúvida ou de tabela desordenada.” |
| Alta para a consistência da seleção | pp. 3 e 5, aplicação de I2 e X4 | A p. 3 admite resultado obtido por prompting, sem exigir comparador; a p. 5 afasta avaliações apenas auxiliares ou usadas como comparação e admite resultados reportados e discutidos. Falta uma regra operacional que permita distinguir os casos sem depender da conclusão desejada. | Explicitar qual condição adicional torna uma avaliação de prompting elegível; distinguir avaliação comparativa elegível de presença meramente auxiliar. Usar exemplos de fronteira e verificar a aplicação consistente aos selecionados. Esta auditoria não relê os artigos e não declara incorreta nenhuma exclusão específica. |
| Alta antes da síntese | p. 7, IV-C; pp. 3–4, I4 | O próprio texto informa metadados não conferidos em 220 dos 221 incluídos e filtros de data que não implementam integralmente o corte. `dados/estudos.csv` confirma a distribuição 1/220 do campo de conferência. A falta de conferência não demonstra inelegibilidade, mas impede tratar a elegibilidade temporal como encerrada. | Qualificar a contagem como seleção atual, sujeita à conferência final dos metadados e do período. Antes da síntese, registrar primeira versão pública, data e fonte, sobretudo nos casos de 2026. Não presumir que ano da publicação seja ano da primeira versão. |
| Média para a clareza do relato | pp. 5–6, conferência humana e assistência por IA | D83 registra a declaração do autor de não usar IA na conferência. D84 registra a revisão de S314 e S373 por recomendação de Claude Code, sem nova leitura registrada. O PDF relata ambos, mas a formulação geral pode causar dúvida. | Delimitar: “O autor declarou ter realizado a conferência inicial dos textos sem IA. As revisões posteriores das decisões de S314 e S373 seguiram recomendação de Claude Code, sem nova leitura registrada.” Não apagar a participação da IA nem apresentar a declaração como observação independente. |
| Média para o envio | p. 8, conclusão | “A triagem por dois modelos de linguagem reduziu o trabalho do autor” sugere um efeito demonstrado. O procedimento restringiu a leitura humana no lote de título e resumo às exclusões, mas não há comparação do esforço total com um procedimento alternativo equivalente; houve também calibração e auditoria. | Preferir: “Na triagem por título e resumo, a conferência humana do lote concentrou-se nas exclusões consensuais dos modelos, além da triagem das amostras de calibração.” Se mantiver redução, delimitar o que foi reduzido e evitar afirmar economia líquida de tempo. |
| Média para leitores externos | p. 6, Tabela IV | Aritmética correta, mas os 1.589 retirados pelo título e os sete casos já avaliados nas amostras não aparecem explicitamente. “27 + 4” mistura duas origens e pode ser confundido com o número de inclusões humanas. | Acrescentar linha para os 1.589 fora pelo título; explicitar 92 = 85 conferências novas + 7 decisões anteriores; mostrar os 31 resgates, dos quais 27 novos e 4 anteriores, e as 61 exclusões finais. Definir resgate como encaminhamento ao texto completo, incluindo dúvidas. |
| Média para a compreensão | resumo; pp. 4 e 7, κ | As categorias e os denominadores estão descritos, mas o nome e a interpretação básica da estatística não são apresentados. | Introduzir “coeficiente κ de Cohen, que mede concordância descontando a esperada pelo acaso”. Manter explícito que não mede acurácia e que o resultado depende da comparação e das categorias. No resumo, considerar retirar parte dos números de concordância para destacar objetivo, seleção atual e pendências. |
| Média antes da execução das próximas etapas | pp. 2 e 6, pendências metodológicas | Unidade da taxonomia, unidade dos 20% da extração e procedimento dos oito cenários permanecem indefinidos. Isso afeta execução, denominador e interpretação da contribuição. | Resolver essas definições antes da extração e dos cenários. Separar essas decisões das pendências de redação de resultados. Informar o procedimento efetivamente adotado, sem substituir o registro histórico. |
| Baixa para o envio | pp. 3–5, detalhamento operacional | A metodologia ocupa grande parte do texto, com IDs, hashes, levas, restrições de ferramentas e episódios de importação. A rastreabilidade é útil, mas interrompe a descrição principal do método. | Manter no corpo critérios, decisões e desvios que afetam validade. Concentrar detalhes de execução em apêndice ou material suplementar, preservando o registro e a possibilidade de auditoria. |
| Baixa para o envio | p. 1, resumo | “Este trabalho organiza as evidências” pode antecipar a realização da síntese, embora a condição parcial seja declarada depois. | Preferir “Este trabalho tem por objetivo organizar as evidências”. O resumo já permite compreender tema, método e estado atual. |

## Conferência das afirmações pessoais e do orientador

Os registros abaixo dão rastreabilidade ao relato; não substituem o e-mail original, os eventos vividos pelo autor ou a leitura independente dos artigos.

- **Concordância com a revisão rápida e sugestão de corte de preprints:** compatíveis com D62, resposta do orientador relatada pelo autor em 03/11. A adoção pelo autor está em D64. D62 não registra aprovação integral da metodologia ou do texto.
- **Tempo de cerca de 12 h 30 min nos primeiros 230 estudos:** compatível com D78, explicitamente como informação do autor. O PDF distingue corretamente esse tempo retrospectivo do cronômetro do formulário. Não se trata de uma medição independente.
- **S314 e S373:** a redação sobre revisão por recomendação de IA, sem nova leitura registrada, é compatível com D84. Recomenda-se reler os trechos relevantes antes de sustentar as exclusões na defesa e verificar a consistência de X4.
- **Ausência de IA na conferência inicial:** D83 contém a declaração do autor. A auditoria não pode comprovar ausência de uso de ferramentas; deve preservá-la como declaração e delimitar as revisões posteriores.
- **Coautoria do orientador:** corresponde à instrução do autor registrada em D88. A antiga orientação sobre conferir o nome em nota está desatualizada. D88 não registra manifestação do orientador sobre a coautoria.

## Contagens e estatísticas

Recontagem a partir de `dados/triagem.csv`, `dados/estudos.csv` e das tabelas de execução. As 23 contagens recalculadas por `scripts/contar_fluxos.py` coincidiram com as linhas correspondentes em `dados/fluxos.csv`; o script foi utilizado sem `--gravar`.

| Reconciliação | Resultado |
|---|---:|
| Registros das três bases | 1.597 + 665 + 482 = 2.744 |
| Após agrupamento de redundâncias | 2.744 − 440 = 2.304 |
| Restrição de tarefa no título | 2.304 − 1.589 = 715 |
| Triagem por título e resumo | 623 seguem + 92 exclusões consensuais = 715 |
| Encaminhados ao texto completo | 623 + 27 + 4 = 654 |
| Distribuição em etapas | 310 + 233 + 111 = 654 |
| Situação da etapa 1 | 256 lidos + 53 a ler + 1 excluído sem leitura dos modelos = 310 |
| Decisões humanas nos 256 | 221 incluir + 5 dúvida + 30 excluir = 256 |

Recálculo independente do κ pelas frequências marginais, preservando a última decisão de cada responsável por estudo:

| Comparação | N | Decisões iguais | κ recalculado | κ no PDF |
|---|---:|---:|---:|---:|
| Título/resumo, IA-A × IA-B | 715 | 602 | 0,726009 | 0,726 |
| Texto completo, IA-A × IA-B | 256 | 235 | 0,792585 | 0,793 |
| Texto completo, autor × IA-A | 256 | 230 | 0,664668 | 0,665 |
| Texto completo, autor × IA-B | 256 | 216 | 0,556018 | 0,556 |

Os quatro resgates de exclusões consensuais no texto completo são S398, S1034, S1280 e S1359. S2148 permanece fora dos denominadores de concordância dos 256 textos. Não foram recalculadas nesta auditoria as estatísticas históricas das duas amostras de calibração a partir dos arquivos selados.

A perda potencial de 46 dos 79 incluídos das amostras pelo filtro de título deve continuar visível. Ela não estima uma perda de 58% em toda a literatura; descreve esses casos das amostras. É um limite central do alcance da revisão, mesmo que o corpus resultante seja numeroso.

## Linguagem, compreensão e forma

O texto soa acadêmico, sem depender de vocabulário desnecessariamente rebuscado. Introdução, objetivos e definições das quatro tarefas ajudam o leitor externo. O principal ganho editorial virá de encurtar a narrativa operacional e reduzir repetições entre método, resultados, ameaças e conclusão.

Para a defesa, convém saber explicar sem ler o texto:

1. A regra de união encaminha um estudo se ao menos um modelo responde incluir ou dúvida; as duas exclusões não impedem o resgate humano previsto.
2. κ quantifica concordância, não prova que a classificação esteja correta.
3. O limite de X4 precisa distinguir com consistência os estudos que avaliam prompting daqueles em que sua presença é apenas auxiliar.
4. Os oito cenários permitem examinar clareza e apoio nas fontes; não demonstram eficácia das técnicas ou utilidade com usuários.
5. Os resultados atuais descrevem seleção e concordância; as respostas sobre técnicas, riscos e taxonomia dependem da extração e síntese.

As nove páginas foram renderizadas e inspecionadas. Não foram observados cortes de texto, sobreposição ou tabelas ultrapassando as colunas. As tabelas usam fonte menor, ainda legível na renderização inspecionada. A página 9 contém apenas as três últimas referências; é uma oportunidade de ajuste de paginação posterior, sem prioridade sobre conteúdo. O título é compreensível, embora as quatro tarefas sejam mais específicas que “codificação e implementação”.

Foram encontradas 24 entradas bibliográficas e todas têm chamada no texto; não foi encontrada chamada numérica sem entrada. A bibliografia usa versões específicas do arXiv em vários casos, o que exige preservar a distinção entre ano da versão consultada e primeira divulgação. **Esta checagem é formal; não valida autores, datas, metadados ou sustentação das 24 fontes.** Não houve releitura dos originais nesta auditoria. A correspondência entre a rubrica e suas fontes continua explicitamente pendente.

Recomendação sobre as pendências: **manter as 11 marcações em vermelho**, conforme solicitado. Elas comunicam o estado parcial e não devem ser apagadas para sugerir conclusão. A prioridade é resolver a contradição temporal e as ambiguidades metodológicas, não trocar a cor.

## Validação e limites

- `make check`: **zero erros estruturais e 44 testes aprovados**. O resultado não certifica validade científica nem aceitabilidade acadêmica.
- PDF e fontes LaTeX preservados; nenhum dado científico ou decisão humana foi alterado.
- Não foi executado `make pdf`, pois não houve edição da monografia, nem `make release-check`, pois a tarefa é avaliar uma versão declaradamente parcial.
- Persistem para 18/11 a leitura de 53 + 111 = 164 estudos, além das demais etapas. A quantidade já incluída torna a extração, a conferência e a síntese uma preocupação de viabilidade. Esta auditoria não estima horas necessárias nem garante conclusão no prazo.
- Os registros internos sustentam a coerência documental das declarações, sem comprovar sua execução real. A ausência de outros erros identificados não certifica a completude da revisão.
