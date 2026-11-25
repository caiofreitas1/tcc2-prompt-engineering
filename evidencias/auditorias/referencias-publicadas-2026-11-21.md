# Conferência das versões publicadas das referências

Data: 21/11/2026. Executor: Claude Code (Claude Fable 5.2). Natureza: conferência de metadados por IA, sem
revisão humana registrada.

Origem: comentário de uma avaliadora da banca, relatado pelo autor em conversa: «por referencias das revistas
publicadas e nao do arxiv no fim do trabalho».

## Constatação

O comentário procede. Das 26 entradas de `monografia/referencias.bib`, 17 eram manuscritos do arXiv
(`@misc`). Catorze delas têm versão publicada em periódico ou em anais de conferência.

## Método

Para cada uma das 17 entradas, em 21/11/2026:

1. API do arXiv (`export.arxiv.org/api/query`), campos `doi`, `journal_ref` e `comment`;
2. Crossref (`api.crossref.org/works`), busca pelo título e, depois, registro completo de cada DOI;
3. OpenAlex (`api.openalex.org/works`), pelo DOI do arXiv, lista de locais de publicação;
4. BibTeX oficial dos anais, em `proceedings.neurips.cc` e `proceedings.iclr.cc`;
5. Semantic Scholar (`api.semanticscholar.org`), para os casos sem versão publicada nas consultas anteriores;
6. página dos anais do PLoP 2023 (destino do DOI) e página do artigo no site do ICLR 2023.

O DBLP e a API do OpenReview recusaram pedidos automatizados e não foram usados. Só os metadados foram
conferidos: o texto das versões publicadas não foi lido nem comparado com o do arXiv.

## Resultado

| Chave | arXiv consultado | Versão publicada adotada | Fonte da conferência |
|---|---|---|---|
| `jiang2025selfplanningv5` (S1) | 2303.06689v5 | ACM TOSEM, v. 33, n. 7, p. 1–30, 2024, DOI 10.1145/3672456 | Crossref |
| `vaswani2017attention` | 1706.03762v7 | NeurIPS, v. 30, 2017 | BibTeX dos anais (sem páginas) |
| `brown2020fewshot` | 2005.14165v4 | NeurIPS, v. 33, p. 1877–1901, 2020 | BibTeX dos anais |
| `liu2021pretrain` | 2107.13586v1 | ACM Computing Surveys, v. 55, n. 9, p. 1–35, 2023, DOI 10.1145/3560815 | Crossref |
| `wei2022cot` | 2201.11903v6 | NeurIPS, v. 35, p. 24824–24837, 2022, DOI 10.52202/068431-1800 | Crossref |
| `yao2023react` | 2210.03629v3 | ICLR 2023 | Comentário do arXiv («v3 is the ICLR camera ready version»), site do ICLR 2023, Semantic Scholar |
| `white2023patterns` | 2302.11382v1 | Anais do PLoP 2023, DOI 10.64346/PLoP2023p05 | Página dos anais e Crossref |
| `chen2023selfdebug` (S2) | 2304.05128v2 | ICLR 2024, p. 8746–8825 | BibTeX dos anais |
| `fan2023survey` | 2310.03533v4 | ICSE-FoSE 2023, p. 31–53, DOI 10.1109/ICSE-FoSE59343.2023.00008 | Crossref |
| `jimenez2024swebench` | 2310.06770v3 | ICLR 2024, p. 54107–54157 | BibTeX dos anais |
| `shinn2023reflexion` (S3) | 2303.11366v4 | NeurIPS, v. 36, p. 8634–8652, 2023, DOI 10.52202/075280-0377 | Crossref |
| `cordeiro2024refactoring` (S4) | 2411.02320v1 | ACM TOSEM, v. 35, n. 12, p. 1–42, 2026, DOI 10.1145/3801158 | Crossref |
| `perry2023insecure` (S5) | 2211.03622v3 | ACM CCS '23, p. 2785–2799, DOI 10.1145/3576915.3623157 | API do arXiv e Crossref |
| `yang2025aprsurvey` (S820) | 2506.23749v3 | ACM TOSEM, 2026, DOI 10.1145/3845995, sem volume atribuído | OpenAlex e Crossref |
| `chen2021codex` | 2107.03374v2 | não localizada; permanece arXiv | arXiv, Crossref, OpenAlex, Semantic Scholar |
| `sahoo2024survey` | 2402.07927v2 | não localizada; permanece arXiv | arXiv, Crossref, OpenAlex, Semantic Scholar |
| `masthanali2026energy` (S1246) | 2603.00989v4 | não localizada; permanece arXiv | arXiv, Crossref, OpenAlex, Semantic Scholar |

`hou2024slr` já era citado pela TOSEM; recebeu só a indicação da versão consultada (arXiv 2308.10620v6, D122).

## Diferenças entre a versão publicada e a do arXiv

- **Reflexion:** os anais do NeurIPS 2023 listam cinco autores (Shinn, Cassano, Gopinath, Narasimhan e Yao).
  Edward Berman consta só no arXiv v4. A referência segue os anais.
- **Yang et al. (S820):** a TOSEM publicou o artigo com «Software Repair» no título; a entrada anterior trazia
  «Automated Program Repair», da primeira versão no arXiv. Publicação antecipada em 02/11/2026, sem volume.
- **Jiang et al. (S1):** o ano da referência passa de 2025 (arXiv v5) para 2024 (TOSEM). Os resultados
  extraídos continuam sendo os do arXiv v5, como registram `dados/estudos.csv` e `dados/afirmacoes.csv`.
- **Cordeiro et al. (S4):** o fascículo saiu em 18/11/2026; o DOI já constava no registro B3-0040 da busca.
- **Vaswani et al. e Brown et al.:** nomes como nos anais («Łukasz Kaiser», «Tom Brown»).
- **White et al.:** o Crossref registra The Hillside Group como editora e 24/06/2024 como data do depósito; a
  página dos anais sugere «ACM, 2023». Adotados The Hillside Group e 2023, ano da conferência e dos anais.
- **Vaswani et al.:** o BibTeX dos anais não traz páginas; o Semantic Scholar informa 5998–6008. Como só a
  fonte secundária traz o intervalo, ele ficou fora da referência.

## Regra adotada

A referência é a da publicação. O campo `note` de cada entrada registra a versão do arXiv em que o texto foi
consultado, porque nenhuma leitura foi feita na versão da editora. As chaves do BibTeX foram mantidas. Em
`02-fundamentacao.tex`, «nas versões citadas» passou a «nas versões do arXiv indicadas nas referências».

## Apêndice de estudos incluídos (D135)

O apêndice identificava 69 dos 332 estudos pelo número do arXiv e 263 pelo DOI (`dados/estudos.csv`). Com a
decisão do autor («Sim, trocar», 21/11/2026), a mesma conferência foi feita para os 69 estudos.

Método: metadados na API do arXiv; busca no Crossref por título e sobrenome do primeiro autor; locais de
publicação no OpenAlex; para os casos sem DOI no Crossref, BibTeX dos volumes na ACL Anthology, BibTeX oficial
dos anais do ICLR 2025 e registro do DOI no DataCite. Critério: título normalizado igual ao do arXiv e autores
coincidentes.

| Situação | Estudos |
|---|---|
| DOI da publicação, conferido no Crossref | 61 |
| DOI da publicação, conferido no DataCite (S588, BTW 2025) | 1 |
| Anais sem DOI localizado: ACL Anthology (S447, S547, S878, S910) | 4 |
| Anais sem DOI localizado: ICLR 2025 (S479) | 1 |
| Sem publicação localizada; continuam pelo arXiv (S553, S1132) | 2 |

Observações:

- **S328 e S1086:** publicados com título mais longo, que contém o do arXiv; autores idênticos.
- **S328:** o DOI da publicação é o do registro S1749, que o autor já havia excluído por X1 como duplicata de
  S328 em 08/11/2026. A contagem do corpus não muda.
- **S357 e S633:** a publicação lista mais autores que o arXiv (20 contra 18; 9 contra 8).
- **S553:** há em Findings of ACL 2025 um artigo de título diferente dos mesmos primeiros autores
  (10.18653/v1/2025.findings-acl.509). A correspondência não foi confirmada, e o estudo continua pelo arXiv.
- **S1132:** o arXiv informa um workshop do NeurIPS 2025; não foram localizados anais com identificador.
- Em oito estudos há variação na grafia de um nome entre o arXiv e a publicação (por exemplo, «Alex» e
  «Alexander»); nenhuma indica autor diferente.
- Os textos dos 67 estudos foram obtidos em `arxiv.org` (`evidencias/lote/textos.csv`); o apêndice marca esses
  estudos e informa que a leitura foi feita na versão do arXiv. O site continua apontando para o arXiv.

Dados: `dados/publicacoes.csv`. Registros de apoio: `dados/brutos/publicacoes-2026-11-21/`.
