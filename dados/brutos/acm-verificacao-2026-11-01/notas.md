# Verificação complementar da busca ACM — 01/11/2026

Nova coleta da busca B3 para conferir a consistência e a cobertura dos 482 registros
de 29/10/2026 (`../acm-2026-10-29/`). Não é reconstrução da segunda passada de 29/10,
que não foi preservada, nem uma busca nova do corpus: os registros não entram em
`dados/registros.csv`. Pedido do autor em 01/11/2026.

## Execução

- Executor: Claude Code (Claude Opus 5.5), no Chrome do autor (extensão Claude in
  Chrome), sem login (ACM DL edição Basic).
- Horário: 01/11/2026, 22h45–22h48 (UTC−3); no arquivo, `2026-11-02T01:45:49Z` a
  `2026-11-02T01:48:35Z` (UTC).
- Consulta: `consulta.txt`, cópia byte a byte da consulta de 29/10 (mesmo SHA-256).
- URL base (em `captura.json.gz`, campo `url_base`): busca avançada com
  `AllField=<consulta>`, `expand=dl`, `AfterMonth=1&AfterYear=2021`,
  `BeforeMonth=9&BeforeYear=2026`, `pageSize=50`, `sortBy=EpubDate_asc`; páginas
  `startPage=0` a `10`. Parâmetros iguais aos de 29/10, mais a ordenação por data.

## Parâmetros efetivamente aplicados (evidência na própria página)

- Campos e consulta: o título da página devolvido pela ACM expande a consulta em
  `[Title: ...] OR [Abstract: ...]` para os três blocos.
- Filtro de data: o mesmo título termina em
  `AND [E-Publication Date: (01/01/2021 TO 09/30/2026)]`; o painel mostra
  "Applied Filters: January 2021 - September 2026".
- Coleção: "Searched The ACM Full-Text Collection (857,734 records)"; a expansão para
  o ACM Guide aparece desabilitada (recurso Premium).
- Ordenação: os links de paginação trazem `sortBy=EpubDate_asc`, e as datas exibidas
  dos 482 registros não decrescem em nenhum ponto (0 inversões; de abril/2022 a
  setembro/2026). A interface não mostra um rótulo de ordenação legível no HTML;
  a confirmação vem do parâmetro e da sequência das datas.
- Diferenças inevitáveis: nenhuma de parâmetro. O índice da ACM pode ter mudado
  entre 29/10 e 01/11; não há como fixá-lo.

## Arquivos

- `captura.json.gz`: o arquivo baixado do navegador (12.662.129 bytes antes da
  compressão; SHA-256 do JSON descomprimido
  `b53afcaf58c6a099b1fcc2d652c92fa916d86a16df71535e16518a38e8ffaa03`), comprimido com
  `gzip -n -9`. Contém, para cada página: URL, hora, status HTTP, total exibido
  (`.hitsLength`), número de itens, o HTML bruto completo e a extração feita no
  navegador ([posição, tipo, data exibida, DOI, título]). Inclui `p-010` (página após
  a última, vazia) e `verificacao-final-000` (página 1 consultada de novo no fim).
- `consulta.txt`: a consulta.
- `registros.csv`: os 482 registros reextraídos do HTML bruto em Python
  (`scripts/verificar_acm.py`), com tipo, data exibida, DOI, título completo e data de
  publicação (`data-title="Published: ..."`).
- `comparacao.csv`: cada DOI com a situação (`ambos`, `so_nova`, `so_anterior`),
  registro e estudo atuais, igualdade de tipo, data e título frente a 29/10, data de
  publicação e se ela é posterior a 07/09/2026.
- `manifesto.txt`: SHA-256 dos arquivos acima (conferido pelo `make check`).

## Resultado

- Total exibido: 482 em todas as 12 consultas (sem variação durante a coleta).
- Paginação: 9 páginas com 50 itens, a décima com 32, a seguinte vazia; posições 1 a
  482 contínuas; a página 1 consultada no fim é idêntica à do início.
- 482 linhas, 482 DOIs distintos, nenhuma repetição, nenhum registro sem DOI.
- Comparação com os 482 DOIs de 29/10 (`dados/registros.csv`, B3): 482 em ambos,
  0 só na nova coleta, 0 só na anterior. Tipo e data exibida iguais nos 482.
- Títulos: 3 diferenças, todas por truncamento na extração do navegador (o script lia
  só o link do título, que não inclui o subtítulo). A extração de 29/10 tinha o mesmo
  defeito; as correções estão em `dados/correcoes_registros.csv` (D40).
- Datas de publicação: 29 registros publicados depois de 07/09/2026 (o filtro mensal
  da ACM vai até 30/09); tratamento no encaminhamento de I4 (D41).

## Limitações

- Mesma conta (Basic, sem login) e mesmo navegador de 29/10; a ACM não oferece
  exportação nessa edição, então a coleta continua sendo leitura das páginas.
- A coleta confirma o conjunto de 01/11; não prova qual era a resposta da ACM em 29/10
  além do que foi preservado naquele dia.
- Este arquivo é documentação; o `manifesto.txt` não o cobre.
