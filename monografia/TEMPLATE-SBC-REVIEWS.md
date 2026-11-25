# Artigo no formato SBC Reviews — adoção em T16 (24/11/2026)

## Pedido e origem

Em 24/11/2026 o autor trouxe, em conversa, o pedido do orientador: «Sobre o artigo, você conseguiria
colocar no formato da revista SBC Reviews? Além disso, seria legal traduzir o texto para o inglês,
apesar de não ser obrigatório.» O autor decidiu ter as duas versões, em português e em inglês (D140).
Até então o artigo usava o IEEE Conference Template ([TEMPLATE.md](TEMPLATE.md)); a monografia ABNT
([TEMPLATE-MONOGRAFIA.md](TEMPLATE-MONOGRAFIA.md)) não muda.

Este documento registra a adoção do formato. **Não há submissão à revista nem homologação do formato
pelos editores.** Os campos do cabeçalho da primeira página («SBC Computing Reviews, 202X», ISSN, DOI
`10.5753/rocs.202X.XXXXXX`, licença CC BY 4.0 e datas) são marcadores do template, preenchidos pelos
editores quando um artigo é aceito.

Fontes consultadas em 24/11/2026:

- [Página de submissões da SBC Reviews](https://journals-sol.sbc.org.br/index.php/reviews/about/submissions).
- *Author Guidelines* (PDF de agosto de 2025, ligado nessa página).
- [Repositório do template](https://github.com/sbc-reviews/sbc-reviews-template), commit
  `a460231fea64cc166d4302338a7dc4b86bf99235` (31/08/2025), e o
  [modelo no Overleaf](https://www.overleaf.com/latex/templates/template-sbc-reviews-2025/qvbgfsxjsksb).

| Arquivo copiado sem alteração | Origem no repositório do template | SHA-256 |
|---|---|---|
| `monografia/sbcreviews-2025.cls` | `sbcreviews-class-latex/sbcreviews-2025.cls` | `952861d78cd1aa23a45c798d6ff391e66c69a45ee59f021ffd60dd045070f154` |
| `monografia/apalike-sol.bst` | `sbcreviews-class-latex/apalike-sol.bst` | `281ef4993ff26f6aaea19c58613ae09f3bdfce280196da8be73cfab6d919da8b` |

O repositório do template declara licença MIT; o cabeçalho da classe indica CC BY 4.0, da Sociedade
Brasileira de Computação. Os arquivos `aas_macros.sty`, `sectsty.sty` e `sol.jpg` do template não foram
copiados, porque o artigo não os usa.

## O que a revista exige e como está atendido

| Exigência (fonte) | Situação |
|---|---|
| Classe do template, sem alteração local do `.cls` (lista de verificação) | Atendida: cópia idêntica, hash acima. |
| Compilar com XeLaTeX ou LuaLaTeX (lista de verificação) | Atendida: `make pdf` e `make pdf-en` usam `latexmk -lualatex`. |
| Citações autor-ano com colchetes e estilo `apalike-sol` (template) | Atendida. |
| DOI nas referências, quando houver (*Author Guidelines*) | Atendida para as entradas com DOI; as três que só existem no arXiv trazem identificador e endereço. |
| Até 35 páginas com referências (*Author Guidelines*) | Português: 33 páginas. Inglês: 33 páginas. |
| Resumo da primeira página com até 2.000 caracteres (página de submissões) | Resumo: 1.653; *abstract*: 1.688. |
| Declarações obrigatórias: contribuições, conflitos de interesse, artefatos, uso de IA (*Author Guidelines*) | Seções presentes; conflitos de interesse **pendentes** dos autores; contribuições em rascunho a confirmar. |
| ORCID de todos os autores antes da publicação (*Author Guidelines*) | **Pendente** para Caio César de Freitas; os outros dois vêm de busca pública, a confirmar. |
| Artefatos em repositório com identificador persistente e licença (*Author Guidelines*) | **Pendente**: os artefatos estão no GitHub, sem DOI nem arquivo de licença. |

A adequação de uma revisão rápida ao escopo da revista (que cita revisões sistemáticas, multivocais,
de escopo e mapeamentos) é avaliação do orientador e dos editores, não deste registro.

## Adaptação

- `main.tex` (português) e `main-en.tex` (inglês) usam `sbcreviews-2025`; o que é comum fica em
  `sbc-comum.tex`. As declarações estão em `declaracoes.tex` e `declaracoes-en.tex`.
- **Capítulos compartilhados com a monografia.** Os arquivos de `capitulos/` continuam servindo aos dois
  documentos. As citações passaram de `\cite` a `\citep` (entre parênteses) e a
  `\citetexto{autores}{chave}` (no texto). No artigo, a segunda imprime os autores como estão no texto e
  o ano entre colchetes; na monografia, as duas voltam à citação numérica. O texto extraído do PDF da
  monografia ficou idêntico ao anterior (81 páginas); a única mudança posterior na monografia é a de D144,
  descrita em «Compilação e conferência».
- **Referências.** `referencias.bib` continua único. As notas «Versão consultada: arXiv:…» passaram a
  `\versaoconsultada{…}`, definida em cada documento no seu idioma. Nas três entradas que só existem no
  arXiv, `howpublished = {\soartigo{…}}` leva o identificador e o endereço ao artigo, porque o estilo
  da revista não imprime `eprint` nem `url`; na monografia a macro não imprime nada.
- **Tabelas.** Foram dimensionadas para a IEEEtran (coluna de 252 pt). Aqui a coluna tem 240 pt: o
  espaço entre colunas diminui e a tabela que ainda passar da largura é reduzida até caber. Só as duas
  partes da tabela de apoio são reduzidas, em cerca de 5%.
- **Apêndices.** Vêm depois das referências. Como as duas versões têm 33 páginas, a lista dos 332
  estudos (Apêndice B) permanece no artigo; a decisão do autor de transformá-la em material
  suplementar se o limite fosse ultrapassado não precisou ser aplicada.
- O estilo `apalike-sol.bst` imprime «In», «pages», «volume» e «and» em inglês também na versão em
  português, e põe os títulos em minúsculas. É o comportamento do estilo da revista.

## Dados de autoria (busca em fontes públicas, 24/11/2026)

Por decisão do autor, ORCID e e-mail foram buscados em fontes públicas. **Todos estão a confirmar.**

| Autor | Dado | Fonte |
|---|---|---|
| Eduardo Magno Lages Figueiredo | ORCID 0000-0002-6004-2718 | Registro público do ORCID: «Eduardo Figueiredo», professor do Departamento de Ciência da Computação da UFMG, doutorado em Lancaster. |
| Eduardo Magno Lages Figueiredo | e-mail institucional | [Perfil no DCC/UFMG](https://dcc.ufmg.br/professor/eduardo-figueiredo/). |
| Pedro Saint Clair Garcia | ORCID 0009-0005-7744-697X | Registro público do ORCID: «Pedro Garcia», UFMG. O registro lista obra assinada por «Pedro S. C. Garcia» em coautoria com Eduardo Figueiredo (doi:10.5753/sbes.2024.3503, Crossref). A correspondência com o coorientador é inferência, não confirmação. |
| Pedro Saint Clair Garcia | e-mail | Não localizado. |
| Caio César de Freitas | ORCID e e-mail institucional | ORCID não localizado (o único resultado do registro para o nome é de outra pessoa). O e-mail pessoal não foi usado. |

O endereço de correspondência é o do rodapé do sítio do DCC/UFMG. O envelope de autor correspondente
está no primeiro autor por falta de indicação; a escolha é dos autores.

## Tradução para o inglês

A tradução foi feita por Claude Code (Claude Fable 5.2) em 24/11/2026, arquivo por arquivo, em
`capitulos-en/`. **Não foi revisada pelo autor nem por outro humano.** O *abstract* é o de
`pretextual/abstract.tex`, traduzido em 18/11/2026 e também pendente de revisão.

- A tradução não condensa nem acrescenta conteúdo. Rótulos, chaves de citação, identificadores de
  estudos e comparações, marcas de afirmação e nomes de arquivos do repositório são os mesmos.
- `scripts/verificar_traducao.py`, chamado em `make check`, compara cada par de arquivos: rótulos,
  remissões, citações, identificadores, marcas de afirmação, quantidade de seções, tabelas, itens e
  linhas de tabela, e os números do texto (com separadores e datas normalizados). Ele acusa número
  trocado ou trecho omitido; **não avalia a qualidade do inglês nem a fidelidade do sentido.**
- O apêndice de estudos em inglês é gerado por `scripts/gerar_apendice_estudos.py`. A tabela de apoio em
  inglês traduz o `.tex` gerado por `scripts/gerar_tabela_apoio.py` e não é regenerada pelo script.
- «O autor» foi traduzido como *the author* e designa o primeiro autor, como no texto em português.
  Num artigo com três autores, a expressão pode precisar virar *the first author*, nos dois idiomas.
- O título em inglês, «Prompt Engineering for Software Coding and Implementation: A Rapid Literature
  Review», é proposta, pendente de aprovação do autor.

| Português | Inglês |
|---|---|
| revisão rápida | rapid review |
| triagem; título e resumo; texto completo | screening; title and abstract; full text |
| ficha (de extração) | (extraction) record |
| conferência; conferido | check; checked |
| linha de base; comparador | baseline; comparator |
| pacote; ingrediente; contraste pareado; cumulativo | package; ingredient; paired contrast; cumulative |
| contrafactual; mecanismo; rótulo | counterfactual; mechanism; label |
| tabela de apoio à escolha; linha (da tabela) | decision-support table; row |
| evidência favorável, contrária, dividida, indireta, insuficiente | favourable, contrary, mixed, indirect, insufficient evidence |
| agrupamento; ressalvas; força | grouping; caveats; strength |
| exame nos cenários; justificativa nas fontes; orientação concreta | examination in the scenarios; grounding in the sources; concrete guidance |
| ameaças à validade; banca | threats to validity; examining committee |
| QP1, QP2, QP3; IA-A, IA-B | RQ1, RQ2, RQ3; AI-A, AI-B |
| p.p. | percentage points |

## Compilação e conferência

```sh
make check          # inclui a guarda da tradução
make pdf            # build/main.pdf, português
make pdf-en         # build/main-en.pdf, inglês
make pdf-monografia # build/monografia.pdf, sem mudança de conteúdo
```

Conferência local em 24/11/2026 com TeX Live 2026 (LuaHBTeX) e latexmk; são necessários os pacotes
`orcidlink`, `fontawesome`, `underscore` e as fontes TeX Gyre Termes e Roboto, todos do TeX Live.

- Sem citação nem remissão indefinida nas duas versões.
- Avisos que vêm da classe e aparecem também no modelo da revista: duas caixas 66 pt mais largas no
  bloco de título (o fio horizontal dentro de um parágrafo com recuo à direita) e o aviso de
  `\headheight` do `fancyhdr` na primeira página.
- Páginas inspecionadas em imagem (Ghostscript, 110 dpi): primeira página, tabelas de coluna, as duas
  partes da tabela de apoio, figura do sistema, declarações, referências e início dos apêndices.
- O parágrafo de abertura do Apêndice B saía alinhado à esquerda e com entrelinha reduzida, porque o
  arquivo gerado abria o grupo `\scriptsize\raggedright` sem linha em branco antes. Corrigido no
  gerador a pedido do autor (D144), também na monografia: ela continua com 81 páginas, e o parágrafo
  passou de seis para cinco linhas, o que desloca os itens da lista em uma linha.
- A figura do sistema mostra a interface em português também na versão em inglês.

## Pendências antes de uma submissão

1. ORCID e e-mail institucional de Caio César de Freitas; e-mail de Pedro Saint Clair Garcia.
2. Confirmação, pelos autores, dos ORCID e do e-mail obtidos em fontes públicas e do autor correspondente.
3. Declaração de conflitos de interesse e de financiamento, se houver.
4. Confirmação das contribuições e da leitura da versão final pelos três autores.
5. Revisão humana da tradução e aprovação do título em inglês.
6. Depósito dos artefatos com identificador persistente e licença.
7. Avaliação, com o orientador, do enquadramento da revisão rápida no escopo da revista.
