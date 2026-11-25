# Publicações dos estudos identificados pelo arXiv

Coleta de 21/11/2026 por Claude Code (Claude Fable 5.2), para `dados/publicacoes.csv` (D135).

`evidencia.json.gz`: por estudo, os metadados do arXiv (`export.arxiv.org/api/query`: versão mais recente, título,
autores, `doi`, `journal_ref`, `comment`) e o registro que sustenta a publicação: item do Crossref
(`api.crossref.org/works?query.bibliographic=`título e sobrenome do primeiro autor), entrada do BibTeX do volume na
ACL Anthology (`aclanthology.org/volumes/<volume>.bib`), BibTeX oficial dos anais do ICLR 2025 ou registro do DOI
no DataCite (`doi.org`, formato CSL). O OpenAlex (`api.openalex.org/works`) foi usado só para localizar candidatos.

Critério de correspondência: título normalizado igual ao do arXiv e autores coincidentes. S328 e S1086 foram
publicados com título mais longo e aceitos pelos autores idênticos e pelo título do arXiv contido no publicado.
Variações de grafia de nomes e autores a mais na publicação (S357, S633) estão em `dados/publicacoes.csv`.
Só metadados foram conferidos; o texto das publicações não foi lido.
