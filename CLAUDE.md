# Claude Code neste repositório

@AGENTS.md

## Ambiente
- Skills do projeto: `.claude/skills` é um link para `.agents/skills/`; editar somente em `.agents/skills/`.
- Antes de cada tarefa, partir de `main` atualizada (`git pull --ff-only`) e criar a branch da issue.
- Issues e PRs: `gh` autenticado em `caiofreitas1`; repositório privado `caiofreitas1/tcc2-prompt-engineering`.
- Verificações: `make check`; para LaTeX, `make pdf` e inspecionar `build/main.pdf`.

## Sessões na nuvem (app do Claude no celular)
- Rodam a partir do GitHub, sem os arquivos ignorados pelo Git. O hook de
  `.claude/settings.json` baixa S1 com `scripts/obter_s1.py` ao iniciar; sem ele,
  `make check` falha por fonte ausente.
- O ambiente precisa de acesso de rede a arxiv.org, export.arxiv.org,
  api.openalex.org, api.crossref.org, dl.acm.org e ieeexplore.ieee.org
  (configurado pelo autor no ambiente em claude.ai). Sem isso, registrar o bloqueio.
- `make pdf` depende de TeX Live; se não houver, relatar que o PDF não foi compilado
  e deixar a compilação para uma sessão no Mac.
- PDFs e textos baixados na nuvem não persistem entre sessões; o que precisa ficar
  vai para o Git (dados e evidências), nunca os PDFs.
