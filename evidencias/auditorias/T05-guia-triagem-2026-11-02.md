# Auditoria por IA do guia de triagem do piloto — T05

Objeto: guia "Guia da triagem do piloto (T05)" (Claude Docs,
https://claude.ai/artifact/4TVMdTnmvSDoW7dbL83D6b), versão de 01/11/2026 exportada
pelo autor em Markdown, confrontada com `protocolo/protocolo.md`,
`protocolo/prompts/triagem-titulo-resumo.md` (tr-v1) e D41–D43, na branch
`t05/triagem-titulo-resumo`.

Executor/data: Codex (IA), 02/11/2026, a pedido do autor. O Codex declarou não ter
acessado a pasta selada, o formulário nem decisões de triadores.

Natureza: auditoria por IA. Não é revisão humana.

## Parecer do Codex (abertura citada; achados resumidos)

O guia é parcialmente fiel, mas precisa de ajustes antes de orientar a triagem. O principal problema é transformar interpretações das zonas cinzentas em condições adicionais de elegibilidade, especialmente exigir "código como produto avaliado".

Achados (resumo dos 13 itens; os trechos citados e as referências estão na
conversa de 02/11/2026 e foram verificados no guia antes da correção):

| # | Gravidade | Achado |
|---|---|---|
| 1 | Crítico | I2/X3: o guia exigia "código como produto avaliado", condição ausente do protocolo, e lhe dava consequência de exclusão no roteiro |
| 2 | Importante | I2: teste adicional "executável ou compilável como um programa" para artefatos de fronteira |
| 3 | Importante | Zonas cinzentas: centralidade temática ("código é só um dos benchmarks?") e avaliação direta do código; âncora favorável no S3 |
| 4 | Importante | I2/X4: tratamento inconsistente de decodificação e métodos mistos ("coadjuvante") |
| 5 | Importante | I3: exigia resultados no resumo; "estudo sério" introduzia julgamento de qualidade; I1 misturado com I3 |
| 6 | Importante | X2: contradição entre tabela, lembretes e roteiro |
| 7 | Importante | X3: exemplo sem a ressalva "apenas" |
| 8 | Importante | X5 com "livro" como categoria; equivalência categórica entre veículos, contra a seção 3 |
| 9 | Importante | Incluir e Dúvida tratados como equivalentes, embora a regra de parada conte só Incluir; codificação do κ indefinida |
| 10 | Importante | Limites de revisão das seções 7 e 8 sem articulação; faltava o registro da revocação como limitação |
| 11 | Importante | Projeção de horas sem a abrangência de todos os pontos de controle; "sem custo" contraditório |
| 12 | Menor | D41: faltavam a pendência de I4, quem busca o resumo e o motivo "resumo ausente" |
| 13 | Menor | I5/X7: idioma do resumo não comprova o do texto |

Observação final do Codex: acrescentar regras apenas ao guia humano criaria
condições metodológicas diferentes entre os triadores, já que IA-A e IA-B usaram
tr-v1.

## Tratamento (Claude Code, Claude Opus 5.5, 02/11/2026)

Os 13 achados procedem e foram corrigidos no guia (revisão 23 do documento):

- Princípio declarado na abertura: o guia só explica o protocolo e tr-v1; onde o
  protocolo não resolve, a orientação é Dúvida (observação final, achados 1–4).
- I2 sem "código como produto"; tarefa indeterminada → Dúvida; X3 só com clareza de
  ausência de tarefa elegível, com "apenas" (1, 7).
- Artefatos de fronteira declarados como não resolvidos pelo protocolo → Dúvida (2).
- Zonas cinzentas reescritas em termos de I2, I3, X3 e X4, sem âncora no S3 e sem
  condições novas (3, 4).
- I1 separado de I3; I3 não exige resultados no resumo; "sério" retirado (5).
- X2 distinguido de falta de informação, com Dúvida no caso indistinto (6).
- X5 ligado à natureza do trabalho; veículo não decide I1–I3, com a identificação
  separada de preprints e literatura cinzenta (8).
- Incluir e Dúvida diferenciados pela regra de parada; codificação do κ proposta em
  D44 antes da abertura dos selos (9).
- Seções 7 e 8 articuladas e revocação persistente como limitação (10).
- Projeção de horas com todos os pontos de controle; "sem custo" substituído (11).
- Pendência de I4, busca do resumo por Claude Code e motivo "resumo ausente" (12).
- Idioma incerto → Dúvida (13).
