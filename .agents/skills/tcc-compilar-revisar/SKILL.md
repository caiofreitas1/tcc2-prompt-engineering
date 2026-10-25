---
name: tcc-compilar-revisar
description: "Compilar o LaTeX do TCC e revisar visualmente PDF, tabelas, referências e paginação. Usar após alterações de documento; não certificar conteúdo científico nem tratar o esqueleto como template oficial."
---

# tcc-compilar-revisar

Ler AGENTS.md, README.md e Makefile na raiz do projeto ativo.
Verificar se o template institucional está identificado e registrar quando estiver pendente.
Executar make check e make pdf; se faltar dependência, relatar a dependência precisa.
Não remover citações ou texto para esconder erros de compilação. Inspecionar o log
por referências indefinidas, citações ausentes, overfull e erros de fonte.
Renderizar as páginas alteradas com pdftoppm ou equivalente e abrir as imagens para
conferir cortes, sobreposições, tabelas, legendas, sumário, numeração e quebras.
Recompilar e reinspecionar após correções visuais. Se não puder abrir as imagens,
relatar que a revisão visual não ocorreu. Compilação não comprova validade científica.
Antes da entrega final, executar make release-check e ler pendências conhecidas.
Entregar caminho do PDF, comandos, páginas inspecionadas e problemas remanescentes;
não afirmar normalização institucional sem template e conferência correspondentes.
