"""Barreiras do site «Prompt em Código» (D131): o arquivo publicado corresponde às fontes,
preserva as contagens da síntese e não leva trechos dos artigos nem caminhos locais."""
import csv
import json
import re
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / 'scripts'))
import gerar_site as g  # noqa: E402


class GerarSite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dados = g.montar()
        cls.texto = g.serializar(cls.dados)
        cls.linhas = {l['id']: l for l in cls.dados['linhas']}

    def grupos(self, cenario_id):
        c = next(c for c in self.dados['cenarios'] if c['id'] == cenario_id)
        cond = g.condicoes_do_cenario(c)
        saida = {'aplicavel': [], 'falta': [], 'lacuna': []}
        for l in self.dados['linhas']:
            if l['tarefa'] in (c['tarefa'], 'todas'):
                saida[g.classificar(l, cond)].append(l['id'])
        return saida

    def test_arquivo_versionado_corresponde_as_fontes(self):
        self.assertEqual((RAIZ / 'site/dados.json').read_text(encoding='utf-8'), self.texto,
                         'site/dados.json desatualizado: execute python3 scripts/gerar_site.py')

    def test_contagens_e_identidade(self):
        d = self.dados
        self.assertEqual(len(d['linhas']), 31)
        self.assertEqual(len(d['cenarios']), 8)
        self.assertEqual(len(d['comparacoes']), 805)
        self.assertEqual(len({c['id'] for c in d['comparacoes']}), 805)
        self.assertEqual(len(d['estudos']), 332)
        self.assertFalse({'E1', 'E2'} & {c['id'] for c in d['comparacoes']})
        self.assertTrue(all(c['estudo'] in {s['id'] for s in d['estudos']} for c in d['comparacoes']))

    def test_linhas_na_ordem_e_com_o_texto_da_tabela(self):
        with open(RAIZ / 'evidencias/sinteses/tabela-apoio-v2.csv', encoding='utf-8', newline='') as fh:
            tabela = list(csv.DictReader(fh))
        self.assertEqual([l['id'] for l in self.dados['linhas']], [r['id'] for r in tabela])
        for r in tabela:
            l = self.linhas[r['id']]
            for campo_site, campo_csv in (('evidencia', 'evidencia'), ('indicacao', 'indicacao'),
                                          ('ressalvas', 'ressalvas'), ('forca', 'forca'),
                                          ('condicao', 'condicao_verificacao')):
                self.assertEqual(l[campo_site], r[campo_csv])

    def test_direcoes_iguais_as_da_sintese(self):
        self.assertEqual(self.dados['meta']['direcoes'],
                         {'melhora': 516, 'piora': 145, 'igual': 28, 'sem_direcao': 91, 'descritiva': 25})

    def test_matriz_confere_com_a_tabela_09(self):
        with open(RAIZ / 'evidencias/sinteses/tabelas/09-direcao-comparacoes.csv', encoding='utf-8', newline='') as fh:
            esperado = {(r['tarefa'], r['mecanismo_acrescentado']): int(r['comparacoes']) for r in csv.DictReader(fh)}
        obtido = {}
        for c in self.dados['comparacoes']:
            for m in (c['acrescentados'] or ['(nenhum acrescentado)']):
                obtido[(c['tarefa'], m)] = obtido.get((c['tarefa'], m), 0) + 1
        self.assertEqual(obtido, esperado)
        self.assertEqual(obtido[('geracao', 'contexto')], 181)
        self.assertEqual(obtido[('refatoracao', 'contexto')], 12)

    def test_referencias_das_linhas_tem_registro(self):
        for l in self.dados['linhas']:
            for r in l['comparacoes'] + l['estudos']:
                self.assertTrue(r['registrada'], f'{l["id"]}: {r["id"]} sem registro')
        self.assertIn('S1-C1', [r['id'] for r in self.linhas['G7']['comparacoes']])
        # ID de estudo sozinho não vira comparação
        self.assertEqual([r['id'] for r in self.linhas['T5']['estudos']], ['S1220', 'S1803', 'S1836'])
        self.assertEqual(self.linhas['T5']['comparacoes'], [])
        self.assertIn('S556', [r['id'] for r in self.linhas['G14']['estudos']])

    def test_cada_linha_cai_em_um_unico_grupo_na_ordem_da_tabela(self):
        ordem = [l['id'] for l in self.dados['linhas']]
        for c in self.dados['cenarios']:
            gr = self.grupos(c['id'])
            todos = gr['aplicavel'] + gr['falta'] + gr['lacuna']
            esperado = [l['id'] for l in self.dados['linhas'] if l['tarefa'] in (c['tarefa'], 'todas')]
            self.assertEqual(sorted(todos, key=ordem.index), esperado)
            self.assertEqual(len(todos), len(set(todos)))
            for lista in gr.values():
                self.assertEqual(lista, sorted(lista, key=ordem.index))
            self.assertIn('G13', gr['lacuna'])

    def test_cenarios_do_design(self):
        g1 = self.grupos('G1')
        self.assertEqual((len(g1['aplicavel']), len(g1['falta']), len(g1['lacuna'])), (8, 3, 3))
        d2 = self.grupos('D2')
        self.assertIn('D1', d2['falta'])
        self.assertIn('D2', d2['aplicavel'])
        self.assertIn('D7', d2['lacuna'])
        t2 = self.grupos('T2')
        self.assertIn('T1', t2['falta'])
        self.assertTrue({'T2', 'T5'} <= set(t2['lacuna']))
        r2 = self.grupos('R2')
        self.assertIn('R2', r2['aplicavel'])
        self.assertIn('R5', r2['lacuna'])

    def test_regra_de_recursos(self):
        regra = g.analisar_regra('testes+varias | executor+varias')
        self.assertEqual(g.faltas(regra, {'testes'}), [['varias']])
        self.assertEqual(g.faltas(regra, {'testes', 'varias'}), [])
        self.assertEqual(g.faltas(regra, set()), [['testes', 'varias'], ['executor', 'varias']])
        self.assertEqual(g.faltas([], set()), [])
        with self.assertRaises(ValueError):
            g.analisar_regra('recurso_inexistente')

    def test_comparacao_de_referencia(self):
        c = next(c for c in self.dados['comparacoes'] if c['id'] == 'S1-C1')
        self.assertEqual((c['base'], c['intervencao'], c['direcao']), (48.1, 60.3, 'melhora'))
        self.assertEqual((c['benchmark'], c['modelo'], c['metrica']), ('HumanEval', 'code-davinci-002', 'Pass@1'))
        self.assertEqual(c['revisao_humana'], 'pendente')

    def test_sem_trechos_citados_nem_caminhos_locais(self):
        for proibido in g.PROIBIDOS:
            self.assertNotIn(f'"{proibido}":', self.texto)
        self.assertNotIn('fontes/artigos', self.texto)
        self.assertNotIn('fontes/textos', self.texto)
        self.assertNotIn('/Users/', self.texto)
        self.assertIsNone(re.search(r'\.pdf\b', self.texto, flags=re.I))
        campos_comparacao = set().union(*(c.keys() for c in self.dados['comparacoes']))
        self.assertFalse(campos_comparacao & set(g.PROIBIDOS))

    def test_conferencia_humana_nao_e_ampliada(self):
        m = self.dados['meta']
        self.assertEqual(m['estudos_revisados'], 67)
        self.assertEqual(m['estudos_revisados_por_modalidade'], {'declaracao_autor': 56, 'formulario': 11})
        self.assertEqual(m['comparacoes_revisadas'],
                         sum(1 for c in self.dados['comparacoes'] if c['revisao_humana'] == 'confirmada'))
        self.assertEqual(m['data_corte'], '2026-09-07')

    def test_links_das_fontes(self):
        s1 = next(s for s in self.dados['estudos'] if s['id'] == 'S1')
        self.assertEqual(s1['url'], 'https://arxiv.org/abs/2303.06689v5')
        self.assertEqual(g.url_fonte('doi:10.1145/1', 'nao_conferido'), 'https://doi.org/10.1145/1')
        self.assertIsNone(g.url_fonte('nao_informado', ''))

    def test_site_nao_calcula_media_nem_ranking(self):
        js = (RAIZ / 'site/app.js').read_text(encoding='utf-8')
        # A lista do Guia segue a ordem do CSV: o único sort do script é por número de ID.
        self.assertEqual(len(re.findall(r'\.sort\(', js)), 2)
        self.assertIsNone(re.search(r'reduce\([^)]*\+', js))


if __name__ == '__main__':
    unittest.main()
