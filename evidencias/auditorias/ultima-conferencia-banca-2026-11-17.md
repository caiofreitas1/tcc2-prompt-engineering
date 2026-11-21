# Última conferência antes do envio à banca

Data: 17/11/2026. Executor: Codex (IA). Natureza: auditoria assistida por IA.

Versão: `3e119bf5d96e1dcf5ee76194e9971298781309ce`. O merge ocorrido durante a conferência não alterou os arquivos em relação a `aab3f72`. PDF examinado: `build/main.pdf`, 33 páginas, compilado em 17/11/2026 às 12h52.

**Parecer:** os principais problemas de conteúdo da revisão anterior foram corrigidos. Não identifiquei novo problema científico grave no escopo desta conferência. Há duas pendências concretas que ajustaria antes do envio: posição das tabelas e disponibilidade do repositório. O artigo e os dados não foram alterados por esta conferência.

## Pendências

| Prioridade | Local | Evidência e consequência | Ajuste recomendado |
|---|---|---|---|
| Média, apresentação | Tabela X e tabelas XI–XII; PDF pp. 32–33 | A Tabela X, segunda parte da tabela de apoio, foi deslocada para depois das referências. As tabelas de cenários e julgamentos também ficaram no final. O log registra `Float too large for page by 3.34528pt` na segunda tabela de `04c2-tabela-apoio-v2.tex`. O conteúdo continua visível, mas o deslocamento prejudica a leitura da contribuição e de seu exame. | Ajustar a composição da segunda tabela, reduzindo seu excesso de altura ou dividindo-a, e recompilar para mantê-la junto da QP3 e liberar as tabelas do exame para a seção correspondente. Conferir visualmente a nova paginação. |
| Média, disponibilidade | `03-metodologia.tex`, linhas 431–434 | O texto anuncia repositório público. A consulta autenticada ao GitHub nesta rodada ainda retornou `visibility: private`. Há decisão do autor de torná-lo público, mas intenção e disponibilidade efetiva são estados distintos. | Antes do envio, disponibilizar efetivamente os materiais à banca ou corrigir a frase para descrever o acesso real. Nenhuma publicação ou alteração de permissões foi realizada nesta rodada. |

Locais: [segunda tabela de apoio](</Users/caiofreitas/Documents/ChatGPT/TCC 2/tcc2-prompt-engineering/monografia/capitulos/04c2-tabela-apoio-v2.tex:33>), [tabelas do exame](</Users/caiofreitas/Documents/ChatGPT/TCC 2/tcc2-prompt-engineering/monografia/capitulos/04e-exame.tex:7>) e [disponibilidade do repositório](</Users/caiofreitas/Documents/ChatGPT/TCC 2/tcc2-prompt-engineering/monografia/capitulos/03-metodologia.tex:431>).

## Pontos anteriores resolvidos

- A presença de componentes fora de prompting passou a ser distinguida de sua variação não controlada entre condições.
- Foi retirada a afirmação de superioridade geral da informação externa; resumo e conclusão restringem as observações às comparações extraídas.
- A discussão reconhece o estudo com 20 participantes de S62 e distingue seus resultados de produtividade geral.
- As subseções passaram a reconhecer a conferência humana por amostra.
- Os 3,2% são apresentados como proporção descritiva de correções na amostra, sem estimar a taxa de erro do corpus.
- A106 inclui o terceiro denominador, 206; a nota correta do autor está registrada e a antiga pendência foi retirada.
- Os quatro comandos de itálico corrompidos foram corrigidos. Não foram localizadas marcas de edição como `TODO`, `FIXME` ou comandos `extit` quebrados no texto.

## Verificação

- `make check`: zero erros estruturais e 54 testes aprovados nesta rodada.
- `make pdf`: sucesso; latexmk informa que o PDF está atualizado. Não há citações ou referências LaTeX indefinidas.
- Inspeção visual: visão geral das 33 páginas e ampliação das pp. 32–33. A pendência de paginação descrita acima foi confirmada. Permanecem pequenos avisos de largura excedente e substituição de fonte.
- Dados: 332 fichas, 805 comparações ex-v2.2, 67 fichas com revisão humana confirmada; tarefas 247/62/27/20; direções 516 favoráveis, 145 desfavoráveis, 28 iguais, 91 sem direção e 25 descritivas. As contagens centrais permanecem coerentes.
- O Apêndice B contém exatamente os 332 identificadores das fichas, sem faltantes ou extras. Os 120 julgamentos A6–A125 estão presentes.
- `make release-check`: continua reprovado com os mesmos 1.596 apontamentos de estado: 805 extrações sem `conferido_original`, 649 revisões humanas pendentes de comparações, 125 afirmações em rascunho, 16 estudos sem extração numérica e uma flag de revisão humana final. A barreira exige conferência integral e comparação numérica por estudo, enquanto o protocolo atual admite conferência amostral e fichas descritivas. Não interpretar a contagem como 1.596 erros científicos distintos, nem afirmar aprovação da barreira.

Esta foi uma conferência das alterações, da coerência documental, das contagens e da apresentação. Não foi uma nova reconferência exaustiva dos 332 artigos ou das 805 comparações nos originais. A aprovação estrutural e a ausência de outro achado grave não certificam integralmente as fontes.

## Verificação posterior da correção de paginação

Em 17/11/2026, no commit `12de78a` (merge da correção `77d8748`), o problema de paginação foi confirmado como **resolvido**. O PDF atualizado tem 32 páginas: a Tabela X está na p. 22 e as tabelas XI e XII estão na p. 23, junto do exame dos cenários, antes das referências. `make pdf` confirmou o arquivo atualizado; o aviso `Float too large` desapareceu e não há referências LaTeX indefinidas. As páginas 22 e 23 foram renderizadas e inspecionadas visualmente, sem cortes ou sobreposições identificados. A alteração foi de composição das tabelas e do gerador correspondente; não houve nova execução dos testes gerais, já aprovados na conferência acima.

A consulta ao GitHub nesta verificação ainda retornou o repositório como privado; a frase da metodologia continua anunciando acesso público. Essa pendência de disponibilidade permanece separada do problema de paginação, agora corrigido.
