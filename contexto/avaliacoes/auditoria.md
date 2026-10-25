# Registro de uso de skill durante a preparação

Este parecer reflete os arquivos disponíveis no instante do teste. A falta inicial
de referencias.bib foi resolvida depois; a verificação final passou em dez testes.
Não constitui auditoria dos artigos primários nem revisão humana.

# Parecer de auditoria científica — evidências do piloto

**Escopo:** seção 2.2, Tabelas 1–2 e inferências relacionadas nas seções 2.3–2.5 de `fontes/legado/analise-inicial.txt`, no projeto `/workspace/scratch/02a13c6b9b7d/tcc2-prompt-engineering`.

**Executor/data/ferramentas:** agente de IA, 25/10/2026; leitura de arquivos locais, Python padrão para aritmética decimal e inspeção do XML do DOCX, `make check`. Natureza: auditoria assistida por IA; não constitui revisão humana independente. Não foi possível registrar commit: a pasta disponibilizada não contém repositório Git.

**Procedimento:** aplicada a skill `tcc-auditar-ciencia`; lidos `AGENTS.md`, `README.md`, `protocolo/protocolo.md`, `contexto/estado-atual.md`, contratos de dados e formulário `evidencias/modelos/auditoria.md`. O parecer foi escrito fora do projeto por determinação da tarefa, em lugar do destino usual da skill. Nenhum arquivo do projeto foi alterado e nenhum material externo foi buscado.

**Parecer: não conferível com os materiais locais quanto ao suporte científico dos resultados.** A aritmética apresentada é internamente consistente. O documento é utilizável como registro histórico de um piloto com ressalvas, mas seus números e metadados não podem ser promovidos a evidências validadas nesta auditoria.

## Achados e pendências

Gravidade indica o impacto sobre a utilização atual dos resultados, não uma demonstração de que o artigo ou o relatório contenha dado falso.

| Gravidade | Arquivo/trecho | Achado e evidência local | Correção ou providência necessária |
|---|---|---|---|
| Alta | `analise-inicial.txt`, seção 2.2 e Tabela 1, linhas 93–108; referências [3]–[8] | Nenhum dos seis textos primários está disponível no projeto. Não existe pasta local `fontes/artigos/`; `dados/estudos.csv` tem seis linhas, todas com `metadados_conferidos=nao` e `fonte_primaria=nao_conferido`. O relatório afirma leitura anterior dos originais, mas esse relato não substitui os artigos nesta conferência. | Manter os números e metadados como `nao_conferido` e registrar `fonte_indisponivel` para a indisponibilidade nesta auditoria. Recuperar futuramente as versões identificadas, guardar caminhos e conferir comparação, localizador e metadados antes de reutilizar como evidência validada. Não interpretar a indisponibilidade atual como prova de que a leitura de 07/09 não ocorreu. |
| Alta | `dados/extracoes.jsonl`, `dados/afirmacoes.csv`; seções 2.2–2.5 | O arquivo de extrações está vazio e o de afirmações contém somente cabeçalho. Assim, não há cadeia executável de rastreabilidade entre afirmação, extração, versão primária e referência conferida. Os rótulos S1–S6 e localizadores herdados não completam essa cadeia. | Registrar cada comparação e afirmação ao realizar a conferência no original; manter revisão humana pendente. Não promover diretamente os números do legado a extrações `conferido_original`. |
| Média | Seção 2.3, linha 48; Tabela 2, linhas 109–118 | A designação “recorte comparável” está apoiada no mesmo benchmark, mas a tabela local não registra tamanho e versão do conjunto, amostragem, parâmetros, número de chamadas, tentativas, custo ou disponibilidade de feedback. Mesmo benchmark não comprova igualdade de orçamento ou protocolo. A ressalva geral de Pass@1 na linha 44 é adequada, porém não supre esses campos. | Tratar as diferenças como contrastes descritivos dos valores transcritos; conferir as condições de cada coluna na Tabela 4 do original de S6. Explicitar se o orçamento difere e evitar inferência de eficiência ou superioridade em condições equivalentes sem esse suporte. |
| Média | Seção 2.3, linha 51 | Confere-se localmente `40,75 − 35,50 = 5,25 p.p.`. Não se pode conferir que a discussão de [8] diga `4,25`, nem a atribuição de divergência entre tabela e discussão, sem S6. | Preservar separadamente o cálculo certo e a pendência bibliográfica. Ao obter o original, indicar página/parágrafo para os `4,25` e investigar o comparador; até lá, descrever essa divergência como alegação herdada não conferida. |
| Média | S5, Tabela 1, linha 106; QP2, linha 60 | A tabela relata 47 participantes, cinco tarefas e maior frequência de insegurança em quatro tarefas. Faltam distribuição por grupo, denominadores por tarefa, medidas e definição de insegurança. A inferência adicional de divergência entre percepção e segurança observada não tem resultado específico extraído na tabela. Nada disso pode ser conferido no original localmente. | Extrair resultados por tarefa e a comparação entre percepção e medida de segurança com localizadores próprios. Não atribuir causalidade a comportamentos de prompting; o relatório já faz essa ressalva, que deve ser preservada. |
| Média | S4, Tabela 1, linha 103; QP2, linha 60 | Os percentuais de aprovação não vêm acompanhados de número de unidades avaliadas, definição da unidade de refatoração ou classes de falha. A expressão “falhas funcionais” não pode ser validada apenas pelo complemento aritmético da taxa de aprovação: a classificação de resultados depende do protocolo original. | Conferir em S4 o denominador, tratamento de falhas de compilação/execução e critério de preservação de comportamento. Até lá, preferir “nem todos os casos obtiveram aprovação nos testes, segundo os valores transcritos”, sem inventar categorias de falha. |
| Média | Verificação automática do projeto | `PYTHONDONTWRITEBYTECODE=1 make check` falhou com código 2: o verificador não encontra `monografia/referencias.bib`. Pelo encadeamento do Makefile, a suíte de testes não chegou a executar nesse comando. | Restaurar ou disponibilizar os arquivos esperados do projeto e repetir `make check`. Esta falha impede declarar aprovação automática; não demonstra erro nos números do piloto. |

## Conferência aritmética e coerência interna

A Tabela 1 e a Tabela 2 do DOCX local foram lidas diretamente pelo XML: os valores correspondem aos apresentados no TXT. Isso confirma a transcrição entre dois documentos legados, sem validar os artigos citados. As tabelas surgem após o Apêndice A na extração textual; no DOCX são tabelas próprias. Essa disposição do TXT não foi tratada como erro de organização do documento original.

| Comparação dos valores locais | Cálculo conferido | Resultado |
|---|---|---|
| S1, planejamento versus direto | 60,3 − 48,1 | +12,2 p.p. |
| S1, ganho relativo | (60,3 − 48,1) / 48,1 × 100 | 25,3638…%, arredondado a 25,4% |
| S2, tradução | 92,5 − 80,4 | +12,1 p.p. |
| S3, HumanEval | 91,0 − 80,1 | +10,9 p.p. |
| S3, MBPP | 77,1 − 80,1 | −3,0 p.p. |
| S4, CoT versus zero-shot | 32,22 − 28,36 | +3,86 p.p. |
| S4, one-shot versus zero-shot | 34,51 − 28,36 | +6,15 p.p. |
| S6, 8B: CGO versus direto / self-planning | 28,00 − 26,00 / 28,00 − 30,00 | +2,00 / −2,00 p.p. |
| S6, 70B: CGO versus direto / self-planning | 49,00 − 41,50 / 49,00 − 48,30 | +7,50 / +0,70 p.p. |
| S6, GPT-3.5: CGO versus direto / self-planning | 40,75 − 35,50 / 40,75 − 38,30 | +5,25 / +2,45 p.p. |

Não foi encontrado erro aritmético nos contrastes publicados nessas duas tabelas. Os contrastes adicionais de S3 e S4 acima são apenas conferência dos números locais; não são novas extrações de artigos. Não se calcularam médias entre estudos nem intervalos de confiança sem denominadores.

São adequadas, no plano interno do relato, a separação entre piloto e corpus definitivo, a caracterização dos experimentos como pertencentes aos artigos, a preservação da queda em MBPP e da desvantagem do CGO no 8B e a recusa de inferir produtividade, custo ou segurança apenas de acurácia. A matriz é explicitamente preliminar e apresentada como decisão de projeto; oito cenários e revisão pelo orientador permanecem planejados. Não foi encontrada alegação de dupla triagem humana realizada. Essas qualidades de redação não certificam o suporte primário das afirmações.

Os seis IDs locais correspondem à contagem declarada do piloto e o mapeamento rotulado cobre as quatro tarefas. Não há registros preenchidos de busca, triagem, qualidade ou fluxo; arquivos somente com cabeçalho não significam zero recuperados e não permitem calcular cobertura, elegibilidade ou concordância. O estado do projeto não prova a ausência de avanços do autor após o ponto de controle.

## Limites de conferência

Nenhum achado científico de S1–S6, autoria, ano, DOI, versão, status editorial ou localizador foi validado em texto primário. Também não foram conferidos pacotes de replicação, execução anterior das consultas, significância, custos, orçamento de interação ou revisão humana. Campos ausentes nos materiais locais foram tratados como não conferidos ou fonte indisponível, nunca como “não informado pelo artigo”. O resultado automático foi falha, e não aprovação com ressalvas. A ausência de outros erros identificados não certifica completude ou validade científica.
