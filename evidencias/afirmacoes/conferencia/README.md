# Conferência das afirmações empíricas (T12)

Preparada por Claude Code (Claude Opus 5.5) em 17/11/2026, a pedido do autor («Sim, preparar»).
A conferência é do autor; nada aqui é revisão humana até que os julgamentos sejam gravados.

- Formulário: https://claude.ai/artifact/GZqmTGomTn6Y47s1yRE7Sw (privado). Julgamentos na
  coleção `afirmacoes_autor`: `sustentada`, `corrigir` ou `nao_verificavel`, com nota e o
  SHA-256 do texto registrado em `dados/afirmacoes.csv`.
- Gerado por `python3 scripts/gerar_formulario_afirmacoes.py` a partir de `modelo.html`.
- Itens: as 113 afirmações marcadas no LaTeX (`% AFIRMACAO: A<n>`), cada uma com o trecho em
  que aparece (14 aparecem também na discussão), o texto registrado e as comparações que a
  sustentam, com valores, localizador, citações literais e o PDF local do estudo.
- Fora do formulário: A1–A5, afirmações do piloto que não aparecem mais no texto.
- Depois da conferência: as afirmações sustentadas passam a `sustentada` com revisor e data.
  O verificador exige, para isso, que as extrações citadas tenham status `conferido_original`,
  o que depende também dos metadados conferidos; essa dependência será tratada ao importar.
