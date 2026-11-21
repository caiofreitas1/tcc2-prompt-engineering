<!--
Especificação de design do site, produzida por Codex CLI 0.169.0 (IA) em 20/11/2026, em modo
somente leitura, a pedido do autor. Texto preservado como devolvido; só os caminhos absolutos
foram convertidos em relativos. A implementação em site/ segue este documento, com os ajustes
registrados em contexto/decisoes.md (D131). O mapeamento de recursos (seção 7) e o
preenchimento dos cenários (seção 6) são propostas editoriais sujeitas à revisão do autor.
-->

# Prompt em Código — especificação do Guia e do Explorador

**Nome do site:** Prompt em Código. **Descrição:** “Um guia para consultar o que os estudos mediram sobre engenharia de prompt para código.”

A página inicial é o **Guia**. A primeira pergunta é “O que você precisa fazer?”. Quem já tem uma dúvida prática começa pela tarefa e pelos recursos disponíveis. Quem quer investigar um resultado entra pelo **Explorador**. Os dois percursos chegam à mesma unidade de evidência, a comparação identificada por `Sxxx-Cn`.

O desenho usa três expressões com sentidos distintos em todo o site: **“aplicável às condições”** descreve os recursos, **“evidência favorável”** descreve a síntese de uma linha e **“melhora”** descreve uma métrica em uma comparação. Cada expressão ocupa um lugar próprio na interface. Essa distinção é o principal requisito do produto.

## 1. Conteúdo, arquitetura e navegação

| Destino | Rota por hash | Conteúdo |
|---|---|---|
| Guia | `#/guia` | Tarefa, condições, oito cenários e linhas da tabela v2 em três grupos. Uma linha pode ficar expandida. |
| Explorador · Comparações | `#/explorador` | Busca, três filtros, total, lista paginada e acesso ao estudo de cada comparação. |
| Explorador · Matriz | `#/explorador?vista=matriz` | Contagens de comparações por tarefa e mecanismo acrescentado. Cada célula com registros abre sua lista. |
| Explorador · Estudos | `#/explorador?vista=estudos` | Índice das 332 fichas, pesquisável por ID ou título. Dá acesso também aos estudos sem comparação extraída. |
| Estudo | `#/estudo/S1` | Identificação bibliográfica, ficha, riscos registrados e comparações daquele estudo. |
| Comparação em um estudo | `#/estudo/S1?cmp=S1-C1` | Mesma página, com a comparação aberta e seu título em foco. |
| Sobre | `#/sobre` | Método, cobertura, conferência humana, limites, versões e documentos. `#/sobre?sec=como-ler` leva diretamente à explicação de leitura. |

**Estrutura comum.** Cabeçalho com nome, links **Guia**, **Explorador**, **Sobre** e seletor de tema. A página de Estudo mantém Explorador como área atual. Abaixo da navegação, em todas as telas, uma linha de procedência: **“Extração por IA. O autor conferiu uma amostra de 67 estudos.”** O link **Entender a conferência** abre a seção correspondente em Sobre. Rodapé compacto em todas as rotas.

**Cobertura que deve aparecer na interface:**

| Onde | Texto |
|---|---|
| Guia | “31 linhas de apoio, elaboradas a partir de sínteses de 302 fichas.” |
| Explorador | “805 comparações em um corpus de 332 estudos. Há estudos com ficha e sem comparação extraída.” |
| Sobre | “As extrações posteriores às sínteses parciais ampliaram o corpus do Explorador. Elas não foram incorporadas retroativamente às linhas do Guia.” |

G13 tem `tarefa=todas`. Entra nas quatro consultas, sempre com o mesmo ID e com o rótulo **Todas as tarefas**. Assim, geração recupera 14 linhas, depuração 8, tradução 6 e refatoração 6. O total de linhas distintas continua sendo 31. Dentro de cada grupo, preservar a posição física do CSV, inclusive a de G13. [Tabela de apoio v2](<../evidencias/sinteses/tabela-apoio-v2.csv>) · [Cobertura e limites da QP3](<../monografia/capitulos/04c-qp3.tex:134>)

### Estado compartilhável

- **Guia.** `tarefa=geracao|depuracao|traducao|refatoracao`. Repetir `r=` para recursos marcados: `testes`, `executor`, `compilador`, `analisador`, `contexto`, `exemplos`, `pequeno`. `ch=uma|varias` representa o orçamento. Em depuração, `rep=teste|outro|nao` e `diag=sim|nao` qualificam reprodução e informação diagnóstica. Omitir respostas desconhecidas. `cenario=G1` identifica o exemplo e `linha=G7` identifica o cartão aberto. **Cenário G1** e **Linha G1** são entidades distintas, inclusive nos nomes acessíveis.
- **Exemplo de link:** `#/guia?tarefa=geracao&r=testes&ch=varias&cenario=G1&linha=G7`. Um cenário sozinho também resolve seu preenchimento. O link canônico inclui as condições explícitas. Ao editar uma condição, preservar as demais e retirar `cenario`. A hipótese do cenário nunca entra no filtro.
- **Explorador.** `tarefa`, `mec`, `dir`, `q`, `vista` e `p` descrevem a consulta. Exemplo: `#/explorador?tarefa=geracao&mec=contexto&dir=melhora&p=1`. Uma escolha por filtro, combinada com as demais por **E**. Alterar filtro volta à página 1. Lista e matriz compartilham os filtros. O índice de estudos tem sua própria busca por ID ou título.
- **Histórico.** Navegar para estudo, abrir célula, aplicar cenário ou trocar de vista cria entrada no histórico. Digitar uma busca substitui a entrada corrente após 250 ms. Voltar restaura filtros, página, expansão e foco no link de origem quando ele existe. A rota inicial sem hash abre o Guia. ID desconhecido apresenta uma mensagem com saída útil. Parâmetros inválidos nunca selecionam silenciosamente outra tarefa ou outro estudo.
- **Tema.** Opções **Sistema**, **Claro**, **Escuro**. Padrão Sistema. Guardar só a preferência de tema em `localStorage`. Um link compartilhado conserva a consulta e respeita o tema de quem o abre.

### Contrato estático de publicação

Um `index.html`, CSS, JavaScript e um único `dados.json` relativo à página. HTML semântico, pilha tipográfica do sistema, nenhum framework, serviço de busca ou build de front-end. No GitHub Pages, usar caminhos relativos para funcionar sob o nome do projeto. Em abertura direta por `file://`, se o navegador impedir a leitura do JSON, oferecer **Abrir dados.json deste site**, com seleção local do mesmo arquivo.

| Coleção em `dados.json` | Regra de composição |
|---|---|
| `meta` | Versão da tabela e da extração, data de corte, revisão ou commit de origem, data efetiva da publicação e URLs dos documentos. Data de publicação e data de corte são campos distintos. |
| `linhas` | As 31 linhas, na ordem do CSV. Preservar agrupamento, condição, resultado medido, indicação, evidência literal, força, ressalvas e referências. Manter as regras de recursos da seção 7 como metadados editoriais separados. |
| `cenarios` | Oito registros v2 com nome, domínio, modelo, verificações, orçamento literal, objetivo e preenchimento. Se a hipótese for exibida, usar o título **Hipótese do exame**. |
| `comparacoes` | Selecionar `prompt_versao=ex-v2.2` e IDs `^S\d+-C\d+$`, como no recorte da síntese. As duas linhas históricas `E1` e `E2` explicam por que o JSONL tem 807 registros físicos e o Explorador tem 805. |
| `estudos` | Começar pelos IDs das 332 fichas. Associar título, ano do registro e identificador de `estudos.csv` por ID. Conservar a versão quando documentada. O cadastro geral de busca tem escopo maior que o corpus. |

Exportar uma **lista permitida de campos públicos**. Ela inclui metadados, valores, resumos da ficha, localizadores, proveniência e ligações. Excluir `citacoes`, `trecho`, `fonte`, `texto_fonte`, `ficha_origem`, PDFs primários e caminhos incorporados em campos livres. Um localizador público contém tabela, figura, seção, página, coluna ou linha pertinente. Se precisar de limpeza, preservar essas coordenadas. Renderizar texto dos dados como texto, inclusive no resultado de busca. [Regra utilizada na síntese](<../scripts/sintetizar.py:50>)

## 2. Wireframes

Os colchetes representam controles. As reticências abreviam conteúdo nestes desenhos. Na interface, os rótulos científicos e suas ressalvas podem quebrar linha e permanecem legíveis por inteiro.

### Guia vazio

```text
DESKTOP
Prompt em Código                 Guia   Explorador   Sobre    Tema [Sistema v]
Extração por IA. O autor conferiu uma amostra de 67 estudos.  [Entender a conferência]

Guia por tarefa
Consulte as linhas de evidência para as condições do seu projeto.
+--------------------------------+  +--------------------------------------------+
| O que você precisa fazer?      |  | Comece por um cenário                      |
| ( ) Geração    ( ) Depuração   |  | Geração     [Funções Python] [Solidity]     |
| ( ) Tradução   ( ) Refatoração |  | Depuração   [Teste falhando] [Relato Java]  |
|                                |  | Tradução    [C para Rust] [COBOL para Java] |
| Recursos disponíveis           |  | Refatoração [Métodos Python] [Migração API] |
| [ ] Testes executáveis ...     |  |                                            |
| Chamadas [Ainda não sei v]     |  | Selecione uma tarefa para consultar o Guia.|
+--------------------------------+  +--------------------------------------------+
Tabela v2 · Extração ex-v2.2 · Corte 07/09/2026                    [Como ler]

CELULAR · 360 px
Prompt em Código       [Tema v]
Guia     Explorador     Sobre
Extração por IA. Conferência por
amostra. [Entender a conferência]
Guia por tarefa
O que você precisa fazer?
( ) Geração       ( ) Depuração
( ) Tradução      ( ) Refatoração
[Usar um dos 8 cenários       v]
Recursos disponíveis
[ ] Tenho testes executáveis
...
Chamadas [Ainda não sei       v]
Selecione uma tarefa para
consultar o Guia.
[Como ler]        Tabela v2
```

### Guia com resultado

```text
DESKTOP
Condições                         Geração · 14 linhas
(•) Geração                       Cenário G1 · Funções Python · até 5 chamadas por função
[x] Testes  [ ] Compilador        [Ir às lacunas] [Como ler]
(•) Várias chamadas               Aplicáveis às condições marcadas (8)
[Escolher outro cenário]          + G1  Feedback de testes ou execução em laço       [Abrir]
                                  | favorável; contrária com orçamento igualado
                                  | Mede Pass@1 e aprovação nos testes
                                  + G3  Autocrítica sem execução · dividida           [Abrir]
                                  ...
                                  Exigem recurso não marcado (3)
                                  + G2  Feedback de compilador ou analisador estático [Abrir]
                                  | Falta marcar compilador ou analisador.
                                  Lacunas declaradas (3)
                                  + G12 Formulação, língua, compressão e otimização   [Abrir]
                                  | dividida; insuficiente por variante
                                  ...

CELULAR
Geração · 14 linhas
Cenário G1 · Funções Python
Até 5 chamadas por função
[Editar condições v] [Como ler]
[Aplicáveis 8] [Exigem recurso 3]
[Lacunas 3]
Aplicáveis às condições marcadas
+ G1  Feedback de testes ou
| execução em laço
| favorável; contrária com
| orçamento igualado
| Mede Pass@1 e aprovação
| nos testes.           [Abrir]
...
Exigem recurso não marcado (3)
...
Lacunas declaradas (3)
...
```

### Guia com cartão expandido

```text
DESKTOP
G7  Planejamento ou decomposição antes do código                         [Recolher]
    Evidência da linha   [+ favorável ao pacote]
    Condição estudada    Duas ou mais etapas, no nível de função.
    Resultado medido     Pass@1
    Indicação            [texto da tabela]
    Força descritiva     [texto da tabela, inclusive aproximações]
    Ressalvas            [texto da tabela]
    Comparações citadas
    ID        Modelo / benchmark          Métrica       Base    Intervenção   Direção
    S1-C1     code-davinci-002 / HumanEval Pass@1       48,1%       60,3%     Melhora
              Revisão humana pendente     [Detalhes de S1-C1] [Abrir no arXiv]
    ...

CELULAR
G7  Planejamento ou decomposição
antes do código        [Recolher]
[+ favorável ao pacote]
Condição estudada ...
Resultado medido ...
Indicação ...  Força ...  Ressalvas ...
Comparações citadas
+ S1-C1 · HumanEval
| code-davinci-002 · Pass@1
| Base · Direct              48,1%
| Intervenção · Self-planning 60,3%
| Direção da métrica       Melhora
| Revisão humana pendente
| Tabela 1, p. 7 ... [Detalhes]
| [Abrir no arXiv]
```

### Explorador com lista e filtros

```text
DESKTOP
Explorador
[Comparações]    [Matriz]    [Estudos]
+--------------------------+  +-------------------------------------------------+
| Filtrar comparações      |  | 805 comparações                                 |
| Buscar [ID, modelo...  ] |  | ID / estudo   Modelo e benchmark  Par medido ... |
| Tarefa       [Todas   v] |  | S1-C1         code-davinci-002    Pass@1          |
| Mecanismo    [Todos   v] |  | [Estudo S1]   HumanEval           48,1% | 60,3%  |
| Direção      [Todas   v] |  | Revisão humana pendente          [Ver comparação]|
| [Limpar filtros]         |  | ...                                             |
+--------------------------+  | [Anterior]    Página 1 de 33           [Próxima] |
                              +-------------------------------------------------+

CELULAR · FILTROS FECHADOS        CELULAR · FILTROS ABERTOS
Explorador                        Explorador
Comparações | Matriz | Estudos    Comparações | Matriz | Estudos
[Filtros (0)                v]    [Filtros (0)                ^]
805 comparações                   Buscar [ID, modelo...        ]
+ S1-C1 · Geração                 Tarefa [Todas                v]
| HumanEval · code-davinci-002    Mecanismo acrescentado [Todos v]
| Pass@1 · maior é melhor         Direção [Todas               v]
| Base 48,1% · Intervenção 60,3%   [Limpar filtros] [Ver resultados]
| Melhora                        805 comparações
| Revisão humana pendente         + S1-C1 ...
| [Ver comparação]
[Anterior]  1 de 33  [Próxima]
```

### Explorador com matriz e índice de estudos

```text
DESKTOP · MATRIZ
[Comparações]  [Matriz]  [Estudos]
[Filtros]     Comparações por tarefa e mecanismo acrescentado
              Mecanismo          Geração   Depuração   Tradução   Refatoração
              Instrução             [90]        [12]        [4]           [4]
              Contexto             [181]        [77]        [5]          [12]
              Restrições           [150]        [16]        [9]           [3]
              ...
              Cada comparação pode aparecer em mais de um mecanismo.

CELULAR · MATRIZ                 ÍNDICE DE ESTUDOS · AMBOS
Comparações | Matriz | Estudos    Comparações | Matriz | Estudos
[Filtros (0)                v]    Buscar estudo [ID ou título       ]
[Geração                    v]    332 estudos
  Instrução              [90]    S1 · Self-planning Code Generation
  Contexto              [181]    with Large Language Models
  ...                            2025                    [Abrir estudo]
[Depuração                  >]    ...
[Tradução                   >]    [Anterior] Página ... [Próxima]
[Refatoração                >]
```

### Estudo

```text
DESKTOP
[Voltar aos resultados]                          Estudo S1 · Ano do registro 2025
Self-planning Code Generation with Large Language Models
arXiv:2303.06689 · Versão cadastrada v5                          [Abrir no arXiv]
+-------------------------------+  +---------------------------------------------+
| Ficha do estudo               |  | Comparações do estudo                       |
| Tarefas / técnicas            |  | S1-C1  Self-planning / Direct    [Recolher]  |
| Modelos / benchmarks          |  | HumanEval · code-davinci-002 · Pass@1       |
| Riscos registrados            |  | Base 48,1%           Intervenção 60,3%      |
| Conferência da ficha          |  | Localizador · Origem · Revisão humana       |
+-------------------------------+  | S1-C2  Zero-shot CoT (Two-phase)     [Abrir] |
                                   +---------------------------------------------+

CELULAR
[Voltar aos resultados]
Estudo S1 · 2025
Self-planning Code Generation
with Large Language Models
[arXiv:2303.06689] · Versão v5
[Ficha do estudo             v]
Comparações do estudo
S1-C1 · Self-planning    [Aberta]
HumanEval · code-davinci-002
Pass@1 · maior é melhor
Base · Direct               48,1%
Intervenção · Self-planning  60,3%
Localizador ...
Revisão humana pendente
[Origem da extração           v]
S1-C2 ...                 [Abrir]
```

### Sobre

```text
DESKTOP
Sobre a revisão
+------------------------+  +---------------------------------------------------+
| Nesta página           |  | Método e recorte                                  |
| Método e recorte       |  | Revisão rápida · quatro tarefas · período e bases |
| Como ler               |  | Como ler o Guia e as comparações                  |
| Conferência humana     |  | Cobertura do Guia e do Explorador                 |
| Versão e documentos    |  | Conferência por amostra e formas de registro      |
+------------------------+  | Versão dos dados · corte · revisão de origem      |
                            | [Ler a monografia (PDF)] [Repositório do projeto] |
                            +---------------------------------------------------+

CELULAR
Sobre a revisão
[Nesta página                v]
Método e recorte
...
Como ler
...
Conferência humana
...
Versão e documentos
[Ler a monografia (PDF)]
[Repositório do projeto]
```

## 3. Sistema visual

A interface deve parecer uma **publicação técnica consultável**. Usar fundo levemente quente no tema claro, superfícies simples, texto alinhado à esquerda e bastante espaço entre uma observação e outra. Reservar a cor de destaque para ações. Aplicar as cores de evidência apenas aos selos. Um cartão inteiro verde daria peso excessivo a uma palavra e esconderia as ressalvas.

```css
:root {
  color-scheme: light;
  --fundo: #F5F4EF;
  --superficie: #FFFFFF;
  --painel: #ECEEEB;
  --texto: #182923;
  --secundario: #43564E;
  --borda: #71827A;
  --acao: #125641;
  --sobre-acao: #FFFFFF;
  --foco: #7044AF;

  --favoravel: #155B45;      --favoravel-fundo: #E4F2E9;
  --contraria: #872D42;      --contraria-fundo: #FBE8EB;
  --dividida: #714600;       --dividida-fundo: #FAEFCF;
  --indireta: #304D82;       --indireta-fundo: #E9EFFB;
  --insuficiente: #515565;   --insuficiente-fundo: #ECECF2;

  --melhora: var(--favoravel);    --melhora-fundo: var(--favoravel-fundo);
  --piora: var(--contraria);      --piora-fundo: var(--contraria-fundo);
  --igual: var(--indireta);       --igual-fundo: var(--indireta-fundo);
  --sem-direcao: var(--dividida); --sem-direcao-fundo: var(--dividida-fundo);
  --descritiva: var(--insuficiente);
  --descritiva-fundo: var(--insuficiente-fundo);

  --fonte: system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: ui-monospace, "SFMono-Regular", Consolas, monospace;
  --texto-pequeno: .875rem; --corpo: 1rem; --subtitulo: 1.125rem;
  --h2: 1.5rem; --h1: clamp(1.875rem, 4vw, 2.625rem);
  --entrelinha: 1.55; --entrelinha-titulo: 1.18;
  --e1: .25rem; --e2: .5rem; --e3: .75rem; --e4: 1rem;
  --e5: 1.5rem; --e6: 2rem; --e7: 3rem; --e8: 4rem;
  --raio-controle: .375rem; --raio-cartao: .625rem; --raio-selo: .375rem;
  --sombra: 0 2px 8px #18292312;
  --largura: 80rem; --leitura: 68ch; --lateral: 19rem;
  --alvo: 2.75rem;
  --bp-medio: 48rem; --bp-amplo: 64rem;
}
:root[data-tema="escuro"] {
  color-scheme: dark;
  --fundo: #101714; --superficie: #18221E; --painel: #222E28;
  --texto: #EDF3ED; --secundario: #B6C6BD; --borda: #81978B;
  --acao: #9CDAB9; --sobre-acao: #112319; --foco: #DDC1FF;
  --favoravel: #A7E0BE;    --favoravel-fundo: #1E392C;
  --contraria: #FFC1CC;    --contraria-fundo: #452731;
  --dividida: #F2D18A;     --dividida-fundo: #3E3421;
  --indireta: #B8CEFF;     --indireta-fundo: #28354B;
  --insuficiente: #D4D4E6; --insuficiente-fundo: #30313C;
  --sombra: 0 2px 8px #00000038;
}
:focus-visible {
  outline: 3px solid var(--foco);
  outline-offset: 3px;
}
```

Aplicar `data-tema` ao elemento raiz com o tema resolvido. Em **Sistema**, acompanhar mudanças de `prefers-color-scheme`. Usar borda de 1 px em controles, sublinhado nos links de texto, corpo de 16 px e metadados de pelo menos 14 px. Reservar a monoespaçada para IDs e identificadores. Usar algarismos tabulares nos pares numéricos.

**Layout.** Até `47.99rem`, uma coluna, margem lateral de 16 px e cartões de comparação. A partir de `48rem`, margem de 24 px e tabela quando houver espaço para o par inteiro. A partir de `64rem`, lateral de 19 rem e conteúdo flexível, com intervalo de 32 px. Escrever os valores literais nos `@media`. Se a coluna de resultados ficar estreita por zoom ou por texto longo, usar a apresentação em cartões mesmo em janela larga.

| Dimensão | Símbolos e textos visíveis | Uso |
|---|---|---|
| Evidência da **linha** | `+ Favorável` · `− Contrária` · `± Dividida` · `≈ Indireta` · `? Insuficiente` | Selo com fundo correspondente, sempre precedido pelo contexto “Evidência da linha”. |
| Direção da **comparação** | `↑ Melhora` · `↓ Piora` · `= Igual` · `— Sem direção` · `≡ Descritiva` | Texto compacto junto da métrica. A seta representa a direção favorável ou desfavorável definida para a métrica. |
| Revisão humana | `Revisão humana pendente` · `Revisão humana confirmada` · `Revisão humana sem registro` | Texto neutro em ambos os temas. Acrescentar a modalidade documentada quando confirmada. |

**Rótulos compostos são conteúdo.** Em G8, apresentar `+ favorável` e `− contrária em parte`, mantendo o texto acessível integral **“favorável; contrária em parte”**. Em R2, preservar **“favorável em um estudo; indireta fora dele”**. Em G1, a expressão **“com orçamento igualado”** fica junto de **“contrária”**, inclusive a 360 px. Ocultar os símbolos das tecnologias assistivas com `aria-hidden="true"`. A unidade de leitura é o texto completo.

Nas combinações de cores especificadas, o menor contraste calculado entre texto e fundo de selo é **6,29:1**. O texto secundário tem pelo menos **6,72:1** sobre as três superfícies de cada tema. A borda de controle tem pelo menos **3,48:1**. A verificação final inclui foco, estados interativos, zoom e cores forçadas. [WCAG 2.2](https://www.w3.org/TR/WCAG22/)

## 4. Componentes e comportamento

| Componente | Anatomia e estados | Interação, celular e acessibilidade |
|---|---|---|
| Navegação | Nome, três destinos, tema, procedência. Página atual sublinhada. | `<nav aria-label="Principal">`, `aria-current="page"`, link inicial **Pular para o conteúdo**, um `h1` por rota e título de janela atualizado. No celular, nome e tema na primeira linha, os três destinos na segunda. |
| Formulário do Guia | `fieldset` **O que você precisa fazer?**, quatro rádios. `fieldset` **Quais recursos você tem?**, caixas independentes. Orçamento com **Uma chamada**, **Várias chamadas**, **Ainda não sei**. Começa sem tarefa. | Atualiza ao selecionar, conserva o foco no controle e anuncia apenas o resumo em `role="status"`. **Ir aos resultados** salta ao título dos grupos. No celular, recolher condições por ação explícita ou após aplicar cenário, com **Editar condições** sempre visível. |
| Condições específicas | Separar **testes executáveis** de **executor sem suíte**, e **compilador** de **analisador estático**. Em depuração, mostrar **Você consegue reproduzir o defeito?** e **Você tem uma mensagem, saída ou relato do defeito?** | Para reprodução: **Por teste**, **Por depurador ou contraexemplo**, **Não**, **Ainda não sei**. “Por teste” também marca testes executáveis. Ao desmarcar testes, limpar “Por teste”. Uma suíte disponível pode coexistir com “Não reproduz”. Rótulos e ajudas associados aos controles. |
| Chips de cenário | Oito botões agrupados por tarefa. Cada botão tem nome de uso, como **C para Rust com testes**. O selecionado recebe contorno e texto **Em uso**. Abaixo, resumo de domínio, verificação, objetivo e orçamento literal. | Botões nativos com `aria-pressed`. Enter ou Espaço aplica o exemplo inteiro, substituindo o formulário anterior. Anunciar o nome aplicado. Chips quebram linha. No celular, ficam sob **Usar um dos 8 cenários**. |
| Grupo de linhas | Título, quantidade e lista na ordem do CSV. Exibir os três títulos, inclusive com zero. | Links de salto com nome e quantidade. O total da tarefa é o número de IDs distintos. Nenhuma ordenação por evidência ou força. |
| Cartão de linha | Fechado: ID, agrupamento literal, selo completo, resultado medido e motivo da posição. Aberto: condição, indicação, força descritiva, ressalvas, comparações e estudos citados. | Botão no título com `aria-expanded` e `aria-controls`. Nome acessível **Abrir linha G7, Planejamento ou decomposição antes do código**. Um cartão aberto por vez. Recolher devolve foco ao botão. Links internos ficam fora dele. |
| Selo de evidência | Cada cláusula conserva sua cor, palavra e qualificadores. “Aprox.”, “em um estudo” e “sem contagem própria” permanecem textuais. | Elemento de texto. Sem ação, tooltip obrigatório ou foco adicional. Força descritiva ocupa campo próprio. |
| Comparações | Desktop com tabela, `caption` e cabeçalhos. Modelo, benchmark, métrica, base, intervenção, direção e revisão humana por ID. Detalhe com técnica, comparador, condições, localizador completo, fonte e proveniência. | Celular com um `article` e `dl` por registro. Só uma representação fica na árvore de acessibilidade. Nenhuma informação depende de passar o mouse. O link **Ver comparação S1-C1** abre a página do estudo no registro certo. |
| Filtros | Busca por ID de estudo ou comparação, título, técnica, comparador, modelo, benchmark ou métrica. Seletores **Tarefa**, **Mecanismo acrescentado**, **Direção da comparação**. Botão **Limpar filtros**. | `<form role="search">`, rótulos visíveis. Busca ignora maiúsculas e acentos, mantém hífens de IDs pesquisáveis e exige todos os termos digitados. No celular, painel expansível no fluxo da página. **Ver resultados** recolhe e foca o total. |
| Lista e paginação | 25 itens por página. Comparações na ordem das extrações, estudos por número do ID e comparações do estudo por número de `C`. Exibir intervalo e total. | `<nav aria-label="Paginação">`, links **Anterior** e **Próxima**, página atual textual. Extremos inativos. Mudança de página foca o título da lista. |
| Matriz | Linhas por mecanismo, colunas por tarefa. Eixos em ordem fixa. Célula com contagem absoluta. Zero aparece como `0`. | Tabela com `caption` e `scope` nos dois eixos. Célula positiva é link, por exemplo **Ver 181 comparações de geração com contexto acrescentado**. No celular, quatro seções expansíveis por tarefa com contagens por mecanismo. |
| Aviso de limite | Uma frase perto do dado que ela qualifica. Texto persistente para amostra, pacote, falta de reprodução, classificação parcial ou cobertura. | `<aside>` com título visível quando houver mais de uma frase. Reservar `role="alert"` para falha que impeça carregar a consulta. Limites científicos permanecem disponíveis sem interação. |
| Rodapé de versão | **Tabela v2 · Extração ex-v2.2 · Corte 07/09/2026**. Link **Versão e documentos**. Em Sobre, revisão de origem e data real da publicação. | `<footer>`, quebra natural entre itens. Alvos interativos de 44 × 44 px. Data com `<time datetime="2026-09-07">`. |

Na mudança de rota, focar o `h1`, a seção solicitada ou a comparação solicitada. Alterações dentro do formulário mantêm o foco de edição. Respeitar `prefers-reduced-motion` e `forced-colors`. A ordem visual acompanha a ordem do DOM.

### Regras da matriz e das referências

**Matriz.** A unidade escolhida para este produto é a **comparação distinta**. Contar uma vez cada `id` por par `(tarefa da comparação, mecanismo acrescentado)`. Um ID com três mecanismos entra em três células e uma única vez no total da busca. Exibir os mecanismos em ordem fixa: instrução, contexto, restrições, exemplos, decomposição, feedback, raciocínio, amostragem, multiagente, otimização de prompt e outro. Acrescentar **Nenhum mecanismo acrescentado** para listas de mecanismos vazias. Os filtros também afetam a matriz. A célula abre a lista com sua tarefa e mecanismo, conservando direção e busca. A contagem deve coincidir exatamente com o total dessa lista. A tabela `09` da síntese fornece a referência por comparação. A tabela `07` usa estudos com técnicas focais e tem outra unidade. [Contagens de referência](<../evidencias/sinteses/tabelas/09-direcao-comparacoes.csv>)

**Referências das linhas.** Resolver `Sxxx-Cn` para aquela comparação e `Sxxx` para a ficha do estudo. Usar `estudos_ids` como lista principal, na ordem registrada. Tornar navegáveis também as referências adicionais explícitas da indicação e das ressalvas, indicando sua origem e evitando duplicação na mesma lista. Em G14, **S556** abre o estudo. Em T5, mostrar **Estudos citados** para S1220, S1803 e S1836. Em R5, S958 também é referência ao estudo. Um ID de estudo sozinho nunca seleciona automaticamente `C1`. Referência sem destino recebe o texto **Referência sem registro nesta versão**.

## 5. Como mostrar base, intervenção e conferência

Cada par ocupa um bloco com **um ID, um modelo, um benchmark, uma métrica e sua unidade**. A mesma composição aparece no Guia, no Explorador e no Estudo.

| Exemplo real da comparação S1-C1 | Apresentação |
|---|---|
| Contexto | **HumanEval · code-davinci-002 · Geração** |
| Métrica | **Pass@1 · percentual · maior é melhor** |
| Base | **Direct — 48,1%** |
| Intervenção | **Self-planning — 60,3%** |
| Direção | **↑ Melhora** |
| Fonte | **Tabela 1, p. 7, colunas HumanEval / Pass@1, linhas Direct e Self-planning**. Abrir o identificador do estudo. |
| Procedência | **Extração por IA · Revisão humana pendente**. Em **Origem da extração**, exibir executor, modelo executor e data registrados. |

O exemplo corresponde à extração `S1-C1` e à afirmação A77. A versão v5 pertence ao cadastro bibliográfico de S1. Mostrar separadamente uma versão de leitura específica quando houver registro correspondente. [Afirmação A77](<../dados/afirmacoes.csv:78>) · [Referência cadastrada de S1](https://arxiv.org/abs/2303.06689v5)

- Usar a escala e a precisão disponíveis na fonte de dados, com vírgula decimal. `48.1` com unidade `percentual` vira `48,1%`. Uma proporção conserva sua escala. Tempo, contagem, energia e temperatura conservam a unidade documentada. Base zero aparece como `0`.
- A tela padrão mostra os dois valores diretamente. Dispensar barras, eixos comuns, diferenças relativas ou totais de desempenho. Se o texto original mencionar diferença em pontos percentuais, escrever **p.p.**. Uma variação relativa usa **%** e precisa de origem documentada.
- Reproduzir a regra `variacao` do projeto. Com dois números e `maior_melhor` ou `menor_melhor`, classificar a diferença no sentido da métrica. Diferença zero dá **Igual**. Quando a direção é indeterminável, usar **Descritiva** se o comparador estiver ausente conforme a síntese, ou **Sem direção** nos demais casos. Aplicar a regra sobre os valores originais, antes da formatação. [Definição de direção](<../scripts/validar_ficha_extracao.py:113>)
- Resultados textuais, nulos e denominadores incertos conservam sua explicação. Para um `null` sem motivo registrado, usar **Sem valor registrado**. Traduzir os estados explícitos separadamente: `nao_conferido` → **Não conferido**, `nao_informado` → **Não informado pela fonte**, `nao_aplicavel` → **Não se aplica**, `fonte_indisponivel` → **Fonte indisponível**. Conservar qualificadores que acompanhem esses estados.
- Revisão humana vem de `revisao_humana` **do registro apresentado**. Para `confirmada`, mostrar revisor, data e modalidade disponíveis. `formulario` → **Conferência registrada por bloco**. `declaracao_autor` → **Conferência declarada pelo autor para a ficha**. Um registro pendente continua pendente mesmo quando existe uma afirmação relacionada conferida. A conferência da extração, a dos metadados e a revisão por pares do artigo são informações distintas. [Registro da conferência humana](<../monografia/capitulos/04d-conferencia.tex:1>)

## 6. Cenários que preenchem o Guia

A tabela abaixo define os preenchimentos iniciais. Marcar apenas o que está descrito. Um recurso omitido fica **não marcado**. O resumo preserva negativas explícitas, como a ausência de oráculo no cenário COBOL. Todos os oito admitem várias chamadas, mas a unidade e o limite diferem.

| Cenário e nome do botão | Marcar | Informação que continua visível depois do preenchimento |
|---|---|---|
| G1 · Funções Python com testes | Geração, testes, várias chamadas | 3 a 10 testes públicos por função, suíte oculta para aceitação e até 5 chamadas por função. Os testes ocultos ficam fora do prompt. |
| G2 · Solidity com modelo local | Geração, compilador, analisador, modelo pequeno local, várias chamadas | Solidity 0.8.x, `solc`, analisador de vulnerabilidades, até 8B, sem testes unitários e até 3 chamadas por contrato. |
| D1 · Função Python com teste falhando | Depuração, testes, reprodução por teste, diagnóstico disponível, várias chamadas | Teste falho, mensagem e traceback. Até 10 chamadas por defeito. |
| D2 · Relato de defeito em Java | Depuração, testes, compilador, contexto, diagnóstico disponível, **não reproduz**, várias chamadas | Repositório Maven, localização desconhecida e suíte que só verifica regressões. Até 20 chamadas por defeito. |
| T1 · C para Rust com testes | Tradução, compilador, testes, várias chamadas | C99 para Rust, `rustc` e suíte portada. Preservar a unidade original **até 5 rodadas de correção por função**. |
| T2 · COBOL para Java sem testes | Tradução, compilador, várias chamadas | Só compilador Java, sem testes automatizados nem oráculo de equivalência. Até 3 chamadas por programa. |
| R1 · Métodos Python com testes | Refatoração, testes, analisador, várias chamadas | O analisador é o medidor de complexidade e *code smells*. Até 3 chamadas por método. |
| R2 · Migração de API em Java | Refatoração, compilador, testes, contexto, várias chamadas | Documentação, changelog e benchmarks de desempenho, cerca de 200 arquivos interdependentes. Até 2 chamadas **por arquivo**. |

Ajuda junto dos botões: **“Estes oito cenários são sintéticos. Foram usados para examinar a tabela de apoio. Você pode alterar as condições depois de escolher um exemplo.”** Exibir a hipótese somente sob demanda. O exame documentado usou os cenários v2 e a tabela v1 congelada. A tabela v2 incorpora ajustes posteriores. [Oito cenários v2](<../evidencias/sinteses/cenarios-v2.md>)

## 7. Recursos exigidos pelas 31 linhas

Este mapeamento é uma **decisão editorial proposta para a interface**. O CSV continua sendo a fonte do texto científico. A coluna **Regra do Guia** define o comportamento implementável. A última coluna identifica limites da classificação.

**Legenda.** `T` testes executáveis, `C` compilador, `A` analisador estático, `K` contexto recuperável, `E` exemplos disponíveis, `V` várias chamadas, `P` modelo pequeno local. **Nenhum** significa que a linha dispensa um requisito comum entre os recursos do formulário. `+` exige ambos. **Ou** aceita alternativas. **Incerta** indica que o agrupamento mistura variantes ou que o formulário cobre apenas parte da condição.

**Precedência dos grupos:**

1. **Lacunas declaradas.** Entram G12, G13, G14, D7, T2, T5, R4 e R5, respeitando a tarefa. G12 recebe **Lacuna parcial, por variante** e conserva “dividida; insuficiente por variante”. Mostrar a condição temática mesmo quando o usuário não a marcou. Cada linha aparece uma única vez.
2. **Exigem recurso não marcado.** Entre as demais, entram as linhas cujo requisito obrigatório ainda não foi satisfeito. Dizer **“Falta marcar…”** ou **“Falta informar…”**. Uma resposta desconhecida conserva esse estado.
3. **Aplicáveis às condições marcadas.** Entram as demais linhas. Para regras incertas, exibir **“Aplicação parcial. Confira a variante e as condições estudadas.”** Uma linha pode ser aplicável e ter evidência contrária ou indireta.

A ordem visual dos grupos é **Aplicáveis**, **Exigem recurso**, **Lacunas**. A precedência acima serve apenas para decidir em qual deles entra cada ID.

| ID | Agrupamento abreviado | Regra do Guia | Precisão e condição a explicar |
|---|---|---|---|
| G1 | Feedback de testes ou execução | `(T ou executor) + V` | O laço precisa de retorno de execução. Explicitar a base de chamada única e a ressalva de orçamento igualado. |
| G2 | Compilador ou analisador | `C ou A` | **Incerta quanto a V.** As rodadas cumulativas exigem iteração. A linha também inclui uso de relatório estático. Testes disponíveis não impedem consultar a evidência sobre compilação. |
| G3 | Autocrítica sem execução | `V` | **Incerta quanto ao número exato.** O mínimo editorial representa o ciclo de criticar e reescrever. Porte pequeno é uma ressalva em um estudo. |
| G4 | Multiagente com papéis | `V` | A quantidade varia por arranjo. Marcar várias chamadas não assegura que um pacote caiba no teto do cenário. |
| G5 | Amostragem e seleção | `V` | **Incerta.** Usar V como aproximação para vários candidatos. Explicar a necessidade de um seletor, como testes gerados ou modelo de valor. Uma API pode gerar diversos candidatos em uma chamada. |
| G6 | Instrução de raciocínio | Nenhum | Raciocínio produzido pelo mesmo modelo. A evidência permanece dividida. |
| G7 | Planejamento ou decomposição | `V` | A linha estudada descreve duas ou mais etapas e cita chamadas adicionais. Exibir o limite do nível de função. |
| G8 | Contexto recuperado | `K` | Repositório ou documentação acessível. Identificar nas ressalvas recuperadores treinados e contexto obtido do gabarito. |
| G9 | Exemplos em contexto | `E` | Exemplos fixos, aleatórios ou recuperados. K só se aplica à variante de recuperação. |
| G10 | Especificação e testes no prompt | Nenhum | **Incerta por variante.** Regras de formato ou pré e pós-condições podem ser fornecidas em texto. Incluir um teste no prompt requer seu conteúdo, independentemente de poder executá-lo. |
| G11 | Instruções de segurança | Nenhum | O scanner aparece como instrumento de medição em estudos. A interface não exige scanner para escrever uma diretriz. |
| G12 | Formulação, língua e otimização | **Lacuna parcial**. Nenhum comum | **Incerta por variante.** Reformulação pode usar uma chamada. Busca e otimização podem usar várias. Preservar as duas cláusulas da evidência. |
| G13 | Distribuição do orçamento fixo | **Lacuna**. `V` no contexto descrito | Transversal. Conservar o limite de chamadas e a diferença entre igualar tentativas, tokens e custo. |
| G14 | Linguagens de domínio e modelos pequenos | **Lacuna**. `P` em parte dos casos | **Incerta como exigência única.** Solidity e pequeno porte são dimensões distintas. P contextualiza o recorte de modelos de até 8B. |
| D1 | Feedback em laço para reparo | `V` + reprodução por teste, depurador ou contraexemplo | Se a reprodução for por teste, requer T. Uma suíte que não dispara o defeito deixa essa linha no grupo de recurso faltante. |
| D2 | Informação diagnóstica | Nenhum dos recursos gerais + **diagnóstico disponível** | **Incerta por variante.** Um relato basta para a variante textual. Mostrar em destaque a localização perfeita no estudo citado para essa variante. |
| D3 | Contexto e ingredientes recuperados | `K` | **Incerta por variante.** Testes disparadores e localização perfeita são frequentes. Exibir essas dependências junto à indicação. |
| D4 | Exemplos para reparo | `E` | Exemplos fixos, históricos ou selecionados. Preservar as inversões descritas. |
| D5 | Raciocínio explícito no reparo | Nenhum | **Incerta por variante.** Instrução e explicação podem caber em uma chamada. ReAct pode exigir interação. Manter **contrária** mesmo no grupo aplicável. |
| D6 | Decomposição, planejamento e agentes | `V` | **Incerta quanto à reprodução.** Variantes que usam rastros exigem reproduzir a falha. Se faltar reprodução, indicar aplicação parcial no cartão. |
| D7 | Reparo sem reprodução conhecida | **Lacuna**. Nenhum | O cenário da lacuna combina relato, ausência de reprodução e localização desconhecida. Uma suíte de regressão pode estar disponível. |
| T1 | Reparo com testes e compilador | `T + C + V` | Conjunção dos três recursos para o reparo iterativo. A sozinho não satisfaz C. |
| T2 | Feedback só do compilador | **Lacuna**. `C` no contexto descrito | O resultado medido é compilação. Preservar a lacuna para equivalência de comportamento. |
| T3 | Exemplos para tradução | `E` | **Incerta quanto a K.** Recuperação e seleção estrutural são variantes. O requisito comum são os exemplos. |
| T4 | Explicação e duas etapas | Nenhum comum | **Incerta.** Para a variante explicitamente em duas chamadas, exigir V na descrição da variante. Explicação no mesmo prompt e o contraste *one-shot* impedem impor V à linha inteira. |
| T5 | Linguagem legada ou migração de plataforma | **Lacuna**. Nenhum | Linguagem e plataforma delimitam a questão. Manter as referências no nível de estudo. |
| R1 | Tipo de refatoração especificado | Nenhum | O usuário precisa saber o tipo pretendido. O desfecho é o recall na identificação de oportunidades. |
| R2 | Esquema de API e changelog | `K` | **Incerta quanto ao conteúdo de K.** Mostrar **“Confira se há esquema da API e changelog.”** Estudo único em Terraform, número de chamadas não informado. |
| R3 | Exemplos para refatoração | `E` | Testes e complexidade são desfechos distintos. A linha conserva a classificação composta. |
| R4 | Feedback, iteração e raciocínio | **Lacuna**. Nenhum comum | **Incerta.** Variantes usam T, C, A ou V. A instrução CoT aparece no mesmo agrupamento. Exibir essas alternativas. |
| R5 | Escala de repositório e desempenho | **Lacuna**. `K` como contexto do problema | **Incerta como requisito técnico.** Acesso ao repositório caracteriza a situação. A lacuna envolve mudanças interdependentes e desempenho no conjunto. |

## 8. Microcopy de produção

### Formulário e resultados

| Elemento | Texto |
|---|---|
| Introdução | **“Consulte o que os estudos mediram para sua tarefa e seus recursos.”** |
| Ajuda dos recursos | **“Marque o que você pode usar. Uma caixa em branco significa que o recurso ainda não foi indicado.”** |
| Contexto | **“Tenho repositório, histórico ou documentação de onde recuperar contexto.”** |
| Exemplos | **“Tenho exemplos que posso incluir no prompt.”** Ajuda: “Uma descrição da tarefa e sua assinatura, sozinhas, não contam como demonstração.” |
| Modelo pequeno | **“Uso um modelo pequeno, executado localmente.”** Ajuda: “A linha G14 discute, entre outros casos, modelos de até 8 bilhões de parâmetros.” |
| Orçamento | **“Quantas chamadas ao modelo você pode usar?”** Ajuda: “Várias chamadas podem permitir uma nova tentativa ou etapa. Confira o orçamento específico de cada estudo.” |
| Grupo aplicável | **“Estas linhas têm ao menos uma forma de uso compatível com os recursos informados. Leia o resultado medido e as ressalvas.”** |
| Recurso faltante | **“Para esta linha, falta marcar testes executáveis e compilador.”** Gerar a frase a partir da regra, preservando **e** ou **ou**. |
| Lacunas | **“A revisão identificou evidência insuficiente para estas condições. Abra a linha para ver o que chegou a ser medido.”** |
| Nenhuma linha aplicável | **“Nenhuma linha atende aos recursos marcados. Veja os recursos exigidos e as lacunas desta tarefa.”** |
| Grupo vazio | **“Nenhuma linha deste grupo para as condições atuais.”** |
| Falta de reprodução | **“A suíte roda, mas não reproduz o defeito. Ela pode apontar regressões. A linha D1 exige uma forma de observar a falha.”** |
| Busca sem resultado | **“Nenhuma comparação corresponde aos filtros atuais.”** Ação: **Limpar filtros**. |
| Estudo sem comparação | **“Este estudo tem ficha no corpus. Nenhuma comparação foi extraída para ele nesta versão.”** |
| Carregando ou erro | **“Carregando os dados da revisão…”** / **“Não foi possível carregar os dados desta versão.”** Ação: **Tentar novamente**. Em falha de integridade, identificar a coleção afetada. |
| ID inválido | **“Esta comparação não consta neste estudo.”** Ações: **Ver comparações do estudo** e **Abrir o Explorador**. |
| Direção desconhecida | **“Sem direção. Falta um par numérico ou um sentido definido para a métrica.”** |
| Descritiva | **“Descritiva. O registro apresenta um resultado sem comparador.”** |

### Texto integral de “Como ler”

> Comece pela tarefa e pelas condições de uso. Cada linha reúne estudos sobre um agrupamento de técnicas. Leia juntos a condição estudada, o resultado medido, a indicação e as ressalvas. “Aplicável” significa que os recursos marcados permitem ao menos uma forma de uso descrita. A evidência dessa forma de uso pode ser dividida, indireta ou contrária.
>
> “Favorável” indica que a maioria das comparações do agrupamento registrou melhora no sentido da métrica de cada estudo. “Contrária” indica resultados que pesam contra a orientação examinada. “Dividida” indica variação entre comparações ou condições. “Indireta” indica que o desenho ou o resultado medido responde apenas em parte à questão prática. “Insuficiente” identifica uma lacuna. Leia os qualificadores: uma linha pode ser favorável em um estudo e indireta fora dele.
>
> Quando a indicação diz “favorável ao pacote”, várias mudanças foram avaliadas em conjunto. Abra uma comparação para ver o que foi acrescentado, qual foi a base e em que modelo, benchmark e métrica os valores foram obtidos. A força descritiva informa quantos estudos ou tipos de contraste sustentam a linha, com as aproximações registradas na tabela.
>
> Os benchmarks e as métricas diferem entre estudos. Por isso o Guia preserva a ordem da tabela e apresenta os pares de valores separadamente. A proporção de melhoras depende da escolha dos contrastes e do viés de publicação. Ela não estima a chance de sucesso no seu projeto. Compilação, aprovação em testes, similaridade textual e alertas de scanner também têm alcances diferentes. Produtividade, segurança em uso e economia de custo exigem medições próprias.
>
> As extrações foram feitas por IA. O autor conferiu uma amostra de 67 estudos. Em cada comparação, consulte o estado da revisão humana e o localizador para encontrar o resultado na fonte. Contagens e direções podem mudar com correções futuras.

**Sobre.** Identificar Caio César de Freitas, Engenharia de Sistemas/UFMG, e o trabalho como revisão rápida. Informar as quatro tarefas, o período de **01/01/2021 a 07/09/2026** para a primeira versão pública, os idiomas português e inglês, as buscas em ACM Digital Library, IEEE Xplore e arXiv e os recortes efetivamente aplicados: restrição de tarefa no título, ausência de *snowballing* amplo e recorte da versão da banca para estudos com indício de revisão por pares. Explicar a conferência por amostra e a diferença entre conferência por bloco e declaração por ficha. [Protocolo da revisão](<../protocolo/protocolo.md>)

**Documentos.** Usar **Ler a monografia (PDF)** para um PDF público verificado ou para uma cópia estática autorizada do PDF existente, em URL relativa como `./publicacoes/monografia.pdf`. O checkout contém o PDF compilado, mas não estabelece uma URL pública permanente para ele. Até haver um destino válido, mostrar **“Link público da monografia pendente nesta versão.”** Para o GitHub, usar **Repositório do projeto · acesso restrito** enquanto essa for a visibilidade real. A publicação do site pode manter o repositório de pesquisa privado. [Repositório do projeto](https://github.com/caiofreitas1/tcc2-prompt-engineering)

## 9. Critérios de aceitação

| Verificação | Resultado esperado |
|---|---|
| Contagem e identidade | 31 IDs de linha, 8 IDs de cenário, 805 IDs únicos de comparação e 332 fichas. E1 e E2 ficam fora do Explorador. Uma ficha sem comparação continua acessível pelo índice. |
| Guia sem tarefa | Exibe a pergunta, condições e cenários. Nenhuma técnica aparece pré-selecionada como indicação. |
| Ordem e completude | A união dos três grupos contém todas as linhas da tarefa mais G13, sem repetição. Cada grupo respeita a ordem do CSV. G13 é contado uma vez no total de 31. |
| Cenário G1 | Com o mapeamento proposto, aparecem 8 aplicáveis, 3 com recurso faltante e 3 lacunas. G1 preserva “contrária com orçamento igualado”. G7 abre S1-C1. |
| Cenário D2 | Testes, compilador e contexto ficam marcados. Reprodução fica em **Não**. D1 aponta falta de reprodução, D2 mostra a ressalva sobre localização e D7 permanece como lacuna. |
| Cenários T2 e R2 | COBOL com compilador e sem testes mantém T1 fora de aplicáveis e exibe T2 e T5 como lacunas. Em R2, acesso à documentação permite consultar a linha R2 e a lacuna R5 permanece visível. |
| Evidência composta | G8 conserva as duas cláusulas, G12 aparece uma vez como lacuna parcial, R2 conserva “em um estudo” e “fora dele”, R3 distingue aprovação e complexidade. Os textos sobrevivem à quebra de linha e ao leitor de tela. |
| Comparação verificável | S1-C1 apresenta Direct 48,1%, Self-planning 60,3%, HumanEval, code-davinci-002, Pass@1, localizador, arXiv e revisão humana pendente. A abertura pelo Guia e pelo Explorador leva ao mesmo registro. |
| Direções da versão | Sem filtros, reproduzir **516 melhoras, 145 pioras, 28 iguais, 91 sem direção e 25 descritivas**. Um valor menor em métrica `menor_melhor` pode ser melhora. Igualdade numérica e ausência de significância estatística conservam significados distintos. |
| Matriz | Sem filtros, geração × contexto abre **181** comparações e refatoração × contexto abre **12**. Após filtrar por direção ou busca, toda célula positiva abre exatamente sua contagem. |
| Fontes e revisão | S556 em G14 leva ao estudo. DOI e arXiv usam o identificador cadastrado, com versão quando disponível. Ausência de identificador produz texto explicativo. Nenhum trecho citado ou caminho de PDF primário consta do JSON público, do HTML ou da busca. |
| Links e retorno | Recarregar um hash, abri-lo em outra aba e usar Voltar preserva o estado relevante. Abrir comparação pelo teclado leva o foco ao registro correto. Busca ou expansão não desloca o foco durante a digitação. |
| Acessibilidade | Percorrer todas as ações por teclado, com foco visível, nomes compreensíveis e ordem coerente. Verificar os dois temas, cores forçadas, zoom de 200%, reflow a 320 CSS px e uso a 360 px. Sem rolagem horizontal do documento ou valores cortados. Texto comum com contraste mínimo de 4,5:1, controles e foco com pelo menos 3:1. [WCAG 2.2](https://www.w3.org/TR/WCAG22/) |
| Publicação | Abrir o site no subcaminho real do GitHub Pages, testar uma rota profunda, o JSON e o PDF da monografia. O rodapé usa revisão e data reais. Link privado é identificado como tal. |

Os principais riscos de interpretação ficam tratados no próprio ponto de leitura: “aplicável” ao lado da condição, “favorável ao pacote” junto da indicação, “melhora” junto da métrica, “revisão humana” junto da comparação e “comparações” junto de cada contagem da matriz. A classificação de recursos, o tratamento de G12 como lacuna parcial e a unidade da matriz são decisões de design explicitadas para implementação. **Nenhum arquivo foi alterado.**