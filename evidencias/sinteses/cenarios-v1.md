# Cenários de exame da taxonomia e da tabela de apoio — proposta v1

Claude Code (Claude Opus 5.5), 17/11/2026. **Proposta para aprovação do autor; não congelada.**

## Regras (protocolo, seção 11; D97)

- Origem sintética, declarada: os cenários descrevem situações típicas de uso. Não são
  casos reais nem foram tirados de um estudo do corpus.
- Escrevi os cenários antes da síntese (T08) e sem consultar resultados agregados, para
  que não fossem escolhidos pelo que a tabela responde bem. Conheço o corpus pela extração,
  e isso fica declarado como limite.
- Dois por tarefa. Pelo menos um por tarefa tende a cair em evidência insuficiente, quando
  não recomendar pode ser a resposta adequada.
- Cada cenário é julgado em três critérios, com julgamento, justificativa e ambiguidades:
  - **clareza:** a tabela leva a uma orientação sem interpretação extra;
  - **justificativa nas fontes:** a orientação aponta estudos e extrações do corpus;
  - **orientação concreta:** diz o que fazer, em que condição e com que limite.
- Isso não mede eficácia. Depois da aprovação, os cenários e a versão da tabela aplicada
  são congelados com hash antes do exame.

## Cenários

| ID | Tarefa | Situação | Condições que a tabela precisa considerar | Expectativa declarada |
|---|---|---|---|---|
| G1 | Geração | Uma equipe gera funções Python a partir de descrições em linguagem natural, com um modelo comercial de grande porte, e tem testes unitários para cada função. Quer aumentar a taxa de funções corretas. | Modelo grande; testes executáveis; problemas no nível de função; custo de chamadas aceitável. | Evidência provavelmente abundante. |
| G2 | Geração | Um desenvolvedor gera código para um domínio especializado (por exemplo, contratos inteligentes ou descrição de hardware) com um modelo aberto pequeno (até cerca de 8B) rodando localmente, sem testes, e se preocupa com vulnerabilidades. | Modelo pequeno; sem testes; linguagem pouco representada; segurança como risco. | Evidência provavelmente esparsa ou heterogênea. |
| D1 | Depuração/reparo | Um teste unitário falha numa função Python isolada. A equipe tem a mensagem de erro e pode executar os testes quantas vezes quiser. | Defeito no nível de função; feedback de execução disponível; várias rodadas permitidas. | Evidência provavelmente abundante. |
| D2 | Depuração/reparo | Há só um relato de defeito em linguagem natural num repositório grande. Não existe teste que reproduza o defeito, e a localização é desconhecida. | Nível de repositório; sem teste de reprodução; contexto extenso. | Evidência possivelmente insuficiente. |
| T1 | Tradução | Um módulo C é traduzido para Rust. O compilador e uma suíte de testes do original estão disponíveis, e o objetivo é código que compile e preserve o comportamento. | Par C → Rust; compilador e testes disponíveis; rodadas de correção permitidas. | Evidência provavelmente presente. |
| T2 | Tradução | Um sistema legado (por exemplo, COBOL) migra para Java, sem testes automatizados e com regras de negócio pouco documentadas. | Linguagem legada; sem testes; equivalência difícil de verificar. | Evidência possivelmente insuficiente. |
| R1 | Refatoração | Métodos Python longos são refatorados para reduzir complexidade e code smells, preservando o comportamento, com testes existentes. | Refatoração local; testes disponíveis; métricas de qualidade estrutural. | Evidência provavelmente presente, mas limitada. |
| R2 | Refatoração | A migração de uma API obsoleta para a nova versão afeta muitos arquivos de um repositório, e o desempenho é sensível. | Muitos arquivos; dependências entre mudanças; desempenho como requisito. | Evidência possivelmente insuficiente. |

## O que o exame registra, por cenário

1. A orientação que a tabela de apoio dá: técnicas ou mecanismos indicados, condições e
   cautelas, ou a declaração de evidência insuficiente.
2. Os estudos e as extrações que sustentam a orientação.
3. Para cada critério: julgamento (`atende`, `parcial` ou `nao_atende`), justificativa e
   ambiguidades.

Quem examina: proposta de exame redigida por Claude Code; julgamento final do autor.
