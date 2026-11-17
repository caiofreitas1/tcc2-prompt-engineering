# Exame da tabela de apoio v1 nos oito cenários (proposta para julgamento do autor)

Claude Code (Claude Opus 5.5), 17/11/2026, sobre os cenários v2 e a tabela de apoio v1 congelados
(`cenarios-congelamento.txt`). Em cada cenário, o exame aplica as linhas da tabela (numeradas como em
`tabela-apoio-v1.csv`) e confere os estudos citados nas fichas. Os julgamentos abaixo são **propostas**; o julgamento
final é do autor. As fichas são extração por IA, ainda em conferência.

Escala: `atende`, `parcial`, `nao_atende`. Critérios: clareza (C), justificativa nas fontes (J) e orientação
concreta (O).

---

## G1 — Funções Python com testes, modelo grande, até 5 chamadas

**Linhas aplicadas:** 9 (testes no prompt), 1 (*feedback* de execução), 4 (amostragem e seleção), 6 (planejamento),
5 (CoT), 3 (multiagente).

**Orientação derivada da tabela**
1. Pôr os testes públicos no prompt (linha 9).
2. Usar o orçamento num laço de *feedback* com os testes (linha 1). Como a linha 1 registra ausência de ganho
   quando o orçamento de tentativas é igualado, comparar localmente com a amostragem de até 5 candidatos e
   seleção pelos testes (linha 4).
3. O planejamento antes do código é opcional e consome chamadas (linha 6).
4. Não usar a instrução de raciocínio como recurso isolado (linha 5).
5. Os pacotes multiagente usam mais chamadas que o orçamento permite (linha 3).

**Estudos e comparações**
- S150-C1: µFiX, pacote com *feedback*, Pass@1 de 73,78% para 90,24% (gpt-3.5-turbo-0613, HumanEval).
- S150-C2: retirar a fase de *feedback* deixa 85,37%.
- S1086-C4 e S1086-C5: testes no prompt, acurácia de 19,6% para 33,4% (um teste dado) e para 48,2% (teste dado
  e testes gerados), com Llama 3.2 3B.
- S479-C2: com 3 tentativas igualadas, multiturno com testes que falham 2,4% contra 2,9% (pass 1@3, Llama 3.0 8B,
  CodeContests).
- S645-C1: SEIDR 11,5 problemas resolvidos contra 12,2 da amostragem sem reparo (GPT-3.5, PSB2).
- S1-C1: *self-planning*, de 48,1% para 60,3% (code-davinci-002, HumanEval).
- S1747-C3: MapCoder com 8,1 chamadas em média.

**Limitações**
- Os ganhos de pacote não isolam o laço.
- Os estudos com orçamento igualado usam modelos abertos de 8B e problemas competitivos, e não um modelo comercial
  grande em funções simples.
- HumanEval tem risco de contaminação.
- Os modelos dos estudos são, em geral, anteriores à classe GPT-4o.

**Ambiguidades**
- A tabela não diz como repartir 5 chamadas entre rodadas de reparo e candidatos.
- A condição da linha 1 («base de chamada única») não coincide com um orçamento fixo.
- Usar os mesmos testes no prompt e na verificação pode favorecer soluções ajustadas aos testes públicos. A tabela
  só menciona esse risco na ressalva da linha 9 (S1613).

**Hipótese H-G1:** confirmada em parte. Há evidência suficiente para os elementos, mas não para a escolha sob
orçamento.

| Critério | Proposta | Justificativa |
|---|---|---|
| C | parcial | Várias linhas favoráveis se aplicam, sem prioridade entre elas sob orçamento fixo. |
| J | atende | Cada elemento tem comparações citadas, inclusive as contrárias com orçamento igualado. |
| O | parcial | Diz o que usar e o que evitar, mas não como gastar as 5 chamadas. |

---

## G2 — Solidity com modelo local de até 8B, compilador e analisador, até 3 chamadas

**Linhas aplicadas:** 1 (*feedback*: há compilador), 2 (autocrítica sem execução), 10 (instruções de segurança),
3 e 11. Nenhuma linha trata de Solidity ou do *feedback* de analisador estático.

**Orientação derivada da tabela**
- A evidência é insuficiente para recomendar uma técnica como padrão.
- Pode-se usar o compilador como *feedback* (linha 1), sabendo que a evidência vem de outros modelos e linguagens.
- Evitar a autocrítica sem execução com modelo pequeno (linha 2).
- Não confiar em instruções de segurança isoladas (linha 10).
- Multiagente e amostragem extensa excedem o orçamento.

**Estudos e comparações**
- S2055-C1: SolGen, Solidity, rodadas com o relatório de erros do Remix. Prompts com código compilável de 8 para 17
  (Llama 3.1). A comparação é cumulativa, sem condição paralela.
- S556: contexto de API e de dependências em vários domínios, incluindo Solidity. Só diferenças de CodeBLEU, com
  CodeLlama-7B.
- S996: descritivo, sem comparador.
- S1065-C1: Reflexion com *feedback* de segurança, de 72,86% para 84,47% (Qwen2.5-Coder-32B; C, C++, Java e
  outras; pacote).
- S1763-C3: relatório estático estruturado empatou com a autorrevisão genérica, 27 de 30 (deepseek-chat;
  HTML/JS).
- S759-C1: autocrítica pior com modelo de 1,5B.

**Limitações**
- Não há contraste de técnica de prompting em Solidity.
- A evidência sobre *feedback* de analisador vem de modelos maiores e de outras linguagens.
- A métrica de S556 (CodeBLEU) não mede correção nem segurança.

**Ambiguidades**
- A linha 1 não distingue *feedback* de compilador, de testes e de analisador estático.
- A tabela não tem linha de evidência insuficiente por linguagem ou por porte de modelo. O usuário precisa inferir
  a insuficiência a partir das ressalvas.

**Hipótese H-G2:** confirmada.

| Critério | Proposta | Justificativa |
|---|---|---|
| C | parcial | É preciso combinar quatro linhas e notar a ausência de evidência específica. |
| J | parcial | As fontes citáveis são de outras linguagens e portes; Solidity só tem estudo cumulativo ou descritivo. |
| O | parcial | Diz o que evitar, mas a insuficiência não está explícita numa linha. |

---

## D1 — Reparo de função Python com teste falhando, até 10 chamadas

**Linhas aplicadas:** 13 (informação diagnóstica), 12 (*feedback* de execução), 16 (raciocínio), 15 (exemplos).

**Orientação derivada da tabela**
1. Incluir no prompt o teste que falha e a mensagem de erro (linha 13).
2. Iterar com o resultado dos testes dentro do orçamento (linha 12).
3. Não acrescentar instrução de raciocínio (linha 16).
4. Não usar exemplos fixos (linha 15).

**Estudos e comparações**
- S1674-C5: saída dos testes, taxa de reparo de 62,5% para 70% (Qwen2.5-Coder 7B, QuixBugs, Python).
- S647-C2: teste disparador com mensagem de erro, de 34 para 59 correções corretas (WaveCoder 6,7B, Java,
  localização perfeita).
- S412-C3: *feedback* de interação, de 36 para 62, com até 5 interações (gpt-3.5-turbo).
- S62-C2: observações reais do depurador, 73% contra 63% das previstas.
- S275-C2 e S1598-C2: o raciocínio piorou.
- S1598-C1: exemplos fixos pioraram.

**Limitações**
- Vários estudos medem *patches* plausíveis (S62).
- Parte usa localização perfeita, o que aqui corresponde à função dada.
- Os modelos dos estudos são, em geral, menores ou mais antigos que o do cenário.

**Ambiguidades**
- A linha 13 registra piora com *stack trace* (S1678-C1, de 47 para 32 bugs localizados, tarefa de localização) e
  melhora com a saída dos testes (S1674-C5). Não fica claro se o *traceback* do cenário deve ser incluído.
- A linha 12 não diz quantas rodadas usar entre 1 e 10.

**Hipótese H-D1:** confirmada, com a ambiguidade do *traceback*.

| Critério | Proposta | Justificativa |
|---|---|---|
| C | parcial | A linha 13 tem sinais opostos para tipos próximos de informação. |
| J | atende | Comparações de ingrediente em Python e Java sustentam cada elemento. |
| O | atende | Diz o que incluir, o que evitar e que se deve iterar com testes. |

---

## D2 — Repositório Java com relato de defeito, sem teste de reprodução, até 20 chamadas

**Linhas aplicadas:** 14 (contexto recuperado), 17 (decomposição e agentes), 13 (relato de defeito). A linha 12
(*feedback*) não se aplica, porque não há teste que reproduza o defeito.

**Orientação derivada da tabela**
- As linhas 14 e 17 são favoráveis, mas quase toda a sua evidência supõe localização perfeita ou testes que
  disparam o defeito.
- Sem esses recursos, a tabela não sustenta recomendação.
- O relato de defeito no prompt é o único elemento com comparação favorável aplicável (linha 13), e mesmo ele foi
  medido com localização perfeita.

**Estudos e comparações**
- S647-C3: relato de defeito, de 34 para 72 correções corretas (WaveCoder 6,7B; localização perfeita em nível de
  linha).
- S303-C2: ferramentas de busca do RepairAgent, *patches* plausíveis de 14 para 23 (GPT-3.5, Defects4J, com testes
  disparadores).
- S2046-C2: busca interna de ingredientes, de 85 para 116 (GPT-4o, localização perfeita).
- S1304-C2: rastros de execução, de 154 para 177. Exige execução que reproduza o defeito.

**Limitações**
- O Defects4J fornece testes disparadores.
- A tabela não tem linha para reparo sem reprodução nem localização.

**Ambiguidades**
- As condições das linhas 14 e 17 («repositório, histórico» e «vários estágios») não dizem que a evidência supõe
  localização ou testes. Essa dependência só aparece nas ressalvas.

**Hipótese H-D2:** confirmada.

| Critério | Proposta | Justificativa |
|---|---|---|
| C | parcial | As linhas favoráveis parecem aplicáveis até que se leiam as ressalvas. |
| J | parcial | Há estudos citáveis, mas em condições diferentes das do cenário. |
| O | nao_atende | A tabela não diz explicitamente que a evidência é insuficiente sem reprodução e localização, e pode induzir a uma recomendação indevida. |

---

## T1 — C para Rust com compilador e testes, até 5 rodadas

**Linhas aplicadas:** 18 (reparo com *feedback*), 19 (exemplos), 20 (explicação em duas etapas).

**Orientação derivada da tabela**
1. Usar o reparo iterativo com o compilador e os testes, até 5 rodadas (linha 18).
2. Incluir testes no prompt.
3. Não acrescentar etapa de explicação (linha 20).
4. Exemplos não são recomendados como padrão (linha 19).

**Estudos e comparações**
- S732-C1: SafeTrans, C para Rust, acurácia computacional de 54% para 80% (gpt-4o, 2.653 programas, até 5
  iterações de reparo; pacote).
- S329-C2 e S329-C3: testes no prompt de 22,74% para 27,43%, e o reparo acrescenta até 28,45% (LLaMA-7B).
- S2051-C1: o reparo iterativo reduziu a taxa de aprovação de 29,71% para 16,57% (CodeLlama-70b; Rust entre os
  alvos; métricas não equivalentes).
- S193-C1: a explicação prévia piorou.

**Limitações**
- O pacote de S732 inclui exemplos e decomposição.
- O requisito de Rust seguro não é medido nas comparações extraídas.
- S2051 é contrário, e a tabela não explica em que condição.

**Ambiguidades**
- A linha 18 junta compilador e testes.
- A tabela não diz se o ganho depende de ter os dois.

**Hipótese H-T1:** confirmada.

| Critério | Proposta | Justificativa |
|---|---|---|
| C | atende | Linha direta para a condição do cenário. |
| J | atende | Estudo C para Rust com orçamento igual ao do cenário, mais ablação e contrário citados. |
| O | parcial | Orienta o reparo e o que evitar; não trata da segurança de memória pedida. |

---

## T2 — COBOL para Java, só compilador, até 3 chamadas

**Linhas aplicadas:** 18 (só o compilador), 19 e 20. Nenhuma linha trata de linguagens legadas.

**Orientação derivada da tabela**
- A evidência é insuficiente.
- O *feedback* do compilador garante, no máximo, a compilação, e não a equivalência. Em S1163, a compilação ficou
  no teto nas duas condições.
- Não recomendar técnica como padrão.

**Estudos e comparações**
- Nenhum estudo do corpus traduz COBOL. COBOL aparece só como linguagem de um *benchmark* de geração (S495).
- Migrações de versão ou de plataforma só aparecem sem contrafactual ou em contraste cumulativo: S1220 (Java 8
  para 11, descritivo), S1803 (Oracle SQL para BigQuery, cumulativo, com humano no laço) e S1836.
- S1163-C1: compilação no teto.

**Limitações**
- A tabela não registra a ausência de evidência por linguagem de origem. O texto (lacunas da tradução) registra,
  mas a tabela não.

**Ambiguidades**
- A condição da linha 18 («testes ou compilador disponíveis») sugere que o compilador sozinho basta para a
  orientação favorável.

**Hipótese H-T2:** confirmada.

| Critério | Proposta | Justificativa |
|---|---|---|
| C | parcial | A linha 18 parece se aplicar, mas a sua evidência depende de testes. |
| J | nao_atende | Não há estudo de COBOL nem de migração legada com contrafactual. |
| O | parcial | Leva a não recomendar só com leitura atenta; não há linha explícita de evidência insuficiente. |

---

## R1 — Refatoração local de métodos Python com testes, até 3 chamadas

**Linhas aplicadas:** 21 (especificação, conhecimento e exemplos), 22 (*feedback*, iteração e raciocínio).

**Orientação derivada da tabela**
1. Especificar no prompt o tipo de refatoração e o objetivo (linha 21).
2. Incluir de 1 a 3 exemplos selecionados (linha 21).
3. Verificar com os testes.
4. Não confiar na iteração nem no raciocínio (linha 22).

**Estudos e comparações**
- S202-C1: 3 exemplos selecionados, Pass@1 de 87,44% para 91,11% (gpt-3.5-turbo, Python). Segundo a ficha, a
  complexidade ciclomática do *one-shot* piorou.
- S4-C2: *one-shot*, aprovação nos testes de 28,36% para 34,51% (StarCoder2-15B, Java).
- S511-C2: especificar o tipo de refatoração, *recall* de 15,6% para 52,2% (GPT-4, Java). Mede a identificação de
  oportunidades, e não a refatoração executada.
- S4-C1: CoT de 28,36% para 32,22%.

**Limitações**
- Os ganhos são medidos sobretudo em aprovação nos testes, e não na redução de complexidade, que é o objetivo do
  cenário.
- Há poucos estudos, a maioria em Java e com conjuntos próprios.

**Ambiguidades**
- A linha 21 junta três ingredientes com condições diferentes.
- A condição «linha de base baixa» não se verifica no cenário.
- A tabela não diz se os exemplos reduzem a complexidade.

**Hipótese H-R1:** confirmada (evidência presente e limitada).

| Critério | Proposta | Justificativa |
|---|---|---|
| C | parcial | A linha agrupa ingredientes distintos e a condição de linha de base baixa não se aplica. |
| J | atende | Comparações em Python e Java sustentam especificação e exemplos. |
| O | parcial | Diz o que incluir, mas não informa o efeito sobre a complexidade, que é o objetivo do cenário. |

---

## R2 — Migração de API em ~200 arquivos Java, com desempenho, até 2 chamadas por arquivo

**Linhas aplicadas:** 21 (conhecimento de API e *changelog*), 22.

**Orientação derivada da tabela**
- Fornecer no prompt o *changelog* e a documentação da API (linha 21). É o único elemento com evidência, de um
  estudo em outro domínio.
- A escala de repositório, as mudanças interdependentes e o requisito de desempenho não têm evidência.
- Não recomendar além disso.

**Estudos e comparações**
- S2122-C1: TerraMod, Terraform, Pass@1 de 4% para 76% (Mistral-Large).
- S2122-C2 e S2122-C3: sem esquema da API, 56%; sem *changelogs*, 60%; contra 76% do pacote (LLaMA-4-Maverick).
- Nenhum estudo de migração de API em Java com contrafactual.
- Desempenho só aparece em S958, contra código humano.

**Limitações**
- É um estudo único, em configuração Terraform.
- A tabela não informa o número de chamadas do TerraMod.

**Ambiguidades**
- A linha 21 sugere um resultado favorável geral para «conhecimento de domínio», sem dizer que vem de um estudo.

**Hipótese H-R2:** confirmada.

| Critério | Proposta | Justificativa |
|---|---|---|
| C | parcial | A linha favorável mistura evidências de força distinta. |
| J | parcial | Um estudo, em outro domínio, sustenta o único elemento recomendado. |
| O | parcial | Indica o *changelog*, mas não declara a insuficiência para escala e desempenho. |

---

## Síntese do exame (proposta)

- Proposta por critério, nos oito cenários:
  - clareza: 1 `atende`, 7 `parcial`;
  - justificativa: 4 `atende`, 3 `parcial`, 1 `nao_atende`;
  - orientação concreta: 1 `atende`, 6 `parcial`, 1 `nao_atende`.
- A tabela funciona melhor quando a condição do cenário coincide com a dos estudos (T1, D1). Funciona pior quando o
  cenário não tem testes, usa linguagem legada ou opera em escala de repositório (D2, T2, R2), porque não tem
  linhas explícitas de evidência insuficiente por condição.
- Revisões sugeridas para uma versão 2 da tabela, a decidir pelo autor depois do julgamento (não aplicadas):
  - separar compilador, testes e analisador estático na condição de *feedback*;
  - explicitar na condição quando a evidência supõe localização perfeita ou testes disparadores;
  - acrescentar linhas de evidência insuficiente por condição (sem testes, linguagem legada, escala de
    repositório, modelo pequeno);
  - indicar como repartir o orçamento de chamadas, ou declarar que a evidência não orienta essa escolha.
- Hipóteses: as oito foram confirmadas, H-G1 só em parte. O exame não testa as técnicas, só a orientação da tabela.
