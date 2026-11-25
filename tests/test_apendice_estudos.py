"""Barreiras do apêndice de estudos incluídos (D135): o arquivo versionado corresponde aos dados e o
identificador da publicação só substitui o do arXiv quando há registro em dados/publicacoes.csv."""
import csv
import re
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / 'scripts'))
import gerar_apendice_estudos as g  # noqa: E402


def ler(caminho):
    with open(RAIZ / caminho, encoding='utf-8', newline='') as fh:
        return list(csv.DictReader(fh))


class ApendiceEstudos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.texto, cls.total, cls.sem_ficha, cls.publicados = g.montar()
        cls.estudos = {r['id']: r for r in ler('dados/estudos.csv')}
        cls.pub = ler('dados/publicacoes.csv')

    def test_arquivo_versionado_corresponde_aos_dados(self):
        self.assertEqual((RAIZ / 'monografia/capitulos/08-apendice-estudos.tex').read_text(encoding='utf-8'), self.texto,
                         'apêndice desatualizado: execute python3 scripts/gerar_apendice_estudos.py')

    def test_publicacoes_cobrem_so_os_estudos_do_arxiv_no_corpus(self):
        do_arxiv = {i for i, r in self.estudos.items() if r['corpus'] == 'definitivo' and r['identificador'].startswith('arXiv')}
        self.assertEqual({p['estudo_id'] for p in self.pub}, do_arxiv)
        self.assertEqual(len(self.pub), len(do_arxiv))
        for p in self.pub:
            self.assertEqual('arXiv:' + p['arxiv'], self.estudos[p['estudo_id']]['identificador'])

    def test_cada_linha_tem_tipo_fonte_e_responsavel(self):
        for p in self.pub:
            self.assertIn(p['tipo'], ('doi', 'url', 'nao_localizada'), p['estudo_id'])
            self.assertTrue(p['fonte'] and p['responsavel'] and p['data'], p['estudo_id'])
            self.assertIn(p['natureza'], ('ia', 'humano'))
            if p['tipo'] == 'doi':
                self.assertRegex(p['identificador'], r'^10\.\d{4,9}/\S+$')
                self.assertFalse(p['identificador'].lower().startswith('10.48550'), 'DOI do próprio arXiv não é publicação')
            elif p['tipo'] == 'url':
                self.assertRegex(p['identificador'], r'^https://')
                self.assertNotIn('arxiv.org', p['identificador'])
            else:
                self.assertEqual((p['identificador'], p['local'], p['ano']), ('', '', ''))
            if p['tipo'] != 'nao_localizada':
                self.assertTrue(p['local'] and p['ano'], p['estudo_id'])

    def test_apendice_lista_todos_os_estudos_uma_vez(self):
        ids = re.findall(r'\\item\[(S\d+)', self.texto)
        definitivos = [i for i, r in self.estudos.items() if r['corpus'] == 'definitivo']
        self.assertEqual(sorted(ids), sorted(definitivos))
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(self.total, len(definitivos))

    def test_arxiv_permanece_onde_nao_ha_publicacao(self):
        sem = sorted(p['arxiv'] for p in self.pub if p['tipo'] == 'nao_localizada')
        self.assertEqual(sorted(re.findall(r'\\texttt\{arXiv:([\d.]+)\}', self.texto)), sem)
        marcados = set(re.findall(r'\\item\[(S\d+)(?:\$\^\\dagger\$)?\$\^\\ast\$\]', self.texto))
        self.assertEqual(marcados, {p['estudo_id'] for p in self.pub if p['tipo'] != 'nao_localizada'})
        self.assertEqual(self.publicados, len(marcados))


if __name__ == '__main__':
    unittest.main()
