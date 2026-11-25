# Contratos dos dados

CSV: UTF-8, separador vírgula, cabeçalho obrigatório. JSONL: um objeto por linha.
IDs Sxx identificam estudos; Exx identificam extrações; Axx identificam afirmações.
Os IDs S1–S6 foram preservados do piloto. Novos estudos podem usar S7 em diante.
Arquivos só com cabeçalho significam estrutura vazia, nunca zero estudos recuperados.

## estudos.csv
Uma linha por estudo. titulo, identificador, versao e ano iniciais são metadados
herdados; conferi-los antes de preencher metadados_conferidos=sim. `fonte_primaria`
recebe caminho relativo ao texto acessível. `corpus` é candidato (identificado na
busca, ainda não incluído), piloto ou definitivo; só usar definitivo após decisão
documentada de inclusão no texto completo. Candidatos são criados por
`scripts/deduplicar.py`, com origem busca_T04.
nao_conferido não significa que a informação não existe no artigo.
`acesso_aberto`: sim, institucional, nao ou nao_conferido. O corpus definitivo exige sim ou
institucional (critério I6). `institucional` indica texto obtido pelo autor no Portal de Periódicos
da CAPES, com acesso da UFMG (D69); o PDF não é redistribuído.
`sim` indica versão aberta localizada (registro arXiv, DOI ACM 10.1145, pela abertura da
ACM em 2026, ou URL em versoes_abertas.csv); o acesso ao texto é confirmado na leitura
(T06). `nao` só depois de procurar versões abertas na T06; não localizar local aberto no
OpenAlex mantém nao_conferido. Candidatos sem DOI nem arXiv têm identificador nao_informado.

## registros.csv
Uma linha por registro exportado de uma busca (`busca_id` em buscas.csv), inclusive
de *snowballing*. `doi` e `arxiv` ficam vazios quando ausentes na exportação.
`estudo_id` é preenchido após a deduplicação: registros com o mesmo estudo formam um
grupo de duplicatas. As contagens PRISMA de identificação e deduplicação vêm daqui.

## deduplicacao.csv
Adjudicação de grupos de título idêntico com DOIs distintos ou anos distantes, que
`scripts/deduplicar.py` só une com decisão `unir` (protocolo, seção 5): chave (título
normalizado), registros, decisao (unir ou separar), evidencia, fonte, responsavel,
natureza (ia ou humano) e data. Sem adjudicação, os registros ficam separados.

## correcoes_registros.csv
Correções de metadados de registros que não alteram a captura: registro_id, campo
(só `titulo`), valor_capturado (igual ao de registros.csv, conferido pelo `make check`),
valor_corrigido, evidencia, fonte (arquivo bruto que sustenta a correção), responsavel,
natureza e data. `scripts/deduplicar.py` usa o valor corrigido no agrupamento e no
título do estudo candidato; registros.csv mantém o valor capturado.

## versoes_abertas.csv
Versões em acesso aberto localizadas para estudos sem texto aberto evidente (I6):
estudo_id, url, tipo (fonte no OpenAlex), versao, origem e data. Gerado por
`scripts/versoes_abertas.py`, que preserva as respostas do OpenAlex em `dados/brutos/`.
Registros do arXiv e da ACM (aberta desde 01/01/2026) contam como abertos sem consulta.

## publicacoes.csv
Publicação em periódico ou em anais dos estudos do corpus definitivo registrados pelo arXiv (D135):
estudo_id, arxiv, tipo (doi, url ou nao_localizada), identificador, local, ano, titulo_publicado (só
quando difere do título do arXiv), fonte, observacao, responsavel, natureza e data. Não altera
`estudos.csv`: o identificador e a versão lida continuam sendo os do arXiv. Só metadados foram
comparados (título e autores); o texto da publicação não foi lido. O registro que sustenta cada
linha está em `dados/brutos/publicacoes-2026-11-21/`. Usado por `scripts/gerar_apendice_estudos.py`.

## resumos.csv
Um resumo por estudo para a triagem de título e resumo: estudo_id, registro_id (registro
de onde veio o texto), fonte (arxiv, ieee_xplore, openalex, crossref, semanticscholar ou
nao_encontrado, isto é, não localizado nas fontes consultadas) e resumo. Gerado por `scripts/resumos.py` a partir das exportações e,
na falta delas (registros só da ACM), das APIs pelo DOI, com respostas em `dados/brutos/`.
O resumo do OpenAlex é reconstruído do índice invertido de palavras.

## buscas.csv e triagem.csv
Buscas têm data ISO, base, consulta exata, filtros, total exportado e caminho para
exportação original. Registro deduplicado não pode apagar a exportação original.
Triagem tem fase (titulo_resumo ou texto_completo), decisão (incluir, excluir, duvida),
critério aplicado, motivo, responsável, natureza (ia ou humano), versão do prompt e data.
`criterio`: códigos I1–I6 e X1–X7 do protocolo (seção 3), separados por ponto e vírgula;
exclusão cita pelo menos um código X. `responsavel`: ia-A, ia-B ou o nome do autor.
`prompt_versao` é obrigatório para decisões de IA e vazio para decisões humanas.
Só a decisão humana `incluir` no texto completo coloca um estudo no corpus definitivo.

## extracoes.jsonl
Campos obrigatórios: id, estudo_id, tarefa, tecnica, modelo, benchmark, metrica,
unidade, comparador, resultado, localizador, fonte, status, revisao_humana.
`resultado`: objeto com baseline e intervencao numéricos ou null se não reportados;
`unidade`: percentual, proporcao, contagem, tempo, energia, temperatura, qualitativo ou
nao_informado (D106); não misturar escalas. Em energia e temperatura, e quando a métrica
não tem unidade definida, a unidade literal (ex.: mWh, °C) ou o nome original da métrica
ficam em `metrica` ou `condicoes`.
`status`: nao_conferido, conferido_original ou fonte_indisponivel.
`revisao_humana`: pendente ou confirmada, com revisor e data_revisao quando confirmada.
`fonte`: caminho relativo ao texto primário, igual ao registro do estudo.
Guardar também linguagem, parametros, chamadas, testes, custos, limitacoes,
artefatos, executor e data. Acrescentar campos sem remover os mínimos.
Para lacunas: nao_conferido, nao_informado, nao_aplicavel ou fonte_indisponivel.
Não escrever um valor numérico como string contendo unidade.

Contrato 2 (extrações a partir do protocolo v2, marcadas com `"contrato": 2`) exige também:
- `citacoes`: lista de `{"trecho", "localizador"}` com cópia literal do texto que
  sustenta os valores. Com status conferido_original, o `make check` procura cada
  trecho, ignorando espaços e hífens, no arquivo `texto_fonte`.
- `texto_fonte`: caminho relativo ao texto extraído do PDF (`fontes/textos/`, fora do Git).
- `riscos`: lista de `{"categoria", "descricao", "localizador"}`; `mitigacoes`: lista de
  `{"descricao", "avaliada", "localizador"}`, com `avaliada` sim ou nao. Listas vazias
  quando o estudo não trata do tema. Categorias no protocolo, seção 9.
- `prompt_versao`: versão do prompt de extração.
E1–E2 seguem o contrato 1 da T02.

Extrações com `prompt_versao` ex-v2 (D97) acrescentam `selecao` (`principal_declarado`,
`desempate_ordem` ou `cobertura`), `mecanismos` e `condicoes`, e, quando houver,
`selecao_motivo` para exceções ao alvo de três por estudo.

## fichas.jsonl
Uma ficha por estudo incluído, extraída com ex-v2 (D97): estudo_id, tarefas, tecnicas
(`{nome_original, mecanismos, papel, avaliada_isoladamente, localizador}`, com papel
focal, comparador ou componente), modelos, benchmarks, metricas, linguagens, riscos,
mitigacoes, sem_comparador, so_classificadas, heterogeneidade (busca dirigida a
discrepâncias, não amostra neutra), citacoes, texto_fonte, leitura (completa ou parcial),
prompt_versao, executor, modelo_executor, data e revisao_humana (pendente ou confirmada,
com revisor e data_revisao). A conferência humana usa o estudo como unidade: ficha,
extrações e qualidade do estudo juntas.

Com ex-v2.1 (D101), a ficha acrescenta `componentes_fora_escopo`
(`{nome_original, natureza, localizador}`, natureza `ajuste_fino`, `embeddings_aprendidos`,
`decodificacao`, `orcamento`, `selecao_modelo` ou `outro`) e `observacoes`;
`avaliada_isoladamente` aceita só `sim` ou `nao`; `qualidade` é uma lista de sete objetos.
As extrações acrescentam `sentido` (`maior_melhor` ou `menor_melhor`; com D106, também
`nao_informado` quando o artigo não diz se valor maior ou menor é melhor), `denominador` e
`conferido_pdf` (`sim` ou `nao`). Resultado com `sentido` = `nao_informado` não recebe
classificação automática de melhora ou piora (`variacao` em
`scripts/validar_ficha_extracao.py` devolve vazio).

Com ex-v2.2 (D102):
- **Técnicas:** acrescentam `mecanismos_acrescentados`, contido em `mecanismos`, que
  passa a cobrir o pacote completo, e `tipo_contrafactual`: `pacote`, `ingrediente` ou
  `contraste_pareado` com `avaliada_isoladamente` = `sim`, e `cumulativo` ou `nenhum` com
  `nao`.
- **`componentes_fora_escopo`:** acrescenta `descricao`; `natureza` aceita só o rótulo.
- **Extrações:** acrescentam `mecanismos_acrescentados` e `derivacao` (`direta` ou
  `contraste_pareado`). Resultado descritivo tem `comparador` e `baseline` nulos e
  `sem_comparador` = `sim`.
- **Validação:** `scripts/validar_ficha_extracao.py` confere os rótulos antes de uma
  ficha ser aceita.

## afirmacoes.csv
Uma afirmação empírica por linha. `extracao_ids`: IDs separados por ponto e vírgula.
`status`: rascunho ou sustentada. `bibkey` corresponde à chave conferida no .bib;
múltiplas chaves são separadas por ponto e vírgula. `destino` é arquivo LaTeX relativo.
Só marcar sustentada com extrações conferidas no original e revisor humano identificado.
Inserir no .tex `% AFIRMACAO: A1` próximo ao trecho e citar as referências acadêmicas.
A auditoria semântica precisa confirmar se a fonte sustenta o enunciado inteiro.

## qualidade.csv
Uma linha por estudo e critério (objetivo, procedimento, comparador, metricas, ameacas,
reprodutibilidade, contaminacao; perguntas no protocolo, seção 10).
Julgamento: atende, parcial, nao_atende ou nao_informado. Não converter automaticamente
em uma nota global. Incluir localizador, justificativa e identidade do avaliador.

## fluxos.csv
Registrar contagens de busca/seleção somente quando houver os dados de origem,
denominador e regra de contagem. Não gerar um fluxograma a partir dos seis estudos piloto.

## Exemplos e modelos
Usar evidencias/modelos/ como formulários, não como observações reais.
Os testes usam dados sintéticos isolados em diretório temporário; eles não entram no corpus.
