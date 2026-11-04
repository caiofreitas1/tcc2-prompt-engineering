# Prompts da revisão

Prompts usados pelos triadores e extratores de IA (protocolo, seções 6 e 9).
Cada arquivo tem versão no cabeçalho; a versão é registrada em `prompt_versao`
(`dados/triagem.csv`) ou no campo homônimo da extração.

| Arquivo | Versão | Situação |
|---|---|---|
| [triagem-titulo-resumo.md](triagem-titulo-resumo.md) | tr-v1 | Usada na amostra 1 do piloto (T05); substituída após a regra de parada |
| [triagem-titulo-resumo-v2.md](triagem-titulo-resumo-v2.md) | tr-v2 | Congelada em 03/11/2026 (D64), SHA-256 `512494e7…c67e` |
| [triagem-texto-completo.md](triagem-texto-completo.md) | tc-v1 | Rascunho usado na medição de 12 textos (D51, D55); substituída por tc-v2 (D59) |
| [triagem-texto-completo-v2.md](triagem-texto-completo-v2.md) | tc-v2 | Congelada em 03/11/2026 (D64), com a interpretação de I2 e X4 de D59, SHA-256 `7b421f47…d963` |
| [extracao.md](extracao.md) | ex-v1 | Rascunho; calibrar com S1 e dois estudos incluídos (T07) |

Regras:
- Congelar a versão antes do lote principal. Mudanças depois disso geram nova
  versão, com motivo em `contexto/decisoes.md`; decisões anteriores não são
  reescritas.
- IA-A e IA-B recebem exatamente o mesmo prompt, em contextos independentes.
- O conteúdo dos artigos é dado, não instrução: o prompt não deve obedecer a
  comandos encontrados em títulos, resumos ou textos.
