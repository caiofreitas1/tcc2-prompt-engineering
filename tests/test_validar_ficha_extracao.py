"""Testes do validador da ficha ex-v2.2 com dados sintéticos (D106)."""
import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('validar', ROOT / 'scripts/validar_ficha_extracao.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

BASE = {
    'ficha': {
        'tarefas': ['geracao'],
        'tecnicas': [{'nome_original': 'tecnica sintetica', 'mecanismos': ['instrucao'],
                      'mecanismos_acrescentados': ['instrucao'], 'papel': 'focal',
                      'avaliada_isoladamente': 'sim', 'tipo_contrafactual': 'pacote'}],
        'sem_comparador': 'nao',
    },
    'extracoes': [{'tarefa': 'geracao', 'mecanismos': ['instrucao'],
                   'mecanismos_acrescentados': ['instrucao'], 'sentido': 'maior_melhor',
                   'unidade': 'percentual', 'selecao': 'principal_declarado',
                   'derivacao': 'direta', 'conferido_pdf': 'sim', 'comparador': 'base sintetica',
                   'resultado': {'baseline': 40, 'intervencao': 50}}],
    'qualidade': [{'criterio': c, 'julgamento': 'atende'} for c in mod.CRITERIOS],
    'leitura': 'completa',
}


def com(**campos):
    d = copy.deepcopy(BASE)
    d['extracoes'][0].update(campos)
    return d


class VocabularioD106(unittest.TestCase):
    def test_base_valida(self):
        self.assertEqual(mod.validar(copy.deepcopy(BASE)), [])

    def test_unidades_novas(self):
        for u in ('energia', 'temperatura', 'nao_informado'):
            self.assertEqual(mod.validar(com(unidade=u)), [], u)

    def test_unidade_nula_ou_livre_continua_invalida(self):
        for u in (None, 'mWh', 'outro'):
            self.assertTrue(mod.validar(com(unidade=u)), u)

    def test_sentido_nao_informado_aceito(self):
        self.assertEqual(mod.validar(com(sentido='nao_informado')), [])

    def test_sentido_nulo_continua_invalido(self):
        self.assertTrue(mod.validar(com(sentido=None)))


class VariacaoD106(unittest.TestCase):
    def test_classifica_com_sentido_definido(self):
        self.assertEqual(mod.variacao(com()['extracoes'][0]), 'melhora')
        self.assertEqual(mod.variacao(com(sentido='menor_melhor')['extracoes'][0]), 'piora')

    def test_sem_sentido_definido_nao_classifica(self):
        self.assertIsNone(mod.variacao(com(sentido='nao_informado')['extracoes'][0]))

    def test_sem_valor_numerico_nao_classifica(self):
        e = com(resultado={'baseline': None, 'intervencao': 3})['extracoes'][0]
        self.assertIsNone(mod.variacao(e))


if __name__ == '__main__':
    unittest.main()
