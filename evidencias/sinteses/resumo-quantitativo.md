# Síntese descritiva (tabelas geradas por `scripts/sintetizar.py`)

Fichas: 302; comparações ex-v2.2: 753. Extração por IA; conferência humana em andamento (D109, D110).

## Corpus

Ano (registro): 2021: 1; 2022: 1; 2023: 30; 2024: 86; 2025: 117; 2026: 67.

Tarefas (multirrótulo): geracao: 222; depuracao: 59; traducao: 25; refatoracao: 19; estudos com mais de uma tarefa: 21.

Famílias de modelos (estudos): GPT-4 / GPT-4o / GPT-4.x: 171; GPT-3.5 / ChatGPT: 126; DeepSeek: 110; Llama: 82; Qwen: 82; Code Llama: 72; Gemini / PaLM / Bard: 62; Claude: 52; Mistral / Mixtral / Codestral: 40; StarCoder / SantaCoder: 33; CodeGen / CodeT5: 29; Codex / davinci: 26.

Benchmarks (estudos): HumanEval (e variantes): 75; MBPP (e variantes): 48; APPS: 13; CoderEval: 12; CodeNet / Avatar / transcoder: 12; Defects4J: 11; LeetCode: 11; LiveCodeBench: 10; CodeContests: 10; BigCodeBench: 9; estudos sem nenhum desses: 170.

Linguagens (estudos): Python: 131; Java: 60; C++: 33; C: 17; JavaScript: 15; Go: 13; C#: 9; nao_informado: 8; Rust: 7; PHP: 6.

Sem comparador: 29; com técnica só classificada (sem número): 53; sem nenhuma comparação extraída: 15.

## Mecanismos (técnicas focais; estudos distintos)

| tarefa | estudos | instrucao | contexto | restricoes | exemplos | decomposicao | feedback | raciocinio | amostragem | multiagente | otimizacao_prompt | outro |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| geracao | 222 | 35 | 79 | 68 | 71 | 71 | 66 | 58 | 22 | 26 | 13 | 19 |
| depuracao | 59 | 11 | 34 | 16 | 24 | 18 | 19 | 18 | 8 | 6 | 2 | 4 |
| traducao | 25 | 1 | 4 | 6 | 8 | 9 | 7 | 4 | 2 | 3 | 2 | 2 |
| refatoracao | 19 | 2 | 5 | 3 | 8 | 6 | 5 | 4 | 1 | 1 | 0 | 0 |

(mecanismos acrescentados pela técnica focal ao prompt base; a tabela 06 traz o pacote completo)

## Contrafactual das técnicas focais (técnicas, não estudos)

Total: pacote: 347; ingrediente: 204; contraste_pareado: 3; cumulativo: 13; nenhum: 101.

Componentes (ingredientes registrados das técnicas focais): pacote: 14; ingrediente: 310; contraste_pareado: 9; cumulativo: 28; nenhum: 304.

Estudos (técnica focal ou componente; um estudo pode ter vários tipos): geracao: 222 estudos, pacote 141, ingrediente ou pareado 132, cumulativo 17, só nenhum 39; depuracao: 59 estudos, pacote 46, ingrediente ou pareado 38, cumulativo 12, só nenhum 2; traducao: 25 estudos, pacote 17, ingrediente ou pareado 12, cumulativo 6, só nenhum 3; refatoracao: 19 estudos, pacote 12, ingrediente ou pareado 9, cumulativo 1, só nenhum 4; todas: 302 estudos, pacote 202, ingrediente ou pareado 180, cumulativo 31, só nenhum 45.

## Comparações extraídas (unidade: comparação)

Total: melhora: 476; igual: 26; piora: 138; sem_direcao: 94; descritiva: 19. «sem_direcao»: sem sentido definido ou sem dois números; «descritiva»: sem comparador.

Seleção: desempate_ordem: 246; cobertura: 466; principal_declarado: 41. Derivação: direta: 749; contraste_pareado: 4.

Só comparações principais declaradas: geracao: 22 melhora, 0 igual, 0 piora; depuracao: 7 melhora, 0 igual, 0 piora; traducao: 4 melhora, 0 igual, 0 piora; refatoracao: 4 melhora, 0 igual, 0 piora.

Os autores escolhem a comparação principal, e estudos com resultado favorável tendem a ser publicados; a proporção de melhoras não estima efeito.

## Qualidade (estudos; julgamento por IA)

| critério | atende | parcial | nao_atende | nao_informado |
|---|---|---|---|---|
| objetivo | 298 | 4 | 0 | 0 |
| procedimento | 19 | 283 | 0 | 0 |
| comparador | 98 | 187 | 17 | 0 |
| metricas | 5 | 295 | 2 | 0 |
| ameacas | 78 | 196 | 0 | 28 |
| reprodutibilidade | 5 | 295 | 2 | 0 |
| contaminacao | 15 | 118 | 2 | 167 |

## Riscos e mitigações (estudos distintos)

| tarefa | estudos | correcao_funcional | seguranca | alucinacao | contaminacao | nao_determinismo | custo | manutenibilidade | outro | com mitigação | mitigação avaliada |
|---|---|---|---|---|---|---|---|---|---|---|---|
| geracao | 222 | 210 | 61 | 63 | 89 | 78 | 109 | 29 | 180 | 219 | 103 |
| depuracao | 59 | 56 | 14 | 20 | 30 | 24 | 30 | 6 | 51 | 58 | 24 |
| traducao | 25 | 25 | 5 | 5 | 11 | 11 | 10 | 2 | 20 | 25 | 11 |
| refatoracao | 19 | 17 | 6 | 9 | 6 | 10 | 6 | 8 | 15 | 19 | 7 |
| todas | 302 | 288 | 78 | 90 | 128 | 111 | 144 | 39 | 248 | 298 | 133 |

## Outros

Estudos com componente fora do escopo de prompting: 274 (outro: 432; decodificacao: 200; selecao_modelo: 165; ajuste_fino: 108; orcamento: 80; embeddings_aprendidos: 6).

Estudos com registro de heterogeneidade (busca dirigida): 302; registros: 3215.
