# Conferência humana das fichas ex-v2.2 (protocolo, seção 7; D109)

Preparada por Claude Code (Claude Opus 5.5) em 17/11/2026. A conferência é do autor e
ainda não começou; nada aqui é revisão humana.

## Amostra (`amostra.csv`)

- Tamanho: `max(10, teto(0,20 × N))`, com N = 304 estudos do corpus definitivo: 61 estudos.
- Quadro: as 292 fichas finais em `evidencias/extracao-v2.2/`. As 10 fichas do piloto ficam
  fora do quadro; pelo protocolo, só contam se o autor as conferir na versão final, e isso
  ficaria além dos 61. S1610 e S667 não têm ficha.
- Obrigatórios: S1608 (texto extraído ilegível, leitura pelas imagens) e S1743 (tabelas
  ilegíveis nas imagens, valores só do texto).
- Demais 59: amostra sistemática com início aleatório (semente 20261117) sobre o quadro
  ordenado por extrator, por haver correção manual vigente, por tarefas e por chave
  aleatória. Isso dá estratificação implícita, proporcional e sem cotas fixas.
- Distribuição (população × amostra):
  - Extrator: Claude Opus 5.5, 266 × 55; Codex, 26 × 6.
  - Fichas com correção manual vigente: 58 × 11.
  - Tarefas: geração, 198 × 41; depuração, 39 × 8; tradução, 20 × 5;
    depuração+geração, 15 × 3; refatoração, 14 × 2; geração+tradução, 2 × 1;
    geração+refatoração, 1 × 1; as combinações com 1 ou 2 estudos restantes ficaram fora.
- Mecanismos das técnicas focais, em estudos (população × amostra):
  - instrução, 275 × 58; contexto, 206 × 43; restrições, 197 × 41; exemplos, 159 × 36;
  - decomposição, 129 × 24; feedback, 116 × 29; raciocínio, 99 × 23; amostragem, 46 × 10;
  - multiagente, 40 × 9; outro, 25 × 4; otimização de prompt, 17 × 1.
- Desvio: o protocolo manda priorizar os estudos que sustentam afirmações, mas a síntese
  ainda não existe. Por decisão do autor, a conferência vem antes dela. Na redação, cada
  afirmação continua conferida no original (T12), mesmo quando o estudo não estiver na amostra.
- Reproduzir: `python3 scripts/sortear_conferencia.py --gravar`.

## Formulário (`formulario.html`)

- Publicado como artifact privado: https://claude.ai/artifact/Q3fy3wYHt25KPCw9WVqGrt.
  Os julgamentos ficam na coleção `extracao_v22_autor` e são exportados para o repositório
  depois.
- Gerado por `python3 scripts/gerar_formulario_conferencia.py` a partir de `modelo.html`.
  Cada estudo leva:
  - o SHA-256 da ficha, gravado com o julgamento;
  - as correções manuais vigentes, num bloco próprio;
  - a marcação das citações.
- Volume: 61 fichas, 147 comparações numéricas e 1.810 citações.
- Marcação das citações no texto extraído: 441 contíguas, 791 intercaladas, 385 aproximadas
  (`scripts/verificar_citacoes_aprox.py`) e 193 não achadas, 37 delas na S1608. Não achada
  não quer dizer inexistente; a conferência é feita no PDF.
