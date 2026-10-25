# Estado documentado em 25/10/2026 — T01 / issue #1

**Situação:** reconciliação documental realizada por Codex em 25/10/2026;
consolidação do protocolo ainda depende das confirmações abaixo. Não representa
revisão acadêmica do autor nem aprovação do orientador.

## Origens e alcance

| ID | Origem | Alcance |
|---|---|---|
| L1 | [Proposta de TCC I](../fontes/legado/proposta-tcc1.txt), 29/11/2025, seções 1.1–1.2 e 4 | Objetivo, escopo e método originalmente propostos. |
| L2 | [Análise inicial](../fontes/legado/analise-inicial.txt), 07/09/2026, versão modificada em 08/09, seções 1.2–1.5, 2.4–2.6 e Apêndice A | Relato do piloto e protocolo proposto; não comprova execução posterior. |
| L3 | [Ponto de controle](../fontes/legado/ponto-de-controle.txt), 03/10/2026, campo «Estado atual» | Estágio declarado pelo aluno e plano de recuperação; não comprova cumprimento das metas nem avaliação/assinatura do orientador. |
| A1 | [Issue #1, «Estado confirmado pelo autor em 25/10/2026»](https://github.com/caiofreitas1/tcc2-prompt-engineering/issues/1), consultada em 25/10/2026 | Registra declaração direta do autor de que não realizou atividades do TCC após 03/10/2026; dispensa nova pergunta sobre esse intervalo. |
| R1 | Inspeção do repositório e `make check`, por Codex em 25/10/2026 | Situação dos arquivos e integridade estrutural, sem validar resultados científicos. |

Os originais PDF/DOCX permanecem imutáveis em `fontes/legado/`; suas identidades e
hashes constam em [fontes/manifesto.json](../fontes/manifesto.json). Nesta execução,
os três hashes conferiram e todos os trechos textuais dos dois DOCX constavam nas
transcrições. Os documentos legados sustentam o histórico do TCC, não substituem
os artigos primários para sustentar achados científicos.

## Fatos confirmados e estágio acadêmico

- O objetivo documentado é realizar uma RSL e construir uma taxonomia para apoiar
  geração, tradução, refatoração e depuração de código (L1, seções 1.1–1.2).
- O estágio acadêmico permanece no ponto de controle de 03/10: protocolo inicial,
  piloto com seis estudos e taxonomia/matriz preliminares. A busca sistemática
  completa, a deduplicação e a triagem não estavam concluídas; a leitura e a extração
  do corpus definitivo precisavam ser reprogramadas (L3; ausência de atividade
  posterior confirmada em A1).
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

## Propostas preservadas

O [protocolo](../protocolo/protocolo.md) mantém as quatro tarefas, modelos
pré-treinados via prompting, português/inglês e período de 01/01/2021 a 07/09/2026;
ACM Digital Library, IEEE Xplore, arXiv e rastreamento de referências/citações;
corpus primário empírico com texto completo, apoio secundário separado; taxonomia
multirrótulo e matriz a avaliar em oito cenários, dois por tarefa (L2, seções
1.2–1.5 e 2.4). Não há confirmação atual do autor nem aprovação documentada do
orientador desses termos. A evolução em relação a L1 está registrada em
[decisoes.md](decisoes.md).

## Confirmações e bloqueios de T01

Perguntas agrupadas apresentadas ao autor nesta execução em 25/10/2026; sem
resposta registrada até esta atualização. Não interpretar silêncio como aceite.

| ID | Confirmação necessária | Situação e origem | Consequência |
|---|---|---|---|
| P1 | Recorte, idiomas, critérios e corte de 07/09/2026 | Propostos em L2; confirmação atual do autor pendente. | Não tratar o protocolo como confirmado nem alterar o corte. |
| P2 | Taxonomia/matriz, oito cenários e adequação da contribuição prática | Planejados em L2, seções 1.4 e 2.4; aceite do autor e manifestação do orientador pendentes. | Não declarar matriz avaliada ou contribuição aprovada. |
| P3 | Aceite do protocolo e viabilidade pelo orientador | L3 prevê reavaliação após a triagem; não há avaliação preenchida/assinada no arquivo preservado. | Registrar manifestação, data e condições quando fornecidas; não presumir aprovação. |
| P4 | Defesa: banca, dia, horário, modalidade e envio da marcação/formulário/planilha | L2, seção 2.6, prevê marcação até 25/10; A1 não confirma agendamento nem banca. Situação atual: não confirmada. | Solicitar confirmação ao autor/orientador; prazo previsto não prova entrega. |
| P5 | Acesso à busca, exportação e textos completos nas bases | Bases previstas em L2, seção 1.3. ACM, IEEE e arXiv: acesso atual do autor não conferido; acesso institucional/CAFe/VPN não informado. | Identificar limitação por base; não declarar acesso nem substituir base por web sem decisão registrada. |

Os prazos históricos são: marcação em 25/10, texto inicial em 08/11, defesas em
16–19/11 e texto final em 29/11/2026 (L2, seção 2.6 e Tabela 4). L3 propôs
buscas/triagem até 11/10, leitura/extração até 18/10 e síntese até 24/10. Essas metas
não foram realizadas após 03/10, conforme A1; a viabilidade e o cronograma precisam
ser revistos com o orientador. Não se fixa novo prazo aqui.

Template oficial e dados institucionais ainda não confirmados permanecem pendências
de T03; não foram resolvidos nesta issue.

## Verificação e aceitação da issue #1

`make check` executado por Codex em 25/10/2026: **zero erros estruturais e dez
testes aprovados**. Os avisos sobre ausência de extrações e limites das checagens
permanecem aplicáveis: aprovação estrutural não confirma o protocolo nem a validade
científica. Nenhum resultado do piloto foi promovido a evidência conferida.

| Critério da issue | Estado nesta execução |
|---|---|
| Registrar confirmados e pendentes com origem | Atendido documentalmente: L1–L3, A1, R1 e P1–P5. |
| Confirmar recorte, critérios, corte e contribuição com o autor | Pendente: P1–P2. |
| Registrar situação da marcação e disponibilidade das bases | Registrada como não confirmada/não conferida: P4–P5; informações concretas ainda dependem de resposta. |
| Executar `make check` e relatar | Atendido; resultado acima. |

**Manter a issue aberta.** Consolidar as respostas e registrar as decisões antes de
considerar T01 concluída ou liberar tarefas dependentes como se o protocolo já
estivesse confirmado. Esta execução se limita às três entregas de T01.
