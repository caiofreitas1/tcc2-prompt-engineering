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
`acesso_aberto`: sim, nao ou nao_conferido. O corpus definitivo exige sim (critério I6).

## registros.csv
Uma linha por registro exportado de uma busca (`busca_id` em buscas.csv), inclusive
de *snowballing*. `doi` e `arxiv` ficam vazios quando ausentes na exportação.
`estudo_id` é preenchido após a deduplicação: registros com o mesmo estudo formam um
grupo de duplicatas. As contagens PRISMA de identificação e deduplicação vêm daqui.

## versoes_abertas.csv
Versões em acesso aberto localizadas para estudos sem texto aberto evidente (I6):
estudo_id, url, tipo (fonte no OpenAlex), versao, origem e data. Gerado por
`scripts/versoes_abertas.py`, que preserva as respostas do OpenAlex em `dados/brutos/`.
Registros do arXiv e da ACM (aberta desde 01/01/2026) contam como abertos sem consulta.

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
`unidade`: percentual, proporcao, contagem, tempo ou qualitativo; não misturar escalas.
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
