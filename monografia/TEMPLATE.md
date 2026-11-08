# IEEE Conference Template — adoção em T03

## Escolha e origem

O autor escolheu o **IEEE Conference Template** neste chat em **27/10/2026**.
Essa é a origem da escolha de formato; não é registro de aprovação pelo curso ou
pelo orientador. O orientador revisará ao final, conforme fluxo já definido em T01.

Fontes consultadas em 27/10/2026:

- [IEEE Author Center: Authoring Tools and Templates](https://conferences.ieeeauthorcenter.ieee.org/write-your-paper/authoring-tools-and-templates/).
- [Página IEEE de templates para conferências](https://cai.ieee.org/2025/manuscript-templates-for-conference-proceedings/), que orienta o uso do modo `conference` e remete à documentação no CTAN.
- [Distribuição IEEEtran no CTAN](https://ctan.org/pkg/ieeetran).
- [Esqueleto de conferência bare_conf.tex](https://mirrors.ctan.org/macros/latex/contrib/IEEEtran/bare_conf.tex), **V1.4b, 2015/08/26**, por Michael Shell, lido para orientar a adaptação.

A obtenção do ZIP no domínio central do IEEE retornou conteúdo que não era um ZIP
válido nesta sessão; não se afirma incorporação desse arquivo nem de sua edição
mais recente. A implementação usa a distribuição IEEEtran do TeX Live e o modo de
conferência documentado no esqueleto do CTAN.

| Componente conferido | Versão / identificação | SHA-256 na conferência |
|---|---|---|
| `bare_conf.tex`, obtido do CTAN | V1.4b, 2015/08/26 | `cc4fa258aa90115ad6afbd8ca5555f448880b29a971398bf1a20ee5f240b45f7` |
| `IEEEtran.cls`, resolvido pelo TeX Live | V1.8b, 2015/08/26 | `da751920a317ed318b7b5cd7fa585a6cc7d28502d457856382e9be24b10a3bd7` |
| `IEEEtran.bst`, disponível no TeX Live | Estilo bibliográfico IEEEtran | `314f0ece704568faf827011bac498650691b2b5ee06320720830e782416d5a5f` |

A classe não foi modificada ou copiada para o repositório. Sua distribuição é sob
LPPL 1.3, conforme o CTAN; instalar o pacote `ieeetran` da distribuição TeX para
reproduzir a compilação. Os hashes identificam os componentes conferidos, sem
substituir os requisitos ou a identificação de versão da distribuição usada.

## Adaptação do documento

- `main.tex` usa `\documentclass[conference,a4paper]{IEEEtran}`: corpo de 10 pontos,
  duas colunas e dimensões controladas pela classe. A4 preserva o tamanho que já
  estava configurado no projeto; não foi atribuído a uma exigência do curso.
- O título e a autoria usam os comandos da classe. Nome, curso, universidade e
  cidade vieram dos materiais do projeto. Até 08/11/2026, o orientador ficava em
  nota de orientação por `\thanks`; por decisão do autor nessa data (D88), passou a
  figurar como coautor, em um segundo bloco `\IEEEauthorblockN`. E-mail e ORCID não
  foram adicionados.
- O texto continua em português brasileiro. Resumo e palavras-chave usam os
  ambientes da classe, com rótulos em português; o resumo permanece pendente.
- Os seis arquivos de `capitulos/` continuam separados e entram por `\input`;
  constituem seções do artigo. Foram ajustadas apenas instruções desatualizadas
  sobre T01/aval do orientador e a referência a capítulos na organização do texto.
- A capa, o sumário e os cabeçalhos personalizados do esqueleto anterior foram
  retirados da composição do artigo. Margens e espaçamento não são redefinidos
  por `geometry`, `setspace` ou `fancyhdr`.
- Citações serão numéricas, com `cite` e estilo `IEEEtran`. A bibliografia continua
  comentada até haver fontes efetivamente citadas no texto; nada foi removido do
  `.bib` e não se usou `\nocite{*}` para simular uma lista de referências.
- Pendências de redação continuam visíveis em vermelho. O PDF é demonstração do
  formato, não artigo concluído nem submissão a um evento IEEE.

## Compilação e conferência

Na raiz do projeto:

```sh
python3 scripts/obter_s1.py  # apenas se a fonte local de S1 ainda não existir
make check
make pdf
```

`make pdf` usa `latexmk` e `pdflatex`. Conferência local com TeX Live 2026,
pdfTeX 1.40.29 e latexmk 4.88; são necessários IEEEtran, os recursos de português
do Babel e os pacotes listados em `main.tex`. O resultado está em `build/main.pdf`,
fora do Git. Não é preciso alterar o Makefile para compilar esta adaptação.

A inspeção abrange título/autoria, acentos, duas colunas, resumo/palavras-chave,
hierarquia das seis seções, ausência de cortes e sobreposições, e ausência de
cabeçalhos e números de página adicionais. O equilíbrio das colunas da última
página deverá ser revisto quando houver texto final. Ainda não há tabelas,
figuras ou citações na redação para testar esses elementos com dados reais.

## Orientador confirmado em 27/10/2026

O autor informou neste chat que seu orientador é o docente do
[perfil Eduardo Figueiredo no DCC/UFMG](https://dcc.ufmg.br/professor/eduardo-figueiredo/).
A relação de orientação tem origem na declaração do autor. A página institucional,
consultada em 27/10/2026, identifica **Eduardo Magno Lages Figueiredo** nos registros
curriculares/projetos, a formação de doutorado e o vínculo com o DCC/UFMG. No PDF,
ele consta como **Orientador: Prof. Dr. Eduardo Magno Lages Figueiredo**, do
Departamento de Ciência da Computação da UFMG, em nota no rodapé da primeira página.
Não houve contato com o docente ou confirmação de revisão/aprovação do trabalho.

## Elementos da entrega confirmados pelo autor

Em 27/10/2026, à pergunta sobre capa, folha de aprovação ou outros elementos,
o autor respondeu **«Somente o artigo IEEE»**. Assim, não haverá capa ou folha de
aprovação separadas nesta entrega. Essa confirmação, somada à escolha do formato
e à identificação do orientador, atende à parte informacional do primeiro critério
de T03. A origem é a declaração do autor sobre sua entrega, sem alegar homologação
independente por uma instância do curso ou aprovação do orientador.

O campo `template_institucional_confirmado` em `projeto.json` foi atualizado para
verdadeiro com essa origem. A implementação mantém o artigo IEEE em A4 e português,
os dados de autoria conhecidos e a nota de orientação. T03 fica pronta para revisão
e integração do PR; a redação e a revisão acadêmica final continuam por realizar.

## Resultado da primeira verificação de 27/10/2026

- `make check`: zero erros estruturais e dez testes aprovados.
- `make pdf`: compilação concluída; `build/main.pdf` com uma página A4.
- Log final sem avisos, caixas overfull/underfull, caracteres faltantes ou
  referências/citações indefinidas. Não há citações ativas nesta estrutura.
- Quatro fontes Type 1 incorporadas, verificadas pela estrutura do PDF com pypdf;
  título e autor presentes nos metadados. Página inteira renderizada por Poppler e
  inspecionada após a compilação final, sem cortes ou sobreposições.
- `make release-check`: falha esperada com 17 bloqueios: afirmações em rascunho,
  flags de entrega, ausência de buscas/corpus/qualidade e redação pendente.
  Entre as flags está `protocolo_confirmado=false` em `projeto.json`, ainda não
  sincronizada com a confirmação do autor documentada em T01. Não é nova ausência
  de confirmação do protocolo; a flag foi preservada fora do escopo de T03.
- Não foram criadas tabelas, figuras ou referências fictícias para preencher a
  página. Não se declarou validação científica ou homologação institucional.

### Complemento após as confirmações do autor

Orientador e entrega apenas em artigo IEEE confirmados pelo autor em 27/10/2026.
A página com a nota de orientação foi recompilada e inspecionada visualmente;
continua com uma página A4, log sem avisos/overfull/underfull e autoria do aluno nos
metadados. O resultado de `make check` permanece zero erros e dez testes aprovados.
A primeira execução de `make release-check` acima precede a confirmação da flag
do template. Após atualizar essa flag, `make release-check` falha com 16 bloqueios
acadêmicos e de entrega, sem tratar o template como pendente. A flag antiga do
protocolo continua fora do escopo; a confirmação do autor permanece registrada
em T01.
