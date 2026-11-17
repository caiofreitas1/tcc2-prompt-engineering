# Contrafactuais dos sistemas comparadores: S6, S216 e casos análogos (D107)

Claude Code (Claude Opus 5.5), 17/11/2026, a pedido do autor. Conferência nas imagens das
páginas: S6 p. 8 (Tabelas 1 e 2), S216 p. 12 (Tabela 8), S724 p. 8 (Tabela I), S1415 p. 16
(Tabela 4) e S1977 p. 5 (Tabela I). Nenhuma ficha foi alterada: o que segue é proposta para
decisão do autor.

## A distinção

O prompt ex-v2.2 tem duas regras que se cruzam:
- `avaliada_isoladamente` = `sim` exige condição contrafactual no estudo, com e sem a técnica,
  em condições comparáveis; `pacote` é «o pacote completo comparado com a condição sem ele», e
  `sim` para o pacote não autoriza atribuir o ganho a um único mecanismo.
- «Sistemas comparadores cujos mecanismos não são isolados recebem `nao`.»

Lida ao pé da letra, a segunda regra dá `nao` a todo comparador que é um pacote de vários
mecanismos, mesmo quando o estudo traz a condição sem ele. Isso confunde dois planos:
- **avaliação do pacote:** a técnica inteira contra a condição de base, no mesmo modelo,
  benchmark e métrica. Basta para `sim` / `pacote`;
- **isolamento dos ingredientes:** retirar um mecanismo mantendo os demais. É o que `pacote`
  já declara não ter; só `ingrediente` ou `contraste_pareado` o afirmam.

As correções manuais que fiz em S6, S216, S724, S1415 e S1977 (`pacote` → `nenhum`, mantendo
`nao`) seguiram a segunda regra. Mas `nenhum` afirma que não há contrafactual, o que as
tabelas desmentem. A classificação coerente com a distinção acima é `sim` / `pacote`, com a
observação de que os ingredientes não são isolados. A saída bruta tinha `nao` / `pacote`
(incoerente); a proposta muda `avaliada_isoladamente`, não o tipo.

## S6 (correção não confirmada) — base: Direct prompting

Tabelas 1 (LLaMA3-8B-Instruct) e 2 (LLaMA3-70B-Instruct), p. 8: todas as condições na mesma
tabela, com o mesmo modelo, os mesmos quatro benchmarks e as mesmas métricas (pass@1, n = 10;
pass-ratio@10). Direct prompting é a condição sem técnica (o código gerado só a partir da
descrição do problema).

| Comparador | Par (Tabela 1, HumanEval, pass@1) | Proposta | Ingredientes não isolados |
|---|---|---|---|
| Few-shot (1, 2 e 3 exemplos) | Direct 54,4 × 1-shot 47,8 / 2-shot 47,2 / 3-shot 45,4 | `sim` / `pacote` | exemplos e contexto juntos; cada número de exemplos é um pacote; fora do LiveCodeBench por limite de contexto |
| CodeCoT | Direct 54,4 × 57,5 | `sim` / `pacote` | raciocínio, decomposição e exemplo one-shot juntos; contra Zero-shot CoT difere em mais de um ingrediente (exemplo e cadeias curadas), então não há contraste pareado |
| Zero-shot CoT | Direct 54,4 × 59,8 | `sim` / `pacote` | raciocínio e encadeamento em duas etapas juntos |
| Self-Planning | Direct 54,4 × 60,1 | `sim` / `pacote` | decomposição em plano e exemplos juntos |
| Self-Pseudo | Direct 54,4 × 52,4 | `sim` / `pacote` | requisitos, pseudocódigo e encadeamento em três etapas juntos |

Sem mudança: Direct prompting continua `nao` / `nenhum` (é a própria base), e a variante do
CGO continua `nao` / `nenhum` (a Tabela 7 não tem condição sem CGO).

## S216 (correção não confirmada) — base: Pass@1 sem CoT

Tabela 8, p. 12: para cada ℓLM e corpus (HE, OE, HE-p), a coluna Pass@1 é o prompt original
sem CoT, e as colunas CoT-Pass@1 trazem o mesmo ℓLM com a CoT de cada gerador concatenada ao
prompt. Muda só a fonte da CoT; modelo, corpus e métrica são os mesmos.

| Comparador | Par (Tabela 8, HE, CodeGen 350M) | Proposta | Ingredientes não isolados |
|---|---|---|---|
| CoT do Gemini, do CodeLlama e do ChatGLM (técnica agrupada na ficha) | sem CoT 14,63 × Gemini 24,39 / CodeLlama 18,90 / ChatGLM 18,29 | `sim` / `pacote`, uma comparação por coluna | modelo gerador, exemplos do prompt do gerador e, no CodeLlama, ausência de ajuste fino, todos juntos |
| Teacher (gpt-3.5-turbo, CoT one-shot) | sem CoT 14,63 × 24,39 | `sim` / `pacote` | modelo e exemplo do prompt juntos |

A proposta também alinha a ficha consigo mesma: Think step by step, Self-planning e SCoT, na
mesma S216, já tinham `sim` / `pacote` do extrator contra o Pass@1 sem CoT da Tabela 7.

## Casos análogos já confirmados pelo autor (sem alteração)

O autor confirmou em D106 as correções de S724, S1415 e S1977 como consistência de registros.
A mesma distinção indica que também nelas os comparadores têm contraste de pacote:

| Estudo | Base e tabela | Pares | Proposta | Ressalva |
|---|---|---|---|---|
| S724 | Original (descrição sem reparo, geração zero-shot), Tabela I, p. 8, mesmo modelo e benchmark | DeepSeek, HumanEval+, Pass@1: Original 87,8 × Original + µFix 88,9 / Vanilla Repair 84,8 / ClarifyGPT-auto 89,0 | `sim` / `pacote` nos três | µFix muda o método de geração, não a descrição; Vanilla Repair e ClarifyGPT reescrevem as descrições |
| S1415 | A (sem injeção), Tabela 4, p. 16, Round 0, os mesmos 10 modelos e 2.000 itens | média: A 5,79 × X 38,13 / R 10,99 / R_sem 12,05 | `sim` / `pacote` em X, R e R_sem | a técnica agrupa R_sem e R_semB; R_semB (orçamento igualado, Tabela 9) é pacote híbrido, com componente de orçamento fora do escopo |
| S1977 | Native Baseline (zero-shot, sem restrições), Tabela I, p. 5, HumanEval, Pass@1 | 40,2 × Expert Prompt 30,5 / CoT 70,5 / Self-Refine 78,0 / ReAct+AST 70,4 | `sim` / `pacote` nos quatro, se o autor aceitar a comparabilidade | a tabela só nomeia o modelo (Qwen2.5-1.5B) na linha de base; a coluna «Improvement» relativa à base sugere o mesmo modelo, mas não o declara por linha; se o autor não aceitar, fica `nao` / `nenhum` |

S2085 (D106) já segue a distinção: `sim` / `pacote`, com a observação de que o few-shot não é
isolado.

## Alcance no corpus

Nas 302 fichas finais do corpus, 583 técnicas com papel `comparador` têm `nao` / `nenhum`, e
34 têm `sim` / `pacote`. Parte das 583 é a própria condição de base, corretamente `nao`. Uma
busca nas observações por menções explícitas a contraste de pacote ou à mesma tabela achou
dez estudos com esse padrão (S6, S195, S216, S233, S604, S724, S1415, S1863, S2048 e S2118);
a busca não esgota os casos. Se o autor adotar a distinção, ela vira regra de leitura do
prompt congelado, e os comparadores das fichas precisam de uma revisão dirigida (lista gerada
por script e conferência nas tabelas), com cada mudança registrada como correção manual.

## Decisões pedidas ao autor

1. S6 e S216: substituir as correções pendentes (`nao` / `nenhum`) por `sim` / `pacote` nos
   comparadores das tabelas acima.
2. S724, S1415 e S1977: rever as correções já confirmadas, pela mesma distinção. Na S1977,
   decidir se a Tabela I basta para a comparabilidade.
3. Corpus: adotar a distinção como regra e autorizar a revisão dirigida dos comparadores.
