# Síntese descritiva (tabelas geradas por `scripts/sintetizar.py`)

Fichas: 334; comparações ex-v2.2: 807. Extração por IA; conferência humana em andamento (D109, D110).

## Corpus

Ano (registro): 2021: 1; 2022: 1; 2023: 31; 2024: 88; 2025: 138; 2026: 75.

Tarefas (multirrótulo): geracao: 249; depuracao: 62; traducao: 27; refatoracao: 20; estudos com mais de uma tarefa: 22.

Famílias de modelos (estudos): GPT-4 / GPT-4o / GPT-4.x: 187; GPT-3.5 / ChatGPT: 137; DeepSeek: 128; Llama: 92; Qwen: 91; Code Llama: 81; Gemini / PaLM / Bard: 74; Claude: 60; Mistral / Mixtral / Codestral: 44; StarCoder / SantaCoder: 38; CodeGen / CodeT5: 32; Codex / davinci: 26.

Benchmarks (estudos): HumanEval (e variantes): 83; MBPP (e variantes): 50; APPS: 16; CodeNet / Avatar / transcoder: 14; Defects4J: 12; CoderEval: 12; LeetCode: 12; LiveCodeBench: 10; CodeContests: 10; BigCodeBench: 10; estudos sem nenhum desses: 189.

Linguagens (estudos): Python: 149; Java: 65; C++: 36; C: 20; JavaScript: 18; Go: 15; C#: 10; PHP: 10; nao_informado: 9; HTML: 8.

Sem comparador: 36; com técnica só classificada (sem número): 57; sem nenhuma comparação extraída: 17.

## Mecanismos (técnicas focais; estudos distintos)

| tarefa | estudos | instrucao | contexto | restricoes | exemplos | decomposicao | feedback | raciocinio | amostragem | multiagente | otimizacao_prompt | outro |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| geracao | 249 | 39 | 89 | 78 | 77 | 78 | 71 | 64 | 24 | 29 | 14 | 21 |
| depuracao | 62 | 11 | 35 | 16 | 25 | 18 | 19 | 18 | 8 | 6 | 2 | 4 |
| traducao | 27 | 2 | 4 | 7 | 8 | 9 | 8 | 5 | 3 | 3 | 2 | 2 |
| refatoracao | 20 | 2 | 5 | 3 | 8 | 6 | 5 | 4 | 2 | 2 | 1 | 0 |

(mecanismos acrescentados pela técnica focal ao prompt base; a tabela 06 traz o pacote completo)

## Contrafactual das técnicas focais (técnicas, não estudos)

Total: pacote: 373; ingrediente: 212; contraste_pareado: 3; cumulativo: 13; nenhum: 112.

Componentes (ingredientes registrados das técnicas focais): pacote: 15; ingrediente: 328; contraste_pareado: 9; cumulativo: 30; nenhum: 328.

Estudos (técnica focal ou componente; um estudo pode ter vários tipos): geracao: 249 estudos, pacote 155, ingrediente ou pareado 141, cumulativo 19, só nenhum 43; depuracao: 62 estudos, pacote 47, ingrediente ou pareado 39, cumulativo 13, só nenhum 3; traducao: 27 estudos, pacote 19, ingrediente ou pareado 13, cumulativo 6, só nenhum 3; refatoracao: 20 estudos, pacote 12, ingrediente ou pareado 9, cumulativo 1, só nenhum 5; todas: 334 estudos, pacote 219, ingrediente ou pareado 191, cumulativo 33, só nenhum 51.

## Comparações extraídas (unidade: comparação)

Total: melhora: 514; igual: 28; piora: 145; sem_direcao: 95; descritiva: 25. «sem_direcao»: sem sentido definido ou sem dois números; «descritiva»: sem comparador.

Seleção: desempate_ordem: 272; cobertura: 490; principal_declarado: 45. Derivação: direta: 803; contraste_pareado: 4.

Só comparações principais declaradas: geracao: 24 melhora, 0 igual, 0 piora; depuracao: 7 melhora, 0 igual, 0 piora; traducao: 4 melhora, 0 igual, 0 piora; refatoracao: 4 melhora, 0 igual, 0 piora.

Os autores escolhem a comparação principal, e estudos com resultado favorável tendem a ser publicados; a proporção de melhoras não estima efeito.

## Qualidade (estudos; julgamento por IA)

| critério | atende | parcial | nao_atende | nao_informado |
|---|---|---|---|---|
| objetivo | 329 | 5 | 0 | 0 |
| procedimento | 20 | 314 | 0 | 0 |
| comparador | 105 | 208 | 21 | 0 |
| metricas | 5 | 325 | 4 | 0 |
| ameacas | 85 | 218 | 0 | 31 |
| reprodutibilidade | 5 | 326 | 3 | 0 |
| contaminacao | 17 | 126 | 2 | 189 |

## Riscos e mitigações (estudos distintos)

| tarefa | estudos | correcao_funcional | seguranca | alucinacao | contaminacao | nao_determinismo | custo | manutenibilidade | outro | com mitigação | mitigação avaliada |
|---|---|---|---|---|---|---|---|---|---|---|---|
| geracao | 249 | 234 | 73 | 71 | 96 | 90 | 121 | 30 | 204 | 246 | 114 |
| depuracao | 62 | 58 | 15 | 20 | 31 | 26 | 31 | 6 | 54 | 61 | 25 |
| traducao | 27 | 27 | 6 | 6 | 13 | 13 | 11 | 3 | 22 | 27 | 12 |
| refatoracao | 20 | 18 | 6 | 9 | 6 | 10 | 6 | 8 | 16 | 20 | 7 |
| todas | 334 | 316 | 91 | 99 | 138 | 127 | 158 | 41 | 277 | 330 | 146 |

## Outros

Estudos com componente fora do escopo de prompting: 305 (outro: 470; decodificacao: 218; selecao_modelo: 182; ajuste_fino: 119; orcamento: 86; embeddings_aprendidos: 8).

Estudos com registro de heterogeneidade (busca dirigida): 334; registros: 3546.
