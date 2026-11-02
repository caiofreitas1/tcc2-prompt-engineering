# Lote piloto da triagem de título e resumo (T05)

**Situação (02/11/2026):** primeira rodada concluída; a regra de parada foi acionada.
Elaborado por Claude Code (Claude Opus 5.5). O autor ainda não decidiu o recuo nem a
versão seguinte do prompt. Nenhuma triagem em lote foi iniciada.

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

## Próximos passos, se o autor aprovar

1. Registrar o recuo antes de qualquer triagem em lote (seção 1).
2. Publicar tr-v2 (rascunho abaixo) e aplicá-la às IAs em nova amostra de 50, com o
   autor cego (seção 7).
3. Medir o tempo de texto completo em um lote pequeno e refazer a projeção.

### Mudança proposta em tr-v2 (rascunho, não aplicado)

Não altera I2 nem X3 ou X4 no protocolo; só envia à leitura do texto completo os casos
que tr-v1 excluía:

- Se o estudo usa prompting para gerar código, mas a tarefa final é outra (agentes,
  matemática, perguntas), responda `duvida`, não `excluir`.
- Use X4 só quando o estudo for centrado apenas em treinamento, ajuste fino ou
  arquitetura. Se também avaliar prompting em uma das tarefas, ou gerar dados por
  prompting para elas, responda `duvida`.

## Limitações

- `dados/triagem.csv` ainda não recebeu estas decisões. O validador exige critério e
  motivo, que o autor não registrou. O registro de origem é `piloto/autor-amostra-1.jsonl`;
  a forma de levá-lo ao CSV será tratada sem inventar conteúdo.
- IA-A foi executada pelo mesmo agente que redigiu o guia, esta análise e a proposta
  de tr-v2.
- A leitura das perdas e a proposta são de IA e não constituem revisão humana.
