# Auditoria do protocolo v2 — 27/10/2026

Escopo/commit: protocolo v2 integrado pelo PR #17, HEAD `7f2bd8e`, com alteração
principal em `b0652a1`. Revisados protocolo, prompts, contratos CSV/JSONL,
validador, testes, backlog e registros de decisões/estado.

Executor/data/ferramenta: Codex, 27/10/2026, inspeção de arquivos, Git, Python e
consulta web a fontes primárias. Natureza: auditoria assistida por IA; não é
verificação humana pelo autor nem aprovação do orientador.

**Parecer: requer correções antes da execução em lote.** A estrutura melhorou,
mas há contradições operacionais e controles prometidos que ainda podem ser
contornados. Nenhum resultado científico foi reextraído nesta auditoria.

## Achados prioritários

### F1 — Alta: amostragem de extrações incompatível com a barreira de entrega

**Arquivo/trecho:** `protocolo/protocolo.md:169`, seção 7;
`scripts/verificar.py:220–225`; T07 em `tarefas/backlog.json`.

**Evidência:** o protocolo e T07 exigem revisão humana de 20% das extrações,
mínimo 10. Na entrega, o código exige `revisao_humana=confirmada` em **todas** as
extrações de todos os estudos incluídos. Assim, executar exatamente a amostragem
prevista pode deixar a entrega bloqueada. A conferência de cada afirmação em T12
não resolve automaticamente as extrações que não sustentam afirmações no texto.

**Correção:** explicitar uma política única e refletir essa política no validador
e na estimativa de horas. Uma opção compatível com a amostragem é exigir a
conferência das evidências de todas as afirmações usadas e a auditoria da amostra
restante, registrando exatamente quais extrações foram revisadas. Se a opção for
conferência integral, atualizar o protocolo e o cronograma. Não confirmar revisões
que não tenham ocorrido nem simplesmente remover a barreira sem substituí-la.

### F2 — Alta: regra de recuo e limite de recalibrações se contradizem

**Arquivo/trecho:** `protocolo/protocolo.md:172–190`, seções 7–8;
seções 1 e 4.2.

**Evidência:** a seção 7 admite duas revisões do prompt e, persistindo a perda,
manda registrá-la como limitação. A seção 8 exige ausência de perdas após no
máximo uma revisão; o descumprimento determina recuo. São instruções diferentes
para o mesmo evento. Além disso, o recuo apenas restringe termos de tarefa ao
título. Essa restrição reduz o universo, mas não demonstra correção do erro de
classificação que motivou o recuo quando o segundo critério falha.

**Correção:** definir uma única sequência de decisão, número máximo de revisões,
amostra de validação de cada versão e condição de avanço. Separar inviabilidade
por volume/horas de falha de triagem. Após restringir a busca, reavaliar volume,
horas e desempenho da triagem no universo resultante; prever a ação se o recuo
também falhar. Não adotar a restrição de título como solução automática para
falsos negativos da IA.

### F3 — Alta: contrato 2 é opcional na implementação

**Arquivo/trecho:** `protocolo/protocolo.md:194–199`;
`dados/README.md:45–54`; `scripts/verificar.py:140–154`.

**Evidência:** as regras novas só são executadas se `e.get('contrato') == 2`.
Uma extração nova sem esse campo, ou com outro valor, passa pelo contrato antigo.
Reproduzido em diretório temporário: uma extração `E_NOVA`, marcada como
`conferido_original`, sem `contrato`, citações, texto-fonte, riscos, mitigações ou
versão do prompt produziu **zero erros**. A exceção documentada é apenas E1–E2.
Mesmo declarando contrato 2, riscos com categoria inválida, mitigação vazia e
`prompt_versao` vazio também produziram zero erros.

**Correção:** identificar explicitamente as exceções legadas E1–E2, exigir
contrato 2 nas demais extrações e rejeitar versões desconhecidas. Validar campos
internos, categorias e valores permitidos, além de conteúdo não vazio do prompt.
Testar esses casos sem alterar os dados científicos reais.

### F4 — Alta: o prompt delega a uma automação de elegibilidade ainda ausente

**Arquivo/trecho:** `protocolo/prompts/triagem-titulo-resumo.md:13–15`;
`protocolo/protocolo.md:46`; contratos de estudos/registros e
`scripts/verificar.py:59–93`.

**Evidência:** o prompt determina que o triador não decida I4/I6 porque período e
acesso aberto são conferidos automaticamente. O código inspecionado verifica
apenas a declaração de acesso aberto para o corpus definitivo; não verifica
data de primeira versão pública. Os CSVs contêm `ano`, mas nenhum campo próprio
para a data completa e sua fonte. Em fixture temporária, um estudo com ano
`1900`, inclusão humana declarando I4 e acesso aberto `sim` passou sem erros.

**Correção:** implementar e documentar a etapa responsável, ou declarar a
conferência manual desses critérios com responsável e evidência. Registrar data
da primeira versão, fonte da data e URL/versão aberta efetivamente localizada.
Datas de edição/publicação posterior não devem substituir a primeira versão
pública. Até existir essa etapa, retirar do prompt a garantia de automação.

## Ajustes metodológicos e documentais

| ID / gravidade | Arquivo/trecho | Problema e evidência | Correção necessária |
|---|---|---|---|
| F5 / Média | Protocolo, seções 6–7, linhas 153–178 | Há três decisões possíveis, divergências entre IAs e regra de união, mas não se define o «consenso» usado no κ contra o autor. A revocação também não tem fórmula ou denominador definidos. | Definir o desfecho binário avançar/excluir para a comparação operacional e o tratamento de `duvida`; preservar as decisões originais. Por exemplo, sensibilidade da triagem = registros que avançam pela união entre os que o autor manda avançar / todos os que o autor manda avançar na amostra. Relatar matriz de confusão, contagens e denominadores; não apresentar isso como revocação de toda a busca nem como elegibilidade final confirmada. Prever κ/razão não estimável quando o denominador necessário for zero. |
| F6 / Média | Protocolo, seção 7, linhas 167–176 | Há auditoria de exclusões após o piloto, mas não há ação prescrita se forem encontrados estudos perdidos nessa auditoria de lote ou no texto completo. Também faltam regra para populações menores que os mínimos e sorteio reproduzível. | Registrar universo, IDs e semente/método de sorteio; usar toda a população quando menor que o mínimo. Definir resgate do estudo, investigação do erro e ampliação/reaplicação da triagem quando necessário. Uma exclusão humana revertida precisa alterar o fluxo e a decisão final registrada. |
| F7 / Média | Protocolo, seção 4.1, linhas 68–75; cronograma de T04 | A abertura do texto da ACM não garante a disponibilidade de todas as ferramentas de busca e exportação em lote na edição Basic. A documentação primária distingue ferramentas Premium. | Antes de depender da etapa, testar a consulta nos campos previstos, paginação e exportação completa na modalidade disponível; registrar limites. Confirmar se a busca cobre somente publicações ACM ou também o Guide. Não substituir silenciosamente a base ou apresentar uma busca web como sua execução. |
| F8 / Média | Protocolo, critério I2, linha 44; prompt de texto completo, linhas 12–13 | O critério diz «aplica prompting»; o prompt exige que prompting seja parte do objeto avaliado, excluindo o mero uso do modelo. A segunda formulação é mais restrita e pode afetar estudos sobre riscos da QP2. | Dar a I2 a mesma definição no protocolo e nos dois prompts, com exemplos de inclusão/exclusão para estudos de riscos. Registrar a interpretação antes da seleção e aplicá-la também aos candidatos do piloto. |
| F9 / Baixa | `projeto.json`; `contexto/estado-atual.md:147–161`; `tarefas/T04.md` a `T07.md` | HEAD já contém o merge do PR #17, mas os documentos ainda falam na integração como futura e `protocolo_confirmado` continua falso. Os corpos de T04–T07 em `backlog.json` foram atualizados, mas os arquivos Markdown dessas tarefas mantêm instruções antigas. | Registrar a integração efetiva e distinguir esse fato de aprovação científica/humana. Reconciliar a flag somente com a confirmação correspondente; sincronizar os arquivos de tarefas e indicar qual é a fonte operacional. |

F7 é um risco de execução a testar, **não** uma afirmação de que toda exportação
gratuita da ACM esteja indisponível. A pendência sobre o aceite de resultados
parciais em 08/11 já está registrada em D30 e continua sendo uma condição do
cronograma. A projeção de horas deve distinguir título/resumo, texto completo,
extração e verificação das afirmações; apenas cronometrar título/resumo não mede
as demais etapas.

## Verificações realizadas

- `make check`: zero erros estruturais e **17 testes aprovados**.
- `make release-check`: **16 erros**, compatíveis com a estrutura ainda
  incompleta (rascunhos, flags pendentes, ausência de buscas/corpus/qualidade e
  seções com pendências). Não é uma versão pronta para entrega.
- Quatro sondas sintéticas, reaproveitando a fixture de
  `tests/test_verificar.py`, executadas exclusivamente em diretórios temporários:

| Sonda | Resultado observado |
|---|---|
| Extração nova conferida sem declarar contrato 2 | Zero erros; reproduz F3. |
| Contrato 2 com risco inválido, mitigação vazia e versão de prompt vazia | Zero erros; reproduz F3. |
| Inclusão declarando I4 em estudo de ano 1900 | Zero erros; evidencia a ausência de validação temporal de F4. |
| Estudo incluído com extração de revisão humana pendente, em modo release | `E_TEST: revisão humana pendente`, além das demais pendências esperadas da fixture; reproduz F1. |

As sondas não são estudos do corpus nem testes incorporados ao projeto.
Nenhum teste existente foi alterado. Nenhum protocolo, prompt, decisão humana,
registro científico ou flag foi corrigido nesta revisão; este parecer é a única
entrega nova.

## Fontes e limites da conferência

O [checklist expandido oficial PRISMA 2020](https://www.prisma-statement.org/s/PRISMA_2020_expanded_checklist-w7ra.pdf),
itens 8–9, pede descrição do uso e validação das ferramentas de automação na
seleção e extração. Isso apoia o registro explícito dessas escolhas; não certifica
o desempenho dos dois modelos nem os tamanhos de amostra escolhidos.

O [material oficial da ACM sobre as edições Basic e Premium](https://libraries.acm.org/binaries/content/assets/libraries/acmo/tbi-an-acm-digital-library-flyer-a4-mar25.pdf)
distingue o acesso aberto ao conteúdo dos recursos de pesquisa e gestão, incluindo
operações em lote. A [página institucional sobre acesso aberto](https://prod-www.acm.bloomreach.cloud/publications/openaccess)
confirma a abertura das publicações ACM em 2026. Não foi realizada busca/exportação
na interface da base nesta auditoria.

As páginas primárias de [S2, arXiv:2304.05128](https://arxiv.org/abs/2304.05128)
e [S4, arXiv:2411.02320](https://arxiv.org/abs/2411.02320) foram consultadas
somente para identificação, histórico e texto de título/resumo. Não foi
reproduzida a calibração nas três bases, nem conferidas as contagens informais
1.509/516. Não se inferiu que S3/S5 serão encontrados por snowballing: isso ainda
precisa ser observado. A elegibilidade desses estudos segue pendente.

Os sete itens bibliográficos do método não foram todos reconferidos em texto
integral nesta auditoria. A declaração anterior de conferência Crossref permanece
atribuída ao seu executor. Não se validaram resultados empíricos, a suficiência
estatística das amostras ou a disponibilidade dos modelos na conta de execução.

Pontos preservados e coerentes: corte temporal explicitado, separação de
piloto/corpus, inclusão definitiva condicionada a decisão humana, registro de
limitação por acesso aberto, prompts versionados e síntese que evita rankings
entre benchmarks incompatíveis. Esses pontos são adequados como planejamento;
sua execução ainda depende dos registros correspondentes.
