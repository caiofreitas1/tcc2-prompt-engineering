# Síntese descritiva (tabelas geradas por `scripts/sintetizar.py`)

Fichas: 304; comparações ex-v2.2: 756. Extração por IA; conferência humana em andamento (D109, D110).

## Corpus

Ano (registro): 2021: 1; 2022: 1; 2023: 30; 2024: 86; 2025: 117; 2026: 69.

Tarefas (multirrótulo): geracao: 224; depuracao: 59; traducao: 25; refatoracao: 19; estudos com mais de uma tarefa: 21.

Famílias de modelos (estudos): GPT-4 / GPT-4o / GPT-4.x: 172; GPT-3.5 / ChatGPT: 126; DeepSeek: 112; Llama: 83; Qwen: 82; Code Llama: 72; Gemini / PaLM / Bard: 64; Claude: 52; Mistral / Mixtral / Codestral: 41; StarCoder / SantaCoder: 33; CodeGen / CodeT5: 29; Codex / davinci: 26.

Benchmarks (estudos): HumanEval (e variantes): 76; MBPP (e variantes): 48; APPS: 13; CoderEval: 12; CodeNet / Avatar / transcoder: 12; Defects4J: 11; LeetCode: 11; LiveCodeBench: 10; CodeContests: 10; BigCodeBench: 9; estudos sem nenhum desses: 171.

Linguagens (estudos): Python: 133; Java: 61; C++: 33; C: 17; JavaScript: 16; Go: 14; C#: 10; nao_informado: 8; Rust: 7; PHP: 7.

Sem comparador: 29; com técnica só classificada (sem número): 53; sem nenhuma comparação extraída: 15.

## Mecanismos (técnicas focais; estudos distintos)

| tarefa | estudos | instrucao | contexto | restricoes | exemplos | decomposicao | feedback | raciocinio | amostragem | multiagente | otimizacao_prompt | outro |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| geracao | 224 | 36 | 80 | 68 | 72 | 71 | 66 | 59 | 22 | 26 | 13 | 20 |
| depuracao | 59 | 11 | 34 | 16 | 24 | 18 | 19 | 18 | 8 | 6 | 2 | 4 |
| traducao | 25 | 1 | 4 | 6 | 8 | 9 | 7 | 4 | 2 | 3 | 2 | 2 |
| refatoracao | 19 | 2 | 5 | 3 | 8 | 6 | 5 | 4 | 1 | 1 | 0 | 0 |

(mecanismos acrescentados pela técnica focal ao prompt base; a tabela 06 traz o pacote completo)

## Contrafactual das técnicas focais (técnicas, não estudos)

Total: pacote: 349; ingrediente: 205; contraste_pareado: 3; cumulativo: 13; nenhum: 101.

Componentes (ingredientes registrados das técnicas focais): pacote: 14; ingrediente: 310; contraste_pareado: 9; cumulativo: 28; nenhum: 306.

Estudos (técnica focal ou componente; um estudo pode ter vários tipos): geracao: 224 estudos, pacote 142, ingrediente ou pareado 133, cumulativo 17, só nenhum 39; depuracao: 59 estudos, pacote 46, ingrediente ou pareado 38, cumulativo 12, só nenhum 2; traducao: 25 estudos, pacote 17, ingrediente ou pareado 12, cumulativo 6, só nenhum 3; refatoracao: 19 estudos, pacote 12, ingrediente ou pareado 9, cumulativo 1, só nenhum 4; todas: 304 estudos, pacote 203, ingrediente ou pareado 181, cumulativo 31, só nenhum 45.

## Comparações extraídas (unidade: comparação)

Total: melhora: 479; igual: 26; piora: 138; sem_direcao: 94; descritiva: 19. «sem_direcao»: sem sentido definido ou sem dois números; «descritiva»: sem comparador.

Seleção: desempate_ordem: 247; cobertura: 467; principal_declarado: 42. Derivação: direta: 752; contraste_pareado: 4.

Só comparações principais declaradas: geracao: 23 melhora, 0 igual, 0 piora; depuracao: 7 melhora, 0 igual, 0 piora; traducao: 4 melhora, 0 igual, 0 piora; refatoracao: 4 melhora, 0 igual, 0 piora.

Os autores escolhem a comparação principal, e estudos com resultado favorável tendem a ser publicados; a proporção de melhoras não estima efeito.

## Qualidade (estudos; julgamento por IA)

| critério | atende | parcial | nao_atende | nao_informado |
|---|---|---|---|---|
| objetivo | 300 | 4 | 0 | 0 |
| procedimento | 19 | 285 | 0 | 0 |
| comparador | 99 | 188 | 17 | 0 |
| metricas | 5 | 297 | 2 | 0 |
| ameacas | 79 | 197 | 0 | 28 |
| reprodutibilidade | 5 | 297 | 2 | 0 |
| contaminacao | 15 | 120 | 2 | 167 |

## Riscos e mitigações (estudos distintos)

| tarefa | estudos | correcao_funcional | seguranca | alucinacao | contaminacao | nao_determinismo | custo | manutenibilidade | outro | com mitigação | mitigação avaliada |
|---|---|---|---|---|---|---|---|---|---|---|---|
| geracao | 224 | 212 | 63 | 63 | 91 | 80 | 110 | 29 | 182 | 221 | 104 |
| depuracao | 59 | 56 | 14 | 20 | 30 | 24 | 30 | 6 | 51 | 58 | 24 |
| traducao | 25 | 25 | 5 | 5 | 11 | 11 | 10 | 2 | 20 | 25 | 11 |
| refatoracao | 19 | 17 | 6 | 9 | 6 | 10 | 6 | 8 | 15 | 19 | 7 |
| todas | 304 | 290 | 80 | 90 | 130 | 113 | 145 | 39 | 250 | 300 | 134 |

## Outros

Estudos com componente fora do escopo de prompting: 276 (outro: 433; decodificacao: 202; selecao_modelo: 168; ajuste_fino: 108; orcamento: 80; embeddings_aprendidos: 6).

Estudos com registro de heterogeneidade (busca dirigida): 304; registros: 3238.
