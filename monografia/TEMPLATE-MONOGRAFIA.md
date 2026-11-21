# Formato de monografia (ABNT) — 18/11/2026

## Motivo

Em 18/11/2026 o autor relatou mensagem de uma professora da banca: o trabalho estava em
formato de artigo, e o curso de Engenharia de Sistemas exige monografia, com capa, resumo
e abstract, entre outros elementos. O autor pediu um novo documento em formato de
monografia, sem excluir o artigo (D127). `monografia/main.tex` (IEEE) continua no projeto.

## Fontes consultadas em 18/11/2026

| Documento | Onde | SHA-256 do PDF obtido |
|---|---|---|
| Regulamento Geral do Curso de Engenharia de Sistemas (arquivo datado de 2024.05.14) | https://www.ufmg.br/prograd/arquivos/cursos/projeto/RegEngenhariaDeSistemas.pdf | `ef71070250fad4946623346f681a07b470ca40535be599b3cf404910363ab343` |
| Diretrizes para normalização de trabalhos acadêmicos da UFMG, 3. ed., Biblioteca Universitária, 2025 | https://repositorio.ufmg.br/assets/public_html/diretrizes-para-normalizacao-de-trabalhos-academicos-da-UFMG.pdf | `53d09ac1dfcebb4d8f7b9b8b743f0fb48a1eba28d5bd136d90a3a68f90a79dff` |

O que o Regulamento diz, nos trechos lidos:

- Art. 14: o TCC «deve assumir o formato de uma monografia».
- Art. 19: no TCC I, a parte inicial da monografia segue «modelo fornecido pelo Colegiado».
- Art. 20: a documentação do TCC II contém os itens do Art. 13, «além de resumo e
  abstract, preferencialmente em um dos formatos padrão definidos pelo Colegiado».

**O modelo do Colegiado não foi localizado** na busca feita em 18/11/2026 nem está no
repositório. Por isso o documento segue as Diretrizes da UFMG, que se baseiam na ABNT
(NBR 14724). Não se afirma conformidade com o modelo do Colegiado. Se o autor obtiver o
modelo, o arquivo deve ser ajustado a ele.

## O que foi feito

`monografia/monografia.tex` usa a classe `abntex2` (v1.9.7, 2018/11/24, do TeX Live) e
`abntex2cite` em modo numérico. Compilar com `make pdf-monografia`; a saída é
`build/monografia.pdf`.

- **Texto:** os arquivos de `capitulos/` são os mesmos do artigo, sem alteração. No
  preâmbulo, cada `\section` do artigo vira capítulo e os demais níveis sobem um degrau.
  O resumo foi movido de `main.tex` para `capitulos/00-resumo.tex`, lido pelos dois
  documentos; o texto extraído do PDF do artigo ficou idêntico ao anterior.
- **Pré-textuais:** capa, folha de rosto, resumo, abstract, lista de tabelas, lista de
  abreviaturas e siglas e sumário.
- **Pós-textuais:** referências e, depois, os dois apêndices.
- **Logo na capa:** `figuras/logo-ufmg.png`, recortado em 18/11/2026 da capa de um TCC do
  mesmo curso que o autor trouxe como referência de formato (o arquivo de referência não
  está no repositório). É imagem de baixa resolução; pode ser trocada pelo arquivo oficial
  da UFMG. Esse TCC de referência não tem folha de aprovação e usa citações autor-data.
- **Sem dedicatória, agradecimentos e epígrafe:** elementos opcionais; o autor decidiu não
  incluir agradecimentos (18/11/2026).
- **Apresentação (Diretrizes, seção 2.2):** A4; margens de 3 cm (superior e esquerda) e
  2 cm (inferior e direita); Times, tamanho 12; espaçamento 1,5; recuo de parágrafo de
  1,25 cm; títulos em tamanho 12, os de seção primária em negrito e caixa alta; número
  da página no canto superior direito a partir da introdução, contado desde a folha de
  rosto.
- **Tabelas:** título acima e «Fonte: elaborado pelo autor» abaixo. As larguras de
  coluna foram pensadas para o artigo; o preâmbulo amplia cada tabela em 25% para manter
  a proporção com o corpo de 12 pt. As duas partes da tabela de apoio vão em paisagem.
- **Referências:** formato ABNT gerado por `abntex2cite`, em sistema numérico, na ordem de
  citação. O sistema numérico foi mantido porque o texto foi escrito com chamadas
  numéricas. As Diretrizes recomendam ordem alfabética, mas não fixam uma norma.

## Pendências e limites

- **Abstract:** tradução do resumo feita por Claude Code em 18/11/2026
  (`pretextual/abstract.tex`). Falta a revisão do autor.
- **Lista de siglas:** composta por Claude Code a partir das siglas usadas no texto
  (`pretextual/siglas.tex`). É elemento opcional; falta a revisão do autor.
- **Folha de aprovação:** retirada desta versão por decisão do autor em 18/11/2026, como
  no TCC de referência. As Diretrizes a listam como obrigatória (folha de aprovação ou
  ata de defesa); deve entrar na versão final, depois da defesa, com os nomes da banca.
- **Titulação e natureza:** «Prof. Dr.» vem de D23; a redação da natureza do trabalho
  («requisito parcial à obtenção do título de Bacharel em Engenharia de Sistemas») é a
  fórmula usual e não foi conferida com o Colegiado.
- **Ficha catalográfica:** não incluída. As Diretrizes a exigem para teses e
  dissertações; para monografias, remetem às normas do curso.
- **PDF/A:** as Diretrizes pedem PDF/A para o depósito no Repositório Institucional. O
  arquivo gerado é PDF comum.
- O texto dos capítulos chama de «Seção» também os capítulos, como no artigo.
- A compilação não comprova conformidade institucional nem validade científica.
