# Entrega da estrutura inicial — 25/10/2026

## Conteúdo preparado
- Instruções permanentes em AGENTS.md e protocolo derivado dos documentos existentes.
- Seis skills no projeto, com SKILL.md e metadados de interface validados.
- Doze tarefas, corpos de issues e dependências em tarefas/.
- Três documentos anteriores preservados e manifesto de integridade.
- Cadastro dos seis estudos piloto sem promoção a corpus definitivo ou evidência conferida.
- Contratos, formulários e verificações de integridade dos dados.
- Esqueleto LaTeX em seis arquivos de conteúdo; template institucional ainda pendente.
- Script de publicação privada com simulação por padrão e retomada das issues por título.

## Verificação realizada
- make check: zero erros estruturais e dez testes aprovados.
- Seis skills aprovadas pelo quick_validate.py do criador de skills.
- Dois testes de uso por agentes separados: extração de S1 e auditoria do relatório
  com os materiais locais. Ambos reconheceram a ausência das fontes primárias e
  não promoveram o histórico a evidência conferida. Esses testes não constituem
  revisão humana, validação das referências ou execução da RSL.
- Os cálculos históricos conferíveis internamente foram distinguidos do suporte empírico.
- make release-check: falha esperada com quatorze pendências, impedindo tratar a
  estrutura inicial como texto pronto para entrega.
- make pdf: compilação concluída; cinco páginas inspecionadas visualmente, sem cortes
  ou sobreposições. O PDF é somente uma demonstração do esqueleto.
- Script de publicação executado em modo de simulação: nenhum recurso remoto criado.

## Salvamento das skills
As seis skills foram criadas e commitadas no workspace pessoal de Skills, commit
ac6ff47. Duas tentativas de envio retornaram HTTP 422; a referência remota permaneceu
em 5ec289a. Portanto, não se afirma instalação/salvamento na página pessoal de Skills.
As cópias completas e validadas em .agents/skills/ pertencem ao projeto e podem ser
descobertas por um agente que abra sua raiz. Preservar as duas cópias ao atualizar.

## GitHub
A conta conectada foi identificada como caiofreitas1. A integração disponível permite
arquivos, commits e issues em repositórios existentes, mas não expõe criação de repositório.
O GitHub CLI não está instalado neste ambiente. Após autorização do autor, o repositório
caiofreitas1/tcc2-prompt-engineering foi criado no navegador com visibilidade privada,
e as doze issues foram abertas. O autor confirmou a autenticação e habilitou o projeto
na integração. Os arquivos foram preparados para publicação pela API Git do GitHub,
preservando o commit inicial criado pela interface. O índice está em tarefas/indice-github.md.

A publicação inclui as seis skills locais, os documentos de origem, o protocolo,
os contratos de dados, o esqueleto LaTeX, os scripts e os dez testes já aprovados.
Para começar, clonar o repositório privado e executar make check. A cópia distribuída
antes da publicação contém o estado anterior; usar o GitHub como referência atual.

## Primeiro trabalho acadêmico
Executar T01 para confirmar o estado atual e, em seguida, T02 para conferir S1 no
original. O presente preparo não executou buscas acadêmicas nem reescreveu a monografia.
