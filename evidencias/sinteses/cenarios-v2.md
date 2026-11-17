# Cenários de exame da taxonomia e da tabela de apoio — v2 (congelada)

Claude Code (Claude Opus 5.5), 17/11/2026. Ajustes pedidos pelo autor sobre a v1 (D111): linguagens e domínios
definidos com precisão, recursos de verificação e orçamento de chamadas explícitos, e as expectativas de evidência
escritas como hipóteses a confrontar no exame. Esta versão é congelada junto com a tabela de apoio v1; os hashes
estão em `cenarios-congelamento.txt`.

## Regras (protocolo, seção 11; D97)

- Origem sintética, declarada. Os cenários descrevem situações típicas e não vêm de casos reais nem de estudos do
  corpus. A v1 foi escrita antes da síntese. A v2 foi ajustada depois dela, e por isso a escolha de linguagens e
  domínios pode refletir o conhecimento do corpus. Esse limite é declarado no exame.
- Dois cenários por tarefa. As hipóteses H indicam o que se espera encontrar na tabela. O exame verifica se a
  tabela confirma ou refuta cada hipótese, e uma hipótese refutada não muda o cenário.
- Critérios, cada um com julgamento (`atende`, `parcial` ou `nao_atende`), justificativa e ambiguidades:
  - **clareza:** a tabela leva a uma orientação sem interpretação extra;
  - **justificativa nas fontes:** a orientação aponta estudos e comparações do corpus;
  - **orientação concreta:** diz o que fazer, em que condição e com que limite, inclusive quando a resposta
    adequada é não recomendar.
- O exame não mede eficácia. O julgamento final é do autor.

## Cenários

### G1 — Geração de funções Python com testes

- **Tarefa e domínio:** geração de funções Python 3 isoladas, de 10 a 50 linhas, a partir de *docstring* e
  assinatura, com bibliotecas padrão.
- **Modelo:** modelo comercial de grande porte, acessado por API (classe GPT-4o).
- **Recursos de verificação:** de 3 a 10 testes unitários públicos por função, executáveis localmente em
  segundos. Há uma suíte oculta para a aceitação final.
- **Orçamento:** até 5 chamadas ao modelo por função.
- **Objetivo:** maximizar a proporção de funções que passam na suíte oculta.
- **H-G1:** a tabela traz evidência suficiente para orientar o uso dos testes, do *feedback* de execução e do
  planejamento, com ressalvas sobre o orçamento.

### G2 — Contratos inteligentes Solidity com modelo pequeno local

- **Tarefa e domínio:** geração de contratos Solidity 0.8.x (tokens e cofres simples, de 50 a 200 linhas) a partir
  de requisitos em linguagem natural.
- **Modelo:** modelo aberto de até 8B parâmetros, executado localmente.
- **Recursos de verificação:** compilador `solc` e um analisador estático de vulnerabilidades. Não há testes
  unitários nem rede de testes.
- **Orçamento:** até 3 chamadas por contrato.
- **Objetivo:** contratos que compilem, sem alertas de vulnerabilidade de alta severidade.
- **H-G2:** a evidência é esparsa ou heterogênea para essa combinação de linguagem, porte do modelo e
  verificação, e a orientação adequada tende a ser não recomendar uma técnica como padrão.

### D1 — Reparo de função Python com teste falhando

- **Tarefa e domínio:** reparo de um defeito numa função Python isolada, de até 80 linhas, com um único defeito.
- **Modelo:** modelo comercial de grande porte.
- **Recursos de verificação:** o teste que falha, com mensagem de erro e *traceback*, e a suíte da função,
  executável à vontade.
- **Orçamento:** até 10 chamadas por defeito.
- **Objetivo:** um *patch* que passe na suíte e corresponda à correção pretendida.
- **H-D1:** a evidência é suficiente para orientar o uso das informações diagnósticas e do *feedback* de testes.

### D2 — Reparo em repositório Java a partir de relato de defeito

- **Tarefa e domínio:** reparo em um repositório Java com Maven, de 200 a 500 mil linhas, a partir de um relato de
  defeito em linguagem natural.
- **Modelo:** modelo comercial de grande porte.
- **Recursos de verificação:** compilação do projeto e a suíte de testes existente, que não reproduz o defeito. A
  localização é desconhecida.
- **Orçamento:** até 20 chamadas por defeito.
- **Objetivo:** um *patch* que compile, não quebre a suíte e corrija o comportamento relatado.
- **H-D2:** a evidência é possivelmente insuficiente sem teste de reprodução e sem localização conhecida.

### T1 — Tradução de C para Rust com compilador e testes

- **Tarefa e domínio:** tradução de um módulo C99 de utilidades, de 300 a 800 linhas, sem E/S de baixo nível,
  para Rust seguro.
- **Modelo:** modelo comercial de grande porte.
- **Recursos de verificação:** compilador `rustc` e a suíte de testes do módulo original, portada para Rust e
  executável.
- **Orçamento:** até 5 rodadas de correção por função.
- **Objetivo:** código que compile, passe nos testes e preserve o comportamento.
- **H-T1:** a evidência está presente para o reparo com *feedback* de compilação e de testes.

### T2 — Migração de COBOL para Java sem testes

- **Tarefa e domínio:** migração de programas COBOL de lote, com regras de negócio financeiras pouco documentadas,
  para Java 17.
- **Modelo:** modelo comercial de grande porte.
- **Recursos de verificação:** só o compilador Java. Não há testes automatizados nem oráculo de equivalência.
- **Orçamento:** até 3 chamadas por programa.
- **Objetivo:** código Java equivalente ao original.
- **H-T2:** a evidência é possivelmente insuficiente, e a orientação adequada tende a ser não recomendar.

### R1 — Refatoração local de métodos Python com testes

- **Tarefa e domínio:** refatoração de métodos Python longos (mais de 50 linhas) para reduzir a complexidade
  ciclomática e os *code smells*, sem mudar o comportamento.
- **Modelo:** modelo comercial de grande porte.
- **Recursos de verificação:** suíte de testes do projeto e medidor de complexidade e *smells*.
- **Orçamento:** até 3 chamadas por método.
- **Objetivo:** menor complexidade, com todos os testes passando.
- **H-R1:** há evidência presente, mas limitada.

### R2 — Migração de API em repositório Java

- **Tarefa e domínio:** migração de chamadas a uma API obsoleta para a versão nova de uma biblioteca, em cerca de
  200 arquivos de um repositório Java, com mudanças interdependentes.
- **Modelo:** modelo comercial de grande porte.
- **Recursos de verificação:** compilação, suíte de testes e *benchmarks* de desempenho do projeto, além do
  *changelog* e da documentação da biblioteca.
- **Orçamento:** até 2 chamadas por arquivo.
- **Objetivo:** migração completa, sem regressão funcional nem de desempenho.
- **H-R2:** a evidência é possivelmente insuficiente para a escala de repositório e o requisito de desempenho.
