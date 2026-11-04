# Reavaliação do esboço após as alterações

**Parecer: o relato está substancialmente mais fiel ao trabalho realizado. Nove dos 13 achados anteriores estão resolvidos no texto; quatro estão parcialmente atendidos, com pendências corretamente declaradas.** Não identifiquei novo erro nas contagens ou nos cálculos apresentados. A metodologia ainda não está fechada para execução em lote, principalmente pela interpretação de I2 e pelo encaminhamento dos estudos históricos.

Escopo/commit: PDF de seis páginas, confrontado com a fonte LaTeX, os registros e a auditoria anterior, na revisão `a52d24291a280bcfe35fe5c2ad26a00229a47af3`. [PDF analisado](../../build/main.pdf); [fonte da metodologia](../../monografia/capitulos/03-metodologia.tex); [apêndice de busca](../../monografia/capitulos/07-apendice-busca.tex); [parecer anterior](T10-esboco-PDF-2026-11-03.md).

Executor/data/ferramenta: Codex, auditoria assistida por IA em 03/11/2026, data do autor em America/Sao_Paulo. Leitura integral do PDF, extração com pypdf, renderização com Poppler e inspeção das seis páginas; comparação de alterações com Git; consultas a fontes primárias para conferir referências e correções conceituais. Não constitui revisão humana independente.

Identidade do PDF: SHA-256 `fa8e4b7b4db6421f52eb7e848ba58e1dc3069df5ba128d3810e1c098b2f42203`; criação registrada em 03/11/2026 às 21:37:53, UTC−03. O PDF corresponde ao conteúdo atualizado inspecionado, incluindo o apêndice e as quatro referências acrescentadas.

## 1. Situação dos achados anteriores

“Resolvido” nesta tabela significa que a falha de relato identificada foi corrigida; não certifica a validade científica de toda a revisão ou a execução de etapas futuras.

| Achado | Situação | O que mudou / o que falta |
|---|---|---|
| M01 — 2.304 estudos e 2.300 candidatos | Parcialmente atendido | Agora explica os quatro históricos, nomeia os seis estudos e esclarece que não foram incluídos nem excluídos. Falta decidir e implementar o encaminhamento posterior dos quatro e dos dois não recuperados |
| M02 — interpretação de I2 | Parcialmente atendido | A diferença entre protocolo e tc-v1 está explícita, com os casos S2261, S306 e S2128. A interpretação continua pendente; o artigo não a apresenta como resolvida |
| M03 — reconstrução da busca | Parcialmente atendido | Apêndice com expressão geral e filtros, fiel ao protocolo. As sintaxes exatas continuam remetidas ao CSV privado, sem meio de acesso definido para a banca |
| M04 — projeção de esforço | Resolvido no relato | Explicita 38/50, 1.748 textos, aproximadamente 1.515 conferências e custos não cobertos; distingue estimativa central de impossibilidade demonstrada |
| M05 — teste com texto extraído | Resolvido no relato | Relata a releitura, reduções registradas de tokens, três mudanças de IA-B e impossibilidade de separar efeito de formato da variação entre execuções |
| M06 — IA na conferência humana | Resolvido | Incorpora a declaração do autor de 03/11, mantendo a natureza retrospectiva dos três minutos |
| M07 — κ e dúvidas eliminadas | Resolvido | Define a codificação binária, mantém κ de três categorias entre modelos, mostra 67/100 e 38/50 e explica as dúvidas consensualmente excluídas |
| M08 — independência e alteração de X4 | Resolvido no relato | Explica contextos separados, mudança de IA-A e limite probatório do hash; tr-v2 é descrito como explicitação da regra de X4 |
| M09 — datas IEEE/ACM | Resolvido no relato | Acrescenta os 196 registros IEEE de 2026; substitui existência exclusiva na ACM por recuperação apenas nessa base; reconhece conferências de data pendentes |
| M10 — extração, qualidade e cenários | Parcialmente atendido | Descreve campos, lacunas e julgamentos; reconhece seleção dirigida. Faltam unidade dos 20%, responsáveis operacionais, conferência da rubrica e procedimento completo dos cenários |
| M11 — extrações anteriores de S1 | Resolvido | Distingue E1–E2 de calibração da extração do corpus definitivo, que não começou |
| M12 — coleta e denominadores | Resolvido no relato | Explica seis cursos IEEE, limite da coleta ACM, preservação dos registros e 2.298 resumos entre os 2.304 estudos |
| M13 — snowballing | Resolvido no relato | Identifica rodada única nas duas direções, OpenAlex e ausência de busca até saturação |

Também foram atendidos os ajustes de introdução: Codex/Copilot situado historicamente em 2021; expectativa de utilidade apresentada como motivação; distinção entre experimentos de eficácia nas tarefas e avaliação operacional das IAs na revisão. Na fundamentação, a relação entre few-shot e aprendizado em contexto foi esclarecida, e a descrição de chain-of-thought foi delimitada à formulação citada.

## 2. Pontos que ainda exigem atenção

### R01 — I2 está descrito com honestidade, mas precisa ser decidido antes do lote

**Gravidade: alta para a execução futura; não é nova falsidade do PDF.** Localizador: Seção III-B, pp. 2–3; fonte, linhas 32–41; proposta D58 em [decisoes.md](../../contexto/decisoes.md).

O texto atualizado não esconde a indefinição. Isso corrige a descrição do estágio real. A pendência, porém, não substitui a regra operacional necessária para aplicar I2 de forma consistente. A próxima versão precisa fixar se entram estudos observacionais, se há exigência de comparador e qual resultado torna elegível o código produzido como etapa intermediária. Depois, reexaminar casos afetados e versionar os prompts e registros pertinentes.

**Ressalva nova à proposta D58:** ela sugere excluir como X4 toda intervenção avaliada que não seja prompting, sem criar código novo. O X4 vigente se refere apenas a treinamento, ajuste fino ou arquitetura. A proposta é mais ampla: decodificação, por exemplo, não cabe necessariamente nesses três termos.

Se adotada, essa solução precisa de revisão explícita da definição de X4 no protocolo, na tabela de critérios, nos prompts e no contrato dos dados, com tratamento dos pareceres históricos. Outra solução é definir um motivo/código próprio. A escolha depende da decisão metodológica; não deve ser implementada apenas trocando o código de S2128. **D58 ainda é proposta e o PDF não afirma que ela já foi aplicada.**

### R02 — o encaminhamento dos estudos conhecidos permanece aberto

**Gravidade: alta para fechar o fluxo de seleção.** Localizador: III-C, p. 3; fonte, linhas 97–109.

A explicação de 2.304 para 2.300 está correta. Os dados continuam com seis estudos históricos e 2.300 candidatos; nenhum está no corpus definitivo. A proposta de submeter os quatro recuperados às mesmas regras de elegibilidade evita inclusão automática. Ainda é preciso registrar a decisão e executá-la.

Os IDs dos estudos não recuperados já são conhecidos. Caso sejam considerados por conhecimento prévio, registrar essa origem e sua contagem; não atribuir retroativamente a descoberta ao snowballing. Caso não sejam considerados, documentar a decisão e sua justificativa. O fluxo final precisa reconciliar todos esses caminhos.

**Ajuste pequeno de redação:** em vez de “seus resumos não trazem todos os termos exigidos pela expressão” (linha 106), preferir “título e resumo não satisfazem a combinação dos três blocos da expressão”. Há alternativas OR dentro de cada bloco; a busca não exige todos os termos individualmente.

### R03 — o apêndice melhora a reprodução, mas ainda depende de material privado

**Gravidade: média no esboço; necessária resolução antes da entrega.** Localizador: Apêndice A, p. 5, linhas 15–18 da fonte; III-H, linhas 258–259.

A expressão geral e os filtros estão coerentes com o protocolo. O apêndice explica a diferença temporal entre bases. Entretanto, o caminho `dados/buscas.csv` não é um endereço acessível ao leitor, e o apêndice não contém as consultas completas específicas de cada interface.

Pode-se resolver com suplemento contendo as três consultas exatas e os prompts, ou com pacote/repositório acessível à banca e uma referência inequívoca à versão entregue. Não há necessidade de tornar o projeto público. A pendência reconhecida no PDF é adequada, mas M03 só será encerrado quando existir um caminho de consulta verificável.

### R04 — extração e avaliação de qualidade ainda precisam de executor e unidade

**Gravidade: média.** Localizador: III-F, p. 5; fonte, linhas 226–237; [contrato dos dados](../../dados/README.md).

O texto avançou ao listar campos, estados de lacuna e julgamentos da qualidade e ao reconhecer que a conferência prioritária não estima taxa geral de erro. Permanecem dois componentes de M10:

1. A unidade dos 20%: estudos, fichas, comparações ou registros de extração. Esses denominadores produzem cargas e coberturas distintas.
2. Quem realiza a extração inicial e quem aplica a rubrica; se haverá um ou dois modelos, como divergências serão tratadas e qual será a conferência humana da qualidade.

Listar os executores gerais em III-H não define esses procedimentos futuros. Convém registrá-los na metodologia ou em protocolo/suplemento acessível. A origem dos itens da rubrica segue explicitamente pendente de conferência nos textos primários. Não a tratar como instrumento validado apenas por citar Dybå/Dingsøyr e Sallou et al.

### R05 — o procedimento dos cenários ainda não está pronto para aplicação

**Gravidade: média.** Localizador: III-G, p. 5; fonte, linhas 239–247.

O artigo agora promete registrar origem, entrada, saída, evidência e verificação, e declara corretamente que esse exame não mede eficácia. Ainda faltam a origem e seleção dos casos, quem os constrói e examina, o registro dos julgamentos de clareza/justificativa/orientação e o procedimento de alteração da matriz. A pendência é legítima; precisa ser resolvida antes da aplicação, para não definir o sucesso depois de observar os resultados.

## 3. Conferências adicionais do relato atualizado

**Dados e execução.** Não houve alteração de dados, scripts ou protocolo entre `a063d7e` e `a52d242`. As recontagens da primeira auditoria continuam aplicáveis à mesma base. Nesta rodada, reconferi o estado do corpus e o novo detalhamento dos 12 textos: zero linhas de triagem principal e de qualidade; seis `piloto` e 2.300 `candidato`; decisões humanas de nove incluir, duas excluir e uma dúvida. As contagens acrescentadas ao artigo correspondem aos registros, sem transformação dos 12 em corpus definitivo.

**Projeções.** O encadeamento das 77 h e das 27 h está agora suficientemente explicado para avaliar seu alcance. A inclusão de indisponibilidade não descontada, seleção dos 12 apenas entre textos com indicação de acesso e mistura das duas versões do prompt impede que a projeção pareça uma medição geral. Não é necessário repetir no corpo todo o cálculo do relatório de viabilidade; preservar as hipóteses já expostas é suficiente.

**Formulário e orientação de I2.** O novo texto informa que o formulário exibiu ao autor a orientação de tc-v1. Isso é compatível com ausência de IA na leitura: receber uma instrução metodológica no formulário não é usar IA para resumir o artigo ou redigir os motivos. Também é compatível com cegamento aos pareceres. O acréscimo reconhece uma possível influência na interpretação do critério.

Limite de verificação: esse conteúdo do formulário é documentado em D57, mas não encontrei uma cópia local de seu código/exportação para conferi-lo independentemente. Para fechar a rastreabilidade, preservar o formulário e suas instruções na versão usada, se disponível. Não concluí que a orientação causou alguma decisão específica.

**Números de tokens.** Os 40% e 60% são apresentados como consumo registrado e coincidem com o relato de D55. Nesta auditoria não foram obtidos logs de telemetria nem repetidas as execuções. A afirmação de três mudanças de IA-B permanece sustentada pelos pareceres brutos já comparados. A cautela quanto à atribuição causal das mudanças está correta.

## 4. Referências acrescentadas e correções conceituais

Conferi título, autores e ano/versão dos novos registros usados para identificar o conjunto de referência nas páginas primárias:

- S3: [arXiv 2303.11366v4](https://arxiv.org/abs/2303.11366v4), Shinn, Cassano, Berman, Gopinath, Narasimhan e Yao, versão de 2023.
- S4: [arXiv 2411.02320v1](https://arxiv.org/abs/2411.02320v1), Cordeiro, Noei e Zou, 2024.
- S5: [arXiv 2211.03622v3](https://arxiv.org/abs/2211.03622v3), Perry, Srivastava, Kumar e Boneh, versão de 2023. O identificador iniciado em 2211 não torna errado o ano da versão citada.
- S6: [registro da editora Dagstuhl](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2025.35), Yeo, Hwang e Ma, ECOOP 2025. Os dados essenciais conferem; como ajuste bibliográfico, usar o tipo `inproceedings` e acrescentar volume 333 e páginas 35:1–35:25, disponíveis no BibTeX oficial, em vez de cadastrar o artigo apenas como `misc`.

Essa conferência identifica os trabalhos; não constitui nova extração ou validação de seus resultados científicos.

O trecho histórico sobre Codex/Copilot encontra suporte no resumo de [Chen et al., v2 de 2021](https://arxiv.org/html/2107.03374v2). A distinção atual entre few-shot e aprendizado em contexto está de acordo com a apresentação de zero-, one- e few-shot em [Brown et al., seção 1 e nota terminológica](https://arxiv.org/html/2005.14165v4). As correções não introduziram resultados desses estudos no corpus da revisão.

## 5. Organização e apresentação

As três tabelas agora aparecem próximas dos trechos que as apresentam. O problema anterior das tabelas interrompendo o parágrafo inicial da metodologia foi resolvido. A tabela de calibração aparece na própria subseção III-E. Não identifiquei texto cortado, tabelas sobrepostas ou caracteres ilegíveis nas seis páginas. O log de compilação inspecionado não contém ocorrências de warning, overfull, underfull ou referências indefinidas.

A metodologia cresceu de aproximadamente 1.593 para 2.861 palavras por contagem bruta da fonte, incluindo comandos e pendências. O crescimento atende à auditoria, mas a versão final pode ficar mais enxuta depois das decisões: há várias explicações sobre o que ainda não foi definido e referências a IDs internos. Preservar as limitações científicas, mas concentrar cronologia detalhada, hashes, exemplos de adjudicação e registros extensos no suplemento, quando isso mantiver o método compreensível no artigo.

A prioridade atual não é acrescentar mais ressalvas ao texto. É tomar as decisões metodológicas restantes, registrá-las e substituir as pendências por procedimentos determinados. Resumo, resultados, discussão e conclusão continuam em elaboração; sua condição de pendência é compatível com o estado documentado.

## 6. Verificação e conclusão

`make check` executado nesta rodada: **zero erros estruturais e 32 testes aprovados**. Não foram alterados LaTeX, PDF, dados, critérios ou propostas. Este arquivo registra a reavaliação; o primeiro parecer foi preservado como histórico.

**Parecer final: adequado como esboço do estágio real, com os limites declarados. Ainda não adequado como metodologia definitiva para iniciar o lote ou como artigo concluído.** Os pontos de maior prioridade são a decisão operacional de I2 e o encaminhamento dos estudos conhecidos; em seguida, completar extração/qualidade/cenários e o acesso da banca aos materiais.
