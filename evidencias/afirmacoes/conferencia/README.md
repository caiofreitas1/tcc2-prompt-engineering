# Conferência das afirmações empíricas (T12)

Preparada por Claude Code (Claude Opus 5.5) em 17/11/2026, a pedido do autor («Sim, preparar»).
A conferência é do autor; nada aqui é revisão humana até que os julgamentos sejam gravados.

- Formulário: https://claude.ai/artifact/GZqmTGomTn6Y47s1yRE7Sw (privado). Julgamentos na
  coleção `afirmacoes_autor`: `sustentada`, `corrigir` ou `nao_verificavel`, com nota e o
  SHA-256 do texto registrado em `dados/afirmacoes.csv`.
- Gerado por `python3 scripts/gerar_formulario_afirmacoes.py` a partir de `modelo.html`.
- Itens: as 120 afirmações (113 na primeira versão; A119–A125, sobre outras revisões e a rubrica, entraram em D122, com o PDF local de cada referência) marcadas no LaTeX (`% AFIRMACAO: A<n>`), cada uma com o trecho em
  que aparece (14 aparecem também na discussão), o texto registrado e as comparações que a
  sustentam, com valores, localizador, citações literais e o PDF local do estudo.
- Fora do formulário: A1–A5, afirmações do piloto que não aparecem mais no texto.
- Depois da conferência: as afirmações sustentadas passam a `sustentada` com revisor e data.
  O verificador exige, para isso, que as extrações citadas tenham status `conferido_original`,
  o que depende também dos metadados conferidos; essa dependência será tratada ao importar.

## Resultado (D124)

- O autor julgou as 120 afirmações em 17/11/2026: 89 sustentadas, 30 a corrigir e 1 não verificável (A84).
  Julgamentos em `julgamentos-autor.json`.
- As correções de 29 afirmações e a reformulação de A84 foram aplicadas no texto e em `dados/afirmacoes.csv`.
  A nota de A106 repete a de A77 e não foi aplicada; aguarda o autor.
- O estado das afirmações continua `rascunho`, com revisor e data nas sustentadas, porque `sustentada` exige
  extrações `conferido_original`, que dependem de metadados conferidos.
