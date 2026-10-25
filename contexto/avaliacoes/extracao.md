# Registro de uso de skill durante a preparação

Este parecer reflete os arquivos disponíveis no instante do teste. A falta inicial
de referencias.bib foi resolvida depois; a verificação final passou em dez testes.
Não constitui auditoria dos artigos primários nem revisão humana.

# Parecer sobre a conferência de S1

Data: 25/10/2026. Executor: agente de IA Codex, com a skill `tcc-extrair-evidencias` de `/root/.codex/skills/remote-skills/tcc-extrair-evidencias/SKILL.md`. Revisão humana: pendente.

**Não é possível conferir os resultados de S1 no original com os materiais atualmente presentes no projeto.** Foram consultados AGENTS.md, README.md, o protocolo, o estado atual, os contratos de dados, a tarefa T02, o formulário de fichamento, os registros e os materiais locais de origem. Não houve busca externa nem alteração do corpus ou dos arquivos do projeto.

## Material disponível e identidade do estudo

`dados/estudos.csv` identifica S1 como *Self-planning Code Generation with Large Language Models*, arXiv:2303.06689, v5, ano 2025. Os campos permanecem herdados: `corpus=piloto`, `metadados_conferidos=nao`, `fonte_primaria=nao_conferido`. Não há artigo primário em `fontes/`; a pasta contém os três documentos legados e suas extrações auxiliares. `fontes/manifesto.json` classifica expressamente os documentos como não primários. `dados/extracoes.jsonl` está vazio.

A referência [3] de `fontes/legado/analise-inicial.docx` atribui o trabalho a Jiang et al., informa aceite em TOSEM e versão arXiv:2303.06689v5, 2025. Isso é informação histórica do documento, sem conferência bibliográfica primária nesta tarefa. Não confirma autores completos, publicação, DOI ou equivalência entre versões.

## O que pôde ser conferido

Conferiu-se diretamente o conteúdo da célula da Tabela 1 do DOCX legado, linha `S1 [3] Geração`, mediante leitura do XML interno do arquivo. A extração auxiliar `fontes/legado/analise-inicial.txt`, linhas 93–94, coincide com essa célula. Ela relata:

| Campo | Informação herdada | Situação atual |
|---|---|---|
| Tarefa | Geração de código | Não conferida no artigo |
| Técnica | Self-planning | Não conferida no artigo |
| Modelo | code-davinci-002 | Não conferido no artigo |
| Benchmark | HumanEval | Não conferido no artigo |
| Métrica e escala | Pass@1, percentual | Não conferidas no artigo |
| Comparador | Geração direta | Não conferido no artigo |
| Baseline e intervenção | 48,1 e 60,3 | Valores herdados, não validados |
| Localizador alegado no artigo | Seção 4.1, Tabela 1 | Não acessado; não é localizador conferido |

Assim, há confirmação da transcrição histórica, não um resultado `conferido_original`.

Também foi conferida a aritmética **condicionada aos valores herdados**:

- Diferença absoluta: `60,3 − 48,1 = 12,2` pontos percentuais.
- Variação relativa: `100 × (60,3 − 48,1) / 48,1 = 25,363825…%`, aproximadamente `25,4%`.

Os cálculos foram executados com `decimal.Decimal` do Python, entradas `48.1` e `60.3`. Sua correção não valida as entradas, a comparabilidade das condições, a métrica nem o desenho experimental. Não há divergência aritmética nesses dois derivados do legado; eventuais divergências entre texto e tabela do artigo seguem desconhecidas.

## Registros que podem ser feitos

Um fichamento de acesso pode registrar a identidade herdada, o documento efetivamente lido, a ausência local do texto primário e as pendências. Sua situação deve ser `fonte_indisponivel` ou `nao_conferido`; a revisão humana deve continuar `pendente`. Não há base para marcar `metadados_conferidos=sim`, promover S1 ao corpus definitivo, preencher uma afirmação como `sustentada` ou avaliar a qualidade científica do artigo.

Se for necessário materializar uma pendência em `dados/extracoes.jsonl` posteriormente, o contrato permite um registro como o exemplo abaixo. Ele é apenas uma proposta: **não foi inserido no projeto**, e o ID deve ser reservado no momento da gravação. Os números herdados ficam em campo de proveniência separado para não parecerem resultados extraídos do primário.

```json
{
  "id": "E1",
  "estudo_id": "S1",
  "tarefa": "nao_conferido",
  "tecnica": "nao_conferido",
  "modelo": "nao_conferido",
  "benchmark": "nao_conferido",
  "metrica": "nao_conferido",
  "unidade": "percentual",
  "comparador": "nao_conferido",
  "resultado": {"baseline": null, "intervencao": null},
  "localizador": "fonte_indisponivel",
  "fonte": "fonte_indisponivel",
  "status": "fonte_indisponivel",
  "revisao_humana": "pendente",
  "versao": "nao_conferido",
  "versao_herdada": "arXiv:2303.06689v5",
  "linguagem": "nao_conferido",
  "parametros": "nao_conferido",
  "chamadas": "nao_conferido",
  "amostragem": "nao_conferido",
  "testes": "nao_conferido",
  "custos": "nao_conferido",
  "denominador": "nao_conferido",
  "limitacoes": "nao_conferido",
  "artefatos": "nao_conferido",
  "executor": "Codex (IA)",
  "data": "2026-10-25",
  "proveniencia_legado": {
    "arquivo": "fontes/legado/analise-inicial.docx",
    "localizador": "Tabela 1, linha S1 [3] Geração",
    "tarefa": "geracao",
    "tecnica": "self-planning",
    "modelo": "code-davinci-002",
    "benchmark": "HumanEval",
    "metrica": "pass@1",
    "comparador": "geracao direta",
    "baseline": 48.1,
    "intervencao": 60.3,
    "localizador_alegado_no_artigo": "secao 4.1, Tabela 1",
    "situacao": "nao_conferido_no_original"
  }
}
```

Nesse exemplo, `unidade=percentual` serve exclusivamente à escala declarada no legado; a escala primária continua pendente. Se adotado, `fonte_indisponivel` deve ser mantido de modo consistente no registro do estudo e da extração até obtenção do arquivo. Uma alternativa mais simples é deixar o JSONL vazio e registrar o bloqueio no fichamento. Nenhuma opção produz uma extração científica validada.

Não cabe usar `nao_informado` para orçamento, amostragem, linguagem ou limitações: o artigo não foi lido, portanto não se sabe se ele os informa. A ausência local também não prova indisponibilidade pública nem ausência de acesso pelo autor.

## Pendências para concluir T02

1. Confirmar o andamento de T01 com o autor; a dependência continua aberta no backlog. A leitura local realizada aqui não satisfaz essa confirmação.
2. Obter o texto primário completo da versão indicada, preservar identificador, versão e arquivo, e verificar se há versão publicada pertinente conforme o protocolo.
3. Conferir metadados e a comparação na seção/tabela efetivamente presente nessa versão, separando tarefas, modelos e benchmarks.
4. Extrair denominadores, amostragem, tentativas, chamadas, orçamento, parâmetros, testes, ferramentas, custo, ameaças e artefatos com seus localizadores. Pass@1 não demonstra uma única interação.
5. Registrar resultados e derivados em fichamento e JSONL com proveniência primária. Não inferir produtividade, segurança ou economia de custo a partir do ganho de benchmark.
6. Submeter a revisão real do autor/orientador, mantendo `revisao_humana=pendente` até manifestação identificada e datada. Este parecer constitui avaliação por IA.

## Verificação técnica

Foi executado `make check` na raiz do projeto. Na primeira execução, a estrutura ainda estava em preparação e o verificador não encontrou `monografia/referencias.bib`. Após o agente principal informar a conclusão desse arquivo e do esqueleto LaTeX, o comando foi reexecutado na versão atual: **saída 0, zero erros estruturais e nove testes aprovados**.

O verificador advertiu que não há extrações registradas nem resultados validados pelo fluxo e que verificações estruturais não conferem a veracidade das fontes ou a sustentação semântica das afirmações. Portanto, a aprovação técnica não altera as conclusões sobre a ausência do texto primário. T02 permanece bloqueada para resultados primários e não deve ser declarada concluída.
