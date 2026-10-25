# Registro de decisões

| Data | Decisão | Base | Situação |
|---|---|---|---|
| 2026-10-25 | Preservar o piloto separado do corpus definitivo | Análise e ponto de controle | Aplicada à estrutura |
| 2026-10-25 | Manter corte proposto em 2026-09-07 | Análise, seção 1.2 | A confirmar em T01 |
| 2026-10-25 | Repositório privado; revisão antes da integração | Conversa com o autor | Preparado |
| 2026-10-25 | Usar esqueleto técnico até obter template oficial | Template da monografia não identificado | Pendência T03 |

Acrescentar mudanças com motivo, impacto e quem decidiu. Registrar aprovação somente
quando houver manifestação real do autor/orientador.

## Reconciliação de T01 — 25/10/2026

Registro elaborado por Codex a partir das fontes identificadas em
[estado-atual.md](estado-atual.md). Os registros iniciais acima foram preservados;
os itens abaixo detalham seu alcance. «Proposta» não significa decisão aprovada.

| ID | Natureza / responsável | Registro e motivo | Origem | Impacto / situação |
|---|---|---|---|---|
| D01 | Fato informado pelo autor, registrado na issue #1 | Nenhuma atividade do TCC realizada após 03/10/2026. A organização do ambiente não constitui avanço acadêmico. | A1, seção «Estado confirmado pelo autor em 25/10/2026» | Atualizar o estado a partir de L3 sem repetir a pergunta sobre avanços. Não confirma protocolo, banca ou defesa. |
| D02 | Delimitação proposta nos documentos do autor; confirmação atual pendente | Preservar quatro tarefas, prompting de modelos pré-treinados, português/inglês e corte em 07/09/2026, com início em 2021. | L1, seções 1.1–1.2; L2, seção 1.2; AGENTS.md | Nenhuma ampliação temporal ou temática nesta execução. Aguardar P1 e registrar motivo/impacto antes de eventual mudança. |
| D03 | Evolução metodológica documentada; aprovação não comprovada | L1, seção 4.3, admitia estudos primários ou secundários e propostas de ferramentas/revisões. L2, seção 1.5.2, restringe o corpus empírico a estudos primários com avaliação empírica ou estudo de caso suficientemente descrito. Revisões e fontes metodológicas apoiam a fundamentação e a localização de estudos. | L1, seção 4.3 → L2, seção 1.5.2 | Explicitar a restrição já herdada pelo protocolo operacional. Não contar estudos secundários como evidência primária. Confirmação em P1/P3; não é nova seleção executada. |
| D04 | Proposta herdada explicitada por Codex; confirmação pendente | Manter literatura cinzenta como síntese complementar identificada, sem equivalência automática com evidência revisada por pares. A versão inicial do protocolo operacional não explicitava esse tratamento. | L1, seção 4.2; L2, seção 1.5.2 | Restaurar a explicitação no protocolo, separando-a do corpus empírico. Não adicionar bases, consultas ou coleta nesta issue. Aguardar P1/P3. |
| D05 | Evolução de formulação, documentada em L2 | QP1 passa de «mais eficazes» em geral a eficácia sob modelos, tarefas, métricas e condições específicas; QP2/QP3 mantêm riscos/mitigações e mapeamento para tarefas. | L1, seção 4.1 → L2, seção 1.2 | Evitar ranking universal e inferência de produtividade a partir de benchmarks; formulação já herdada, ainda sem aprovação documentada. |
| D06 | Contribuição proposta nos documentos do autor; confirmação pendente | Taxonomia multirrótulo e matriz com oito cenários, dois por tarefa; avaliação de orientação localizável, justificada e específica, seguida de revisão pelo orientador. | L2, seções 1.4 e 2.4; L3 | Preservar proposta sem alegar execução, teste de eficácia ou estudo com usuários. Adequação e viabilidade dependem de P2/P3. |
| D07 | Regra metodológica herdada explicitada por Codex | Usar qualidade para apreciar a confiabilidade na síntese, sem exclusão apenas por qualidade ou nota global automática. Confirmar rubrica antes da aplicação em lote. | L1, seção 4.4; L2, seção 1.5.2; dados/README.md | Não criar limiar de exclusão, pesos ou avaliações fictícias. Nenhuma rubrica foi aplicada em T01. |
| D08 | Pendência, sem nova decisão de prazo | Metas de recuperação de L3 não foram cumpridas após 03/10, conforme A1; a viabilidade e o cronograma precisam ser revistos com o orientador. Marcação da defesa e acessos às bases continuam sem confirmação. | L3; A1; P3–P5 | Não substituir o cronograma por promessa de execução nem declarar a defesa marcada. Registrar resposta com data e responsável. |
| D09 | Organização documental por Codex, não decisão científica | Consolidar proveniência, propostas e perguntas somente nas três entregas de T01; registrar o resultado real de `make check`. | Issue #1 e inspeção R1, 25/10/2026 | Nenhuma busca, triagem, extração ou avaliação de cenário executada. Preservar dados, legado, testes e monografia; manter issue aberta enquanto houver critérios obrigatórios pendentes. |

As explicitações D03–D07 tornam visíveis escolhas e mudanças já presentes no
histórico; não registravam aprovação nova na primeira preparação do PR. Naquele
momento, nenhuma alteração de recorte, bases, critério de elegibilidade ou
contribuição havia sido autorizada. As confirmações posteriores constam abaixo.
Para alterações futuras, acrescentar data, manifestação do autor/orientador, regra
anterior, nova regra, motivo e efeito sobre buscas ou registros já produzidos.

## Confirmações do autor após as perguntas — 25/10/2026

Os registros D01–D09 descrevem a primeira preparação do PR. As respostas diretas
A2–A4, identificadas em `estado-atual.md`, atualizam as situações então pendentes:

| ID | Responsável / natureza | Decisão ou confirmação | Motivo e efeito |
|---|---|---|---|
| D10 | Autor, confirmação A3 | Manter geração, tradução, refatoração e depuração; português/inglês; 01/01/2021 a 07/09/2026; corpus primário com avaliação empírica/caso concreto, apoio secundário separado e exclusão de trabalhos apenas sobre treinamento/arquitetura. | Confirma o recorte e os critérios herdados, sem ampliar datas ou tema. Resolve P1 e as confirmações do autor em D02–D05. Não é execução de seleção. |
| D11 | Autor, decisão de fluxo A2/A4 | Decisões do trabalho tomadas pelo autor com apoio do agente; revisão do orientador ao final do trabalho. | Substitui a expectativa de aprovação prévia usada como bloqueio na primeira versão do PR. A revisão final continua necessária e futura; não representa aprovação já obtida nem nova evidência científica. |
| D12 | Autor, confirmação da proposta A4 | Adotar classificação multirrótulo e tabela de apoio à escolha, examinadas em oito exemplos (dois por tarefa) por clareza, justificativa nas fontes e orientação concreta; sem novos experimentos com LLMs nem promessa de medir ganhos de produtividade ou eficácia. | Confirma a contribuição prática herdada (D06/P2) e sua forma de avaliação, com revisão do orientador ao final. A avaliação ainda não foi executada. |
| D13 | Autor, informação de situação A2 | Defesa/marcação ainda não realizadas; detalhes de data, horário, modalidade e banca não fornecidos. | Resolve a informação de situação em P4, sem realizar o agendamento e sem inferir ausência de contatos prévios com membros da banca. |
| D14 | Autor, informação de recurso A2 | Acesso a artigos acadêmicos como estudante da UFMG apenas na rede da universidade. | Registrar a condição de acesso em P5. Não inferir VPN, acesso remoto ou disponibilidade individual de consulta/exportação/texto completo em ACM, IEEE ou arXiv. Verificação por base fica para a preparação da busca; nenhuma base foi substituída. |

A mudança de fluxo D11 tem origem na instrução atual do autor e retira a aprovação
prévia do orientador como condição para T01. Não altera critérios científicos,
cobertura ou datas. A situação das bases e da defesa agora está informada, embora
a execução da busca e a marcação permaneçam por realizar. Os quatro critérios
documentais da issue estão atendidos nesta branch; manter a issue aberta para
revisão e integração do PR, sem executar outras issues neste trabalho.
