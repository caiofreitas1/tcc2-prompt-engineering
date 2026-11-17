# Parecer de elegibilidade: S1721, S1929, S1886 e S433/S2053 (17/11/2026)

Preparado por Claude Code (Claude Opus 5.5) a pedido do autor, com leitura do texto
extraído completo de cada estudo e das imagens das páginas com tabelas e figuras
(`fontes/artigos/paginas/<ID>/`). É recomendação de IA; a decisão é do autor. Critérios
do protocolo (seção 3) e regras de D59 e D90 para X4 no texto completo.

## S1721 — recomendação: excluir por X4

Iliev et al., *Bias Detection and Mitigation in LLMs for Code Generation* (IEEE IoT
Journal, 2026).

- **Intervenção avaliada.** Três partes: análise contextual do código (CCA), prompts
  contrafactuais (CPE) e RLHF. Só o RLHF, e as variantes com LoRA e SFT, têm resultado
  quantitativo: escore de viés de 0,68 para 0,35 (seção IV.C, p. 6) e Tabela II (p. 7),
  que mede baseline, RLHF completo (sem memória), LoRA + RLHF e destilação + SFT. Todas
  são ajuste fino do Llama-3.2-3B-Instruct (seção III.D).
- **Papel do prompting.** Os prompts contrafactuais trocam nome, gênero ou deficiência da
  pessoa no enunciado («John» por «Aisha», seção III.B). Servem de sonda para medir viés;
  não são uma estratégia para gerar código. Os achados sobre esses pares (seções IV.A e
  IV.B) são qualitativos, e a Tabela I traz escores de viés de 4 prompts isolados, sem a
  comparação entre os pares.
- **Pela regra de D90**, o resultado obtido por prompting só serve para mostrar o viés
  que o ajuste fino corrige; não há análise de uma técnica de prompting.
- **Qualidade (não é critério de exclusão, mas pesa):** várias referências não têm
  relação com o tema (por exemplo, [3] sobre operadores de Toeplitz, citado como fonte
  sobre viés em código; [9] sobre áxions); o texto diz que não houve teste estatístico e,
  logo depois, relata teste t pareado com p < 0,01; o baseline da Tabela II (0,45)
  difere do da prosa (0,68); o RLHF completo falhou por memória (Tabela II), mas o resumo
  atribui a ele a redução de 49%.
- **Alternativa:** manter por analogia com S1617 (efeito de um atributo do prompt sobre o
  código). A analogia é fraca: em S1617 o idioma do prompt é a variável estudada, com
  Pass@1 por condição; em S1721 a variação demográfica não tem medida comparável.
- **Efeito:** S1721 sai do corpus e da amostra de conferência (entrou no complemento de
  D114); a amostra passa a 66 estudos sorteados, e o tamanho exigido continua 67 se o
  corpus ficar em 331–334. Um estudo novo seria sorteado do mesmo quadro para repor.

## S1929 — recomendação: manter

Algorithmic Inversion (ICPC 2025).

- A técnica principal treina embeddings de algoritmo sobre o modelo congelado (seção
  III.B), da família do prompt tuning, e fica fora do escopo.
- O estudo, porém, analisa o self-planning como achado próprio (seção V.A, p. 7): o SP
  «provides minimal assistance» no CodeContests, chega a piorar, e os autores explicam a
  queda no StarCoder2-15B pelo desvio do padrão problema→código do pré-treino. A Tabela II
  traz SP e Vanilla para quatro modelos em dois conjuntos.
- **Pela regra de D90**, isso basta para incluir: há análise própria de um resultado de
  código obtido por prompting em modelo sem ajuste fino. O caso difere de S314 e S373,
  excluídos porque o prompting aparecia só como linha de base, sem análise.
- **Limite:** a única comparação extraída (SP contra Vanilla, Pass@1 de 0,1 para 0 no
  CodeContests com DeepSeek-Coder-1.3B) é de linha de base; a ficha está correta em deixar
  a técnica focal fora do escopo.
- **Alternativa:** excluir por X4, se o autor entender que dois parágrafos de comentário
  não fazem do SP um objeto do estudo. É um caso de fronteira.

## S1886 — recomendação: manter, decidindo junto com S261, S320 e S398

Comparação de GPT-4.1 e Claude 3.7 Sonnet no GitHub Copilot (modo agente), ICoABCD 2025.

- A variável independente é o modelo; o prompt inicial é idêntico nas duas condições
  (seção III.A e III.C). Mede número de prompts e duração por tarefa em 12 funcionalidades
  de uma API Laravel.
- Atende I2 na letra (aplica prompting de modelo pré-treinado à geração de código) e, pela
  regra de D90, analisa como achado próprio o código obtido por prompting em modelos sem
  ajuste fino. Não avalia técnica de prompting, por isso não tem comparação para a QP1.
- **Precedentes:** S261, S320 e S398 também comparam modelos numa única condição de
  prompt, foram apontados na extração para avaliação do autor e continuam no corpus sem
  decisão explícita. A coerência pede decidir os quatro juntos.
- **Recomendação:** manter os quatro, como estudos sem comparação de técnicas (o texto já
  os conta entre os 17 estudos sem comparação numérica), úteis para a QP2 e a
  caracterização. **Alternativa:** excluir os quatro por X4 (D59: a intervenção avaliada é
  a escolha do modelo, não o prompting).

## S433 e S2053 — recomendação: X1, mantendo S2053

- **Mesmo trabalho.** Mesmos cinco autores (Taherkhani, Sepidband, Pham, Wang e Hemmati,
  York University), mesmo título (só «Algorithm» e «Algorithms»), mesma técnica (EPiC) e
  resumo quase idêntico.
- **Diferenças.** S2053 (ACM, `doi:10.1145/3805704`, 25 páginas) é a versão publicada e
  ampliada: acrescenta a linha de base Self-Collaboration e revisa os números do resumo
  (até 5% em pass@k e de 1,2 a 10 vezes mais barato, contra 6% e 2 a 10 vezes em S433,
  arXiv, 18 páginas). As duas fichas extraíram as mesmas duas comparações, com números
  quase iguais (EPiC contra zero-shot no HumanEval+ com o3-mini: 0,945 em S433-C1 e 0,941
  em S2053-C1).
- **Recomendação.** X1 para S433, agrupado a S2053, que fica como registro principal por
  ser a versão de registro, revisada por pares e com números finais. Pelo protocolo, X1
  agrupa e não descarta o registro.
- **Diferença em relação a S1749.** Em D78, o autor excluiu a versão ACM (S1749) e manteve
  o arXiv (S328), sem fixar regra. Se preferir a mesma direção, a alternativa é manter
  S433 e aplicar X1 a S2053; a vantagem prática é que a tabela de apoio congelada cita S433.
- **Efeito.** O corpus perde um estudo; a afirmação A89 deixa de citar dois estudos para o
  mesmo resultado; a linha da tabela de apoio que cita S433 recebe nota, sem mudar a tabela.
