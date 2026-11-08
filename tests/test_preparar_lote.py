import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'scripts'))

from preparar_lote import indicio, local_publicado, publicado_openalex


class LocalPublicado(unittest.TestCase):
    def test_repositorio_de_preprints_nao_conta(self):
        self.assertEqual(local_publicado({'venue': 'arXiv.org', 'journal': {'name': 'ArXiv'},
                                          'externalIds': {'DOI': '10.48550/arXiv.2401.00001'}}), '')

    def test_evento_conta(self):
        self.assertEqual(local_publicado({'venue': 'Empirical Software Engineering'}),
                         'Empirical Software Engineering')

    def test_doi_de_editora_conta(self):
        self.assertEqual(local_publicado({'venue': 'arXiv.org', 'externalIds': {'DOI': '10.1145/1'}}),
                         'doi:10.1145/1')

    def test_sem_resposta(self):
        self.assertEqual(local_publicado(None), '')


class PublicadoOpenAlex(unittest.TestCase):
    def test_periodico_conta(self):
        obra = {'doi': 'https://doi.org/10.48550/arxiv.2401.00001',
                'locations': [{'source': {'type': 'repository', 'display_name': 'arXiv'}},
                              {'source': {'type': 'journal', 'display_name': 'TOSEM'}}]}
        self.assertEqual(publicado_openalex(obra), '2401.00001')

    def test_doi_da_editora_com_arxiv_no_local(self):
        obra = {'doi': 'https://doi.org/10.1145/1',
                'locations': [{'landing_page_url': 'https://arxiv.org/abs/2401.00001',
                               'source': {'type': 'repository', 'display_name': 'arXiv'}},
                              {'source': {'type': 'conference', 'display_name': 'ICSE'}}]}
        self.assertEqual(publicado_openalex(obra), '2401.00001')

    def test_so_repositorio_nao_conta(self):
        obra = {'doi': 'https://doi.org/10.48550/arxiv.2401.00001',
                'locations': [{'source': {'type': 'repository', 'display_name': 'arXiv'}}]}
        self.assertEqual(publicado_openalex(obra), '')


class Indicio(unittest.TestCase):
    def registro(self, base, doi='', arxiv=''):
        return {'busca_id': base, 'doi': doi, 'arxiv': arxiv}

    def test_registro_em_base_com_revisao(self):
        self.assertEqual(indicio([self.registro('B1', arxiv='1'), self.registro('B3')], set(), {}), 'base')

    def test_metadado_do_arxiv(self):
        self.assertEqual(indicio([self.registro('B1', arxiv='1')], {'1'}, {}), 'arxiv')

    def test_semantic_scholar(self):
        self.assertEqual(indicio([self.registro('B1', arxiv='1')], set(), {'1': {'venue': 'ICSE'}}),
                         'semantic_scholar')

    def test_so_arxiv_sem_local(self):
        self.assertEqual(indicio([self.registro('B1', arxiv='1')], set(), {'1': {'venue': 'arXiv.org'}}), '')


if __name__ == '__main__':
    unittest.main()
