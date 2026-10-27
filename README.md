# TCC II — Engenharia de Prompt para Codificação e Implementação

Ambiente de trabalho de Caio César de Freitas, Engenharia de Sistemas/UFMG.
Estrutura inicial preparada em 25/10/2026. A revisão completa não está declarada concluída.

Repositório privado: [caiofreitas1/tcc2-prompt-engineering](https://github.com/caiofreitas1/tcc2-prompt-engineering).
As [12 issues](https://github.com/caiofreitas1/tcc2-prompt-engineering/issues) já estão abertas.
Consultar [o índice de tarefas e dependências](tarefas/indice-github.md).

## Começar
1. Ler contexto/estado-atual.md e confirmar o que avançou após o ponto de controle.
2. Em checkout sem as fontes locais, executar `python3 scripts/obter_s1.py` para
   recuperar S1 e conferir seu hash. Depois executar `make check` (Python 3.10+;
   sem bibliotecas Python externas). PDFs permanecem fora do Git.
3. Iniciar pela [issue #1 (T01)](https://github.com/caiofreitas1/tcc2-prompt-engineering/issues/1).
   Os IDs Txx permanecem estáveis no backlog; o índice relaciona-os aos números das issues.
4. Executar T02 e conferir S1 no artigo original antes de usar o fluxo em escala.
5. Para cada seção: evidências → esboço → redação → auditoria → revisão do autor.

## Organização
| Pasta | Uso |
|---|---|
| protocolo/ | Plano da revisão, critérios e mudanças |
| dados/ | Registros em CSV e extrações JSONL |
| evidencias/ | Fichamentos, sínteses e auditorias |
| fontes/legado/ | Cópias imutáveis dos documentos recebidos |
| fontes/artigos/ | Textos primários; pasta ignorada pelo Git por padrão |
| monografia/ | Estrutura LaTeX de trabalho, dividida por seção |
| tarefas/ | Backlog, dependências e critérios de aceitação |
| .agents/skills/ | Seis skills versionadas para agentes neste projeto |
| scripts/ | Verificações e publicação pelo GitHub CLI |

## Usar com um agente
Abrir a raiz do projeto e pedir: “Leia AGENTS.md. Execute a tarefa T02 de
tarefas/backlog.json usando $tcc-extrair-evidencias. Entregue os arquivos, indique
o que foi conferido no original e execute make check.” A tarefa T02 depende de T01.
As seis skills estão versionadas neste repositório em .agents/skills/. A tentativa de
instalação na página pessoal de Skills falhou; detalhes em contexto/entrega.md.
Usar as skills do repositório ao trabalhar neste projeto.
O GitHub organiza as tarefas; criar issues não inicia agentes automaticamente.

## Comandos
- `python3 scripts/obter_s1.py`: obter a cópia arXiv v5 usada em T02 e conferir o
  SHA-256, sem sobrescrever arquivo divergente. Requer rede; ver evidencias/S1.md.
- `make check`: integridade dos registros e testes das barreiras científicas.
- `make pdf`: compilar o esqueleto em build/main.pdf (requer latexmk e TeX Live).
- `make release-check`: verificar pré-condições mínimas da versão para entrega.
  Deve falhar nesta estrutura inicial, pois há etapas e revisão humana pendentes.
- `git clone https://github.com/caiofreitas1/tcc2-prompt-engineering.git`: obter a cópia
  atual do projeto, usando uma conta com acesso ao repositório privado.

O repositório e as issues já foram publicados. scripts/publicar_github.py foi preservado
como utilitário da preparação inicial; não é necessário executá-lo para começar.

## Documento e pendências
monografia/main.tex é um esqueleto técnico compilável; não é um template institucional
homologado nem uma monografia pronta. Incorporar o template oficial em T03 antes da
normalização final. Os textos anteriores foram preservados sem reescrita; os números
do piloto continuam sujeitos à conferência no artigo original. As referências acadêmicas
de S1 foram conferidas na versão arXiv v5 e cadastradas no .bib em T02, com revisão
humana pendente; S2–S6 continuam com metadados herdados. Ver evidencias/S1.md.

## Datas registradas nos materiais
Marcação da defesa: 25/10; texto inicial: 08/11; defesas: 16–19/11;
texto final: 29/11/2026. Não são confirmações de entrega ou de agendamento.
Confirmar imediatamente a situação da marcação da defesa com o orientador.

## Privacidade e compartilhamento
Manter privado durante o desenvolvimento. Não incluir tokens, credenciais ou material
de trabalho do Banco Inter. Os documentos acadêmicos contêm identificação do autor.
Não redistribuir PDFs de editoras sem verificar as condições aplicáveis.
