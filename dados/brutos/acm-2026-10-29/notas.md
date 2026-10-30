# Busca ACM Digital Library — 29/10/2026

- Busca avançada (Title e Abstract), consulta em `consulta.txt`, filtro de publicação
  eletrônica 01/2021–09/2026 (granularidade mensal; o limite de 07/09/2026, I4, é
  conferido na triagem). "The ACM Full-Text Collection". Resultado exibido: 482.
- Executada no Chrome do autor (extensão Claude in Chrome): o navegador do app foi
  barrado pela verificação da Cloudflare.
- A exportação de citações é recurso Premium na edição Basic e não estava disponível.
  Os registros foram extraídos das páginas de resultados (50 por página): posição, tipo,
  data, DOI e título. Sem resumo; os resumos serão obtidos pelo DOI antes da triagem.
- `extracao-ordenada-por-relevancia.json`: primeira passada (ordem padrão). A ordem por
  relevância variou entre páginas: 2 DOIs repetidos (10.1145/3712255.3726700,
  10.1145/3808347) e 2 ausentes.
- Segunda passada ordenada por data (`sortBy=EpubDate_asc`): 482 DOIs distintos. O
  Chrome bloqueou o download automático desse arquivo; os 2 registros ausentes da
  primeira passada foram copiados dela para `complemento-ordenado-por-data.json`.
- `pagina-001.json` a `pagina-010.json`: primeira passada sem as 2 repetições;
  `pagina-011.json`: o complemento. Total: 482 = contagem da ACM.
- Executor: Claude Code (Claude Opus 5.5).
