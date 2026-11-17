# Extração em escala — lote 17 (D114)

Claude Opus 5.5 (subagentes, Read e Write), 17/11/2026, prompt ex-v2.2 congelado
(`f738eb50…c96d`), uma rodada (r1). Os 29 estudos incluídos pelo autor na última leva da
etapa 3: S1624, S1636, S1655, S1682, S1684, S1688, S1702, S1713, S1715, S1721, S1735, S1738,
S1748, S1754, S1778, S1807, S1809, S1847, S1869, S1871, S1875, S1880, S1883, S1886, S1888,
S1926, S1929, S1931 e S1935.

- As 29 saídas passam no validador; fichas finais idênticas às brutas, salvo S1883, com uma
  correção de unidade (speed-up 2X rotulado como proporção; unidade nao_informado, pela
  regra de D106).
- 50 comparações: 34 melhora, 7 piora, 2 igual, 7 sem direção definida ou descritivas.
- Sem nenhuma comparação de prompting: S1886 (compara GPT-4.1 e Claude 3.7 Sonnet com o
  mesmo prompt) e S1721 (a técnica de prompting só detecta viés; a mitigação é RLHF e LoRA).
  Em S1929, a técnica focal usa embeddings treináveis e ficou fora do escopo; a única
  comparação é de uma linha de base de prompting. S1721 e S1929 foram exclusões
  consensuais das duas IAs no texto completo e inclusões do autor; os três ficam para o
  autor reexaminar a elegibilidade.
- Só descritivas, sem comparador: S1624, S1715, S1809, S1875 e S1883.
- S1778: o extrator identificou na Fig. 2 os modelos do COM (DeepSeek-Coder-V2-Instruct e
  Qwen2.5-Coder-7B-Instruct), que o texto extraído não traz.
- As fichas não foram conferidas pelo autor. Seis estudos entram no complemento da amostra
  de conferência (S1682, S1721, S1735, S1869, S1875 e S1926).

## S667 (Codex, 17/11/2026)

Extraído pelo Codex CLI 0.169.0 (gpt-6.1-sol, esforço high), depois que a gravação pelo
Opus foi interrompida por filtro de segurança. Uma comparação: CodeJailbreaker contra EMP
no RMCBench (texto para código, 182 prompts) com DeepSeek-V3, taxa de sucesso do ataque de
61,54% para 93,41%. «Melhora» aqui é no sentido da métrica do estudo (sucesso do ataque),
relevante para a QP2. Ficha não conferida pelo autor.
