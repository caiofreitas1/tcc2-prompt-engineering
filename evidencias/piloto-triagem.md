# Lote piloto da triagem de título e resumo (T05)

**Situação (02/11/2026):** duas rodadas concluídas. A amostra 1 (tr-v1) teve 6 perdas e
acionou a regra de parada; a amostra 2 (tr-v2) não teve perdas. Elaborado por Claude Code
(Claude Opus 5.5). O autor decidiu manter a RSL completa (D47). A viabilidade até 08/11
segue sem medição, tr-v2 ainda não foi congelada e nenhuma triagem em lote foi iniciada.
As seções até "Efeito do recuo na amostra" descrevem a amostra 1 e não mudam.

## Execução

| Item | Registro |
|---|---|
| Amostra | 100 de 2.300 candidatos, semente 20261101 (`piloto/amostra-1.csv`) |
| IA-A | Claude Opus 5.5, prompt tr-v1, decisões seladas antes do autor (`piloto/selado/ia-a-tr-v1-amostra-1.jsonl`) |
| IA-B | Claude Sonnet 5.5 em subagente, prompt tr-v1, seladas (`piloto/selado/ia-b-tr-v1-amostra-1.jsonl`) |
| Autor | Triagem cega no formulário privado, exportada em `piloto/autor-amostra-1.jsonl` (SHA-256 `6981c1e666e27d34c1cbca266e713c0729510268360da930229c5a6df214c8f9`) |
| Selos | Os SHA-256 de IA-A e IA-B conferem com os de D43 na abertura |
| Comparação | `piloto/comparacao-amostra-1.csv`, gerada por `scripts/analisar_piloto.py` com a codificação de D44/D45 |

O autor não preencheu o campo opcional de motivo em nenhum dos 100 estudos, e o
formulário não registra critério para `duvida`: esses motivos são `nao_informado`.

## Resultados

| Medida | Valor |
|---|---|
| Revocação (Incluir do autor que seguem pela união) | 50/56 (89,3%) |
| Revocação complementar (Incluir + Dúvida do autor que seguem) | 67/81 (82,7%) |
| Perdas (Incluir do autor, Excluir das duas IAs) | 6: S251, S812, S1040, S1249, S1621, S2021 |
| κ binário autor × regra de união (principal) | 0,645 |
| κ em 3 categorias, autor × IA-A | 0,478 |
| κ em 3 categorias, autor × IA-B | 0,425 |
| κ em 3 categorias, IA-A × IA-B | 0,808 |
| κ binário, IA-A × IA-B | 0,870 |

Amostra pequena: as estimativas são imprecisas. Os modelos são do mesmo fornecedor, e
o κ entre as IAs não indica acerto, pois elas podem errar da mesma forma.

### Autor × regra de união

| Autor | Segue | Sai | Total |
|---|---:|---:|---:|
| Incluir | 50 | 6 | 56 |
| Dúvida | 17 | 8 | 25 |
| Excluir | 0 | 19 | 19 |
| Total | 67 | 33 | 100 |

Nenhum Excluir do autor seguiu. Das 33 exclusões consensuais, o autor excluiu 19, ficou
em dúvida em 8 e incluiu 6.

### Autor (linhas) × cada IA (colunas)

| Autor | IA-A incluir | IA-A dúvida | IA-A excluir | IA-B incluir | IA-B dúvida | IA-B excluir |
|---|---:|---:|---:|---:|---:|---:|
| Incluir | 39 | 10 | 7 | 39 | 11 | 6 |
| Dúvida | 6 | 9 | 10 | 8 | 6 | 11 |
| Excluir | 0 | 0 | 19 | 0 | 0 | 19 |

### IA-A (linhas) × IA-B (colunas)

| IA-A | Incluir | Dúvida | Excluir |
|---|---:|---:|---:|
| Incluir | 43 | 2 | 0 |
| Dúvida | 4 | 12 | 3 |
| Excluir | 0 | 3 | 33 |

## As seis perdas

| Estudo | Motivo das IAs (resumido) | Padrão |
|---|---|---|
| S251 | Código como espaço de ações de agentes | Código como meio |
| S812 | Orquestração de ferramentas em descoberta de fármacos | Código como meio |
| S1249 | Interface de voz; código é uma alternativa avaliada | Código como meio |
| S2021 | Raciocínio matemático com geração de programas | Código como meio |
| S1621 | Perguntas financeiras com CoT e PoT; ajuste fino em ambas as condições | Código como meio e treinamento |
| S1040 | Treinamento para tradução, com dados gerados por prompting | Treinamento |

**Leitura (de IA, a confirmar pelo autor).** Nos seis casos, as IAs excluíram porque
leram X3 ou X4 de forma estrita. A expressão "código como meio" não está no protocolo
nem em tr-v1: é uma interpretação que IA-A e IA-B aplicaram por conta própria. A
auditoria D44 a retirou do guia do autor, mas tr-v1 não a proibia às IAs. O autor não
registrou motivos, então não se sabe por qual razão incluiu cada estudo. O piloto não
define quem está certo; a regra da seção 7 é acionada de qualquer forma.

**Condições diferentes entre autor e IAs.** Ao atualizar o guia em 02/11, após a abertura
dos selos, notou-se que a versão usada pelo autor dizia, sobre geração de código em
tarefa mais ampla, que o protocolo "não exige que o código seja o produto final", e que
X4 não se aplica se há prompting em tarefa elegível. tr-v1 não trazia essas orientações
às IAs. Parte das perdas pode, portanto, vir dessa diferença de instruções, contrariando
o objetivo de D44 de dar as mesmas condições aos triadores. tr-v2 reduz a diferença, mas
não a elimina.

## Critérios da decisão RSL completa ou recuo (seção 8)

| Critério | Situação |
|---|---|
| 1. Até 2.500 estudos únicos | Atendido: 2.304 |
| 2. Sem perda após no máximo uma revisão | Em aberto: 6 perdas em tr-v1; depende de nova versão e de nova amostra de 50 |
| 3. Até 12 h do autor até 08/11 | Não sustentado pela projeção abaixo |

### Projeção de horas

**Medido:** 4.667 s de tempo ativo nos 100 estudos, ou seja, 1,30 h e 46,7 s por estudo
(mediana de 37 s). O tempo de leitura de texto completo **não foi medido**.

| Ponto de controle de título e resumo | Horas |
|---|---:|
| Piloto já feito (100) | 1,30 |
| Nova amostra após a revisão (50) | 0,65 |
| Amostra de exclusões consensuais (100) | 1,30 |
| **Subtotal** | **3,24** |

Restam 8,76 h para texto completo, extração e conferência do texto (seção 7, D33). O
volume é uma extrapolação da amostra, e os intervalos são de Wilson a 95%, cálculo
complementar que não estava previsto em D44.

| Cenário | Seguem ao texto completo | As duas IAs incluem | Limite do texto completo a 3 min por estudo (suposição) |
|---|---:|---:|---:|
| RSL completa (2.300) | 67%: cerca de 1.541 (1.319–1.735) | 43%: cerca de 989 | 175 estudos, 11% dos que seguem |
| Recuo (711) | 27/31: cerca de 619 (506–675) | 22/31: cerca de 505 | 175 estudos, 28% dos que seguem |

O limite de 175 estudos é otimista, pois não reserva horas para extração e conferência
do texto. O autor precisa ver toda inclusão e divergência e 20% das exclusões
consensuais (seção 7). A 3 min por estudo, a RSL completa só caberia em 12 h se o autor
visse no máximo 11% dos estudos que seguem, mas as duas IAs incluem 43% da amostra. O
recuo reduz o volume, mas o limite de 28% também fica abaixo dos 71% incluídos pelas duas
IAs na subamostra: só cabe se o texto completo eliminar boa parte deles, o que ainda não
foi medido.

## Efeito do recuo na amostra

Estimativa local: o bloco de tarefas foi aplicado aos títulos dos candidatos (seção
4.2), sem repetir a busca nas bases.

- Candidatos: de 2.300 para 711. S1, S2, S4 e S6 têm os termos no título.
- Amostra: 31 dos 100 ficam. Dos 56 Incluir do autor, 23 ficam e **33 saem**.
- Perdas: só S1040 permanece. As outras cinco saem porque o recorte é mais estreito,
  não porque as IAs melhoraram.

Essa perda de cobertura teria de ser relatada como limitação da revisão rápida.

## Amostra 2 (tr-v2)

| Item | Registro |
|---|---|
| Amostra | 50 de 2.200 candidatos restantes, semente 20261102 (`piloto/amostra-2.csv`) |
| IA-A e IA-B | claude-opus-5-5 e claude-sonnet-5-5, em subagentes novos, com tr-v2 (D48, D49) |
| Autor | Triagem cega, exportada em `piloto/autor-amostra-2.jsonl` (SHA-256 `b807f7cf455bfc3059085bb4fe0d21a43f9c51883422b56eb4bdbac2b6f27cab`) |
| Selos | Os SHA-256 de IA-A e IA-B conferem com os de D49 na abertura |
| Comparação | `piloto/comparacao-amostra-2.csv`, com a codificação de D44/D45 |

| Medida | Amostra 1 (tr-v1) | Amostra 2 (tr-v2) |
|---|---:|---:|
| Revocação | 50/56 | 23/23 |
| Revocação complementar | 67/81 | 37/41 |
| Perdas | 6 | 0 |
| κ binário autor × regra de união (principal) | 0,645 | 0,700 |
| κ em 3 categorias, autor × IA-A | 0,478 | 0,627 |
| κ em 3 categorias, autor × IA-B | 0,425 | 0,494 |
| κ em 3 categorias, IA-A × IA-B | 0,808 | 0,613 |
| κ binário, IA-A × IA-B | 0,870 | 0,680 |
| Seguem pela união | 67/100 | 38/50 |
| Tempo do autor | 1,30 h (46,7 s por estudo) | 0,47 h (33,8 s por estudo) |

### Autor × regra de união (amostra 2)

| Autor | Segue | Sai | Total |
|---|---:|---:|---:|
| Incluir | 23 | 0 | 23 |
| Dúvida | 14 | 4 | 18 |
| Excluir | 1 | 8 | 9 |
| Total | 38 | 12 | 50 |

As quatro Dúvidas do autor que saem são S24, S539, S962 e S2112. Não são perdas pela
seção 7. S539 e S2112 ainda citam geração de código e saíram por X3 ou X4.

### Autor (linhas) × cada IA (colunas), amostra 2

| Autor | IA-A incluir | IA-A dúvida | IA-A excluir | IA-B incluir | IA-B dúvida | IA-B excluir |
|---|---:|---:|---:|---:|---:|---:|
| Incluir | 18 | 5 | 0 | 16 | 5 | 2 |
| Dúvida | 2 | 12 | 4 | 2 | 8 | 8 |
| Excluir | 0 | 1 | 8 | 0 | 0 | 9 |

### IA-A (linhas) × IA-B (colunas), amostra 2

| IA-A | Incluir | Dúvida | Excluir |
|---|---:|---:|---:|
| Incluir | 16 | 4 | 0 |
| Dúvida | 2 | 9 | 7 |
| Excluir | 0 | 0 | 12 |

### Como ler

- **A regra de parada não é acionada** com tr-v2, e o critério 2 da seção 8 fica atendido
  com uma revisão. Com 23 Incluir, zero perda não prova revocação total: o limite inferior
  de Wilson a 95% é de 85,7% (cálculo complementar).
- **As amostras não são um experimento controlado.** O autor já conhecia os motivos das IAs
  na amostra 1 e participou da regra de tr-v2, que espelha a leitura dele. IA-A mudou de
  contexto (D48). A diferença entre as rodadas não mede só o efeito do prompt.
- **As IAs concordam menos entre si com tr-v2.** Os erros em comum podem ter diminuído, mas
  a amostra é pequena e a causa não foi investigada.
- **O autor não registrou motivos** em nenhum dos 50 estudos.

### Volume e esforço com tr-v2

Extrapolação da amostra 2 para os 2.300 candidatos, com intervalos de Wilson a 95%:

| Etapa | Proporção | Estudos estimados |
|---|---:|---:|
| Seguem ao texto completo | 38/50 | cerca de 1.748 (1.440–1.971) |
| As duas IAs incluem | 16/50 | cerca de 736 |
| Exclusões consensuais | 12/50 | cerca de 552 |

Tr-v2 aumenta o volume em relação à estimativa com tr-v1 (cerca de 1.541).

- **Autor:** 1,77 h medidas nas duas rodadas, mais 0,94–1,30 h na amostra de 100 exclusões.
  O tempo de texto completo, extração e conferência do texto não foi medido.
- **IAs, título e resumo:** cada subagente usou cerca de 90 mil tokens em 50 estudos
  (86.683 e 91.402). Nos 2.150 restantes, isso daria cerca de 7,7 milhões de tokens.
- **IAs, texto completo:** não medido. Duas leituras de cerca de 1.748 textos são a maior
  incerteza de viabilidade.

### Critérios da seção 8 após a amostra 2

| Critério | Situação |
|---|---|
| 1. Até 2.500 estudos únicos | Atendido: 2.304 |
| 2. Sem perda após no máximo uma revisão | Atendido na amostra 2, com tr-v2 |
| 3. Horas do autor | Teto retirado pelo autor (D47); projeção pendente da medição |

## Decisão do autor e próximos passos (D47)

O autor manteve a RSL completa, com entrega em 08/11: o teto de 12 h deixa de decidir o
recuo, e a viabilidade precisa ser medida. A estimativa do recuo acima fica só como
registro. A busca ampla e as verificações da seção 7 não mudam.

1. **Amostra 2:** concluída, sem perdas.
2. **Medição do texto completo (preparada, D51):** 12 estudos sorteados entre os que seguem pela união nas
   duas amostras, com acesso aberto `sim`. A amostra 2 entra porque a triagem cega já
   terminou e ela representa melhor o fluxo de tr-v2. IA-A e IA-B leem o texto com tc-v1;
   o autor confere, com início e fim marcados por estudo, e o uso de tokens é registrado.
3. **Projeção e cronograma:** refeitos com os tempos medidos (seção 12).
4. **Lote principal:** congelar tr-v2 e triar os 2.150 restantes. Pela seção 1, o recuo não
   pode ser aplicado depois de iniciada a triagem em lote, por isso a medição vem antes.

## Limitações

- `dados/triagem.csv` ainda não recebeu estas decisões. O validador exige critério e
  motivo, que o autor não registrou. O registro de origem é `piloto/autor-amostra-1.jsonl`;
  a forma de levá-lo ao CSV será tratada sem inventar conteúdo.
- IA-A foi executada, na amostra 1, pelo mesmo agente que redigiu o guia e esta análise.
- A leitura das perdas é de IA e não constitui revisão humana.
- A alteração do critério 3 ocorreu depois de conhecidos os dados e é um desvio a relatar.
