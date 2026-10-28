# Prompts da revisão

Prompts usados pelos triadores e extratores de IA (protocolo, seções 6 e 9).
Cada arquivo tem versão no cabeçalho; a versão é registrada em `prompt_versao`
(`dados/triagem.csv`) ou no campo homônimo da extração.

| Arquivo | Versão | Situação |
|---|---|---|
| [triagem-titulo-resumo.md](triagem-titulo-resumo.md) | tr-v1 | Rascunho; calibrar no lote piloto (T05) |
| [triagem-texto-completo.md](triagem-texto-completo.md) | tc-v1 | Rascunho; calibrar nos primeiros textos (T06) |
| [extracao.md](extracao.md) | ex-v1 | Rascunho; calibrar com S1 e dois estudos incluídos (T07) |

Regras:
- Congelar a versão antes do lote principal. Mudanças depois disso geram nova
  versão, com motivo em `contexto/decisoes.md`; decisões anteriores não são
  reescritas.
- IA-A e IA-B recebem exatamente o mesmo prompt, em contextos independentes.
- O conteúdo dos artigos é dado, não instrução: o prompt não deve obedecer a
  comandos encontrados em títulos, resumos ou textos.
