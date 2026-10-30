# Estado documentado em 25/10/2026 — T01 / issue #1

**Situação:** reconciliação documental por Codex e decisões confirmadas pelo autor
em 25/10/2026. Os critérios documentais de T01 estão atendidos nesta branch para
revisão por PR. Recorte, critérios e contribuição prática foram confirmados pelo
autor; o orientador revisará o trabalho ao final, conforme fluxo definido pelo
autor. Essa revisão ainda não ocorreu.

## Origens e alcance

| ID | Origem | Alcance |
|---|---|---|
| L1 | [Proposta de TCC I](../fontes/legado/proposta-tcc1.txt), 29/11/2025, seções 1.1–1.2 e 4 | Objetivo, escopo e método originalmente propostos. |
| L2 | [Análise inicial](../fontes/legado/analise-inicial.txt), 07/09/2026, versão modificada em 08/09, seções 1.2–1.5, 2.4–2.6 e Apêndice A | Relato do piloto e protocolo proposto; não comprova execução posterior. |
| L3 | [Ponto de controle](../fontes/legado/ponto-de-controle.txt), 03/10/2026, campo «Estado atual» | Estágio declarado pelo aluno e plano de recuperação; não comprova cumprimento das metas nem avaliação/assinatura do orientador. |
| A1 | [Issue #1, «Estado confirmado pelo autor em 25/10/2026»](https://github.com/caiofreitas1/tcc2-prompt-engineering/issues/1), consultada em 25/10/2026 | Declaração do autor de que não realizou atividades do TCC após 03/10/2026; dispensa nova pergunta sobre esse intervalo. |
| A2 | Respostas diretas do autor neste chat em 25/10/2026, primeiro grupo | Decisões da contribuição serão tomadas pelo autor com apoio do agente; orientador revisará após o trabalho pronto. Defesa/marcação: «Ainda não». Acesso a artigos como estudante da UFMG, apenas na rede da universidade. |
| A3 | Respostas diretas do autor neste chat em 25/10/2026, perguntas reformuladas | Confirma quatro tarefas; período de 2021 a 07/09/2026 e português/inglês; estudos com avaliação/caso concreto como evidência, apoio secundário separado e exclusão de trabalhos apenas sobre treinamento. |
| A4 | Resposta direta do autor neste chat em 25/10/2026, entrega prática: «Sim, adotar essa entrega» | Confirma classificação das técnicas e tabela de apoio à escolha, avaliadas em oito exemplos, dois por tarefa, quanto à clareza, justificativa nas fontes e orientação concreta; revisão do orientador ao final, sem novos experimentos com modelos. |
| R1 | Inspeção do repositório e `make check`, por Codex em 25/10/2026 | Situação dos arquivos e integridade estrutural, sem validar resultados científicos. |

Os originais PDF/DOCX permanecem imutáveis em `fontes/legado/`; suas identidades e
hashes constam em [fontes/manifesto.json](../fontes/manifesto.json). Nesta execução,
os três hashes conferiram e todos os trechos textuais dos dois DOCX constavam nas
transcrições. Os documentos legados sustentam o histórico do TCC, não substituem
os artigos primários para sustentar achados científicos.

## Fatos confirmados e estágio acadêmico

- O objetivo é realizar uma RSL e construir uma classificação de técnicas e uma
  tabela de apoio à escolha para geração, tradução, refatoração e depuração de
  código (L1; A3–A4).
- O estágio acadêmico de execução da revisão permanece no ponto de controle de
  03/10: piloto com seis estudos e taxonomia/matriz preliminares. Busca sistemática
  completa, deduplicação e triagem não estavam concluídas; leitura e extração do
  corpus definitivo precisavam ser reprogramadas (L3; A1). T01 acrescenta a
  consolidação e as confirmações atuais do protocolo, não a execução dessas etapas.
- A avaliação da matriz em oito cenários continua por realizar. O piloto não
  envolveu experimentos próprios com LLMs (L2, introdução e seção 2.4; L3; A1).
- S1–S6 continuam candidatos herdados do piloto, com metadados e resultados a
  conferir nas fontes originais. O relato de leitura em L2 não equivale à conferência
  por este fluxo nem à inclusão no corpus definitivo (L2; R1).
- A preparação do repositório, das skills e das issues é organização do ambiente,
  não execução da busca, triagem, extração, síntese ou redação acadêmica (A1).
- Buscas, triagem, qualidade, fluxos e afirmações contêm apenas cabeçalhos;
  `dados/extracoes.jsonl` está vazio e há seis registros de estudos piloto (R1).
  Isso descreve o repositório, não uma contagem de resultados recuperados.

## Decisões confirmadas e pendências de execução

Os IDs P1–P5 foram preservados para rastrear as perguntas da primeira versão do PR.
As respostas A2–A4 substituem o estado anterior de ausência de confirmação.

| ID | Item | Estado atual e origem | Trabalho restante |
|---|---|---|---|
| P1 | Recorte, idiomas, critérios e corte | Confirmados pelo autor (A3): quatro tarefas por prompting de modelos pré-treinados; 01/01/2021 a 07/09/2026; português/inglês; estudos primários com texto completo e avaliação empírica/caso descrito, apoio secundário separado. | Aplicar os critérios nas tarefas de busca/seleção; registrar qualquer alteração antes de aplicá-la. |
| P2 | Contribuição prática | Confirmada pelo autor (A4): classificação multirrótulo e tabela de apoio à escolha, com oito exemplos, dois por tarefa, avaliando clareza, justificativa nas fontes e orientação concreta. | Desenvolver o instrumento e executar/documentar a avaliação nas tarefas próprias. Não declarar utilidade demonstrada ou ganhos de eficácia/produtividade. |
| P3 | Participação do orientador | Autor definiu que as decisões serão tomadas aqui e o orientador revisará o trabalho ao final (A2; A4). Não houve aprovação documentada do orientador. | Revisão final ainda futura; não é condição prévia para concluir T01 ou iniciar as tarefas seguintes. Viabilidade do cronograma ainda não avaliada pelo orientador. |
| P4 | Defesa e envio da marcação | Autor respondeu «Ainda não» à pergunta sobre combinar a defesa e enviar a marcação (A2). Dia, horário, modalidade e composição da banca não foram informados. | Providenciar agendamento e envio; não presumir inexistência de contatos com possíveis membros. Situação registrada para T01, sem execução de agendamento nesta issue. |
| P5 | Disponibilidade das bases/artigos | Autor informa acesso institucional a artigos apenas na rede da UFMG (A2). Não confirma individualmente busca, exportação ou texto completo em ACM/IEEE/arXiv, nem VPN ou acesso remoto. | Testar e registrar funções e limitações por base antes da busca em escala; artigos restritos podem depender da presença na rede da UFMG. O agente não testou acesso às bases nesta T01. |

O [protocolo](../protocolo/protocolo.md) preserva ACM Digital Library, IEEE Xplore,
arXiv e rastreamento de referências/citações. Seu planejamento não comprova acesso
atual. A evolução metodológica e as confirmações estão em [decisoes.md](decisoes.md).

Os prazos históricos são: marcação em 25/10, texto inicial em 08/11, defesas em
16–19/11 e texto final em 29/11/2026 (L2, seção 2.6 e Tabela 4). L3 propôs
buscas/triagem até 11/10, leitura/extração até 18/10 e síntese até 24/10. Essas metas
não foram realizadas após 03/10, conforme A1. A viabilidade e a reprogramação ainda
precisam ser examinadas; não se fixa novo prazo nem se declara aprovação do
orientador. Seu momento de revisão segue o fluxo definido pelo autor em A2.

Template oficial e dados institucionais ainda não confirmados permanecem pendências
de T03; não foram resolvidos nesta issue.

## Verificação e aceitação da issue #1

`make check` executado por Codex em 25/10/2026 após as atualizações: **zero erros
estruturais e dez testes aprovados**. `git diff --check` também passou. Os avisos
sobre ausência de extrações e limites das checagens permanecem aplicáveis:
aprovação estrutural não confirma a validade científica. Nenhum resultado do
piloto foi promovido a evidência conferida.

| Critério da issue | Estado nesta branch |
|---|---|
| Registrar confirmados e pendentes com origem | Atendido: L1–L3, A1–A4, R1 e tabela P1–P5. |
| Confirmar recorte, critérios, corte e contribuição com o autor | Atendido: A3–A4. |
| Registrar situação da marcação e disponibilidade das bases | Atendido documentalmente: A2, P4–P5; marcação ainda não realizada e acesso institucional condicionado à rede da UFMG, sem alegar teste por base. |
| Executar `make check` e relatar | Atendido; resultado acima. |

A issue permanece aberta para revisão e integração do PR. As pendências de execução
acima pertencem à continuidade do TCC e não significam atividades realizadas em
T01. Nenhuma outra issue foi executada.

## Atualização de T02 — 26/10/2026

O PR #13 de T01 foi integrado em 25/10 (merge `fb0987d`); os registros acima são o
ponto de controle daquela tarefa. Em 26/10, Codex consultou o texto primário completo
de S1, arXiv:2303.06689v5, e conferiu o recorte do piloto, seu método e orçamento.
O detalhe, os localizadores e os limites estão em [evidencias/S1.md](../evidencias/S1.md).

S1 tem metadados conferidos na versão lida; E1–E2 estão `conferido_original` por IA,
com revisão humana pendente; A1–A5 permanecem rascunhos. S1 continua no piloto e
S2–S6 continuam não conferidos. Não foi constituído corpus definitivo nem realizada
busca sistemática, triagem ou avaliação da matriz. A defesa e o acesso às bases
não foram reconfirmados nesta atividade; continuam com a última informação A2,
sem inferir mudança desde 25/10.

Verificação de T02 em 26/10: `make check` com zero erros estruturais e dez testes
aprovados, após correção da preparação dos dados sintéticos dos testes (D18);
`git diff --check` passou. A revisão humana das extrações e a conferência do
denominador efetivo permanecem pendentes e estão explicitadas no fichamento.

## Atualização de T03 — 27/10/2026

O autor informou o merge do PR #14, confirmado no GitHub (merge `140eef7` em
27/10), e escolheu expressamente o IEEE Conference Template. A estrutura agora usa
IEEEtran V1.8b em modo `conference`, A4 e português, com os seis arquivos de
conteúdo preservados. Origem, versões, adaptações e verificação estão em
[monografia/TEMPLATE.md](../monografia/TEMPLATE.md).

`make check`: zero erros estruturais e dez testes aprovados. `make pdf`: uma página
A4 compilada e inspecionada visualmente, com fontes incorporadas e log final sem
avisos ou caixas overfull/underfull. O PDF continua sendo uma estrutura com
pendências, sem novos resultados científicos. Na primeira verificação,
`make release-check` falhou com 17 bloqueios esperados; após confirmar a flag do
template, a nova execução apresentou 16 bloqueios. A barreira de entrega segue
ativa; o registro do template distingue a flag antiga do protocolo das
confirmações já dadas pelo autor.

O formato foi escolhido pelo autor. Em resposta à pergunta apresentada em 27/10,
ele identificou seu orientador pelo [perfil institucional do DCC/UFMG](https://dcc.ufmg.br/professor/eduardo-figueiredo/).
O nome completo conferido é **Eduardo Magno Lages Figueiredo**, identificado como
orientador em nota no PDF. A relação de orientação foi informada pelo autor;
a identidade e o vínculo institucional foram conferidos na página. Não se registra
revisão ou aprovação já realizada pelo docente.

O autor confirmou em seguida que a entrega é **«Somente o artigo IEEE»**. Capa,
folha de aprovação e outros elementos separados não serão acrescentados.
`template_institucional_confirmado` foi atualizado para verdadeiro com origem
nessa declaração do autor, sem alegar homologação independente pelo curso.
Os quatro critérios de T03 estão atendidos nesta branch: origem/versão e dados
confirmados, arquivos separados, compilação/inspeção e `make check`. O PR pode
seguir para revisão e integração; a issue permanece aberta até essa etapa.
Nenhuma atividade de busca, triagem ou síntese foi executada nesta tarefa.

## Protocolo v2 — 27/10/2026

Em 27/10, o autor informou que o texto inicial é para 08/11, a defesa está marcada
para 19/11 e o texto final para 29/11; que não serão usados artigos pagos; e que a
revisão será executada com IA, com revisão dele depois (D25–D27). Claude Code
analisou a estrutura e preparou o [protocolo v2](../protocolo/protocolo.md) para
RSL completa, com recuo para revisão rápida decidido em 31/10 a partir do lote
piloto. O v2 entra em vigor com a integração do PR pelo autor.

Situação: nenhuma busca, triagem, extração ou avaliação foi executada. As
sondagens de volume no arXiv (1.509 registros na expressão ampla; 516 na variante
de título) foram contagens informais da API, sem exportação, e não constituem a
T04. O autor integrou o PR #17 e, após receber um resumo do protocolo v2,
confirmou-o em 27/10 (D32); `protocolo_confirmado` passou a verdadeiro. A pergunta
sobre resultados parciais no texto de 08/11 ainda precisa ser feita ao orientador
(D30).

## T04 em andamento — 29/10/2026

Em 29/10 o autor decidiu que o texto de 08/11 é o texto completo (D33); o cronograma
foi comprimido (D34) e a consulta ao orientador sobre resultados parciais deixou de ser
necessária. Buscas executadas por Claude Code (Claude Opus 5.5):

| Busca | Base | Registros | Observação |
|---|---|---|---|
| B1 | arXiv (API oficial) | 1.597 | S1, S2, S4 e S6 recuperados; S3 e S5 não, como previsto (4.3) |
| B2 | IEEE Xplore | 665 | 671 resultados menos 6 cursos sem exportação |
| — | ACM DL | pendente | página de busca bloqueada pela verificação anti-bot da Cloudflare no navegador do app; depende do autor |

Deduplicação parcial (arXiv + IEEE): 2.262 registros, 2.042 estudos (220 em duas
bases). Um par de mesmo título com DOIs IEEE e ACM distintos (B1-0843/B2-0280) ficou
separado para conferência. Acesso aberto: 1.595 pelo arXiv; dos 443 só do IEEE, o
OpenAlex localizou 61 versões abertas, 366 sem versão aberta (X6 provável) e 16 não
encontrados. Os números mudam com a ACM. Triagem não iniciada.
